#!/bin/bash
# fixed-9 Q2 crops: the ceiling streak (x 411-451, y 71-85) in a crop x 0.24-0.30, y 0.05-0.12 (at 384, 45), 512 samples
cd /home/user/earf
F=renders/2026-11-21/barkhorn/b1-test
export LAMPS_ROOT=/home/user/lamps-ecb1
for v in "$@"; do
  t0=$(date +%s)
  python3 studio/engine/render.py $F/fixed9-$v.json --out $F/crop9q2-$v.png --crop 0.24 0.05 0.30 0.12 --samples 512 > /tmp/claude-0/crop9q2-$v.log 2>&1; rc=$?
  echo "$v exit $rc $(( ($(date +%s)-t0)/60 )) min"
  rm -f "${F:?}"/*.raw.png
done
