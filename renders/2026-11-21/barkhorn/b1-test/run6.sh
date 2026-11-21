#!/bin/bash
# B1 fixed-2 at 1600 x 900 with masks (the front head at 10 W/m2, the ceiling panel at 8); committed and pushed
cd /home/user/earf
F=renders/2026-11-21/barkhorn/b1-test
export LAMPS_ROOT=/home/user/lamps-ecb1
t0=$(date +%s)
python3 studio/engine/render.py $F/fixed6.json --out $F/fixed6.png --masks > /tmp/claude-0/b1-fixed6.log 2>&1
echo "fixed6 exit $? $(( ($(date +%s)-t0)/60 )) min $(grep -m1 'equipment in frame' /tmp/claude-0/b1-fixed6.log)"
rm -f $F/*.raw.png
git add $F/fixed6.* $F/run2.sh && git commit -q -m "B1 test: fixed-6 (every light real: t7 with the frontal softbox at 40 on both bays; not a final)

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01CsZ9sPVytkpnrfV4BgTgfB" && git push -q -u origin r33-speaker-horn
