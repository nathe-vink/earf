#!/usr/bin/env bash
# Fetch the photographed CC0 surfaces round 44 renders with (see TEXTURES.md) into studio/assets/cache/ (kept out of git).
# The renders also fetch on demand; this warms the cache. Poly Haven needs a User-Agent; assets.py sends one.
set -euo pipefail
cd "$(dirname "$0")/../../../.."
for id in oak_veneer_01 beige_wall_001 brown_leather smoked_walnut_veneer; do
  python3 studio/engine/assets.py get "$id" --res 2k
done
