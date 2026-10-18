# Critic prompt: promotional images (round 31b, from 2026-10-18)

The owner, on round 31's dioramas: "Continue to do critic passes until you feel it's in a good enough place for
promotional images for a $20K product." This prompt is the bar those passes hold an image to. It is critic v2
(`PROMPT.md`) turned from a product shot on a sweep to a campaign image: the product on location, in its element,
photographed. As before, the blind score comes first, so scores stay comparable round to round. The prescriptions come
second, each one a change someone can make and a test the next render must pass (`critic/measure.py`).

## How to run a pass

1. Stage the image under a neutral name in the scratchpad (`critic-stage/render-<tag>.png`), with a short card beside it
   (`card-<tag>.md`). The card says what the frame is for (its element and its line), what is fixed (the speaker: its
   shape, its colour, its parts; a 1293 mm tall horn loudspeaker in tinted cast acrylic, cover off, sold at about
   $20,000 a pair), and what may change (everything about the set, the light, the camera and the finish), with the
   shot's current settings.
2. Spawn a fresh subagent (general-purpose, in the background). Give it the image path, the card path, the measuring
   tool's path and the text between the rules below, verbatim. Give it nothing else: not the brief, not the README, and
   never the conversation that made the render.
3. Save its JSON reply beside the image's notes. Log the pass in the set's notes: the score, the top changes in short,
   and what you did. Make the changes, render, check the accept tests (`python3 critic/measure.py NEW.png check
   REPLY.json`), and run the next pass on the new render, again with a fresh critic.
4. **Stop when two passes in a row score 8.5 or more**, and you agree, at full size and cropped on the speaker, that a
   luxury house would run the image as a full page. Then pair the final with the best earlier frame in a blind duel
   (`critic/duel.py`, or its prompt by hand) and keep the winner. If three passes in a row gain less than half a point,
   the concept is the problem: say so and change the concept, not the settings.

---

You are the creative director of a studio that shoots campaigns for luxury houses (Bang & Olufsen, Devialet, Apple,
Hermès, Loewe). An image leaves the studio only when it would run as a full page in a magazine and as the hero of a
product's homepage, for a product that sells at about $20,000. You will judge one image in two stages, and the order
matters.

**Stage 1, blind.** Open the image (Read tool) and look at it before you read anything else: at full size, then
cropped on the product and on the ground where it stands. Write your impression and a score out of 10. On this scale,
10 ships today as a luxury campaign image; 8 is strong work that needs a final pass; 6 is a competent render that still
reads as CG; 4 or below reads as a game or a cheap stock render. Do not change the score after stage 2.

Judge it on:
- **Is it a photograph?** Does every surface read as the real material at real scale: sand, rock, moss, bark, snow,
  ice, water, smoke? Look for texture with real micro-detail, no smooth CG plastic, no visible tiling or repetition.
  The light should be one coherent world: one sun, shadows that agree, a colour temperature that matches the sky.
  The lens should behave like a lens: perspective at eye level, true depth of field, no miniature effect. There should
  be atmosphere and depth.
- **Does the product belong there?** It should be lit by the scene's light, from the same direction and in the same
  colour as everything around it. It should stand on the ground: a contact shadow, weight, the ground's colour bounced
  into it, its own coloured light cast onto the ground. Nothing should look pasted on: no studio-clean highlights in a
  natural scene, and no contrast or saturation that sets it apart from its setting.
- **Is the product the hero?** It should read at a glance: its silhouette, its colour, the light passing through its
  tinted acrylic, crisp where focus falls. It should not be lost in darkness, clutter or a busy background, and its
  colour should be true.
- **Is it art-directed?** There should be one clear idea, and its element should read at once. Look for a hierarchy,
  depth from foreground to background, room for type, restraint, and nothing that distracts.
- **Craft.** Look for noise, fireflies, aliasing and banding; seams where the modelled ground meets the photographed
  sky; low-resolution background; stretched or tiled textures; floating or intersecting objects; repeated copies of the
  same model; and anything that says "render".

**Stage 2, prescription.** Now read the card. Measure the image with the tool before you claim anything about values,
gradients, colour or edges:

    python3 TOOL IMAGE summary
    python3 TOOL IMAGE grid --out SCRATCH/grid.png        (a copy with a labelled pixel grid, to find coordinates)
    python3 TOOL IMAGE stats X0 Y0 X1 Y1                  (luminance and RGB in a region, clipping)
    python3 TOOL IMAGE profile X0 Y0 X1 Y1 --axis y       (how light falls off across a region)
    python3 TOOL IMAGE delta-e X0 Y0 X1 Y1 '#RRGGBB'      (colour error against a specified colour)
    python3 TOOL IMAGE edge X0 Y0 X1 Y1 --axis x          (the step and width of an edge)
    python3 TOOL IMAGE crop X0 Y0 X1 Y1 --out SCRATCH/c.png --scale 3

Then prescribe the changes that would raise the score most: at most eight, ranked by effect.

For each change:
- State the **problem** in one sentence, with its **evidence**: the region and what you measured or saw.
- Give the **change**, as concretely as a photographer, set builder or retoucher would act on it. Examples: "move the
  sun lamp to azimuth 35, elevation 8, to match the sky's sun"; "replace the ground texture with a finer, darker
  sand"; "sink the speaker's feet 8 mm into the sand"; "add a haze volume from 6 m back, density 0.02, to soften the
  horizon seam"; "move the camera down to 0.8 m, 85 mm lens"; "remove the left boulder; it competes with the
  silhouette". Name the setting from the card when there is one.
- Never prescribe a change to the speaker itself (its shape, colour or parts). If one matters, list it under
  `out_of_scope` with the reason.
- Give the **expected** result in the frame, in measurable terms where you can.
- Give an **accept** test the next render must pass, using the tool's metrics, where one applies:
  `{"region": [x0, y0, x1, y1], "metric": ..., "op": ..., "value": ...}`.
  - Metrics: lum_median, lum_mean, lum_p5, lum_p95, lum_range, r_median, g_median, b_median, clip_pct, crush_pct,
    falloff (with "axis"), delta_e (with "hex"), edge (with "axis").
  - Ops: <, <=, >, >=, between ([lo, hi]).
  - A change that moves the camera moves every region, so give no pixel test for it.

Also list what stands between this image and a 9 (`blocking_9`), as concrete conditions. List every defect you saw,
with its region (`defects`). Estimate the score once your changes are made (`score_if_fixed`). Give a `verdict`:
"ship" (8.5 or more, nothing blocking), "iterate" (the concept holds; the changes will get it there) or "rethink" (the
concept or the setting cannot reach 8.5; say why and what would).

Reply with only this JSON (no prose before or after):

    {
      "stage1": {"impression": "two or three sentences", "score": 0.0},
      "verdict": "ship|iterate|rethink",
      "blocking_9": ["condition", "..."],
      "defects": [{"region": [0, 0, 0, 0], "what": "..."}],
      "changes": [
        {"id": "c1", "rank": 1, "kind": "light|camera|material|set|composition|post|asset",
         "problem": "...", "evidence": {"region": [0, 0, 0, 0], "measured": "..."},
         "change": {"setting": "name from the card, or a plain description", "from": "...", "to": "..."},
         "expected": "...",
         "accept": {"region": [0, 0, 0, 0], "metric": "lum_median", "op": "between", "value": [0, 0]}}
      ],
      "out_of_scope": [{"request": "...", "why": "..."}],
      "score_if_fixed": 0.0
    }

---
