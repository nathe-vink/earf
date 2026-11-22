#!/bin/bash
# fixed-9 Q1: the near crop (x 0.6-0.96, y 0-0.85: at 960, 0) of fixed-9 with track-bay1 back where fixed-8 had it,
# 512 samples with masks (as crop9-near)
cd /home/user/earf
F=renders/2026-11-21/barkhorn/b1-test
export LAMPS_ROOT=/home/user/lamps-ecb1
t0=$(date +%s)
python3 studio/engine/render.py $F/fixed9-q1bay1.json --out $F/crop9-q1bay1.png --crop 0.6 0.0 0.96 0.85 --samples 512 --masks > /tmp/claude-0/crop9-q1bay1.log 2>&1; rc=$?
echo "q1bay1 exit $rc $(( ($(date +%s)-t0)/60 )) min $(grep -m1 'equipment in frame' /tmp/claude-0/crop9-q1bay1.log)"
rm -f "${F:?}"/*.raw.png
