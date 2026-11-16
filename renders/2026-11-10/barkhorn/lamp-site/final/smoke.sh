#!/bin/bash
# B-SMOKE (2026-11-16, decided): Smoke at Hemisphere 1.2x and Core 0.6x (lamp_site.py's defaults since this commit).
# The photometry for Smoke and the three Smoke singles at their names, in views.sh's and run.sh's rigs, with the
# corrected method. Every other picture holds until the owner picks the direction (rows, core-row-day, cluster,
# hemisphere-smoke).
cd /home/user/earf/spinoffs/barkhorn/companions
D=/home/user/earf/renders/2026-11-10/barkhorn/lamp-site/final
S=/tmp/claude-0/-home-user-earf/e73bd455-48f8-5f69-9a3b-fa1e22e4e1e9/scratchpad
DIR='((0.0,-1.04,0.55),(0.0,0.0,0.55),90.0)'
UND='((0.287,-0.496,0.10),(0.0,0.0,0.52),60.0)'
fit() { python3 -c "
from PIL import Image; import os,sys
p=sys.argv[1]; im=Image.open(p)
if os.path.getsize(p)>5e6 and im.mode=='RGBA' and im.getchannel('A').getextrema()==(255,255): im.convert('RGB').save(p,optimize=True)" "$1"; }
aud() { o=$1; shift; "$@" > "$o.tmp" 2>&1; mv "$o.tmp" "$o"; }
# the singles' recipes' exports (views.sh for Hemisphere; core-final.sh for Core), which the first pass left out
HV=(WB=4000 STUDIO_K=4000 PAPER='#9A9A9A' WORLD='#BDBDBD' EXR=0 DENOISE=1)
CV=(WB=4000 STUDIO_K=4000 PAPER='#9A9A9A' WORLD='#BDBDBD' EXR=0 'ORBCAM=((0.09,-0.86,0.21),(0.0,0.0,0.10),70.0)')
P=$S/smoke-photometry.txt
if [ ! -s $P ]; then
echo "hemisphere smoke: $(BOUNCES=64 FRAME=dome-black SPP=128 python3.11 launch/isphere.py 2>&1 | grep ISPHERE)" >> $P
echo "hemisphere smoke: $(env PAPER='#9A9A9A' LUX_SPAN=1.4 LUXPROBE=$S/lux.exr python3.11 lamp_site.py dome-black --samples 256 2>&1 | grep -E '^LUXPTS')" >> $P
echo "core smoke: $(FRAME=orb-black SPP=256 python3.11 launch/isphere.py 2>&1 | grep ISPHERE)" >> $P
fi
aud $D/audit/hemisphere-smoke-direct.txt env "${HV[@]}" DOMECAM="$DIR" AUDIT=1 MASK=$D/masks/hemisphere-smoke-direct.png python3.11 lamp_site.py dome-black
aud $D/audit/hemisphere-smoke-under.txt env "${HV[@]}" DOMECAM="$UND" AUDIT=1 MASK=$D/masks/hemisphere-smoke-under.png python3.11 lamp_site.py dome-black
aud $D/audit/core-smoke.txt env "${CV[@]}" STUDIO=0.5 EV=-1 AUDIT=1 MASK=$D/masks/core-smoke.png python3.11 lamp_site.py orb-black
env "${HV[@]}" DOMECAM="$DIR" LAMP_OUT=$S/n-hsd.png python3.11 lamp_site.py dome-black --samples 128 --scale 1.0 > /dev/null 2>&1 && mv $S/n-hsd.png $D/hemisphere-smoke-direct.png; fit $D/hemisphere-smoke-direct.png
env "${HV[@]}" DOMECAM="$UND" LAMP_OUT=$S/n-hsu.png python3.11 lamp_site.py dome-black --samples 128 --scale 1.0 > /dev/null 2>&1 && mv $S/n-hsu.png $D/hemisphere-smoke-under.png; fit $D/hemisphere-smoke-under.png
env "${CV[@]}" STUDIO=0.5 EV=-1 LAMP_OUT=$S/n-cs.png python3.11 lamp_site.py orb-black --samples 256 --scale 1.0 > /dev/null 2>&1 && mv $S/n-cs.png $D/core-smoke.png
echo DONE > $S/smoke-done.txt
