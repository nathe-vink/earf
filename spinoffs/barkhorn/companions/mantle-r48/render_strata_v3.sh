#!/bin/sh
# Strata Float v3 (the coordinator's detail notes): the Ice studio frame and the dusk Ember-custom frame, the same rig as v2's r2.
cd "$(dirname "$0")"
OUT=../../../../renders/2026-10-31/barkhorn/mantle-r48
COMMON="--scale 0.75 --samples 80 --exposure -2.0 --paper #7A7570"
python3.11 scene.py hero --model out-strata-v3 --colour ice-custom --tint-mode custom --front-strip 300 --out $OUT/strata-v3-ice-custom.png $COMMON > /tmp/mantle-r48-sv3a.log 2>&1; echo "ice $(grep -c wrote /tmp/mantle-r48-sv3a.log)"
# at dusk the smoked base passes little of the strip's light through its edge, so the strip runs at 600 and most of it
# falls from the open slot onto the shelf: the deck floats on a pool of light
python3.11 scene.py dusk --model out-strata-v3 --colour ember-custom --tint-mode custom --strip 600 --strip-color 1.0 0.55 0.25 --front-strip 40 --out $OUT/strata-v3-dusk-ember-custom.png $COMMON > /tmp/mantle-r48-sv3b.log 2>&1; echo "dusk $(grep -c wrote /tmp/mantle-r48-sv3b.log)"
