#!/bin/bash
# The Hemisphere top sheet v4's renders (check 3, 2026-11-24), the commands as run: today, A and B on the fixed CAD
# (top_tiers.py's meshes), Ember OFF on p6's ground. Each audit names its top, its meshes, HEMI_COLLAR_CAP and BORDER.
#   renders/2026-11-24/barkhorn/lamp-site/tests/r2/v4.sh
cd "$(dirname "$0")/../../../../../.."
T=renders/2026-11-24/barkhorn/lamp-site/tests/r2.sh
G="HOUSE_AIM=key:-0.7,0,0.1;wall_left:0,0,-0.5 HOUSE_LAMP_K=wall_left:1.2,key:1.08 HEMI_COLLAR_CAP=1 GASKETS=1"
LV="HOUSE_CAM=0.693,-1.442,0.405,0,0,0.405,200"           # level, 1.6 m off, 200 mm lens
# from below: 0.29 under the rim, 40 mm lens, aimed freely. Looking up, the studio's hidden lamps and the room's ceiling
# stood in frame (CASTCHECK), so this view is lit by an even white dome instead: the studio's lamps removed, no room
BL="HOUSE_CAM=0,-0.03,0.02,0,0,0.306,40,1 HOUSE_ROOM=0 HOUSE_DOME=1.0 STUDIO_OFF=house-key,house-key-face,house-key-housing,house-fill,house-fill-face,house-fill-housing,house-kick,house-kick-face,house-kick-housing,house-horn,house-horn-face,house-horn-housing,house-bg-left,house-bg-right,house-wall_left,house-bg-high,house-wall-ll"
C=0.22,0.78,0.40,0.62                                       # the crop at full scale (1.8x the half-scale frame)
for t in today A B; do
  H=""; [ $t = today ] || H="HEMI_TOP=$t"
  [ -n "$BELOW_ONLY" ] || X="$G $LV $H" $T v4-$t hoff red
  [ -n "$BELOW_ONLY" ] || X="$G $LV $H" $T v4-$t-x2 hoff red 128 1 $C
  X="$G $BL $H" $T v4-$t-below hoff red
done
date -u
