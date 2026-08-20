#!/usr/bin/env python3
"""agent_tick.py — one bounded tick of the Riemann research operator.

Drives the local operator model (llama-server, OpenAI-compatible) through
ONE tick of the 7-step loop defined in tools/prompt.md, using a single
`bash` tool. After the model stops, the script enforces repo discipline:
append the tick record to logs/ticks.log, and commit any dirty tree so a
tick never ends with a dirty working copy.

Environment:
  RIEMANN_API_BASE   default http://localhost:8080/v1
  RIEMANN_MODEL      default: first model served
  RIEMANN_MAX_STEPS  default 25 bash calls per tick
  RIEMANN_TICK_BUDGET_SEC default 1200
"""
import json
import os
import subprocess
import sys
import time
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
API_BASE = os.environ.get("RIEMANN_API_BASE", "http://localhost:8080/v1")
MAX_STEPS = int(os.environ.get("RIEMANN_MAX_STEPS", "25"))
BUDGET = int(os.environ.get("RIEMANN_TICK_BUDGET_SEC", "1200"))


def api_key() -> str:
    for line in Path.home().joinpath(".llama/api-keys.txt").read_text().splitlines():
        line = line.strip()
        if line and not line.startswith("#"):
            return line
    raise SystemExit("no API key in ~/.llama/api-keys.txt")


def first_model() -> str:
    req = urllib.request.Request(
        f"{API_BASE}/models", headers={"Authorization": f"Bearer {api_key()}"})
    with urllib.request.urlopen(req, timeout=10) as r:
        return json.load(r)["data"][0]["id"]


def chat(messages, model):
    body = json.dumps({
        "model": model,
        "messages": messages,
        "temperature": 0.3,
        "tools": [{
            "type": "function",
            "function": {
                "name": "bash",
                "description": "Run one bash command in the repo root /home/niklas/riemann. "
                               "One bounded step per command. Output is truncated to 8000 chars.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "command": {"type": "string"},
                        "timeout": {"type": "integer", "description": "seconds, default 600"}
                    },
                    "required": ["command"],
                },
            },
        }],
    }).encode()
    req = urllib.request.Request(
        f"{API_BASE}/chat/completions", data=body,
        headers={"Authorization": f"Bearer {api_key()}",
                 "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=BUDGET) as r:
        return json.load(r)["choices"][0]["message"]


def run_bash(command: str, timeout: int) -> str:
    try:
        p = subprocess.run(["bash", "-c", command], cwd=ROOT,
                           capture_output=True, text=True, timeout=timeout)
        out = (p.stdout or "") + ("\n[stderr]\n" + p.stderr if p.stderr else "")
        return f"exit {p.returncode}\n{out[-8000:]}"
    except subprocess.TimeoutExpired:
        return f"exit 124 (timeout after {timeout}s)"


def state_block() -> str:
    parts = []
    for f in ["HANDOFF.md", "DEAD_ENDS.md"]:
        p = ROOT / f
        parts.append(f"=== {f} ===\n{p.read_text() if p.exists() else '(missing)'}")
    try:
        import sqlite3
        db = sqlite3.connect(ROOT / "ledger/claims.db")
        rows = db.execute("SELECT id,status,track,statement FROM CLAIM ORDER BY id").fetchall()
        parts.append("=== ledger ===\n" +
                     "\n".join(f"#{r[0]} {r[1]} [{r[2]}] {r[3][:100]}" for r in rows)
                     or "=== ledger ===\n(empty)")
    except Exception as e:
        parts.append(f"=== ledger ===\n(unreadable: {e})")
    parts.append("=== gates ===\n" +
                 subprocess.run(["python3", "tools/gate.py", "status"], cwd=ROOT,
                                capture_output=True, text=True).stdout)
    ticks = (ROOT / "logs" / "ticks.log").read_text().splitlines() \
        if (ROOT / "logs" / "ticks.log").exists() else []
    parts.append("=== last ticks ===\n" + "\n".join(ticks[-5:]))
    return "\n\n".join(parts)


def main() -> int:
    t0 = time.time()
    started = datetime.now(timezone.utc)
    ticks_log = ROOT / "logs" / "ticks.log"
    tick_no = (len(ticks_log.read_text().splitlines()) + 1) if ticks_log.exists() else 1

    model = os.environ.get("RIEMANN_MODEL") or first_model()
    contract = (ROOT / "tools" / "prompt.md").read_text()
    system = contract + f"""

== TICK PROTOCOL (mechanical, this run) ==
This is tick {tick_no}. You have at most {MAX_STEPS} bash calls and {BUDGET // 60} minutes.
Your only tool is `bash`, run in the repo root. The current state of the repo:

{state_block()}

Follow the 7-step tick loop from your operating contract, in order.
Prefer commands that end with a machine saying yes or no.
Before finishing you MUST have: (a) appended this tick's attempt and the
machine's verbatim output to logs/<YYYY-MM-DD>.tick.log, and
(b) REWRITTEN HANDOFF.md to the fixed schema (under 80 lines), and
(c) committed with a 'track/verb: ...' message (or 'track/dead: ...'),
leaving the tree clean.
If you run out of steps, stop at a clean boundary and hand off honestly."""

    messages = [{"role": "system", "content": system},
                {"role": "user", "content": "Run tick " + str(tick_no) + "."}]
    steps = 0
    try:
        while steps < MAX_STEPS and time.time() - t0 < BUDGET:
            msg = chat(messages, model)
            messages.append(msg)
            tools = msg.get("tool_calls") or []
            if not tools:
                break
            for tc in tools:
                args = json.loads(tc["function"]["arguments"] or "{}")
                cmd = args.get("command", "")
                timeout = min(int(args.get("timeout", 600)), BUDGET)
                steps += 1
                res = run_bash(cmd, timeout)
                messages.append({"role": "tool", "tool_call_id": tc["id"],
                                 "content": res})
    except Exception as e:
        (ROOT / "logs" / "ticks.log").touch(exist_ok=True)
        with ticks_log.open("a") as f:
            f.write(f"{started.isoformat()} tick {tick_no} ERROR {e} steps={steps}\n")
        return 1

    # Deterministic enforcement: a tick never ends with a dirty tree.
    st = subprocess.run(["git", "status", "--porcelain"], cwd=ROOT,
                        capture_output=True, text=True).stdout.strip()
    if st:
        subprocess.run(["git", "add", "-A"], cwd=ROOT, check=True)
        msg = f"tick/auto: commit residual state after tick {tick_no} (see logs)"
        subprocess.run(["git", "commit", "-m", msg], cwd=ROOT, check=True)
    handoff = (ROOT / "HANDOFF.md").read_text().splitlines()
    next_action = ""
    for i, l in enumerate(handoff):
        if l.startswith("## Next action") and i + 1 < len(handoff):
            next_action = handoff[i + 1].strip()
            break
    with ticks_log.open("a") as f:
        f.write(f"{started.isoformat()} "
                f"tick {tick_no} model={model} steps={steps} "
                f"wall={int(time.time()-t0)}s next={next_action[:90]}\n")
    print(f"tick {tick_no} done: steps={steps} wall={int(time.time()-t0)}s next={next_action[:90]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
