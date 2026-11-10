#!/bin/bash
# Core's base, as drawn and angled (a look for the owner, 2026-11-10): Ice, the hero camera, the studio, the lamp off.
# (run after the r2 batch)
D=/home/user/earf/renders/2026-11-10/barkhorn/lamp-site/proofs/angled
cd /home/user/earf/spinoffs/barkhorn/companions
WB=4000 LIGHTS_OFF=1 EXR=0 LAMP_OUT=$D/core-ice-base-as-drawn.png python3.11 lamp_site.py orb-blue --samples 128 --scale 0.5 > /dev/null 2>&1
WB=4000 LIGHTS_OFF=1 EXR=0 CORE_ANGLED=1 LAMP_OUT=$D/core-ice-base-angled.png python3.11 lamp_site.py orb-blue --samples 128 --scale 0.5 > /dev/null 2>&1
echo DONE > $D/done.txt
