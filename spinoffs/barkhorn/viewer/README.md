# The site's 3D view (round 47, built and switched off)

A "View in 3D" for a product's page: its fabkit render model, the acrylic as physically based transmission tinted as the
renders tint it, lit by a small studio made in code, turned by hand within limits. **It is off** (`VIEW3D = False` in
`../web.py`) because it does not yet hold up beside the path-traced pictures (below).

    npm install && node build.mjs      # three.js (pinned, 0.170.0) and the viewer into ../site/3d, and each model compressed

- `compress.mjs`: a fabkit GLB (render/<name>.glb, 62 MB for Tropos) made web-sized. The printed words and labels go;
  each part takes a material named by its finish (from the build's render/<name>.json); merged by finish, welded,
  simplified within 0.1 mm, quantized, meshopt-compressed. Tropos: 2.1 MB, 34 meshes (one draw a finish), 460k triangles.
- `viewer.js`: `open(box, spec, tint)`, `tint()`, `dispose()`. three.js r170 modules, imports made relative by
  `build.mjs` (no import map, no bundler). The spec comes from `web.py`'s `view3d()`, which reads the engine's product file
  (`studio/products/barkhorn-cloud.json`, the finishes the renders were painted with) and each colour's flavour (`finals.py`'s).
- The acrylic: the engine's clear resin is Beer's-law absorption, a colour (`deep`) reached after a distance (`radius`),
  which is three.js's `attenuationColor` and `attenuationDistance`, so the numbers carry straight over. A shader patch
  makes the path grow with the viewing angle (thickness over the refracted angle's cosine), so a face square on is pale
  and one edge-on deep. Inside parts are coloured as if lit through a wall.
- On the page (`web.py`): a "View in 3D" pill on the gallery, shown only where a model exists and `WebGL2RenderingContext`
  does; the module and model fetched only on the tap; the colour coins repaint it in place; Escape or "Back to pictures"
  closes it; leaving the page frees the GPU. Reduced motion skips the opening quarter turn. Keyboard: arrows turn,
  + and - zoom. Any failure puts the pictures back with a line saying so.

## Why it is off

A blind critic (fresh context, images only, 2026-10-31) was shown three pairs, a viewer frame beside the studio render of
the same colour, the order mixed: Ember 4 against 7, Haze 4 against 7, Fog 3.5 against 6.5, and "hurt" on all three:
"each weaker image looks like a flat real-time model shown beside a photograph." Its reasons: no bright edges and no
light carried through the walls (the cabinet reads as tinted film over a box), the inside reading as opaque card, no
coloured light on the floor, and a smear in the horn's throat (a reflection of the key along the flare). Software
rendering here (SwiftShader) is the same image a GPU makes, so a phone would not look better.

## What would close the gap

1. The edges and the floor are what the path tracer gets from light travelling inside the slab. Bake them: render the
   cabinet's light (its edge glow and the coloured caustic on the floor) once per colour in Cycles into textures on the
   model (`pathtrace.py` can), so the browser shows baked light and only adds reflections.
2. Or skip real time: a turntable of path-traced frames, 36 a colour, at about 900 px, the way the horns turn on the
   speakers' page already. It is a picture, so it matches the pictures; it costs render time (a few hours on this CPU for
   eight colours) instead of fidelity.

## The press kit PDF

`node presskit.mjs` (after `python3 ../web.py`) prints the press page to `../site/press/earf-press-kit.pdf` with its
print styles (in `web.py`), so the PDF and the page cannot disagree. Run `web.py` again afterwards so the page's link
shows the PDF's size.
