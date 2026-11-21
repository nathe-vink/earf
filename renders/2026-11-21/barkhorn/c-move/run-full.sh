#!/bin/bash
# C's full frame from m035: 1600x2000, 256 samples, masks; committed and pushed when it lands
cd /home/user/earf
export TROPOS_BASE=A LAMPS_ROOT=/home/user/lamps-ecb1
F=renders/2026-11-21/barkhorn/c-move; t0=$(date +%s)
python3 studio/engine/render.py $F/c-full.json --out $F/c-full.png --masks > /tmp/claude-0/c-full.log 2>&1
echo "c-full exit $? $(( ($(date +%s)-t0)/60 )) min $(grep -m1 -o 'LAMPS PIN: [^ ]* [0-9a-f]\{10\}' /tmp/claude-0/c-full.log) $(grep -m1 'equipment in frame' /tmp/claude-0/c-full.log)"
rm -f $F/*.raw.png
git add $F/c-full.* $F/run-full.sh && git commit -q -m "C full frame from m035 (group and camera -0.35 m off the window's line, book +6 cm)

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01CsZ9sPVytkpnrfV4BgTgfB" && git push -q -u origin r33-speaker-horn
