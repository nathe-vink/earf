#!/bin/sh
# Round 48, second pass: the blind critics' notes applied (scene.py), the Core frames again as -v2.
cd "$(dirname "$0")"
OUT=../../../../renders/2026-10-31/barkhorn/mantle-r48
COMMON="--scale 0.75 --samples 80 --exposure -2.0 --paper #7A7570"
for n in ${@:-hero closed detail use}; do
  shot=$n; [ $n = detail ] && shot=macro
  python3.11 scene.py $shot --model out-core --out $OUT/core-$n-v2.png $COMMON > /tmp/mantle-r48-$n-v2.log 2>&1
  echo "core-$n-v2 $(grep -c wrote /tmp/mantle-r48-$n-v2.log)"
done
