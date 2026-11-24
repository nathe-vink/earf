#!/bin/bash
# B1 fixed-9 at 1600 x 900, 512 samples, with masks; its log kept beside it; committed and pushed
cd /home/user/earf
F=renders/2026-11-21/barkhorn/b1-test
export LAMPS_ROOT=/home/user/lamps-ecb1
t0=$(date +%s)
python3 studio/engine/render.py $F/fixed9.json --out $F/fixed9.png --masks > /tmp/claude-0/b1-fixed9.log 2>&1; rc=$?; grep -v "INFO\|Timer" /tmp/claude-0/b1-fixed9.log > $F/fixed9.log
echo "fixed9 exit $rc $(( ($(date +%s)-t0)/60 )) min $(grep -m1 'equipment in frame' /tmp/claude-0/b1-fixed9.log)"
rm -f "${F:?}"/*.raw.png
git add $F/fixed9.* $F/run9.sh && git commit -q -m "B1 test: fixed-9 (fixed-8 with track-bay0 at x 6.05, the far softbox 30 cm back, mantle-front +0.3 m, track-bay1 +10 cm, camera true on the lamps)

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01CsZ9sPVytkpnrfV4BgTgfB" && git push -q -u origin r33-speaker-horn
