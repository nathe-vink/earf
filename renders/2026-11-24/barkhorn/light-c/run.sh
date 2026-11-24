#!/bin/bash
# Light model C renders: bash renders/2026-11-24/barkhorn/light-c/run.sh NAME [NAME ...]
#   NAME is a shot here without .json (front-ember, turn-ember-07, ...); a frame with its .equipment.txt is skipped,
#   so a run stopped by the 2-hour limit picks up where it left off. Each frame is rendered with masks (the audit),
#   committed and pushed to the current branch. Needs only the two speaker models (studio/setup.sh, then the cloud and
#   variants builds), no LAMPS_ROOT and no Mantle.
cd "$(git rev-parse --show-toplevel)"
O=renders/2026-11-24/barkhorn/light-c
B=$(git rev-parse --abbrev-ref HEAD)
for n in "$@"; do
  [ -f $O/$n.equipment.txt ] && { echo "$n done before"; continue; }
  t0=$(date +%s)
  python3 studio/engine/render.py $O/$n.json --out $O/$n.png --masks > /tmp/lightc-$n.log 2>&1; rc=$?
  echo "$n exit $rc $(( ($(date +%s)-t0)/60 )) min $(grep -m1 'equipment in frame' /tmp/lightc-$n.log) $(grep -o 'NO GLASS SHADOWS: [0-9]* materials' /tmp/lightc-$n.log)"
  rm -f "${O:?}"/*.raw.png
  [ $rc -eq 0 ] || continue
  git add $O/$n.* && git commit -q -m "Light model C: $n

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01CsZ9sPVytkpnrfV4BgTgfB" && git push -q -u origin "$B"
done
