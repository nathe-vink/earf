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

| tint | cabinet (3/4 in) | source | horn: formed, 10 mm (horn A, since 2026-11-03) | horn chip, TT through 10 mm, against the stock code at 10 mm |
|---|---|---|---|---|
| Ember | **mill run**, 2423 at 3/4 in | not stocked above 1/2 in (R1 l.133; `make/stock-pair.md` l.12) | **custom batch**, deep red | #C50206, 11 % against 2423's 36 % |
| Dust | **mill run**, 2422 at 3/4 in | stocked only to 1/2 in (R1 l.134) | **custom batch**, deep orange | #B85010, 15 % against 2422's 74 % |
| Acid | **mill run**, 9097 at 3/4 in (to confirm: a fluorescent at 20 mm is unverified) | TruCast 9097 stocked only to .220 (R1 l.161) | **custom batch**, deep amber | #B88E00, 27 % against 9097's 85 % |
| Poison | **custom batch**, 32.3 % through 20 mm in 2092's hue | colors F (above) | **custom batch**, deep green | #0E6A06, 10 % against the cabinet batch's 55 % |
| Ice | **mill run**, 2069 at 3/4 in | stocked to 1/2 in, AC 42 in stock (R1 l.176) | **custom batch**, deep blue (a little more green than 2069 made deeper, which drifts violet) | #0A52B8, 9 % against 2069's 73 % |
| Haze | **custom batch**, 25.8 % through 20 mm in 2287's hue, transparent | colors F (above); 2287 is stocked nowhere in R1's lists, and is translucent (R1 l.259: a chip only) | **custom batch**, deep violet | #4512D0, 6 % against the cabinet batch's 49 % |
| Fog | **stock**, clear cell cast 3/4 in | Canal stocks clear to 1 in (R1 l.195) | **stock**, clear 3/8 in | clear, 92 %: clear is stocked in every thickness to 1 in (R1 l.195) |
| Smoke | **mill run**, 2074 at 3/4 in; the first pair stocked 2064 3/4 in | 2074 only to 1/2 in (R1 l.204); 2064 3/4 in, 3 left (R1 l.203) | **custom batch**, deep grey; **the first pair on stock 2074 3/8 in** (it reads at 0.48 of its cabinet, still deep) | #424548, 5 % against 2074's 33 % |

- **The caldera and the plinth** are 1/2 in in the cabinet's tint (`variants/BASES.md`). They follow the cabinet's code
  at 1/2 in: stocked for Ember (2423), Dust (2422, 1 left), Ice (2069), Fog (clear) and Smoke (2074; the first pair 2064,
  stocked). Acid (9097) needs a mill run at 1/2 in. Poison and Haze come from their custom batches, poured at 1/2 in too.
- **Count (horn A, 2026-11-03):** custom batches 9, the cabinets of Poison and Haze and seven formed horns (all but
  Fog's), each poured as 10 mm sheet for the forming. Mill runs 5, the cabinets of Ember, Dust, Acid, Ice and Smoke,
  plus Acid's caldera and plinth at 1/2 in in the same 9097 run if the mill pours both thicknesses. Stock: Fog's
  cabinet and horn, and the first pair's Smoke horn (2074 3/8 in). (With Strata's stepped horn, the alternative, it was 6
  custom batches and 6 mill runs.)
- Stock counts move. Recheck each line against the vendor before an order. These are R1's counts of 2026-10-31.

**The formed horn (horn A; the owner, 2026-11-03 03:00: "Horn: A, smooth"; polished outside since 15:14: "if so just go polished").** Each of the eight is
matched by eye to its cabinet and kept deep, as Ice and Ember were in the horn study (`renders/2026-11-02/barkhorn/
horn-study/deep/README.md`, round 2). The method: front-off-tall proxies in the site's studio (the rim lamp off), the horn's
colour moved until its median hue sits within 5 degrees of the cabinet's and its median luminance near round 2's, a
quarter to a half of the cabinet's. Five rounds in all, chips and depths in `FORMED_HORN` (`product.py`):

| tint | chip | horn against cabinet (luminance) | hue difference | in sheet terms |
|---|---|---|---|---|
| Ember | #C50206 | 0.45 | 0 | custom, about 2.3 times 2423's dye |
| Dust | #B85010 | 0.46 | +2 | custom deep orange (2422 made deeper drifts red, so the chip is its own) |
| Acid | #B88E00 | 0.56 | -1 | custom deep amber; its cabinet is the brightest, and deeper turned orange |
| Poison | #0E6A06 | 0.34 | +1 | custom deep green |
| Ice | #0A52B8 | 0.29 | +3 | custom deep blue |
| Haze | #4512D0 | 0.25 | 0 | custom deep violet |
| Fog | clear | 0.92 | (clear) | stock clear 3/8 in |
| Smoke | #424548 | 0.36 | (grey) | custom deep grey; stock 2074 3/8 in reads 0.48, deep enough for the first pair |

