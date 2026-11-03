# Mantle, round 48: make it real, make it EARF's

(Proposal B was first called Core; the coordinator renamed it Outcrop, since Core is the table lamp. Older commits say core.)

The owner, 2026-10-31: "I mostly want to nail design, make it realistic, make it cooler … Make it well architected,
novel, lasting." The current Mantle (`../turntable_float.py`, `../out-turntable-float/`, round 34 and round 43's BOM)
**stays the baseline**. Nothing of it was changed. This folder holds two proposals beside it. Each has its own CAD,
drawings, parts list, numbers and renders. The owner chooses.

| | baseline | **A, Strata Float** | **B, Outcrop** |
|---|---|---|---|
| idea | a squared plinth floating over a lit base, hinged box lid | the same architecture, every fault fixed, the plinth and base laminated as strata | a stepped block of strata; lift the top strata off and the deck is there; the lifted strata frame the sleeve |
| product file | `turntable_float.py` | `mantle_strata.py` | `mantle_outcrop.py` |
| build | `out-turntable-float/` | `out-strata/` (23 sheets) | `out-outcrop/` (30 sheets + `drawings/details.png`) |
| size | 470 x 380 x 194 | 470 x 380 x about 200 | 472 x 382 x 155 closed, 47 deck |
| mass | about 15.5 kg | about 15 kg | 16.1 kg (deck 8.7, cover 2.9, turning 2.1) |
| parts list, one off | $3,910 | **$3,822** | **$3,773** |
| supplies at the wall | Neo + Mean Well (light, shared with the phono stage) | Neo + Mean Well (light) + the S2's own | Neo + the S2's own |
| checks | | 0 clashes, stock ok, library ok | 0 clashes, stock ok, library ok |

    .venv-fab/bin/python studio/fabkit/build.py spinoffs/barkhorn/companions/mantle-r48/mantle_outcrop.py --out spinoffs/barkhorn/companions/mantle-r48/out-outcrop
    .venv-fab/bin/python studio/fabkit/build.py spinoffs/barkhorn/companions/mantle-r48/mantle_strata.py --out spinoffs/barkhorn/companions/mantle-r48/out-strata
    .venv-fab/bin/python spinoffs/barkhorn/companions/mantle-r48/outcrop_numbers.py > spinoffs/barkhorn/companions/mantle-r48/out-outcrop/numbers.md
    .venv-fab/bin/python spinoffs/barkhorn/companions/mantle-r48/details.py
    sh spinoffs/barkhorn/companions/mantle-r48/render_all.sh          # Cycles, 6-15 min a frame on 4 cores (render_v2.sh, render_v3.sh: the later passes)

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
3. The acrylic reads as opaque gloss or gray metal. Nothing passes light, edges don't pipe it, and the inside can't
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
Both proposals answer every point. Outcrop's `details.png` draws the missing pieces.

## 2. The signature: strata, and why the tint goes in thin lines

The coordinator's direction was to make lamination the line's signature. I tested it in the physical renderer
before drawing anything, and the numbers turned it around.

- **Stock tint is dark at thickness.** A&C's TruCast chart gives 2064 Gray **29.3 %** luminous transmission at 1/8 in
  (2423 Red 14.1 %). Take out the two Fresnel losses (0.923) and apply Beer-Lambert. Then 3 mm of 2064 passes about a
  third, 12.7 mm about 1 %, and 25 mm about 0.01 %. Rendered at those numbers, a stack of thick tinted sheet is a black
  slab (`scene.py`, first passes): nothing passes through it, and the strata vanish. That matches round 43's "harsh
  case". The $1 chips and a 1/2 in offcut will confirm it before any sheet is bought.
- **So the strata are clear, and the color is the contour line.** Each proposal is thick water-clear stock
  (12.7, 5.6) with thin tinted laminae (3 mm). In Outcrop each tinted lamina is a **20 mm ring round a clear inlay** cut
  from the same file. The color sits at the edges as a dark contour line under every terrace. The inside is clear,
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

### B, Outcrop (recommended)

Closed, Outcrop is a stepped block of strata 155 mm tall. The deck is six laminae (tinted 3 / clear 12.7 ×3, 47.1),
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

