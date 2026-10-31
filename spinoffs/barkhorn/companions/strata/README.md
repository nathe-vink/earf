# Strata and Contour: laminated proposals for Hemisphere and Core (2026-10-31)

**Proposals, nothing more.** The owner signs designs; the current Hemisphere (`dome_pendant.py`) and Core
(`orb_table.py`) stay the baseline, and nothing here overwrites their CAD or the site's pictures. The brief is the
owner's (2026-10-31, `r46-owner-notes` 6a9fa7f4): *"nail design, make it realistic, make it cooler … well architected,
novel, lasting."* Dates and logistics are parked.

**Why laminate.** The critique (`CRITIQUE.md`) found the line reads as familiar archetypes in coloured plastic. A blind
read gave the current Core 3/10 for distinctiveness and Hemisphere 4/10. What only EARF has is:
- through-tinted cast acrylic in eight tints;
- light passing through it;
- the stacked horn ("Stacked like contour lines").

Laminating stock cast sheet makes that the signature:
- every layer's edge is a line of light;
- the layers can differ in tint and finish;
- it needs no moulds, so small batches are honest;
- thick sections can be re-polished for decades.

## The four proposals

Two families, two lamps each. The owner may pick a family, or one lamp from each.

| | Core (table) | Hemisphere (pendant) |
|---|---|---|
| **Strata** (straight: a core sample) | **Core Sample** `core_sample.py` | **Halo** `halo.py` |
| **Contour** (curved: terraces) | **Contour Core** `contour_core.py` | **Terrace** `terrace.py` |

Each is a fab-kit product: run `.venv-fab/bin/python studio/fabkit/build.py spinoffs/barkhorn/companions/strata/NAME.py
--out spinoffs/barkhorn/companions/strata/out-NAME`. That writes:
- STEP and STL;
- the DXF cut file for every layer, nested on 1/2 in sheet;
- the drawing set;
- the parts list with a budget;
- the checks.

Every one builds with **0 clashes**. Each layer is a CNC-routed sheet part, so the cut files exist. The numbers are
worked in `stack.py` and printed by each file's notes; run `python3 stack.py` for the summary.

