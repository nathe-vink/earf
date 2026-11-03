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
C="--edge-frost 0.35 --base-tint smoke-2074 --scale 0.75 --samples 80 --paper #7A7570 --tint-mode custom"   # per-frame options follow and win
r() { n=$1; shift; python3.11 scene.py dusk $C "$@" --out $OUT/$n.png > /tmp/mantle-r48-$n.log 2>&1; echo "$n $(grep -c ^wrote /tmp/mantle-r48-$n.log)"; }
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
# the gate's third pass (10:16): the skin's edges painted black, black edge tape round the core, the groove's ceiling
# printed black; the guide's glow a 4000 K blackbody (the speakers' CCT; the tint comes from the skin's absorption,
# not a picked color), graded darker at the rim (--grade-edge-mid 0.5 1.1 --grade-fall 0.08); the strip's own
# emitter off (the glow sheet is its whole output; on, it doubled at the groove); exposure -1.5; the speaker lane's night
# set (--night-room 20: a wall close behind, the floor #2A2D33 at 0.15, a low navy ambient), no rim, no kicker
G3="--pan 0.05 --base-rough 0.12 --blacken"
NIGHT5="--strip 0 --cct 4000 --ambient 0.003 --exposure -1.5 --grade --grade-edge-mid 0.5 1.1 --grade-fall 0.08 --night-room 20 --samples 128 $G3"
if [ "$1" = g3 ]; then
r a4-night-ember-2423-g3 --model out-strata-v4 --colour ember-2423 $NIGHT5 --core-glow 4
r a4-night-poison-2092-g3 --model out-strata-v4 --colour poison-2092 $NIGHT5 --core-glow 12
r a4-day-ember-2423-g3 --model out-strata-v4 --colour ember-2423 --day --strip 0 --core-glow 7 --strip-color 0.848 0.124 0.168 --exposure -2.0 $G3
fi
# the gate's fourth pass (11:26): the glow lights the world (--glass-shadows: shadow rays pass the flat acrylic, so the
# arm, the pillar and the platter's sides catch it from below); the glow down half a stop (Ember 2.8, Poison 6), a
# short vignette at the bezel and a broad front-to-back gradient (--grade-edge-mid 0.35 1.0 --grade-fall 0.025 --tilt
# 0.15); a dim wash on the wall behind for a broad soft reflection across the top (--wall-wash 6); the navy ambient up
# (--night-room 35) so the base, the posts and the float read; Poison's red matched to the lamps' day hue (scene.py
# STOCK_HELD); the acrylic's wear at 0.3 (it read as wrinkles under the glow), 192 samples; the border's underside
# printed white up, black down (by day it reads as tint over white, as the field does: --border-glow 1.0, its room
# light baked as the field's; at night it gets no light of its own); the groove's ceiling the same print, its glow
# scaled to the field (--ceil-k 0.6: it rendered 1.6x at the same strength, cause not found); the posts' seats' walls
# clear; the platter's rim a soft satin (--platter-edge 0.15)
G4="--pan 0.05 --base-rough 0.12 --blacken --wear 0.3 --platter-edge 0.15 --ceil-k 0.6"
NIGHT6="--strip 0 --cct 4000 --ambient 0.003 --exposure -1.5 --grade --grade-edge-mid 0.35 1.0 --grade-fall 0.025 --tilt 0.15 --night-room 35 --glass-shadows --wall-wash 6 --samples 192 $G4"
if [ "$1" = g4 ]; then
r a4-night-ember-2423-g4 --model out-strata-v4 --colour ember-2423 $NIGHT6 --core-glow 2.8
r a4-night-poison-2092-g4 --model out-strata-v4 --colour poison-2092 $NIGHT6 --core-glow 6
r a4-day-ember-2423-g4 --model out-strata-v4 --colour ember-2423 --day --strip 0 --core-glow 7 --strip-color 0.848 0.124 0.168 --exposure -2.0 --border-glow 1.0 $G4
fi
# the gate's fifth pass (12:33), the Ember pair first: by day the border and the groove's ceiling carry the field's own
# sparse dots (5 % at the rim), so the day bake follows the real dot ramp (--grade-edge-mid 0.15 1.0 --grade-fall 0.07)
# and the border continues the field's tone (--border-glow 0.4, the field's rim value); the skin's lacquered edges and
# the black print glossy, the rings' edges polished (--edge-frost 0.08), the smoked base glossy; at night the glow a third
# down (1.9), falling gently from the lit edge (--grade-edge-mid 1.0 0.8 --grade-fall 0.1), AgX at base contrast (the
# medium-high look clipped it to a flat red), no wear arcs, little film grain
G5="--pan 0.05 --blacken --wear 0 --platter-edge 0.15 --ceil-k 0.6 --edge-frost 0.08 --grain 0.004"
if [ "$1" = g5 ]; then
r a4-night-ember-2423-g5 --model out-strata-v4 --colour ember-2423 --strip 0 --cct 4000 --ambient 0.003 --exposure -1.5 --grade --grade-edge-mid 1.0 0.8 --grade-fall 0.1 --night-room 35 --glass-shadows --wall-wash 6 --samples 192 --core-glow 1.9 --look "AgX - Base Contrast" $G5
r a4-day-ember-2423-g5 --model out-strata-v4 --colour ember-2423 --day --strip 0 --core-glow 7 --strip-color 0.848 0.124 0.168 --exposure -2.0 --grade --grade-edge-mid 0.15 1.0 --grade-fall 0.07 --border-glow 0.4 $G5
fi
# option C (the coordinator, 13:26; mantle_strata_v5.py, out-strata-v5): the print graded by distance from the
# spindle, dense under the platter, clear glass by 230 (--radial 0.150 0.230); the strip in an octagonal groove at r 78
# under the platter (fed from the center, so nothing shows); the border clear tinted glass; glass shadows on, so the
# float is lit through the clear deck by day and the glow reaches the hardware at night. Night as v4's g5 (3 W/m2 at
# the dense center); day the room's light on the dots baked as before (7 at the dense center, falling with the cover)
C5="--pan 0.05 --blacken --wear 0 --platter-edge 0.15 --edge-frost 0.08 --grain 0.004 --radial 0.150 0.230 --glass-shadows"
if [ "$1" = c ]; then
r a5-night-ember-2423-c --model out-strata-v5 --colour ember-2423 --strip 0 --cct 4000 --ambient 0.003 --exposure -1.5 --night-room 35 --wall-wash 6 --samples 192 --core-glow 3 --look "AgX - Base Contrast" $C5
r a5-day-ember-2423-c --model out-strata-v5 --colour ember-2423 --day --strip 0 --core-glow 7 --strip-color 0.848 0.124 0.168 --exposure -2.0 $C5
fi
# option C, gate 1 (the coordinator, 14:21): the glow sent down through the clear gaps at grazing angles, near the
# critical angle (a control with every gap backed matched A on the base and floor; a thin-film AR top cut little), so
# the whole field is backed black (--backed) with nothing printed under the platter (--back-r 0.150), the border clear;
# at night the glow rises off the platter's foot over 35 mm (--rise) and falls to 55 % at the rim (cover 0.22 to 0.12
# by 280), not to black; by day an even print (0.18); the strip's channel the backer's flat black (--matte-channel);
# the label's wordmark on its near half (--label-near)
C7="--pan 0.05 --blacken --wear 0 --platter-edge 0.15 --edge-frost 0.08 --grain 0.004 --radial 0.150 0.280 --back-r 0.150 --backed --matte-channel --label-near --glass-shadows"
if [ "$1" = c2 ]; then
r a5-night-ember-2423-c2 --model out-strata-v5 --colour ember-2423 --strip 0 --cct 4000 --ambient 0.003 --exposure -1.5 --night-room 35 --wall-wash 6 --samples 192 --core-glow 2.6 --cover-max 0.22 --cover-floor 0.12 --rise 0.035 --look "AgX - Base Contrast" $C7
r a5-day-ember-2423-c2 --model out-strata-v5 --colour ember-2423 --day --strip 0 --core-glow 7 --cover-max 0.18 --cover-floor 0.18 --strip-color 0.848 0.124 0.168 --exposure -2.0 $C7
fi
# option C3 (the coordinator, 15:34; out-strata-v5 rebuilt with the skin's border as its own frame): the print and the
# glow begin at r 105, well under the platter (--back-r 0.105), so no black crescent shows in front of it and the glow
# lights the platter's rim; a center-out falloff, cover 0.24 to 0.05 by 280 (--radial 0.105 0.280), backed throughout;
# the print a real 2.5 mm dot screen (--dot-pitch); the border clear tinted glass, the rings' undersides bare
# (--clear-ring), the frame bonded to the field with black cement; the edges polished (--edge-frost 0.012) with no
# shader bevel on them (--no-edge-bevel); by day an even print (0.15) and the room's light on it baked at 5 (deeper).
# The first full pair (16:14) showed the 2.5 mm dot screen as a mesh, like perforated metal: the frames are re-rendered
# with the print as a tone (--dot-pitch 0) and the channel hidden behind the backer film (it glinted amber again)
C9="--pan 0.05 --blacken --wear 0 --platter-edge 0.15 --edge-frost 0.012 --grain 0.004 --radial 0.105 0.280 --back-r 0.105 --backed --matte-channel --label-near --glass-shadows --clear-ring --dot-pitch 0 --no-edge-bevel"
if [ "$1" = c3 ]; then
r a5-night-ember-2423-c3 --model out-strata-v5 --colour ember-2423 --strip 0 --cct 4000 --ambient 0.003 --exposure -1.5 --night-room 35 --wall-wash 6 --samples 192 --core-glow 2.6 --cover-max 0.24 --cover-floor 0.05 --look "AgX - Base Contrast" $C9
r a5-day-ember-2423-c3 --model out-strata-v5 --colour ember-2423 --day --strip 0 --core-glow 5 --cover-max 0.15 --cover-floor 0.15 --strip-color 0.848 0.124 0.168 --exposure -2.0 $C9
fi
# C3 night gate (the coordinator, 17:07): a thin red line inside the border along the back-left edge, the border
# frame's inner cut face (glossy black lacquer) mirroring the field's glow, and a fainter one low on the front face.
# The bond lines (the frame to the field, the rings to the core) are now matte black, as index-matched black cement
# is: no gloss from either side. The night frame only; the day frame stands
if [ "$1" = c3b ]; then
r a5-night-ember-2423-c3b --model out-strata-v5 --colour ember-2423 --strip 0 --cct 4000 --ambient 0.003 --exposure -1.5 --night-room 35 --wall-wash 6 --samples 192 --core-glow 2.6 --cover-max 0.24 --cover-floor 0.05 --look "AgX - Base Contrast" $C9
fi
# the C3 pair (the coordinator, 17:57), night and day from one build: as c3b, plus no post seats in the light guide
# (out-strata-v5 rebuilt: the posts butt-bond to the backed underside; the seat's wall had drawn a ring in the glow in
# front of the platter) and the glow faded over the last 8 mm before the core's edge (--edge-fade), inside the black
# band (a lit tick showed by the arm pillar). Set, camera and centre feed unchanged
if [ "$1" = c3c ]; then
r a5-night-ember-2423-c3c --model out-strata-v5 --colour ember-2423 --strip 0 --cct 4000 --ambient 0.003 --exposure -1.5 --night-room 35 --wall-wash 6 --samples 192 --core-glow 2.6 --cover-max 0.24 --cover-floor 0.05 --look "AgX - Base Contrast" $C9 --edge-fade 0.008
r a5-day-ember-2423-c3c --model out-strata-v5 --colour ember-2423 --day --strip 0 --core-glow 5 --cover-max 0.15 --cover-floor 0.15 --strip-color 0.848 0.124 0.168 --exposure -2.0 $C9 --edge-fade 0.008
fi
