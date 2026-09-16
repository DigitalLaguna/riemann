#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
python3 downstream.py | tee machine-run-check.txt
grep -q "CHECK downstream effective constant: PASS" machine-run-check.txt
echo "CHECK downstream: PASS"
