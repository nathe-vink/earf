#!/bin/bash
# renders what is not yet rendered (a frame is done when its .equipment.txt is in), commits and pushes each one
cd /home/user/earf
F=renders/2026-11-21/barkhorn/s1-test
export TROPOS_BASE=A
for v in ember-a ember-b ember-c fog-a fog-b fog-c; do
  [ -f $F/$v.equipment.txt ] && { echo "$v done before"; continue; }
  t0=$(date +%s)
  python3 studio/engine/render.py $F/$v.json --out $F/$v.png --masks > /tmp/claude-0/s1-$v.log 2>&1
  echo "$v exit $? $(( ($(date +%s)-t0)/60 )) min $(grep -h 'in frame' $F/$v.equipment.txt 2>/dev/null | tr '\n' ' ') $(grep -o 'NO GLASS SHADOWS: [0-9]* materials' /tmp/claude-0/s1-$v.log)"
  rm -f "${F:?}"/*.raw.png
  git add $F/$v.* && git commit -q -m "S1 test: $v (the audit's test, not a final)

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01CsZ9sPVytkpnrfV4BgTgfB" && git push -q -u origin r33-speaker-horn
done
