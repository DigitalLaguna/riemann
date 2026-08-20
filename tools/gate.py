#!/usr/bin/env python3
"""gate.py — check lit/cards/ against lit/reading/<track>.md and flip the gate line.

Usage:
  gate.py check [track]   check one track or all; print PASS/FAIL per seed
  gate.py flip  <track>   run the check and update the `gate:` line in the reading file
  gate.py status          one line per track: A CLOSED (2/4 carded) etc.

The gate flips ONLY via this script. The agent may not hand-edit the `gate:`
line: a card is valid only if the document was fetched and quoted (checked
here), so a bare assertion of readiness is not a gate.

Seed lines in lit/reading/<track>.md have the form:
  - bibkey: title — source
A seed passes iff lit/cards/<bibkey>.md exists and contains:
  - a matching `bibkey:` line
  - a `main_result:` line holding a quoted verbatim result ("...")
  - a `fetched:` date (YYYY-MM-DD)
  - a `local:` line (fetched document or local clone path)
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
READING = ROOT / "lit" / "reading"
CARDS = ROOT / "lit" / "cards"

TRACKS = ["a", "b", "c", "d", "e"]


def seeds_of(track: str) -> list[str]:
    text = (READING / f"{track}.md").read_text()
    return re.findall(r"^-\s+([a-z0-9][a-z0-9-]*):", text, re.M)


def card_ok(bibkey: str) -> tuple[bool, str]:
    p = CARDS / f"{bibkey}.md"
    if not p.exists():
        return False, "missing card"
    t = p.read_text()
    problems = []
    if not re.search(rf"^bibkey:\s*{re.escape(bibkey)}\s*$", t, re.M):
        problems.append("bibkey mismatch")
    if not re.search(r'^main_result:.*"[^"]{10,}".*\((?:Theorem|Lemma|Proposition|Corollary|Section|sec|Abstract|post|para|p\.|page|eq|README|CONTRIBUTING|PULL_REQUEST|wiki|fetched)[^)]*\)', t, re.M):
        problems.append("main_result lacks verbatim quote with location")
    if not re.search(r"^fetched:\s*\d{4}-\d{2}-\d{2}\s*$", t, re.M):
        problems.append("no fetched date")
    if not re.search(r"^local:\s*\S", t, re.M):
        problems.append("no local path")
    return (not problems, ", ".join(problems))


def check(track: str) -> tuple[bool, int, int]:
    seeds = seeds_of(track)
    ok = 0
    for b in seeds:
        good, why = card_ok(b)
        print(f"  {b}: {'PASS' if good else 'FAIL (' + why + ')'}")
        ok += good
    return ok == len(seeds) and bool(seeds), ok, len(seeds)


def main() -> int:
    args = sys.argv[1:]
    if not args:
        print(__doc__)
        return 2
    cmd = args[0]
    if cmd == "check":
        tracks = args[1:] or TRACKS
        rc = 0
        for t in tracks:
            good, _, _ = check(t)
            rc |= 0 if good else 1
        return rc
    if cmd == "flip":
        t = args[1]
        p = READING / f"{t}.md"
        good, _, _ = check(t)
        status = "OPEN" if good else "CLOSED"
        text = p.read_text().replace("gate: CLOSED", f"gate: {status}", 1) \
                       .replace("gate: OPEN", f"gate: {status}", 1)
        p.write_text(text)
        print(f"track {t.upper()} gate: {status}")
        return 0 if good else 1
    if cmd == "status":
        for t in TRACKS:
            p = READING / f"{t}.md"
            line = [l for l in p.read_text().splitlines() if l.startswith("gate:")][0]
            _, ok, n = check(t)
            print(f"track {t.upper()} {line.split(':',1)[1].strip()} ({ok}/{n} seeds carded)")
        return 0
    return 2


if __name__ == "__main__":
    sys.exit(main())
