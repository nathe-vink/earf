#!/bin/bash
# The Hemisphere top sheet v8's renders (the v7 check, 2026-11-24), the commands as run: today, A and B on the v8 CAD
# (top_tiers.py's meshes), Ember OFF on p6's ground. Each audit names its top, its meshes, HEMI_COLLAR_CAP, BORDER and
# the light (LIGHTSET).   renders/2026-11-24/barkhorn/lamp-site/tests/r2/v8.sh
cd "$(dirname "$0")/../../../../../.."
T=renders/2026-11-24/barkhorn/lamp-site/tests/r2.sh
G="HOUSE_AIM=key:-0.7,0,0.1;wall_left:0,0,-0.5 HOUSE_LAMP_K=wall_left:1.2,key:1.08 HEMI_COLLAR_CAP=1 GASKETS=1"
LV="HOUSE_CAM=0.693,-1.442,0.405,0,0,0.405,200"           # level, 1.6 m off, 200 mm lens
C=0.22,0.78,0.40,0.62                                       # the crop at full scale (1.8x the half-scale frame)
# from below (the same in all three tops: the collar's lip, the disc and the carrier do not change): the studio's lamps
# removed and no room (looking up, they stood in frame), lit by an even white dome, the camera at Blender's neutral (6500 K, tint 10; the v5 check's (13))
LIT="HOUSE_ROOM=0 HOUSE_DOME=1.0 HOUSE_WB=6500,10 STUDIO_OFF=house-key,house-key-face,house-key-housing,house-fill,house-fill-face,house-fill-housing,house-kick,house-kick-face,house-kick-housing,house-horn,house-horn-face,house-horn-housing,house-bg-left,house-bg-right,house-wall_left,house-bg-high,house-wall-ll"
BL="HOUSE_CAM=0,-0.03,0.02,0,0,0.306,40,1"                 # 0.29 under the rim, 3 cm off the axis, 40 mm lens
B35="HOUSE_CAM=0,-0.172,0.06,0,0,0.37,50,1"                # 35 deg off the axis, 50 mm lens, aimed at the crown's inside
for t in today A B; do
  H=""; [ $t = today ] || H="HEMI_TOP=$t"
  X="$G $LV $H" $T v8-$t hoff red
  X="$G $LV $H" $T v8-$t-x2 hoff red 128 1 $C
done
X="$G $LIT $BL" $T v8-below hoff red
X="$G $LIT $B35" $T v8-below35 hoff red
# v8 (the v7 check's (3)): A's lock as the owner's pictures show it, the lamp turned about its axis (HEMI_ROT): the knob
# in profile (-79) and toward the camera (-169)
X="$G $LV HEMI_TOP=A HEMI_ROT=-79" $T v8-A-profile hoff red
X="$G $LV HEMI_TOP=A HEMI_ROT=-169" $T v8-A-back hoff red
date -u
