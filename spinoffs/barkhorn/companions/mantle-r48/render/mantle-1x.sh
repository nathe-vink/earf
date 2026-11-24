#!/bin/bash
# Mantle at the speakers' dye, 1x (the owner, 2026-11-24, "Speakers dye"): the deck polished top and underside, satin outer
# edge, nothing white; the physical light model on the house ground; then the emitter and hidden-mesh audits.
#   LOAD=1 render/mantle-1x.sh VIEW TINT OUTDIR [SCALE SAMPLES]     VIEW: three-quarter | cover | top
# LOAD is the deck's dye as a share of the speakers' cabinets' loading: 1 (the default) or 0.1, whichever the owner picks.
# Run from anywhere in the repo, on the system Python (python3.11 with bpy). Full size is SCALE 1 (1600 x 2000), 128 samples.
set -u
LOAD=${LOAD:-1}; view=$1; c=$2; out=$3; sc=${4:-1.0}; sm=${5:-128}
R=$(cd "$(dirname "$0")" && pwd); M=$(dirname "$R"); ROOT=$(cd "$M" && git rev-parse --show-toplevel)
mkdir -p "$out"; out=$(cd "$out" && pwd)
declare -A CV=([ember]=solid [poison]=solid [haze]=solid [fog]=solid [dust]=solid-strong:2.25 [acid]=solid-strong:2.45 [ice]=solid-strong:3.05 [smoke]=solid-strong:4.30)
case $view in
  three-quarter) A="$(cat $R/house.args)"; n=mantle-house-$c;;
  cover)         A="$(cat $R/house.args) --cover ${CV[$c]} --cover-bounces 128"; n=mantle-house-$c-cover;;
  top)           A="$(cat $R/house-nocam.args) --house-cam 0 89.5 1.37 70 --house-aim 0 0 0.1"; n=mantle-house-$c-top;;
  *) echo "unknown view $view"; exit 2;;
esac
DAY="dusk --model out-strata-v3 --tint-mode custom --day --strip 0 --core-glow 0 --exposure 0 --edge-frost 0.55 --base-tint smoke-2074 --size 1600 2000 --scale $sc --samples $sm --paper #F7F0E8 --wear 0 --no-top-bevel --vignette 0 --blank-label --grain 0.004 --platter-clear --deck-load $LOAD"
B="--black-posts --side-fix --black-bearing --satin-underside --black-hub --black-hardware --edge-c --physical --polished-underside"
s=$(date +%s)
(cd "$M" && python3.11 v3_day.py "$out/$n.png" $B $A -- $DAY --colour sp-$c) > "$out/$n.log" 2>&1; rc=$?
cd "$ROOT"
python3.11 spinoffs/barkhorn/night-pictures/gt_audit.py "$out/$n.blend" --res 1600 2000 2>&1 | grep "^GT" > "$out/$n.gt.txt"
python3.11 spinoffs/barkhorn/night-pictures/scene_audit.py "$out/$n.blend" 2>&1 | grep -E "IN FRAME|^out|no mesh|seen directly|casts no|hidden" > "$out/$n.audit.txt"
python3.11 "$R/castcheck.py" "$out/$n.blend" --mask "$out/$n-mask.png" 2>&1 | grep -E "^HIDDENCAST|^   |^RAYVIS|^LINK|^CASTCHECK" > "$out/$n.cast.txt"
echo "$n LOAD=$LOAD rc=$rc $(( $(date +%s)-s ))s | $(grep 'emitter check' "$out/$n.gt.txt") | gt flags $(grep -c 'IN FRAME\|seen through' "$out/$n.gt.txt") | audit $(grep -c 'IN FRAME' "$out/$n.audit.txt") | $(grep -c 'no mesh is hidden' "$out/$n.audit.txt") no-hidden | $(grep '^HIDDENCAST' "$out/$n.cast.txt") | $(grep '^CASTCHECK' "$out/$n.cast.txt")"
