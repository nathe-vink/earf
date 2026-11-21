#!/bin/bash
# fixed-8b test: the near crop (576 x 765 at 960, 0) of fixed8-mv2 (the near softbox moved off the cone), 256 samples, masks
cd /home/user/earf
F=renders/2026-11-21/barkhorn/b1-test
export LAMPS_ROOT=/home/user/lamps-ecb1
t0=$(date +%s)
python3 studio/engine/render.py $F/fixed8-mv2.json --out $F/crop8-mv2.png --crop 0.6 0.0 0.96 0.85 --samples 256 --masks > /tmp/claude-0/crop8-mv2.log 2>&1; rc=$?
echo "mv2 exit $rc $(( ($(date +%s)-t0)/60 )) min $(grep -m1 'equipment in frame' /tmp/claude-0/crop8-mv2.log)"
rm -f "${F:?}"/*.raw.png
