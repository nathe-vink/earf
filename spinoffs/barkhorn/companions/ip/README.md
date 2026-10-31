# Design-drawing pack: Hemisphere, Core, Mantle, Tropos, Mother EARF, the EARFcoin (round 43, 2026-10-31)

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
- Tropos's comes from `r33-speaker-horn` at `9af7b277` (`spinoffs/barkhorn/cloud.py`, and `horn_options.py` for the
  laminated horn), read from a checkout without changing that branch.
- Mother EARF is `spinoffs/barkhorn/globe_colour.py` and the EARFcoin `companions/earf_coin.py`, both on this branch.
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

The files are in `hemisphere/`, `core/`, `mantle/`, `tropos-a/`, `tropos-b/`, `globe/` and `coin/`. The views carry no text, no dimensions and no FIG. labels, as
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

### Tropos (one application, or two: see below)

**The ornamental design for a loudspeaker, as shown.** Two variants are drawn, one per horn:
- `tropos-a/`: **the formed horn**, the flare thermoformed over the plug and the throat block.
- `tropos-b/`: **the stepped laminated horn** (Plan B, `horn-plan-b`): 22 layers of 1/2 in sheet, a terrace a layer,
  standing in the formed horn's place on the same pod, cap, pads and posts.
- **Claimed (solid lines):**
  - the cabinet: its sides, top, bottom, front panel and back;
  - the woofer's ring and the two ports with their frames;
  - the horn on top, with its pod and cap, raised on four short posts and their pads.
- **In broken lines, not claimed:**
  - the woofer and the tweeter with its adaptor;
  - the amplifier plate on the back;
  - the cloth disc and its frame over the woofer;
  - the posts' sockets and sleeves;
  - the feet, the back's and the ports' screws;
  - the rating plate and the EARF mark.
- **The cable is not in the drawings.** The model has no mains or link cable as a solid (only a parts-list line), so
  there is nothing to draw. The draftsperson adds a short broken stub at the amplifier plate if the attorney wants one.
- **Left out:** the parts inside (braces, ribs, lining, the amplifier's box, the leads), the horn's tooling and the
  fallback IR window, an option not chosen.
- **The two horns: one application or two [Atty].** They differ only in the horn's outside: smooth and continuous in (a),
  stepped in 22 visible terraces in (b). The terraces read at a glance and change the whole top of the speaker.
  - If only one horn is built, file that one.
  - If the owner wants both protected, R11 A5's rule (one design per application) suggests two applications, or one
    application with both as embodiments, which the examiner may restrict to one. The attorney decides which.
- **A partial design for the horn alone: worth filing [Atty].** The horn on its posts is Tropos's signature: the thing
  the renders lead with, and the part a copier would take. A partial design (the horn, pod and posts in solid lines,
  the cabinet in broken lines) protects it on any box, and on a future product that reuses it. The drawings here can be
  reused for it: the draftsperson swaps the line types. The horn's shape was set by acoustic simulation, so the attorney
  should check it is not dictated by function: alternative flares with the same performance exist (the stepped one is
  one), which supports ornamentality.
- **Drawn opaque.** Tropos's horn and cabinet are tinted acrylic; the lining shows through the tint in the renders. The
  same transparency decision as below applies (item 2 of the draftsperson's list).

### Mother EARF, the six-disc globe (one application, both sizes)

**The ornamental design for a decorative globe (or a lamp, if the UV-lit night mode leads) [Atty], as shown.**
- **Claimed (solid lines):**
  - three whole meridian discs through the poles and three parallel rings at 40 N, the equator and 40 S, each slotted
    round those before it;
  - the axis leaning 23.4 degrees;
  - the round base the globe rests in.
- **One design at two sizes.** The 300 mm desk globe and the 1 m back-bar piece are the same drawing scaled. A design
  patent claims the shape, not its size, so **one application covers both.** The views are drawn from the 300 mm model.
- **Left out:** the glow bands, the UV ring (inside the base) and the hue-check chips.
- **The base: claim it or not [Atty].** Claimed here, since the globe resting low in it is part of the look. To cover
  the globe on any stand, the base goes into broken lines.
- **Colour.** Its six colours are the point, but colour drawings would tie the claim to them; file in black and white.
- **Drawn opaque.** The discs are tinted acrylic, so the discs behind would show through. Same decision as below.

### The EARFcoin, design A (one application)

**The ornamental design for a token, as shown.** One coin, design A as signed: the globe engraved into the back face,
the words in a band round the front face, both edges rounded and the edge reeded.
- **Claimed (solid lines):** the whole coin: the faces with their engravings and the reeded edge.
- **The views:** the top plan is the front face (the words) and the bottom plan the back face (the globe); the four
  elevations all show the edge.
- **Drawn opaque.** The coin is clear tinted acrylic, so from the front the globe on the back shows through, mirrored.
  This is the coin's main effect, so it is worth claiming: the draftsperson draws the globe in light full lines behind
  the words on the front view (R11 A6).
- **The words: a caution [Atty].** Words in a design drawing are part of the design but give it no protection as
  words; the mark is protected as a trademark. A second partial-design application could claim the reeded edge and the
  engraved globe without the words.

## What a draftsperson must finish (37 CFR 1.84 and 1.152; R11 A6)

1. **Surface shading.** These drawings are outlines only. Add contour shading to the dome, the ball, the platter and
   the posts, so curved and flat read apart.
2. **Transparent and translucent surfaces: decision needed [Atty].**
   - Every product here is through-tinted cast acrylic. R11 A6: transparent surfaces must be shown with **oblique
     line shading**, and elements visible behind them in **light full lines, not broken lines**.
   - So the attorney must decide whether to claim the acrylic as transparent and which visible internals that
     brings in:
     - Mantle: the pod, the bearing and the posts through the plinth and lid;
     - Core: none, as the ball is frosted inside;
     - Hemisphere: none, as the opal liner hides the top's underside;
     - Tropos: the lining, the horn's throat and the drivers' backs through the tint;
     - Mother EARF: the discs behind, through the discs in front;
     - the EARFcoin: the back's globe through the front.
   - The hidden-line removal here treats every part as opaque, so the outlines show no internals.
3. **Line quality and cleanup.**
   - Curved parts are drawn from meshes. Check the silhouettes for faceting and short stray segments, especially:
     - the cable's segment marks (Core);
     - the cord (Hemisphere);
   - the coin's reeds, drawn from a fine mesh (its engravings are exact outlines, projected);
   - Tropos's ports, whose flared lips come out as a band of close lines: draw each as one or two clean circles;
   - Tropos's side views: the back's screw heads show as small solid ticks along the back edge; they are disclaimed,
     so draw them broken or leave them out.
   - Make the broken lines even and consistent.
   - Tropos (b)'s 22 terraces must stay crisp and evenly spaced; they are its design.
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
   - Core with its cable leaving at the back;
   - Tropos with its cloth disc on;
   - the coin's figure count: seven views of one coin.

**Colour.** File in black and white, which covers every tint. Colour drawings would claim the colour (R11 A5).

**Before filing, from R11:**
- Default to small entity, not micro (A2).
- One design per application (A5).
- File before the debut (A1).
