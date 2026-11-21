#!/bin/bash
# the two quarter tests, then the olive-disc crops; each frame committed and pushed as it lands
cd /home/user/earf
export TROPOS_BASE=A LAMPS_ROOT=/home/user/lamps-ecb1
for job in "c-move/m025.json c-move/m025.png" "c-move/m035.json c-move/m035.png" "c-disc/e1-book.json c-disc/e1-book.png --crop 0.3 0.45 1.0 0.85 --samples 128" "c-disc/e2-glass.json c-disc/e2-glass.png --crop 0.3 0.45 1.0 0.85 --samples 128"; do
  set -- $job; F=renders/2026-11-21/barkhorn; in=$F/$1; out=$F/$2; shift 2
  [ -f $out ] && { echo "$out done before"; continue; }
  t0=$(date +%s)
  python3 studio/engine/render.py $in --out $out "$@" > /tmp/claude-0/$(basename $out .png).log 2>&1
  echo "$out exit $? $(( ($(date +%s)-t0)/60 )) min $(grep -m1 -o 'LAMPS PIN: [^ ]* [0-9a-f]\{10\}' /tmp/claude-0/$(basename $out .png).log)"
  rm -f "${F:?}"/c-*/*.raw.png
  git add ${out%.png}.* && git commit -q -m "C test: $(basename $out) (not a final)

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01CsZ9sPVytkpnrfV4BgTgfB" && git push -q -u origin r33-speaker-horn
done
