#!/bin/bash
# Core Ember LIT, round 3 (the coordinator 02:33): as round 2 (ember-tests2.sh, 338cb60a: studio 0.8 at -3.5 EV, the
# floor cutters) with the base's liner in optical contact (BASE_CONTACT, the default since 63609cbf). Quarter size, gap
# against contact: the base's lip top L*/C* 2.0/7.8 -> 5.9/24.6, the flanks +8 to +10 C*, the ball's glow unchanged.
# Walls off, as the Ember set.
cd /home/user/earf/spinoffs/barkhorn/companions
D=/home/user/earf/renders/2026-11-20/barkhorn/lamp-site/house6; mkdir -p $D/audit
S=/tmp/claude-0/-home-user-earf/e73bd455-48f8-5f69-9a3b-fa1e22e4e1e9/scratchpad/et6; mkdir -p $S
FPY=/home/user/earf/.venv-fab/bin/python
E=(HOUSE_S=0.19 CORE_DOCK=0 HOUSE_CUT2=fill,1.0 "HOUSE_FLAGS=horn cutter" BASE_CONTACT=1 HOUSE_STUDIO=0.8 HOUSE_EV=-3.5 HOUSE_BG=1.16)
n=core-ember-lit
[ -s $D/audit/$n.txt ] || { env "${E[@]}" AUDIT=1 MASK=$S/m-$n.png python3.11 lamp_site.py house-orb-red > $S/$n.aud 2>&1 && \
    grep -E "^AUDIT|HIDDENCAST|CASTCHECK|  (in|out) " $S/$n.aud > $D/audit/$n.txt; }
[ -s $D/$n.png ] || { env "${E[@]}" EXR=0 DENOISE=1 LAMP_OUT=$S/$n-raw.png python3.11 lamp_site.py house-orb-red --samples 512 > $S/$n.log 2>&1 && \
    $FPY launch/house_finish.py $S/$n-raw.png $D/$n.png > /dev/null && ls -la $D/$n.png; }
