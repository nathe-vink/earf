# Planet EARF, round 33: the den

The owner, 2026-10-19, on round 32's room (`../README.md`): "The bar is a little too sterile and open, and that much
space in SF is unlikely. It's gotta be cozier, including cozier, warmer lighting. I also don't love the overt rainbow
coloring. It's too Castro for SF."

The coordinator's reading, which this round follows: a real San Francisco storefront (about 7 m by 16 to 18 m, a ceiling
around 3.4 m, one long bar down one side, the listening corner at the back, about 30 seats); one storefront in an
ordinary building, with a recessed door and a transom; pools of warm light (2200 to 2700 K) with real dark between them;
dark wood, leather, brass, plaster, old brick, a heavy curtain at the door, a worn rug, books and records for clutter;
no rainbow, and colour only from a few speakers (Smoke and Fog read as part of a warm room, Ember or Dust as accents,
at most one cool speaker in any frame); and to keep the hi-fi listening bar, the record wall, the leather chairs, and the
speakers as the heroes of the frames that show them.

Status: **a proposal.** Every number is a working assumption for the owner to overturn. Round 32's room (the 18 x 9 m
corner storefront, the spectrum bar, the membrane's colour clock) is kept in `../` for the record; none of its finals
go anywhere.

<!-- VIEWS -->

## The room

You come in off the sidewalk into a recessed entry with a white mosaic floor, through a half-glazed door, and past an
oxblood velvet curtain. The room is 6.1 m (20 ft) wide and 17 m deep under a dark plaster ceiling. On the left runs the bar,
6.9 m of reeded walnut on an aged-brass kick, with an oiled walnut top, an oxblood leather armrest and a brass
footrail, under three spun-brass pendants. Behind it is the back-bar: walnut, an antique mirror, and three shelves of
bottles, each lit warm from a strip under its front edge. The Smoke pair stands in two walnut niches among the bottles,
the horns at a stool-sitter's eye, each lit by a pinhole against a softly glowing linen back. On the right, an oxblood
leather banquette, channel-tufted, runs under shaded brass sconces, with five walnut two-tops; Bell (Dust) on two of
them and candles on the rest. A round table sits in the window behind café curtains.

At the back, through a cased walnut opening with velvet curtains drawn to the sides, is the listening room. Old
brick is bare on the left wall; books run floor to 2.4 m on the right; walnut slats over absorber form the ceiling.
The record wall fills the back, with a walnut console in its middle (Cumulus small on it, a valve amplifier beside
it). The Ember pair stands either side on low walnut plinths, aimed at seven leather lounge chairs on a worn rug.

Outside: a three-storey Edwardian with bay windows over the shop. The shopfront is painted near-black brown, with a
panelled bulkhead, prism-glass transoms lit from inside, and EARF's wordmark in gold leaf on the window.

## Where things are

| | |
|---|---|
| `den_plan.py` | every dimension (metres; x into the room from the shopfront glass, y across from the right-hand wall) |
| `../../../../studio/engine/kit_ext/planet_den.py` | the room as one kit piece: shell, shopfront, bar, back-bar, banquette, lamps, listening room, record wall, street |
| `den_shots.py` | the views, the products placed, the room's lamps; `DEFAULT` the room's settings |
| `den_card.py`, `den_stage.py` | the blind critic's card and staging (critic/PROMPT-promo.md) |
| `den_sheets.py` | the plan and the long section, 1:50 on A3: `drawings/planet-earf-den-sheets.pdf` |
| `critic/` | every blind pass, verbatim |
| `../../../../renders/2026-10-19/barkhorn/planet33/` | the views, and `proofs/` |

    python3 spinoffs/barkhorn/planet/den/den_shots.py
    python3 studio/engine/render.py studio/shots/barkhorn/planet33/bar.json --out IMG --samples 48 --scale 0.5
    .venv-fab/bin/python spinoffs/barkhorn/planet/den/den_sheets.py

## Assumptions (each one the owner's to overturn)

- **Site:** a mid-block ground floor, 6.1 x 17.0 m (20 x 56 ft, about 1,120 sq ft; first drawn 7 m wide, narrowed so the aisle between stools and chairs is about 1.5 m, not 2.4), 3.4 m ceiling, brick party walls,
  flats above. The site's neighbourhood is unnamed and the street has no landmarks.
- **Capacity:** 29 seats (bar 10, banquette 10, window 2, listening room 7); occupant load 40, Group B, so no Place of
  Assembly permit.
- **Pairs:** two, not three. The Ember pair is the listening room's; the Smoke pair is in the back-bar. Round 32's Fog
  and Ice pairs are dropped. No cool speaker appears anywhere.
- **Bell** in Dust, as table lamps only (round 32's pendant Bell is dropped). The bar's pendants are plain spun-brass
  domes, not an EARF product.
- **The bar top is walnut, oiled and waxed**, not stone (round 32 used stone because spirits craze acrylic; there is no
  acrylic on the bar now). It needs re-oiling, and a stone top remains the low-maintenance alternative.
- **Acoustics:** soft and diffusing by default (velvet, leather, books, records, the rug, a slat ceiling over absorber),
  with no applied panels.
- **The scanned stand-ins** (Poly Haven CC0): bar stools `bar_chair_round_01`, dining chairs `dining_chair_02`, lounge
  chairs `mid_century_lounge_chair` in their own tan leather, and the street lamp. They are stand-ins, not a
  specification.

## What each choice costs

The permit and licence notes in `../README.md` ("What each choice costs") still hold: the Type 48 licence, the
entertainment permits for a DJ, Police Code §2909 on bass (binding here, with flats overhead), and Group B under 50.
What changes:

- **No back-lit acrylic** means no CC1/CC2 plastics classification and none of the $10,000 to $31,000 back-lit front.
  Walnut joinery (a reeded front, a back-bar, wainscot, a record wall, bookshelves, a slat ceiling) is the larger line.
- **Smaller:** about 38 % less floor area to lease and build out than round 32's 1,800 sq ft.
- **Velvet curtains and upholstery** need a flame-retardant (NFPA 701 / CA TB 117-2013) rating.

## The owner's open questions

- Is this the room: the size, the warmth, walnut and brass, brick at the back?
- Which pairs, and how many: Ember at the back and Smoke at the bar, or one pair only?
- A walnut bar top (oiled) or stone?
- The listening room's curtains: drawn for quiet sessions, open otherwise?
- People: no figures are in these views yet.

<!-- PASSES -->
