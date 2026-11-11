#!/bin/bash
# core-base-options.png (2026-11-11, for the owner): columns A as now, B rounded lip, C crystal-ball stand; rows satin
# black (Ember), own colour in Ice, own colour in Ember (a 6 mm satin skin of the shell's own pour over a white liner, the
# touch ring satin black). Lit, the finals' camera rig and backdrop, the studio x3 at EV -2 so the black bases read
# (declared). Rows at 0.6 scale, 256 samples, denoised; labelled and stacked.
cd /home/user/earf/spinoffs/barkhorn/companions
D=/home/user/earf/renders/2026-11-10/barkhorn/lamp-site/final
S=/tmp/claude-0/-home-user-earf/e73bd455-48f8-5f69-9a3b-fa1e22e4e1e9/scratchpad/bo
export WB=4000 STUDIO_K=4000 PAPER='#9A9A9A' WORLD='#BDBDBD' EXR=0 STUDIO=3 EV=-2
AUDIT=1 MASK=$D/masks/core-base-options.png python3.11 lamp_site.py baseopts-red > $D/audit/core-base-options.txt 2>&1
[ -s $S/row1.png ] || LAMP_OUT=$S/row1.png python3.11 lamp_site.py baseopts-red --samples 256 --scale 0.6 > /dev/null 2>&1
[ -s $S/row2.png ] || BASE_MAT=own LAMP_OUT=$S/row2.png python3.11 lamp_site.py baseopts-blue --samples 256 --scale 0.6 > /dev/null 2>&1
[ -s $S/row3.png ] || BASE_MAT=own LAMP_OUT=$S/row3.png python3.11 lamp_site.py baseopts-red --samples 256 --scale 0.6 > /dev/null 2>&1
cd $S
for i in 1 2 3; do L=$( [ $i = 1 ] && echo 'Satin black' || ([ $i = 2 ] && echo 'Own colour, Ice' || echo 'Own colour, Ember')); \
  convert row$i.png -gravity northwest -fill white -pointsize 26 -annotate +20+16 "$L" r$i.png; done
convert -size 1440x56 xc:'#202020' -fill white -pointsize 28 -gravity center \
  -annotate -494+0 'A  As now' -annotate +0+0 'B  Rounded lip' -annotate +494+0 'C  Crystal-ball stand' head.png
convert head.png r1.png r2.png r3.png -append -depth 8 -type TrueColor PNG24:$D/core-base-options.png
echo DONE > $S/done.txt
