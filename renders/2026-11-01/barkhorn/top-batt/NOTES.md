# Why the top of the insulation looked triangular (2026-11-01)

**The owner's question:** "Why does the top of the speaker insulation look triangular". It was asked of the four-pieces
room (r48-four-pieces fe292a3d, `four-pieces-day-1920.png`, the left speaker).

**The answer: a modeling error, made by the asset.**
- The top batt (`lining-top-3-web`) is a plain 48-face box, 100 mm thick, with a notch for the top rib.
- `asset/make_blend.py` collapsed every `lining-*-web` mesh to 30 % of its faces, to keep the file small. That is right
  for the quilted batts (15,000 to 35,000 faces each), but this box came out with 14 faces. Its front face lost its
  corners and became a sliver wedge, pale through the green.
- It is not a reflection, not refraction through the walls and not the notch. Hiding the batt removes it, coloring the
  batt magenta colors exactly the wedge, and the CAD's own mesh draws a clean rectangle.

`top-batt-crops.png` shows the top bay of each view. The views are `view-*.png`, rendered by `top_batt.py`: the asset
linked as four-pieces links it, the camera matched (0, -4.5, 1.0), level, 30 mm, cropped to the speaker's box.

| | what it shows |
|---|---|
| (a) as is | the wedge, as in the four-pieces frame |
| (b) the top batt magenta | the wedge is magenta: it is the batt |
| (c) the top batt hidden | no wedge |
| (d) black sleeves on the broken mesh | the wedge is darker but still there |
| (e) the fix: the batt's full mesh | a clean rectangle with the rib's notch |
| (f) the fix with black sleeves | the lining recedes |

**The fix (done):** `make_blend.py` never collapses a mesh under 2,000 faces. Both assets are rebuilt: `tropos.blend` and
`tropos-strata.blend`. Their top batts keep all 48 faces, and the files are the same size. Any scene that links the
asset picks the fix up on its next render. The four-pieces branch reads its own copy of `tropos.blend`, so it needs this
one.

**Black sleeves are a look, not a fix.** The voile sleeves are white in the product (`product.py`). Black or tinted
sleeves make the lining recede (f); with white sleeves (e) the batts read as pale blocks through the tint. That is the
owner's choice.
