# Tropos's horn, laminated from stock sheet (2026-10-31)

The coordinator pointed out that the laminated horn may be more than a Plan B. Its terraced outside reads as strata, and
every EARF product is named for a layer of the Earth. The stock-colour research (R1) adds a practical reason: tinted
stock cast sheet mostly stops at 1/2 in, so no stock deep lot exists at 10 or 20 mm. Laminating 1/2 in sheet turns
that around. The horn needs no custom pour and no tooling, so a prototype horn can start the day the sheet arrives.

This note covers:
- the horn from 22 layers of stock 1/2 in sheet, stepped and smooth;
- its colour;
- its air path, edges, bond lines and mass;
- its cost and schedule beside the formed horn.

The owner chooses between formed, laminated stepped and laminated smooth from the renders in
`renders/2026-10-31/barkhorn/horn-choice/`.

## The model

`horn-plan-b` and `horn-plan-b-smooth` are in `horn_options.py`. Their drawings and parts list are in
`out-horn-options/`, and the geometry comes from `product.formed_horn`'s `laminated`.

- **22 layers** of 1/2 in sheet, plus the boss.
  - The horn is 278 mm deep, so the pitch is 12.64 mm, each layer and its bond line.
  - Each layer is faced to that pitch from nominal 12.7 sheet. Cast sheet runs about ±10 % on thickness, so the facing
    is needed anyway.
- **Stepped:** each layer's outline sits 10 mm outside the air path at its front face. Each layer is a terrace, 22
  contour lines from the throat to the mouth.
- **Smooth:** the same stack, its outside machined on 5 axes to follow the flare 10 mm outside the air path, then
  polished. The bond lines stay as 22 fine rings round it.
- Both take the formed flare's and the throat piece's place, on the same pod, cap, pads and posts.

| | formed (round 36) | laminated, stepped | laminated, smooth |
|---|---|---|---|
| horn's acrylic | 3.2 kg (flare and throat) | 4.8 kg (4.05 L) | 3.1 kg (2.57 L) |
| **the whole horn** (with the pod, the cap and the pads) | **4.1 kg** | **5.7 kg** | **3.9 kg** |
| walls | 4.9 (corners) to 8.5 mm | 10 mm at each layer's front, to about 30 at its back | 10 mm throughout |

## Colour: do the thick walls read deep enough?

`make/stock_tints.py` estimates each stock sheet's colour from its published light transmission (R1). The same code
varies 2 to 5 times between makers. The central case, "held", takes the seller's own LT at the sheet's own thickness.
That is what a maker does that dilutes the dye in thick sheet so the code keeps its look. The chips decide.

| | through 10 mm | through 20 mm | the site's horn lot, through 10 / 20 mm |
|---|---|---|---|
| **Ember: TruCast 2423 Red, 1/2 in** (AC Plastics, 19 in stock) | #E02B3A, 18 % | #C40206, 12 % | #C8262B / #9C0102 |
| **Smoke: TruCast 2074 Dark Gray, 1/2 in** | #787B7E, 20 % | #35383B, 4 % | #2A292C / #020202 |

- **Ember: yes.** Stock 2423 at 1/2 in, through the laminated horn's 10 to 30 mm walls, comes within a few percent of
  the site's deep horn. No heavier dye lot is needed.
- **Smoke: not quite.** 2074 is a mid smoke through the walls, about ten times lighter than the site's near-black horn
  at 20 mm. Two ways to deepen it:
  - alternate 2074 with 2370 Dark Bronze (11.85 %, warmer);
  - accept a lighter smoke horn for the first pair.

  The render shows the plain 2074.
