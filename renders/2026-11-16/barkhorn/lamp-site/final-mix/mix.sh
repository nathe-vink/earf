#!/bin/bash
# B-MIX (2026-11-16, the coordinator): THE MIX rendered into STAGING, final/'s names, the corrected method, LOAD_MIX=1
# INSTALLED 2026-11-17 (the owner said yes): its pictures, audits and masks moved to renders/2026-11-10/barkhorn/lamp-site/final/
# under the same names (the rows and the cluster excepted, re-rendered there); the mix is now lamp_site.py's default.
# (Hemisphere Ember 1.8, Acid 5, Ice 6, Haze 1.8; Core Poison 0.6; Smoke the approved pair; Dust and Fog as built).
# Nothing in final/ or legible/ is written. Each picture uses the recipe that made its final/ version (run.sh, views.sh,
# views2.sh, hemi-fix.sh, corrected.sh, core-final.sh, core-day2.sh, base-*.sh, legible*.sh). Skips what is done.
# Groups write G<n>-done.txt so each can be pushed as it finishes.
cd /home/user/earf/spinoffs/barkhorn/companions
export LOAD_MIX=1
D=/home/user/earf/renders/2026-11-16/barkhorn/lamp-site/final-mix
S=/tmp/claude-0/-home-user-earf/e73bd455-48f8-5f69-9a3b-fa1e22e4e1e9/scratchpad/final-mix; mkdir -p $S $D/audit $D/masks
L=/home/user/earf/renders/2026-11-12/barkhorn/lamp-site/legible
# BUDGET (s, default 4800): start no new picture after it, so each run ends inside the session's 2 h job limit; rerun to go on
START=$(date +%s)
r() { [ -s "$1" ] && return 0; [ $(( $(date +%s) - START )) -gt ${BUDGET:-4800} ] && { echo "BUDGET reached before $1"; exit 3; }; shift; "$@"; }
aud() { o=$1; shift; "$@" > "$o.tmp" 2>&1; mv "$o.tmp" "$o"; }
fit() { python3 -c "
from PIL import Image; import os,sys
p=sys.argv[1]; im=Image.open(p)
if os.path.getsize(p)>5e6:
    if im.mode=='RGBA' and im.getchannel('A').getextrema()==(255,255): im=im.convert('RGB')
    im.save(p,optimize=True)
print(p, os.path.getsize(p))" "$1"; }
LIT=(WB=4000 STUDIO_K=4000 PAPER='#9A9A9A' WORLD='#BDBDBD' EXR=0)
DCAM='((0.04,-0.66,0.98),(0.0,-0.05,0.34),45.0)'
DIR='((0.0,-1.04,0.55),(0.0,0.0,0.55),90.0)'
UND='((0.287,-0.496,0.10),(0.0,0.0,0.52),60.0)'
BELOW='((0.0,0.0,0.03),(0.0,0.0,0.5),50.0)'
H="red:ember amber:acid blue:ice violet:haze"
# THE PLACEMENT (2026-11-16, the coordinator, after B-SMOKE: no studio lamp's reflection with a visible outline on the
# lit glass): the key a 3.0 x 0.5 m strip overhead, the fill a wash on the back paper behind the lamp, the paper about
# 30 (final/smoke.sh). Every lit view where both stay out of frame: Hemisphere's hero and direct, Core's lit pictures.
# The under and below views keep the old placement (from below the moved fill is in frame).
# Hemisphere (the coordinator, 11:36: the overhead strip read as a slot on the lit picture's shoulder; the bar was the
# fill's reflection, the wash facing down): no key; the fill faces the back paper square (the shade sees only its dark
# back), the world (4000 K grey, even) lifting the paper to about 30; the kicker's rim strip stays
NH=(STUDIO_OFF=key 'FILL_POS=(0.0,0.55,2.1)' 'FILL_AIM=(0.0,1.0,2.1)' FILL_W=0.105 WORLD='#FFD4A5' WORLD_STR=0.82)
NC=(STUDIO_OFF=key 'FILL_POS=(0.0,0.55,1.3)' 'FILL_AIM=(0.0,1.0,1.3)' FILL_W=0.25 WORLD='#FFD4A5' WORLD_STR=0.38)   # Core: final/smoke.sh's
# Ember at 1.8 (the coordinator: a blotchy cell pattern over the lit bowl in the mix row): more samples for that lamp
spp() { [ "$1" = red ] && echo $(( $2 * ${RED_X:-3} )) || echo $2; }
# ---- G1: Hemisphere singles (hero, direct, under) for Ember, Acid, Ice, Haze; the Smoke hero (direct/under: B-SMOKE's)
for kv in $H black:smoke; do k=${kv%%:*}; n=${kv##*:}
  r $D/audit/hemisphere-$n.txt aud $D/audit/hemisphere-$n.txt env "${LIT[@]}" "${NH[@]}" DOMECAM="$DCAM" AUDIT=1 MASK=$D/masks/hemisphere-$n.png python3.11 lamp_site.py dome-$k
  r $D/hemisphere-$n.png env "${LIT[@]}" "${NH[@]}" DOMECAM="$DCAM" DENOISE=1 LAMP_OUT=$D/hemisphere-$n.png python3.11 lamp_site.py dome-$k --samples $(spp $k 192) --scale 1.0 > /dev/null 2>&1; fit $D/hemisphere-$n.png
  [ $k = black ] && continue
  r $D/audit/hemisphere-$n-direct.txt aud $D/audit/hemisphere-$n-direct.txt env "${LIT[@]}" "${NH[@]}" DENOISE=1 DOMECAM="$DIR" AUDIT=1 MASK=$D/masks/hemisphere-$n-direct.png python3.11 lamp_site.py dome-$k
  r $D/hemisphere-$n-direct.png env "${LIT[@]}" "${NH[@]}" DENOISE=1 DOMECAM="$DIR" LAMP_OUT=$D/hemisphere-$n-direct.png python3.11 lamp_site.py dome-$k --samples $(spp $k 128) --scale 1.0 > /dev/null 2>&1; fit $D/hemisphere-$n-direct.png
  r $D/audit/hemisphere-$n-under.txt aud $D/audit/hemisphere-$n-under.txt env "${LIT[@]}" DENOISE=1 DOMECAM="$UND" AUDIT=1 MASK=$D/masks/hemisphere-$n-under.png python3.11 lamp_site.py dome-$k
  r $D/hemisphere-$n-under.png env "${LIT[@]}" DENOISE=1 DOMECAM="$UND" LAMP_OUT=$D/hemisphere-$n-under.png python3.11 lamp_site.py dome-$k --samples $(spp $k 128) --scale 1.0 > /dev/null 2>&1; fit $D/hemisphere-$n-under.png
done
echo DONE > $D/G1-done.txt
# ---- G2: Ember's details, the cutaway and in use, the row, the cluster
OFF=(WB=5000 STUDIO_K=5000 LIGHTS_OFF=1 STUDIO=12 KEY_STRIP=3.0,0.5 'KEY_POS=(0.0,-0.5,2.2)' 'KEY_AIM=(0,0,0.55)' STUDIO_OFF=fill 'DOMECAM=((0.0,-1.04,0.55),(0.0,0.0,0.55),90.0)')
CAP=(WB=5000 STUDIO_K=5000 LIGHTS_OFF=1 STUDIO=8 KEY_STRIP=3.0,0.6 'KEY_POS=(0.0,0.9,1.5)' 'KEY_AIM=(0,0,0.62)' 'DOMECAM=((0.12,-0.60,0.73),(0.0,0.0,0.645),100.0)')
RIM=(WB=4000 STUDIO_K=4000 EV=-3.5 'DOMECAM=((0.15,-0.50,0.43),(0.0,-0.05,0.535),100.0)')
B2=(PAPER='#9A9A9A' WORLD='#BDBDBD' EXR=0 DENOISE=1)
r $D/audit/hemisphere-ember-off.txt aud $D/audit/hemisphere-ember-off.txt env "${B2[@]}" "${OFF[@]}" AUDIT=1 MASK=$D/masks/hemisphere-ember-off.png python3.11 lamp_site.py dome-red
r $D/hemisphere-ember-off.png env "${B2[@]}" "${OFF[@]}" LAMP_OUT=$D/hemisphere-ember-off.png python3.11 lamp_site.py dome-red --samples 128 --scale 1.0 > /dev/null 2>&1; fit $D/hemisphere-ember-off.png
r $D/audit/hemisphere-ember-cap.txt aud $D/audit/hemisphere-ember-cap.txt env "${B2[@]}" "${CAP[@]}" AUDIT=1 MASK=$D/masks/hemisphere-ember-cap.png python3.11 lamp_site.py dome-red
r $D/hemisphere-ember-cap.png env "${B2[@]}" "${CAP[@]}" LAMP_OUT=$D/hemisphere-ember-cap.png python3.11 lamp_site.py dome-red --samples 128 --scale 1.0 > /dev/null 2>&1; fit $D/hemisphere-ember-cap.png
r $D/audit/hemisphere-ember-rim.txt aud $D/audit/hemisphere-ember-rim.txt env "${B2[@]}" "${RIM[@]}" AUDIT=1 MASK=$D/masks/hemisphere-ember-rim.png python3.11 lamp_site.py dome-red
r $D/hemisphere-ember-rim.png env "${B2[@]}" "${RIM[@]}" FSTOP=4 'FOCUS=(0.0,-0.095,0.50)' LAMP_OUT=$D/hemisphere-ember-rim.png python3.11 lamp_site.py dome-red --samples 192 --scale 1.0 > /dev/null 2>&1; fit $D/hemisphere-ember-rim.png
r $D/audit/hemisphere-ember-below.txt aud $D/audit/hemisphere-ember-below.txt env "${LIT[@]}" DOMECAM="$BELOW" STUDIO_OFF=key AUDIT=1 MASK=$D/masks/hemisphere-ember-below.png python3.11 lamp_site.py dome-red
r $D/hemisphere-ember-below.png env "${LIT[@]}" DOMECAM="$BELOW" STUDIO_OFF=key DENOISE=1 LAMP_OUT=$D/hemisphere-ember-below.png python3.11 lamp_site.py dome-red --samples 192 --scale 1.0 > /dev/null 2>&1; fit $D/hemisphere-ember-below.png
r $D/hemisphere-ember-direct.png true   # (made in G1's loop as hemisphere-ember-direct and -under)
r $D/audit/hemisphere-ember-cutaway.txt aud $D/audit/hemisphere-ember-cutaway.txt env "${LIT[@]}" DENOISE=1 AUDIT=1 MASK=$D/masks/hemisphere-ember-cutaway.png python3.11 lamp_site.py cutaway
r $S/cutaway-raw.png env "${LIT[@]}" DENOISE=1 LAMP_OUT=$S/cutaway-raw.png python3.11 lamp_site.py cutaway --samples 192 --scale 1.0 > $S/cutaway.log 2>&1
r $D/hemisphere-ember-cutaway.png python3 $L/label.py $S/cutaway-raw.png $S/cutaway.log $D/hemisphere-ember-cutaway.png
r $D/hemisphere-ember-cutaway-phone.png python3 $L/label.py $S/cutaway-raw.png $S/cutaway.log $D/hemisphere-ember-cutaway-phone.png phone
r $D/audit/hemisphere-ember-inuse.txt aud $D/audit/hemisphere-ember-inuse.txt env "${LIT[@]}" DENOISE=1 ROOM_FILL=6 EV=-0.5 AUDIT=1 MASK=$D/masks/hemisphere-ember-inuse.png python3.11 lamp_site.py inuse
r $D/hemisphere-ember-inuse.png env "${LIT[@]}" DENOISE=1 ROOM_FILL=6 EV=-0.5 LAMP_OUT=$D/hemisphere-ember-inuse.png python3.11 lamp_site.py inuse --samples 256 --scale 1.0 > /dev/null 2>&1; fit $D/hemisphere-ember-inuse.png
r $D/audit/hemisphere-row.txt aud $D/audit/hemisphere-row.txt env "${LIT[@]}" DENOISE=1 AUDIT=1 MASK=$D/masks/hemisphere-row.png python3.11 lamp_site.py lamps-domes
r $D/hemisphere-row.png env "${LIT[@]}" DENOISE=1 LAMP_OUT=$D/hemisphere-row.png python3.11 lamp_site.py lamps-domes --samples 256 --scale 1.0 > /dev/null 2>&1; fit $D/hemisphere-row.png
r $D/audit/hemisphere-cluster.txt aud $D/audit/hemisphere-cluster.txt env "${LIT[@]}" DENOISE=1 AUDIT=1 MASK=$D/masks/hemisphere-cluster.png python3.11 lamp_site.py cluster
r $D/hemisphere-cluster.png env "${LIT[@]}" DENOISE=1 LAMP_OUT=$D/hemisphere-cluster.png python3.11 lamp_site.py cluster --samples 128 --scale 1.0 > /dev/null 2>&1; fit $D/hemisphere-cluster.png
echo DONE > $D/G2-done.txt
# ---- G3: Core, the whole set (Poison 0.6, Smoke 0.6; the rest as built), the corrected method throughout
export ORBCAM='((0.09,-0.86,0.21),(0.0,0.0,0.10),70.0)'
T="red:ember orange:dust amber:acid green:poison blue:ice violet:haze ice:fog black:smoke"
for kv in $T; do k=${kv%%:*}; n=${kv##*:}
  r $D/audit/core-$n.txt aud $D/audit/core-$n.txt env "${LIT[@]}" "${NC[@]}" STUDIO=0.5 EV=-1 AUDIT=1 MASK=$D/masks/core-$n.png python3.11 lamp_site.py orb-$k
  r $D/core-$n.png env "${LIT[@]}" "${NC[@]}" STUDIO=0.5 EV=-1 LAMP_OUT=$D/core-$n.png python3.11 lamp_site.py orb-$k --samples 256 --scale 1.0 > /dev/null 2>&1; fit $D/core-$n.png
done
r $D/audit/core-row.txt aud $D/audit/core-row.txt env "${LIT[@]}" STUDIO=0.5 EV=-1 AUDIT=1 MASK=$D/masks/core-row.png python3.11 lamp_site.py lamps-orbs
r $D/core-row.png env "${LIT[@]}" STUDIO=0.5 EV=-1 LAMP_OUT=$D/core-row.png python3.11 lamp_site.py lamps-orbs --samples 256 --scale 1.0 > /dev/null 2>&1; fit $D/core-row.png
DAY=(PAPER='#9A9A9A' WORLD='#BDA999' EXR=0 WB=5000 STUDIO_K=5000 LIGHTS_OFF=1 STUDIO=12 EV=-1 KEY_STRIP=3.0,0.5 'KEY_POS=(0.0,-0.6,2.0)' 'KEY_AIM=(0,0,0.10)' STUDIO_OFF=fill WORLD_STR=2.8)
r $D/audit/core-row-day.txt aud $D/audit/core-row-day.txt env "${DAY[@]}" AUDIT=1 MASK=$D/masks/core-row-day.png python3.11 lamp_site.py lamps-orbs
r $D/core-row-day.png env "${DAY[@]}" LAMP_OUT=$D/core-row-day.png python3.11 lamp_site.py lamps-orbs --samples 256 --scale 1.0 > /dev/null 2>&1; fit $D/core-row-day.png
unset ORBCAM
# core-base-b-lit (base-b-lit.sh)
# The lit Core sheets take the Core placement (NC; the coordinator: the new placement for every picture rendered from
# now on where it leaves the tints' look unchanged): the old key's two discs on every lit ball go, the tints do not move
BL=(WB=4000 STUDIO_K=4000 PAPER='#9A9A9A' EXR=0 STUDIO=0.5 EV=-1 CORE_BASE=B 'ORBCAM=((0.06,-0.60,0.16),(0.0,0.0,0.075),70.0)' "${NC[@]}")
mkdir -p $S/blit; r $D/audit/core-base-b-lit.txt aud $D/audit/core-base-b-lit.txt env "${BL[@]}" AUDIT=1 MASK=$D/masks/core-base-b-lit.png python3.11 lamp_site.py orb-red
r $S/blit/c1.png env "${BL[@]}" LAMP_OUT=$S/blit/c1.png python3.11 lamp_site.py orb-red --samples 192 --scale 0.4 > /dev/null 2>&1
r $S/blit/c2.png env "${BL[@]}" BASE_MAT=own LAMP_OUT=$S/blit/c2.png python3.11 lamp_site.py orb-blue --samples 192 --scale 0.4 > /dev/null 2>&1
r $S/blit/c3.png env "${BL[@]}" BASE_MAT=own LAMP_OUT=$S/blit/c3.png python3.11 lamp_site.py orb-red --samples 192 --scale 0.4 > /dev/null 2>&1
( cd $S/blit && convert c1.png -gravity south -fill white -pointsize 24 -annotate +0+18 'B, satin black, lit' l1.png && \
  convert c2.png -gravity south -fill white -pointsize 24 -annotate +0+18 'B, own colour Ice, lit' l2.png && \
  convert c3.png -gravity south -fill white -pointsize 24 -annotate +0+18 'B, own colour Ember, lit' l3.png && \
  convert l1.png l2.png l3.png +append -depth 8 -type TrueColor PNG24:$D/core-base-b-lit.png )
# core-base-b-allcolor (base-b-allcolor.sh)
mkdir -p $S/allc; AC=(EXR=0 BASE_MAT=own_all 'ORBCAM=((0.0,-0.42,0.17),(0.0,0.0,0.085),58.0)')
CD=(WB=5000 STUDIO_K=5000 PAPER='#D6D6D4' WORLD='#E0E0E0' STUDIO=3 EV=-2 LIGHTS_OFF=1)
CL=(WB=4000 STUDIO_K=4000 PAPER='#9A9A9A' STUDIO=0.5 EV=-1 "${NC[@]}")
r $D/audit/core-base-b-allcolor.txt aud $D/audit/core-base-b-allcolor.txt env "${AC[@]}" "${CL[@]}" AUDIT=1 MASK=$D/masks/core-base-b-allcolor.png python3.11 lamp_site.py orb-blue
r $S/allc/ice-off.png env "${AC[@]}" "${CD[@]}" LAMP_OUT=$S/allc/ice-off.png python3.11 lamp_site.py orb-blue --samples 128 --scale 0.3 > /dev/null 2>&1
r $S/allc/ice-lit.png env "${AC[@]}" "${CL[@]}" LAMP_OUT=$S/allc/ice-lit.png python3.11 lamp_site.py orb-blue --samples 128 --scale 0.3 > /dev/null 2>&1
r $S/allc/ember-off.png env "${AC[@]}" "${CD[@]}" LAMP_OUT=$S/allc/ember-off.png python3.11 lamp_site.py orb-red --samples 128 --scale 0.3 > /dev/null 2>&1
r $S/allc/ember-lit.png env "${AC[@]}" "${CL[@]}" LAMP_OUT=$S/allc/ember-lit.png python3.11 lamp_site.py orb-red --samples 128 --scale 0.3 > /dev/null 2>&1
( cd $S/allc && for n in ice-off ice-lit ember-off ember-lit; do
  Lb=$(echo $n | sed 's/ice/Ice/;s/ember/Ember/;s/-off/, lamp off (daylight)/;s/-lit/, lamp on/')
  F=$([ ${n##*-} = off ] && echo black || echo white)
  convert $n.png -gravity south -fill $F -pointsize 22 -annotate +0+14 "B, all own colour: $Lb" l-$n.png; done && \
  convert l-ice-off.png l-ice-lit.png l-ember-off.png l-ember-lit.png +append -depth 8 -type TrueColor PNG24:$D/core-base-b-allcolor.png )
# core-base-options (base-options.sh; row 1 BASE_MAT=black as corrected.sh) and its day version (corrected.sh)
for v in night day; do mkdir -p $S/bo-$v
  # night: NC scaled to this sheet's STUDIO=3 EV -2; the world lifts the paper back to its 27
  if [ $v = night ]; then BO=(WB=4000 STUDIO_K=4000 PAPER='#9A9A9A' EXR=0 STUDIO=3 EV=-2 STUDIO_OFF=key 'FILL_POS=(0.0,0.55,1.3)' 'FILL_AIM=(0.0,1.0,1.3)' FILL_W=0.083 WORLD='#FFD4A5' WORLD_STR=2.4); SP=256; F=white; OUT=core-base-options; SUF=''
  else BO=(WB=5000 STUDIO_K=5000 PAPER='#D6D6D4' WORLD='#E0E0E0' EXR=0 STUDIO=3 EV=-2 LIGHTS_OFF=1 BASE_DX=0.19 'BASECAM=((0.0,-0.92,0.30),(0.0,0.0,0.095),58.0)'); SP=128; F=black; OUT=core-base-options-day; SUF=', lamp off'; fi
  r $D/audit/$OUT.txt aud $D/audit/$OUT.txt env "${BO[@]}" BASE_MAT=black AUDIT=1 MASK=$D/masks/$OUT.png python3.11 lamp_site.py baseopts-red
  r $S/bo-$v/row1.png env "${BO[@]}" BASE_MAT=black LAMP_OUT=$S/bo-$v/row1.png python3.11 lamp_site.py baseopts-red --samples $SP --scale 0.6 > /dev/null 2>&1
  r $S/bo-$v/row2.png env "${BO[@]}" BASE_MAT=own LAMP_OUT=$S/bo-$v/row2.png python3.11 lamp_site.py baseopts-blue --samples $SP --scale 0.6 > /dev/null 2>&1
  r $S/bo-$v/row3.png env "${BO[@]}" BASE_MAT=own LAMP_OUT=$S/bo-$v/row3.png python3.11 lamp_site.py baseopts-red --samples $SP --scale 0.6 > /dev/null 2>&1
  ( cd $S/bo-$v && convert row1.png -gravity northwest -fill $F -pointsize 26 -annotate +20+16 "Satin black$SUF" r1.png && \
    convert row2.png -gravity northwest -fill $F -pointsize 26 -annotate +20+16 "Own colour, Ice$SUF" r2.png && \
    convert row3.png -gravity northwest -fill $F -pointsize 26 -annotate +20+16 "Own colour, Ember$SUF" r3.png && \
    convert -size 1440x56 xc:'#202020' -fill white -pointsize 28 -gravity center \
      -annotate -494+0 'A  As now' -annotate +0+0 'B  Rounded lip' -annotate +494+0 'C  Crystal-ball stand' head.png && \
    convert head.png r1.png r2.png r3.png -append -depth 8 -type TrueColor PNG24:$D/$OUT.png )
done
echo DONE > $D/G3-done.txt
# ---- G4: the photometry for the mix (a separate table; not merged into final/photometry.txt)
P=$D/photometry-mix.raw
if [ ! -s $P ]; then
  for kv in red:ember amber:acid blue:ice violet:haze black:smoke; do k=${kv%%:*}; n=${kv##*:}
    echo "hemisphere $n: $(BOUNCES=64 FRAME=dome-$k SPP=128 python3.11 launch/isphere.py 2>&1 | grep ISPHERE)"
    echo "hemisphere $n: $(env PAPER='#9A9A9A' LUX_SPAN=1.4 LUXPROBE=$S/lux.exr python3.11 lamp_site.py dome-$k --samples 256 2>&1 | grep -E '^LUXPTS')"
  done > $P.tmp
  for kv in green:poison black:smoke; do k=${kv%%:*}; n=${kv##*:}
    echo "core $n: $(FRAME=orb-$k SPP=256 python3.11 launch/isphere.py 2>&1 | grep ISPHERE)"
  done >> $P.tmp && mv $P.tmp $P
fi
echo DONE > $D/G4-done.txt
