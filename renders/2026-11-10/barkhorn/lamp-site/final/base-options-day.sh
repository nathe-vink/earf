#!/bin/bash
# core-base-options-day.png (2026-11-11, for the owner): the same 3 x 3 as core-base-options.png (columns A as now, B
# rounded lip, C crystal-ball stand; rows satin black, own colour Ice, own colour Ember), the lamp OFF in a declared
# daylight studio (5000 K, the camera at 5000 K, the studio x3 at EV -2) on a pale neutral ground (#D6D6D4), the camera
# closer (the three 0.19 m apart). Own colour: the 6 mm skin over a white liner for all three, C 3 mm wider below the
# touch ring. Rows at 0.6 scale, 128 samples, denoised; labelled and stacked.
cd /home/user/earf/spinoffs/barkhorn/companions
D=/home/user/earf/renders/2026-11-10/barkhorn/lamp-site/final
S=/tmp/claude-0/-home-user-earf/e73bd455-48f8-5f69-9a3b-fa1e22e4e1e9/scratchpad/bo-day; mkdir -p $S
export WB=5000 STUDIO_K=5000 PAPER='#D6D6D4' WORLD='#E0E0E0' EXR=0 STUDIO=3 EV=-2 LIGHTS_OFF=1 BASE_DX=0.19
export BASECAM='((0.0,-0.92,0.30),(0.0,0.0,0.095),58.0)'
AUDIT=1 MASK=$D/masks/core-base-options-day.png python3.11 lamp_site.py baseopts-red > $D/audit/core-base-options-day.txt 2>&1
[ -s $S/row1.png ] || LAMP_OUT=$S/row1.png python3.11 lamp_site.py baseopts-red --samples 128 --scale 0.6 > /dev/null 2>&1
[ -s $S/row2.png ] || BASE_MAT=own LAMP_OUT=$S/row2.png python3.11 lamp_site.py baseopts-blue --samples 128 --scale 0.6 > /dev/null 2>&1
[ -s $S/row3.png ] || BASE_MAT=own LAMP_OUT=$S/row3.png python3.11 lamp_site.py baseopts-red --samples 128 --scale 0.6 > /dev/null 2>&1
cd $S
convert row1.png -gravity northwest -fill black -pointsize 26 -annotate +20+16 'Satin black, lamp off' r1.png
convert row2.png -gravity northwest -fill black -pointsize 26 -annotate +20+16 'Own colour, Ice, lamp off' r2.png
convert row3.png -gravity northwest -fill black -pointsize 26 -annotate +20+16 'Own colour, Ember, lamp off' r3.png
convert -size 1440x56 xc:'#202020' -fill white -pointsize 28 -gravity center \
  -annotate -494+0 'A  As now' -annotate +0+0 'B  Rounded lip' -annotate +494+0 'C  Crystal-ball stand' head.png
convert head.png r1.png r2.png r3.png -append -depth 8 -type TrueColor PNG24:$D/core-base-options-day.png
echo DONE > $S/done.txt
