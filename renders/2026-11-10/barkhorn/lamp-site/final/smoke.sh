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
# THE PLACEMENT (2026-11-16, the coordinator: the round key's and fill's reflections read as stains on the darker lit
# glass): the key a 3.0 x 0.5 m strip overhead (the off rig's), its reflection on the black shoulder; the fill moved
# behind the lamp as a wash on the back paper (FILL_POS/AIM/W), which the bowl's front cannot see and the ball shows
# only as a slim edge; the paper held at about 30. -under keeps the approved render (from below the moved fill is in
# frame, so that view keeps the old placement)
# Hemisphere (the coordinator, 11:36: the overhead strip read as a slot on the lit picture's shoulder; the bar was the
# fill's reflection, the wash facing down): no key; the fill faces the back paper square (the shade sees only its dark
# back), the world (4000 K grey, even) lifting the paper to about 30; the kicker's rim strip stays
NH=(STUDIO_OFF=key 'FILL_POS=(0.0,0.55,2.1)' 'FILL_AIM=(0.0,1.0,2.1)' FILL_W=0.105 WORLD='#FFD4A5' WORLD_STR=0.82)
# Core: a ball reflects every lamp in front of or above it, so no key; the fill turned to face the back paper square (the
# ball sees only its dark back), and the world (a 4000 K grey, even, no discrete reflection) lifting the floor: the
# paper about 30 top and bottom; the kicker's slim strip on the right edge stays
NC=(STUDIO_OFF=key 'FILL_POS=(0.0,0.55,1.3)' 'FILL_AIM=(0.0,1.0,1.3)' FILL_W=0.25 WORLD='#FFD4A5' WORLD_STR=0.38)
CV=(WB=4000 STUDIO_K=4000 PAPER='#9A9A9A' WORLD='#BDBDBD' EXR=0 'ORBCAM=((0.09,-0.86,0.21),(0.0,0.0,0.10),70.0)')
P=$S/smoke-photometry.txt
if [ ! -s $P ]; then
echo "hemisphere smoke: $(BOUNCES=64 FRAME=dome-black SPP=128 python3.11 launch/isphere.py 2>&1 | grep ISPHERE)" >> $P
echo "hemisphere smoke: $(env PAPER='#9A9A9A' LUX_SPAN=1.4 LUXPROBE=$S/lux.exr python3.11 lamp_site.py dome-black --samples 256 2>&1 | grep -E '^LUXPTS')" >> $P
echo "core smoke: $(FRAME=orb-black SPP=256 python3.11 launch/isphere.py 2>&1 | grep ISPHERE)" >> $P
fi
aud $D/audit/hemisphere-smoke-direct.txt env "${HV[@]}" "${NH[@]}" DOMECAM="$DIR" AUDIT=1 MASK=$D/masks/hemisphere-smoke-direct.png python3.11 lamp_site.py dome-black
true || aud $D/audit/hemisphere-smoke-under.txt env "${HV[@]}" DOMECAM="$UND" AUDIT=1 MASK=$D/masks/hemisphere-smoke-under.png python3.11 lamp_site.py dome-black
aud $D/audit/core-smoke.txt env "${CV[@]}" "${NC[@]}" STUDIO=0.5 EV=-1 AUDIT=1 MASK=$D/masks/core-smoke.png python3.11 lamp_site.py orb-black
env "${HV[@]}" "${NH[@]}" DOMECAM="$DIR" LAMP_OUT=$S/n-hsd.png python3.11 lamp_site.py dome-black --samples 128 --scale 1.0 > /dev/null 2>&1 && mv $S/n-hsd.png $D/hemisphere-smoke-direct.png; fit $D/hemisphere-smoke-direct.png
true || env "${HV[@]}" DOMECAM="$UND" LAMP_OUT=$S/n-hsu.png python3.11 lamp_site.py dome-black --samples 128 --scale 1.0 > /dev/null 2>&1 && mv $S/n-hsu.png $D/hemisphere-smoke-under.png; fit $D/hemisphere-smoke-under.png
env "${CV[@]}" "${NC[@]}" STUDIO=0.5 EV=-1 LAMP_OUT=$S/n-cs.png python3.11 lamp_site.py orb-black --samples 256 --scale 1.0 > /dev/null 2>&1 && mv $S/n-cs.png $D/core-smoke.png
echo DONE > $S/smoke-done.txt
