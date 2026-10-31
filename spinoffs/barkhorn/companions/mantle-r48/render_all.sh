#!/bin/sh
# Round 48's final frames, one at a time (Cycles on all cores). About 15-25 minutes each at 1800 x 1200, 128 samples.
#   sh spinoffs/barkhorn/companions/mantle-r48/render_all.sh [names]
cd "$(dirname "$0")"
OUT=../../../../renders/2026-10-31/barkhorn/mantle-r48
mkdir -p $OUT
COMMON="--scale 0.75 --samples 80 --exposure -2.0 --paper #7A7570"
for n in ${@:-outcrop-hero outcrop-closed outcrop-detail outcrop-use strata-hero}; do
  case $n in
    outcrop-hero)   python3.11 scene.py hero   --model out-outcrop   --out $OUT/$n.png $COMMON ;;
    outcrop-closed) python3.11 scene.py closed --model out-outcrop   --out $OUT/$n.png $COMMON ;;
    outcrop-detail) python3.11 scene.py macro  --model out-outcrop   --out $OUT/$n.png $COMMON ;;
    outcrop-use)    python3.11 scene.py use    --model out-outcrop   --out $OUT/$n.png $COMMON ;;
    strata-hero) python3.11 scene.py hero   --model out-strata --out $OUT/$n.png $COMMON --strip 3 ;;
  esac > /tmp/mantle-r48-$n.log 2>&1
  echo "$n $(grep -c wrote /tmp/mantle-r48-$n.log)"
done
