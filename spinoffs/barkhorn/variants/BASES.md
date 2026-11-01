# Strata's base: A, a stepped plinth, and B, outrigger feet (2026-11-01, proposals for the owner)

**Why:** IEC 62368-1 8.6.2.2 pushes at the horn's top with 20 % of the weight. The speaker passes only if its center
of mass sits at least 0.2 x that height inside every tipping edge (`stability/README.md`). On today's feet, Strata
fails by 24 % forward, 34 % back and 12 % sideways. The fix is geometric: the feet's centers at about 600 x 600 mm.
Both proposals put four M8 levelling feet at the same points: **x -25 / 585 and y -94 / 526** in the Cabinet's frame
(the cabinet is 560 x 420, its front at y 0), that is, about 300 mm from the center of mass each way.

The CAD is `variants/variants.py`: `PLINTH` and `OUTRIG`, the options "Plinth" and "Outriggers". The shots are
`campaign/shots.py`: `base-plinth`, `base-outriggers` and `base-today`, each with a `-34` three-quarter view.

## A. The stepped plinth

**The design:** three frames of the cabinet's own 1/2 in stock sheet, stepping out under it like the caldera and the
horn's terraces:
- 600 x 460 under the cabinet;
- then 630 x 566;
- then 660 x 670 on the floor;
- each a frame about 80 to 155 mm wide round a 440 x 300 opening;
- the outside edges polished, the three bonded;
- the cabinet bolted down through its own feet's M8 inserts.
It lifts the cabinet 38.5 mm.

| | |
|---|---|
| footprint (the feet's centers) | 610 x 620 mm; the base itself 660 x 670 |
| weight | about 10.3 kg of acrylic (8.6 L), so the speaker is about 85.5 kg (est.) |
| cost, a speaker | about $260 of sheet ($0.03/cm3) + about $250 of cutting, polishing and bonding + $18 of feet: **about $530** (est.) |
| the push | 168 N (20 % of 85.5 kg) at 1.344 m: the arm needed is 269 mm |
| margins (the feet's centers) | **forward +17 %, back +13 %, sideways +13 %** (est.) |

## B. Outrigger feet

**The design:** four arms of bronze bar, 30 x 20, the same bronze as Strata's posts:
- each from under one of the cabinet's corners (two M8 into inserts in the bottom: its foot's own and a second) out
  on the diagonal to a foot;
- the ends rounded, the bar's faces satin.
It lifts the cabinet 20 mm.

| | |
|---|---|
| footprint (the feet's centers) | 610 x 620 mm; the arms reach about 75 mm past the sides and 95 to 105 past the front and back |
| weight | four arms about 1.24 kg each, 4.95 kg, so the speaker is about 80.2 kg (est.) |
| cost, a speaker | about $70 of bronze ($0.12/cm3) + about $200 of machining and finishing + $18 of feet: **about $290** (est.) |
| the push | 157 N at 1.325 m: the arm needed is 265 mm |
| margins | **forward +19 %, back +15 %, sideways +15 %** (est.) |
| each arm | at the tipping point a foot carries up to about half the weight, 390 N. 110 mm outside the cabinet, that is 43 N m on a 30 x 20 section: about 22 MPa, against bronze's 125+ MPa yield |

## Both

- **They pass with margin, each way.** Anchoring stays a lab question for the January pre-check, not a design option.
- **They are drawn on Strata;** the smooth horn sits on either.
- **They change the look.** The owner chooses, after a blind duel judged on looks alone (the critic sees no
  stability numbers).
