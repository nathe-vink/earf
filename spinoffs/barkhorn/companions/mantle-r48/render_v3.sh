#!/bin/sh
# Round 48, third pass: the arm's and the cartridge's details, the vinyl's sheen; a stylus close-up; Outcrop in Ember.
cd "$(dirname "$0")"
OUT=../../../../renders/2026-10-31/barkhorn/mantle-r48
COMMON="--scale 0.75 --samples 80 --exposure -2.0 --paper #7A7570"
for n in ${@:-hero-v3 detail-v3 ember}; do
  case $n in
    hero-v3)   python3.11 scene.py hero --model out-outcrop --out $OUT/outcrop-$n.png $COMMON ;;
    detail-v3) python3.11 scene.py macro-stylus --model out-outcrop --out $OUT/outcrop-$n.png $COMMON ;;
    ember)     python3.11 scene.py hero --model out-outcrop --colour ember --out $OUT/outcrop-$n.png $COMMON ;;
  esac > /tmp/mantle-r48-$n.log 2>&1
  echo "outcrop-$n $(grep -c wrote /tmp/mantle-r48-$n.log)"
done
