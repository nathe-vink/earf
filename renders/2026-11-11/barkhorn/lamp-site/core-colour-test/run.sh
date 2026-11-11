#!/bin/bash
# Core colour test (the coordinator, 2026-11-11 03:10; the owner: "get dust acid and ice more colorful, and smoke look
# more lit ... and less brown"). Four tints by three recipes, half size, the set's camera, exposure (studio 0.5, EV -1)
# and white balance (4000 K), on a neutral grey backdrop (the paper #9A9A9A, the studio lights at 4000 K so the paper
# reads neutral at the camera's balance, the world grey). Recipes:
#   1 as specified: Dust 2700, Acid 2700, Ice 3000, Smoke 2700 K; the outer ball at its loading, 0.5
#   2 whiter LED: 4000 K, the same lumens, the same balls
#   3 whiter LED and stronger tint: 4000 K; Dust, Acid, Ice at loading 1.5 (3x); Smoke lightened to 0.15
# Then the enclosing sensor's lumens out, and a labelled 4 x 3 contact sheet. Skips what is done.
cd /home/user/earf/spinoffs/barkhorn/companions
D=/home/user/earf/renders/2026-11-11/barkhorn/lamp-site/core-colour-test; mkdir -p $D
export WB=4000 STUDIO=0.5 EV=-1 EXR=0 STUDIO_K=4000 PAPER='#9A9A9A' WORLD='#BDBDBD'
r() { [ -s "$1" ] && return 0; shift; "$@"; }
for t in "dust orange 2700" "acid amber 2700" "ice blue 3000" "smoke black 2700"; do set -- $t
  r $D/$1-1-as-specified.png env LED_K=$3 CORE_LOAD=0.5 LAMP_OUT=$D/$1-1-as-specified.png python3.11 lamp_site.py orb-$2 --samples 256 --scale 0.5
  r $D/$1-2-whiter-led.png env LED_K=4000 CORE_LOAD=0.5 LAMP_OUT=$D/$1-2-whiter-led.png python3.11 lamp_site.py orb-$2 --samples 256 --scale 0.5
  L3=1.5; [ $1 = smoke ] && L3=0.15
  r $D/$1-3-whiter-led-stronger-tint.png env LED_K=4000 CORE_LOAD=$L3 LAMP_OUT=$D/$1-3-whiter-led-stronger-tint.png python3.11 lamp_site.py orb-$2 --samples 256 --scale 0.5
done > /dev/null 2>&1
# lumens out of the ball (the enclosing sensor; the set and studio gone)
F=$D/lumens.txt
if [ ! -s $F ]; then
  for t in "smoke black 2700 0.5" "fog ice 2700 0.5" "dust orange 2700 0.5" "acid amber 2700 0.5" "ice blue 3000 0.5" \
           "dust orange 4000 1.5" "acid amber 4000 1.5" "ice blue 4000 1.5" "smoke black 4000 0.15"; do set -- $t
    echo "$1 ${3}K loading $4: $(LED_K=$3 CORE_LOAD=$4 FRAME=orb-$2 SPP=256 python3.11 launch/isphere.py 2>&1 | grep ISPHERE)"
  done > $F.tmp && mv $F.tmp $F
  echo "opal out: $(DROP=ball- FRAME=orb-black SPP=256 python3.11 launch/isphere.py 2>&1 | grep ISPHERE)" >> $F
fi
AUDIT=1 python3.11 lamp_site.py orb-black 2>&1 | grep -E "lights|HIDDENCAST" > $D/audit.txt
cd $D && montage -label '%t' \
  dust-1-as-specified.png acid-1-as-specified.png ice-1-as-specified.png smoke-1-as-specified.png \
  dust-2-whiter-led.png acid-2-whiter-led.png ice-2-whiter-led.png smoke-2-whiter-led.png \
  dust-3-whiter-led-stronger-tint.png acid-3-whiter-led-stronger-tint.png ice-3-whiter-led-stronger-tint.png smoke-3-whiter-led-stronger-tint.png \
  -tile 4x3 -geometry 400x500+6+6 -pointsize 18 -background '#202020' -fill white -depth 8 -type TrueColor PNG24:contact-sheet.png
echo DONE > $D/done.txt
