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

## B-001 GL quadrature (n=32/64) reaching the Polymath15 barrier point
tried: 2026-08-21, tick 39
failed: degree-difference (n=32 vs n=64) at the barrier point X0=6e10+83951.5+0.2i, t=0.2 gives
  rel radius 0.227 (vs 4.3e-39 at the verified reference z=35+10i); the integrand cos(z*u)
  oscillates with period ~1e-10 in u and GL n=32/64 (node spacing ~0.03) aliases it. Pointwise
  GL quadrature does NOT reach the barrier.
evidence: evidence/2026-08-21-ht-barrier/machine-run.txt
closed by: machine output (VERDICT: barrier rel radius LARGE; AFE needed)

## B-002 tick-53 TloopSinglematv2 binary: Arb/FLINT header layout mismatch (segfault)
tried: 2026-08-21, ticks 53-66 (14 ticks)
failed: binary compiled tick 53 with Arb 2.23 headers ($PFX/include) against the FLINT 3.2
  library (libflint.so.20) segfaulted at 0x168 in the first rectangle (ASan: SEGV on 0x168).
  Root cause (machine-verified by nm + header diff, tick 67): 2018 dbn code expects
  acb_poly_struct = { coeffs; length; alloc; } (Arb 2.23 layout, length@8); FLINT 3.2 is
  { coeffs; alloc; length; } (length@16). Inline acb_poly_zero() compiled from Arb headers
  zeros offset 8, which the FLINT library reads as alloc=0 -> acb_poly_fit_length does
  realloc on a 0-sized pointer. Fix: compile with FLINT 3.2 headers (include-v2) + forced
  -include arb_mat.h (FLINT acb headers don't pull in arb_mat.h). BarrierLocationAssistant
  (claim #6) never hit the bug because it calls no acb_poly functions.
evidence: evidence/2026-08-21-tloop/README.md "The segfault bug" section; nm -D of both
  binaries (both import arb_mat_init; only the ACB header set differs); ASan log in
  tracks/b-dbn/dbn/dbn_upper_bound/arb/ (TloopSinglematv2_asan, tick 64)
closed by: tick 67 — FLINT-header build runs clean, output matches the paper exactly
  (claim #7 NUMERIC).

## A-003 tick-79 (timer/local) PNG-as-text crash
tried: 2026-08-22 04:35-04:41 UTC, timer tick 79 (local model)
failed: tick crashed with "'utf-8' codec can't decode byte 0x89 in position 387:
  invalid start byte" (0x89 = PNG signature) after 11 steps; the lagarias re-run it
  launched completed (run_N1e6_rerun.txt, 04:41:37Z) but the tick died before committing.
  Same class as A-002 (binary-as-text): the local model's file reader hit an image —
  almost certainly a dbn-repo PNG (tradeoff.png / meshbarrier images) read as text.
fix/avoid: treat *.png/*.jpg in the dbn repo as binaries; use `file` before read.
  Residual state (ticks.log line, rerun file) committed by frontier tick 79.

## A-004 manual session vs timer tick concurrency (no shared lock)
tried: 2026-08-22 08:22-09:00 CEST, manual session (track A, 3-lemma refinement)
  ran CONCURRENT with timer tick 83 (local, 08:36-09:00 CEST, same track A plan).
failed: both sessions worked the same pnt file and the same claim: tick 83 created
  claim #12 (08:54); the manual session's `promote.sh add` became #13 (08:56) and its
  `promote.sh promote 12 FORMAL` (aimed at its own claim) promoted tick 83's #12 via
  the shared checker (PASS — same state). Tick 83's auto-commit 62937f8 swept the
  manual session's in-flight evidence/ + claims.db into git mid-work.
  Root cause: flock in tools/tick.sh guards tick.sh invocations against each other,
  but a manual session takes no lock at all.
fix/avoid: manual sessions must `flock ledger/.tick.lock` (or a second lock that
  tick.sh also checks) for the whole session; or park manual work in a branch.
  Residual: claim #13 is a duplicate of #12 — GARDEN merge #13 into #12 (keep #12
  FORMAL; #13's extra detail already in evidence/2026-08-22-pnt-ik-api/README.md).

## A-005 nohup background launch inside riemann-tick.service cgroup
tried: 2026-08-23, tick 152 (launch) / tick 153 (diagnosis + relaunch)
failed: full zero scan (pid 743305) launched with plain `nohup python3 ... &`
  inside the tick's bash tool call died at 20:13:06 CEST = the moment
  riemann-tick.service (Type=oneshot, default KillMode=control-group) finished
  tick 152 — systemd killed all remaining processes in the service cgroup.
  nohup only ignores SIGHUP, not the cgroup-wide SIGTERM/SIGKILL. Lost 1.5%
  of the run (t=1501). The S(t) scan survived 5+ ticks because tick 147
  launched it as a transient systemd unit (st-scan-1e5.service, own cgroup) —
  the "tick-138 lesson" was applied there but forgotten for the zero scan.
fix/avoid: launch long background jobs with
  `systemd-run --user --unit=<name>.service bash -c 'cd /home/niklas/riemann && ...'`
  (own cgroup, survives tick service end). Zero scan relaunched tick 153 as
  zero-scan-1e5.service (pid 745484), verified active + progressing.
evidence: logs/2026-08-23.tick.log (TICK 153, journalctl verbatim);
  evidence/2026-08-23-zero-scan/full.stderr (dead run's 3 lines + new run's
  lines, append-only)
closed by: machine output — systemctl --user status zero-scan-1e5.service
  "Active: active (running)" + new progress line in full.stderr
