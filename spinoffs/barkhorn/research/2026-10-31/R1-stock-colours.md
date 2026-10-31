# R1: Stock cell-cast acrylic nearest to EARF's eight tints (US, checked 2026-10-31)

Prepared for EARF, San Francisco. Only the public web was used. No forms were filled, no accounts were made and no one was contacted. Prices are as shown on 31 Oct 2026 and exclude freight and tax. "Estimate" marks anything I computed or inferred rather than copied from a source. "Derived" marks simple arithmetic on published numbers, such as $/ft² = sheet price ÷ 32 ft² for a 48"×96" sheet.

**Coverage limits.**
- Several sites blocked automated access, so I did not browse them:
  - TAP Plastics product pages returned HTTP 403. A TAP PDF did load, and I also used search-engine excerpts of TAP pages.
  - Acme Plastics returned 403.
  - Professional Plastics showed a bot check.
  - Interstate Advanced Materials (interstateplastics.com) showed a Cloudflare 403. The interstateadvancedmaterials.com domain is parked.
- The shared web-search quota ran out partway through the job. A few leads are therefore unchecked; §8 lists them.

---

## 0. Bottom line

| EARF tint | Nearest stock colour (all cell cast) | Thickest US stock found | Runner-up(s) |
|---|---|---|---|
| **Ember** #CD8553 (deep red when lit) | **2423 Red** (transparent) | 1/2" (12.7 mm), TruCast at AC Plastics | 2422 Amber (if a copper/orange read is wanted); ACRYLITE Soundstop GS **Ruby 3S02**, made in 15/20/25 mm but subject to a mill minimum |
| **Ember deep** (6–10× dye) | **2423 at double path**, i.e. 2 × 3 mm, about 2% LT (estimate) | — | 2793 translucent red; 2240 burgundy |
| **Dust** #DDBA7B (warm orange) | **2422 Amber/Orange** | 1/2" (AC Plastics) | Soundstop **Topaz 2S01** (15–25 mm, mill minimum); 1300 "Gold" (1/8" only, may be extruded) |
| **Acid** #E2D481 (warm yellow) | **2208 Yellow** | 3/8" (AC Plastics) | Soundstop **Citrine 1S02**; fluorescent yellow |
| **Poison** #A4C87C (green) | **Fluorescent green**, yellow-green (TruCast 9093 / Canal 5320 / Chemcast L-111) | 1/2" (TruCast 9093) | 2092 Green (deeper and bluer); 2111 Light Green; Soundstop **Emerald 6S56** |
| **Ice** #5AC0E7 (sky blue) | **2069 Light Blue** (Pantone ref. PMS 2995 C) | 1/2" (AC Plastics) | 2120 Teal; Soundstop **Sky Blue 5S33 / Sapphire 5S09** |
| **Haze** #A080D7 (violet) | **1020 Purple**, "light purple/violet" | 1/8"–1/4" (check cast vs extruded) | 3730 dark purple; 373 Purple (TruCast); Soundstop **Amethyst 4S01** (reads magenta) |
| **Fog** #F7F8F7 (near clear, cool) | **3030 Glass Green** ("green edge") | **1" (25.4 mm) in stock** (AC Plastics) | Clear cast (to 4" at Reynolds); 2515/2514 pale greys |
| **Smoke** #787E87 (neutral grey) | **2064 Gray** | **3/4" (19 mm)** (AC Plastics, 3 sheets left) | 2074 Dark Gray; 2094 (lighter; not found in cast stock) |
| **Smoke deep** (near-black transparent) | **2074 at double or triple path** (2 layers about 1.5–1.8%, 3 layers about 0.2–0.26% LT, estimate) | — | 2370 Dark Bronze (warmer). No stock "transparent black" cast sheet was found. |

- **Thick stock is the bottleneck.** No transparent colour is stocked at 20–30 mm except 3030 Glass Green 1" and 2064 at 3/4". Most colours stop at 1/2" ([AC Plastics TruCast listing][acp-api], [Canal][canal-2064], [eStreet][es-2064-500], [ePlastics][ep-2064-500]).
- **True 20–32 mm in a standard colour needs a mill run.** There are two routes:
  - Chemcast standard colours: minimum run of 10 sheets of 48×96 at 24–32 mm ([Chemcast catalogue][cc-cat]).
  - ACRYLITE Soundstop GS: 14 transparent colours in 15/20/25 mm, minimum 2 skids (about 4,000 lb) ([Polyvantis][ac-ss-pdf]).
- **Samples cost about $63 for all chip sets:**
  - Canal 19-colour swatch pack, $19 ([link][canal-swatch])
  - eStreet chip set, $15 ([link][es-chipset])
  - ePlastics transparent set, $14.98 ([link][ep-set-transp]), plus its grey/bronze tint set, $8.69 ([link][ep-set-tint])
  - Delvie's transparent kit, $4.99 ([link][dv-samples])
- **Custom colour terms that have been published:**
  - Plastiglas/Chemcast: $150 per colour match fee; minimum 60 sheets of 48×96×0.118" or one full pallet ([catalogue][cc-cat]).
  - TAP's Chemcast policy: 2,500 lb pallet minimum and a $350 fee ([TAP PDF][tap-cc]).
  - ACRYLITE Soundstop GS: about 4,000 lb ([PDF][ac-ss-pdf]).
  - Plaskolite extruded colours: 3,000–10,000 lb ([guide][pk-guide]).

---

## 1. Four things that change how to read every table

### 1.1 The same code is not the same sheet

Published light transmission (LT) for one code varies by up to 5× between sources:

| Code | Chemcast chart @0.118" ([cc-lt], [cc-cat]) | TruCast @? ([tc-lt]) | Plexiglas/OPTIX tint values @0.118" ([pk-guide], [ep-set-tint]) | Röhm ACRYLITE aviation cast, same industry ref ([ac-db]) | Retail page |
|---|---|---|---|---|---|
| 2064 Gray | 57.07% | 29.3% | 27% | 27% (7Y43) | Canal 57% ([canal-2064]) |
| 2074 Gray | 35.49% | 11.7% | 13% | 14% (7Y17) | — |
| 2423 Red | 49.85% | 14.1% | — | — | Canal **80%** ([canal-2423]); looks like a template value |
| 2422 Amber/Orange | 85.80% | 59.1% | — | — | — |
| 2069 Light Blue | 85.53% | 57.6% | — | — | — |
| 2092 Green | 78.74% | 18.6% | — | — | — |
| 2404 Bronze | 79.58% | 59.5% | 49% | 33% (7Y38) | — |
| 2370 Bronze | 11.85% | 13.8% | 10% | — | US Plastic 10% ([usp-kb]) |

Chemcast's chart says only that LT was "measured as a function of the opacity of the material in 0.118''" ([cc-lt]). TruCast's chart calls its numbers "typical properties of the base resins" ([tc-lt]).

**Inference (not confirmed):** Chemcast's figures are either on a different measurement basis or describe lighter formulations. 2370 agrees across all sources, but the greys and reds disagree by 2–3×. Two practical consequences:
- Buy chips from the exact vendor and brand you will buy sheet from.
- Build both units of a pair from one source.

Code numbers are not universal either. Chemcast lists 2538 as a 38% bronze ([cc-cat]), while Plaskolite lists 2538 as a 16% grey ([pk-guide]).

### 1.2 Thickness: does the tint deepen or not?

- Some makers keep LT the same at every thickness by changing the dye loading:
  - ACRYLITE's extruded brief says LT for "all thicknesses of a given translucent or transparent color… is the same… by adjusting the colorant concentration" ([ac-ext-lt]).
  - ePlastics says of its Plexiglas tint set that values "do not change with thickness" ([ep-set-tint]).
  - Plaskolite flags only its whites as thickness-dependent ([pk-guide]).
- Chemcast gives LT at 0.118" only and refers other thicknesses to customer service ([cc-cat]).

So a stock 1/2" sheet may look exactly like the 3 mm chip, or about 4× deeper. **Order a 1/2" off-cut of the same code (§5) before buying thick sheet.**

If EARF's own pour uses **one dye loading for all thicknesses** ("tinted all the way through"), Beer–Lambert gives the following. This is an *estimate*: it treats the hex as the 5 mm transmitted colour, works per sRGB channel and assumes 8% surface loss.

