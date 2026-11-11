#!/bin/bash
# views.sh's last two, again (2026-11-11 21:20): the cluster without the kicker (it sat in frame) and with the heights
# re-staggered; hemisphere-row.png re-rendered (views.sh skipped it: the old file was still there). Rerun until views2-done.txt.
cd /home/user/earf/spinoffs/barkhorn/companions
D=/home/user/earf/renders/2026-11-10/barkhorn/lamp-site/final
export WB=4000 STUDIO_K=4000 PAPER='#9A9A9A' WORLD='#BDBDBD' EXR=0 DENOISE=1
r() { [ -s "$1" ] && return 0; shift; "$@"; }
aud() { o=$1; shift; "$@" > "$o.tmp" 2>&1; mv "$o.tmp" "$o"; }
r $D/audit/hemisphere-cluster.txt aud $D/audit/hemisphere-cluster.txt env AUDIT=1 MASK=$D/masks/hemisphere-cluster.png python3.11 lamp_site.py cluster
r $D/hemisphere-cluster.png env LAMP_OUT=$D/hemisphere-cluster.png python3.11 lamp_site.py cluster --samples 128 --scale 1.0 > /dev/null 2>&1
r $D/audit/hemisphere-row-disc95.txt aud $D/audit/hemisphere-row-disc95.txt env AUDIT=1 MASK=$D/masks/hemisphere-row.png python3.11 lamp_site.py lamps-domes
r $D/hemisphere-row.png env LAMP_OUT=$D/hemisphere-row.png python3.11 lamp_site.py lamps-domes --samples 256 --scale 1.0 > /dev/null 2>&1
echo DONE > $D/views2-done.txt
