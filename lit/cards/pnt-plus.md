bibkey:      pnt-plus
title:       PrimeNumberTheoremAnd (PNT+) repository, blueprint, contributing guide, open issue list
authors:     Alex Kontorovich et al.
year:        2026
url:         https://github.com/AlexKontorovich/PrimeNumberTheoremAnd
local:       tracks/a-lean/pnt (local clone); lit/pdf/pnt-open-issues.json (issue list fetched 2026-08-20)
fetched:     2026-08-20
main_result: "The objective of this project is to formalize in Lean the Prime Number Theorem (with classical error term), as well as related results such as the Prime Number Theorem in Arithmetic Progressions." (README.md, para 4)
             "We are also hosting the Integrated Explicit Analytic Number Theory network." (README.md, para 4)
             "Tasks are posted as GitHub issues and can be found in the `Unclaimed` column of the project dashboard." (CONTRIBUTING.md, section 1)
             "To claim a task, comment the single word `claim` on the relevant GitHub issue." (CONTRIBUTING.md, section 2)
             "Contributions produced with the aid of an AI coding assistant (Cursor, Claude Code, Copilot, Codex, aider, ...) are welcome and follow the same rules as any other contribution" — disclosure required in PR body; CI auto-applies the `ai` umbrella label (PULL_REQUEST_STYLE.md, section 13)
constants:   no numeric constants; fixes the workflow: claim word on issue, `propose #N` / `awaiting-review` comments, one PR per issue from a fork branch; 39 open issues as of fetch (list in lit/pdf/pnt-open-issues.json), several already carry `claude,ai` labels
supersedes:  none; the host repository for the ANT network formalization half
superseded:  none known as of 2026-08-20
relevance:   Track A working repository. First action per design doc: get the blueprint building locally (done, tick 1), join the Lean Zulip, close one XS issue. Task size labels XS-XL live in the project dashboard (GitHub project 1), not in issue bodies; pick XS/S tasks from the dashboard. AI disclosure: one line in PR body, e.g. "Made with ..." + Co-Authored-By footer.