| Path length in base tint | Ember LT | Ember look (est. hex) | Smoke LT | Smoke look (est. hex) |
|---|---|---|---|---|
| 5 mm (the reference) | ~30% | #CD8553 | ~21% | #787E87 |
| 10 mm | ~13% | #AB4516 | ~4.7% | #373D47 |
| 20 mm | ~4.1% | #750D00 | ~0.24% | #05080E |
| 30 mm (≈ "6× dye" at 5 mm) | ~1.7% | #4F0100 | ~0.013% | near black |
| 50 mm (≈ "10× dye" at 5 mm) | ~0.3% | #210000 | ≈0 | black |

**Implication (estimate):** at one loading, 25–30 mm Smoke cabinet walls would look as dark as the "deep Smoke" horn, close to black face-on. EARF should decide whether thick parts should deepen or read like the 5 mm reference before a custom pour.

### 1.3 Thick colours are scarce

See §4. Above 1/2", the only stocked transparent colours I found were 2064 at 3/4" ([acp-2064-750]) and 3030 at 1" ([acp-3030-1000]).

### 1.4 Nominal sizes

- "1/4" colour sheet" is often 0.220" (5.6 mm). Canal states this explicitly ([canal-2423]).
- AC Plastics sells .220 and .250 as separate items ([acp-api]).
- Chemcast makes 8.0 mm (0.315") and 10 mm (0.394") as standard thicknesses ([cc-cat]), but I found no US **stock** colour sheet at 8 mm. The nearest stock is 3/8" (9.0–9.5 mm).

---

## 2. Targets: what the hex values imply (estimates)

The CIELAB values are computed from each hex. "Est. LT" assumes the hex is the colour transmitted through 5 mm against white, so it is an *estimate* only.

| Tint | Hex | EARF's transmitted-light description | L* / C* / hue° | Est. LT @5 mm | Stock family to look in |
|---|---|---|---|---|---|
| Ember | #CD8553 | deep red | 62 / 44 / 59° | ~30% | transparent red (2423), amber (2422) |
| Dust | #DDBA7B | warm orange | 77 / 37 / 83° | ~52% | amber/orange 2422, gold |
| Acid | #E2D481 | warm yellow | 84 / 43 / 99° | ~65% | yellow 2208 |
| Poison | #A4C87C | green | 77 / 42 / 126° | ~51% | yellow-green (fluorescent green), 2092, 2111 |
| Ice | #5AC0E7 | sky blue | 73 / 34 / 237° | ~46% | light blue 2069 |
| Haze | #A080D7 | violet | 60 / 50 / 307° | ~28% | purple 1020 / 3730 |
| Fog | #F7F8F7 | near clear, cool | 98 / 0.6 / — | ~94% | clear, 3030 glass green, pale greys |
| Smoke | #787E87 | neutral grey (slightly cool) | 53 / 6 / 267° | ~21% | grey 2064 (photopic 27–29%) / 2074 (12–13%) |
| Ember deep | — | deep, nearly opaque red | — | ~1.7% (6×) to ~0.3% (10×) | 2423 ×2 layers ≈ 2.2% (est.) |
| Smoke deep | — | near-black, transparent | — | ≤0.01% (6×), estimate | 2074 ×3 layers ≈ 0.2% (est.) |

---

## 3. Nearest stock colours, tint by tint

All entries are cell cast unless flagged. "48×96" means a 48"×96" sheet, and $/ft² is *derived*. AC Plastics stock counts are live values read from its public store data on 31 Oct 2026 ([acp-api]).

### Ember (#CD8553, "deep red when lit")

