#!/bin/bash
cd /home/user/earf
F=renders/2026-11-21/barkhorn/c-disc
export TROPOS_BASE=A LAMPS_ROOT=/home/user/lamps-ecb1
for v in e1-book e2-glass; do
  [ -f $F/$v.png ] && continue
  python3 studio/engine/render.py $F/$v.json --out $F/$v.png --samples 128 --crop 0.3 0.45 1.0 0.85 > /tmp/claude-0/cd-$v.log 2>&1; echo "$v exit $?"
  grep -m1 "LAMPS PIN" /tmp/claude-0/cd-$v.log
done
rm -f "${F:?}"/*.raw.png
