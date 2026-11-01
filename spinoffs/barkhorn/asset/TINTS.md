# Tropos's tints: stock TruCast sheet's, the line's default since 2026-11-01

**Colors F, the owner's pick (2026-11-01, about 22:45: "Go", taken as the coordinator's picks; owner note
68adc2c39e6058397dfa98d2818a1254ac6d2b71 on r46-owner-notes).** After "they might be too dark now" (about 15:10), the
comparison rows (`renders/2026-11-01/barkhorn/deck/tropos-eight-row-*.png`, A to G) showed it was the lining more than
the tint: through the clear walls you saw the black lining, the woofer and the internals.
- **The lining:** white voile sleeves (the batting preset's own white, as the site had) in Ember, Dust, Acid, Poison,
  Ice, Haze and Fog. **Smoke keeps its black lining.**
- **Poison's cabinet at 32.3 % and Haze's at 25.8 % through 20 mm**, each in its stock code's channel split (2092's
  green, 2287's violet), only lighter. Both are **custom batches at production** (Haze needed one anyway: 2287 is
  translucent, and the model keeps Haze transparent).
- **Every other cabinet stays stock** (Ember 2423, Dust 2422, Acid 9097, Ice 2069, Fog clear, Smoke 2074), and **every
  horn is unchanged** (Dust, Acid and Ice deep in their cabinet's hue; the other five their stock code).
- In `product.py` (`LINING_WHITE`, `COLORS_F_DEPTH`) after the stock tints, so every engine render and asset carries it.
- **The lamps and Mantle keep their parts as they are**, unless their lanes report a mismatch with these colors.

The rest of this file is the stock-tint record it builds on.

**The owner, 2026-11-01:** "I like the darker colors" (r46-owner-notes 8832050e).
- The eight colors are now stock cast sheet's own tints: each cabinet in its TruCast code with its TT held at 20 mm, and
  each horn, stepped or formed, in the same code at 12.7 mm.
- They are applied to the line's eight flavors in `product.py` (from `tints-trucast.json`), so every engine render and
  both `.blend` assets carry them.
- Smoke's cabinet is now 2074 Dark Gray (11.7 %), as it has been since the backlight pass.

**The horns: "Deep, like the site"** (the owner, 2026-10-31). Every horn must read at least as deep as the site's
horn.
- **Dust, Acid and Ice's horns are a heavier batch, not stock sheet** (the coordinator, 2026-11-01). Stock 2422, 9097
  and 2069 at 12.7 mm pass 59, 78 and 58 %, against the site's horns at 19, 42 and 14 %. Their horns take the site
  horn's depth (`SITE_DEEP_HORN` in `product.py`).
- **In the cabinet's own hue, only deeper** (the coordinator's call, 2026-11-01). The owner's ruling is about depth, not
  hue. With the site's horn color, Ice's horn read cobalt over a teal-navy cabinet: two materials in one speaker (the
  site-set critics, round 3). Each deep horn now keeps its stock code's channel split, with the absorbance scaled so its
  luminance after 10 mm matches the site horn's. Dust #E0661C becomes #F25508, Acid #F2B705 becomes #FFB101, Ice
  #3C86C2 becomes #2981E7. The site's color stays on each flavor as `horn_deep_site_hue`, for reference.
- **The other five keep their stock codes** (the coordinator's reading of the ruling, 2026-11-01, which the owner may
  overrule). The ruling's intent is that no horn reads pale, and at 12.7 mm, seen through several stepped layers, these
  five read deep. The owner chose the darker colors from `link_example_strata_trucast.png`, which shows stock-code
  horns. By TT they are still lighter than the site's horn, through 12.7 mm:

  | tint | stock sheet | the site's horn |
  |---|---|---|
  | Ember | 2423, 14.1 % | 10.2 % |
  | Poison | 2092, 18.6 % | 6.4 % |
  | Haze | 2287, 13.5 % | 4.0 % |
  | Smoke | 2074, 11.7 % | 0.7 % |
  | Fog | 0000, 92 % | 78 % |

  The owner may ask for deeper.
- A heavier-batch horn is a custom pour: its 22 layers of 1/2 in come from a horn lot with a pour's minimum and lead
  time, not from stock sheet.
  The three heavier-batch horns are a custom horn lot at production. The prototype pair is priced in Smoke, so the cash
  table is unchanged.

**A doubt about Haze's code: 2287 is listed as translucent, not transparent.**
- Acme lists 2287 as "Violet – Translucent", a diffusing sheet, not a clear tint (the lamps lane, 2026-11-01).
- The research's stock lists do not carry 2287. R1 (r46-owner-notes, `research/2026-10-31/R1-stock-colours.md`, line
  259) has it only as a translucent chip, beside 2793, 2240 and 2283.
- Its 13.5 % TT is a translucent sheet's. A real 2287 cabinet would look milky and diffuse, not glassy, and the
  internals would not show.
- **The transparent violets that are known:**
  - **TruCast 373 Purple**, transparent, TT 7.4 %: stocked only in .220 in (R1, line 187).
  - **3730 Dark Purple**, transparent, TT not published: 1/8 in only (eStreet).
  - **1020 Purple**, a light violet: TT not reliably published, thin sheet only.
  - **ACRYLITE Soundstop GS Amethyst 4S01**, transparent, made in 15, 20 and 25 mm. It reads magenta, and its minimum
    is about two skids.
- **None is stocked as a transparent violet at 1/2 or 3/4 in.** Haze in the deep, transparent look needs a custom
  pour, or a mill run of a transparent purple such as 373.
- The renders keep Haze transparent at the current calibration (13.5 % held at 20 mm) until a code is settled.

The rest of this note is the comparison that led here.

---

# The comparison: the site's tints, and stock TruCast sheet's (reconciled 2026-10-31)

There are two calibrations of Tropos's eight tints on two branches. This note compares them.

- **This branch** (`make/stock_tints.py`, the stock flavors `stock-ember`, `stock-ember-trucast`, `stock-smoke`) covers
  three stock codes: 2423 Red, 2064 Gray and 2074 Dark Gray.
- **r48-biomes** (`spinoffs/barkhorn/biomes/tints.json`, commit b970bb3f) covers all eight tints. It uses this
  branch's "held" method: the seller's total transmission (TT) held at the sheet's own thickness.

`tints.py` here copies biomes' codes, TT and channel splits, and writes `tints-trucast.json`. Since 2026-11-01 these are
the line's tints (above). `make_blend.py --tints trucast` is now the same as the default.

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
