#!/usr/bin/env bash
# promote.sh — the ONLY writer to the claim ledger's status column.
# The model may call it; the model may not edit claims.db by hand.
#
# Usage:
#   promote.sh add "<statement>" <track>                 new NOTE claim; prints id
#   promote.sh list [status]                             table of claims
#   promote.sh promote <id> <NUMERIC|FORMAL|PUBLISHED> <evidence_path>
#       Promotion runs the checker: <evidence_path>/check.sh must exit 0.
#       Order: NOTE < NUMERIC < FORMAL < PUBLISHED; any upward move allowed
#       provided the target's checker passes. The script writes the row.
#   promote.sh verdict <id> "<adversary verdict text>"    record Adversary pass
#
# Evidence convention: <evidence_path> is a directory under evidence/ containing
# the run's outputs plus a check.sh that re-verifies the claim and exits 0/1.
#   NUMERIC    check.sh re-runs the Arb ball-arithmetic computation, asserts the bound
#   FORMAL     check.sh runs the Lean compile (lake build) of the commit the claim rests on
#   PUBLISHED  check.sh verifies the upstream merge / arXiv record
set -euo pipefail
cd "$(dirname "$0")/.."
export RIEMANN_DB=ledger/claims.db
python3 - "$@" <<'EOF'
import os, sqlite3, subprocess, sys
from datetime import datetime, timezone

db = sqlite3.connect(os.environ["RIEMANN_DB"])
db.executescript("""
CREATE TABLE IF NOT EXISTS CLAIM (
  id INTEGER PRIMARY KEY,
  statement TEXT NOT NULL,
  track TEXT NOT NULL,
  status TEXT NOT NULL DEFAULT 'NOTE'
    CHECK (status IN ('NOTE','NUMERIC','FORMAL','PUBLISHED')),
  evidence_path TEXT,
  created TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%SZ','now')),
  promoted_by TEXT,
  adversary_verdict TEXT
);""")
args = sys.argv[1:]
cmd = args[0] if args else ""

def rows(where=None, val=None):
    q = "SELECT id,status,track,statement,evidence_path FROM CLAIM"
    if where:
        q += f" WHERE {where} ORDER BY id"
    else:
        q += " ORDER BY id"
    return db.execute(q, (val,) if val is not None else ()).fetchall()

if cmd == "add":
    r = db.execute("INSERT INTO CLAIM (statement, track) VALUES (?, ?)",
                   (args[1], args[2]))
    db.commit()
    print(f"NOTE #{r.lastrowid}: {args[1]}")
elif cmd == "list":
    for r in rows("status = ?" if len(args) > 1 else None,
                  args[1] if len(args) > 1 else None):
        print(f"#{r[0]} {r[1]:8} [{r[2]}] {r[3][:80]} {r[4] or ''}")
elif cmd == "promote":
    cid, target, ev = int(args[1]), args[2], args[3]
    cur = db.execute("SELECT status FROM CLAIM WHERE id=?", (cid,)).fetchone()
    if not cur:
        sys.exit(f"no claim #{cid}")
    cur = cur[0]
    order = ["NOTE", "NUMERIC", "FORMAL", "PUBLISHED"]
    if order.index(target) <= order.index(cur):
        sys.exit(f"not an upward move: {cur} -> {target}")
    checker = os.path.join(ev, "check.sh")
    if not os.path.isfile(checker):
        sys.exit(f"no checker at {checker}")
    print(f"running checker: {checker}")
    ok = subprocess.run(["bash", checker], cwd=os.path.dirname(os.path.dirname(checker))
                        if False else ".", ).returncode == 0
    if ok:
        now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        db.execute("UPDATE CLAIM SET status=?, evidence_path=?, promoted_by=? WHERE id=?",
                   (target, ev, f"promote.sh {now}", cid))
        db.commit()
        print(f"promoted #{cid}: {cur} -> {target}")
    else:
        sys.exit(f"checker failed; stays {cur}")
elif cmd == "verdict":
    db.execute("UPDATE CLAIM SET adversary_verdict=? WHERE id=?",
               (" ".join(args[2:]), int(args[1])))
    db.commit()
    print(f"verdict recorded for #{args[1]}")
elif cmd == "merge":
    # garden: mark a duplicate claim as merged into another; status column untouched
    cid, into = int(args[1]), int(args[2])
    cur = db.execute("SELECT statement,status FROM CLAIM WHERE id=?", (cid,)).fetchone()
    ref = db.execute("SELECT status FROM CLAIM WHERE id=?", (into,)).fetchone()
    if not cur or not ref:
        sys.exit("no such claim")
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    db.execute("UPDATE CLAIM SET statement=?, promoted_by=? WHERE id=?",
               (f"MERGED into #{into} ({now}): {cur[0]}", f"promote.sh merge {now}", cid))
    db.commit()
    print(f"merged #{cid} (was {cur[1]}) into #{into} ({ref[0]}); status of #{cid} unchanged")
else:
    sys.exit("usage: promote.sh add|list|promote|verdict|merge ...")
EOF
