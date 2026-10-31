# Tropos: the first pair in stock sheet (2026-10-31)

The question: can the prototype pair be built from stock tinted cast sheet, with no custom pour, and still look like
EARF? The source is research R1 (`spinoffs/barkhorn/research/2026-10-31/R1-stock-colours.md` on r46-owner-notes). The
colours come from `make/stock_tints.py` (estimates, see below). The picture is
`renders/2026-10-31/barkhorn/horn-choice/lineup-stock.png`: the site's Ember and Smoke beside the stock ones.

## The decision

| part | Smoke | Ember |
|---|---|---|
| **cabinet** (20 mm in the CAD) | **TruCast 2064 Gray, 3/4 in (19 mm)**: AC Plastics, $1,003.20 a sheet, **3 in stock**. A pair needs about 5.2 m² of 20 mm, so two sheets, nested; buy all three. | **Not from stock.** 2423 is stocked only to 1/2 in, and stock 1/2 in 2423 is far too deep for the cabinet (below). Chemcast 2423 at 20 mm is a standard-colour mill run: no colour fee, a minimum of about 8 to 10 sheets of 48 x 96, enough for 4 or 5 pairs. |
| **horn** | **Laminated, TruCast 2074 Dark Gray 1/2 in** (`laminated-horn.md`), a lighter smoke than the site's | **Laminated, TruCast 2423 Red 1/2 in** (19 in stock): within a few percent of the site's deep horn |
| look against the site | cabinet within 3 % of the site's Smoke at 20 mm; horn lighter | cabinet (Chemcast run) and horn both within a few percent of the site's |
| for 19 January | **yes** (`schedule.md`) | the horn yes; the cabinet only if the mill run ships by mid-December (to confirm with Plastiglas or a distributor) |

**Recommendation: the first pair in Smoke.** It is the only colour whose cabinet is a stock sheet at full thickness
today, and it matches the site's Smoke cabinet. Build an Ember horn in stock 2423 alongside it, to show the Ember horn at
the debut. Order the Chemcast 2423 run at 20 mm for an Ember pair by Milan.

**Two orders before any sheet:**
- the chips;
- a 1/2 in off-cut of 2064 and of 2423 (R1 §5, about $40).

R1 shows that the same code differs 2 to 5 times between makers. It also shows that a maker may hold LT across
thicknesses, or not. Only the vendor's own sheet settles either.

## Smoke at 19 mm: what changes in the CAD

Nothing that shows outside. The CAD's 20 mm is a nominal anyway: cast sheet's thickness tolerance is about ±10 %, so a
"20 mm" sheet can arrive anywhere from 18 to 22. If built at 19:

- **Outside dimensions:** unchanged (SPEC). Each panel's inner face moves 1 mm out.
- **Volume:** the inside grows by about 1 %, 2 mm in each direction. The port's tuning moves by under 1 %, about 0.3 Hz.
  The port lengths are found with the box assembled anyway (`assembly.md`).
- **Joints:** butt joints in polymerising cement. A 19 mm edge on a 19 mm face is the same joint. The rebates for the
  back's land and the baffle's ring are cut to the measured sheet, as they must be for any cast sheet.
- **Inserts and screws:** the 12 mm inserts and the back's 22 screws fit in 19.
- **The back's cord seal groove:** 3.0 deep in 19 is fine.
- **The cutlist:** generate it for the measured thickness (`T` in `cloud.py`). That changes the inner parts' sizes by
  1 to 2 mm.

`T` is SPEC in the spec. A build at 19 means a measured sheet, not a design change. Confirm with the owner that the
pair may be built at the sheet's measured thickness.

## Why not an Ember cabinet in stock 1/2 in

The thinner walls or two laminated 1/2 in layers were considered:
- Stock 2423 at 1/2 in, through 20 mm, is about #C40206 (12 %). That is as deep as the horn, a dark ruby box.
- The site's Ember cabinet through 20 mm is #F5B2AC (54 %), a pale rose.
- A cabinet of 12.7 mm walls is a SPEC change (the owner's), and it would still read about 4 times deeper.
- Bonding two 1/2 in layers face to face over 1.3 m² panels invites bubbles in every panel.

The `stock-ember-trucast` flavour renders that dark ruby box, if the owner wants to see it.

## The horn: is a stock-tint horn even possible?

- **Formed:** stock tints exist at 3/8 in (9.5 mm): 2423 (10 in stock at AC Plastics), 2064 and 2074. The formed horn
  is drawn in 10 mm, and 9.5 mm stays above the 4 mm floor in the corners (about 4.6 estimated, against 4.9 at 10). The
  quarter trial tells. So a formed horn in stock tint is possible. Its colour is the 3/8 in sheet's, through 5 to 8.5 mm
  walls: about half as deep as the laminated horn's 10 to 30 mm. **The render shows this matters for Smoke.** A formed
  horn in stock 2074 is nearly clear, and the black throat, pod and driver show through as a hard shape
  (`renders/2026-10-31/barkhorn/horn-choice/choice-formed-smoke.png`). A formed Smoke horn needs the custom deep lot. A
  formed Ember horn in stock 2423 reads as a pale glassy red.
- **Laminated:** stock 1/2 in through 10 to 30 mm reads as deep as the site's horn lot for Ember (`laminated-horn.md`).
- **Do not form the first horn in clear and tint later.** The trial's first shot is clear on purpose (`forming-trial.md`),
  but the shown horn should carry its colour. Keep the custom deep lot for the matched production casts.

## The estimates, and what replaces them

- `make/stock_tints.py` turns each code's published LT at 3 mm into a colour per millimetre. It assumes a hue split per
  colour, and 8 % surface loss.
- Its "held" case is used for every render.
- The flavours are in `stock_colours.json` (`stock-smoke`, `stock-ember`, `stock-ember-trucast`), refreshed into the
  engine by `flavours.py`.
- When the chips and off-cuts arrive:
  - photograph each on the light box against a 20 mm coupon of the site's colour;
  - put the measured hex and thickness into `stock_colours.json`;
  - re-render the line-up.
