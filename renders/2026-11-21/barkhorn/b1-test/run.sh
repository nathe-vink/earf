#!/bin/bash
# B1: live, then fixed, at 1600 x 900 with masks; each committed and pushed as it lands
cd /home/user/earf
F=renders/2026-11-21/barkhorn/b1-test
export LAMPS_ROOT=/home/user/lamps-ecb1   # the 14 Nov frame recorded no lamps commit; live and fixed both at the current pin, ecb1650c24
for v in live fixed; do
  [ -f $F/$v.equipment.txt ] && { echo "$v done before"; continue; }
  t0=$(date +%s)
  python3 studio/engine/render.py $F/$v.json --out $F/$v.png --masks > /tmp/claude-0/b1-$v.log 2>&1
  echo "$v exit $? $(( ($(date +%s)-t0)/60 )) min $(grep -m1 'equipment in frame' /tmp/claude-0/b1-$v.log) $(grep -m1 -o 'NO GLASS SHADOWS: [0-9]* materials' /tmp/claude-0/b1-$v.log) $(grep -c 'WATER GLASS:' /tmp/claude-0/b1-$v.log) glasses"
  rm -f $F/*.raw.png
  git add $F/$v.* && git commit -q -m "B1 test: $v (bar-backbar at half size; not a final)

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01CsZ9sPVytkpnrfV4BgTgfB" && git push -q -u origin r33-speaker-horn
done
