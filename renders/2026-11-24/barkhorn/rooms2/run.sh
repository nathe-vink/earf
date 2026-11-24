#!/bin/bash
# the new living-room proofs (rooms2.py): 960 x 640, 48 spp, with masks (the audit); each committed and pushed
cd /home/user/earf
O=renders/2026-11-24/barkhorn/rooms2
export TROPOS_BASE=A LAMPS_ROOT=/home/user/lamps-ecb1
for n in "$@"; do
  [ -f $O/$n.equipment.txt ] && { echo "$n done before"; continue; }
  t0=$(date +%s)
  python3 studio/engine/render.py $O/$n.json --out $O/$n.png --masks > /tmp/claude-0/rooms2-$n.log 2>&1; rc=$?
  echo "$n exit $rc $(( ($(date +%s)-t0)/60 )) min $(grep -m1 'equipment in frame' /tmp/claude-0/rooms2-$n.log)"
  rm -f "${O:?}"/*.raw.png
  [ $rc -eq 0 ] || { tail -5 /tmp/claude-0/rooms2-$n.log; continue; }
  git add $O/$n.* && git commit -q -m "Living-room proofs: $n (a proof, not a final)

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01CsZ9sPVytkpnrfV4BgTgfB" && git push -q -u origin r33-speaker-horn
done
