#!/bin/bash
# The owner's lock pictures (the coordinator's v7 check, 2026-11-24): top A's level frame four ways, one camera, light and
# exposure (v7.sh's level view), and one view from 30 deg below on the knob's side. The lock (Ganter GN 617) points at
# 105 deg; the level camera looks from -64 deg. HEMI_ROT turns every part of the lamp about its axis.
#   lock-1-hidden   = v7-A (the lock as drawn, its knob behind the crown), copied
#   lock-2-profile  HEMI_ROT=-79   (the knob at 26 deg: across the view, in profile)
#   lock-3-back     HEMI_ROT=-169  (the knob at -64 deg: toward the camera, end-on)
#   lock-4-none     HEMI_ROT=-79 HEMI_LOCK=0 (no lock, from 2's angle)
#   lock-5-below    the knob's side (105 deg), 30 deg below the top, 0.75 m off, 100 mm lens; the even dome, no room
cd "$(dirname "$0")/../../../../../.."
T=renders/2026-11-24/barkhorn/lamp-site/tests/r2.sh
D=renders/2026-11-24/barkhorn/lamp-site/tests/r2
G="HOUSE_AIM=key:-0.7,0,0.1;wall_left:0,0,-0.5 HOUSE_LAMP_K=wall_left:1.2,key:1.08 HEMI_COLLAR_CAP=1 GASKETS=1 HEMI_TOP=A"
LV="HOUSE_CAM=0.693,-1.442,0.405,0,0,0.405,200"
LIT="HOUSE_ROOM=0 HOUSE_DOME=1.0 HOUSE_WB=6500,10 STUDIO_OFF=house-key,house-key-face,house-key-housing,house-fill,house-fill-face,house-fill-housing,house-kick,house-kick-face,house-kick-housing,house-horn,house-horn-face,house-horn-housing,house-bg-left,house-bg-right,house-wall_left,house-bg-high,house-wall-ll"
[ -f $D/lock-1-hidden.png ] || { cp $D/v7-A.png $D/lock-1-hidden.png; cp $D/audit/v7-A.txt $D/audit/lock-1-hidden.txt; }
X="$G $LV HEMI_ROT=-79" $T lock-2-profile hoff red
X="$G $LV HEMI_ROT=-169" $T lock-3-back hoff red
X="$G $LV HEMI_ROT=-79 HEMI_LOCK=0" $T lock-4-none hoff red
# (the first try, 1.6 m off with the 200 mm lens, put the camera under the paper ground: re-shot from 0.75 m, 100 mm lens)
X="$G $LIT HOUSE_CAM=-0.168,0.628,0.03,0,0,0.38,100,1" $T lock-5-below hoff red
date -u
