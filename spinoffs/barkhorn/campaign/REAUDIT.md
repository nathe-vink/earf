# Re-audit of the phase-2 pictures after the cast fix (2026-11-09)

The old cast (shots._frame_rays) fitted the sensor to the frame's larger side, aimed at the target instead of looking
level, and measured lens shift in the larger side; render.py fits the sensor HORIZONTAL and Blender measures the shift
in frame widths. Fixed in fa7665dc; the corrected cast lands on the same pixel as bpy's world_to_camera_view.

Ground truth: render.py's mask pass on each picture's own rendered shot.json (`--masks-only`), every camera-hidden mesh
and every lit area lamp drawn as its own id, every set flag and bounce card as 255, all visible to the camera for
that pass, occlusion by the product included. One picture per distinct camera, lights and set (14 groups covering
203 shot files; the turn frames move only the speaker). Cast table for all 203: `REAUDIT-cast.tsv` (191 clean; the
cast ignores occlusion, so it can only overcount).

| group | files | picture masked | hidden px | equipment px |
|---|---|---|---|---|
| p2 horn-back, all seven | 7 | horn-back-acid | **61,101 (glow lamp)** | 0 |
| p2 turn-ember-00 to -04 | 5 | turn-ember-00 | **41,226 (glow lamp)** | 0 |
| p2 turn-ember-05 to -23 | 19 | turn-ember-05, -12 | 0, 0 | 0, 0 |
| p2 amp-plate-ember | 1 | itself | 0 | 0 |
| p2 turn-acid-00 to -16 | 17 | turn-acid-00 | 0 | 0 |
| p2 turn-dust | 24 | turn-dust-00 | 0 | 0 |
| rc1 turn-acid-17 to -23 | 7 | turn-acid-17 | 0 | 0 |
| rc1 turn-fog | 24 | turn-fog-00 | 0 | 0 |
| rc1 turn-haze | 24 | turn-haze-00 | 0 | 0 |
| rc1 turn-ice | 24 | turn-ice-00 | 0 | 0 |
| rc1 turn-poison | 24 | turn-poison-00 | 0 | 0 |
| rc2 turn-fog | 24 | turn-fog-00 | 0 | 0 |
| backfix and backrig horn-back-acid (one group) | 2 | backfix horn-back-acid | 0 | 0 |
| backfix amp-plate-ember | 1 | itself | 0 | 0 |

Pulled (the coordinator, 23:28): the six p2 horn-backs approved (Ember, Dust, Poison, Ice, Haze, Fog) and
turn-ember-00 to -04. The `glow` lamp (0.7 x 0.32 at 0, 0.66, 1.12, irradiance 1.6, specular 0) stood in open frame
beside the horn. The current rollout code deletes it from phase-2 shots; the replacements re-run phase 2 (tag p2r).
The tall (tallr6, fa7665dc's rig): hidden 0 px, equipment 0 px.

## The front face's reflection (2026-11-10, the skeptic's physics question)

The lower front face carries about 1 % of floor reflection in the pictures where acrylic gives about 4 %. Settled:
the material is physical and the display curve removes it.
- The material (materials._clear_resin, Ember's bark): Principled, transmission 1, IOR 1.49, roughness 0.05, white
  base, no coat or scaling; the tint is a volume; only shadow rays see a transparent BSDF.
- `fresnel_plate.py`: a 10 mm plate of it at 39 deg mirroring radiance 1.0 reflects 0.044 linear in G and B (0.040 at
  25 deg; a clear plate both faces 0.083).
- The lower front face (rows 950-1045) mirrors open, in-frame floor in front of the base (display 236-244).
- The view transform, Khronos PBR Neutral, subtracts a black-level offset from all channels when the smallest is low:
  the same plate reads 0.044 through Standard and 0.012 through it, which is the 23-26 measured on Ember.
The coordinator (00:22): keep Khronos PBR Neutral, a global tone curve like a camera's profile; AgX stays a look
question for the owner at the corrected studio re-shoot.