| # | Brand / line | Code / name | Published LT @~3 mm | Colour evidence | US stock thicknesses (where) | Price examples | Notes |
|---|---|---|---|---|---|---|---|
| 1 | Chemcast (Plastiglas de México); TruCast (AC Plastics); also sold by Canal, eStreet, Delvie's, US Plastic | **2423 Red**, transparent | Chemcast 49.85% ([cc-cat]); TruCast 14.1% ([tc-lt]) | Pantone ref. PMS 186 C ([cc-cat]). Photos: [Delvie's][dv-img-2423], [Canal][canal-img-2423]. Canal: "a theater gel or stained glass panel" ([canal-2423]) | 1/16"–1/4" at all; .250, .375, .500 TruCast ([acp-2423-250], [acp-2423-375] 10 in stock, [acp-2423-500] 19 in stock) | Canal 1/8" $142, 1/4" (0.220") $267 per 48×96 (~$4.44 / $8.34 per ft²) ([canal-2423]); eStreet 1/8" $124, 1/4" $240 ([es-2423-125], [es-2423-250]); AC 3/8" $680.40, 1/2" $835.80 (~$21.26 / $26.12 per ft²); Delvie's 24×48 1/8" $39.50, 1/4" $73 ([dv-transp]) | Best fit to "deep red when lit". Photo hue is redder than the Ember hex (App. A, estimate). |
| 2 | Chemcast; TruCast | **2422 Amber** (sold as "Orange" by US Plastic and eStreet) | Chemcast 85.80%; TruCast 59.1% | PMS 1505 C ([cc-cat]); [Delvie's photo][dv-img-2422] | to 1/2": [acp-2422-375] 13 in stock, [acp-2422-500] 1 left | AC 3/8" $680.40, 1/2" $835.80; Canal 1/8" $142 / 1/4" $267 ([canal-2422]) | Choose this if Ember should read copper/orange in thin parts. Overlaying 2422 on 2423 shifts the red toward the Ember hex (untested suggestion). |
| 3 | ACRYLITE Soundstop GS (Polyvantis; cell cast noise-barrier sheet) | **Ruby 3S02** | not published (−1 in [ac-db]) | [product image][img-ruby] | 15, 20, 25 mm in 2030×3050/4050/5050 and 2380×3300 mm ([ac-ss-pdf]) | Not priced. **Minimum 2 skids (~4,000 lb)** ([ac-ss-pdf]) | The only standard red I found at 20–25 mm. Catalogue item, not distributor stock. |
| alt | TruCast; Chemcast; Reynolds | Fluorescent red: 9095 / L-116 / Fl Red 3375 | TruCast 9095 34.5% ([tc-lt]) | — | TruCast ≤ .220" ([acp-9095-220], $210 per 48×96); Reynolds lists Fl Red 3375 among stocked thin-gauge colours ([rp-thin]) | — | Glowing edges. Chemcast rates its fluorescents "for indoor application only" ([cc-cat]). |

### Ember deep (6–10× dye: deep, nearly opaque red)

| # | Option | LT | Stock / price | Notes |
|---|---|---|---|---|
| 1 | **2423 Red at double path**: two 1/8" layers, or one 1/4"–3/8" sheet *if* that vendor keeps dye loading constant | 2 × TruCast 14.1% ≈ **2.2%** (estimate); 3 layers ≈ 0.33% (estimate). Brackets the 6–10× target of ~1.7–0.3% (estimate) | AC .250 48×96 $423.64, 3 left ([acp-2423-250]); AC .125 48×96 $151.20 ([acp-2423-125]); eStreet 1/4" $240 ([es-2423-250]) | Stays clear. For a formed horn, two thin formed shells nested together is an untested suggestion. |
| 2 | **2793 Red**, translucent sign red | Chemcast 7.12%, PMS 485 C 2X ([cc-cat]); TruCast 4.5% ([tc-lt]) | AC .375 $680.40 (27 in stock), .500 $835.80 (45 in stock) ([acp-2793-500]); chip $1.45 ([es-chip-2793]) | Pigmented, so it diffuses light. Reads as solid deep red and glows rather than looking clear. |
| 3 | **2240 Burgundy** (TruCast; listed "Opaque") | TruCast 3.1% ([tc-lt]) | AC .125 $151.20, .187 $229.60 ([acp-2240-125]); "Maroon #2240" chip $1.45 ([es-chip-2240]) | Darkest red. Near-opaque. |

### Dust (#DDBA7B, "warm orange")

| # | Brand / line | Code / name | LT | Colour evidence | US stock thicknesses | Price examples | Notes |
|---|---|---|---|---|---|---|---|
| 1 | Chemcast; TruCast; others | **2422 Amber** | 85.80% (Chemcast) / 59.1% (TruCast) | Photo-derived hue ≈79° vs Dust 83°, the closest stock hue (App. A, estimate). PMS 1505 C | to 1/2" (AC) | as above | Best stock match for "warm orange". |
| 2 | ACRYLITE Soundstop GS | **Topaz 2S01** | n/p | [image][img-topaz] (amber-orange) | 15/20/25 mm | ~4,000 lb minimum ([ac-ss-pdf]) | Thick option. |
| 3 | Canal; Delvie's | **1300 Gold**, "transparent" | n/p | [Canal photo][canal-img-1300]: pale peach-gold. Delvie's photo is captioned "*Extruded sheet" ([dv-img-1300]) | Canal 1/8" only ([canal-1300]); Delvie's 1/8" | Canal 48×96 $246 (~$7.69/ft²); 24×48 $77 | Closer to the Dust hex in reflected light but much paler in transmission (estimate). **Confirm cast vs extruded.** |
| alt | Chemcast; TruCast | **2404 Light Bronze** | 79.58% / 59.5% / Plexiglas 49% | PMS 463 U | TruCast .125/.220/.500 ([acp-2404-500], $569.80 at 1/2") | — | For a more muted, "dusty" read. |

### Acid (#E2D481, "warm yellow")

| # | Brand / line | Code / name | LT | Colour evidence | US stock thicknesses | Price examples | Notes |
|---|---|---|---|---|---|---|---|
| 1 | Chemcast; TruCast; others | **2208 Yellow** | Chemcast 90.69% (PMS 109 C) ([cc-cat]) | [Delvie's photo][dv-img-2208]; photo hue ≈102° vs 99° (estimate) | 1/8"–1/4" everywhere; 3/8" TruCast, 18 in stock ([acp-2208-375]) | AC 3/8" $680.40; Canal $142 / $267 ([canal-2208]); eStreet $124 / $240 | Best stock match. |
| 2 | ACRYLITE Soundstop GS | **Citrine 1S02** | n/p | [image][img-citrine] (pale lemon) | 15/20/25 mm | ~4,000 lb minimum | Thick option. |
| 3 | TruCast 9097; Canal 5740; Chemcast L-043 | Fluorescent yellow | TruCast 77.6% | Canal: "sharp, high-visibility yellow" ([canal-5740]) | TruCast ≤ .220 ([acp-9097-220], $210); Canal 1/8", 1/4" ($166 / $290) | — | Greener, with glowing edges. Indoor only per Chemcast. |

### Poison (#A4C87C, "a green", yellow-green hue 126°)

| # | Brand / line | Code / name | LT | Colour evidence | US stock thicknesses | Price examples | Notes |
|---|---|---|---|---|---|---|---|
| 1 | TruCast 9093; Canal 5320; Chemcast L-111 | **Fluorescent green** | TruCast 92.9% ([tc-lt]) | Canal: "a bright, yellow-green fluorescent" ([canal-5320]) | TruCast to 1/2", 5 left ([acp-9093-500]); Canal 1/8", 1/4" | AC 1/2" 48×96 $873.60; Canal $166 / $290 | Closest *hue*, but glows at the edges. Chemcast: fluorescents for indoor use only. |
| 2 | Chemcast; TruCast; others | **2092 Green** | Chemcast 78.74% (PMS 355 C); TruCast 18.6% | [Delvie's photo][dv-img-2092]; photo hue ≈151°, bluer and more saturated (estimate) | ≤ .220 at AC ([acp-2092-220], $294); 1/4" at Canal ([canal-2092]), eStreet, Delvie's, US Plastic ([usp-250]) | Canal $142 / $267 | A deeper "bottle" green. |
| 3 | TruCast; Canal; ePlastics set | **2111 Light Green** | TruCast 78.3%; Röhm aviation 6Y32 (ref. 2111) 76% ([ac-db]) | [Canal photo][canal-img-2111] reads pale sea-green | 3/8" TruCast, 11 in stock ([acp-2111-375], $680.40); Canal 1/8", 1/4" ([canal-2111]) | — | Paler and bluer than Poison. |
| thick | ACRYLITE Soundstop GS | **Emerald 6S56** / Spring Green 6S40 | n/p | [Emerald image][img-emerald] (light yellow-green) | 15/20/25 mm | ~4,000 lb minimum | — |

### Ice (#5AC0E7, "sky blue")

| # | Brand / line | Code / name | LT | Colour evidence | US stock thicknesses | Price examples | Notes |
|---|---|---|---|---|---|---|---|
| 1 | Chemcast; TruCast; others | **2069 Light Blue** | Chemcast 85.53% (**PMS 2995 C**, a sky blue); TruCast 57.6% | [Delvie's photo][dv-img-2069]; Canal: "a clear, open sky blue" ([canal-2069]); photo hue ≈219° vs 237° (estimate) | 1/8"–1/4" everywhere; 3/8" (AC, 6 in stock; ePlastics 0.375" [ep-2069-375]); 1/2" (AC, 42 in stock, [acp-2069-500]) | AC 3/8" $680.40, 1/2" $835.80; ePlastics 3/8" $845.31; Canal $142 / $267 | Strongest match of the whole set. |
| 2 | Canal; Delvie's | **2120 Teal** | n/p | Canal: light through it "throws a bright aqua cast" ([canal-2120]) | Canal 1/8" ($246 per 48×96); Delvie's 1/8"–1/4" | — | Greener. |
| 3 | ACRYLITE Soundstop GS | **Sky Blue 5S33 / Sapphire 5S09** | n/p | [Sky Blue][img-skyblue], [Sapphire][img-sapphire] | 15/20/25 mm | ~4,000 lb minimum | Sapphire's image reads closest to Ice. |
| no | — | 2424 Blue | Chemcast 48.11% (PMS 286 C royal blue); TruCast 10.4% | — | — | — | Too dark and too purple. |

### Haze (#A080D7, "a violet")

| # | Brand / line | Code / name | LT | Colour evidence | US stock thicknesses | Price examples | Notes |
|---|---|---|---|---|---|---|---|
| 1 | Canal; Delvie's; ePlastics | **1020 Purple**, "light purple/violet" | Not reliably published. Canal shows 80% ([canal-1020]), which looks like a template value | [Delvie's photo][dv-img-1020]; Canal: "a vivid violet… leans warm rather than blue" ([canal-1020]); photo hue ≈315° vs 307°, the closest (estimate) | Canal 1/8" (cast); Delvie's 1/8", 1/4" ([dv-transp]) | Canal 48×96 $246, 2"×2" $1; Delvie's 24×48 $39.50 / $73 | ePlastics notes 0.125" 1020 is "only stocked in extruded" ([ep-transp]). **Confirm cast.** |
| 2 | eStreet; ePlastics set | **3730 Dark Purple** (transparent) | n/p | eStreet chip ([es-chip-3730]) | eStreet 1/8" only ([es-3730], $124 per 48×96) | — | Darker. |
| 3 | TruCast | **373 Purple** (transparent) | TruCast 7.4% | — | .220 only, 69 in stock ([acp-373-220], $294) | — | Darker. |
| thick | ACRYLITE Soundstop GS | **Amethyst 4S01** | n/p | [image][img-amethyst] reads magenta | 15/20/25 mm | ~4,000 lb minimum | Pinker than Haze. |

### Fog (#F7F8F7, "near clear, cool")

| # | Brand / line | Code / name | LT | Colour evidence | US stock thicknesses | Price examples | Notes |
|---|---|---|---|---|---|---|---|
| 1 | Chemcast; TruCast; others | **3030 Glass Green** ("green edge") | Chemcast 91.75% (PMS 331 C); TruCast 86.8% | [Delvie's photo][dv-img-3030]: near-clear face, green edges | **Thickest coloured stock found**: 3/8" and 1/2" (Canal [canal-3030]; AC [acp-3030-500]); **1"** (AC 48×96, 9 in stock, [acp-3030-1000]; 48×48, 2 left, [acp-3030-1000-48]) | Canal 3/8" $375, 1/2" $495; AC 1" 48×96 $1,919.40 (~$59.98/ft²), 48×48 $959.70 | Best Fog proxy at true cabinet thickness. |
| 2 | many | **Clear** cell cast | Chemcast 91.9% | — | Canal to 1" (0.944"/24 mm), $915 per 48×96 ([canal-clear]); Reynolds stocks clear 1.00"–4.00" ([rp-thick]) | — | Fully neutral. |
| 3 | Chemcast; TruCast | **2515 / 2514** pale greys | Chemcast 85.77 / 86.64%; TruCast 69.1 / 60.7%; Plaskolite (extruded) 75 / 58% | — | TruCast 2515 .220, 1 left ([acp-2515-220]); 2514 .125 only | AC 2515 .220 $231 | Slightly cool grey. |
| thick | ACRYLITE Soundstop GS | Steel Blue 5S31 / Danish Green 6S50 | n/p | [Steel Blue][img-steelblue], [Danish Green][img-danish] (very pale cool tints) | 15/20/25 mm | ~4,000 lb minimum | — |

### Smoke (#787E87, "a neutral grey"; est. ~21% at 5 mm)

| # | Brand / line | Code / name | LT | Colour evidence | US stock thicknesses | Price examples | Notes |
|---|---|---|---|---|---|---|---|
| 1 | Chemcast (TAP's "Light Smoke"); TruCast; Plexiglas-type (ePlastics); Reynolds | **2064 Gray** | Chemcast 57.07% (PMS 418 C); TruCast 29.3%; Plexiglas/OPTIX 27%; Röhm aviation 7Y43 27% | [Delvie's photo][dv-img-2064] (neutral) | **Widest thick stock of any tint:** 3/8" and 1/2" (Canal [canal-2064], eStreet [es-2064-500], ePlastics [ep-2064-500], AC [acp-2064-375]/[acp-2064-500]); **3/4" (19 mm)**, 3 left ([acp-2064-750]). Reynolds lists 2064 among stocked thin-gauge colours; its thin-gauge range runs 0.060"–0.944" ([rp-thin]) | Canal 3/8" $375, 1/2" $495 (~$15.47/ft²); eStreet 1/2" 48×96 $550, 24×48 $174.03; ePlastics 1/2" $636.90; AC 3/8" $424.60, 1/2" $569.80, 3/4" $1,003.20 (~$31.35/ft²) | Closest by luminance (photopic 27–29% vs ~21% target, estimate). Neutral rather than slightly cool. |
| 2 | same sources | **2074 Dark Gray** (TAP's "Dark Smoke") | Chemcast 35.49% (ref. Black C); TruCast 11.7%; Plexiglas 13%; Röhm 7Y17 14% | [Delvie's photo][dv-img-2074], slightly warm | to 1/2" (AC [acp-2074-500]; eStreet [es-2074-500]; ePlastics [ep-2074-500]) | AC 1/2" $569.80; eStreet $550; ePlastics $636.90 | Darker than target. |
| 3 | Chemcast; TruCast | **2094 Gray** | Chemcast 72.25% (PMS 404 C, warm grey); TruCast 48.7%; OPTIX (extruded) 45% | — | **Not found in US cast stock.** OPTIX extruded only ([pk-guide]) | — | Lighter than target. |

TAP Plastics sells Chemcast ([TAP Chemcast info page][tap-info]; [TAP custom-colour PDF][tap-cc]). Search-engine excerpts of TAP's transparent-colour page ([tap-519]; the page blocked automated fetch) show these figures, which match the Chemcast chart:
- "Transparent Light Smoke" ~57%, "Dark Smoke" 36% (35.5% in the technical table)
- "Dark Red" ~50%
- "Amber" ~86%
- "Light Blue" 86%

The same excerpts show Dark Red in 1/8" only, and Amber and Dark Smoke in several thicknesses.

### Smoke deep (near-black transparent)

| # | Option | LT | Stock / price | Notes |
|---|---|---|---|---|
| 1 | **2074 at double or triple path** | 2 layers ≈ 1.5–1.8%, 3 layers ≈ 0.2–0.26% (estimate from TruCast 11.7% / Plexiglas 13%). The 6× target is ~0.01% (estimate) | AC .125 48×96 $128.70, 478 in stock ([acp-2074-125]); eStreet 1/8" 48×96 $124 ([es-2074-125]) | Stays neutral and clear. |
| 2 | **2074 at 1/2"** | ≈0.02–0.03% *if* dye loading is constant (estimate); ~12–13% if LT is held constant (see §1.2) | AC $569.80 ([acp-2074-500]); eStreet $550 | Check a 1/2" off-cut first. |
| 3 | **2370 Dark Bronze** | Chemcast 11.85% (PMS 412 C); TruCast 13.8%; Plexiglas 10% | Canal 3/8" $375, 1/2" $495 ([canal-2370]); AC .500 $569.80 ([acp-2370-500]) | Warm/brown cast. |

No cast "transparent black" sheet turned up in any US stock list I checked. Production deep Smoke will probably need a custom colour.

---

## 4. Thick cast sheet (15–32 mm): what exists

| Source | Colours | Thickness | Status | Minimum | Link |
|---|---|---|---|---|---|
| AC Plastics (TruCast, cell cast; stock locations Houston TX, Illinois and Colorado per a product page) | 2064 Gray | .750" (19 mm) | **Stock**, 3 left | 1 sheet (48×96) | [acp-2064-750] |
| AC Plastics | 3030 Glass Green | 1.000" (25.4 mm) | **Stock**: 48×96 (9), 48×48 (2) | 1 sheet | [acp-3030-1000] |
| AC Plastics | 2064, 2074, 2370, 2412, 2404, 2423, 2422, 2069, 2424, 2793, 2283, 9092, 9093, 3030; plus 2208, 2111 at 3/8" | ≤ .500" (12.7 mm) | Stock | 1 sheet | [acp-api] |
| Canal Plastics | 2064, 2370, 3030 | ≤ 1/2" (0.472"/12 mm) | Stock | — | [canal-2064] |
| Canal Plastics | Clear | to 1" (0.944"/24 mm) | Stock, $915 per 48×96 | — | [canal-clear] |
| eStreet; ePlastics | 2064, 2074 (+2069 3/8" at ePlastics) | ≤ 1/2" | Stock | — | [es-2064-500], [ep-2064-500], [ep-2069-375] |
| Reynolds Polymer (Grand Junction, CO) | Thin gauge stocks clear, 2064, 2412, fluorescents (Fl Amber 2422, Fl Red 3375, Fl Blue 3372, Fl Green 3377); thick gauge stocks clear only | Thin gauge 0.060"–0.944"; thick 1.00"–4.00" | Which gauges each colour is stocked in is not published. "Custom colors for thick cast sheets available by special order" | Not published | [rp-thin], [rp-thick] |
| Plastiglas de México (Chemcast GP) | All standard colours (see App. B) | 1.5–50 mm, incl. 15, 18, 20, 21, 24, 25, 32 mm | **Made to order**, standard colour, so no colour development | Minimum run per batch (48×96): 15 sheets (1.5–12 mm), 8 (15–18 mm), **10 (24–32 mm)**, 6 (38–50 mm). Larger sizes: 8 / 8 / 8 / 6 | [cc-cat] |
| Polyvantis: ACRYLITE Soundstop GS (cell cast) | Ruby, Topaz, Citrine, Amethyst, Sky Blue, Steel Blue, Midnight Blue, Sapphire, Spring Green, Emerald, Sea Green, Forest Green, Danish Green, Smoky Brown (all transparent) | 15, 20, 25 mm; sheets ≈ 80"×120" and larger | Catalogue product | **2 full skids (~4,000 lb)** | [ac-ss-pdf], [ac-ss] |
| Polyvantis: ACRYLITE cast "General Grade" | Clear only in the public database | 3–40 mm | — | — | [ac-db], [ac-gp] |
| Plaskolite: OPTIX Cell Cast (ex-Plazcast) | "Wide range of colors" | 3–60 mm | "Only available in EMEA, APAC, LATM", **not North America** | — | [pk-cellcast] |
| Plaskolite: OPTIX-L (continuous cast, NA) | Standard: clear, whites, Bronze 2412, black, Cascade Blue 7T5D | 0.080"–0.315" | Non-stock colours "may require a minimum quantity order" | — | [pk-optixl], [pk-optixl-colors] |
| Spartech Polycast | Sheet: custom aerospace SolarControl tints; **rods** in transparent 2064, 2069, 2074, 2092, 2111, 2208, 2370, 2404, 2414, 2422, 2423, 2424, 2473 Copper, 6738 Violet, 3030 | Coloured rods 0.500"–3.00" dia., 4 ft lengths | Rods are stock items. Sheet colours are not | — | [sp-rod], [sp-rods-broch], [sp-sc] |

**Weight check (derived):**
- ACRYLITE gives 25 mm sheet as 6.10 lb/ft² ([ac-ss-pdf]). A 48×96 sheet at 25 mm therefore weighs ≈195 lb, and a 10-sheet Chemcast run at 24–32 mm is ≈1,950–2,500 lb, about one pallet.
- Chemcast packs 14 sheets per pallet at 24 mm (48×96) and 10 sheets at 32 mm ([cc-cat]).
- ePlastics lists a 1/2" 48×96 sheet at 93.6 lb ([ep-2064-500]).

---

## 5. Cheap physical samples

| Vendor | Product | Contents | Size / thickness | Price | Link |
|---|---|---|---|---|---|
| Canal Plastics | **Transparent Collection Swatch Pack** | One of each of 19 transparent colours | 2"×2", 1/8" | **$19.00** | [canal-swatch] |
| Canal Plastics | Single "2"×2" Sample" option on each colour page (2064, 2370, 3030, 2423, 2422, 2208, 2092, 2111, 2069, 2424, 1020, 2120, 2414, 1300, 1350, L-709, fluorescents…) | 1 chip | 2"×2", 1/8" | **$1.00** each | e.g. [canal-2064], [canal-1020] |
| eStreet Plastics | **Transparent Colored Plexiglass Sample Chip Set** | All transparent colours | 2.75"×2.75", 1/8", cell cast | **$15.00** | [es-chipset] |
| eStreet Plastics | Single chips: 2064, 2074, 2370, 2069, 2422, 2208, 2092, 2424, 2423, 3030, 3730; translucent 2793, 2240, 2283, 2287 | 1 chip | 2.75"×2.75" | **$1.45** each | [es-chip-2423], [es-chip-2793] |
| ePlastics | **Plexiglass Transparent Colors Sample Set** | 2069, 2424, 2208, 2422, 2111, 2092, 3030, 2423, 1020, 3730 | 1/8"; listed as 4"×6" (SKU says 3.75"×5.75") | **$14.98** | [ep-set-transp] |
| ePlastics | **Plexiglas Bronze & Gray tint sample set** | colourless, 2064, 2074, 2404, 2412, 2370, plus LT table | 1/8" | **$8.69** | [ep-set-tint] |
| ePlastics | Fluorescent set / Color set | — | — | $21.74 / $22.44 | [ep-transp], [ep-colors] |
| Delvie's Plastics | **Transparent Sample Kit** (full kit $24.99) | Every transparent colour Delvie's carries | 1"×2" | **$4.99** | [dv-samples] |
| Thickness test pieces | eStreet 2064 1/2"×12"×12" $27.35 ([es-2064-1212]); Delvie's 12"×12" 1/4" any transparent $11.00 ([dv-transp]); Canal 12"×12" 1/4" $11.50 ([canal-2423]) | — | — | — | — |

**Suggested basket (estimate ≈ $63 plus shipping):**
- Canal pack ($19)
- eStreet set ($15)
- ePlastics transparent set ($14.98) and tint set ($8.69)
- Delvie's kit ($4.99)

Add the eStreet 1/2" 2064 square ($27.35) and a 1/4" 2423 square ($11–11.50) to settle the thickness question in §1.2.

Compare all chips against a high-CRI white light and EARF's actual LED. Polyvantis and Plaskolite also offer sample-request forms ([ac-finder], [pk-optixg]); they were not used, per the rules.

**Local option:** Piedmont Plastics' San Francisco branch is at 33340 Central Avenue, Union City, CA ([pd-sf]), and Piedmont lists the Chemcast colour catalogue among its literature ([pd-cast]).

---

## 6. Recommended stock set for the first prototypes

This uses stock only, with no minimums. The aim is to get geometry, acoustics and the light look right now. A custom pour comes later.

| Part | Tint | Stock pick | Build | Source and price (48×96 unless noted) | Check before cutting |
|---|---|---|---|---|---|
| **Tropos cabinet ×2** | Ember | **TruCast 2423 Red, 1/2" (12.7 mm)** | Use as 12.7 mm walls, or laminate 2 × 1/2" to ≈25 mm (untested suggestion; doubles the dye path) | AC Plastics $835.80/sheet, 19 in stock ([acp-2423-500]). Two sheets = $1,671.60 | A 1/2" off-cut vs the 1/8" chip (§1.2). If too deep, step down to 3/8" ($680.40, [acp-2423-375]). |
| **Tropos horn ×2** (formed) | Ember deep | **2423 Red .250"** single, or two formed 1/8" shells nested | AC .250 $423.64, 3 left ([acp-2423-250]); AC .125 $151.20 ([acp-2423-125]) | Compare with 2793 translucent ([acp-2793-500]) if "nearly opaque" matters more than clarity. |
| **Tropos cabinet ×2** | Smoke | **TruCast 2064 Gray, 3/4" (19 mm)**. Add a .220" layer for ≈24.6 mm, or use 2 × 1/2" | 3/4" + 0.220" laminate, or 2 × 1/2" | AC 3/4" $1,003.20, 3 left ([acp-2064-750]); AC .220 $231 ([acp-api]); or Canal 1/2" $495 each ([canal-2064]) | Same thickness check. Buy all Smoke sheet from one source (§1.1). |
| **Tropos horn ×2** (formed) | Smoke deep | **2074 Dark Gray 1/8"** ×2–3 layers or nested shells | — | AC .125 $128.70, 478 in stock ([acp-2074-125]); eStreet 1/8" $124 ([es-2074-125]) | Two layers ≈1.5–1.8% LT (estimate); three ≈0.2% (estimate). |
| **Lamp** | Ember | **2423** 1/8"–1/4", optionally with a 2422 Amber layer for a warmer ember tone | — | Canal 24×48: $56 (1/8"), $84 (1/4") ([canal-2423]); Delvie's 24×48: $39.50 / $73 ([dv-transp]) | Matte (P-95) versions exist for diffusion: Chemcast offers all standard colours in P-95/DP-95 ([cc-cat]). |
| **Lamp** | Smoke | **2064** 1/8"–1/4" (2074 for darker accents) | — | Canal 24×48 $56 / $84 ([canal-2064]); Delvie's $39.50 / $73 | — |

**Rough budget (estimate):** ≈ $3.6–4.0k in sheet, plus LTL freight for 48×96 sheets from AC Plastics. The total is the sum of the listed sheet prices plus about $225 of 24×48 lamp sheet. Using 2 × 1/2" Canal 2064 ($990) instead of 3/4" + .220 ($1,234.20) saves about $240.

**If the 20–30 mm look must be monolithic for the first pair:** order Chemcast **2423** and **2064** at 24/25 or 32 mm as a *standard-colour* run. That means a 10-sheet minimum per colour and thickness, no colour-match fee, and LT published at 3 mm only ([cc-cat]). Alternatively, look for Soundstop GS **Ruby** remnants through an ACRYLITE distributor. That is not verified, and the mill minimum is ~4,000 lb ([ac-ss-pdf]).

**Other tints, for the next prototypes:**
- Dust: 2422
- Acid: 2208
- Poison: fluorescent green (or 2092)
- Ice: 2069
- Haze: 1020
- Fog: 3030 (1" in stock)

---

## 7. Published custom-colour minimums and fees

| Maker / seller | Applies to | Minimum | Fee | Lead time / other | Source |
|---|---|---|---|---|---|
| **Plastiglas de México** (Chemcast GP catalogue, file modified June 2026) | Custom colour match | **60 sheets of 48"×96" at 0.118"**, or **one full pallet** for other sizes and thicknesses. Repeat orders: minimum production run | **$150 per colour** | ~2–3 weeks colour development. The colour bank is searched first to avoid development cost. **100% cancellation charge** once approved. Shipments ±20% for custom colours | [cc-cat] |
| Plastiglas de México | Standard colours in non-stock sizes/thicknesses (per-batch minimum run) | 48×96: 15 (1.5–12 mm), 8 (15–18 mm), 10 (24–32 mm), 6 (38–50 mm) sheets | — | "Rainbow pallets" of mixed standard colours allowed | [cc-cat] |
| **TAP Plastics** (Chemcast distributor) | Custom colour | **2,500 lb (one full pallet)** to start. Repeat orders need a minimum batch | **$350 per colour**, non-refundable | ~4–5 weeks. 100% cancellation charge | [tap-cc] |
| **Polyvantis (ACRYLITE)** | Soundstop GS / GS CC cell cast, catalogue colours, 15–25 mm | **2 full skids (~4,000 lb)** | — | Doc. 4081I, 04/26 | [ac-ss-pdf] |
| Polyvantis (ACRYLITE) | Soundstop XT extruded colours | 15,000 lb (US line) / 22,000 lb (German line) | — | — | [ac-ss-pdf] |
| **Plaskolite** (OPTIX, extruded) | Non-stock colour production | **3,000 lb**; **5,000 lb** for 0.500" colour; **10,000 lb** over 0.500"; Run-to-Size colours 3,000 lb | — | "Custom color matching available" | [pk-guide] |
| Plaskolite (OPTIX-L, continuous cast) | Non-stock colours | "may require a minimum quantity order". Pallet weight 2,000 lb | — | — | [pk-optixl], [pk-optixl-colors] |
| Reynolds Polymer | Custom colours, thin and thick | Not published ("special order") | — | — | [rp-thin], [rp-thick] |
| Spartech (Polycast) | Custom colours | Not published ("available upon request") | — | — | [sp-rod] |

**Derived (estimate):**
- 2,500 lb ≈ 12–13 sheets of 48×96×25 mm, or ≈ 26 sheets at 1/2" (93.6 lb each per [ep-2064-500]).
- The Plastiglas "60 sheets at 3 mm" option weighs ≈ 60 × 32 ft² × ~0.73 lb/ft² ≈ 1,400 lb. The 0.73 lb/ft² figure is scaled from ACRYLITE's 25 mm weight ([ac-ss-pdf]).
- EARF's ~2,500 lb assumption matches TAP's published Chemcast policy. Ordering directly under the Plastiglas catalogue terms may allow a smaller first pour at 3 mm.

---

## 8. Not verified / next checks

1. **Blocked sites:** TAP Plastics product pages, Acme Plastics, Professional Plastics and Interstate (interstateplastics.com) could not be read. TAP data rest on its PDF ([tap-cc]) and search excerpts ([tap-519], [tap-info]).
2. **ACRYLITE GP colours:** the public ACRYLITE product database lists only *Clear* for cast General Grade, 3–40 mm ([ac-db], [ac-gp]). I found no GP colour list. The coloured cast lines in the database are Soundstop GS, Satinice velvet cast (translucent, 6 mm) and aviation greys.
3. **Arkema/Trinseo Plexiglas G** colours (US): Piedmont still lists Plexiglas G literature ([pd-cast]), but I could not verify current US availability because the search quota ran out.
4. **LT basis and thickness behaviour** of Chemcast and TruCast: not stated. Resolve with the 1/8" vs 1/2" chips (§1.2, §5).
5. **Cast vs extruded** for 1020 Purple, 1300 Gold, 1450 Pink and 2120 Teal. Delvie's and ePlastics notes suggest some of these are extruded ([dv-img-1300], [ep-transp]).
6. **Reynolds:** the gauges in which 2064 and 2412 are stocked are not published ([rp-thin]).
7. **AC Plastics stock counts** are live and change quickly. Thick colours are often "Low Stock".
8. Pantone's own sRGB/hex values for the Chemcast Pantone references require a pantone.com login, so they are not reproduced.

---

## Appendix A. Photo-derived colour check (rough estimate)

**Method (estimate):**
- Source: Delvie's product photos, all taken in the same studio setup with a 1/8" sheet standing on a white surface ([dv-transp]).
- Measurement: the coloured shadow on the floor (light transmitted at an oblique angle) divided by the adjacent unshadowed floor, per linear-sRGB channel.
- Limits: camera tone curves and the oblique path make these numbers good for **hue only**. Lightness is not reliable, and some channels clip (2208, 2422).

| Stock colour | Photo | Photo-derived transmitted colour | L* / C* / hue° | Nearest EARF tint (hue°) |
|---|---|---|---|---|
| 2423 Red | [link][dv-img-2423] | #D4606F | 56 / 49 / 17° | Ember (59°): redder |
| 2422 Amber | [link][dv-img-2422] | #FFBD43 | 81 / 69 / 79° | Dust (83°): close hue, more saturated |
| 2208 Yellow | [link][dv-img-2208] | #FFF662 | 95 / 72 / 102° | Acid (99°): close hue, more saturated |
| 2092 Green | [link][dv-img-2092] | #0FC76D | 71 / 70 / 151° | Poison (126°): bluer |
| 2069 Light Blue | [link][dv-img-2069] | #83E5FA | 86 / 30 / 219° | Ice (237°): close |
| 2120 Teal | [Delvie's][dv-img-2120] | #00BCC6 | 70 / 39 / 205° | Ice: greener |
| 1020 Purple | [link][dv-img-1020] | #BC8DD9 | 66 / 45 / 315° | Haze (307°): **closest overall** |
| 3030 Glass Green | [link][dv-img-3030] | #FBFDFF | 99 / 1 / — | Fog |
| 2064 Light Grey | [link][dv-img-2064] | #A5A5A4 | 68 / 0.5 / — | Smoke (neutral) |
| 2074 Dark Grey | [link][dv-img-2074] | #8C8887 | 57 / 2 / 39° | Smoke (slightly warm) |
| 2370 Dark Bronze | [link][dv-img-2370] | #93837F | 56 / 7 / 39° | Smoke deep (warm) |
| 1300 Gold (extruded per photo) | [link][dv-img-1300] | #FFF6E6 | 97 / 9 / 88° | Dust: far too pale |

The ACRYLITE Soundstop GS images ([img-ruby], [img-topaz], [img-citrine], [img-amethyst], [img-sapphire], [img-emerald]) show 15–25 mm sheets. They are clipped renders, so they are useful only as qualitative hue references.

## Appendix B. Chemcast standard transparent colours, cross-referenced

LT values are at 0.118". The Plaskolite column is for its extruded OPTIX sheet, used as the industry tint reference.

| Code | Chemcast type | Pantone ref. ([cc-cat]) | Chemcast LT ([cc-cat], [cc-lt]) | TruCast TT ([tc-lt]) | Plaskolite OPTIX LT ([pk-guide]) | Röhm aviation equivalent ([ac-db]) |
|---|---|---|---|---|---|---|
| Clear | T | — | 91.90 | 93.0 | 92 | — |
| 2423 Red | T | PMS 186 C | 49.85 | 14.1 | — | — |
| 2422 Orange/Amber | T | PMS 1505 C | 85.80 | 59.1 | — | — |
| 2208 Yellow | T | PMS 109 C | 90.69 | — | — | — |
| 2092 Green | T | PMS 355 C | 78.74 | 18.6 | — | — |
| 3030 Green (glass) | T | PMS 331 C | 91.75 | 86.8 | — | — |
| 2069 Blue | T | PMS 2995 C | 85.53 | 57.6 | — | — |
| 2424 Blue | T | PMS 286 C | 48.11 | 10.4 | — | — |
| 2064 Gray | T | PMS 418 C | 57.07 | 29.3 | 27 | 7Y43: 27% |
| 2074 Gray | T | Black C | 35.49 | 11.7 | 13 | 7Y17: 14% |
| 2094 Gray | T | PMS 404 C | 72.25 | 48.7 | 45 | — |
| 2514 Gray | T | PMS 413 U | 86.64 | 60.7 | 58 | — |
| 2515 Gray | T | PMS 406 U | 85.77 | 69.1 | 75 | 7Y16: 76% |
| 2370 Bronze | T | PMS 412 C | 11.85 | 13.8 | 10 | — |
| 2404 Bronze | T | PMS 463 U | 79.58 | 59.5 | 49 | 7Y38: 33% |
| 2412 Bronze | T | PMS 462 C | 47.38 | — | 27 | — |
| 2538 | T (Chemcast: bronze) | PMS 448 C | 38.41 | — | 16 (Plaskolite: grey) | — |
| 2540 Bronze | T | PMS 406 U | 84.65 | — | 75 | — |
| 2283 Red | TL | PMS 485 C 2X | 37.32 | 12.3 | — | — |
| 2793 Red | TL | PMS 485 C 2X | 7.12 | 4.5 | — | — |
| 2157 Red | TL | PMS 186 C | 1.56 | 3.2 | — | — |
| L-032 / L-043 / L-089 / L-111 / L-116 | T fluorescent orange / yellow / blue / green / red, "indoor application only" | — | — | (TruCast 9092 76.5, 9093 92.9, 9095 34.5, 9097 77.6) | — | — |
| 2111 Green (TruCast) | T | — | — | 78.3 | — | 6Y32 (ref. 2111): 76% |
| 373 Purple (TruCast) | T | — | — | 7.4 | — | — |

---

## Sources

[cc-cat]: https://ppi-website2023.s3.us-east-1.amazonaws.com/media-library/chemcast-product-and-color-catalogue.pdf
[cc-lt]: https://www.eplastics.com/pdf/Chemcast%20LightTransmissionChart.pdf
[tap-cc]: https://www.tapplastics.com/image/pdf/Colors-Acrylic.pdf
[tap-519]: https://www.tapplastics.com/product/plastics/cut_to_size_plastic/acrylic_sheets_transparent_colors/519
[tap-info]: https://www.tapplastics.com/product_info/plastics_information/chemcast_info
[tc-lt]: https://www.acplasticsinc.com/wp-content/uploads/2026/08/Trucast-Acrylic-Light-Transmissions-5.26.26-1.pdf
[acp-api]: https://www.acplasticsinc.com/wp-json/wc/store/v1/products?search=TruCast&per_page=100
[acp-2423-125]: https://www.acplasticsinc.com/product/2423-125-48x-96-trucast-p-2/
[acp-2423-250]: https://www.acplasticsinc.com/product/2423-250-48x-96-trucast-p/
[acp-2423-375]: https://www.acplasticsinc.com/product/2423-375-48x-96-trucast-p-2/
[acp-2423-500]: https://www.acplasticsinc.com/product/2423-500-48x-96-trucast-p-2/
[acp-2422-375]: https://www.acplasticsinc.com/product/2422-375-48x-96-trucast-p-2/
[acp-2422-500]: https://www.acplasticsinc.com/product/2422-500-48x-96-trucast-p-2/
[acp-2208-375]: https://www.acplasticsinc.com/product/2208-375-48x-96-trucast-p-2/
[acp-2069-500]: https://www.acplasticsinc.com/product/2069-500-48x-96-trucast-p-2/
[acp-2111-375]: https://www.acplasticsinc.com/product/2111-375-48x-96-trucast-p-2/
[acp-2092-220]: https://www.acplasticsinc.com/product/2092-220-48x-96-trucast-p-2/
[acp-9093-500]: https://www.acplasticsinc.com/product/9093-500-48x-96-trucast-p/
[acp-9095-220]: https://www.acplasticsinc.com/product/9095-220-48x-96-trucast-p/
[acp-9097-220]: https://www.acplasticsinc.com/product/9097-220-48x-96-trucast-p-2/
[acp-373-220]: https://www.acplasticsinc.com/product/373-220-48x-96-trucast-p-2/
[acp-3030-500]: https://www.acplasticsinc.com/product/3030-500-48x-96-trucast-p-2/
[acp-3030-1000]: https://www.acplasticsinc.com/product/3030-1-000-48x-96-trucast-p/
[acp-3030-1000-48]: https://www.acplasticsinc.com/product/3030-1-000-48x48-trucast-p/
[acp-2064-375]: https://www.acplasticsinc.com/product/2064-375-48x-96-trucast-p-2/
[acp-2064-500]: https://www.acplasticsinc.com/product/2064-500-48x-96-trucast-p-2/
[acp-2064-750]: https://www.acplasticsinc.com/product/2064-750-48x-96-trucast-p-2/
[acp-2074-125]: https://www.acplasticsinc.com/product/2074-125-48x-96-trucast-p-2/
[acp-2074-500]: https://www.acplasticsinc.com/product/2074-500-48x-96-trucast-p-2/
[acp-2370-500]: https://www.acplasticsinc.com/product/2370-500-48x-96-trucast-p-2/
[acp-2404-500]: https://www.acplasticsinc.com/product/2404-500-48x-96-trucast-p-2/
[acp-2515-220]: https://www.acplasticsinc.com/product/2515-220-48x-96-trucast-p-2/
[acp-2793-500]: https://www.acplasticsinc.com/product/2793-500-48x-96-trucast-p-2/
[acp-2240-125]: https://www.acplasticsinc.com/product/2240-125-48x-96-trucast-p-2/
[canal-2064]: https://www.canalplastic.com/products/2064-gray-smoke-acrylic-sheet
[canal-2370]: https://www.canalplastic.com/products/2370-bronze-smoke-acrylic-sheet
[canal-3030]: https://www.canalplastic.com/products/3030-green-edge-acrylic-sheet
[canal-2423]: https://www.canalplastic.com/products/2423-red-transparent-acrylic-sheet
[canal-2422]: https://www.canalplastic.com/products/2422-amber-transparent-acrylic-sheet
[canal-2208]: https://www.canalplastic.com/products/2208-yellow-transparent-acrylic-sheet
[canal-2092]: https://www.canalplastic.com/products/2092-green-transparent-acrylic-sheet
[canal-2111]: https://www.canalplastic.com/products/2111-light-green-transparent-acrylic-sheet
[canal-2069]: https://www.canalplastic.com/products/2069-light-blue-transparent-acrylic-sheet
[canal-2120]: https://www.canalplastic.com/products/2120-teal-transparent-acrylic-sheet
[canal-1020]: https://www.canalplastic.com/products/1020-purple-transparent-acrylic-sheet
[canal-1300]: https://www.canalplastic.com/products/1300-gold-transparent-acrylic-sheet
[canal-5320]: https://www.canalplastic.com/products/5320-green-fluorescent-acrylic-sheet
[canal-5740]: https://www.canalplastic.com/products/5740-yellow-fluorescent-acrylic-sheet
[canal-clear]: https://www.canalplastic.com/products/clear-colorless-acrylic-sheet
[canal-swatch]: https://www.canalplastic.com/products/transparent-collection-swatch-pack
[canal-img-2423]: https://cdn.shopify.com/s/files/1/1408/9874/files/2423_Red_Transparent_sq_21f02f29-9e9b-44ba-a650-4f0817713c01.jpg
[canal-img-1300]: https://cdn.shopify.com/s/files/1/1408/9874/files/1300_Gold_Transparent_sq_a189ba96-6f63-49fd-b3a9-37fee87ec173.jpg
[canal-img-2111]: https://cdn.shopify.com/s/files/1/1408/9874/files/2111_Light_Green_Transparent_sq_517f1ed2-cafa-4722-b668-161aa8549ee3.jpg
[es-2423-125]: https://estreetplastics.com/product/1-8-x-48-x-96-transparent-red-plexiglass-acrylic-sheet-cast-2423/
[es-2423-250]: https://estreetplastics.com/product/1-4-x-48-x-96-transparent-red-plexiglass-acrylic-sheet-cast-2423/
[es-2064-500]: https://estreetplastics.com/product/1-2-x-48-x-96-transparent-gray-plexiglass-acrylic-sheet-cast-2064/
[es-2064-1212]: https://estreetplastics.com/product/1-2-x-12-x-12-gray-smoked-plexiglass-acrylic-sheet-cast-2064/
[es-2074-500]: https://estreetplastics.com/product/1-2-x-48-x-96-transparent-gray-plexiglass-acrylic-sheet-cast-2074/
[es-2074-125]: https://estreetplastics.com/product/1-8-x-48-x-96-transparent-gray-plexiglass-acrylic-sheet-cast-2074/
[es-3730]: https://estreetplastics.com/product/1-8-x-48-x-96-transparent-purple-plexiglass-acrylic-sheet-cast-3730/
[es-chipset]: https://estreetplastics.com/product/transparent-colored-plexiglass-sample-chip-set/
[es-chip-2423]: https://estreetplastics.com/product/sample-chip-transparent-red-plexiglass-2423/
[es-chip-2793]: https://estreetplastics.com/product/sample-chip-red-plexiglass-acrylic-2793/
[es-chip-2240]: https://estreetplastics.com/product/sample-chip-maroon-plexiglass-acrylic-2240/
[es-chip-3730]: https://estreetplastics.com/product/sample-chip-transparent-purple-plexiglass-dark-3730/
[ep-transp]: https://www.eplastics.com/plexiglass/acrylic-sheets/transparent-colors
[ep-colors]: https://www.eplastics.com/plexiglass/acrylic-sheets/translucent-colors
[ep-2069-375]: https://www.eplastics.com/ACRY20690-375PM48X96
[ep-2064-500]: https://www.eplastics.com/ACRY20640-500PM48X96
[ep-2074-500]: https://www.eplastics.com/ACRY20740-500PM48X96
[ep-set-transp]: https://www.eplastics.com/SAMPLE-ACRYTRANSPARENT
[ep-set-tint]: https://www.eplastics.com/SAMPLE-ACRYBRONZE-GRAY
[dv-transp]: https://www.delviesplastics.com/products/transparent-cell-cast-plexiglass-sheet
[dv-samples]: https://www.delviesplastics.com/products/acrylic-samples
[dv-img-2423]: https://cdn.shopify.com/s/files/1/0779/0438/0184/files/2423_Red_2_2.jpg
[dv-img-2422]: https://cdn.shopify.com/s/files/1/0779/0438/0184/files/2422_Amber_2.jpg
[dv-img-2208]: https://cdn.shopify.com/s/files/1/0779/0438/0184/files/2208_Yellow_2.jpg
[dv-img-2092]: https://cdn.shopify.com/s/files/1/0779/0438/0184/files/2092_Green_2_1.jpg
[dv-img-2069]: https://cdn.shopify.com/s/files/1/0779/0438/0184/files/2069_LightBlue_1.jpg
[dv-img-2120]: https://cdn.shopify.com/s/files/1/0779/0438/0184/files/2120_Teal.jpg
[dv-img-1020]: https://cdn.shopify.com/s/files/1/0779/0438/0184/files/1020_Purple_1.jpg
[dv-img-3030]: https://cdn.shopify.com/s/files/1/0779/0438/0184/files/3030_Glass_Green.png
[dv-img-2064]: https://cdn.shopify.com/s/files/1/0779/0438/0184/files/2064_LightGrey.jpg
[dv-img-2074]: https://cdn.shopify.com/s/files/1/0779/0438/0184/files/2074_DarkGrey.jpg
[dv-img-2370]: https://cdn.shopify.com/s/files/1/0779/0438/0184/files/2370_DarkBronze_1.jpg
[dv-img-1300]: https://cdn.shopify.com/s/files/1/0779/0438/0184/files/1300TransparentGoldExtrudedNote_34087922-a51b-473d-bed1-6f297c31dbd6.png
[usp-250]: https://www.usplastic.com/catalog/item.aspx?itemid=145285
[usp-kb]: https://www.usplastic.com/knowledgebase/article.aspx?contentkey=727
[ac-db]: https://www.acrylite.co/productdatabase/products
[ac-finder]: https://www.acrylite.co/products/product-finder
[ac-gp]: https://www.acrylite.co/products/brands/cast/general-grade
[ac-ss]: https://www.acrylite.co/products/brands/acrylite-soundstop/gs
[ac-ss-pdf]: https://www.acrylite.co/files/content/acrylite.co/documents/product-information/ACRYLITE-Soundstop-Colors-and-Availability-Product-Information.pdf
[ac-ext-lt]: https://www.acrylite.co/files/content/acrylite.co/00-global/documents/technical-product-briefs/ACRYLITE-Extruded-Light-Transmission-Reflectance-Information.pdf
[img-ruby]: https://www.acrylite.co/assets/images/4/Soundstop_3S02_GS-d7649d5b.jpg
[img-topaz]: https://www.acrylite.co/assets/images/5/Soundstop_2S01_GS-c5e50fd7.jpg
[img-citrine]: https://www.acrylite.co/assets/images/0/Soundstop_1S02_GS-5acdb822.jpg
[img-amethyst]: https://www.acrylite.co/assets/images/0/Soundstop_4S01_GS-a65c785f.jpg
[img-skyblue]: https://www.acrylite.co/assets/images/1/ACRYLITE-Soundstop-GS-Sky%20Blue-5S33-5989edc8.jpg
[img-sapphire]: https://www.acrylite.co/assets/images/1/Soundstop_5S09_GS-89803134.jpg
[img-emerald]: https://www.acrylite.co/assets/images/5/Soundstop_6S56_GS-df2d7804.jpg
[img-steelblue]: https://www.acrylite.co/assets/images/7/ACRYLITE-Soundstop-GS-Steel-Blue-5S31-516c0abc.jpg
[img-danish]: https://www.acrylite.co/assets/images/a/ACRYLITE-Soundstop-GS-Danish-Green-6S50-93c66794.jpg
[pk-guide]: https://www.plaskolite.com/docs/default-source/bro/bro068_psk_guide_us.pdf
[pk-optixl]: https://www.plaskolite.com/catalog/optix-l-colored/
[pk-optixl-colors]: https://www.plaskolite.com/docs/default-source/gpi/gpi071_opx_l_colors.pdf
[pk-cellcast]: https://www.plaskolite.com/catalog/optix-cell-cast-plazcast/
[pk-optixg]: https://www.plaskolite.com/catalog/optix-g-series-cell-cast-br-acrylic
[sp-rod]: https://www.spartech.com/media/documents/SPA201015-Rod-Color-Chart.pdf
[sp-rods-broch]: https://www.spartech.com/media/documents/SPA261012-Polycast-Rods-Tubes-Brochure-08.pdf
[sp-sc]: https://www.spartech.com/media/documents/SPA221040-Polycast-Solar-Control-Color-Selection-Guide.pdf
[rp-thick]: https://www.reynoldspolymer.com/commercial/r-cast-acrylic-thick-gauge-sheet/
[rp-thin]: https://www.reynoldspolymer.com/commercial/r-cast-acrylic-thin-gauge-sheet/
[pd-cast]: https://www.piedmontplastics.com/products/cast-acrylic
[pd-sf]: https://www.piedmontplastics.com/locations/san-francisco
[ld-cast]: https://lairdplastics.com/categories/acrylic/cast-acrylic.html

**Readable list of the main sources** (the same links as above):
- **Plastiglas de México / Chemcast:**
  - [Chemcast GP Product & Color Catalogue (PDF)][cc-cat], via [Piedmont's literature page](https://www.piedmontplastics.com/resources/literature/plastiglas-chemcast-gp-product-and-color-catalogue)
  - [Chemcast Light Transmission Chart (PDF, hosted by ePlastics)][cc-lt]
- **TAP Plastics:** [Chemcast custom-colour policy (PDF)][tap-cc]; [transparent-colour page][tap-519] (blocked; search excerpt); [Chemcast info page][tap-info] (blocked; search-result title)
- **AC Plastics:** [TruCast light-transmission chart (PDF)][tc-lt]; [public store listing of TruCast products][acp-api]
- **Polyvantis / ACRYLITE:** [product database][ac-db]; [Soundstop GS][ac-ss]; [Soundstop colours & availability (PDF)][ac-ss-pdf]; [extruded LT brief (PDF)][ac-ext-lt]; [cast General Grade][ac-gp]
- **Plaskolite:** [US product guide (PDF)][pk-guide]; [OPTIX-L Colored][pk-optixl]; [OPTIX-L colours (PDF)][pk-optixl-colors]; [OPTIX Cell Cast][pk-cellcast]
- **Spartech:** [rod colour chart][sp-rod]; [rods & tubes brochure][sp-rods-broch]; [SolarControl colour guide][sp-sc]
- **Reynolds Polymer:** [thick gauge][rp-thick]; [thin gauge][rp-thin]
- **Distributors:**
  - [Canal Plastics swatch pack][canal-swatch]
  - [eStreet chip set][es-chipset]
  - [ePlastics transparent colours][ep-transp]
  - [Delvie's transparent sheet][dv-transp]
  - [US Plastic 1/4" transparent][usp-250]
  - [US Plastic LT FAQ][usp-kb]
  - [Piedmont cast acrylic][pd-cast]
  - [Piedmont SF branch][pd-sf]
  - [Laird cast acrylic][ld-cast]: online listings show only clear cast, clear rod and OPTIX-L; colours require a branch quote.