- **The plinth** is laminated (tinted 3 ring / clear 12.7 / tinted 3 ring / clear 5.6 = 24.3), stepping 2 mm. *(v1 only. Since v2 the deck is two 12.7 sheets cemented flush, 25.4, through-tinted: see section 11's spec.)*
- **The posts** are torqued studs (rigid). Four stainless feet on Sorbothane locate and level it. Since the audit (2026-11-01), they make no isolation claim.
- **The motor** hangs from the plinth in the float's gap. Since the audit, it is screwed hard to the plinth as Rega fits it, with no grommets.
- **The base** is clear 12.7 under a tinted 3 ring. The light's slot is 6 deep and 25 in from the edge, in one closed
  loop of dotless COB strip (4.4 W). The black band is printed inside the stack.
- **The lid** is 3 mm 2064, 1.1 kg, within the hinges' rating.

A is the safer choice; B is the new idea.

## 4. Real details (Outcrop; A shares them unless noted)

`out-outcrop/drawings/details.png` draws A to F. `out-outcrop/numbers.md` has the arithmetic.

| detail | what | mass | cost (one off) | service |
|---|---|---|---|---|
| bearing and oil | Lead-free brass housing M30 x 1.5, clamped by its nut under the deck (10 N m, PTFE washer), with **no insert near the bore**. Two C932 bushes honed to 10 H6 on a 10 g5 440C spindle (8-12 µm). A 6 mm carbide ball on a lapped 52100 plate: 20 N, Hertz peak 2.3 GPa, under half the static limit. 2.5 ml ISO VG 32, filled to 10 mm under the flange. **Audit, 2026-11-01:** 1.0 ml, because the space is about 1.2 ml. A 1.0 x 0.3 vent flat runs along the spindle. The spindle is 440C in the parts list as well as on the drawing. The nut bears on a DIN 2093 63 x 31 x 1.8 disc spring and a brass washer, about 1.5 kN, so the preload holds over temperature (STOCK-AND-AUDIT.md 3.3). | 0.38 kg | housing $~90, nut, bushes $40, ball $5, plate $20, oil $15 | Lift the platter, hub and spindle out together; wipe; 1 ml of oil every two years with a syringe; lower it slowly. Shipping: that assembly in its own foam, a nitrile cap on the housing. |
| platter | Tinted 3 / clear 12.7 / tinted 5.6, cemented, annealed, turned to 300 x 21. Run-out 0.05. **Why acrylic:** PMMA's bar impedance (1.95 MRayl) is within 4 % of vinyl's (2.03), so only 0.04 % of the stylus's energy reflects at the record's underside; the rest goes into a material with a loss factor of 0.03-0.06 (aluminum about 0.0001). It doesn't ring, so there's no mat. I = 0.020 kg m2. | 1.74 kg (2.07 turning) | $170 + hub $71 | The six M4 screws hold it on the hub, so the bond carries no torque and the platter can be refaced and repolished. **Audit:** the screws now come up through the hub into bonded brass inserts at 0.6 N m, so no head bears on acrylic. |
| motor, belt, decoupling | Rega's 24 V motor on its plate, **hung on Rega's three grommets** in a pocket in the deck, so the pulley's height is fixed to the platter's by solid acrylic. Pulley 39.48 (250 rpm), 180 from the spindle, wrap 87°. Flat belt 5 x 0.6, path 992 mm, cut to about 945. **Audit:** the plate is screwed hard to the pocket's shoulder (three M3 into inserts), as Rega fits its motor; no grommets. The pulley is 32.8 if the motor runs at 300 rpm on the US Neo at 60 Hz, and is not turned until a bench test confirms it (STOCK-AND-AUDIT.md 3.1). | 0.41 kg | motor kit $265, screws $6, pulley $47, belt $30 | Three screws lift the motor plate out of its pocket; the belt is changed with the platter off. |
| arm and arm board | Rega RB330 at 222 on an **aluminum arm-board puck** (84 x 12, bead-blasted, Rega three-point), on three M5 into inserts. Another arm takes another puck. The record sits 28.8 over the deck's top; Rega spacers set the tube level on the first sample. | 0.46 kg | arm $675, puck about $40 | The arm comes off from below through the 56 bore. |
| arm rest and cueing | Rega's own lift and rest, on the arm's base. The lever sits to the right of the arm, front. | in the arm | in the arm | Rega's. |
| feet and levelling | **Three** turned stainless feet (40 x 12; brass read as amber through the tint) on Sorbothane 40 x 4, on M8 studs in bonded inserts, levelled by turning and locked with a nut. Three never rock. **They locate and level the deck; no isolation is claimed** (the audit, 2026-11-01). At about 50 Hz on 13 kg they do nothing in the speakers' 25-40 Hz feedback band, and they pass footfall. If isolation is wanted, it is a platform at 3-5 Hz under the record player. | 0.47 kg | stainless $~70, pads $20, studs $18 | Turn to level; replaceable pads. |
| external supply and connector | Rega's Neo PSU MK2 (mains, its maker's listing; check its US mark) drives the motor through its own lead in a groove to the back notch. The S2's own listed 18 V adapter plugs into a 2.1 mm jack on the brass plate. Nothing inside Outcrop is above 24 V. | | Neo $445 | Both are standard, replaceable boxes. |
| speed change | 33/45 on the Neo's button, trimmed in 0.01 rpm steps. One pulley diameter; the belt never moves. | | | |
| hinges and stays (A) | A: Pro-Ject's Debut friction hinges in 9.5 acrylic blocks on M4 into inserts (in shear), with a 1.1 kg lid. **B: none.** The cover lifts off on dowels. | | A $34 | |
| cartridge and phono cable | Ortofon 2M Black (or 2M Blue for the first build, round 43). The RB330's own lead goes down the puck's bore, along an 8 x 6 groove under the deck, into the **S2 in a tunnel from the back** (on felt runners). The S2 feeds the brass plate's 4PDT (stage or bypass) to the gold RCAs. A 4PDT switches the S2's input as well as its output, so in bypass the cartridge sees one 47k load and not two in parallel (the audit; it was a DPDT). Star earth at the plate's post: arm, bearing housing (M3 tag), S2. | S2 0.57 kg | 2M $750, S2 $269, plate hardware $48, wiring $25 | Four M3 screws hold the plate; the S2 slides out for its switches. |
| labels and rating | Laser-engraved and black-filled on the brushed brass plate: name, line out, 18 V DC 0.5 A (center +), SN, "Motor: Rega Neo PSU". EARF etched at the deck's front right, filled. No compliance mark until tested (the supplies carry their own). | 0.11 kg | plate about $50, etch $15 | |

