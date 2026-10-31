#!/bin/sh
# Strata Float v2 (the coordinator's head-to-head notes): the Ice studio frame at the same rig, the dusk Ember-custom frame.
cd "$(dirname "$0")"
OUT=../../../../renders/2026-10-31/barkhorn/mantle-r48
COMMON="--scale 0.75 --samples 80 --exposure -2.0 --paper #7A7570"
python3.11 scene.py hero --model out-strata-v2 --colour ice-custom --tint-mode custom --out $OUT/strata-v2-ice-custom.png $COMMON > /tmp/mantle-r48-sv2a.log 2>&1; echo "ice $(grep -c wrote /tmp/mantle-r48-sv2a.log)"
python3.11 scene.py dusk --model out-strata-v2 --colour ember-custom --tint-mode custom --strip 40 --out $OUT/strata-v2-dusk-ember-custom.png $COMMON > /tmp/mantle-r48-sv2b.log 2>&1; echo "dusk $(grep -c wrote /tmp/mantle-r48-sv2b.log)"
