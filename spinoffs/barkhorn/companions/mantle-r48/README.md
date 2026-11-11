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

Since 2026-11-10 Mantle has **no light** (the owner: "Forget the lights on mantle"). The rows below are updated; the
light notes above and in sections 12 and 13 are history. See "No light" at the end of section 13.

| | |
|---|---|
| deck | two 12.7 mm sheets of stock cast acrylic in the flavor's tint, cemented flush: 25.4 mm, through-tinted, one bond line; 450 x 360, the outer edge satin, the top glassy, the underside bead-blasted satin (2026-11-10) |
| float | the deck floats 40 mm over the base on four solid 303 stainless posts, 30 mm across, bonded under the deck; satin black (the owner, 2026-11-10): hot black oxide for stainless, the lamps' #18181A |
| base | one 12.7 mm sheet of stock Smoke 2074, 380 x 290, 35 mm in from the deck all round; solid, no light (2026-11-10) |
| hardware | every visible piece satin black (2026-11-11): the arm puck and pulley black anodized, the feet hot black oxide, black-oxide screws and studs, the cartridge's screws and washers black, the arm's counterweight and trim black (to confirm with Rega); bright by necessity the spindle's tip and the cartridge's cantilever, pins and diamond; $115 (an estimate), budget $3,957 |
| bearing, hub | no brass in sight: the bearing's housing, nut and washer (2026-11-10), the platter's hub and its six inserts (2026-11-11) black nickel plated on the brass, satin, to match the posts; the rear plate, hidden under the deck, stays brass |
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
| `a4-night-ember-2423-r2.png` | (a) at night, a stop down (the coordinator's pass, 07:39): the top deep red glass, not a flat salmon field (its clipped share 25 % to about 1 %); the room at 0.6 % so the record and arm read; nothing added on the floor |
| `a4-night-poison-2092-r2.png` | the same in Poison: deep green glass |
| `b-night-ember-40.png` | (b) at night: still a neon outline. A lighter pour alone does not make a lantern; the light needs the white print to leave by the face |
| `b-day-ember-40.png` | (b) by day: a lighter red glass, the parts under the deck showing through |

**The blind critic, one round:** 5.5 on (a)'s night frame, the same score as section 12's for other reasons. The outline
is gone, and the critic now reads "an acrylic deck lit like a gaming-PC LED panel" (`critic/LOG.md`). Two of its notes
are settings or the renderer:
- the top clips (the night exposure, a stop over the day's): a stop down keeps it deep red;
- the shelf gets no red from the glowing deck (a caustic path Cycles drops here). A real deck would throw a faint red
  spill, which the owner allows.

### The coordinator's gate, pass 1 (08:15): what the judges found and what changed

The judges found three things:
- by day the top matched the lit night top, reading as "coral lacquer": a 3 skin over a dense white print reads as an
  opaque white backer;
- at night the top was a flat, near-clipped lightbox in primary colors;
- the groove and the bottom arris read as neon lines.

What changed (`mantle_strata_v4.py`, rebuilt with 0 clashes, **$3,897** in the parts list):

| | before | now |
|---|---|---|
| skin | 3 of the stock tint | **5.6** of the stock tint: deeper color by day and by night |
| core | 9.5 + 12.7 | 9.5 + 9.5; the deck **24.6** (about 24.8 with bonds), 0.6 under the spec's 25.4, a change for the owner to sign |
| dots | 10 % rising to 70 % | **5 % rising to 35 %**: by day the skin reads as color inside glass, not over a white backer |
| groove | its ceiling bead-blasted (seen from above as a line) | its ceiling printed white over black, opaque from above; the strip's light enters the core through the groove's clear sides |
| the rings' undersides | glossy | printed black: no light leaves by the bottom arris |
| strip | 4 W/m | **2 W/m** (about 3 W): the glow about a stop under before, 4 W/m2 |

The cost stays about +$120-150 a unit over v3. Printing the groove's ceiling and the rings' undersides goes with the
dot print, and the skin and core sheets net about -$10 in the parts list.

How the new frames are drawn (`render_lantern.sh g1`):
- **Night:** the guide's glow is graded, brighter at the strip's edge and softer inside, as a gentle dot ramp gives.
  One large, dim, soft source behind the deck, unseen by the camera, lays a long reflection across the glossy skin.
- **Day:** the room's light on the print is baked for the new build, at about half the old strength. The sparser dots
  and the deeper skin account for that.
- With no room-light term at all, the deck reads black by day. Cycles leaves a print sealed under glass unlit; the real
  deck would not read black.

The third judge (08:17) added five fixes. All of them are in the frames:
- **Hardware at night:** a low warm kicker and rim, small and tight and unseen by the camera, so the arm, the posts,
  the base's edge and the feet read. The floor stays neutral.
- **The red bar on the base's top** (its mirror of the deck's lit end): the base's top is now a fine satin, a real
  finish (machined, then fine-blasted).
- **Poison:** its glow a stop up, so the top is the light source and its edges read as see-through green glass.
- **Framing:** the camera panned 50 mm, the same for the set, so the deck has room on both sides.
- **Day:** the print's room light is shaded round the platter and the arm plate, and baked a little lower (7). The top
  reads as deeper ruby with depth, clearly unlike the lit night face.

| frame | what |
|---|---|
| `a4-night-ember-2423-g1.png` | Ember at night after the gate's fixes |
| `a4-night-poison-2092-g1.png` | Poison at night after the gate's fixes |
| `a4-day-ember-2423-g1.png` | Ember by day after the gate's fixes |

### The gate's second pass (09:30)

The three judges found the underglow fixed: there is no colored light on the floor or the base in either night. Five
notes were left; each is fixed in the model or the scene, not per frame (`render_lantern.sh g2`).

- **No light out of the edges.** A white-backed reflector tape now runs round the core's perimeter, white toward the
  core and black outside (3M or Oracal kind, about $1 a deck). The core's light leaves only up, through the dots, and
  the four edge faces read as dark tinted glass at night.
- **No lit border.** I kept the 10 mm tinted border, which is truer to Strata Float, since the deck's edge stays tinted
  glass, not a clear core edge. The rings' tops are printed black before the skin is cemented on, so no light reaches
  the border.
  - The cost of that: by day the border and the edges read as dark tinted glass round a ruby field, not as the
    richest red.
  - Taking the tint full-bleed would mean a clear core edge behind reflector tape, a grey band on every edge. I chose
    the border.
- **The top carries the glow.** It is graded brighter in the field than at the rim. Poison's glow is raised, so its
  top is the light source.
- **No white key at night.** The large reflector and the front kicker are gone. A single low rim sits behind and
  under the record's plane, so the vinyl cannot mirror it, and gives the posts, the base and the feet their shape.
- **No amber glint by day.** The bearing's nut, washer and housing under the deck are chemically blackened on the
  brass, so they no longer read as a light left on.

### The gate's third pass (10:16)

The day frame passed 3/3, and the underglow stays fixed. Both nights were held: they did not read as tinted glass and
they read as cheap. The fixes (`render_lantern.sh g3`, all in the model or the light):

- **The edge stripe** was the 5.6 skin acting as a light guide. Light trapped in it by total internal reflection left
  through its polished edges. The skin's four perimeter edges are now painted black after polishing: masked, one coat
  of black acrylic lacquer, about **$8-12 a deck** in labor.
- **The bright band just inside the rim** was the print over the groove's ceiling. It sits right over the strip.
  - That ceiling is now printed black, an opaque band over the strip.
  - The core's perimeter tape is black, not white, so it absorbs what reaches the rim.
  - The dark tinted frame now reads about 19 mm wide.
  - The glow is graded darker toward the rim: 0.5 at the rim, rising to 1.1 inside.
- **The color is derived, not picked.**
  - The strip is a 4000 K COB, the speakers' CCT, drawn as a blackbody at 4000 K.
  - The tint comes from the 5.6 skin's own absorption on the way out.
  - The lamps lane's note (r32-lamps-final, `launch/stock-tints-lamps.md`) was not found at that path, so the
    derivation is the render's own.
- **The light:**
  - exposure down half a stop;
  - the speaker lane's night set: a wall close behind, the floor #2A2D33 at roughness 0.15, a low navy ambient, so the
    record, the platter and the arm read and the top has a room to reflect;
  - no rim and no kicker, so there is no lamp pool on the floor and no grey wash on the deck's side;
  - more samples, for less grain.
- **The strip's own emitter is off in the render.** The glow sheet is the strip's whole output once it has spread; with
  both on, the light counted twice at the groove.
- **The day frame** is re-rendered, because the black skin edges and the masked band change it.

| frame | what |
|---|---|
| `a4-night-ember-2423-g3.png` | Ember at night after the gate's third pass |
| `a4-night-poison-2092-g3.png` | Poison at night after the gate's third pass |
| `a4-day-ember-2423-g3.png` | Ember by day after the gate's third pass |

### The gate's fourth pass (11:26)

The judges: the underglow and the edge lines are gone, and Ember's glow holds the day hue. The nights were still held
on "tinted glass" (Poison read as "gaming"). By day the black edges and the masked band read as "a lacquer inlay in a
black tray". The fixes (`render_lantern.sh g4`):

- **The glow lights the world.** Shadow rays now pass the flat acrylic, tinted by it. The tonearm's pillar, the arm
  rest, the tube and the platter's sides catch the glow from below. It stays upward only: the floor and the base keep
  their dark.
- **Depth:**
  - the glow is half a stop down;
  - a short vignette at the bezel, instead of a hard step;
  - a broad gradient, brighter at the front and deeper toward the far corners;
  - a dim wash on the wall behind, a lamp out of frame, lays a broad soft reflection across the glossy top.
- **Poison's color.** The render's Poison passed too little red. Its day hue was 138 deg CIELAB, a screen green; the
  lamps lane's table gives 122. Its red is matched to 122, so lit at 4000 K the brightest part leans yellow-green, as
  the lamps' 111 deg says it should.
- **Mottling.** The acrylic's wear is lighter (its fine scratches read as wrinkles under the glow), with more samples.
- **The base and the float read.** The navy ambient is up.
- **The tray, by day.** The coordinator's idea is physically right.
  - The rings' tops are printed white up, black down, as the field's dots are. By day the border reads as tint over
    white, ruby like the field.
  - At night no light reaches it: the core's black edge tape and the rings' black inner walls stop it.
  - The groove's ceiling has the same print, so by day there is no dark band.
  - The skin's black edge paint stays: it is only 5.6.
  - Cost: a second screen pass, about +$10. The line becomes about **+$140-170 a unit**, $3,897 in parts.
- **Small:** the posts' seats' walls are clear, so the front disc no longer reads as a control (it was a post's
  bonded seat seen through). The platter's polished rim is a soft satin, so there is no white ring.
- **One honest note on the render.** The glow over the groove's ceiling rendered 1.6x the field at the same strength,
  and I could not find why. It is scaled to the field, as the real white print there would be lit.

| frame | what |
|---|---|
| `a4-night-ember-2423-g4.png` | Ember at night after the gate's fourth pass |
| `a4-night-poison-2092-g4.png` | Poison at night after the gate's fourth pass |
| `a4-day-ember-2423-g4.png` | Ember by day after the gate's fourth pass |

### Is "lacquer by day, lightbox at night" inherent to v4? (the coordinator's question, 12:33)

**Mostly, yes.** v4 is a backlight. It is a light guide with a printed backer: white dots on black, under a tinted skin.

- **By day** the eye sees the tint over the backer. The backer is mostly black, with 5-35 % white dots, so the slab reads
  as color on an opaque ground: lacquer, or an inlay. Nothing below it shows, so it has no depth.
- **At night** the print exists to make the output even. Even output is the definition of a lightbox.

Renders can soften both, with grading, reflections, exposure and gloss, but they cannot remove them. What would give
real depth, with what each does to the night look and to the cost (all estimates, all proposals):

| option | by day | at night | cost per unit over v4 |
|---|---|---|---|
| **A. v4 as is** | tint over an opaque backer: lacquer, no see-through | even, graded glow: a lit panel | — |
| **B. a thicker skin** (9.5 or 12.7 of tint, the core thinner) | deeper color; it darkens toward grazing angles (the path through the tint grows), a real depth cue; still opaque | about half to one stop dimmer; deeper red; still a panel | about +$15-25 (sheet) |
| **C. a partly clear field**: the print only in a band round the rim, or in a pattern, with clear windows elsewhere | through the windows you see down into the float: the posts, the motor, the base, the bearing. That is real depth | the glow only where it is printed: a lit frame or pattern round a dark clear center. Guided light stays in the clear windows (total internal reflection), so little leaks down | ±$0 (the same print, a new layout); design time |
| **D. a light-diffusing core** (an edge-lit diffusing acrylic, Acrylite EndLighten or Plexiglas LED kind, its particles scattering light through its whole volume, with no print) | tinted glass with a faint haze; you see into it if nothing opaque is under it | the whole volume glows, soft and deep, not a flat panel. **But** it emits down as much as up, so without a backer it lights the base and the shelf, which the owner ruled out. With a backer it is opaque again by day | about +$40-60 (the sheet), plus a backer if the floor must stay dark |
| **E. a stronger graded print** | a visible tone gradient under the tint; still opaque | a visible falloff from the lit edge: some depth, no line; still a panel | ±$0 |

**My reading.** Only C gives real see-through depth by day while keeping the floor dark at night. It costs the
"whole deck glows" look: at night it becomes a lit frame or pattern. B and E soften v4 but keep its nature. D is the
truest "glows from within" at night, but it breaks the owner's rule unless it is backed.

This is the owner's decision, not a matter of repainting. The g5 frames are v4 at its best as built.

### Option C, rendered (2026-11-03, the coordinator's request after the gate's fifth pass; `mantle_strata_v5.py`)

The gate held v4's Ember pair on tinted glass alone, as predicted, so v4 stops at g5 as option A. Option C is a design
exploration for the owner. Every part of it is a proposal.

**The layout.**
- **The print** is graded by distance from the spindle. It is dense under the platter (60 % cover) and thins
  linearly to clear glass by 230 mm out. The outer deck and the border are clear tinted glass.
- **The light is fed from the center, not the rim.** The strip runs in an octagonal groove at r 78, eight straight
  runs, under the platter, where nothing sees it. Its corners clear the posts.
  - I changed the coordinator's layout here, and this is why: fed from the rim, the strip would sit under the clear
    outer glass and show as a line by day and a lit line at night, the rejected edge strip again.
  - From the center, the light spreads outward. At night the glow is a halo round the platter fading into clear
    glass, with no source, band or outline anywhere.
- **The edges:** the skin's black edge paint and the core's black edge tape stay, so the light that reaches the rim dies
  there.
- **Power:** 0.54 m of strip at 4 W/m, about 2.2 W, on the same adapter.
- **Cost:** about the same as v4 (the same print in a new layout; the border print is gone), so about +$130-150 a unit
  over v3. $3,897 in the parts list.

**The leak, measured.** Light guided into the clear zone stays in the slab by total internal reflection, top and
bottom alike. It leaves the bottom only by scatter, from dust and polish marks, a few percent. What the render does
show is the Fresnel share: a few percent of the glow is reflected back down at the inside of the top surface, and in
the clear zone nothing stops it. It falls on the base under the clear zone at about R 11 of 255, about 4 % of the
field. The floor in front stays dark (4,6,14). That is a real, faint spill, not a pool.

| frame | what |
|---|---|
| `a5-night-ember-2423-c.png` | option C at night: a halo round the platter fading into clear glass |
| `a5-day-ember-2423-c.png` | option C by day: the outer deck clear tinted glass, the float seen through it |

### Option C, gate 1 (2026-11-03, the coordinator's 14:21 fixes)

The gate held C 3/3 at night: red on the base's top (R 13-16) and a red pool on the floor in front, a crescent at the
platter's foot, a black outer zone, an amber glint under the deck, and the label's wordmark behind the spindle.

**Where the downward light came from, measured on proxies (900 x 600) against A's g5 on the same settings.**
Red, of 255, in fixed patches. "Base spots" are the two patches near the posts; "floor" is in front of the base.

| run | base top | base spots | floor L / R | platter foot |
|---|---|---|---|---|
| A, g5 | 4.7 | 0 / 0 | 6.6 / 5.0 | 135 |
| C as gated | 8.1 | 10.8 / 7.2 | 15.8 / 16.0 | 163 |
| C, solid backer under the platter, backed dots, clear gaps | 4.4 | 15.4 / 12.0 | 16.8 / 14.6 | 109 |
| the same, with a thin-film AR coat on the top (MgF2, 100 nm) | | 13.8 / 11.2 | 16.0 / 14.0 | |
| the same, glow off (room light only) | | 0 / 0 | 6.7 / 5.5 | |
| the same, every gap backed (a control) | | 0 / 0 | 6.4 / 4.9 | |

- It is the glow, and only through the clear gaps: with the glow off, or with every gap backed, the base and floor
  match A.
- It is not mostly the top's ordinary Fresnel reflection: the AR coat cut little. Most of it is the light near the
  critical angle (about 38-42° inside). The top reflects a large share of that back down. Leaving through a bare gap,
  it refracts out almost flat, at grazing angles, onto the base's glossy top and the floor in front: the spots and the
  pools. No coating removes that. Any patch of lit glass you can see through sends some light down.
  - The options table's line for C ("little leaks down") was wrong about this. Light guided past the dots stays in,
    but the light the dots scatter does not.
- So a clear see-through window and no downward light cannot both hold where the glass is lit. C keeps the floor
  dark, as the owner ruled, and gives up the see-through field.

**The fixes, as rendered (`render_lantern.sh c2`).**
1. **Downward light:** the whole printed field is backed black: the white dot print, then a black flood over it, as on
   A. Nothing is printed under the platter: there is only the backer, which also hides the strip and its channel. The
   clear border ring stays as it was. On the proxies the base and the floor now match A: base top 4.4 against 4.7,
   base spots 0, floor 6.4 / 4.9 against 6.6 / 5.0. The lifted difference shows red only on the deck itself.
2. **The grade:** flatter, and peaking about 35 mm off the platter's foot. The glow rises from 55 % at the foot to its
   peak, then falls to 55 % at 280 mm out. The platter foot now reads about 96, against A's 135 and C's old crescent at
   163.
3. **The outer zone's floor:** the print never thins to nothing. At night the rim glows deep Ember (R 77 at the left
   rim, against A's 72), not black. By day the print is even (18 %), so the deck is an evenly tinted sheet, not a
   vignette. The night grade is then the guide's own fall-off: light fed from the center thins outward, so an even
   print would fall off by itself. The rendered grade stands for that; the print's exact ramp is set on the first
   panel with a luminance meter.
4. **The glint** was the strip's aluminum channel, seen through the clear underside (found by painting parts flat green,
   `scene.py --debug-emit`). It is now behind the backer and drawn in the backer's flat black. **The label's**
   wordmark is moved to the label's near half, so the spindle no longer stands in front of it from this camera
   (`--label-near`, `out-outcrop/render/label-near.png`; the prop only).

