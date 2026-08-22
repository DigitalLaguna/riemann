#!/usr/bin/env bash
# Re-run the arXiv height sweep and assert no document claims RH verified to >= 1e13.
set -uo pipefail
cd "$(dirname "$0")"
python3 fetch.py > /tmp/rhscan_recheck.txt 2>/dev/null || { echo "CHECK FAIL: fetch.py (network?)"; exit 1; }
python3 fetch2.py > /tmp/rhscan_recheck2.txt 2>/dev/null || { echo "CHECK FAIL: fetch2.py (network?)"; exit 1; }
cat /tmp/rhscan_recheck.txt /tmp/rhscan_recheck2.txt > /tmp/rhscan_all.txt
if grep -qEi "10\^13|10\^\{13\}|1e13|10,000,000,000,000" /tmp/rhscan_all.txt; then
  echo "CHECK FAIL: a 1e13-height claim appeared in the sweep:"
  grep -nEi "10\^13|10\^\{13\}|1e13|10,000,000,000,000" /tmp/rhscan_all.txt
  exit 1
fi
# sanity: the 3e12 record must still be present (else the sweep silently broke)
if ! grep -qEi "3\\\\cdot ?10\^\{?12\}?|3\*10\^12|3e12" /tmp/rhscan_all.txt; then
  echo "CHECK FAIL: 3e12 record (Platt-Trudgian) not found in sweep — sweep may have broken"
  exit 1
fi
echo "CHECK PASS: no RH-verified-to-1e13 source; record still Platt-Trudgian 3e12"
