# Stock colours for the first Hemisphere, Core and Mantle (round 43, 2026-10-31)

From the research's R1 (`spinoffs/barkhorn/research/2026-10-31/R1-stock-colours.md` on `r46-owner-notes`, 6840e741).
Every price and stock figure there was read from public pages on 31 October, so check it before ordering. The study
render is `renders/2026-10-31/barkhorn/stock-colours/` (`stock_colours.py`).

## The picks (Ember and Smoke, the first set)

The same code differs 2 to 5× in transmission between makers (R1 §1.1), so **all sheet in one tint comes from one
source.** That source is AC Plastics (TruCast, cell cast), which stocks 3/8" and 1/2" in both colours. Canal (Chemcast)
is the alternate for Smoke, and also sells the 24 × 48 thin sheet.

| Part (design thickness) | Stock | Ember | Smoke |
|---|---|---|---|
| Hemisphere shell (9 from 10 mm sheet) | 3/8" (9.5 mm) | **2423 Red** .375, AC $680.40 / 48×96, 10 in stock | **2064 Gray** .375, AC; Canal 3/8" $375 |
| Hemisphere skin (3) | 1/8" (3.2) | 2423 1/8", 24×48 $56 (Canal) or $39.50 (Delvie's) | 2064 1/8", the same |
| Hemisphere liner (3, opal) | 1/8" white translucent | a stock white cast translucent, **to sample** (not in R1); about 50–70 % transmission | the same |
| Hemisphere rim | cut and turned from 3/8" | 2423 | 2064 |
| Core ball (9 from 10 mm sheet) | 3/8" (9.5 mm) | 2423 .375 (the same sheet as the shells) | 2064 .375 |
| Mantle plinth (25) | **2 × 1/2" laminated (25.4)** | 2423 .500, AC $835.80, 19 in stock | 2064 .500, Canal $495 |
| Mantle base (10, edge-lit) | 3/8" (9.5) | 2423 .375 | 2064 .375 |
| Mantle lid (6) | 1/4" (0.220", 5.6) | 2423 .220, about $240 / 48×96 | 2064 .220, about $231 (AC) |
| Mantle platter (25, turned) | 2 × 1/2" laminated, turned true | 2423 .500 | 2064 .500 |
| Mantle posts (40 OD) | turned from stock rod: Spartech stocks 2064 and 2423 rod, 0.5"–3" | 1.75" rod | 1.75" rod |
| Mantle pod rings (20 and 12) | 2 × 3/8" laminated (19), and 1/2" | 2423 | 2064 3/4" (19, AC, 3 left) or 2 × 3/8" |

**Sheet for one set of each product, per tint (estimate):**

| Tint | What | Cost |
|---|---|---|
| Ember | one 3/8" 48×96, one 1/2" 48×96, a 24×48 of 1/8", a 1/4" sheet | about $1,800 |
| Smoke (from Canal) | the same | about $1,200 |
| Samples first | all the chip packs ($63, R1 §5), plus a 1/2" off-cut of each colour | under $150 |

Most of each sheet is left over for the next units: a 48×96 at 3/8" gives about 30 shell or ball blanks. Add LTL
freight for full sheets.

## Mantle's plinth: laminate it

- **19 mm** (stock 2064 at 3/4"): this changes a design dimension, so no.
- **A mill run** (Chemcast, 10 sheets per colour at 24–32 mm, about a pallet): right for production, wrong for the first
  one.
- **Laminate two 1/2" sheets** with a polymerising cement (Acrifix 2R 0190 or Weld-On 40) under a press or vacuum,
  then anneal and machine. That gives 25.4 mm, close to the drawn 25.

**The risk** is the bond line, a fine line halfway up every polished edge, and any bubble in it. Two answers:
- **Make it a decision:** cut a 1 mm V at the bond line round the plinth's edge, so the line reads as drawn. This
  changes the geometry, so it is a **proposal for the owner**.
- **Or hide it:** bond with the sheets' cast faces together, flood the joint, and polish. It shows as a faint line at
  most, which a prototype can carry.

**If the harsh case holds** (stock 2423 one dye loading, so 25 mm nearly black; see below), keep the depth by design:
- laminate **clear 1/2" + tinted 1/8" + clear 3/8"**, a thin tinted layer inside clear;
- then the depth of colour is set by the tinted layer, not by the plinth's thickness.

That is a good production idea too.

## Does a stock-colour prototype still look like EARF?

The study renders show Core and Mantle in Ember and in Smoke, three ways:
- the site's tint;
- the stock colour, **kind case**: each stock sheet transmits like its 1/8" chip;
- the stock colour, **harsh case**: one dye loading, so thick parts deepen by Beer–Lambert from the chip.

The stock colours are the photo hues in R1 Appendix A, scaled to TruCast's published transmission (2423 14.1 %,
2064 29.3 %).

**What the renders say** (`stock-colours-sheet.png`: Core above, Mantle below; Ember, then Smoke):

| | Kind case (each sheet like its chip) | Harsh case (one dye loading) |
|---|---|---|
| **Core in Ember** (2423) | **Still EARF**, but crimson where the site's Ember is red-orange: 2423's hue is about 17° against Ember's 59°. A 2422 Amber layer over it would pull it back (R1, untested). | A dark maroon ball, its glow dim: **not EARF.** |
| **Core in Smoke** (2064) | **Too pale:** 3/8" of 2064 reads near clear and slightly peach. Use **2074 Dark Gray** for Core if the chips show this case. | **Close to the site's Smoke**, a mid grey with a warm cast. |
| **Mantle in Ember** (2423) | **Still EARF, and richer:** the plinth and lid a deeper, more saturated red than the site's pinkish Ember. | Deeper still, but **still clear red, not black**, because the site's Mantle tint is already deep at 25 mm. |
| **Mantle in Smoke** (2064) | Reads like the site's Smoke. | Reads like the site's Smoke. |

**The answer to the owner: yes, a stock-colour prototype still looks like EARF.**
- **Mantle** in either tint is safe on stock sheet.
- **Core in Ember** is safe if the chips show the kind case, and reads crimson.
- **Core in Smoke** takes 2064 or 2074 depending on the chips.
- **The one combination that fails is Core in 2423 under the harsh case.** If a 1/2" off-cut of 2423 is much deeper than its 1/8" chip, cut Core's ball from 1/4" 2423 (or 2423 1/8" over clear) instead of 3/8".

The $1 chips and a 1/2" off-cut of each colour decide it before any sheet is bought. Order those first.
