#!/bin/bash
# fixed-8 crop tests: the far speaker, the record wall and the print (x 0.15-0.62, y 0-0.8: at 240, 0), 128 samples
cd /home/user/earf
F=renders/2026-11-21/barkhorn/b1-test
export LAMPS_ROOT=/home/user/lamps-ecb1
for v in "$@"; do
  t0=$(date +%s)
  python3 studio/engine/render.py $F/fixed8-$v.json --out $F/cropfar8-$v.png --crop 0.15 0.0 0.62 0.8 --samples 128 > /tmp/claude-0/cropfar8-$v.log 2>&1
  echo "$v exit $? $(( ($(date +%s)-t0)/60 )) min"
  rm -f "${F:?}"/*.raw.png
done
