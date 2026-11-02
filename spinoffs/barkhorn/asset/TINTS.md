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
- **The deep horns against F's cabinets** (the coordinator's call, 2026-11-02). The white lining lifted the colored
  cabinets, but Ice's, Dust's and Acid's deep horns did not change, so in the site set's critics the horn reads much
  darker than its cabinet: Ice's horn median about 33 to 59 against the cabinet's 130 to 150, named in six of ten passes.
  Light through the horn barely moves it. **The contrast is the design** ("the horn is the jewel"): the owner's "Deep,
  like the site" stands, and stock 1/2 in sheet would break it. **The fallback, if the owner asks:** a middle depth for
  the three deep horns, about 30 % through 12.7 mm in each cabinet's hue, still a custom batch.

**Sourcing per color in colors F** (the coordinator asked, 2026-11-01; the source lines are R1,
`spinoffs/barkhorn/research/2026-10-31/R1-stock-colours.md` on r46-owner-notes, its stock counts as of 2026-10-31).
The cabinet is 20 mm in the model (3/4 in, 19 mm, at order). The horn, caldera and plinth are 1/2 in (12.7 mm) layers.
A **mill run** is a standard code poured to a thickness nobody stocks (a minimum of about 8 to 10 sheets, no color fee;
`make/stock-pair.md`). A **custom batch** is a new tint or depth (a color match and a pour minimum).

| tint | cabinet (3/4 in) | source | horn (1/2 in layers) | source |
|---|---|---|---|---|
| Ember | **mill run**, 2423 at 3/4 in | not stocked above 1/2 in (R1 l.133; `make/stock-pair.md` l.12) | **stock**, TruCast 2423 1/2 in | AC Plastics, 19 in stock (R1 l.133) |
| Dust | **mill run**, 2422 at 3/4 in | stocked only to 1/2 in (R1 l.134) | **custom batch**, the deep horn in 2422's hue | the coordinator's call (above): deeper than stock 2422 1/2 in (59.1 %) |
| Acid | **mill run**, 9097 at 3/4 in (to confirm: a fluorescent at 20 mm is unverified) | TruCast 9097 stocked only to .220 (R1 l.161) | **custom batch**, the deep horn in 9097's hue | as Dust; 9097 is not stocked at 1/2 in at all (R1 l.161) |
| Poison | **custom batch**, 32.3 % through 20 mm in 2092's hue | colors F (above) | **mill run**, 2092 at 1/2 in | **2092 is not stocked at 1/2 in**: AC only to .220, Canal, eStreet, Delvie's and US Plastic to 1/4 in (R1 l.168) |
| Ice | **mill run**, 2069 at 3/4 in | stocked to 1/2 in, AC 42 in stock (R1 l.176) | **custom batch**, the deep horn in 2069's hue | as Dust; stock 2069 1/2 in (57.6 %) is the pale one |
| Haze | **custom batch**, 25.8 % through 20 mm in 2287's hue, transparent | colors F (above); 2287 is stocked nowhere in R1's lists, and is translucent (R1 l.259: a chip only) | **custom batch**, a transparent pour in 2287's hue at 13.5 % through 12.7 mm, as the model renders it | **no transparent violet at 1/2 in**: 373 Purple is .220 only and far deeper (7.4 %), 3730 1/8 in only, 1020 1/8 to 1/4 in (R1 ll.25, 186, 187). A 373 mill run would be the wrong depth and hue, so the custom pour is the route |
| Fog | **stock**, clear cell cast 3/4 in | Canal stocks clear to 1 in (R1 l.195) | **stock**, clear 1/2 in | clear is stocked in every thickness to 1 in (R1 l.195) |
| Smoke | **mill run**, 2074 at 3/4 in; the first pair stocked 2064 3/4 in | 2074 only to 1/2 in (R1 l.204); 2064 3/4 in, 3 left (R1 l.203) | **stock**, TruCast 2074 1/2 in | AC, eStreet, ePlastics (R1 l.204) |

- **The caldera and the plinth** are 1/2 in in the cabinet's tint (`variants/BASES.md`). They follow the cabinet's code
  at 1/2 in: stocked for Ember (2423), Dust (2422, 1 left), Ice (2069), Fog (clear) and Smoke (2074; the first pair 2064,
  stocked). Acid (9097) needs a mill run at 1/2 in. Poison and Haze come from their custom batches, poured at 1/2 in too.
- **Count:** custom batches 6, the cabinets of Poison and Haze and the horns of Dust, Acid, Ice and Haze. Mill runs 6,
  the cabinets of Ember, Dust, Acid, Ice and Smoke, and Poison's horn. Plus Acid's caldera and plinth at 1/2 in, in the
  same 9097 run if the mill pours both thicknesses. Stock: Fog's cabinet, and the horns of Ember, Fog and Smoke.
- Stock counts move. Recheck each line against the vendor before an order. These are R1's counts of 2026-10-31.

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
- **Color-matched by eye, not the dye made deeper** (the coordinator, 2026-11-02). Scaling the stock code's channel
  split up to the site's depth deepens the same dye, and a deeper dye shifts a warm tint toward red and blue toward
  violet. A real pour made that way would do the same, so this is a spec fix, not only a render fix. Measured as the
  median hue of the saturated mid-tones in the horn's mouth against the cabinet's front panel above the woofer:

  - the deck row (16641879): Dust 5 against 26, Acid 19 against 49, Ice 222 against 210; the stock horns sit on
    their cabinets (Ember -2 against -2, Poison 128 against 121, Haze 263 against 259);
  - the deck cover (f729451f): Dust 8 against 27, Acid 27 against 49, Ice 219 against 206;
  - blind naming from the row: Dust's horn "red" 3/3 against "orange" (Ember's word), Acid's "orange" 2/3 against
    "yellow", Ice's "royal blue" 3/3 against "sky blue".

  So **the three deep-horn custom batches are color-matched to look like the cabinet, at 12.7 mm, at the site's
  depth**: the caster matches each to a chip we approve against the cabinet's sheet, not to a multiple of its dye. In
  the model, each horn-lot `deep` (reached in 10 mm) is set by front-off-tall proxies until the horn's hue is within
  8 degrees of its cabinet's in the same render and its luminance within 10 % of the depth before:

  | tint | was | now | horn hue against cabinet | horn luminance | blind naming (3 viewers) |
  |---|---|---|---|---|---|
  | Dust | #F25508 (4 against 25) | **#DFA934** | 25 against 25 | 0.142 against 0.152 (-7 %) | "orange" 3/3, the cabinet "orange" 3/3 |
  | Acid | #FFB101 (14 against 50) | **#DFD710** | 52 against 50 | 0.272 against 0.265 (+3 %) | "yellow" 3/3, the cabinet "yellow" 3/3 |
  | Ice | #2981E7 (229 against 208) | **#369BCA** | 211 against 208 | 0.054 against 0.055 (-2 %) | "royal blue" 2/3, "blue" 1/3; the cabinet "sky blue" 3/3 |

  Ice passes on the coordinator's ruling: "royal blue" is the word for a deep blue at that hue, the depth the owner
  asked for, not another color; turning it further toward cyan would make a teal horn on a sky-blue cabinet. Dust's
  first match at full depth (#B68006) read brown; lightened slightly, it reads orange. The proxies and readings are
  in `renders/2026-11-02/barkhorn/site-strata-F/horn-hue/`.
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
