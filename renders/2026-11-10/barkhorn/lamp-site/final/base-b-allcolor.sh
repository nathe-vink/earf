#!/bin/bash
# core-base-b-allcolor.png (2026-11-11, the coordinator 16:37): base B with the WHOLE base in its own colour: one 6 mm
# satin skin of the lamp sheet over a white liner from the ball's seat to the floor, the bullnose lip included, the dock
# hidden under the skirt, the touch electrode under the skin. Four cells: Ice and Ember, lamp off in the declared daylight
# studio (5000 K, pale #D6D6D4, studio x3 at EV -2) and lamp on in the finals' dim studio (4000 K, #9A9A9A, studio 0.5,
# EV -1). Framed like the day grid's cells. 128 samples, denoised.
cd /home/user/earf/spinoffs/barkhorn/companions
D=/home/user/earf/renders/2026-11-10/barkhorn/lamp-site/final
S=/tmp/claude-0/-home-user-earf/e73bd455-48f8-5f69-9a3b-fa1e22e4e1e9/scratchpad/allc; mkdir -p $S
export EXR=0 BASE_MAT=own_all ORBCAM='((0.0,-0.42,0.17),(0.0,0.0,0.085),58.0)'
DAY="WB=5000 STUDIO_K=5000 PAPER=#D6D6D4 WORLD=#E0E0E0 STUDIO=3 EV=-2 LIGHTS_OFF=1"
LIT="WB=4000 STUDIO_K=4000 PAPER=#9A9A9A WORLD=#BDBDBD STUDIO=0.5 EV=-1"
env $LIT AUDIT=1 MASK=$D/masks/core-base-b-allcolor.png python3.11 lamp_site.py orb-blue > $D/audit/core-base-b-allcolor.txt 2>&1
for c in "ice-off blue $DAY" "ice-lit blue $LIT" "ember-off red $DAY" "ember-lit red $LIT"; do set -- $c; n=$1; k=$2; shift 2
  [ -s $S/$n.png ] || env "$@" LAMP_OUT=$S/$n.png python3.11 lamp_site.py orb-$k --samples 128 --scale 0.3 > /dev/null 2>&1
done
cd $S
for n in ice-off ice-lit ember-off ember-lit; do
  L=$(echo $n | sed 's/ice/Ice/;s/ember/Ember/;s/-off/, lamp off (daylight)/;s/-lit/, lamp on/')
  F=$([ ${n##*-} = off ] && echo black || echo white)
  convert $n.png -gravity south -fill $F -pointsize 22 -annotate +0+14 "B, all own colour: $L" l-$n.png
done
convert l-ice-off.png l-ice-lit.png l-ember-off.png l-ember-lit.png +append -depth 8 -type TrueColor PNG24:$D/core-base-b-allcolor.png
echo DONE > $S/done.txt
