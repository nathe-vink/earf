#!/bin/bash
# B-MIX: the two rows first (the coordinator: what the owner looks at first), the same recipes as mix.sh, LOAD_MIX=1
cd /home/user/earf/spinoffs/barkhorn/companions
export LOAD_MIX=1
D=/home/user/earf/renders/2026-11-16/barkhorn/lamp-site/final-mix
r() { [ -s "$1" ] && return 0; shift; "$@"; }
aud() { o=$1; shift; "$@" > "$o.tmp" 2>&1; mv "$o.tmp" "$o"; }
LIT=(WB=4000 STUDIO_K=4000 PAPER='#9A9A9A' WORLD='#BDBDBD' EXR=0)
r $D/audit/hemisphere-row.txt aud $D/audit/hemisphere-row.txt env "${LIT[@]}" DENOISE=1 AUDIT=1 MASK=$D/masks/hemisphere-row.png python3.11 lamp_site.py lamps-domes
r $D/hemisphere-row.png env "${LIT[@]}" DENOISE=1 LAMP_OUT=$D/hemisphere-row.png.part.png python3.11 lamp_site.py lamps-domes --samples 256 --scale 1.0 > /dev/null 2>&1 && mv $D/hemisphere-row.png.part.png $D/hemisphere-row.png
export ORBCAM='((0.09,-0.86,0.21),(0.0,0.0,0.10),70.0)'
r $D/audit/core-row.txt aud $D/audit/core-row.txt env "${LIT[@]}" STUDIO=0.5 EV=-1 AUDIT=1 MASK=$D/masks/core-row.png python3.11 lamp_site.py lamps-orbs
r $D/core-row.png env "${LIT[@]}" STUDIO=0.5 EV=-1 LAMP_OUT=$D/core-row.png.part.png python3.11 lamp_site.py lamps-orbs --samples 256 --scale 1.0 > /dev/null 2>&1 && mv $D/core-row.png.part.png $D/core-row.png
echo DONE > $D/rows-done.txt
