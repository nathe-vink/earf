# The Tint Library: a proposal (round 43, 2026-10-31)

**A proposal.** The owner signs any new product, and nothing is ordered or sent. It comes from idea (f) in `r47-brand`
`brandbook/IDEAS.md`: EARF's eight tints in a case, for:
- **designers and architects** who specify EARF colours: "Designers specify what they can hold" (IDEAS);
- **the press mailer**: a box that shows what a render can't;
- **a first product that needs no certification**: no electricity, no battery, no FCC.

Making it also forces the decision manufacturing needs anyway: the eight cast colours, matched and fixed with the
suppliers.

**Files:**
- `tint_library.py` (CAD, fab kit);
- `out-tint-library/` (STEP, STL, DXF cut files, 14 drawing sheets, the parts list, the render model). Its checks pass
  with 0 clashes.

## What it is

| Part | What |
|---|---|
| **Eight chips** | 80 × 50, cut from 3/8" (9.5) cast sheet, corners R4, edges polished. **Stepped:** the left 45 at the full 9.5 (Hemisphere's shell, Core's ball, Mantle's base), the right 35 milled from the back down to **3.2** (Hemisphere's skin), the pocket's floor polished clear. So each chip shows its tint at both depths EARF uses. |
| **The engraving** | On the thick part's front, laser-engraved and filled white (Smoke's and Fog's filled black), in IBM Plex Mono: the tint's name (EMBER), the sheet code (TruCast 2423), and **its light transmission at 9.5 and at 3.2, measured on the lot** (`LT 14 % · 9.5   41 % · 3.2`, the figures from the lot). |
| **The tray** | solid birch, 100 × 144 × 28, eight slots routed at 15 pitch. The chips stand on edge in the spectrum's order: Ember, Dust, Acid, Poison, Ice, Haze, Fog, Smoke. Oiled, with felt pads under it. |
| **The hood** | five panels of 3 mm Smoke cast acrylic, bonded, 106 × 150 × 64. It slips over the tray and stands on the table. THE TINT LIBRARY is engraved on its top. |
| **The card** | 140 × 95, 600 gsm: each tint's code, its LT at both depths, and where EARF uses it. |
| **The mailer** | a rigid box with a foam insert. |

**For now, stock stand-ins** (R1 on `r46-owner-notes`, and `stock-colours.md`):

| Tint | Stand-in |
|---|---|
| Ember | TruCast 2423 |
| Dust | 2422 Amber |
| Acid | 2208 Yellow |
| Poison | TruCast 9093 |
| Ice | 2069 Light Blue |
| Haze | 1020 Purple (confirm it is cast) |
| Fog | 3030 Glass Green |
| Smoke | TruCast 2064 |

The custom tints replace them later. The files stay the same; only the card and the engraving change. A Library
labelled with stock codes is honest about it.

**Why LT is measured, not copied.** The same code transmits 2 to 5 times differently between makers (R1 §1.1), and a
designer will hold the chip to a window. So each lot is measured, with a lux meter through each step against an open
reading, and the chip and the card carry that lot's figures.

## Cost (estimates [E]; quotes replace them)

The fab kit's one-off budget is **$125** a set (`out-tint-library/bom.md`; a one-off shop's rates, the tray milled
singly). In a batch:

| A set | 100 sets | 500 sets | Basis |
|---|---|---|---|
| Sheet, eight chips | $15 | $11 | 100: one 24×48 of 3/8" a tint (about $170–200), ~154 chips; 500: one 48×96 a tint (about $680), ~600 chips |
| Laser: cut, engrave, fill (8) | $20 | $14 | $2.50 → $1.80 a chip |
| The step, milled and polished (8) | $32 | $22 | $4.00 → $2.75 a chip, a fixture of eight |
| Tray, birch, CNC | $20 | $12 | a fixture of 4 on a router; one-off is $53 |
| Hood, 3 mm Smoke, cut, bonded, polished | $15 | $10 | |
| Card, felt, mailer | $6 | $4 | |
| Assembly, QC, the LT measurement | $3 | $2.50 | a lux meter, two readings a chip |
| Setup (fixtures, programs), spread | $6 | $1.20 | about $600 once |
| **A set** | **about $117** [E] | **about $77** [E] | |
| **The run** | **about $11,700** | **about $38,500** | |

