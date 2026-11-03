# The lamps in stock sheet's deeper tints (2026-11-01)

The owner, 2026-11-01: "I like the darker colors". The line takes stock TruCast tints (r46-owner-notes 8832050e):
- Ember 2423
- Poison 2092
- Haze 2287
- Dust 2422
- Acid 9097
- Ice 2069
- Fog 0000
- Smoke 2074

This note checks the lamps at their real thicknesses.

The proofs are in `renders/2026-11-01/barkhorn/tint-proof/`, made by `strata/tint_proof.py` with the calibrated acrylic.
- **The calibration:** Beer–Lambert by path length, from the chart's figure taken at 3 mm. This is the "deep" case.
- **The open question:** the chart (AC Plastics' TruCast light-transmission table) gives no thickness.
  - If the maker dilutes the dye in thick sheet so the figure holds at any thickness (the speaker lane's "held" case),
    thick stock sheet is far lighter than the proofs show.
  - Measuring chips at 1/8 and 3/8 in settles it. **Order these chips first:** about $50, a few days.

## What the proofs show (the "deep" case)

| Part | Tinted thickness | 2423 | 2092 | Read |
|---|---|---|---|---|
| Core's ball | 9 mm | 0.36 % | 0.83 % | Unlit: a dark ruby or black glass ball. Lit: a hot spot over the LED in a dark ball (`tint-proof-sheet.png`) |
| Hemisphere's shade, as drawn | 9 + 3 mm | 0.06 % | 0.17 % | Unlit: deep red / black. Lit: dim red / black (re-rendered with refractive light on the opal; the first sheet's Hemisphere frames had it off) |
| 3 mm (1/8 in) of stock | 3 mm | 15.3 % | 20.2 % | glows |

More light can't fix this: it would take 25 to 60 times the LED, and the heat with it.

## Hemisphere

Two constructions were proofed. Both keep the geometry, the lumens and the heat.

**v2, approved as a proposal and now in the CAD notes and the BOM:**
- The 9 mm outer shell is clear 0000; only the 3 mm inner skin is stock tint.
- Lit, it glows in its color (`tint-proof-hemi-v2.png`).
- **Unlit, it reads as a white opal dome behind clear glass, and the color shows only at the rim.** The day look
  loses its color.

**v3, recommended: the tint outside** (`tint-proof-hemi-v3.png`).
- **Layers, from outside in:**
  - a 3 mm stock-tint shell;
  - a 6 mm clear shell (the structural one, clamped by the collar);
  - the 3 mm opal liner, seen directly from below.
- **The look:** colored unlit (a deep gloss red or green) and glowing in color lit.
- **It is still three formed layers,** but their order and thicknesses change:
  - the outer shell goes 9 → 3 mm, and is now tinted;
  - the middle layer becomes 6 mm clear;
  - the tinted skin is replaced by the opal liner.
- **What that means:** new moulds' offsets and a change to the drawings. **The owner decides** between v2 (in the CAD
  now) and v3. No change to heat or lumens.

### Stock at 1/8 in (3 mm): what public listings show

Only clear 1/8 in is confirmed in TruCast's own listings. The rest are to confirm with AC Plastics, (888) 702-6028.

