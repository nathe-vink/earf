#!/usr/bin/env bash
# Renders round 31's companion shots (shots.py writes them) into renders/2026-10-18/barkhorn/companions/.
#   spinoffs/barkhorn/companions/render_all.sh [shot-name ...]      (default: every shot)
# bpy runs on the Python it was installed for: PY=python3.11 where the system's python3 is newer than bpy's wheel.
set -euo pipefail
cd "$(dirname "$0")/../../.."
PY="${PY:-python3}"
OUT=renders/2026-10-18/barkhorn/companions
mkdir -p "$OUT"
names=("$@")
[ ${#names[@]} -eq 0 ] && names=($(ls studio/shots/barkhorn/companions/ | grep -v '^concept-' | sed 's/\.json$//'))
for n in "${names[@]}"; do
  "$PY" studio/engine/render.py "studio/shots/barkhorn/companions/$n.json" --out "$OUT/$n.png" 2>&1 | grep -E "samples|Error" | tail -1
done
