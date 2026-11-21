#!/bin/bash
# B1 fixed-2 at 1600 x 900 with masks (the front head at 10 W/m2, the ceiling panel at 8); committed and pushed
cd /home/user/earf
F=renders/2026-11-21/barkhorn/b1-test
export LAMPS_ROOT=/home/user/lamps-ecb1
t0=$(date +%s)
python3 studio/engine/render.py $F/fixed7.json --out $F/fixed7.png --masks > /tmp/claude-0/b1-fixed7.log 2>&1
echo "fixed7 exit $? $(( ($(date +%s)-t0)/60 )) min $(grep -m1 'equipment in frame' /tmp/claude-0/b1-fixed7.log)"
rm -f "${F:?}"/*.raw.png
git add $F/fixed7.* $F/run2.sh && git commit -q -m "B1 test: fixed-7 (fixed-7d: skirted frontal softboxes at 20, the ceiling diffuser at 6, the wall heads at 0.35; not a final)

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01CsZ9sPVytkpnrfV4BgTgfB" && git push -q -u origin r33-speaker-horn