**Every formed horn is a custom batch but Fog's.** Stock tinted sheet, through a formed horn's single 10 mm wall, reads
pale against its 20 mm cabinet: the formed horn needs more dye a millimetre than any stocked code. The stepped horn hid
this by stacking 22 layers. The batch minimum is the caster's, to quote (the RFQ).

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

## Acid's edges, and the physical samples to order (2026-11-03)

**Acid's polished edges render coral-red** because the model's amber passes red completely: its absorption colour `#FFEB6C` has a red channel of 1.0, so along an edge's long path (0.3-0.42 m) only red survives, at 9 to 22 times the green. Fluorescence isn't modelled either. The real TruCast 9097 Fluorescent Yellow's edges glow yellow. A non-fluorescent amber would go orange at its edges, but 9097 doesn't. The model stays as it is in every shot (the coordinator, 2026-11-03: one look across the roll-out), so treat Acid's edges in any render as the model's, not the sheet's.

**The samples to order** (the coordinator puts this list to the owner, with Smoke's):

| sample | what it settles |
|---|---|
| TruCast 9097 Fluorescent Yellow, a chip with polished edges, photographed edge-on in daylight | Acid's edge colour (yellow glow, against the render's coral) |
| Chemcast 2064 "Light Smoke" (TAP), an off-cut at 3/4 in | whether it passes about 45-55 % at 20 mm, the Smoke target (R1 gives 57.07 % at 0.118 in only) |
| a Smoke horn sheet near 38 % through 10 mm | the Smoke horn's depth (`renders/2026-11-03/barkhorn/smoke-target/`) |

## Acid's long path: an approximation for a fluorescent sheet (2026-11-03)

The coordinator's gates on horn-back-acid and the biomes lane's Acid habitat held the same fault: Acid's edges and long paths rendered scarlet (236, 42, 15) on a yellow cabinet, the brightest thing on it. No fluorescent yellow sheet does that; its edges glow yellow or yellow-green.

- **The cause:** 9097's published TT (77.6 % at 20 mm) needs about 12 % lost outside the blue. The split (0, 0.10, 1.00) put all of it in green. Beer's law then leaves red alone at long path: hue 52 at 20 mm, 43 at 100 mm, 21 at 300 mm, 6 at 600 mm.
- **What the sheet really does:** its dye absorbs blue and re-emits it as yellow-green (fluorescence). The re-emitted light is guided to the edges, so the long path brightens in yellow-green rather than deepening to red. The renderer has no fluorescence.
- **The approximation:** the same loss, shared between red and green. The split goes from (0, 0.10, 1.00) to (0.085, 0.10, 1.00), red at 0.85 of green.
  - The faces stay lemon: hue 59 at 20 mm.
  - The long paths deepen to amber: hue 57 at 100 mm, 53 at 300 mm, 44 at 600 mm.
  - The edges stay within about 6° of the faces up to 300 mm.
  - The luminance at 20 mm is unchanged; it is still fitted to the TT.
  - Cabinet deep: #FFEB6C to #F1EE7F. Strata horn: #FFF296 to #F6F4A5. The formed horn keeps the site's deep lot, #B88E00, the deeper amber of the same glass.
- **What it does not do:** brighten the edges, as fluorescence would. It is darker at long path than the real sheet. Check it against the TruCast chart and, when they arrive, the off-cuts.
- **Dust (2422) is unchanged.** It is not fluorescent. An orange dye that absorbs green as well as blue does turn red at long path (hue 33 at 20 mm, 18 at 100 mm, about 0 at 300 mm). Its red top-back edge is what Beer's law gives for its TT and split, and is within what orange cast acrylic shows edge-on. No spectral curve is published to confirm the split; the off-cut is the check.

### Acid's horn and mark, re-derived from the corrected dye (2026-11-04)

The horn-back-acid gate (2/3 held) found the horn left behind by 732a8671: the cabinet moved to the new split (hue 103-107), while the horn kept #B88E00, a hand-match to the old, warmer cabinet. Horn-to-cabinet ΔE went from about 5 to 17.
- **The horn, as poured, one dye:** the same split (0.085, 0.10, 1.00) at the loading that keeps the old horn's luminance at 12.7 mm. Its deep at 10 mm is #A39700. OKLCH: 0.77 / 0.164 / 106 at 6 mm, 0.60 / 0.126 / 102 at 12.7 mm, 0.38 / 0.078 / 93 at 25 mm (the pod). The old horn was hue 81 at 12.7 mm.
- **The EARF letters' tint (`disc`):** #81720E (OKLCH 0.55 / 0.11 / 100), the cabinet's own colour about 300 mm deep. It was #9A6A12 (hue about 77, orange).
- **Which Acid frames carry which cabinet:** every frame rendered on a SHA containing 732a8671 (22:13, 2026-11-03) has the new cabinet. Every frame rendered before has the old one. Every frame before this note has the old horn and mark.
