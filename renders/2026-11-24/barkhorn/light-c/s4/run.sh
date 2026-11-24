#!/bin/bash
# S4 test renders: the four fronts with real flags (masks, the audit), then Dust's convergence crop at 96 and 768 spp;
# each committed and pushed. Logs (filtered) kept beside the frames.
cd /home/user/earf
D=renders/2026-11-24/barkhorn/light-c/s4
B=$(git rev-parse --abbrev-ref HEAD)
CROP="0.44 0.36 0.80 0.944"
for n in "$@"; do
  [ -f $D/$n.png ] && { echo "$n done before"; continue; }
  t0=$(date +%s)
  case $n in conv-*) extra="--crop $CROP";; *) extra="--masks";; esac
  python3 studio/engine/render.py $D/$n.json --out $D/$n.png $extra > /tmp/claude-0/s4-$n.log 2>&1; rc=$?
  grep -v "INFO\|Timer\|^Fra:\|| Sample\|Rendering\|Updating\|Loading" /tmp/claude-0/s4-$n.log > $D/$n.log
  echo "$n exit $rc $(( ($(date +%s)-t0)/60 )) min $(grep -m1 'equipment in frame' $D/$n.log) $(grep -o 'NO GLASS SHADOWS: [0-9]* materials' $D/$n.log)"
  rm -f "${D:?}"/*.raw.png
  [ $rc -eq 0 ] || { tail -5 $D/$n.log; continue; }
  git add $D/$n.* $D/run.sh $D/gen.py && git commit -q -m "Light C, S4 test: $n

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01CsZ9sPVytkpnrfV4BgTgfB" && git push -q -u origin "$B"
done
