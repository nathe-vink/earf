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

## Sources (public pages, not quotes)

- AC Plastics' TruCast transmission table: https://www.acplasticsinc.com/wp-content/uploads/2026/08/Trucast-Acrylic-Light-Transmissions-5.26.26-1.pdf
- TruCast listings: https://www.acplasticsinc.com/brands/trucast, https://www.acplasticsinc.com/products/2074-187-48x-96-trucast-p,
  https://acplasticsinc.com/products/9097-220-48x-96-trucast-p, https://www.acplasticsinc.com/products/9093-125-48x-96-trucast-p
- Acme Plastics' cast colors (2287 "Violet – Translucent"): https://www.acmeplastics.com/acrylic-sheets/acrylic-cast-color-sheet-paper-masked
