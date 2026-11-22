#!/bin/bash
# Group F (2026-11-22): the lm out of every lamp at the owner's pours (lamp_site.py's defaults since 3b180d8c; Haze's Core
# 981bd837), the same method and sensor as the 17 Nov table (renders/2026-11-16/barkhorn/lamp-site/final-mix/mix.sh, G4:
# launch/isphere.py, the enclosing sensor; Hemisphere BOUNCES=64 SPP=128, Core SPP=256). All eight tints (Fog's pours
# are unchanged, so it needs no Fog frame). Writes pass/photometry.raw, one ISPHERE line per lamp; skips lines it has.
#   renders/2026-11-21/barkhorn/lamp-site/pass/photometry.sh
ROOT=$(cd "$(dirname "$0")/../../../../.." && pwd); P=$ROOT/renders/2026-11-21/barkhorn/lamp-site/pass/photometry.raw
cd $ROOT/spinoffs/barkhorn/companions; touch $P
for kv in red:ember orange:dust amber:acid green:poison blue:ice violet:haze ice:fog black:smoke; do k=${kv%%:*}; n=${kv##*:}
  grep -q "^hemisphere $n:" $P || { t0=$(date +%s); echo "hemisphere $n: $(BOUNCES=64 FRAME=dome-$k SPP=128 python3.11 launch/isphere.py 2>&1 | grep ISPHERE)" >> $P; echo "hemisphere $n $(( $(date +%s) - t0 )) s"; }
  grep -q "^core $n:" $P || { t0=$(date +%s); echo "core $n: $(FRAME=orb-$k SPP=256 python3.11 launch/isphere.py 2>&1 | grep -E 'ISPHERE|CORE_ABS' | tr '\n' ' ')" >> $P; echo "core $n $(( $(date +%s) - t0 )) s"; }
done
cat $P
