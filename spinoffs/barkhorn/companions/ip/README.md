# Design-drawing pack: Hemisphere, Core, Mantle (round 43, 2026-10-31)

**Draft drawings for EARF's US design applications.** They are for the attorney's review and a draftsperson's
finishing, not for filing as they stand.

**Why now:**
- R11 (`r46-owner-notes` 35f9ddf2, `research/2026-10-31/R11-design-protection.md`, section A) recommends **one US
  design application per product, filed before the debut on 19 January 2027**.
- The hard stop is **15 October 2027**, a year after the first public posting.
- About $300–800 of each design's $1.3k–2.8k in attorney fees is the drawings (R11 A3). Starting from these views
  should cut that.

**How they are made:** `design_drawings.py`.
- The views come from the same solids the fab kits cut and turn, projected with OpenCascade's hidden-line removal
  (the fab kit's `drawings.hlr`).
- Mantle's model comes from `r32-turntable-final`, which holds its product file.
- Each view is saved as an SVG (vector, for the draftsperson) and a 300 dpi PNG.

## The views (each product)

| File | FIG. | View |
|---|---|---|
| `<product>-1-perspective` | 1 | perspective (an axonometric from front-right, above) |
| `<product>-2-front` | 2 | front elevation |
| `<product>-3-rear` | 3 | rear elevation |
| `<product>-4-left` | 4 | left side elevation |
| `<product>-5-right` | 5 | right side elevation |
| `<product>-6-top` | 6 | top plan |
| `<product>-7-bottom` | 7 | bottom plan |

The files are in `hemisphere/`, `core/` and `mantle/`. The views carry no text, no dimensions and no FIG. labels, as
asked; the draftsperson adds the labels.

## What each design claims: a draft for the attorney's review **[Atty]**

### Hemisphere (one application)

**The ornamental design for a pendant lamp, as shown.**
- **Claimed (solid lines):**
  - the shade: a shallow dome of three nested layers, seen as one, closed at its mouth by a turned rim;
  - its low stepped black top: the clamp ring, the hub, the crown and the small cap, stacked and stepping in;
  - the two pins at the collar.
- **In broken lines, not claimed:**
  - the cord, cut short;
  - the steel suspension cable, cut short.
- **Left out entirely:** the ceiling canopy. Seen from above, it would hide the whole design.

  The mountings differ between the plug-in swag and the hardwired version, so one claim on the shade and its top
  covers both.
- **One design or two?** "North" and "South" were Hemisphere's two variants. South was dropped on 25 October
  (`studio/engine/kit_ext/earf_moon.py`: "dropped 2026-10-25, kept as a record"), so **one application, North only.** If the owner revives South, it needs its own
  application: a bowl rather than a dome, different enough to be a separate design (R11 A5).
- **A partial design is worth weighing:** the stepped top on the dome alone (R11 A5).

### Core (one application)

**The ornamental design for a table lamp, as shown.**
- **Claimed (solid lines):**
  - a ball sitting low in the shallow cup of a round base;
  - the base's band (the touch ring) and its small window;
  - the underside's hatch and foot ring (bottom view).
- **In broken lines, not claimed:** the cable.
- **Left out:** the parts inside the frosted ball and the opaque base, which can't be seen.
- **A partial design is worth weighing:** R11 names the ball-to-base junction as Core's signature. A ball on a
  round base is crowded prior art, so the claim's strength is in the proportion and the junction.

### Mantle (one application)

**The ornamental design for a record player, as shown.**
- **Claimed (solid lines):**
  - the plinth floating over the base on four short round posts;
  - the base's outline;
  - the round platter and its hub;
  - the motor pod standing apart in its stacked rings.
- **The lid is left out of these views [Atty].** The hidden-line removal treats every part as opaque, so the closed
  lid hid the plinth, the platter and the pod: the whole design. The choices:
  - claim Mantle without the lid, as drawn here;
  - have the draftsperson add the lid as a transparent part, with oblique shading and the parts behind it in light
    full lines (R11 A6);
  - file the lid in its own application.
- **In broken lines, not claimed:** the bought and functional parts:
  - the Rega tonearm and the cartridge;
  - the motor, the belt and the levelling feet;
  - the phono stage and the rear box;
  - the hinges;
  - the LED strip and the slot's mask;
  - the EARF mark (a trademark, not design).
- **A partial design is worth weighing:** the floating plinth over its base (R11 A5).

## What a draftsperson must finish (37 CFR 1.84 and 1.152; R11 A6)

1. **Surface shading.** These drawings are outlines only. Add contour shading to the dome, the ball, the platter and
   the posts, so curved and flat read apart.
2. **Transparent and translucent surfaces: decision needed [Atty].**
   - All three products are through-tinted cast acrylic. R11 A6: transparent surfaces must be shown with **oblique
     line shading**, and elements visible behind them in **light full lines, not broken lines**.
   - So the attorney must decide whether to claim the acrylic as transparent and which visible internals that
     brings in:
     - Mantle: the pod, the bearing and the posts through the plinth and lid;
     - Core: none, as the ball is frosted inside;
     - Hemisphere: none, as the opal liner hides the top's underside.
   - The hidden-line removal here treats every part as opaque, so the outlines show no internals.
3. **Line quality and cleanup.**
   - Curved parts are drawn from meshes. Check the silhouettes for faceting and short stray segments, especially:
     - the cable's segment marks (Core);
     - the cord (Hemisphere).
   - Make the broken lines even and consistent.
   - **Check every line's type against the claim.** A line counts as solid when it lies on a claimed part's own
     outline, within 1 mm. Where a claimed and a disclaimed edge run together, a few claimed edges came out broken,
     for example the plinth's back edge in Mantle's perspective. Redraw them solid.
4. **Sheets.**
   - Lay the views onto A4 or US letter sheets with the 37 CFR 1.84(g) margins: top 2.5 cm, left 2.5 cm, right
     1.5 cm, bottom 1.0 cm.
   - Number the sheets and label FIG. 1 to FIG. 7.
   - Black ink, with nothing else on the sheet.
5. **The perspective.** It is an axonometric (parallel) projection. Ask the attorney whether a true perspective is
   preferred.
6. **Consistency.** Every view must show the same object in the same state:
   - Mantle without its lid in all seven (see above);
   - Hemisphere is drawn with its suspension cable;
   - Core with its cable leaving at the back.

**Colour.** File in black and white, which covers every tint. Colour drawings would claim the colour (R11 A5).

**Before filing, from R11:**
- Default to small entity, not micro (A2).
- One design per application (A5).
- File before the debut (A1).
