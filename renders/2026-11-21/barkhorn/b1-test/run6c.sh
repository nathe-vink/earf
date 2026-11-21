#!/bin/bash
# fixed-6 crop tests: the near speaker, tall enough for the sill (x 0.6-0.96, y 0-0.85 of the frame: at 960, 0), 128 samples
cd /home/user/earf
F=renders/2026-11-21/barkhorn/b1-test
export LAMPS_ROOT=/home/user/lamps-ecb1
for v in "$@"; do
  t0=$(date +%s)
  python3 studio/engine/render.py $F/fixed6-$v.json --out $F/crop6-$v.png --crop 0.6 0.0 0.96 0.85 --samples 128 > /tmp/claude-0/crop6-$v.log 2>&1
  echo "$v exit $? $(( ($(date +%s)-t0)/60 )) min"
  rm -f $F/*.raw.png
done
