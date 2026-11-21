#!/bin/bash
# fixed-8 P5/P6: the lower cone's green smear (1095,495-1140,530) and the far batt band's blotches (470,400-540,435),
# small crops of fixed8-p3m at 1024 samples, to set against fixed-7's 256 (what stays is real)
cd /home/user/earf
F=renders/2026-11-21/barkhorn/b1-test
export LAMPS_ROOT=/home/user/lamps-ecb1
for job in "p5 0.66 0.52 0.74 0.62" "p6 0.28 0.42 0.36 0.5"; do
  set -- $job; t0=$(date +%s)
  python3 studio/engine/render.py $F/fixed8-p3m.json --out $F/samp8-$1.png --crop $2 $3 $4 $5 --samples 1024 > /tmp/claude-0/samp8-$1.log 2>&1
  echo "$1 exit $? $(( ($(date +%s)-t0)/60 )) min"
  rm -f "${F:?}"/*.raw.png
done
