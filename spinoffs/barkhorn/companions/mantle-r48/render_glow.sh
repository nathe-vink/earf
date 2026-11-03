#!/bin/sh
# The light up through the acrylic (2026-11-03): Strata Float v3 with its deck edge-lit from a groove in its underside.
# The same camera as 2026-11-01's a-dusk-ember-2423 (the dusk shot): night with the light on, day with it off, in stock
# Ember 2423, and a Poison 2092 night. The strip at its physical output, about 300 W/m2 off its 5 mm face (4 W/m
# electrical, about 1.5 W/m radiant), not set by eye.
cd "$(dirname "$0")"
OUT=../../../../renders/2026-11-03/barkhorn/mantle-r48
mkdir -p $OUT
C="--model out-strata-v3 --edge-frost 0.35 --base-tint smoke-2074 --scale 0.75 --samples 80 --exposure -2.0 --paper #7A7570 --tint-mode custom"
r() { n=$1; shift; python3.11 scene.py dusk "$@" --out $OUT/$n.png $C > /tmp/mantle-r48-$n.log 2>&1; echo "$n $(grep -c ^wrote /tmp/mantle-r48-$n.log)"; }
NIGHT="--strip 300 --strip-color 1.0 0.55 0.25 --ambient 0.03"
r a-night-ember-2423 --colour ember-2423 $NIGHT
r a-day-ember-2423 --colour ember-2423 --day --strip 0
r a-night-poison-2092 --colour poison-2092 $NIGHT
