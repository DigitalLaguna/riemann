bibkey:      pnt-plus
title:       PNT+ repository and blueprint (PrimeNumberTheoremAnd)
authors:     Alex Kontorovich (repo owner); PNT+ project contributors
year:        2026
url:         https://github.com/AlexKontorovich/PrimeNumberTheoremAnd
local:       tracks/a-lean/pnt (local clone); open-issue snapshot: lit/text/pnt-plus-issues.json
fetched:     2026-08-20
main_result: "To claim a task, comment the single word `claim` on the relevant GitHub issue." (Section "2. Claiming a Task", CONTRIBUTING.md)
             "After submitting the PR, comment `propose #PR_NUMBER` on the original issue. This links your PR to the task, and the task will move to the `In Progress` column on the dashboard." (Section "4. Submitting a Pull Request", CONTRIBUTING.md)
             "Contributions produced with the aid of an AI coding assistant (Cursor, Claude Code, Copilot, Codex, aider, …) are welcome and follow the same rules as any other contribution — but they should also: 1. **Disclose the tool** in the PR body (e.g. \"Made with Cursor\", or the auto-generated footer produced by these tools)." (Section 13 "AI-assisted contributions", PULL_REQUEST_STYLE.md)
constants:   none fixed in the guides; open-issue snapshot 2026-08-20: 39 open issues, e.g. #1694 [TMEEMT/RS] RS_prime.theorem_c (sum 1/p > log log x for x > 1), #1692 RS_prime.theorem_d, #1687 RS_prime.theorem_b (pi(x) > x/log x for x >= 17), #1429 [FKS2] Upper bound on E_pi (Corollary 24), #722 [FKS2] Further bounds on E_pi (Corollary 23), #1257 [BKLNW] Verify Table 11
supersedes:  none; the PNT+ project is the host of the IEANTN network (tao-2026-ant)
superseded:  none known as of 2026-08-20
relevance:   Track A. Workflow: claim via `claim` comment, PR from fork branch (not main), `propose #N`, `awaiting-review`. AI disclosure: one line "Made with <tool>" in PR body; CI auto-labels. New Lean files must import Architect, be added to PrimeNumberTheoremAnd.lean and blueprint.tex. The 39-issue snapshot is the task queue; XS/S candidates to be screened next tick.
