#!/bin/bash
# Light model C with S4b (real flags) renders: bash renders/2026-11-24/barkhorn/light-c2/run.sh NAME [NAME ...]
#   NAME is a shot here without .json (front-ember, turn-ember-07, horn-back-ember, amp-ember). A frame with its
#   .equipment.txt is skipped, so a run stopped by the 2-hour limit picks up where it left off. Each frame is rendered
#   with masks (the audit); its log, filtered, is kept beside it as NAME.log (the NO GLASS SHADOWS line on file); the
#   frame, its masks and its log are committed and pushed to the current branch. Needs only the speaker models
#   (studio/setup.sh, then the cloud and variants builds): no LAMPS_ROOT, no Mantle.
cd "$(git rev-parse --show-toplevel)"
O=renders/2026-11-24/barkhorn/light-c2
B=$(git rev-parse --abbrev-ref HEAD)
for n in "$@"; do
  [ -f $O/$n.equipment.txt ] && { echo "$n done before"; continue; }
  t0=$(date +%s)
  python3 studio/engine/render.py $O/$n.json --out $O/$n.png --masks > /tmp/lightc2-$n.log 2>&1; rc=$?
  grep -v "INFO\|Timer\|^Fra:\|| Sample\|Rendering\|Updating\|Loading" /tmp/lightc2-$n.log > $O/$n.log
  echo "$n exit $rc $(( ($(date +%s)-t0)/60 )) min $(grep -m1 'equipment in frame' $O/$n.log) $(grep -o 'NO GLASS SHADOWS: [0-9]* materials' $O/$n.log)"
  rm -f "${O:?}"/*.raw.png
  [ $rc -eq 0 ] || { tail -5 $O/$n.log; continue; }
  git add $O/$n.* && git commit -q -m "Light model C (S4b): $n

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01CsZ9sPVytkpnrfV4BgTgfB"
  for i in 1 2 3 4; do git push -q -u origin "$B" && break; sleep $((i * 5)); done
done
