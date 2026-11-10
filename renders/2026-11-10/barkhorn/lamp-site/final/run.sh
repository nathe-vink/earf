#!/bin/bash
# The lamps' final set (2026-11-10, the owner's decisions): each tint lit by its own LED colour (amber 2200 K: Ember,
# Dust, Acid; 2700 K: Poison, Fog, Smoke; 3000 K: Ice, Haze), the LED faces the only emitters, camera balance 4000 K.
# Core on its angled base with the white light well, studio 0.5 and EV -1 (the glow reads); Hemisphere as proofs r2
# (studio 1, EV -2, no denoiser). Audits and masks first, then the frames. For the site lane once checked and seen.
cd /home/user/earf/spinoffs/barkhorn/companions
D=/home/user/earf/renders/2026-11-10/barkhorn/lamp-site/final; mkdir -p $D/masks $D/audit
BELOW='((0.0,0.0,0.03),(0.0,0.0,0.5),50.0)'
T="red:ember orange:dust amber:acid green:poison blue:ice violet:haze ice:fog black:smoke"
for kv in $T; do k=${kv%%:*}; n=${kv##*:}
  WB=4000 STUDIO=0.5 EV=-1 AUDIT=1 MASK=$D/masks/core-$n.png python3.11 lamp_site.py orb-$k > $D/audit/core-$n.txt 2>&1
  WB=4000 AUDIT=1 MASK=$D/masks/hemisphere-$n.png python3.11 lamp_site.py dome-$k > $D/audit/hemisphere-$n.txt 2>&1
done
WB=4000 STUDIO=0.5 EV=-1 AUDIT=1 MASK=$D/masks/core-row.png python3.11 lamp_site.py lamps-orbs > $D/audit/core-row.txt 2>&1
WB=4000 AUDIT=1 MASK=$D/masks/hemisphere-row.png python3.11 lamp_site.py lamps-domes > $D/audit/hemisphere-row.txt 2>&1
WB=4000 DOMECAM="$BELOW" STUDIO_OFF=key AUDIT=1 MASK=$D/masks/hemisphere-ember-below.png python3.11 lamp_site.py dome-red > $D/audit/hemisphere-ember-below.txt 2>&1
for kv in $T; do k=${kv%%:*}; n=${kv##*:}
  WB=4000 STUDIO=0.5 EV=-1 EXR=0 LAMP_OUT=$D/core-$n.png python3.11 lamp_site.py orb-$k --samples 256 --scale 0.5 > /dev/null 2>&1
done
WB=4000 STUDIO=0.5 EV=-1 EXR=0 LAMP_OUT=$D/core-row.png python3.11 lamp_site.py lamps-orbs --samples 256 --scale 0.5 > /dev/null 2>&1
for kv in $T; do k=${kv%%:*}; n=${kv##*:}
  WB=4000 EXR=0 LAMP_OUT=$D/hemisphere-$n.png python3.11 lamp_site.py dome-$k --samples 512 --scale 0.5 > /dev/null 2>&1
done
WB=4000 EXR=0 DOMECAM="$BELOW" STUDIO_OFF=key LAMP_OUT=$D/hemisphere-ember-below.png python3.11 lamp_site.py dome-red --samples 512 --scale 0.5 > /dev/null 2>&1
WB=4000 EXR=0 LAMP_OUT=$D/hemisphere-row.png python3.11 lamp_site.py lamps-domes --samples 512 --scale 0.5 > /dev/null 2>&1
echo BATCH DONE > $D/done.txt
