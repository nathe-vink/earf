# Mantle, round 48: make it real, make it EARF's

The owner, 2026-10-31: "I mostly want to nail design, make it realistic, make it cooler … Make it well architected,
novel, lasting." The current Mantle (`../turntable_float.py`, `../out-turntable-float/`, round 34 and round 43's BOM)
**stays the baseline**. Nothing of it was changed. This folder holds two proposals beside it. Each has its own CAD,
drawings, parts list, numbers and renders. The owner chooses.

| | baseline | **A, Strata Float** | **B, Core** |
|---|---|---|---|
| idea | a squared plinth floating over a lit base, hinged box lid | the same architecture, every fault fixed, the plinth and base laminated as strata | a stepped block of strata; lift the top strata off and the deck is there; the lifted strata frame the sleeve |
| product file | `turntable_float.py` | `mantle_strata.py` | `mantle_core.py` |
| build | `out-turntable-float/` | `out-strata/` (23 sheets) | `out-core/` (30 sheets + `drawings/details.png`) |
| size | 470 x 380 x 194 | 470 x 380 x about 200 | 472 x 382 x 155 closed, 47 deck |
| mass | about 15.5 kg | about 15 kg | 16.1 kg (deck 8.7, cover 2.9, turning 2.1) |
| parts list, one off | $3,910 | **$4,356** | **$4,282** |
| supplies at the wall | Neo + Mean Well (light, shared with the phono stage) | Neo + Mean Well (light) + the S2's own | Neo + the S2's own |
| checks | | 0 clashes, stock ok, library ok | 0 clashes, stock ok, library ok |

    .venv-fab/bin/python studio/fabkit/build.py spinoffs/barkhorn/companions/mantle-r48/mantle_core.py --out spinoffs/barkhorn/companions/mantle-r48/out-core
    .venv-fab/bin/python studio/fabkit/build.py spinoffs/barkhorn/companions/mantle-r48/mantle_strata.py --out spinoffs/barkhorn/companions/mantle-r48/out-strata
    .venv-fab/bin/python spinoffs/barkhorn/companions/mantle-r48/core_numbers.py > spinoffs/barkhorn/companions/mantle-r48/out-core/numbers.md
    .venv-fab/bin/python spinoffs/barkhorn/companions/mantle-r48/details.py
    sh spinoffs/barkhorn/companions/mantle-r48/render_all.sh          # Cycles, about 25 min a frame on 4 cores

