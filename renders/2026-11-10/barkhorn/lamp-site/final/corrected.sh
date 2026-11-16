#!/bin/bash
# (2026-11-16) row 1 sets BASE_MAT=black: the default is the own-colour base since 3e38954b, which the C stand cannot take
# The corrected method (lamp_site.py since 9a6a2913, 2026-11-16): the photometry as the source of truth, then the off and
# daylight finals that do not show Smoke, at the same names. Rerun until corrected-done.txt.
cd /home/user/earf/spinoffs/barkhorn/companions
D=/home/user/earf/renders/2026-11-10/barkhorn/lamp-site/final
S=/tmp/claude-0/-home-user-earf/e73bd455-48f8-5f69-9a3b-fa1e22e4e1e9/scratchpad/corrected-finals; mkdir -p $S/audit $S/masks $S/bo
r() { [ -s "$1" ] && return 0; shift; "$@"; }
aud() { o=$1; shift; "$@" > "$o.tmp" 2>&1; mv "$o.tmp" "$o"; }
T="red:ember orange:dust amber:acid green:poison blue:ice violet:haze ice:fog black:smoke"
# 1. the photometry: Hemisphere's lumens below/above the rim and the table's lux (paper #9A9A9A, as published), 0.5 m
# down at the centre, 0.3 and 0.6 m off; Core's lumens out of the ball
if [ ! -s $S/photometry.raw ]; then
  for kv in $T; do k=${kv%%:*}; n=${kv##*:}
    echo "hemisphere $n: $(BOUNCES=64 FRAME=dome-$k SPP=128 python3.11 launch/isphere.py 2>&1 | grep ISPHERE)"
    echo "hemisphere $n: $(env PAPER='#9A9A9A' LUX_SPAN=1.4 LUXPROBE=$S/lux.exr python3.11 lamp_site.py dome-$k --samples 256 2>&1 | grep -E '^LUX ')"
    echo "hemisphere $n: $(env PAPER='#9A9A9A' LUX_SPAN=1.4 LUXPROBE=$S/lux.exr python3.11 lamp_site.py dome-$k --samples 256 2>&1 | grep -E '^LUXPTS')"
    echo "core $n: $(FRAME=orb-$k SPP=256 python3.11 launch/isphere.py 2>&1 | grep ISPHERE)"
  done > $S/photometry.tmp && mv $S/photometry.tmp $S/photometry.raw
fi
# 2. Hemisphere Ember off and the cap detail (as hemi-fix.sh: daylight, one strip overhead)
export PAPER='#9A9A9A' EXR=0 DENOISE=1
OFF=(WB=5000 STUDIO_K=5000 LIGHTS_OFF=1 STUDIO=12 KEY_STRIP=3.0,0.5 'KEY_POS=(0.0,-0.5,2.2)' 'KEY_AIM=(0,0,0.55)' STUDIO_OFF=fill 'DOMECAM=((0.0,-1.04,0.55),(0.0,0.0,0.55),90.0)')
CAP=(WB=5000 STUDIO_K=5000 LIGHTS_OFF=1 STUDIO=8 KEY_STRIP=3.0,0.6 'KEY_POS=(0.0,0.9,1.5)' 'KEY_AIM=(0,0,0.62)' 'DOMECAM=((0.12,-0.60,0.73),(0.0,0.0,0.645),100.0)')
r $S/audit/hemisphere-ember-off.txt aud $S/audit/hemisphere-ember-off.txt env WORLD='#BDBDBD' "${OFF[@]}" AUDIT=1 MASK=$S/masks/hemisphere-ember-off.png python3.11 lamp_site.py dome-red
r $S/audit/hemisphere-ember-cap.txt aud $S/audit/hemisphere-ember-cap.txt env WORLD='#BDBDBD' "${CAP[@]}" AUDIT=1 MASK=$S/masks/hemisphere-ember-cap.png python3.11 lamp_site.py dome-red
r $S/hemisphere-ember-off.png env WORLD='#BDBDBD' "${OFF[@]}" LAMP_OUT=$S/hemisphere-ember-off.png python3.11 lamp_site.py dome-red --samples 128 --scale 1.0 > /dev/null 2>&1
r $S/hemisphere-ember-cap.png env WORLD='#BDBDBD' "${CAP[@]}" LAMP_OUT=$S/hemisphere-ember-cap.png python3.11 lamp_site.py dome-red --samples 128 --scale 1.0 > /dev/null 2>&1
# 3. core-base-options-day.png (as base-options-day.sh; Ember and Ice, no Smoke)
BO=(WB=5000 STUDIO_K=5000 PAPER='#D6D6D4' WORLD='#E0E0E0' STUDIO=3 EV=-2 LIGHTS_OFF=1 BASE_DX=0.19 'BASECAM=((0.0,-0.92,0.30),(0.0,0.0,0.095),58.0)')
r $S/audit/core-base-options-day.txt aud $S/audit/core-base-options-day.txt env "${BO[@]}" BASE_MAT=black AUDIT=1 MASK=$S/masks/core-base-options-day.png python3.11 lamp_site.py baseopts-red
r $S/bo/row1.png env "${BO[@]}" BASE_MAT=black LAMP_OUT=$S/bo/row1.png python3.11 lamp_site.py baseopts-red --samples 128 --scale 0.6 > /dev/null 2>&1
r $S/bo/row2.png env "${BO[@]}" BASE_MAT=own LAMP_OUT=$S/bo/row2.png python3.11 lamp_site.py baseopts-blue --samples 128 --scale 0.6 > /dev/null 2>&1
r $S/bo/row3.png env "${BO[@]}" BASE_MAT=own LAMP_OUT=$S/bo/row3.png python3.11 lamp_site.py baseopts-red --samples 128 --scale 0.6 > /dev/null 2>&1
cd $S/bo
convert row1.png -gravity northwest -fill black -pointsize 26 -annotate +20+16 'Satin black, lamp off' r1.png
convert row2.png -gravity northwest -fill black -pointsize 26 -annotate +20+16 'Own colour, Ice, lamp off' r2.png
convert row3.png -gravity northwest -fill black -pointsize 26 -annotate +20+16 'Own colour, Ember, lamp off' r3.png
convert -size 1440x56 xc:'#202020' -fill white -pointsize 28 -gravity center \
  -annotate -494+0 'A  As now' -annotate +0+0 'B  Rounded lip' -annotate +494+0 'C  Crystal-ball stand' head.png
convert head.png r1.png r2.png r3.png -append -depth 8 -type TrueColor PNG24:$S/core-base-options-day.png
echo DONE > $S/corrected-done.txt
