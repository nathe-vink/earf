#!/bin/bash
# fixed-9 crops of fixed9-fix (every fixed-9 change): the far region, the Mantle, the near bay; 512 samples (the full
# frame's), with masks
cd /home/user/earf
F=renders/2026-11-21/barkhorn/b1-test
export LAMPS_ROOT=/home/user/lamps-ecb1
for job in "far 0.15 0.0 0.62 0.8" "mantle 0.5 0.72 0.85 1.0" "near 0.6 0.0 0.96 0.85"; do
  set -- $job; t0=$(date +%s)
  python3 studio/engine/render.py $F/fixed9-fix.json --out $F/crop9-$1.png --crop $2 $3 $4 $5 --samples 512 --masks > /tmp/claude-0/crop9-$1.log 2>&1; rc=$?
  echo "$1 exit $rc $(( ($(date +%s)-t0)/60 )) min $(grep -m1 'equipment in frame' /tmp/claude-0/crop9-$1.log)"
  grep -v "INFO\|Timer" /tmp/claude-0/crop9-$1.log > $F/crop9-$1.log
  rm -f "${F:?}"/*.raw.png
done
