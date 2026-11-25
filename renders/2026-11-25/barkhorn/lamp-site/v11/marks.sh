#!/bin/bash
# V11-13: close crops of the two one-way marks for the owner, on top A without the lock (Ember, off, the pass's ground and
# light, r2.sh's hoff base). The lamp turned (HEMI_ROT) so the marks (the crown's line at 30 deg, the clamp ring's groove at
# 60 deg) face the camera; one free-aimed camera close in. LIT=1: the even white dome, no room (as the from-below views). Usage: marks.sh NAME SAMPLES SCALE CAM
cd "$(dirname "$0")/../../../../../spinoffs/barkhorn/companions"
D=/home/user/earf/renders/2026-11-25/barkhorn/lamp-site/v11
E="LIGHTS_OFF=1 HOUSE_ROOM_TRANS=1 HOUSE_S=0.2 HOUSE_LIFT=0.25 HOUSE_WALL_LL=0.35 HOUSE_WALL_LL_SPREAD=30 HOUSE_BG=1.16 HOUSE_LIFT_RX=bg-left,wall_left HOUSE_ROOM_FIT=1"
G="HOUSE_AIM=key:-0.7,0,0.1;wall_left:0,0,-0.5 HOUSE_LAMP_K=wall_left:1.2,key:1.08 HEMI_COLLAR_CAP=1 GASKETS=1 HEMI_TOP=A HEMI_LOCK=0"
env $E $G ${LIT:+HOUSE_ROOM=0 HOUSE_DOME=1.0 HOUSE_WB=6500,10 STUDIO_OFF=house-key,house-key-face,house-key-housing,house-fill,house-fill-face,house-fill-housing,house-kick,house-kick-face,house-kick-housing,house-horn,house-horn-face,house-horn-housing,house-bg-left,house-bg-right,house-wall_left,house-bg-high,house-wall-ll} HEMI_ROT=${ROT:--109} HOUSE_CAM=$4 EXR=0 DENOISE=1 LAMP_OUT=$D/$1.png python3.11 lamp_site.py house-dome-red --samples $2 --scale $3 > /tmp/marks-$1.log 2>&1
tail -1 /tmp/marks-$1.log
