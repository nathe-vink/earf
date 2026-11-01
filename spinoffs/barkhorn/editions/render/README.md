# Editions renders

Blender Cycles path tracing on the Python that has `bpy` (`python3.11` in this container). `studio/setup.sh` installs
it.

| File | What |
|---|---|
| `pt.py` | The acrylic kit: `TINTS`, per-channel absorption from A&C's TruCast chart (`sigma_per_mm`), `acrylic()`, `lamina()` (a tinted stratum with an invisible bond line), `lens_void()` and `tube_void()` (air as inward-facing meshes), set, lights, camera, render |
| `scenes.py` | The editions: `firn` (Moho with lens voids), `iron_core` (Core with a Gibeon slice), `stamper_core` (Bedrock with a stamper shard), and the house set `core_rig()` copied from the lamps lane's pass-4 rig |
| `widman.py` | The etched octahedrite figure as an image: plates that grow until they meet, taenite hairlines, plessite, a slight warp |
| `queue.sh` | Renders frames one after another: `./queue.sh SAMPLES "edition shot tag" ...` |

**Proof:** `python3.11 scenes.py -- iron_core core /tmp/p.png --scale 0.3 --samples 32` (about one minute).

**Final:** `./queue.sh 128 "iron_core core v4"` writes `../renders/2026-10-31/iron_core-core-v4.png` (10 to 30 minutes on
4 CPUs).

Textures are CC0 (Poly Haven `marble_01`, ambientCG `Paper005`). `studio/engine/assets.py` fetches them into
`studio/assets/cache/`, which git ignores. The etch image is written to `cache-widman.png` on first use (also ignored).

Traps met here:
- **Coplanar faces render black.** Every solid stands 0.3 mm off what it rests on.
- **A heterogeneous volume crashed OpenVDB.** Tinted strata are therefore separate inset solids with a transparent
  surface.
- **Fine ring textures alias.** A record's groove bump made a hard line across the disc.
- **A polished slice mirrors every strip light.** Use light linking (`light_linking.receiver_collection`) for fill
  that should reach one object only.
- **Clear acrylic shows what is behind it.** Flags and backgrounds decide how it reads. See `../critic/LOG.md`.
