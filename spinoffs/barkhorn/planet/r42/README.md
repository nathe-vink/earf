# Planet EARF, round 42: the house as a business

The coordinator, 31 October 2026, from the owner's words: "Keep going on whatever you can improve and bring to life ...
Spend the next 12 hours getting our probability of manufacturing and funding as high as possible, and establish EARF as
a world class brand." This round's lane is the bar: a real plan, the rules, the numbers, where, and better pictures.

Everything here is a proposal. Every dimension, price and choice is a working assumption for the owner to overturn.
Nothing has been reviewed by an architect, an engineer, a lawyer, a lender or the city.

| File | What it is |
|---|---|
| `plan42.py` | The house's geometry, in one frame: a 35 x 80 ft ground floor (2,800 sq ft). Also the occupant load (CBC Table 1004.5), with the option to get under 100, and the seat count. Everything below reads it. |
| `drawings/` | The drawing set on ARCH D sheets, as SVG with PNG previews and one PDF (`planet-earf-r42-drawings.pdf`): **A-000** the house in numbers, **A-101** floor plan, **A-102** reflected ceiling plan and lamps, **A-201** two sections, **A-301** axonometric. Built by `drawings42.py` (with `svg42.py`); the PDF and PNGs by `sheets42.mjs` through the pre-installed Chromium. |
| `axo42.py` | The axonometric: the plan built as a cutaway model in Blender (Cycles, orthographic). It writes `drawings/axo.png` and the label anchors. |
| `RULES.md` | San Francisco's rules and the permit path, a summary of `research-sf-rules.md`: which ABC licence, the Entertainment Commission, Planning, health, fire, building, plumbing and accessibility, and the critical path. |
| `NUMBERS.md` | Capex, opex, three revenue scenarios, the P&L, break-even, the levers and the financing, from `numbers42.py`. Also what the comparable bars show. |
| `SITES.md` | Three SF neighbourhoods and one in Oakland, with asking rents and why each fits. |
| `POPUP.md`, `popup42.py`, `popaxo42.py` | The bridge to the flagship, in two sizes: a lean 8-week pop-up inside Vacant to Vibrant's free rent ($22k to $36k), then a 5-month one ($130k to $210k). It includes the drinks route (a partner's Type 58 catering), what must exist by the 19 January 2027 debut in FOG week, and what each step proves. Drawing A-401, and the axonometric `drawings/popaxo.png`. Research in `research-popup.md`. |
| `research-sf-rules.md`, `research-market.md` | The research notes, with a source for every claim. Both are from public web pages; nobody was contacted. |
| `r42_shots.py`, `kit42.py` | New interior views of the rendered room (counter, listening, night, shop wall), and the shop wall as a kit piece holding the products' own models. |
| `r42_card.py`, `r42_stage.py` | The critic's card and staging for the new views (the CLAUDE.md protocol: fresh context, image and card only). |
| `critic/LOG.md` | The critic rounds, the duels and the finals: night p2, counter p1 (the floor fixed), shop p3, listening p1, at 2400 x 1600 in `renders/2026-10-31/barkhorn/planet42/finals/`. |

## Rebuild

    python3 spinoffs/barkhorn/planet/r42/plan42.py                       # areas, load, seats
    python3.11 spinoffs/barkhorn/planet/r42/axo42.py spinoffs/barkhorn/planet/r42/drawings/axo.png
    python3 spinoffs/barkhorn/planet/r42/drawings42.py
    D=spinoffs/barkhorn/planet/r42/drawings; node spinoffs/barkhorn/planet/r42/sheets42.mjs $D $D/A-*.svg
    python3 spinoffs/barkhorn/planet/r42/numbers42.py                    # the tables NUMBERS.md quotes
    python3 spinoffs/barkhorn/planet/r42/r42_shots.py && python3 studio/engine/render.py studio/shots/barkhorn/planet42/night.json --out IMG --scale 0.5

## What the round found

- **The order:** a lean pop-up (19 January to mid-March 2027, paid from the $50k product raise), then a 5-month
  pop-up, then the flagship (lease in spring 2027). Each step is paid for by the one before (POPUP.md).

- **The house:** 2,800 sq ft, 55 seats.
  - The code's occupant load is 133: A-2, sprinklered, two exits.
  - Option: 87, with the front room counted as the shop and the listening chairs fixed. That drops the sprinkler
    requirement.
- **The path:** buy a Type 48 (about $100k now, against about $250k in 2022) and take a Place of Entertainment permit for
  the selector.
  - About 8 months from lease where the uses are permitted outright.
  - About 11 to 12 months where a Conditional Use is needed. That includes late selectors in Hayes-Gough, because a bar
    with a POE is Nighttime Entertainment in the Planning Code.
- **The money:**
  - **To open:** about $2.0M (base).
  - **Base year:** revenue $1.65M, EBITDA about $123k, about break-even after a $620k SBA loan.
  - **Break-even:** 87 guests a night with the shop, 114 without.
  - **The lever:** the shop. One Tropos pair a month is worth more than ten guests a night. The comparables agree: Bar
    Shiru has never made a profit, and Gold Line shows a brand can run a bar.
- **Where:** SoMa's Folsom Street (1539 Folsom, an ex-bar at $27.25; its building for sale), else a smaller Hayes Valley
  space. Oakland Uptown is the cheap fallback.
