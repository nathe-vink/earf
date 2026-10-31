#!/bin/bash
# The finals, one after another, 1800 x 1200 (Lithos 1200 x 1800), 128 samples. Logs to renders/log.txt.
# Usage: run_all.sh [shot ...]   (default: all seven)
cd "$(dirname "$0")"
shots="${@:-moho lithos ionos cairn bedrock relief meridian}"
for s in $shots; do
  python3.11 render_objects.py --shot $s --samples 128 >> renders/log.txt 2>&1 && echo "done $s $(date +%T)" >> renders/log.txt
done
echo ALLDONE >> renders/log.txt
