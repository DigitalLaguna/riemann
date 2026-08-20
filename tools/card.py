#!/usr/bin/env python3
"""card.py — create and validate literature cards.

Usage:
  card.py new   <bibkey> <title> [url]   write a skeleton card with required fields
  card.py check <bibkey>                 exit 0 iff the card has all required fields

Required fields (a card written from memory is a fabrication, even when accurate):
  bibkey, title, authors, year, url, local, fetched,
  main_result  — the main result quoted VERBATIM with equation or page number
  constants    — every explicit constant the paper fixes, and its value
  supersedes, superseded, relevance
"""
import re
import sys
from datetime import date
from pathlib import Path

CARDS = Path(__file__).resolve().parent.parent / "lit" / "cards"

TEMPLATE = """\
bibkey:      {bibkey}
title:       {title}
authors:     ?
year:        ?
url:         {url}
local:       lit/pdf/{bibkey}.pdf
fetched:     {fetched}
main_result: "<verbatim quote>" (Theorem/Section, p. ?)
constants:   ?
supersedes:  ?
superseded:  ?
relevance:   ?
"""

FIELDS = ["bibkey", "title", "authors", "year", "url", "local", "fetched",
          "main_result", "constants", "supersedes", "superseded", "relevance"]


def main() -> int:
    args = sys.argv[1:]
    if len(args) >= 2 and args[0] == "new":
        bibkey, title = args[1], args[2]
        url = args[3] if len(args) > 3 else "?"
        p = CARDS / f"{bibkey}.md"
        if p.exists():
            print(f"exists: {p}")
            return 1
        p.write_text(TEMPLATE.format(bibkey=bibkey, title=title, url=url,
                                     fetched=date.today().isoformat()))
        print(f"wrote {p}")
        return 0
    if len(args) == 2 and args[0] == "check":
        bibkey = args[1]
        p = CARDS / f"{bibkey}.md"
        if not p.exists():
            print(f"missing: {p}")
            return 1
        t = p.read_text()
        bad = []
        for f in FIELDS:
            m = re.search(rf"^{f}:\s*(.*)$", t, re.M)
            if not m or not m.group(1).strip() or m.group(1).strip() == "?":
                bad.append(f)
        if bad:
            print(f"INCOMPLETE ({', '.join(bad)})")
            return 1
        if '"' not in re.search(r"^main_result:.*$", t, re.M).group(0):
            print("INCOMPLETE (main_result has no verbatim quote)")
            return 1
        print("OK")
        return 0
    print(__doc__)
    return 2


if __name__ == "__main__":
    sys.exit(main())
