#!/bin/bash
# The lamps' final set (the owner, "Go", 2026-11-11): each tint in its LED colour (lamp_site.LED_CCT: 4000 K for Dust,
# Acid, Ice, Smoke; Ember 2200 K; Poison, Fog 2700 K; Haze 3000 K) and its shell's loading (lamp_site.TINT_LOAD: Dust,
# Acid, Ice a 3x custom pour; Smoke the speakers' own pour), the LED faces the only emitters. Full size, framed closer, on
# a neutral grey backdrop (paper #9A9A9A, the studio lights at 4000 K, the camera at 4000 K). Core: studio 0.5, EV -1,
# 256 samples, denoised. Hemisphere: studio 1, EV -2, 192 samples (the row 256), the OpenImageDenoise denoiser on the
# beauty (DENOISE=1; emitters, flux, exposure unchanged). Photometry, audits and masks first. Skips what is done, so it
# is rerun until done.txt (the container restarts).
cd /home/user/earf/spinoffs/barkhorn/companions
D=/home/user/earf/renders/2026-11-10/barkhorn/lamp-site/final; mkdir -p $D/masks $D/audit
export WB=4000 STUDIO_K=4000 PAPER='#9A9A9A' WORLD='#BDBDBD' EXR=0
export ORBCAM='((0.09,-0.86,0.21),(0.0,0.0,0.10),70.0)'
DCAM='((0.04,-0.66,0.98),(0.0,-0.05,0.34),45.0)'
BELOW='((0.0,0.0,0.03),(0.0,0.0,0.5),50.0)'
r() { [ -s "$1" ] && return 0; shift; "$@"; }
aud() { o=$1; shift; "$@" > "$o.tmp" 2>&1; mv "$o.tmp" "$o"; }
T="red:ember orange:dust amber:acid green:poison blue:ice violet:haze ice:fog black:smoke"
# photometry: lumens out of Core's ball; Hemisphere's lumens below and above the rim plane, and the table's lux 0.5 m down
P=$D/photometry.txt
if [ ! -s $P ]; then
  for kv in $T; do k=${kv%%:*}; n=${kv##*:}
    echo "core $n: $(FRAME=orb-$k SPP=256 python3.11 launch/isphere.py 2>&1 | grep ISPHERE)"
    echo "hemisphere $n: $(BOUNCES=64 FRAME=dome-$k SPP=128 python3.11 launch/isphere.py 2>&1 | grep ISPHERE)"
    echo "hemisphere $n: $(LUXPROBE=/tmp/claude-0/-home-user-earf/e73bd455-48f8-5f69-9a3b-fa1e22e4e1e9/scratchpad/lux-$n.exr python3.11 lamp_site.py dome-$k --samples 256 2>&1 | grep LUX)"
  done > $P.tmp && mv $P.tmp $P
fi
for kv in $T; do k=${kv%%:*}; n=${kv##*:}
  r $D/audit/core-$n.txt aud $D/audit/core-$n.txt env STUDIO=0.5 EV=-1 AUDIT=1 MASK=$D/masks/core-$n.png python3.11 lamp_site.py orb-$k
  r $D/audit/hemisphere-$n.txt aud $D/audit/hemisphere-$n.txt env DOMECAM="$DCAM" AUDIT=1 MASK=$D/masks/hemisphere-$n.png python3.11 lamp_site.py dome-$k
done
r $D/audit/core-row.txt aud $D/audit/core-row.txt env STUDIO=0.5 EV=-1 AUDIT=1 MASK=$D/masks/core-row.png python3.11 lamp_site.py lamps-orbs
r $D/audit/hemisphere-row.txt aud $D/audit/hemisphere-row.txt env AUDIT=1 MASK=$D/masks/hemisphere-row.png python3.11 lamp_site.py lamps-domes
r $D/audit/hemisphere-ember-below.txt aud $D/audit/hemisphere-ember-below.txt env DOMECAM="$BELOW" STUDIO_OFF=key AUDIT=1 MASK=$D/masks/hemisphere-ember-below.png python3.11 lamp_site.py dome-red
for kv in $T; do k=${kv%%:*}; n=${kv##*:}
  r $D/core-$n.png env STUDIO=0.5 EV=-1 LAMP_OUT=$D/core-$n.png python3.11 lamp_site.py orb-$k --samples 256 --scale 1.0 > /dev/null 2>&1
done
r $D/core-row.png env STUDIO=0.5 EV=-1 LAMP_OUT=$D/core-row.png python3.11 lamp_site.py lamps-orbs --samples 256 --scale 1.0 > /dev/null 2>&1
for kv in $T; do k=${kv%%:*}; n=${kv##*:}
  r $D/hemisphere-$n.png env DOMECAM="$DCAM" DENOISE=1 LAMP_OUT=$D/hemisphere-$n.png python3.11 lamp_site.py dome-$k --samples 192 --scale 1.0 > /dev/null 2>&1
done
r $D/hemisphere-row.png env DENOISE=1 LAMP_OUT=$D/hemisphere-row.png python3.11 lamp_site.py lamps-domes --samples 256 --scale 1.0 > /dev/null 2>&1
r $D/hemisphere-ember-below.png env DOMECAM="$BELOW" STUDIO_OFF=key DENOISE=1 LAMP_OUT=$D/hemisphere-ember-below.png python3.11 lamp_site.py dome-red --samples 192 --scale 1.0 > /dev/null 2>&1
echo DONE > $D/done.txt