IDEAS estimated $100 to $250 a kit at 100. This lands at the low end because the chips are 80 × 50 × 9.5, not 100 ×
100 × 20 tiles: a fifth of the acrylic, at the depths EARF actually uses.

**Price:** [LIBRARY PRICE]. It's for the owner to set: free to specifiers who ask (a sample cost), and sold on the
site. For scale, design-material sample kits of this kind commonly sell for $150 to $300 [E, not researched].

## Quote-request text

Two shops: an acrylic fabricator (the chips and the hood) and a CNC wood shop (the tray). Some acrylic shops do both.

**Acrylic fabricator, short (for a web form):**

```
Quote please: 100 and 500 sets of 8 acrylic sample chips + a small acrylic hood. Chips: 80 x 50 x 3/8" cell-cast
(TruCast 2423, 2422, 2208, 9093, 2069, 1020, 3030, 2064; one colour per chip), corners R4, edges polished; one end
pocketed from the back to 3.2 mm thick over 35 x 50, the floor polished clear; 3 short lines laser-engraved on the
front, paint-filled. Hood: 5 panels 3 mm smoke cast, bonded box 106 x 150 x 64, edges polished, top engraved.
DXF/STEP ready. Price per set, setup, lead time? [Your name], [contact line]
```

**Acrylic fabricator, full (for email):**

```
Subject: Quote: acrylic sample chips (stepped, engraved) and a bonded hood, 100 and 500 sets

Hello,

We're EARF, a small Bay Area product company. We'd like a quote for a sample kit of our acrylic colours, at 100 and
at 500 sets. Each set:

1. Eight chips, one in each of eight cell-cast colours: TruCast 2423 Red, 2422 Amber, 2208 Yellow, 9093 fluorescent
   green, 2069 Light Blue, 1020 Purple, 3030 Glass Green, 2064 Gray (or your nearest equivalents; please name them).
   - 80 x 50 mm from 3/8" sheet, corners R4, all edges polished.
   - A step: over the right 35 mm, a flat-bottomed pocket milled from the back face down to 3.2 mm thick, its floor
     polished clear (it's looked through).
   - Three short lines laser-engraved on the front (name, code, and two light-transmission figures we'll give you per
     lot), paint-filled white (black on the grey and the clear).
2. A hood: five panels of 3 mm smoke-grey cast acrylic, bonded into an open-bottomed box 106 x 150 x 64 mm, the
   joints clear, edges polished, "THE TINT LIBRARY" engraved on the top and filled white.

Files: STEP and DXF (the cuts, the pocket, the engraving layers) and drawings.

Could you tell us:
1. The price per set at 100 and 500, and any setup or fixture charge.
2. Whether you'd buy the sheet (one lot per colour) or we should.
3. How you'd polish the pocket's floor clear (fly-cut, then buff or vapour?).
4. The lead time, and whether you could make one sample set first.

Thank you,
[Your name]
EARF
[contact line]
```

**CNC wood shop, short:**

```
Quote please: 100 and 500 small trays, solid birch 100 x 144 x 28 mm, eight slots 80.6 x 10.1 x 18 deep at 15 mm
pitch routed from the top, edges eased R1, oiled. STEP/DXF ready. Price per tray, setup, lead time? [Your name],
[contact line]
```

## Before it goes further

- **The owner signs:** the product, the chip's 80 × 50 and its two depths, birch and Smoke, and the price.
- **The chips come from the same lots as the first articles' sheet** (`first-articles.md`, 23 November). A Library
  costs nothing extra in sheet if it's cut from the off-cuts of the first builds' 3/8" sheets: about 30 chips a tint
  from a sheet's waste. That's enough for **the first 10 to 20 Libraries** for the press, at the cost of the labour
  alone, about $60–80 a set [E].