(After a build, write `render/meta.json` for the scene: see the commit, or `python -c` the product's `derived(P)`.)

## 1. The critique

### Blind critics on the current pictures (`critic/r1-baseline/k1..k4.json`)

Four fresh critics each judged one image: the studio hero (lid open), dusk, lid open from the left, and the detail. Each
saw only the image, a one-line card and the measuring tool (`critic/PROMPT-realism.md`, PROMPT-promo's blind scale).
**All four scored 4.5.** What they say it reads as: "a generic acrylic two-tier audiophile turntable (the Pro-Ject /
Rega P-series archetype)"; "the clear acrylic sandwich on posts used by Pro-Ject, Clearaudio and Rega"; "a stock
1980s-style hinged dust cover". That confirms the coordinator's read.

**The ten least realistic details** (merged across the four, worst first):

1. The arm is primitives: a box headshell with no cartridge, stylus or finger lift; a cube for the bearing; no cue
   lift or arm rest that reads.
2. Upscaler and denoiser smear: the polished edges look brushed, and the wordmark reads "EACF".
3. The acrylic reads as opaque gloss or grey metal. Nothing passes light, edges don't pipe it, and the inside can't
   be seen.
4. Every edge is a zero-radius CAD line, with no break, no polish line and no seam.
5. The record has no grooves, no lead-in or run-out, and a blank label.
6. A white void, with nothing for the gloss to reflect and no falloff.
7. The fixings read as chrome droplets, not button heads in counterbores.
8. The posts' isolation can't be read: what is elastomer, what is the bolt?
9. The hinges are black blocks with no pin or leaf.
10. The base's glow reads as an emissive stripe, not light travelling through acrylic, and one image has a z-fight
    fragment in the base.

**The five biggest chances to make it cooler** (the critics' and the engineer's, merged):

1. Make the tinted acrylic the hero: light passing through, edges glowing, the mechanism framed like a watch
   caseback.
2. One signature structural move instead of two plates on posts. The engineer suggested laminations of alternating
   tints, so that the bond line, the hard part, becomes the signature.
3. A cover that belongs to this object, not a box hood.
4. One crafted metal accent at the touch points: the arm board, the bearing, the feet.
5. A platter that is a statement: a stepped or banded rim that catches one crisp ring of light.

### A fresh engineering review of the CAD (`critic/r1-baseline/cad-review.md`)

It found ten things a shop or a turntable engineer would not build as drawn:

- The light slot leaves 1 mm of a 10 mm base.
- The pod on the shelf tips under the belt.
- The float on its bushings sits at 25-36 Hz, in the band where speakers feed back.
- The bearing's M4 inserts leave 2.8 mm webs beside its bore.
- The hub is bonded and then has the spindle pressed into it.
- 25 mm cast sheet is ±1.5-2 mm thick.
- The arm's height is not designed.
- The 2.2 kg lid is twice what the Debut hinges carry.
- The light and the phono stage share a supply.
- The webs are thin.

It also listed what is missing: a bearing section, fits and finishes, a wiring and earth scheme, and a rating label.
Both proposals answer every point. Core's `details.png` draws the missing pieces.

## 2. The signature: strata, and why the tint goes in thin lines

The coordinator's direction was to make lamination the line's signature. I tested it in the physical renderer
before drawing anything, and the numbers turned it around.

- **Stock tint is dark at thickness.** A&C's TruCast chart gives 2064 Gray **29.3 %** luminous transmission at 1/8 in
  (2423 Red 14.1 %). Take out the two Fresnel losses (0.923) and apply Beer-Lambert. Then 3 mm of 2064 passes about a
  third, 12.7 mm about 1 %, and 25 mm about 0.01 %. Rendered at those numbers, a stack of thick tinted sheet is a black
  slab (`scene.py`, first passes): nothing passes through it, and the strata vanish. That matches round 43's "harsh
  case". The $1 chips and a 1/2 in offcut will confirm it before any sheet is bought.
- **So the strata are clear, and the colour is the contour line.** Each proposal is thick water-clear stock
  (12.7, 5.6) with thin tinted laminae (3 mm). In Core each tinted lamina is a **20 mm ring round a clear inlay** cut
  from the same file. The colour sits at the edges as a dark contour line under every terrace. The inside is clear,
  so the brass bearing, the feet and the motor show through the block, like a watch's caseback. This also gives the
  critics' "light passing through" and the engineer's "make the bond line the signature".
- **Honest about the bond lines.** A polymerising cement (ACRIFIX 2R 0190, Weld-On 40) cures to PMMA. It is
  index-matched, so a joint shows only as a faint refracting line, and it does **no** constrained-layer damping. Real
  CLD needs a viscoelastic interlayer: an acrylic foam tape, or an optical PSA. Either would creep under the bearing
  and show milky. Neither proposal claims damping from its laminations. The deck is damped by its mass and by PMMA's
  own loss factor (0.03-0.06).
- **The glowing platter ring** (the brief's idea) was tested on paper and set aside. A static light under a turning
  platter lights a ring only if the light under it is a full ring too. The belt crosses the rim, and the LEDs would
  sit an inch from the cartridge. Instead the platter is laminated (tinted 3 / clear 12.7 / tinted 5.6), so its rim
  is a clear band between two dark lines, which catches the room's light as it turns.

## 3. The proposals

### B, Core (recommended)

Closed, Core is a stepped block of strata 155 mm tall. The deck is six laminae (tinted 3 / clear 12.7 ×3, 47.1),
stepping in 3 mm a terrace. The cover continues the same contours: five clear rings 10 wide, each with a tinted ring
on it, and a clear 5.6 top under a tinted 3. Lift the cover off and the record player is underneath, cut into the
block. Stand the cover on its back edge, open side forward, and the sleeve of the record playing stands in it:
**the cover becomes the display stand.** It locates on two stainless dowels and sits on three clear bumpers. It has
no hinges to sag. At 2.9 kg it is a two-handed lift; a lighter top is an open question below.

It has no LED, no dimmer and no second light supply. The light is the room's, passing through the clear strata. Two
plugs: Rega's Neo, and the Phono Box S2's own listed adapter.

### A, Strata Float

The owner's original brief, kept: squared, like a Debut or an Orbit, a clear body and a matching cover. It keeps the
float, the lit base and the hinged lid, and fixes every fault the review found:

- **The plinth** is laminated (tinted 3 ring / clear 12.7 / tinted 3 ring / clear 5.6 = 24.3), stepping 2 mm.
- **The posts** are torqued studs (rigid). Isolation is in four brass feet on Sorbothane.
- **The motor** hangs from the plinth on Rega's grommets, in the float's gap.
- **The base** is clear 12.7 under a tinted 3 ring. The light's slot is 6 deep and 25 in from the edge, in one closed
  loop of dotless COB strip (4.4 W). The black band is printed inside the stack.
- **The lid** is 3 mm 2064, 1.1 kg, within the hinges' rating.

A is the safer choice; B is the new idea.

## 4. Real details (Core; A shares them unless noted)

`out-core/drawings/details.png` draws A to F. `out-core/numbers.md` has the arithmetic.

| detail | what | mass | cost (one off) | service |
|---|---|---|---|---|
| bearing and oil | Lead-free brass housing M30 x 1.5, clamped by its nut under the deck (10 N m, PTFE washer), with **no insert near the bore**. Two C932 bushes honed to 10 H6 on a 10 g5 440C spindle (8-12 µm). A 6 mm carbide ball on a lapped 52100 plate: 20 N, Hertz peak 2.3 GPa, under half the static limit. 2.5 ml ISO VG 32, filled to 10 mm under the flange. | 0.38 kg | housing $~90, nut, bushes $40, ball $5, plate $20, oil $15 | Lift the platter, hub and spindle out together; wipe; 1 ml of oil every two years with a syringe; lower it slowly. Shipping: that assembly in its own foam, a nitrile cap on the housing. |
| platter | Tinted 3 / clear 12.7 / tinted 5.6, cemented, annealed, turned to 300 x 21. Run-out 0.05. **Why acrylic:** PMMA's bar impedance (1.95 MRayl) is within 4 % of vinyl's (2.03), so only 0.04 % of the stylus's energy reflects at the record's underside; the rest goes into a material with a loss factor of 0.03-0.06 (aluminium about 0.0001). It doesn't ring, so there's no mat. I = 0.020 kg m2. | 1.74 kg (2.07 turning) | $170 + hub $71 | The six M4 screws hold it on the hub, so the bond carries no torque and the platter can be refaced and repolished. |
| motor, belt, decoupling | Rega's 24 V motor on its plate, **hung on Rega's three grommets** in a pocket in the deck, so the pulley's height is fixed to the platter's by solid acrylic. Pulley 39.48 (250 rpm), 180 from the spindle, wrap 87°. Flat belt 5 x 0.6, path 992 mm, cut to about 945. | 0.41 kg | motor kit $265, grommets $15, pulley $47, belt $30 | Lift the motor plate out of its pocket (three grommets); the belt is changed with the platter off. |
| arm and arm board | Rega RB330 at 222 on an **aluminium arm-board puck** (84 x 12, bead-blasted, Rega three-point), on three M5 into inserts. Another arm takes another puck. The record sits 28.8 over the deck's top; Rega spacers set the tube level on the first sample. | 0.46 kg | arm $675, puck about $40 | The arm comes off from below through the 56 bore. |
| arm rest and cueing | Rega's own lift and rest, on the arm's base. The lever sits to the right of the arm, front. | in the arm | in the arm | Rega's. |
| feet and levelling | **Three** turned brass feet (40 x 12) on Sorbothane 40 x 4, on M8 studs in bonded inserts, levelled by turning and locked with a brass nut. Three never rock. f about 50 Hz on 13 kg: they keep 70 Hz and up off the deck, pass footfall (a bouncy floor wants a wall shelf), and add nothing in the arm's 8 Hz band. | 0.47 kg | brass $~90, pads $20, studs $18 | Turn to level; replaceable pads. |
| external supply and connector | Rega's Neo PSU MK2 (mains, its maker's listing; check its US mark) drives the motor through its own lead in a groove to the back notch. The S2's own listed 18 V adapter plugs into a 2.1 mm jack on the brass plate. Nothing inside Core is above 24 V. | | Neo $445 | Both are standard, replaceable boxes. |
| speed change | 33/45 on the Neo's button, trimmed in 0.01 rpm steps. One pulley diameter; the belt never moves. | | | |
| hinges and stays (A) | A: Pro-Ject's Debut friction hinges in 9.5 acrylic blocks on M4 into inserts (in shear), with a 1.1 kg lid. **B: none.** The cover lifts off on dowels. | | A $34 | |
| cartridge and phono cable | Ortofon 2M Black (or 2M Blue for the first build, round 43). The RB330's own lead goes down the puck's bore, along an 8 x 6 groove under the deck, into the **S2 in a tunnel from the back** (on felt runners). The S2 feeds the brass plate's DPDT (stage or bypass) to the gold RCAs. Star earth at the plate's post: arm, bearing housing (M3 tag), S2. | S2 0.57 kg | 2M $750, S2 $269, plate hardware $48, wiring $25 | Four M3 screws hold the plate; the S2 slides out for its switches. |
| labels and rating | Laser-engraved and black-filled on the brushed brass plate: name, line out, 18 V DC 0.5 A (centre +), SN, "Motor: Rega Neo PSU". EARF etched at the deck's front right, filled. No compliance mark until tested (the supplies carry their own). | 0.11 kg | plate about $50, etch $15 | |

**Heat:** none to speak of in Core (the S2 draws 0.5 W in an open tunnel). In A the COB loop is 4.4 W in a 6 mm slot
open below, a third less a metre than the baseline's strip, through 25 mm of clear acrylic to the edge. The
baseline's first-sample thermocouple check stays.

**Cost against the baseline ($3,910):** Core is $4,282, about +$370. It adds the turned feet, the puck, the screwed
hub, the threaded housing's nut and the cover's ten rings. It drops the light, the dimmer, the adapter, the rear box,
the regulator, the posts, the bushings and the hinges. A is $4,356, about +$450 (the same turned parts, plus the
COB loop). The kit prices every ring as a full rectangle of sheet. In practice the platter blanks, the puck's ring
and the inlays nest inside the rings' offcuts, so the acrylic line is high.

## 5. The renders (`renders/2026-10-31/barkhorn/mantle-r48/`)

Path-traced in Cycles by `scene.py` from the fab kit's render model (one model, every shot):

- **The acrylic:** IOR 1.49, with Beer-Lambert absorption calibrated to TruCast 2064 per stratum (the tinted rings
  by height and by distance from the edge).
- **Faces as a shop leaves them:** cast faces glassy, outer edges diamond-polished, terrace treads buffed, holes and
  pockets satin, every edge broken 0.5 mm in shading.
- **Wear:** faint hairline scratches and dust on the top faces.
- **Caustics:** Cycles' MNEE caustics (casters and receivers flagged).
- **The record:** a radial anisotropic groove sheen, its bands, lead-in and run-out, and a printed label.
- **A fuller RB330 and 2M** than the kit's envelope.
- **A real lens:** 50-100 mm at f/5.6-8 with true depth of field, then a light vignette and luminance grain.
- **Scale:** the 12-inch record and sleeve; Poly Haven's scanned walnut and plaster (CC0) in the room.

| frame | what |
|---|---|
| `core-hero.png` | Core, studio, cover off, Smoke (2064) |
| `core-closed.png` | Core closed: the block of strata |
| `core-detail.png` | the arm's corner: cartridge, the platter's strata rim, the terrace, the mark |
| `core-use.png` | a record playing (the label blurred at 33⅓, 1/8 s), the cover stood as the sleeve's frame, on a walnut sideboard |
| `strata-hero.png` | Strata Float, studio, lid off, the base's loop lit |

The in-use frame was to have a hand on the cue lever. The procedural hand read as a cartoon, and it would have cost
the frame its realism, so the playing record carries the "in use" instead.

## 6. Blind scores and duels

See `critic/LOG.md` (filled after the renders).

## Open questions for the owner

1. **A or B,** or B's cover on A's float.
2. **The thin-tint stack** depends on 2064 being as dark as its chart says. The chips and a 1/2 in offcut settle it.
   If the caster pours EARF's own tints lighter, thicker tinted strata come back as an option.
3. **Core's cover is 2.9 kg.** A 3 + 3 top instead of 5.6 + 3 would bring it to about 2.4.
4. **Core has no light.** If the owner wants the glow, A's lit base can go under Core's deck on four short clear
   posts, at A's cost.
5. **Cartridge:** the 2M Black ($750), or the 2M Blue ($220) for the first build (round 43).