| | Core Sample | Contour Core | Terrace | Halo |
|---|---|---|---|---|
| Acrylic | 14 discs, Ø110 × 178 (at 12.7) | 13 rings, ball Ø160 | 12 rings, dome Ø280 × 152 | 5 discs, Ø260/160 × 64 |
| Acrylic mass | 1.75 kg | 1.41 kg | 1.88 kg | 2.36 kg |
| Whole | about 2.0 kg, tips at 26° | about 1.7 kg, tips at 31° | about 2.5 kg on a 1.5 mm stainless cable | about 3.0 kg |
| Light | a "filament" (dim-to-warm strip on an aluminium spine in an opal tube), 4.4 W | a 2.5 W warm-dim board under a stock opal globe | Vero SE 10 at 180 mA, about 590 lm, 4.4 W; satin reflector, honeycomb louvre | Terrace's engine |
| Heat (worked) | spine top about 64 °C in a 25 °C room; the bore wall less. **Tight against 70 °C: to measure** | about 8 K over the room | about 6 K over the room on a 7-fin stack (~10× the current top's area; the current runs ~31 K) | about 6 K |
| Power | v1 plug-in: a listed 24 V Class 2 adapter, sealed jack, knurled stainless dimmer knob | the same | the hardwired ERP driver in the canopy (or the plug-in swag) | the same |
| Service | the engine drops out of the bottom: four screws, two set screws | the ball lifts off (balls swap colour); the globe has three set screws | three tool-free radial thumbscrews; COB on two screws; driver in the canopy | three thumbscrews |
| Parts budget (the kit's, one-off) | $303 | $289 | $533 | $448 |

### Core Sample

A drilled core of strata.
- **The column:** fourteen discs, two Smoke at the foot, seven Dust, one Ember stratum, and four Clear at the top. The
  Clear discs are bead-blasted, so the cap glows.
- **Bonding and turning:** the discs are bonded with polymerising cement, annealed, turned true, and bored Ø32 and
  polished.
- **Finish as well as tint:** each disc's outside is buffed clear or bead-blasted satin, masked on the lathe, so the
  strata differ in finish too.
- **The light:** the filament runs up the bore, and the satin bands glow while the clear ones show the filament
  magnified.
- **The foot:** turned aluminium, set 7 mm in to leave a shadow line, with three M5 screws into brass inserts.
- **Heat:** the engine's heat goes down the spine into the foot.
- **Open item:** the spine's top at about 64 °C is the one number to watch. A 12 mm spine, or 3.5 W at full, takes
  10 K off.

### Contour Core

The ball drawn in contour lines.
- **The rings:** each ring is the sphere's section at its height. Its tread is the sheet's own cast face, its outer
  edge is polished, and its inner edge is bead-blasted.
- **The light:** a stock 4 in opal globe inside glows through the rings.
- **A correction:** in a first pass the inner edges were polished, and the globe read as "a bulb in a jar". Blasting
  them melts its outline into the rings.
- **Kept from the current Core:** the ball lifts off, so balls still swap colour.

### Terrace

Hemisphere built from twelve rings.
- **The rings:** each laps the ring above by 10 mm, the bond. The outer edges are diamond-polished and the inner edges
  bead-blasted.
- **The glow:** the COB's satin reflector spills about a quarter of the light onto the rings' inner edges, so each
  terrace glows as a contour line. A 3.2 honeycomb louvre hides the COB beyond about 30° off the axis.
- **Heat:** seven 120 mm aluminium fins (the stack again, in metal) carry the heat, against the current low top's
  marginal ~31 K.
- **Hanging:** the shade hangs from a skirted flange by three radial knurled stainless thumbscrews into brass inserts,
  so it comes off tool-free.
- **Suspension:** a stainless cable and a listed gripper carry it; the cord carries only current, as `certification.md`
  requires.

### Halo

Core Sample's pendant twin.
- **The ring:** five discs bonded into a thick ring, in polished and satin bands, with one Ember stratum.
- **The light:** Terrace's engine sits on a plate over the bore. The COB's light falls straight through, and the
  ring glows in bands.

## What "realistic" meant here

**Drawn as a shop would make it.** Every joint, insert, screw, gasket, cable path, switch, foot and finish is in the
CAD and the parts list. The processes are the ones the quote requests already name:
- stock cell-cast sheet;
- CNC routing;
- polymerising cement (Weld-On 40 class);
- annealing;
- diamond-turning and buffing;
- bead-blasting;
- brass heat-set or press-in inserts;
- 304 stainless screws;
- anodised 6061.

**Pictured as a real object** (`scene.py`, Blender Cycles; the module notes say how):
- **The tint, calibrated.**
  - The absorption comes from A&C's TruCast light-transmission chart (`stack.TINTS`, at 3 mm).
  - It is applied by Beer–Lambert on the length each ray travels inside the acrylic, so thick parts deepen as they
    really do.
  - IOR is 1.49.
- **Caustics.** Each LED and the sun are Cycles caustics lights; the acrylic casts MNEE shadow caustics onto the table
  and the walls.
  - A test showed MNEE ignores a volume absorption and throws white caustics.
  - The ray-length tint carries into the caustics, so they come out coloured.
- **Edges as made:**
  - polished edges and cast faces are clear;
  - bead-blasted faces scatter;
  - fly-cut faces show rings;
  - the arrises are broken 0.4 mm;
  - every bond line is a faintly milky hairline;
  - the polished faces carry sparse hairline scratches.
- **Real props and light:**
  - Poly Haven CC0 furniture, veneers, plaster and a dusk sky;
  - a window frame that throws its bars' shadows;
  - an 85 or 58 mm lens at f/4, focused on the lamp.

**A finding the owner should know: thick laminations need light tints.**
- On TruCast's chart, 2423 (Ember's stand-in) passes about 64 % of its red per 3 mm.
- Through the 39 mm from Core Sample's bore to its skin, about 0.3 % survives: a stock-Ember column is near-black.
- The light stock tints work: 2422 Dust (59 % at 3 mm) and 0000 Clear. Dust deepens to a saturated red-orange at
  depth.
- An Ember lamination means a custom pour at about a quarter of 2423's dye loading.
- The renders use calibrated stock tints and show this honestly.

## The pictures and the critic rounds

Renders go to `renders/2026-10-31/barkhorn/strata/`, each lit at dusk and unlit in daylight. The critic is
`critic/PROMPT.md`, verbatim, given to a fresh subagent per frame (`critic_stage.py`). The duels are blind, against the
current heroes. The rounds are logged in `critic/LOG.md`.

(Scores follow below as the rounds come in.)

## For the owner to decide

1. A family (Strata or Contour), or one lamp from each.
2. Tints for laminations: the light stock tints now (Dust, Clear, Fog, Ice), or a custom lighter Ember.
3. Core's power: the v1 plug-in in every proposal; the battery stays an option in each base.