**Heat:** none to speak of in Outcrop (the S2 draws 0.5 W in an open tunnel). In A the COB loop is 4.4 W in a 6 mm slot
open below, a third less a meter than the baseline's strip, through 25 mm of clear acrylic to the edge. The
baseline's first-sample thermocouple check stays.

**Cost against the baseline ($3,910):** Outcrop is $3,773 (about -$140) and Strata Float $3,822 (about -$90). Outcrop adds the turned stainless feet, the puck, the screwed hub, the threaded housing's nut and the cover's ten rings. It drops the light, the dimmer, the adapter, the rear box, the regulator, the posts, the bushings and the hinges. Strata Float adds the same turned parts and a COB loop, and drops the regulator, the rear box and the bushings. The kit prices every ring as a full rectangle of sheet. In practice the platter blanks, the puck's ring and the inlays nest inside the rings' offcuts, so the acrylic line is high. (An earlier figure of about $4,300 priced the feet as one bounding block of brass; they are now priced as three 45 mm blanks of stainless.)

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
| `outcrop-hero.png`, `-v2`, `-v3` | Outcrop, studio, cover off, Smoke (2064): first pass; the critics' notes (gray sweep, frosted etch, puck screws, stainless feet, polished bores); the arm's and the cartridge's details and the vinyl's sheen |
| `outcrop-closed.png`, `-v2` | Outcrop closed: the block of strata |
| `outcrop-detail.png`, `-v2`, `-v3` | the arm's corner; v3 close on the stylus and headshell (tag wires, screws, pins) |
| `outcrop-use.png`, `-v2` | a record playing (the label blurred at 33⅓, 1/8 s), the cover stood as the sleeve's frame, on a walnut sideboard; v2 lit through from a back window |
| `outcrop-ember.png` | Outcrop in Ember (stock 2423 Red, 14.1 % at 1/8 in, Beer-Lambert): the color as contour lines |
| `strata-hero.png` | Strata Float, studio, lid off, the base's loop lit |

The in-use frame was to have a hand on the cue lever. The procedural hand read as a cartoon, and it would have cost
the frame its realism, so the playing record carries the "in use" instead.

## 6. Blind scores and duels

Fresh blind critics, PROMPT-promo's scale (`critic/LOG.md` has every reply):

