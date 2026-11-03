#!/bin/sh
# Round 2 of the light up through the acrylic (2026-11-03), the camera of 2026-11-01's a-dusk-ember-2423:
#  (a) v4, the lit deck (mantle_strata_v4.py): Ember night and day, Poison night;
#  (b) v3's edge-lit deck in a lighter custom Ember pour (about 40 % TT per 1/2 in), night and day, as a comparison.
# Night: the room at 0.3 % of the day's light and the camera a stop over the day's (it exposes for the glow, as a night
# photograph does); the guide's output from the strip's power (--core-glow 9 W/m2, scene.py core_material).
# (a)'s day: the room's light on the print, baked as the guide's glow is (--core-glow 20 in the skin's downward tint):
# Cycles cannot light a diffuse face sealed under glass in useful time. 20 puts the print in the range the albedos give
# (0.5-1.5 x the paper beside it); it is a judgment within that range, not a measurement.
cd "$(dirname "$0")"
OUT=../../../../renders/2026-11-03/barkhorn/mantle-r48
mkdir -p $OUT
C="--edge-frost 0.35 --base-tint smoke-2074 --scale 0.75 --samples 80 --paper #7A7570 --tint-mode custom"
r() { n=$1; shift; python3.11 scene.py dusk "$@" --out $OUT/$n.png $C > /tmp/mantle-r48-$n.log 2>&1; echo "$n $(grep -c ^wrote /tmp/mantle-r48-$n.log)"; }
NIGHT="--strip 300 --strip-color 1.0 0.55 0.25 --ambient 0.003 --exposure 0.0"
if [ -z "$1" ]; then
r a4-night-ember-2423 --model out-strata-v4 --colour ember-2423 $NIGHT --core-glow 9
r a4-day-ember-2423 --model out-strata-v4 --colour ember-2423 --day --strip 0 --core-glow 20 --strip-color 0.915 0.33 0.38 --exposure -2.0
r a4-night-poison-2092 --model out-strata-v4 --colour poison-2092 $NIGHT --core-glow 9
r b-night-ember-40 --model out-strata-v3 --colour ember-40 $NIGHT
r b-day-ember-40 --model out-strata-v3 --colour ember-40 --day --strip 0 --exposure -2.0
fi
# the coordinator's pass (07:39 UTC): (a)'s nights a stop down (-1.0), so the top reads as deep red and deep green
# glass, not a flat salmon field (its clipped share 25 % to about 1 %); nothing added on the floor
NIGHT2="--strip 300 --strip-color 1.0 0.55 0.25 --ambient 0.006 --exposure -1.0"   # the room at 0.6 %, so the record and arm keep their read
if [ "$1" = r2 ]; then
r a4-night-ember-2423-r2 --model out-strata-v4 --colour ember-2423 $NIGHT2 --core-glow 9
r a4-night-poison-2092-r2 --model out-strata-v4 --colour poison-2092 $NIGHT2 --core-glow 9
fi
# the gate (the coordinator, 08:15 and 08:17, three judges): v4 rebuilt with a 5.6 skin, sparser dots (5 to 35 %), the
# groove's ceiling printed opaque and the rings' undersides black; the strip at 2 W/m. Night: the guide's glow 4 W/m2
# (Poison 8, a stop up), graded brighter at the strip's edge (--grade); one large dim soft source behind the deck for a
# long reflection across the skin (--reflector 3) and a low warm kicker and rim for the hardware (--kicker 0.3), all
# three unseen by the camera, none thrown down. The base's top a fine satin (--base-rough 0.12), so it does not mirror
# the lit deck. The camera panned 50 mm along its right vector for room on both sides (--pan 0.05), the same for the
# set. Day: the room's light on the print baked for the new build (7, in the 5.6 skin's downward tint), shaded round
# the platter and the arm plate (Cycles leaves a print sealed under glass unlit; with no term at all it reads black)
G="--pan 0.05 --base-rough 0.12"
NIGHT3="--strip 150 --strip-color 1.0 0.55 0.25 --ambient 0.006 --exposure -1.0 --grade --reflector 3 --kicker 0.3 $G"
if [ "$1" = g1 ]; then
r a4-night-ember-2423-g1 --model out-strata-v4 --colour ember-2423 $NIGHT3 --core-glow 4
r a4-night-poison-2092-g1 --model out-strata-v4 --colour poison-2092 $NIGHT3 --core-glow 8
r a4-day-ember-2423-g1 --model out-strata-v4 --colour ember-2423 --day --strip 0 --core-glow 7 --strip-color 0.848 0.124 0.168 --exposure -2.0 $G
fi
# the gate's second pass (09:30, three judges): reflector tape round the core (no light out of the edges), the rings'
# tops printed black under the skin (no lit border), the glow graded brighter in the field than at the rim
# (--grade-edge-mid 0.75 1.1), Poison's glow 12; at night no reflector and no front kicker, only a low rim under the
# record's plane (--rim 0.6) and the room at 0.3 %; the bearing's brass blackened under the deck (--blacken)
G2="--pan 0.05 --base-rough 0.12 --blacken"
NIGHT4="--strip 150 --strip-color 1.0 0.55 0.25 --ambient 0.003 --exposure -1.0 --grade --grade-edge-mid 0.75 1.1 --rim 0.6 $G2"
if [ "$1" = g2 ]; then
r a4-night-ember-2423-g2 --model out-strata-v4 --colour ember-2423 $NIGHT4 --core-glow 4
r a4-night-poison-2092-g2 --model out-strata-v4 --colour poison-2092 $NIGHT4 --core-glow 12
r a4-day-ember-2423-g2 --model out-strata-v4 --colour ember-2423 --day --strip 0 --core-glow 7 --strip-color 0.848 0.124 0.168 --exposure -2.0 $G2
fi
