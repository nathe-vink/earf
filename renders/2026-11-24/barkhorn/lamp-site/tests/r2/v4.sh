#!/bin/bash
# The Hemisphere top sheet v4's renders (check 3, 2026-11-24), the commands as run: today, A and B on the fixed CAD
# (top_tiers.py's meshes), Ember OFF on p6's ground. Each audit names its top, its meshes, HEMI_COLLAR_CAP and BORDER.
#   renders/2026-11-24/barkhorn/lamp-site/tests/r2/v4.sh
cd "$(dirname "$0")/../../../../../.."
T=renders/2026-11-24/barkhorn/lamp-site/tests/r2.sh
G="HOUSE_AIM=key:-0.7,0,0.1;wall_left:0,0,-0.5 HOUSE_LAMP_K=wall_left:1.2,key:1.08 HEMI_COLLAR_CAP=1 GASKETS=1"
LV="HOUSE_CAM=0.693,-1.442,0.405,0,0,0.405,200"           # level, 1.6 m off, 200 mm lens
BL="HOUSE_CAM=0,-0.03,0.02,0,0,0.306,40,1"                 # from below: 0.29 under the rim, 40 mm lens, aimed freely
C=0.22,0.78,0.40,0.62                                       # the crop at full scale (1.8x the half-scale frame)
for t in today A B; do
  H=""; [ $t = today ] || H="HEMI_TOP=$t"
  X="$G $LV $H" $T v4-$t hoff red
  X="$G $LV $H" $T v4-$t-x2 hoff red 128 1 $C
  X="$G $BL $H" $T v4-$t-below hoff red
done
date -u