- **If the vendor holds the dye per mm** (R1's "deep" case), 1/2 in 2423 is about three times deeper and 2074 is near
  black. The horn would then read deeper than the site, which suits Smoke and still reads as red for Ember.

**The renders** (`renders/2026-10-31/barkhorn/horn-choice/`, NOTES.md) bear this out:
- The stepped horn is the deepest stock colour in both Ember and Smoke. In Smoke its terrace edges read as bright silver
  lines.
- The smooth horn is paler than the stepped one.
- The formed horn in stock sheet is pale, and in 2074 nearly clear.

## The air path

- The air path is machined through the bonded stack on 5 axes, from the same CAD surface as the formed horn's plug,
  then polished. Its shape is the simulated one, and its accuracy is a machined part's (±0.1), better than forming's.
- The bond lines cross the air path flush. Polymerising cement cures to an acrylic of about the sheet's own hardness, so
  it is cut and polished with the sheet. A step at a joint would be under 0.05 mm. The shortest wavelength the horn
  carries is about 17 mm at 20 kHz, so anything under about 0.8 mm is acoustically invisible. **The layer lines do not
  affect the sound.**
- The walls are 10 to 30 mm of solid acrylic, against 5 to 8.5 for the formed shell. The laminated horn is the most
  inert of all the routes: no shell ringing and no need for damping.

## What each layer's edge looks like

The edges are finished before bonding, one layer at a time, while each is a flat part on the bench.

| finish | how | look | cost a horn |
|---|---|---|---|
| **Polished** (recommended; rendered) | diamond-edge or buff, no flame near a future joint | each terrace a bright line where light catches it; the strata read as glass contour lines, deep red between | about $330 (22 layers, about 15 minutes each) |
| Frosted | bead-blasted or 120-grit edge | soft matt contour lines; hides the bond lines; reads more like stone strata | about $150 |
| Alternating | odd layers polished, even frosted | banded strata, the most geological | about $250 |

- The air path is always polished.
- On the smooth horn the outside is polished all over, and the bond lines show as fine rings.

## The bond lines: 22 faces

Each joint is polymerising cement (ACRIFIX 2R 0190 or Weld-On 40), the cabinet's own.

**The risk.**
- A bubble or a dry patch in any joint shows through the tint. On the stepped horn a void would read as an extra ring.
  Small voids near the outside can pass as part of the strata.
- Within 5 mm of the air path a void is not acceptable. The 5-axis cut would open it into a pit on the air face.
- Twenty-two joints multiply the cabinet's risk C2 (`horn-risks.md`) by 22.

**The mitigation.**
- Cement mixed under vacuum, laid as a bead along each ring's middle, and pressed outward to both edges with a flat
  weighted platen. That pushes air out, not in.
- Bond three sub-stacks of 7 or 8 layers, inspect each joint through its polished edge with a bright light, then join
  the sub-stacks.
- A bad joint scraps at most one sub-stack. A layer is about $20 to $40 of sheet and an hour of work until it is
  bonded, so reject freely.
- Anneal after bonding (80 °C, slow cool), before machining, and again after polishing.
- Machine with an air blast, not coolant, near fresh joints (crazing, A1).

**Three more risks from research R7** (bonding and annealing guidance from Röhm's *Joining PLEXIGLAS*, 311-3):
- **The anneal's length.** Röhm's rule for cast sheet at 80 °C is the thickness in mm ÷ 3 hours of soak, ÷ 4 of cooling,
  with ramps of 10 °C an hour or less. If a shop treats the 292 mm stack as solid, one cycle takes about **7 days**. By
  the thickest wall (about 30 mm, 60 at the boss) it takes about 2. There are two or three cycles: after bonding, after
  machining, and perhaps before bonding if the cut layers show stress.
  - Mitigation: anneal the three sub-stacks apart (each about 95 mm, about 2 to 3 days).
  - Ask the shop which rule it uses. A week per cycle would eat the December float (`schedule.md`).
- **The bond lines' height.** A spacer-controlled bond line is 0.5 to 1.5 mm. Over 21 joints that adds about 10 to 30 mm
  to the stack. The CAD allows 0.2 mm a joint.
  - Mitigation: design to the bond line the shop can hold. Face each layer to the pitch less the bond line: 12.64 − 0.5
    = 12.14 from 1/2 in sheet, which leaves about 0.5 mm on nominal 12.7 sheet. Where 1/2 in comes thin (Canal's is
    0.472 in, 12.0 mm), take a thicker bond line or face the stack's mouth and boss after bonding.
  - The air path is machined after bonding anyway, so its shape does not depend on the stack height. Only the mouth's
    position on the posts does, and the pads take ±2 mm.
- **Colour bleed.** Röhm warns that adhesives can draw the colourant out of tinted sheet at a joint, and that highly
  pigmented sheet can bond weaker.
  - Mitigation: bond two off-cuts of each stock colour (2423, 2074) with the chosen cement first. Check the line for a
    halo, then break-test it. Add this to the 5-layer test stack.

**Likelihood:** medium on the first horn, low after it. These are the same process and inspection as the cabinet's
joints, done by the same shop.

## Mass and stability

The stepped horn weighs 5.7 kg against 4.1 for the formed horn, so the speaker gains 1.6 kg at its top.

The tipping check (README, S7) already assumed 10 kg of horn on top. With the front and back feet 25 mm from the edges,
IEC 62368-1's push at the top (about 118 N m) meets about 124 N m forward and 138 N m back. The laminated stepped horn,
at 5.7 kg, is well inside that assumption, so the margin holds.

The four 20 mm stainless posts carry the extra 1.6 kg easily: about 14 N on each post. The pads' 12 mm inserts are
unchanged.

The smooth horn, at 3.9 kg, is lighter than the formed one.

## Cost and schedule, beside the formed horn

| | formed | laminated, stepped | laminated, smooth |
|---|---|---|---|
| **one-off tooling** | about $7,100 (board plug and base) + about $2,500 (trim fixture) + about $3,450 (the quarter trial first) | about $500 (a bonding jig and platen) | about $500 |
| **a horn, prototype** (the kit, `out-horn-options/bom.md`) | about $1,500 | **about $1,570** | **about $1,790** |
| a horn, bottom-up (sheet, cutting and facing, edges, bonding, anneal, 5-axis air path, polish) | — | about $2,000 to $2,600 | about $2,500 to $3,200 |
| **the prototype pair's horns, with tooling** | **about $13,000 to $16,000** | **about $3,600 to $5,700** | **about $4,100 to $6,900** |
| first horn (`schedule.md`) | about 22 January, if the trial passes | **about 18 December** | about 22 December |
| sheet | 3/8 in stock (2423 or 2064, about $680 a sheet) for the trial; a deep lot later | **1/2 in stock, about one sheet a pair** (the rings nest inside one another: 0.33 m² of material a horn) | as stepped |
| a horn at 100 pairs (estimate) | about $400 to $600 on the aluminium plug ($14,500) | about $900 to $1,400 (CNC and bonding stay labour) | about $1,100 to $1,600 |

**Plainly:**
- **For the prototype pair, the laminated horn is cheaper, about a third of the formed horn's cost with its tooling.
  It is faster, by about five weeks to the first horn. It is as good acoustically: the same air path and more inert
  walls.** The stepped one is heavier, 5.7 kg, within the stability margin. The smooth one is lighter than the formed.
- **At volume, forming is cheaper** once its plug is paid for: about $500 a horn against about $1,100. The break-even
  is roughly 15 to 30 pairs. If the owner prefers the strata, the cost at 100 pairs is about $60,000 to $160,000 more
  across the run (estimate), or about $600 to $800 a pair on a $20,000 pair.
- **The look is a choice the owner makes.** The formed horn is one seamless shell, glossy, pale at its thin corners
  and deep at the rim. The stepped horn is strata, every layer of the Earth in one object. The smooth horn is a deep
  solid lens with fine rings.

## Next

1. Order the 1/2 in 2423 off-cut (or a 12 x 12 in square) with the chips (R1 §5). Settle its depth against the site's
   horn.
2. Bond a 5-layer test stack from off-cuts. Section it to check for voids, and polish an edge of each finish
   (polished, frosted, alternating). Cost: about $150 and two days.
3. The owner chooses the route and the edge finish from the renders and the test stack.
