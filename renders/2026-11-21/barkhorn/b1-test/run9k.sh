#!/bin/bash
# fixed-9: the ceiling's top-left corner (x 0.14-0.2, y 0-0.045: at 224, 0), 512 samples
cd /home/user/earf
F=renders/2026-11-21/barkhorn/b1-test
export LAMPS_ROOT=/home/user/lamps-ecb1
for v in "$@"; do
  t0=$(date +%s)
  python3 studio/engine/render.py $F/fixed9-$v.json --out $F/crop9k-$v.png --crop 0.14 0.0 0.2 0.045 --samples 512 > /tmp/claude-0/crop9k-$v.log 2>&1; rc=$?
  echo "$v exit $rc $(( ($(date +%s)-t0)/60 )) min"
  rm -f "${F:?}"/*.raw.png
done
