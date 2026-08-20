# DEAD_ENDS
Append only. Never trim. Read before every new attempt.
Format:

## <TRACK>-<NNN> <what was tried>
tried: <date>, ticks <range>
failed: <why, one line>
evidence: <path>
closed by: <card or machine output that killed it>

## A-001 gate.py location paren must START with a keyword
tried: 2026-08-20, ticks 1, 4
failed: gate.py's main_result check regex requires the location parenthetical to
  BEGIN with one of Theorem/Lemma/Proposition/Corollary/Section/sec/Abstract/
  post/para/p./page/eq/README/CONTRIBUTING/PULL_REQUEST/wiki/fetched — "(article
  body, p. 342; ...)" FAILS, "(p. 342, article body, ...)" PASSES.
evidence: logs/2026-08-20.tick.log (ticks 1 and 4); tools/gate.py card_ok()
closed by: reordering the parentheticals in conrey-2003, odlyzko-zeros,
  broughan-2017, lean-zulip-pnt; gate.py status shows 21/21 PASS.

## A-002 reading a binary (PNG) as utf-8 text
tried: 2026-08-20, tick 3 (16:40)
failed: agent_tick.py tick 3 crashed at step 4 with "'utf-8' codec can't decode
  byte 0x89 in position 967: invalid start byte" — 0x89 is the second byte of the
  PNG signature, so a downloaded image was fed to a text read.
evidence: logs/ticks.log line 3 (tick 3 ERROR entry)
closed by: keep binaries (pdf/png) out of `read`; use pdftotext/pdftoppm first.
