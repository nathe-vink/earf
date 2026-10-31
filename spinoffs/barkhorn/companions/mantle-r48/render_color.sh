#!/bin/sh
# Round 48, the color pass (the coordinator: more color). Stock = TruCast 2423 (Ember), Beer-Lambert from its chart;
# custom = EARF's own color poured at a lighter dye loading (its `deep` after 25 mm), to order, not stock.
cd "$(dirname "$0")"
OUT=../../../../renders/2026-10-31/barkhorn/mantle-r48
COMMON="--scale 0.75 --samples 80 --exposure -2.0 --paper #7A7570"
for n in ${@:-outcrop-ember-wide-stock outcrop-ember-custom outcrop-ice-custom strata-ice-custom strata-dusk-ember-custom}; do
  case $n in
    outcrop-ember-wide-stock) a="hero --model out-outcrop --colour ember --tint-mode wide" ;;
    outcrop-ember-custom)     a="hero --model out-outcrop --colour ember-custom --tint-mode custom" ;;
    outcrop-ice-custom)       a="hero --model out-outcrop --colour ice-custom --tint-mode custom" ;;
    strata-ice-custom)        a="hero --model out-strata --colour ice-custom --tint-mode custom" ;;
    strata-dusk-ember-custom) a="dusk --model out-strata --colour ember-custom --tint-mode custom --strip 40" ;;
  esac
  python3.11 scene.py $a --out $OUT/$n.png $COMMON > /tmp/mantle-r48-$n.log 2>&1
  echo "$n $(grep -c wrote /tmp/mantle-r48-$n.log)"
done