**Build and cost against C's +$130-150 a unit over v3.**
- The print gains the black flood over the field, one more screen pass. A already has this layer, so C is back at A's
  print: **no change to the +$130-150**.
- Nothing else changes. The backer is the print's own layer, not a part, and the strip, groove and channel stay as
  in v5. The parts list stays at $3,897.
- What C gives up is the see-through field. What it keeps over A: the light is fed from the center, under the platter,
  so the glow has no lit edge or strip anywhere, and the print can be graded radially.

| frame | what |
|---|---|
| `a5-night-ember-2423-c2.png` | C, gate 1, at night: backed field, flattened radial glow, a lit rim |
| `a5-day-ember-2423-c2.png` | C, gate 1, by day: an evenly tinted sheet over an even print |

### For the owner: C or A (2026-11-03, one walkthrough item)

All figures are red of 255, measured in fixed patches on the same set and camera.

1. **The physics.** A lit deck you can see through always sends some light down. The light leaves the bare glass
   almost flat, near the critical angle, onto the base and the floor in front. No coating stops it. In numbers, the
   floor in front read about 16 with C's clear field against about 5 with A; the base's top near the posts read 7-11
   against 0. Backing the field black brings both back to A's: floor 6.3 / 4.8, base 0.
2. **What C2 still gives over A**:
   - **The light source.** C2 is fed from the center, from a strip under the platter, so no lit edge or strip shows
     anywhere. A is fed from the rim.
   - **The grade at night.** C2's glow rises off the platter's foot and falls gently outward: the foot is 92, the
     field 128 and the left rim 75.5. A runs from a lit edge inward (foot 134, field 132, rim 71).
   - **By day they are close.** Both are tinted glass over an opaque print; C2's print is even.
   - **What C2 gives up.** It no longer shows the float through the deck, which was C's reason to exist.