| Color | Code | 1/8 in in stock? | Note / nearest substitute |
|---|---|---|---|
| Fog | 0000 (0001) | **yes** (A&C lists clear .125, limited stock) | |
| Ember | 2423 | not found in listings: confirm | |
| Poison | 2092 | not found: confirm | 9093 Fluorescent Green is listed at .125 (a lighter, fluorescent green: 92.9 %) |
| Haze | 2287 | not found; **Acme lists 2287 as "Violet – Translucent"**, a diffusing violet, not transparent | Confirm whether TruCast 2287 is transparent. If not, Haze needs a transparent violet code from the caster |
| Dust | 2422 | not found: confirm | |
| Acid | 9097 | A&C lists 9097 at .220 in; a 1/8 in 9097 sheet appears at another seller, not branded TruCast | 2016 Yellow is listed at .125 (check that it's transparent) |
| Ice | 2069 | not found: confirm | |
| Smoke | 2074 | A&C lists it at .187 in; 1/8 not found | 3/16 in works for v3's outer layer if 1/8 isn't stocked (2074 at 4.8 mm: about 5 % in the deep case) |

## Core

The ball is one 9 mm part, drape-formed from 10 mm sheet, two hemispheres per ball. It takes about 1.5 kg of sheet a
ball, offcut included [E].

**(a) A custom pour at about 1/3 dye loading, ball only**
- It is a custom cell-cast sheet lot per color. A custom lot's minimum is about a pallet, roughly 2,500 lb (1,130 kg)
  a color (`make/horn-risks.md` L3, on `r33-speaker-horn`).
- That is about 750 balls' worth, against a first run of about 200.
- At about $4 to $6 a pound [E], that is about **$10k to $15k a color**, roughly three quarters of it left on the shelf
  after 200 balls, so about $80k to $120k for eight colors.
- Small lots: a hollow ball isn't something a caster pours in small lots; it has to come from sheet.
- First articles could use a caster's trial sheet if one will pour it [check].

**(b) The two-layer ball, recommended if the chips show "deep"**
- **The layers:** a 6 mm clear outer ball on the existing mould, and a 3 mm stock-tint inner ball, frosted inside, on a
  second, smaller mould. 1 mm of air between them.
- **The joint:** they are joined only at the equator joint and the port's grommet, as Hemisphere's nested layers are.
  **There is no bond across the face, so no bond line to hide.**
- **Cost** [E]:
  - a second mould about $1,200;
  - forming and stock 1/8 in sheet about $15 to $25 a ball;
  - **about $4k to $6k for a run of 200 in all colors.**
- **The look** (`tint-proof-core-options.png`, bottom row): a clear glass ball with a colored core. Unlit it is
  lighter at the rim; lit it glows like (a).

**(c) A stock code near 1/3 loading at 9 mm, color by color**
- What's needed: about 15 % at 9 mm, which is about 53 % or more at 3 mm in the deep case.
- **Single-layer stock 3/8 in works for** Dust 2422 (59.1 %), Ice 2069 (57.6 %), Acid 9097 (77.6 %) and Fog 0000.
- **Too deep, with no lighter stock code of the same color:** Ember 2423 (14.1 %), Poison 2092 (18.6 %), Haze 2287
  (13.5 %) and Smoke 2074 (11.7 %).
- In the "held" case, all eight stock 3/8 in sheets already sit near the target, and (c) covers the whole line.

**Recommendation:**
1. **Measure the chips first.**
2. **If "held":** Core in stock 3/8 in sheet, single layer, nothing else to buy.
3. **If "deep":**
   - Dust, Ice, Acid and Fog in single-layer stock 3/8 in;
   - **Ember, Poison, Haze and Smoke as the two-layer ball (b)**: about $4k to $6k, against about $40k to $60k for four
     custom lots.

Lumens, heat, the board, the battery route and the copy are unchanged by any of these.

## Both outcomes (the coordinator's addendum, 2026-11-01)

The proofs use "deep". The speaker lane renders sheet in its "held" central case (`make/stock_tints.py`,
`stock-pair.md` on `r33-speaker-horn`): the maker dilutes the dye in thick sheet, so a code keeps the chart's figure
at any thickness. R1 says either can be true, and only the vendor's off-cuts settle it.

| | If "held" is confirmed | If "deep" |
|---|---|---|
| **Core's ball** (9 mm, formed from 10 mm sheet) | A ball from stock sheet keeps about the chart's figure (2423 about 14 %, 2092 about 19 %): the "1/3 loading" row of `tint-proof-core-options.png`. **No custom pour, no second layer**, if the codes come at the ball's thickness | Measure, then the recommendation above: single-layer stock for Dust, Ice, Acid and Fog; the two-layer ball for Ember, Poison, Haze and Smoke |
| **Hemisphere** | **Still needed.** As drawn, the shade has two tinted layers (the shell and the skin) and the light crosses both: about 14 % × 14 % ≈ 2 % for 2423, 3.5 % for 2092. That is still dim lit. Either one-tinted-layer construction fixes it; v3 (tint outside) is still the one that keeps the color unlit | v3 recommended (v2 in the CAD now): one tinted 3 mm layer, 15 to 20 % |

**Is 3/8 in (9.5 mm) or 10 mm a stocked thickness for the eight codes?** Not that public listings show:
- A&C's TruCast pages show these and related codes at .125, .187, .220 and .500 in, with no .375 for any of the eight.
- A&C's Illinois surplus list shows 2074 only at .125 and .187.
- The ball is drawn from 10 mm sheet, so if 3/8 in isn't stocked, the nearest are:
  - **.220 in (5.6 mm) laminated pairs:** a lamination, which brings back the two-layer question;
  - **.500 in (12.7 mm):** heavier, and deeper than the chart even if "held";
  - a custom thickness, which is a custom lot.
- **So "held" helps Core only if 3/8 in is stocked or quoted in the line's codes.** Ask that in the same call as the
  chips: (888) 702-6028.

Sources: https://www.acplasticsinc.com/media/IL%20Nov%20Surplus.pdf, https://acplasticsinc.com/products/9093-500-48x-96-trucast-p,
https://www.acplasticsinc.com/products/9095-220-48x-96-trucast-p

## The decisions (the coordinator, 2026-11-01, as proposals for the owner's board)

**Hemisphere: v3 recommended; v2 stays as the alternative.**
- v3 is drawn as its own build: `dome_pendant_v3.py` → `out-dome-pendant-v3/` (drawings, BOM, cut files, 0 clashes).
- The main build `dome_pendant.py` stays v2.

| | v2 (main build) | v3 (proposal) |
|---|---|---|
| Layers, outside in | 9 mm clear shell (R 100–91), 3 mm opal (R 90–87), 3 mm stock-tint skin (R 86–83) | 3 mm stock-tint shell (R 100–97), 6 mm clear structural shell (R 96–90), 3 mm opal (R 89–86) |
| Unlit | white opal behind clear; the color only at the rim | the color, deep and glossy |
| Lit | glows in color | glows in color |
| Moulds | three (shell R 100, liner R 90, skin, female) | three: the shell mould is v2's outer form (R 100); **two new**, the clear R 96 and the opal's female R 86 |
| Layer cost, one-off, the kit's rates | $3,955 (setups $3,900 + material about $55) | $4,248 (setups $4,200 + material about $48) |
| Whole-lamp budget, one-off | $4,599 | $4,894 (+$295, all of it tooling; about $6 a shade less in sheet) |

Heat, lumens, the hub, the collar, the bayonet and the clamp are unchanged. The clamp stack is the same 12 mm of acrylic
plus the gaps.

**Core: no change until the chips are measured.**
- The two-layer ball is in Core's BOM as a priced option: `core-ball-two-layer`, about **$28 a ball** [E] on top of the
  single-layer ball. That is the inner ball's forming and 1/8 in sheet, about $15 to $25, plus the second mould's
  $1,200 spread over 200.
- The custom 1/3 pour is out on cost.

**Parked with logistics, nobody calls yet:** the chips (1/8 and 3/8 in, 2423 and 2092 first), whether 3/8 in is
stocked in the eight codes, and whether 2287 is transparent. AC Plastics, (888) 702-6028. They are on the owner's list.

## Matching the speakers' colors F (2026-11-03)

Colors F (the owner's "Go", 2026-11-01, r46-owner-notes 68adc2c3) gives the speakers:
- a white lining in seven colors, with Smoke on black;
- Poison and Haze as lighter custom batches: 32.3 % and 25.8 % through 20 mm.

The lamps keep their parts. This check uses the four-pieces room frames on `r48-four-pieces`, all in Poison:
- dusk cebd67c8;
- day e79b118d;
- lid-closed dusk ce6d7ae854c5cff34cf5f8d47b86b0abff160fd0.

Each region below is the median of its green-dominant pixels, in CIELAB (L, chroma C, hue h).

| Frame | Tropos cabinet | Tropos horn | Hemisphere | Core |
|---|---|---|---|---|
| Day (lamps off) | L 51, C 65, h 142° | L 36, C 54, h 139° | **L 47, C 60, h 139°** | L 80, C 85, h 141° |
| Dusk (lamps on) | L 28, C 42, h 144° (lit by its plinth) | L 14, C 28, h 145° | L 62, C 64, h 149° (glowing) | L 89, C 68, h 147° (glowing) |
| Lid-closed dusk | the same as dusk (only Mantle's lid changed) | | | |

**Poison: they read as one color.**
- **Hue:** all four pieces sit within 139° to 149° in every frame: one green.
- **Hemisphere:** by day it matches the cabinet closely (ΔL about 4, ΔC about 4, Δh about 2°; ΔE about 7).
- **Core:** by day it reads a step lighter and brighter than the cabinets (L 80 against 51) at the same hue. That is its
  frosted ball, lit by the window, seen through one 9 mm wall: the frost sends daylight back out.
- **At dusk** both lamps glow lighter than the cabinets, as lit glass does. The hue holds.
- **Proposed fix: none.** Core's real ball waits on the chips anyway ("held" against "deep"). Under "deep", Core's
  Poison ball goes two-layer and reads deeper, closer to the cabinets.

**Haze: it is not in any frame, and the stock lamp Haze won't match.**
- The owner's note says Haze "needed [a custom batch] anyway". Stock 2287 is listed as "Violet – Translucent", a
  diffusing violet, not see-through glass (above).
- The lamps' Haze is still drawn in 2287 (13.5 %). It would read as a chalky violet beside the speakers' clear violet.
- **The match condition:** unlit, light crosses the lamp's 3 mm tint twice (in and back out off the opal) and the
  cabinet's 20 mm wall twice (off the white lining). So the lamps' Haze layer wants about the cabinet's transmission at
  its own thickness: **about 25.8 % at 3 mm**. The same syrup as the cabinets would be far too light at 3 mm (about
  80 %). It needs its own dye loading.

**Proposed fixes for Haze, cheapest first:**
1. **A stock transparent violet near 25 % at 1/8 in, if one exists.** It costs nothing over 2287. Ask in the parked
   chip call; it applies to Hemisphere's shell and Core's Haze skin, if Core goes two-layer.
2. **The lamps' 1/8 in Haze in the speakers' Haze campaign.** Ask the caster quoting the cabinets' custom batch to
   also pour 1/8 in sheet at a loading for about 25.8 % at 3 mm in the same run [check whether they will, and the
   minimum]. That costs the run's extra sheet if they will; it costs a separate lot (about $10k to $15k [E], a pallet's
   minimum) if they won't, which is not worth it for the lamps alone.
3. **Until one of these lands,** the lamps' Haze stays unresolved. A Haze room frame from the four-pieces lane would
   confirm the match once the sheet is chosen.

## Sources (public pages, not quotes)

- AC Plastics' TruCast transmission table: https://www.acplasticsinc.com/wp-content/uploads/2026/08/Trucast-Acrylic-Light-Transmissions-5.26.26-1.pdf
- TruCast listings: https://www.acplasticsinc.com/brands/trucast, https://www.acplasticsinc.com/products/2074-187-48x-96-trucast-p,
  https://acplasticsinc.com/products/9097-220-48x-96-trucast-p, https://www.acplasticsinc.com/products/9093-125-48x-96-trucast-p
- Acme Plastics' cast colors (2287 "Violet – Translucent"): https://www.acmeplastics.com/acrylic-sheets/acrylic-cast-color-sheet-paper-masked
