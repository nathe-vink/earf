#!/bin/sh
# Strata Float v2 (the coordinator's head-to-head notes): the Ice studio frame at the same rig, the dusk Ember-custom frame.
cd "$(dirname "$0")"
OUT=../../../../renders/2026-10-31/barkhorn/mantle-r48
COMMON="--scale 0.75 --samples 80 --exposure -2.0 --paper #7A7570"
[ "$1" = r2 ] || python3.11 scene.py hero --model out-strata-v2 --colour ice-custom --tint-mode custom --out $OUT/strata-v2-ice-custom.png $COMMON > /tmp/mantle-r48-sv2a.log 2>&1; echo "ice $(grep -c wrote /tmp/mantle-r48-sv2a.log)"
[ "$1" = r2 ] || python3.11 scene.py dusk --model out-strata-v2 --colour ember-custom --tint-mode custom --strip 40 --out $OUT/strata-v2-dusk-ember-custom.png $COMMON > /tmp/mantle-r48-sv2b.log 2>&1; echo "dusk $(grep -c wrote /tmp/mantle-r48-sv2b.log)"
# round 2 (the critics: a raking strip and a low card on the front edges; the base's glow 1.5 stops down and redder)
if [ "$1" = r2 ]; then
python3.11 scene.py hero --model out-strata-v2 --colour ice-custom --tint-mode custom --front-strip 300 --out $OUT/strata-v2-ice-custom-r2.png $COMMON > /tmp/mantle-r48-sv2c.log 2>&1; echo "ice-r2 $(grep -c wrote /tmp/mantle-r48-sv2c.log)"
python3.11 scene.py dusk --model out-strata-v2 --colour ember-custom --tint-mode custom --strip 14 --strip-color 1.0 0.40 0.16 --front-strip 40 --out $OUT/strata-v2-dusk-ember-custom-r2.png $COMMON > /tmp/mantle-r48-sv2d.log 2>&1; echo "dusk-r2 $(grep -c wrote /tmp/mantle-r48-sv2d.log)"
fi
