# Light model C with S4b (24 Nov)

The coordinator, 24 Nov 09:21: S4b is light C's standard. Every reflect-only flag becomes a real black card (every ray
on, two-sided, casting shadows, out of frame); an overhead one, facing down, comes out (on the fronts and turns, flags
3 and 5: as real cards they shade the backdrop and the product; `../light-c/s4/readings.md`). Otherwise as light C:
both caustics on, clamp 0, filter_glossy 0, the acrylics' shadow-ray shortcut cut, the sweep's contact term off.
Generator: `spinoffs/barkhorn/campaign/light_c.py` (`real_flags`, `model_c`). Convergence: 96 spp matches 768 spp
within 0.25 L* by region (`../light-c/s4/convergence.md`), so the samples stay as they were.

| shots | count | size, samples | source |
|---|---|---|---|
| `front-<tint>` | 8 | 1000 x 1250, 96 | A-polished-tallr7 site front (identical to the tested `../light-c/s4/front-<tint>-s4b.json`) |
| `turn-<tint>-00`..`23` | 192 | 1200 x 1080, 96 | horn_turn.frame (the front's shot, the turn's camera and turn) |
| `horn-back-<tint>` | 8 | 1200 x 900, 128 | `renders/2026-11-13/barkhorn/fa123/horn-back-<tint>.shot.json` (no reflect-only flags) |
| `amp-<tint>` | 8 | 1600 x 1600, 128 | `renders/2026-11-13/barkhorn/fa123/macro-amp-<tint>.shot.json` (no reflect-only flags) |

216 frames. The real cards on the turns are checked against all 24 turn cameras (masks at quarter size, one sample).
Quick audits of horn-back-fog and amp-fog (fifth size): equipment 0, hidden 0, NO GLASS SHADOWS 6.

## Setup (a helper's container)

1. `bash studio/setup.sh` (bpy on python3.11), then the speaker models: the cloud and variants builds as in
   `../light-c/README.md`.
2. `bash renders/2026-11-24/barkhorn/light-c2/run.sh NAME ...`, e.g. `turn-ember-00 ... turn-ember-23 horn-back-ember
   amp-ember`, in chunks under 2 hours as a tracked background task. It is resumable.
3. Check each frame: `.equipment.txt` reads equipment 0 and hidden 0; `NAME.report.json` carries `notes`:
   `no_glass_shadows.cut` 6 and `shadow_ray_links_left.count` 0 (the same lines are in `NAME.log`).
4. Helpers work on their own branch, `r33-lightc2-<tint>`, from r33-speaker-horn: their tint's 24 turn frames,
   `horn-back-<tint>` and `amp-<tint>` (26 frames). The fronts are rendered on r33-speaker-horn.
