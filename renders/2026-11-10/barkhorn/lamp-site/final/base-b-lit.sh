#!/bin/bash
# core-base-b-lit.png (2026-11-11, for the colour pick): base B (the owner's shape) in satin black, own colour Ice, own
# colour Ember, the lamp ON in the finals' dim studio (studio 0.5, EV -1, 4000 K, paper #9A9A9A), the camera closer on
# the base; three cells side by side, labelled. 192 samples, denoised.
cd /home/user/earf/spinoffs/barkhorn/companions
D=/home/user/earf/renders/2026-11-10/barkhorn/lamp-site/final
S=/tmp/claude-0/-home-user-earf/e73bd455-48f8-5f69-9a3b-fa1e22e4e1e9/scratchpad/b-lit; mkdir -p $S
export WB=4000 STUDIO_K=4000 PAPER='#9A9A9A' WORLD='#BDBDBD' EXR=0 STUDIO=0.5 EV=-1 CORE_BASE=B
export ORBCAM='((0.06,-0.60,0.16),(0.0,0.0,0.075),70.0)'
AUDIT=1 MASK=$D/masks/core-base-b-lit.png python3.11 lamp_site.py orb-red > $D/audit/core-base-b-lit.txt 2>&1
[ -s $S/c1.png ] || LAMP_OUT=$S/c1.png python3.11 lamp_site.py orb-red --samples 192 --scale 0.4 > /dev/null 2>&1
[ -s $S/c2.png ] || BASE_MAT=own LAMP_OUT=$S/c2.png python3.11 lamp_site.py orb-blue --samples 192 --scale 0.4 > /dev/null 2>&1
[ -s $S/c3.png ] || BASE_MAT=own LAMP_OUT=$S/c3.png python3.11 lamp_site.py orb-red --samples 192 --scale 0.4 > /dev/null 2>&1
cd $S
convert c1.png -gravity south -fill white -pointsize 24 -annotate +0+18 'B, satin black, lit' l1.png
convert c2.png -gravity south -fill white -pointsize 24 -annotate +0+18 'B, own colour Ice, lit' l2.png
convert c3.png -gravity south -fill white -pointsize 24 -annotate +0+18 'B, own colour Ember, lit' l3.png
convert l1.png l2.png l3.png +append -depth 8 -type TrueColor PNG24:$D/core-base-b-lit.png
echo DONE > $S/done.txt