3. **A middle path**, proxied cheaply (900 x 600, 48 samples; not a gate frame): backed and lit out to 235 mm from the
   spindle, clear unprinted glass beyond, so the corners and the arm side are see-through and unlit.
   - **The leak is small.** Floor 6.4 / 5.9 against A's 6.6 / 5.0; base 0. Clear glass with no print and no glow in
     it keeps its guided light by total internal reflection.
   - **But the look is weak.**
     - At night it reads as a lit disc with dark corners and a hard round edge. A soft edge would bring some leak
       back.
     - By day the clear corners read dark, because under them is the black base and its shadow, not a lit float.
     - So it does not give the see-through depth C was for. Not worth a gate frame unless the owner wants the lit
       disc as a look.
4. **Cost per unit, over v3:**

   | option | cost per unit over v3 |
   |---|---|
   | v4 as gated (A, g5) | about +$140-170 |
   | C as gated | about +$130-150 |
   | C2 | about +$130-150 (the black flood is in the print's estimate) |
   | the middle path | the same as C2 (a different screen) |

   Each costs $3,897 in parts.

### Option C3 (2026-11-03, the coordinator's 15:34 fixes; `render_lantern.sh c3`)

The gate held C2 3/3. Its black backer-only disc under the platter showed as a black crescent in front of it, the
grade read flat, and the border read as a black bezel.

**What changed.**
1. **No crescent.** The black disc stopped at r 150, the platter's own radius. Seen through the 24 mm deck at the
   camera's angle, its edge lands about 17 mm in front of the platter. The print and the glow now begin at r 105, so
   the black center sits well inside the platter's footprint. The glow runs right up to the platter (the foot 140,
   against C2's 92) and lights the platter's acrylic rim from below.
2. **A center-out falloff.** The print's cover runs from about 24 % at r 105 to 5 % by 280, backed black throughout,
   with no boundary.
   - Across the field, the 10th to 90th percentile spread is 101-151. That compares with A's 121-138, C2's 117-150
     and the first C's 81-174. The field CV is 18 % (A 13 %, C2 16 %, the first C 26 %).
   - At the left rim the glow is 54.8, against A's 71. The rim is darker, as a center-fed guide is.
3. **The glow lights what sits on it.** The platter's rim, the record's edge and the arm pillars are lit through the
   deck's top. They are lit from under the platter now too.
4. **The border is clear tinted glass.** The 5.6 top is two pieces cut from one sheet: the field, and a 10 wide frame
   over the rings, bonded edge to edge with black-pigmented ACRIFIX. The rings' undersides are left bare and polished.
   - By day the border shows its thickness and its tint, with one black line at the bond.
   - At night it stays dark. A ×8-lifted difference against A shows only a faint line on the lower front edge.
5. **Clean edges.** The edges are polished, and the shader bevel on them, which rippled their highlight, is dropped.
   By day the print is even (15 %) and the room's light on it is baked lower (5, from 7), for a deeper ruby.
   - A real 2.5 mm dot screen was tried for depth. On the full frames it read as a mesh, like perforated metal, so the
     print is drawn as a tone again.
6. **Underneath, as clean as C2.** Red of 255:

   | | C3 | C2 | A |
   |---|---|---|---|
   | base top | 4.7 | 4.5 | 4.7 |
   | base spots near the posts | 0 / 0 | 0 / 0 | 0 / 0 |
   | floor in front | 6.4 / 4.8 | 6.3 / 4.8 | 6.5 / 4.9 |

   - The glint under the deck had come back: the glow, unfiltered in the clear core, left the strip groove's clear
     sides. The backer film now runs across the groove's opening, so the groove and its channel are hidden.
   - Against A, 6.8 % of C3's pixels differ by more than 4 levels, mean 1.35. For C2 that was 5.1 %, mean 2.17.

**Cost.** About +$15-25 a unit over C2, for the extra cut, the black bond line and the polishing. C3 is then about
+$145-175 a unit over v3 (v4 as gated: +$140-170). $3,897 in the parts list: the sheets are the same.

| frame | what |
|---|---|
| `a5-night-ember-2423-c3.png` | C3 at night: the glow up to the platter, falling off outward; the border dark |
| `a5-day-ember-2423-c3.png` | C3 by day: deeper ruby over an even print; the border clear tinted glass |

**C3's night gate (17:07).** The gate showed C3 by day 3/3, and held it at night 3/3 on one fault. A thin red line
ran inside the border along the back-left edge, with a fainter one low on the front face. It was the border frame's
inner cut face, drawn as glossy black lacquer, mirroring the field's glow.

The bond lines are now matte black: the frame to the field, and the rings to the core. That is what an index-matched
black cement looks like from either side. Nothing else changed, and the day frame stands.

On the line's own pixels (back-left crop at 100 %, 884 px), C3 read RGB 37, 26, 36 and C3b reads 21, 25, 35, the
border's black. Everything else matches C3:

| | C3b |
|---|---|
| base top | 2.7 |
| base spots near the posts | 0 / 0 |
| floor in front | 6.1 / 4.8 |
| platter foot | 140 |
| field | 129 |
| field spread (10th to 90th percentile) | 101-151 |

**Cost:** none. The black cement was already in C3's bond-line estimate.

| frame | what |
|---|---|
| `a5-night-ember-2423-c3b.png` | C3 at night, the bond lines matte black: no line inside the border |

**The C3 pair for the owner (C3d, 2026-11-03, the coordinator's 17:57 pass).** Night and day from one build.
The set, the camera, the center feed and the grade are unchanged.

- **The red tick by the arm pillar was the glow sheet itself,** seen in a sliver past the field's edge (found by
  painting parts flat green). The glow now fades over the last 20 mm before the core's edge, inside the black band
  (`--edge-fade 0.02`). An 8 mm fade (C3c) only halved it. At x 1482-1496, y 497-503 the patch reads RGB:

  | C3b | C3c | C3d |
  |---|---|---|
  | 50, 13, 22 | 27, 13, 22 | 19, 13, 22 (the border's black) |

  The left rim is 53.7, against C3b's 54.4.
- **The ellipse in front of the platter was a print edge:** the front-right post's 2 mm seat in the light guide's
  underside. The seats are gone (`mantle_strata_v5.py`). The posts butt-bond flat to the backed underside with MA310,
  on a 0.1 bond line over about 700 mm2, located by a drilled jig plate. Rebuilt with 0 clashes; the posts are 2
  shorter (30 x 40).
- **The day border.** C3c's matte black bond line took away the day border's ruby: C3's glossy black had mirrored the
  room inside the ring. The ring's inner faces are now painted dark grey (10 %) toward the ring and black toward the
  field, so the glow is still held at night (`--ring-white --ring-albedo 0.10`). White read as a lit edge by day.
  - The front face's red pixels average 102 (C3: 75).
  - The right face's salmon band is not brighter: its red pixels average 120 (C3: 141).
- **Glow on what stands on the deck,** checked on a crop, glow on against off, red of 255:

  | | glow on | glow off |
  |---|---|---|
  | the lift post's foot | 22.6 | 7.0 |
  | the arm pillar's base | 13.7 | 8.2 |
  | the arm-board disc's edge | 25.2 | 17.8 |
  | the counterweight | 42.2 | 36.3 |

  Green and blue do not change. No light-path setting hides it: the glow reaches them as direct light through the
  deck's top, tinted by it, and in their reflections. The arm pillar is black anodized, not steel, so it stays cool;
  the disc's top faces away from the field.
- **Not done:** the cool strip reflection along the ring's top edge. It would add a light, and the set stays as it
  is for the comparison with A.
- **Underneath, unchanged:**

  | | C3d |
  |---|---|
  | base top | 2.9 |
  | base spots near the posts | 0 / 0 |
  | floor in front | 6.1 / 4.8 |
  | field spread (10th to 90th percentile) | 89-151 |

**Cost:** the paint on the ring's inner faces and the jig plate, about +$5 a unit. C3 is about +$150-180 a unit over v3;
the parts list stays at $3,897.

| frame | what |
|---|---|
| `a5-night-ember-2423-c3d.png` | the C3 pair at night |
| `a5-day-ember-2423-c3d.png` | the C3 pair by day, the same build |

**The optional day polish (the coordinator, 19:37), tried on crops and not taken.** The pair stands as passed (night
2/3, day 2/3). Each crop was rendered at 64 samples on the same camera and compared with C3d.

- **The ring's inner faces polished black toward the ring** (`--ring-gloss`), or **polished clear with an air gap**
  to the field's matte black edge (`--ring-clear`).
  - By day both read as glassier: the ring less charcoal, the front face more even, and the pinstripe along the
    field's edge gone.
  - At night both add new edge light: a red line along the deck's lower front edge and an arc by the arm board,
    up to 58 levels over C3d.
  - Any reflective face inside the ring carries the glow that reaches the ring. The diffuse dark grey (10 %) is the
    one finish that holds at night, and it is what draws the faint pinstripe by day.
- **No shader bevel on the top faces** (`--no-top-bevel`): it adds no night light, but it does not remove the
  pinstripe, so it is left out.
- **The front face's charcoal-to-brick ramp, and the right face's grey-pink haze, are the optics, not a finish.** The
  ring is clear tinted glass: through its faces you see down to the white studio floor below (bright) and up into the
  dark ring top. The rings' outer edges are already polished (roughness 0.012). The bands are not visible layers; the
  ring is tint throughout.
- **The night "gaming" read**, black chassis and red field, stays as the coordinator's named residual risk. The set
  is unchanged.

**Rulings 1-3 (the coordinator, 20:06), checked against the C3d rig.**
- **The lamps** are area lights and one spot: key, strip, side, fill, bg, top, spot and the night wall-wash. At night
  the room's lamps are scaled to 0.3 % and tinted navy.
  - None has its specular factor below 1; none is light-linked to some parts only; none has transmission off.
  - The wall-wash is hidden from camera rays only. It sits out of frame, lighting the wall.
- **The glow** is an emitting sheet inside the deck, seen by every ray through the resin. Its shadow visibility is off
  so that it doesn't block light; it emits upward only, as the dot print does. The LED strip itself is drawn unlit,
  with its output carried by the sheet; it sits behind the groove film.
- **One mesh had a ray-visibility hide:** the strip's aluminum channel (camera, glossy and transmission off since C3).
  It is not a lamp, and since C3d the groove film hides it physically, so the hide is removed.
  - Re-proxied on the under-deck crop (64 samples): no amber pixels, against none in C3d. The C3d frames stand.
- **The pair re-rendered from this build** (`render_lantern.sh c3e`, the coordinator's 20:17 ask; scene and model as
  c2e255e3) and diffed full frame against C3d:

  | | pixels identical | max difference | pixels over 10 | 15 px box mean, max |
  |---|---|---|---|---|
  | night | 99.99 % | 1 level | 0 | 0.03 |
  | day | 99.91 % | 2 levels | 0 | 0.14 |

  That is noise only, so the C3e files are the pair, with no new gate:

  | frame | what |
  |---|---|
  | `a5-night-ember-2423-c3e.png` | the C3 pair at night, from the build after rulings 1-3 |
  | `a5-day-ember-2423-c3e.png` | the C3 pair by day, the same build |

### The render (how the light is drawn)

The guide's output is drawn as an even Lambertian glow just above the print: 9 W/m2. That figure follows from the
strip's power, not from the picture: 6 W in, about 2.25 W of light, about 80 % into the core and 70 % out, over about
0.136 m2. Cycles cannot sample the real path (a diffuse bounce inside glass, then glass, then the strip) in useful
time. By day the room's light on the print is baked the same way, at the strength the albedos give, within about half a
stop. The scene's face classification had read the meshes' own frame, which is Y-up, as the world's. It is fixed for
v4's deck and left as it was for the frames already made.

### No light (2026-11-10)

The owner: "Forget the lights on mantle." The coordinator: Mantle has no light of any kind. Out of the model, the CAD
and the parts list (`mantle_strata_v3.py`, rebuilt into `out-strata-v3/`): the deck's groove, its channel and strip,
the 24 V adapter, the plate's light switch and 24 V inlet (`strata-rear-hardware-nolight`), and their wiring
(`strata_rear.py`'s rating and diagram). In: the deck's underside bead-blasted satin (the day win from the light
proposals) and the bearing's visible parts black. Budget $3,850 signed to $3,767; with the black nickel
plating of every brass part that shows (one prototype lot, about $75, an estimate; 2026-11-11) $3,842. The underside's
blasting is not priced by the kit (about +$10-15, an estimate). The final day set, eight
tints: `renders/2026-11-10/barkhorn/mantle-r48/mantle-final-day-*.png`.

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
9. *(Moot since 2026-11-10: no light.)* **Dimming the light:** none inside now. If it is wanted, use a listed Class 2 dimmer in the adapter's lead,
   outside the record player.
