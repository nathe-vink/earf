# Tropos's tints: the site's, and stock TruCast sheet's (reconciled 2026-10-31)

There are two calibrations of Tropos's eight tints on two branches. This note compares them.

- **This branch** (`make/stock_tints.py`, the stock flavors `stock-ember`, `stock-ember-trucast`, `stock-smoke`) covers
  three stock codes: 2423 Red, 2064 Gray and 2074 Dark Gray.
- **r48-biomes** (`spinoffs/barkhorn/biomes/tints.json`, commit b970bb3f) covers all eight tints. It uses this
  branch's "held" method: the seller's total transmission (TT) held at the sheet's own thickness.

`tints.py` here copies biomes' codes, TT and channel splits, and writes `tints-trucast.json`. The assets take it with
`make_blend.py --tints trucast`. The committed `.blend` files keep the site's tints, the look of every picture so far.

## Where they agree

- **The method and the source.** Both use the TruCast chart's TT (2423 at 14.1 %, 2064 at 29.3 %) and the same "held"
  case, 8 % surface loss and channel splits.
- **The cabinets.** `tints-trucast.json` reproduces biomes' `cabinet_deep` exactly for all eight. This branch's stock
  flavors hold 2064 at the 3/4 in sheet's 19.05 mm, against 20 mm: about one point of TT. That is not worth a change.
- **The codes for Ember and Smoke's cabinet** (2423, 2064). Those are this branch's stock pair (`make/stock-pair.md`).
- **Strata's laminated horn** in stock 1/2 in (held at 12.7 mm) gives `#E02B3A` for Ember and `#787B7E` for Smoke. That is
  the same as this branch's stock flavors' horn.

## Where they differ

**1. The horn's rule.** These are three different horns, so there are three rules.

| horn | its sheet | its color in the model |
|---|---|---|
| the site's (formed, the deep lot) | a custom cast lot, deeper than the cabinet | the site's `horn_deep` at 10 mm: e.g. Smoke passes 0.7 % through 12.7 mm, Ember 10 % |
| biomes' | the cabinet's code "as deep as the cabinet" (the owner, 2026-10-22): the horn's 10 mm passes what the 20 mm wall passes | e.g. Smoke 21.5 %, Ember 12.3 % through 12.7 mm |
| Strata's (laminated, stock 1/2 in) | the cabinet's code held at 12.7 mm; Smoke in 2074 Dark Gray | e.g. Smoke 11.7 %, Ember 14.1 % |

The site's horns are much deeper than biomes' in five tints: Smoke 0.7 % against 21.5 %, Haze 4 % against 9.5 %, and
Dust, Ice and Poison too. biomes' rule reads "as deep as the cabinet" literally, while the site's model was made with
the deep lot. **This is the owner's to settle**: does the horn match the cabinet or go deeper? Neither branch should change
it alone.

**2. Smoke's horn code.** biomes uses 2064 for the horn. The stock pair's laminated horn is 2074 Dark Gray (11.7 %),
because 1/2 in 2064 would be a pale gray horn.

**3. Three cabinets are much deeper in stock sheet than on the site.** These are the TruCast codes biomes proposed.

| tint | site's cabinet, TT through 20 mm | stock code, TT | |
|---|---|---|---|
| Ember | 49.7 % | 2423 Red, 14.1 % | 3.5x darker: a deep red box, not a pink-red one |
| Poison | 56.0 % | 2092 Green, 18.6 % | 3x darker: bottle green |
| Haze | 49.2 % | 2287 Violet, 13.5 % | 3.6x darker |
| Dust | 53.9 % | 2422 Orange, 59.1 % | close |
| Acid | 64.7 % | 9097 Fluorescent Yellow, 77.6 % | close, and fluorescent (not modeled) |
| Ice | 65.5 % | 2069 Tinted Blue, 57.6 % | close |
| Fog | 87.3 % | 0000 Clear, 93.0 % | close |
| Smoke | 30.3 % | 2064 Gray, 29.3 % | the same |

- So in stock sheet, the site's light Ember, Poison and Haze cabinets need a lighter code, or a custom lot. Or the
  site moves to the deeper stock look. `link_example_strata_trucast.png` shows Strata in stock tints (Ember, Smoke,
  Poison, Ice), beside `link_example_strata.png` in the site's.
- **Strata's horns in stock sheet:** Ember, Poison and Haze stay deep. Dust, Acid and Ice come out pale: 51 to 75 %,
  against the site's 14 to 42 %. A pale stepped horn shows its terraces more and its color less.
- Under the owner's ruling, no starting color is promised: Smoke stays the pricing reference only.

All TT figures are the "held" case, the central estimate until the chips are measured (`make/stock_tints.py`).
