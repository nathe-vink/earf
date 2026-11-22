#!/bin/bash
# fixed-9: the far region (x 0.15-0.62, y 0-0.8: at 240, 0) of fixed9-fixflag (the far softbox's top flag 0.7 m), 512 samples, masks
cd /home/user/earf
F=renders/2026-11-21/barkhorn/b1-test
export LAMPS_ROOT=/home/user/lamps-ecb1
t0=$(date +%s)
python3 studio/engine/render.py $F/fixed9-fixflag.json --out $F/crop9-far3.png --crop 0.15 0.0 0.62 0.8 --samples 512 --masks > /tmp/claude-0/crop9-far3.log 2>&1; rc=$?
echo "far3 exit $rc $(( ($(date +%s)-t0)/60 )) min $(grep -m1 'equipment in frame' /tmp/claude-0/crop9-far3.log)"
rm -f "${F:?}"/*.raw.png
