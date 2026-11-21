#!/bin/bash
# Core Ember LIT-e (2026-11-21, the critics on LIT-d): LIT-d with the spot in the house lights' colour (FFF4E8, as a
# bi-colour LED or a quarter CTO would give), its emitting radius 3 mm, a real black flag under its snoot (a level card
# 2.5 cm off the floor, 1-6 cm in front of it, 4 cm wide, so the beam's lower edge meets the base's foot), 8 W. Half-size
# test: base 48/1/1 (L* 5.9), front floor 16.8. Writes house9/core-ember-lit-e.png.
# (LIT-d's header follows)
# Core Ember LIT-d (2026-11-21, the critics on LIT-c: the base read black): LIT-c plus a small real spot near the
# camera line, low (0.19, -0.405, z 0.03 m), a 12 deg snoot aimed at the base (z 0.015), 7.5 W, white, no linking (its cone
# covers the base, not the ball, so the ball shows no glint); and GUIDE_ORB=1 (path guiding: the grain 40 % lower at the
# same cost). Half-size tests: 12 deg at 6 W base 43/1/1, at 9 W 51/1/1. Writes house9/core-ember-lit-d.png.
# (LIT-c header follows)
# Core Ember LIT, round 6 (LIT-c;
# LIT plus: HOUSE_SOFTBOX_SEEN=0 (the softboxes flagged off), DENOISE_PASSES=RGB (colour-only guides: no seams),
# HOUSE_LAMP_K=key:0 (the key off in the lit shot: it lit the left floor to 37.9 against the lamp's pool; the walls
# unchanged), and the exposure set from the pendant LIT round 6 (house9, mask A 39.1, B 40.8) by half-size denoised
# tests (which read about 0.9 under the full frame): EV -2.85 with the studio 0.6 x 2^0.25 = 0.714 (walls held), half
# size A 39.1 / B 39.2, so about 40.0 full. Writes house9/core-ember-lit.png.
cd /home/user/earf/spinoffs/barkhorn/companions
D=/home/user/earf/renders/2026-11-20/barkhorn/lamp-site/house9; mkdir -p $D/audit
S=/tmp/claude-0/-home-user-earf/e73bd455-48f8-5f69-9a3b-fa1e22e4e1e9/scratchpad/et9; mkdir -p $S
FPY=/home/user/earf/.venv-fab/bin/python
n=core-ember-lit-e
SET="GUIDE_ORB=1 HOUSE_BOUNCE=0,0,0,0,0.19,-0.405,0.03,12,8,0.015 HOUSE_BOUNCE_COLOR=FFF4E8 HOUSE_BOUNCE_CUT=0.01,0.06,0.0252,0.04 HOUSE_BOUNCE_SOFT=0.003 HOUSE_LAMP_K=key:0 HOUSE_SOFTBOX_SEEN=0 DENOISE_PASSES=RGB HOUSE_STUDIO=0.714 HOUSE_EV=-2.85 HOUSE_SWEEP_AO=0 HOUSE_ROOM_TRANS=1 HOUSE_S=0.19 CORE_DOCK=0 HOUSE_CUT2=fill,1.0 HOUSE_FLOORCARD=0.0755,2.5,0.0005,-1,1 HOUSE_BG=1.16"
[ -s $D/audit/$n.txt ] || { env $SET "HOUSE_FLAGS=horn cutter" AUDIT=1 MASK=$S/m-$n.png python3.11 lamp_site.py house-orb-red > $S/$n.aud 2>&1 && \
    grep -E "^AUDIT|HIDDENCAST|CASTCHECK|  (in|out) " $S/$n.aud > $D/audit/$n.txt; }
[ -s $D/$n.png ] || { env $SET "HOUSE_FLAGS=horn cutter" EXR=0 DENOISE=1 LAMP_OUT=$S/$n-raw.png python3.11 lamp_site.py house-orb-red --samples 512 > $S/$n.log 2>&1 && \
  $FPY launch/house_finish.py $S/$n-raw.png $D/$n.png > /dev/null && ls -la $D/$n.png && date -u; }
