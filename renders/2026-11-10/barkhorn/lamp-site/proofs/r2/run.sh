#!/bin/bash
# proofs r2 (2026-11-10): the lamps' lumens at their colour's luminance (r1 gave 52 % at 2700 K, 57 % at 3000 K), the
# Core window a clear filter (thin_shadow counted its light twice), 32 bounces of each kind; every lit frame twice in
# light colour (-warm as drawn, -amber 2200 K, the same lumens) at one camera balance, 4000 K. Hemisphere: one render,
# the LEDs in their own light group, recoloured (launch/lightcolor.py; no denoiser, so the passes are exact). Core:
# denoised, so rendered once a colour (the light-group passes are not denoised)
cd /home/user/earf/spinoffs/barkhorn/companions
D=/home/user/earf/renders/2026-11-10/barkhorn/lamp-site/proofs/r2
S=/tmp/claude-0/-home-user-earf/e73bd455-48f8-5f69-9a3b-fa1e22e4e1e9/scratchpad/r2; mkdir -p $S
BELOW='((0.0,0.0,0.03),(0.0,0.0,0.5),50.0)'
AUDIT=1 python3.11 lamp_site.py orb-blue > $D/core-ice.audit.txt 2>&1
for t in "ice blue" "ember red"; do set -- $t
  WB=4000 STUDIO=0.5 EV=-1 EXR=0 LAMP_OUT=$D/core-$1-warm.png python3.11 lamp_site.py orb-$2 --samples 256 --scale 0.5 > $S/core-$1-warm.log 2>&1
  WB=4000 STUDIO=0.5 EV=-1 EXR=0 LED_K=2200 LAMP_OUT=$D/core-$1-amber.png python3.11 lamp_site.py orb-$2 --samples 256 --scale 0.5 > $S/core-$1-amber.log 2>&1
done
WB=4000 LIGHTS_OFF=1 EXR=0 LAMP_OUT=$D/core-ice-unlit.png python3.11 lamp_site.py orb-blue --samples 256 --scale 0.5 > $S/core-ice-unlit.log 2>&1
for v in "hemi-ember dome-red 2700" "hemi-ice dome-blue 3000" "hemi-ember-below dome-red 2700"; do set -- $v
  if [ $1 = hemi-ember-below ]; then export DOMECAM="$BELOW" STUDIO_OFF=key; fi
  WB=4000 LIGHTGROUPS=$S/$1-passes.exr LAMP_OUT=$S/$1.png python3.11 lamp_site.py $2 --samples 768 --scale 0.5 > $S/$1.log 2>&1
  python3.11 launch/lightcolor.py $S/$1-passes.exr $D/$1 -2.0 $3 > $D/$1.lightcolor.txt 2>&1
done
echo BATCH DONE > $D/done.txt
