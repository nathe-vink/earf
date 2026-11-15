#!/bin/bash
# Off match (2026-11-15): Hemisphere and Core switched off in ONE rig, the day row's (5000 K, the camera 5000 K, one
# 3.0 x 0.5 strip 1.9 m above and 0.6 m in front of the lamp's middle, the world lifted 2.8 and tinted #BDA999, no fill,
# no kicker, studio 12, EV -1), the same camera distance and lens for both (0.86 m, 70 mm). Env switches only.
cd /home/user/earf/spinoffs/barkhorn/companions
S=/tmp/claude-0/-home-user-earf/e73bd455-48f8-5f69-9a3b-fa1e22e4e1e9/scratchpad/offmatch
export PAPER='#9A9A9A' EXR=0 DENOISE=1 WB=5000 STUDIO_K=5000 WORLD='#BDA999' LIGHTS_OFF=1 STUDIO=12 EV=-1 KEY_STRIP=3.0,0.5 STUDIO_OFF=fill,kicker WORLD_STR=2.8
H=('KEY_POS=(0.0,-0.6,2.45)' 'KEY_AIM=(0,0,0.55)' 'DOMECAM=((0.09,-0.86,0.66),(0.0,0.0,0.55),70.0)')
C=('KEY_POS=(0.0,-0.6,2.0)' 'KEY_AIM=(0,0,0.10)' 'ORBCAM=((0.09,-0.86,0.21),(0.0,0.0,0.10),70.0)')
r() { [ -s "$1" ] && return 0; shift; "$@"; }
aud() { o=$1; shift; "$@" > "$o.tmp" 2>&1; mv "$o.tmp" "$o"; }
r $S/aud-h.txt aud $S/aud-h.txt env "${H[@]}" AUDIT=1 MASK=$S/mask-h.png python3.11 lamp_site.py dome-black
r $S/aud-c.txt aud $S/aud-c.txt env "${C[@]}" AUDIT=1 MASK=$S/mask-c.png python3.11 lamp_site.py orb-black
for t in black ice red orange amber green blue violet; do
  r $S/h-$t.png env "${H[@]}" LAMP_OUT=$S/h-$t.png python3.11 lamp_site.py dome-$t --samples 128 --scale 0.5 > /dev/null 2>&1
  r $S/c-$t.png env "${C[@]}" LAMP_OUT=$S/c-$t.png python3.11 lamp_site.py orb-$t --samples 128 --scale 0.5 > /dev/null 2>&1
done
for L in 0.5 0.8 1.2; do
  r $S/h-black$L.png env "${H[@]}" TINT_LOAD_SET=black:$L LAMP_OUT=$S/h-black$L.png python3.11 lamp_site.py dome-black --samples 128 --scale 0.5 > /dev/null 2>&1
done
for L in 0.5 0.8 1.2 1.6 2.0 2.5; do
  r $S/c-black$L.png env "${C[@]}" TINT_LOAD_SET=black:$L LAMP_OUT=$S/c-black$L.png python3.11 lamp_site.py orb-black --samples 128 --scale 0.5 > /dev/null 2>&1
done
echo DONE > $S/done.txt
