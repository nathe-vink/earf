#!/bin/sh
# The owner's darker stock tints (2026-11-01): both designs as last shown, in stock Ember 2423 and Poison 2092 (studio)
# and Ember at dusk; Strata Float v3's base in the line's Smoke, 2074 Dark Gray. Then one sheet per tint and light.
cd "$(dirname "$0")"
OUT=../../../../renders/2026-11-01/barkhorn/mantle-r48
mkdir -p $OUT
C="--scale 0.75 --samples 80 --exposure -2.0 --paper #7A7570 --tint-mode custom"
A="--model out-strata-v3 --edge-frost 0.35 --base-tint smoke-2074"
B="--model out-outcrop"
r() { n=$1; shift; python3.11 scene.py "$@" --out $OUT/$n.png $C > /tmp/mantle-r48-$n.log 2>&1; echo "$n $(grep -c wrote /tmp/mantle-r48-$n.log)"; }
r a-studio-ember-2423 hero $A --colour ember-2423
r b-studio-ember-2423 hero $B --colour ember-2423
r a-studio-poison-2092 hero $A --colour poison-2092
r b-studio-poison-2092 hero $B --colour poison-2092
r a-dusk-ember-2423 dusk $A --colour ember-2423 --strip 600 --strip-color 1.0 0.55 0.25
r b-dusk-ember-2423 dusk $B --colour ember-2423
sheets() {
for kt in "studio-ember-2423|studio, stock Ember 2423" "studio-poison-2092|studio, stock Poison 2092" "dusk-ember-2423|dusk, its light on, stock Ember 2423"; do
  k=${kt%%|*}; t=${kt#*|}
  convert $OUT/a-$k.png $OUT/b-$k.png +append -resize 2400x \
    -gravity north -background '#F4F1EC' -splice 0x70 -gravity northwest -font DejaVu-Sans -pointsize 30 -fill '#222' \
    -annotate +20+18 "A  Strata Float v3" -annotate +1220+18 "B  Outcrop" \
    -pointsize 24 -fill "#666" -annotate +1840+22 "$t" -quality 92 $OUT/sheet-$k.png
  echo sheet-$k
done
}
sheets
