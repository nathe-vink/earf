# EARFcoin: a quote request for 200 and 1,000 coins (round 43, 2026-10-31)

**A draft.** Nothing has been sent. It gives the Awesome Foundation application (`r47-brand`,
`brandbook/money/applications/`) a real unit cost before it goes in. The House Book has "the coin at the door"; the
grant would pay for about 200 coins handed out free.

**The design, as the owner signed it (2026-10-20, "EARFcoin: A, engraved, reeded edge"; `companions/README.md`, round 33):**
- **The coin:** 40 mm across, 6 thick, cast acrylic in a tint, about 9 g. Both arrises are rounded 1.5 and the edge
  is reeded (100 grooves 0.3 deep), then vapour-polished.
- **The back:** the EARF globe, laser-engraved 0.2 deep from a mirrored file, filled black (Smoke's white), so it reads
  the right way round from the front.
- **The front:** GOOD FOR ONE SONG over the top and EARF under it, IBM Plex Mono caps 1.9 tall, engraved 0.12, filled
  white.
- **The files:** `out-earf-coin/laser/` (SVG and DXF in mm; the cut, the back globe MIRRORED, the front words, and a
  600 × 400 nest of 104).
- **Still proposals** (not signed): the 40 × 6, the 1.5 edges, the globe at 25 across, the words' band.

## The stock colours (stand-ins for the eight tints)

All are cell cast, and all are 1/4" stock where it exists. Sources: R1, on `r46-owner-notes`
(`research/2026-10-31/R1-stock-colours.md`), and `stock-colours.md`.

| Tint | Stock stand-in | Note |
|---|---|---|
| Ember | **TruCast 2423 Red** | the prototypes' pick |
| Dust | **2422 Amber** | the closest stock hue to Dust (about 79° against 83°) |
| Acid | **2208 Yellow** | |
| Poison | **TruCast 9093 fluorescent green** (or 2092 Green, deeper and bluer) | the fluorescent glows under UV; fine for a coin |
| Ice | **2069 Light Blue** | |
| Haze | **1020 Purple** | confirm it is cast, not extruded |
| Fog | **3030 Glass Green** (or clear cast) | |
| Smoke | **TruCast 2064 Gray** | the globe filled white |

**Thickness:** US stock "1/4"" cast is often 0.220" (5.6 mm), not 6. That is fine for a coin: about 8.4 g, still
about a casino chip. The quote asks the shop to say what it stocks.

## Three routes, with estimated unit costs

All figures are **estimates [E]**, from the coin's own cost model (`coin.py --costs`: $5.46 at 500, $4.14 at 1,000 for
this face and edge), scaled for 200. **Sheet** is the swing at 200: eight tints at 25 coins each means eight part
sheets, most of it offcut. A shop with offcuts in these colours changes the answer.

| Route | What you get | 200 coins | 1,000 coins | Notes |
|---|---|---|---|---|
| **A. A Bay Area laser and CNC shop, the full design** | cut, both faces engraved and filled, rounded and reeded edge, vapour polish | **about $8–12 a coin** [E], so $1,600–2,400, sheet included (8 part sheets, about $300–650) | **about $5–6 a coin** [E], so $5,000–6,000 (8 × 24×48 sheets about $800–1,900; labour as the model, $4.14 less its sheet) | The design as signed. The reeding needs a CNC router with a vacuum fixture; a laser-only shop can't. |
| **B. A laser shop, laser only (plain edge)** | cut, both faces engraved; the edge is the laser's own glossy cut edge, arrises left sharp-ish, no reeds | **about $4–7 a coin** [E] | **about $2.50–3.50** [E] | Drops the reeding (signed) and the roundover. EARF could paint-fill by hand ($0.35 of enamel and time a coin). A fallback, not the design. |
| **C. An online laser service** (upload, pick a material) | as B, in its own stock colours (likely fewer than eight, and not these codes) | **about $3–6 a coin** [E] | **about $2–3** [E] | Fast and cheap, but the colours are theirs and nothing is reeded. For a test batch of 20 to check the faces. |

**Recommendation:** ask A-type shops for the full design at 200 and 1,000, and one online service (C) for a 20-coin
test batch in two colours (2423 and 2064) to check the engraving and fill before committing. For the grant, budget
**about $2,000 for 200**, the upper middle of route A, so it doesn't come up short.

**Candidate shops (verify before using; their capability here is from their public descriptions, not a quote):**
- **TAP Plastics** (Bay Area stores): custom fabrication and laser cutting of acrylic; carries cast sheet.
  Their reeding capability is unknown.
- **A Bay Area CNC and laser job shop:** search for a shop with both a CO2 laser (100 W or more) and a CNC router.
  A makerspace's list of fabricators is a quick start.
- **Ponoko** (online, route C): laser cutting and engraving of acrylic from uploaded files.

## The text to paste

**Short (for a web form):**

```
Quote please: 200 and 1,000 acrylic coins, 40 mm dia x 6 mm (or your 1/4" cast, 0.220"), cut from cell-cast acrylic in
8 stock colours (TruCast 2423, 2422, 2208, 9093, 2069, 1020, 3030, 2064; ~25 / ~125 of each). Each coin: laser-engraved
both faces (a line-art globe on the back, mirrored; small text on the front), engravings paint-filled; both edges
rounded 1.5 mm and 100 reeds milled round the edge (like a coin), edge vapour-polished. Vector files ready (SVG/DXF).
Price per coin at each quantity, and lead time? Can you do the reeding, or should we drop it? [Your name], [contact line]
```

**Full (for email):**

```
Subject: Quote: 200 and 1,000 engraved acrylic coins with a reeded edge

Hello,

We're EARF, a small Bay Area product company. We'd like a quote for acrylic coins (song-request tokens) at two
quantities: 200 and 1,000.

The coin:
- 40 mm across and 6 mm thick (your 1/4" cast stock at 0.220" is fine), cut from cell-cast acrylic.
- Eight stock colours, about equal numbers of each: TruCast 2423 Red, 2422 Amber, 2208 Yellow, 9093 fluorescent green,
  2069 Light Blue, 1020 Purple, 3030 Glass Green and 2064 Gray (or your nearest equivalents; please say which).
- The back face: a line-art globe laser-engraved about 0.2 mm deep from a mirrored file, filled black (white on the
  grey coins).
- The front face: two lines of small capitals (1.9 mm tall) engraved about 0.12 mm deep, filled white.
- The edge: both arrises rounded 1.5 mm, then 100 reeds milled across the edge, 0.3 mm deep (like a coin's milled
  edge), and the edge vapour-polished. The faces stay the sheet's own, masked until the end.

We have the files ready: SVG and DXF in mm, the cut, each face's engraving, and a 600 x 400 mm nest of 104.

Could you tell us:
1. The price per coin at 200 and at 1,000, and any setup charge.
2. Whether you can do the reeding and the roundover, or what you'd suggest instead.
3. Whether you'd supply the sheet (and from offcuts?), or should we.
4. The lead time, and whether you can make a sample of 10 first.

Thank you,
[Your name]
EARF
[contact line]
```
