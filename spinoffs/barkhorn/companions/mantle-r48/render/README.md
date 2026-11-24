# Mantle at 1x: render scripts

The owner chose the speakers' dye for the deck on 2026-11-24 ("Speakers dye"). This folder renders that look. The deck is in the speakers' own dye at their cabinets' loading (1×). Its top and underside are polished, its outer edge is satin, and the 1 mm chamfer stays polished. There is nothing white anywhere. The light is the physical model on the house ground (#F7F0E8).

Setup on a fresh container: run `studio/setup.sh` (it installs `bpy` on the system Python). The scene loads the committed GLB in `out-strata-v3/render/`, so no CAD build is needed.

    render/mantle-1x.sh VIEW TINT OUTDIR [SCALE SAMPLES]

- VIEW is `three-quarter`, `cover` or `top`.
- TINT is one of ember, dust, acid, poison, ice, haze, fog or smoke.
- The full size is SCALE 1.0 at 128 samples, giving 1600 × 2000. A frame takes about 11–15 minutes on 4 CPUs.
- For a test, use SCALE 0.25 at 64 samples, about 1 minute.

Each run writes the PNG, .blend, .exr and log, then the emitter audit (`.gt.txt`) and the in-frame and hidden-mesh audit (`.audit.txt`). It prints one line ending in the audit counts. A good frame reads `0 emitting material(s)`, `gt flags 0`, `audit 0` and `1 no-hidden`.

`house.args` is the house camera and light rig, without the edge lamps, which the physical model dropped. `house-nocam.args` is the same rig without the camera, for the top view.
