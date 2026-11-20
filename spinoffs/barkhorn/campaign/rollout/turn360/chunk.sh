#!/bin/bash
# chunk.sh TINT FRAME...: render each missing frame of the turn (masks on), then copy and commit them
cd /home/user/earf
T=/tmp/claude-0/-home-user-earf/e9eacb03-86e9-502d-ab9f-ed75453cbf0d/scratchpad/turn
D=renders/2026-11-20/barkhorn/turn-proof
tint=$1; shift
for n in "$@"; do
  f=turn-$tint-$(printf %02d $n)
  [ -s $D/$f.png ] && { echo "$f already in"; continue; }
  t0=$(date +%s)
  python3 studio/engine/render.py $T/$f.json --out $T/$f.png --masks > $T/$f.log 2>&1
  echo "$f exit $? $(( ($(date +%s)-t0)/60 )) min $(grep -o 'equipment in frame.*' $T/$f.log)"
  for e in png shot.json mask.png mask.json equipment.txt; do cp $T/$f.$e $D/; done
done
rm -f "${T:?}"/*.raw.png
git add $D && git commit -q -m "Horn 360 on the house ground: $tint frames $* (1200 x 1080)

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01CsZ9sPVytkpnrfV4BgTgfB" && git push -q -u origin r33-speaker-horn && git log --oneline -1
