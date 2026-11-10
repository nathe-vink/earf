#!/bin/bash
# the proof batch (2026-11-10, the owner's picks): Core Ø140 concentric, Hemisphere option 3 (bare ring board, 1,000 lm)
cd /home/user/earf/spinoffs/barkhorn/companions
D=/home/user/earf/renders/2026-11-10/barkhorn/lamp-site/proofs
BELOW='((0.0,0.0,0.03),(0.0,0.0,0.5),50.0)'
for v in "core-ice orb-blue" "core-ember orb-red" "hemi-ember dome-red" "hemi-ice dome-blue"; do set -- $v
  AUDIT=1 MASK=$D/masks/$1.png python3.11 lamp_site.py $2 > $D/$1.audit.txt 2>&1; done
DOMECAM="$BELOW" STUDIO_OFF=key AUDIT=1 MASK=$D/masks/hemi-ember-below.png python3.11 lamp_site.py dome-red > $D/hemi-ember-below.audit.txt 2>&1
LUXPROBE=$D/lux-ember.exr python3.11 lamp_site.py dome-red --samples 256 > $D/lux-ember.txt 2>&1
LUXPROBE=$D/lux-ice.exr python3.11 lamp_site.py dome-blue --samples 256 > $D/lux-ice.txt 2>&1
LIGHTS_OFF=1 LUXPROBE=$D/lux-off.exr python3.11 lamp_site.py dome-red --samples 64 > $D/lux-off.txt 2>&1
LAMP_OUT=$D/core-ice.png python3.11 lamp_site.py orb-blue --samples 256 --scale 0.5 > $D/core-ice.log 2>&1
LAMP_OUT=$D/core-ember.png python3.11 lamp_site.py orb-red --samples 256 --scale 0.5 > $D/core-ember.log 2>&1
LAMP_OUT=$D/hemi-ember.png python3.11 lamp_site.py dome-red --samples 768 --scale 0.5 > $D/hemi-ember.log 2>&1
LAMP_OUT=$D/hemi-ice.png python3.11 lamp_site.py dome-blue --samples 768 --scale 0.5 > $D/hemi-ice.log 2>&1
DOMECAM="$BELOW" STUDIO_OFF=key LAMP_OUT=$D/hemi-ember-below.png python3.11 lamp_site.py dome-red --samples 768 --scale 0.5 > $D/hemi-ember-below.log 2>&1
echo BATCH DONE > $D/done.txt
