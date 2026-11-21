#!/bin/bash
# Core Ember OFF, round 3 (the coordinator 23:37: the base's lower flanks and bottom band near-black once the floor
# cutters darkened the floor it mirrors). As round 2 (ember-tests2.sh), plus HOUSE_FLOORCARD: the floor round the base
# spared for the base alone, a flat ring 75.5 mm to 2.5 m from its axis at the floor's albedo (0.8), lit as the floor
# is without the cutters' shade, seen by the base and the ball (in reflections and through the pour), never by the
# camera; it casts nothing and is clear from below, so the floor in frame is unchanged (quarter size: corners within
# 0.3 L* of round 2; base below L* 20 11.2 %, round 1 13.8 %, round 2 25.8 %).
cd /home/user/earf/spinoffs/barkhorn/companions
D=/home/user/earf/renders/2026-11-20/barkhorn/lamp-site/house5; mkdir -p $D/audit
S=/tmp/claude-0/-home-user-earf/e73bd455-48f8-5f69-9a3b-fa1e22e4e1e9/scratchpad/et5; mkdir -p $S
FPY=/home/user/earf/.venv-fab/bin/python
E=(HOUSE_S=0.19 CORE_DOCK=0 HOUSE_CUT2=fill,1.0 "HOUSE_FLAGS=horn cutter" HOUSE_FLOORCARD=0.0755,2.5,0.0005,0.8,1 LIGHTS_OFF=1 HOUSE_BG=1.16)
n=core-ember-off
[ -s $D/audit/$n.txt ] || { env "${E[@]}" AUDIT=1 MASK=$S/m-$n.png python3.11 lamp_site.py house-orb-red > $S/$n.aud 2>&1 && \
    grep -E "^AUDIT|HIDDENCAST|CASTCHECK|  (in|out) " $S/$n.aud > $D/audit/$n.txt; }
[ -s $D/$n.png ] || { env "${E[@]}" EXR=0 DENOISE=1 LAMP_OUT=$S/$n-raw.png python3.11 lamp_site.py house-orb-red --samples 128 > $S/$n.log 2>&1 && \
    $FPY launch/house_finish.py $S/$n-raw.png $D/$n.png > /dev/null && ls -la $D/$n.png; }