| frame | blind | duel against the site's current frame |
|---|---|---|
| current site frames (studio, dusk, open, detail) | 4.5 each | |
| `strata-hero.png` | 6.0 | **7.0** to 4.0 (studio-smoke) |
| `outcrop-use.png` | 6.0 | **6.5** to 4.5 (dusk-smoke) |
| `outcrop-hero.png` (v1; v2, v3 5.5 too) | 5.5 | **6.5** to 4.0 (studio-smoke) |
| `outcrop-detail-v3.png` | 6.0 | **6.5** to 3.5 (detail) |
| `outcrop-ember.png` | 5.5 | |

**The gate is passed by the duels** (four of four won by 2.5-3.5 points). No single blind score reached 7.0. The hero
stopped at the protocol's three rounds. What still holds the scores down, in the critics' words: the bought Rega arm
"reads generic" (it is generic), and the parts inside the clear strata read as debris. The color reads as a red
pinstripe, which is the honest look of thin stock tint (`critic/LOG.md`, the end).

## 7. The color pass (the coordinator: more color)

The owner's brand is color, and the critics read stock Ember's thin rings as "a red pinstripe". There were two
routes to more color, rendered with the same calibrated model (`render_color.sh`):

| frame | tint | what it shows |
|---|---|---|
| `outcrop-ember-wide-stock.png` | **stock** TruCast 2423, each tinted lamina 5.6 thicker (1/4 in tinted + 1/4 in clear in place of 1/2 in clear) | wider stock rings read **darker, not redder**: a 2423 path more than a few mm long goes near black. Stock tint gives a dark line, never a glow |
| `outcrop-ember-custom.png` | **custom pour**: EARF's Ember at a lighter dye loading, 25 mm passing Ember's `deep` (#F2A29C) | every stratum tinted through and still passing light: the color is the whole object |
| `outcrop-ice-custom.png` | **custom pour**, Ice (#B5D9EE after 25 mm) | the cool tint: a blue deck, the brass bearing seen through it |
| `strata-ice-custom.png` | **custom pour**, Ice | Strata Float in color |
| `strata-dusk-ember-custom.png` | **custom pour**, Ember, at dusk | Strata Float's base loop lit (40 x the day's strip), the room down to blue evening |

**What this says:** color like the speakers' needs the caster's own pour at a lighter dye loading. Stock sheet can only
draw lines. That is round 17's casting-partner question again, now with a number: the custom laminae are drawn to pass
Ember's `deep` after 25 mm: about 48 % of the light through 25 mm, about two thirds through 12.7. The stock frames stay the honest prototype look.

## 8. An EARF tonearm: concept only (`out-outcrop/drawings/arm-concept.png`, `arm_concept.py`)

The critics' "cooler" lists all ask for an arm that is EARF's own. This is drawing level, for the owner to weigh:

- **Not an acrylic wand.** PMMA's modulus is about a twentieth of aluminum's. A tube of the same mass and diameter is
  about ten times less stiff, so its bending modes fall about 3.3 times lower, deep in the audio band. The tube and
  bearing stay bought metal.
- **Route 1 (recommended): EARF's parts on a bought RB330.**
  - EARF makes a counterweight sleeve of strata around a tungsten core, a tinted finger lift, a rest column of strata
    and a strata arm board.
  - About $150-250 a set at 10-50 sets, plus the RB330 (estimates, not quotes).
  - Rega supplies OEM arms to other makers (NAD, Rotel). Whether its terms allow a changed counterweight is the first
    question to ask.
- **Route 2: a private-label arm.**
  - Ortofon has built arms for AudioQuest and Sumiko; Origin Live supplies some makers.
  - No terms are published. Plan on about $400-900 an arm at 50-100 a year (estimate).
- **Route 3: our own arm.** About $20,000-50,000 of development and a year of testing (estimate). Not for the first
  Mantle. SME left OEM arms in 2019 and Jelco closed in 2020, so OEM supply is thin.

Sources: Rega's OEM work (Wikipedia, Rega Research); Ortofon's OEM arms (The Absolute Sound, AS-212R review); SME's exit
(Stereonet, 2019); Jelco's closure (Stereonet forum, HiFi News "A call to arms"); Origin Live's OEM supply (Stereophile).

## 9. Strata Float v2 (`mantle_strata_v2.py`, `out-strata-v2/`, $3,784)

The coordinator's blind head-to-head put Strata Float over Outcrop: 3-1, mean 6.4 to 5.5, distinctiveness 6.9 to
3.9. Its idea is "the floating glass turntable". Every critic named the same five faults, and v2 fixes them; v1 is
kept as it was.

| fault (the critics) | v2 |
|---|---|
| supports on two grids: inboard posts, corner feet | **one grid**: the four feet stand directly under the four posts |
| two tiers the same size ("stacked trays", "a display stand") | **the base is subordinate**: 35 mm in from the deck all round and 9.5 thick (was 15.7), so the deck overhangs it and floats |
| double-sheet decks and seams | **each tier one slab**: the deck is two clear 12.7 sheets cemented flush (one bond line, mid-edge, no steps, no rings); the base is one sheet. For color, each sheet is the custom pour |
| screws seen through the clear posts | **none**: each post is bonded at both ends; each foot's M8 insert sits in a blind hole drilled up through the base, 4.5 mm into the post's foot |
| a bold white mark on the top | **a small etched mark** (EARF, 18 wide) in the deck's front edge, low in its lower sheet |

The printed band over the light is gone too. The strip sits in a black anodized U-channel in the base's slot, and the
channel's closed back hides it from above. The posts moved 15 mm inboard and the slot 10 mm outboard, so neither
crosses the other (0 clashes).

**A product note on dust:** two clear sheets 40 mm apart show what settles between them. The gap is open on four sides
and is wiped through with a soft brush. The phono stage there sits on felt runners and lifts out.

| frame | what |
|---|---|
| `strata-v2-ice-custom.png` | studio, the same rig as `strata-ice-custom.png`, custom-poured Ice |
| `strata-v2-dusk-ember-custom.png` | dusk, custom-poured Ember, the base's loop lit |

## 10. Strata Float v3 (`mantle_strata_v3.py`, `out-strata-v3/`, $3,800)

The coordinator's duels: v2 beat v1 3-1, and v2 and Outcrop split 2-2 (distinctiveness 6.0 to 4.75). All eight judges
named the same details under the float, and v3 answers them; v2 stays as it was.

| the judges | v3 |
|---|---|
| the base reads as "a thin, paler accessory tray", its channel line as printed trim | **the base recedes**: stock smoked 2064 in every version (the color is the deck's), 12.7 thick, the deck's corner radius, the same 35 setback on all four sides. The channel is lost in the smoke |
| the clear posts read as "jars with parts inside" | **solid posts**: turned 303 stainless, polished, 30 across. Each is bonded into a 2 mm seat under the deck with a structural methacrylate (Plexus MA310 kind) and held from below by its foot's M8 stud through the base. Nothing shows. The isolation is the Sorbothane pad under each foot |
| the etched mark still reads as printed white | **a polished recess, tone on tone, on the back edge** |
| top-heaviness | the base is heavier (12.7 smoke, was 9.5 clear) and darker, so the deck no longer sits on a pale sliver |

**At dusk** the smoked base passes little of the strip's light through its edge (12 mm of 2064 is about 1 %). So the
strip runs brighter, and most of its light falls from the open slot onto the shelf: the deck floats on a pool of light.
The render's emission was set by eye for the frame's exposure, not converted from the strip's watts. The real loop runs at most at its rated 4.4 W, and whether that is bright enough at dusk is a first-sample check.

| frame | what |
|---|---|
| `strata-v3-ice-custom.png` | studio, v2 r2's rig, custom Ice deck over the smoked base |
| `strata-v3-dusk-ember-custom.png` | dusk, custom Ember deck, the light pooled under the smoked base |

## 11. The owner's pick: Strata Float v3, in the line's stock tints (2026-11-01)

The owner picked A, Strata Float v3, at about 12:10 UTC (r46-owner-notes 5b63e05b), after the stock-tint sheets
(`STOCK-AND-AUDIT.md`, section 1). Outcrop is set aside. What followed, all proposals until the owner signs:

- **The shared audit fixes** (`STOCK-AND-AUDIT.md`, section 3):
  - the pulley waits for a bench test on the US Neo;
  - a 4PDT bypass;
  - the bearing: 1.0 ml of oil, a vented 440C spindle, a disc spring under the nut;
  - no isolation claim for the feet;
  - the motor hard-mounted as Rega fits it;
  - the platter screwed from below into bonded inserts.
- **A product block for other lanes' scenes:** `studio/products/mantle-strata-v3.json`, written by the build. Its
  flavors are the line's stock codes: poison-2092 (the default), ember-2423, smoke-2074, haze-2287 and ice-2069. The
  base is stock Smoke 2074 under every flavor. Proofs: `renders/2026-11-01/barkhorn/mantle-r48/block-proof-*.png`.
- **The rear plate** (the audit: Strata had nowhere to mount its jacks, no wiring or earth drawing, and no rating):
  - 2 mm brass on the base's back edge at the back right, under the deck's 35 mm overhang, so it never shows from
    the front;
  - the upper row: line out, the earth post (the star), the 4PDT and the light's switch;
  - the lower row: the S2's 18 V inlet (2.1 mm), the light's 24 V inlet (2.5 mm, so the plugs can't be swapped) and
    the Neo's inlet;
  - the rating engraved along its foot.
  - The plate, the wiring and earth diagram, the section and the label text are in
    `out-strata-v3/drawings/rear-panel.png` (`strata_rear.py`).
- **The light** (the audit: an 8 mm strip in a 5 mm slot with 2 mm corners, on a 25 W supply):
  - a 5 mm 24 V COB strip of 5 W/m or less, in four straight runs on a mitred black U-channel 7 x 7, in a slot
    7.4 x 7 routed from below, facing down onto the shelf;
  - about 1.2 m and 4.9 W, on a listed Class 2 adapter of 12 W;
  - no PWM dimmer inside, so the record player stays on the PS1 path.
- **The budget** goes from $3,877 to $3,798: the dimmer is out; the plate and its hardware are in. Pricing the deck's two
  sheets as stock tint, which is what they are (the parts list had them as clear), brings it to **$3,850**.

### The spec as built (`mantle_strata_v3.py`, after 9e72cf70; the site's copy should match this)

| | |
|---|---|
| deck | two 12.7 mm sheets of stock cast acrylic in the flavor's tint, cemented flush: 25.4 mm, through-tinted, one bond line; 450 x 360, the outer edge satin, the faces glassy |
| float | the deck floats 40 mm over the base on four solid 303 stainless posts, 30 mm across, polished, bonded under the deck |
| base | one 12.7 mm sheet of stock Smoke 2074, 380 x 290, 35 mm in from the deck all round; the light's loop under it, falling onto the shelf |
| lid | 3 mm stock sheet in the flavor's tint, a five-sided box 448 x 358 x 100, on Pro-Ject's friction hinges |
| size | 450 W x about 370 D (with the hinges) x 94 H to the deck's top, about 199 H with the lid closed |
| weight | about 12.9 kg with the lid (11.8 without); the supplies are outside it |

## 12. The light up through the acrylic (2026-11-03)

The owner (r46-owner-notes 15c15784): "I think mantle has the same issue where the underglow is projected down instead
of casting through the acrylic." A light must shine through the acrylic so the piece glows from within: on in night
pictures, off in day ones. Section 1 had already named the fault ("an emissive stripe, not light travelling through
acrylic"), and 2026-11-01's `a-dusk-ember-2423.png` shows it: warm light pooled on the shelf.

**What changed (a proposal until the owner signs it).** The deck is now edge-lit, the way an acrylic sign is.
- The strip lies in a groove routed into the deck's underside, 10 mm in from its edge: 7.4 wide x 7 deep, one loop of
  four straight runs.
- It sits on the floor of a black U-channel, open face up, and faces up into the slab.
- The groove's ceiling is bead-blasted, so the light spreads into the acrylic rather than beaming straight up.
- The slab carries the light to the satin outer edge, already bead-blasted since v3. The edge glows, and a soft line
  shows through the top over the groove.
- Below, only the channel's black floor shows. Nothing falls on the shelf but a faint spill.
- The base has no light now, and its slot is gone. That leaves the base solid except for the feet's studs and the
  rear plate's inserts.
- The lead leaves the groove at the back right and drops 4 mm onto the rear plate, under the deck's overhang.

**Tried first, and dropped.** A strip in a groove on the base's top, facing up through the gap into a frosted band
under the deck. From any normal eye height it shows through the float's gap as a bright line: the stripe again.

**Supply.** The light keeps its own: a listed Class 2 24 V 12 W adapter into the rear plate's 2.5 mm inlet, through its
SPST. FAULTS.md item 9 (the light and the phono stage sharing one adapter on a Y lead) was fixed by the rear plate
(9d617c0c): the S2 has its own listed 18 V adapter on its own 2.1 mm inlet.

| | |
|---|---|
| parts | the strip, 5 mm 24 V dotless COB, 2700 K, CRI 90+, 5 W/m or less (about 4 W/m chosen): about 1.51 m in four runs, soldered jumpers at the corners; the U-channel 7 x 7, black anodized, about 1.5 m, mitred, bonded with neutral-cure silicone; the adapter and SPST as before |
| power | about 6.0 W at 4 W/m (7.6 W at most at 5 W/m), 0.25 A at 24 V: half the 12 W adapter's rating, a PS1 circuit |
| heat | about 4 W/m inside acrylic, which spreads heat poorly: about 10-15 K over the room at the channel (an estimate). Acrylic is good to about 80 C; check with a thermocouple on the first sample after an hour on |
| the deck | a groove 7.4 x 7 routed into its underside, 10 in from the edge, its ceiling bead-blasted (the same blast as its satin edge); clear of the post seats, the arm's bore and puck screws, the motor pocket and the hinge inserts by 2.7 or more |
| the base | nothing; its slot is gone |
| cost per unit | strip and channel about +$10 (1.5 m against 1.2 m); the groove is one more pass on the deck's routing and the ceiling's blast goes with the edge's, about +$10-15; the base's slot (about -$5) is gone: about **+$15-20** in all, an estimate |

**The frames** (`renders/2026-11-03/barkhorn/mantle-r48/`; the dusk camera of 2026-11-01's `a-dusk-ember-2423.png`; the
strip at its physical output, about 300 W/m2 off its 5 mm face, not set by eye; `render_glow.sh`):

| frame | what |
|---|---|
| `a-night-ember-2423.png` | night, the light on, stock Ember: the rim and the edges glow red from inside; no pool on the shelf |
| `a-day-ember-2423.png` | day, the light off: the groove barely shows through the deck |
| `a-night-poison-2092.png` | night, stock Poison: a thinner green line (green travels less far in 2092) |

**The blind critic, one round:** 5.5 on the Ember night frame, against the owner's bar of about 6.5. It reads as "a black
gaming-PC-style turntable with red LED edge strips" (`critic/LOG.md`). Most of the gap is the stock tint: Ember passes
about 2.2 % through the 25.4 deck, so even lit from inside the deck reads as a black slab with a glowing rim. The
critic's "whole slab as a red lantern" needs the lighter deck of open question 8. It also asked for a red pool on the
floor, which the owner has ruled out.

## 13. Round 2: the deck as a lantern (2026-11-03)

The coordinator, on section 12: "Neon outlines on a black slab aren't what the owner means." At night the whole deck
should glow evenly in its color, like a lantern. It should have no outline, no inset line and no floor pool, and it
should stay good by day. All of this is a proposal until the owner signs.

### (a) v4, the lit deck (`mantle_strata_v4.py`, `out-strata-v4/`; v3 stays as it was)

| layer | what |
|---|---|
| top, 3 | the flavor's stock tint, through: a thin skin, as Tropos's color sits over its white lining |
| core, 9.5 + 12.7 | two clear inlays, each cemented edge to edge into a 10 wide ring of the same tint, so the deck's edge reads tinted all round; together a 22.2 light guide |
| the core's underside | screen-printed white dots, about 10 % cover near the strip rising to about 70 % at 140 in (graded, as a backlight's guide is, so the glow is even), then overprinted black; the print runs over the posts' seats |
| the strip | in a 7.4 x 7 groove routed into the core from below, 11.5 in from the deck's edge (just inside the ring), on its black U-channel, facing up under a bead-blasted ceiling |
| the holes' walls | the bearing, the arm's bore, the motor pocket and the puck screws, painted white toward the acrylic, then black |

- **How it works.** The light spreads through the clear core and scatters off the dots. It leaves up through the 3 mm
  skin, so the deck glows in its color all over, from within. The black overprint and the channel's floor keep all
  of it out of the gap and off the shelf.
- **Overall** the deck is 25.2 mm (3 + 9.5 + 12.7), about 25.4 with its bond lines, as before.
- **Bonding.** The rings and the inlays are cemented edge to edge (ACRIFIX 2R 0190). The top is cemented over both
  in a vacuum press. The print stays on the core's underside, not in a bond line.
- **The float's look.** From above, the deck no longer shows what is under it. The bearing and the motor are hidden
  by the print, though in stock Ember they barely showed before. The float seen from the side, through the gap, is
  unchanged: the posts, the motor's can and the S2.
- **By day** the deck reads as colored glass over white, not black glass. Tropos does the same with its colors F.
  This is the owner's parked question ("should its deck read like the speakers' green glass?").
- **Tried first.**
  - 12.7 of stock tint over a 12.7 core passed too little. The glow left by the edges, as a line at the bond.
  - A strip on the base's top facing up showed through the gap as a bright line (section 12).

| | (a) v4 |
|---|---|
| power | the same strip, about 1.50 m at 4 W/m: about 6.0 W (7.5 W at most at 5 W/m), on its own listed Class 2 12 W adapter (unchanged; the phono stage has its own) |
| heat | as section 12: about 10-15 K over the room at the channel (an estimate); a thermocouple on the first sample |
| cost per unit | about +$120-150 over v3 (estimates): the sheets (a clear 12.7 and 9.5 and a tinted 3 in place of a tinted 12.7) about +$57 in the parts list; cementing two rings to their inlays about +$40; the screen print and its black overprint about +$20-30 a unit, plus about $150 for the screen; painting the holes about +$10 |
| the deck needs | the rings and inlays, the print, the painted holes, the groove in the core; the satin edge as before |
| the base needs | nothing |

### (b) a lighter deck pour, as a comparison (open question 8; a custom batch, the owner's yes needed)

v3's edge-lit deck, its two 12.7 sheets in Ember 2423's hue poured to about 40 % TT per 1/2 in (scene.py `ember-40`,
#F5A0AB after 10 mm). The cost is the estimate of 2026-11-02 (the Poison reconcile): a custom 12.7 run is about $12.5k at the pour's minimum,
for about 90 decks, about +$27 a deck.

### The frames and the critic

`renders/2026-11-03/barkhorn/mantle-r48/`, the camera of 2026-11-01's `a-dusk-ember-2423.png` (`render_lantern.sh`):

| frame | what |
|---|---|
| `a4-night-ember-2423.png` | (a) at night: the whole deck glows red, evenly, from within; no outline, no inset line, nothing on the shelf |
| `a4-day-ember-2423.png` | (a) by day: red glass over white |
| `a4-night-poison-2092.png` | (a) at night in Poison: an even green glow |
| `b-night-ember-40.png` | (b) at night: still a neon outline. A lighter pour alone does not make a lantern; the light needs the white print to leave by the face |
| `b-day-ember-40.png` | (b) by day: a lighter red glass, the parts under the deck showing through |

**The blind critic, one round:** 5.5 on (a)'s night frame, the same score as section 12's for other reasons. The outline
is gone, and the critic now reads "an acrylic deck lit like a gaming-PC LED panel" (`critic/LOG.md`). Two of its notes
are settings or the renderer:
- the top clips (the night exposure, a stop over the day's): a stop down keeps it deep red;
- the shelf gets no red from the glowing deck (a caustic path Cycles drops here). A real deck would throw a faint red
  spill, which the owner allows.

### The render (how the light is drawn)

The guide's output is drawn as an even Lambertian glow just above the print: 9 W/m2. That figure follows from the
strip's power, not from the picture: 6 W in, about 2.25 W of light, about 80 % into the core and 70 % out, over about
0.136 m2. Cycles cannot sample the real path (a diffuse bounce inside glass, then glass, then the strip) in useful
time. By day the room's light on the print is baked the same way, at the strength the albedos give, within about half a
stop. The scene's face classification had read the meshes' own frame, which is Y-up, as the world's. It is fixed for
v4's deck and left as it was for the frames already made.

## Open questions for the owner

1. **A or B,** or B's cover on A's float. *(Answered 2026-11-01: A, Strata Float v3.)*
2. **The thin-tint stack** depends on 2064 being as dark as its chart says. The chips and a 1/2 in offcut settle it.
   If the caster pours EARF's own tints lighter, thicker tinted strata come back as an option.
3. **Outcrop's cover is 2.9 kg.** A 3 + 3 top instead of 5.6 + 3 would bring it to about 2.4.
4. **Outcrop has no light.** If the owner wants the glow, A's lit base can go under Outcrop's deck on four short clear
   posts, at A's cost.
5. **Cartridge:** the 2M Black ($750), or the 2M Blue ($220) for the first build (round 43).
6. **Color:** stock sheet only draws dark lines. Do we ask the caster for EARF's tints at a lighter dye loading, in 3 and
   12.7 mm (section 7)?
7. **The arm:** keep the RB330, or ask Rega about EARF's own counterweight, finger lift and rest on it (section 8)?
8. **The deck as glass:** in the stock deep tints, Strata's 25.4 deck passes 1.5-3.7 % and reads as a deep colored
   slab. A custom pour for its two sheets only, at about 35-40 % TT per 1/2 in, would make it read as glass (about
   12-15 % through). The owner decides after the color chips are measured (`STOCK-AND-AUDIT.md`, section 2).
9. **Dimming the light:** none inside now. If it is wanted, use a listed Class 2 dimmer in the adapter's lead,
   outside the record player.
