#!/bin/bash
# STEP 2 (2026-11-17, the coordinator, after the owner's yes to the mix): rendered once with the decided loadings
# (lamp_site.py's default since 5fa6ef94) straight into final/: hemisphere-row, core-row, hemisphere-cluster, and the lit
# pendants that kept the old discs, hemisphere-dust/-poison/-fog hero and direct (their under views stay). The placement
# leaves no studio lamp's outline on any lit dome or ball: no key; the fill a wash on the back paper, facing it (a
# one-sided lamp the glass cannot see); the world (even, no discrete reflection) lifting the paper. Hemisphere's NH,
# Core's NC (final-mix/mix.sh). Every picture has two audits: AUDIT (nothing hidden, nothing in frame) and the
# reflection audit (launch/reflcheck.py: the frame at half size with and without STUDIO_NOGLOSS=1, their difference
# every studio reflection on the glass; audit/<name>-refl.txt, masks/<name>-refl.png). Reruns skip what exists.
cd /home/user/earf/spinoffs/barkhorn/companions
D=/home/user/earf/renders/2026-11-10/barkhorn/lamp-site/final
S=/tmp/claude-0/-home-user-earf/e73bd455-48f8-5f69-9a3b-fa1e22e4e1e9/scratchpad/step2; mkdir -p $S
FPY=/home/user/earf/.venv-fab/bin/python
r() { [ -s "$1" ] && return 0; shift; "$@"; }
aud() { o=$1; shift; "$@" > "$o.tmp" 2>&1; mv "$o.tmp" "$o"; }
fit() { python3 -c "
import sys,os; from PIL import Image
p=sys.argv[1]; im=Image.open(p)
if im.mode=='RGBA' and im.getchannel('A').getextrema()==(255,255): im=im.convert('RGB')
im.save(p,optimize=True); print(p, os.path.getsize(p))" "$1"; }
LIT=(WB=4000 STUDIO_K=4000 PAPER='#9A9A9A' EXR=0 DENOISE=1)
NH=(STUDIO_OFF=key 'FILL_POS=(0.0,0.55,2.1)' 'FILL_AIM=(0.0,1.0,2.1)' FILL_W=0.105 WORLD='#FFD4A5' WORLD_STR=0.82)
NC=(STUDIO_OFF=key 'FILL_POS=(0.0,0.55,1.3)' 'FILL_AIM=(0.0,1.0,1.3)' FILL_W=0.25 WORLD='#FFD4A5' WORLD_STR=0.38)
DCAM='((0.04,-0.66,0.98),(0.0,-0.05,0.34),45.0)'
DIR='((0.0,-1.04,0.55),(0.0,0.0,0.55),90.0)'
# one picture: name, frame, samples, then its env
one() { n=$1; f=$2; sp=$3; shift 3      # scratch targets (final/ holds the old files under the same names), then installed
  r $S/$n.aud aud $S/$n.aud env "$@" AUDIT=1 MASK=$S/m-$n.png python3.11 lamp_site.py $f
  r $S/$n-r0.png env "$@" LAMP_OUT=$S/$n-r0.png python3.11 lamp_site.py $f --samples 48 --scale 0.5 > /dev/null 2>&1
  r $S/$n-r1.png env "$@" STUDIO_NOGLOSS=1 LAMP_OUT=$S/$n-r1.png python3.11 lamp_site.py $f --samples 48 --scale 0.5 > /dev/null 2>&1
  r $S/$n.refl aud $S/$n.refl $FPY launch/reflcheck.py $S/$n-r0.png $S/$n-r1.png $S/m-$n-refl.png
  r $S/$n-full.png env "$@" LAMP_OUT=$S/$n-full.png python3.11 lamp_site.py $f --samples $sp --scale 1.0 > /dev/null 2>&1 && fit $S/$n-full.png
  [ -s $S/$n-full.png ] || return
  rm -f $D/masks/$n-key.png $D/masks/$n-fill.png $D/masks/$n-kicker.png
  cp $S/$n.aud $D/audit/$n.txt; cp $S/$n.refl $D/audit/$n-refl.txt
  for m in $S/m-$n-*.png; do b=$(basename $m); case $b in m-$n-direct-*) continue;; esac; cp $m $D/masks/${b#m-}; done
  cp $S/$n-full.png $D/$n.png
}
for kv in orange:dust green:poison ice:fog; do k=${kv%%:*}; t=${kv##*:}
  one hemisphere-$t dome-$k 192 "${LIT[@]}" "${NH[@]}" DOMECAM="$DCAM"
  one hemisphere-$t-direct dome-$k 128 "${LIT[@]}" "${NH[@]}" DOMECAM="$DIR"
done
one hemisphere-row lamps-domes ${ROW_SPP:-768} "${LIT[@]}" "${NH[@]}"
one core-row lamps-orbs 256 "${LIT[@]}" "${NC[@]}" STUDIO=0.5 EV=-1
# the cluster's camera looks up: the moved fill stood in its frame (10.6 %), so no studio lamp at all, the world alone
# lifting the paper (at 1.0 the paper as the old cluster's, about 31 to 61 top to bottom)
one hemisphere-cluster cluster ${CLUS_SPP:-512} "${LIT[@]}" STUDIO_OFF=key,fill WORLD='#FFD4A5' WORLD_STR=1.0
echo DONE > /home/user/earf/renders/2026-11-17/barkhorn/lamp-site/step2-done.txt
