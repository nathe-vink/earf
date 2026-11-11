#!/bin/bash
# The finishing batch (the coordinator, 2026-11-10 23:50): Dust and Acid at 2700 K on both lamps (lamp_site.LED_CCT);
# both rows and Hemisphere Smoke clean enough for the site. Everything else as run.sh (camera, exposure, studio, emitters).
# The Hemisphere row and Smoke: 1024 samples and the OpenImageDenoise denoiser on the beauty (DENOISE=1); the emitters,
# their flux and the exposure unchanged. Skips what is done, so it can be rerun until done.txt.
cd /home/user/earf/spinoffs/barkhorn/companions
r() { [ -s "$1" ] && return 0; shift; "$@"; }
aud() { o=$1; shift; "$@" > "$o.tmp" 2>&1; mv "$o.tmp" "$o"; }
D=/home/user/earf/renders/2026-11-10/barkhorn/lamp-site/final
for kv in orange:dust amber:acid; do k=${kv%%:*}; n=${kv##*:}
  r $D/audit/core-$n.txt aud $D/audit/core-$n.txt env WB=4000 STUDIO=0.5 EV=-1 AUDIT=1 MASK=$D/masks/core-$n.png python3.11 lamp_site.py orb-$k
  r $D/audit/hemisphere-$n.txt aud $D/audit/hemisphere-$n.txt env WB=4000 AUDIT=1 MASK=$D/masks/hemisphere-$n.png python3.11 lamp_site.py dome-$k
  r $D/core-$n.png env WB=4000 STUDIO=0.5 EV=-1 EXR=0 LAMP_OUT=$D/core-$n.png python3.11 lamp_site.py orb-$k --samples 256 --scale 0.5 > /dev/null 2>&1
done
r $D/audit/core-row.txt aud $D/audit/core-row.txt env WB=4000 STUDIO=0.5 EV=-1 AUDIT=1 MASK=$D/masks/core-row.png python3.11 lamp_site.py lamps-orbs
r $D/audit/hemisphere-row.txt aud $D/audit/hemisphere-row.txt env WB=4000 AUDIT=1 MASK=$D/masks/hemisphere-row.png python3.11 lamp_site.py lamps-domes
r $D/core-row.png env WB=4000 STUDIO=0.5 EV=-1 EXR=0 LAMP_OUT=$D/core-row.png python3.11 lamp_site.py lamps-orbs --samples 256 --scale 0.5 > /dev/null 2>&1
for kv in orange:dust amber:acid; do k=${kv%%:*}; n=${kv##*:}
  r $D/hemisphere-$n.png env WB=4000 EXR=0 LAMP_OUT=$D/hemisphere-$n.png python3.11 lamp_site.py dome-$k --samples 512 --scale 0.5 > /dev/null 2>&1
done
r $D/hemisphere-smoke.png env WB=4000 EXR=0 DENOISE=1 LAMP_OUT=$D/hemisphere-smoke.png python3.11 lamp_site.py dome-black --samples 1024 --scale 0.5 > /dev/null 2>&1
r $D/hemisphere-row.png env WB=4000 EXR=0 DENOISE=1 LAMP_OUT=$D/hemisphere-row.png python3.11 lamp_site.py lamps-domes --samples 1024 --scale 0.5 > /dev/null 2>&1
echo DONE > $D/done.txt
