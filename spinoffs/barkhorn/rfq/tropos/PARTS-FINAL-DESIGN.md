# Tropos, the owner's final design: parts for a pair (2026-11-01)

**The design:**
- Strata: the stepped laminated horn, flush at 560, on bronze posts, with the caldera round the woofer;
- black voile sleeves;
- stock TruCast tints;
- on the stepped plinth lit from underneath.

**The base:** the Cloud's regenerated parts list (`out-cloud/bom.csv`, 2026-11-01, **$9,563.29** for 2, options
excluded). The Strata and plinth parts replace or add lines. Prices are prototype quantities, parts only: **before
tooling, labor, freight and contingency**. A line marked (est.) is priced with the kit's own rates (stock sheet $0.03 a
cm3, bronze $0.12 a cm3, plus $5 a part) on its blank, because the proposals' full build has not been run.

| | line | for 2 |
|---|---|---|
| | **the Cloud's parts list** | **$9,563.29** |
| − | the formed horn: `waveguide` 2 x $592.19, `horn-throat` 2 x $370.38 | −$1,925.14 |
| + | the laminated stepped horn, 22 layers of 1/2 in and the boss (`out-horn-options/bom.csv`, `horn-plan-b`, 2 x $1,482.62) | +$2,965.24 |
| − | the stainless posts (`post-1` to `post-4`) | −$130.40 |
| + | Strata's ø16 bronze posts and collars, turned (est.: about 130 cm3 of bar, turning) | +$150.00 |
| − | the cover and its ring: `cloth-disc`, `disc-frame`, `cloth-disc-magnets`, `woofer-ring` | −$212.54 |
| + | the caldera: three rings of 1/2 in a speaker, from 510 x 510 blanks (est.) | +$624.00 |
| − | the cabinet's own levelling feet (`feet`; the inserts stay, they take the plinth's bolts) | −$36.00 |
| + | the stepped plinth: three frames of 1/2 in a speaker, from 610 x 470, 640 x 576 and 670 x 680 blanks (est.) | +$876.00 |
| + | the plinth's feet, LED strip, Class 2 supply and controller (`levelling-feet`, `plinth-led`, `plinth-supply`, `plinth-controller`: $18 + $38 + $14 + $22 a speaker) | +$184.00 |
| | **parts for a pair, the final design** | **about $12,058 (est.)** |

**What this replaces:** the deck's "about $11,200 a pair" (the speaker lane's message of 09:42) was low by about
$860.
- That figure took the laminated horn at the formed horn's price with its tooling share (about +$70 a horn).
- Against the parts list, where the formed horn's tooling is a separate option, the laminated horn costs about $520
  more a speaker.
- **In return it needs no forming tooling.** The parts list's prototype tooling option, $6,925 (the plug, its base and
  the trim fixture), drops out.

**Not included:**
- the cabinet's 20 mm sheet in 2074 at 3/4 in. Smoke's cabinet is now 2074, stocked only to 1/2 in, so a mill run
  (`make/schedule.md`, the cash table);
- the bonding of the plinth's frames and the caldera, polishing and assembly (`make/assembly.md`);
- freight, duties and contingency.

## Horn A and the uplight (2026-11-03)

The owner, 03:00: "Horn: A, smooth, satin outside" (README 468c1058). The plinth's light now goes up through the speaker (the owner, 2026-11-02 and 04:27). The base is reopened (`variants/BASES.md`, "The base reopened"). Against the deck's **$20,700** for the first pair (stocked 2064 Smoke; `make/schedule.md`), whose cabinet and horn shops are about $7,750 ($3,750 and $4,000). Estimates.

| line, for the pair | change |
|---|---|
| the laminated stepped horn out (`horn-plan-b`, 2 x $1,482.62) and the formed horn in (`waveguide` and `horn-throat`, 2 x $962.57) | −$1,040 |
| the satin outside: masking the air path and a fine glass-bead blast, about $90 a horn | +$180 |
| the horn shop: the laminated horn's 22 layers, bonding, 5-axis air path and polish ($4,000) become forming, trimming, annealing and cementing, mostly in the parts' rates; the shop's fitting and finishing about $1,000 | −$3,000 |
| **the forming tool, once:** the prototype's tooling-board plug and base (`horn-tool-prototype`, `horn-tool-base`) | **+$6,925** |
| the first pair's Smoke horn in stock 2074 3/8 in (it reads at 0.48 of its cabinet), so no custom batch yet; the other seven tints need one each (`asset/TINTS.md`) | $0 |
| the uplight in place of the floor strip: $246 a speaker (the edge strips, channels, the 40 W board and heat sink, the controller, the 90 W supply) against the strip's $74 | +$344 |
| **the Tropos line, on the stepped plinth** | **about $24,100** |

**If the base becomes optional:**
- **On the slim light plate** instead of the plinth: the plinth's sheet ($876) and its bonding ($800) out, the plate's frame and tray in (about $328 a speaker): **about $23,100**.
- **On its own feet, with no base and no light:** the plinth, its bonding and its floor strip out: **about $22,000**, with the plate sold separately at about $570 a speaker.
- **The shops:**
  - The cabinet shop is unchanged at $3,750 (plus the plinth's $800 if it stays).
  - The horn shop drops to about $1,000.
  - The forming tool, $6,925, goes to a pattern shop, once. The production aluminium tool ($14,465) waits for orders.

**Weight a speaker** (the press sheet's 74 kg was Strata's stepped horn):
- **72.6 kg** with horn A on its own feet (`stability/standard-2018.md`; the render models' volumes and the parts list's masses). The formed horn is about 2 kg lighter than the laminated one.
- **The stepped plinth:** 10.4 kg more.
- **The slim light plate:** about 5.3 kg more.

## Detail pass (2026-11-12)

Finish and detail only (`make/detail-pass.md`, the coordinator's items A to H): no shape or size changes. From the
rebuilt parts list (`out-cloud/bom.csv`) against the one before. Estimates.

| line, for the pair | was | now | change |
|---|---|---|---|
| feet: stems and jam nuts black oxide, the swivel base black (`levelling-feet-black`) | 2 x $18 | 2 x $22 | +$8 |
| back screws: 24 M5 countersunk socket heads, black, flush (`back-screws-flush`) | 2 x $10 | 2 x $14 | +$8 |
| woofer screws: black ultra-low heads with the inserts (`m6-acrylic-inserts-low`) | 2 x $14 | 2 x $20 | +$12 |
| port rings: round, bonded, one polished chamfer (the frame's cut sheet) | $14.88 | $14.28 | −$0.60 |
| port screws: none, the rings are bonded | 2 x $5 | — | −$10 |
| rating: engraved in the back's flange, no plate, no screws (`rating-engraving`) | 2 x $10 | 2 x $4 | −$12 |
| terminals booted black (`push-on-terminal-black`) | 8 x $0.50 | 8 x $0.60 | +$0.80 |
| black braided PET sleeve on every lead (`braid-sleeve`) | — | 2 x $8 | +$16 |
| the IR receiver's cup, black cast acrylic (`ir-bracket`) | $37.43 | $37.67 | +$0.24 |
| **the pair** | **$9,563.29** | **$9,585.73** | **+$22.44** ($11.22 a speaker) |

- **Machining:** the 24 countersinks on the back's own CNC operation, and the bottom batt's pocket, channel and groove
  for the IR lead, cut with the batt. Neither adds a set-up.
- **The amplifier plate (G):** unchanged. It is the one bright bought part.
