# Planet EARF: the listening bar, mocked up (round 32)

The owner, 2026-10-18: "start mocking up what Planet EARF will look like: My acrylic-laden listening bar in San
Francisco. Featuring EARF products, including speakers and lighting, as well as a custom-built, back-lit acrylic bar and
alcohol shelves, wall panels, etc."

Status: **a proposal.** Every number and every choice below is a working assumption, made so there is something to
look at; each is the owner's to overturn (the list is under "Assumptions"). The products are EARF's own, from their
CAD and untouched.

## Round 34: the owner's note, and the response

The owner, 2026-10-19, after round 33 (`den/`, a cozy walnut-and-brass den that answered "cozier, warmer, smaller, no
rainbow"):

> "For the bar I still want a lot of acrylic features, just not rainbow everywhere. The brick is unlikely to happen in
> SF, it's not common here. Cement walls, or cement looking walls would be cool, and I really like the idea of having
> wall screens behind large acrylic panels that could display certain things, like suggestive hands pressed up against
> fogged glass, the fogged silhouette of a woman dancing, alien/foreign objects like the movie arrival, etc. it's hard
> to mix acrylic into a space and have it not feel cheap though. My favorite interior designs are always lots of
> cement, some wood beams and features, and steal/iron features. Mixing acrylic into that tastefully is difficult.
> Might require a better rendering pipeline or critic for intimate listening bar space. Dimly lit too, but not to the
> point that it's hard to see."

The response, round 34 (`loft/`). It keeps the den's footprint: a 20 ft (6.1 m) frontage, 17 m deep, about 30 seats.

- **Materials:** board-formed concrete walls (a scan with tie holes and pour panels) and a polished concrete floor;
  reclaimed Douglas fir beams under a fir plank deck; blackened steel for the shopfront, the back-bar, the frames, the
  kick and the footrail. No brick anywhere.
- **Acrylic, neutral only:** water-clear, frosted or smoked, always thick (25 to 30 mm) and set flush in steel or
  concrete, so the one speaker in each frame stays the only colour. It appears as:
  - the screens;
  - a clear band inlaid along the bar top's front edge, lit from within;
  - clear back-bar shelves with polished, edge-lit fronts;
  - the niches' frosted backs;
  - frosted cylinder pendants;
  - a smoked partition at the listening room.
- **The screens:** large frosted panels set flush into reveals in the concrete, each with a glowing image 100 mm behind
  it, so the panel does the diffusing. They show hands pressed against fogged glass, an Arrival-like shell in fog, an
  ink-ring logogram, and the fogged silhouette of a woman dancing. The dancer is in a two-faced lightbox in the
  shopfront window, seen from the street and from the room. The images are `loft/screens.py`: shapes and shadows,
  never explicit.
- **A new critic for interiors:** `critic/PROMPT-interiors.md`. It judges whether the frame would pass as a photograph
  in a design magazine, against a reference board in words: Japanese listening bars, Ando's concrete, Kuramata's and
  Marcelis's acrylic, Brooklyn's listening rooms. Its explicit checks are premium acrylic, real concrete, timber and
  steel at 1:1, dim but readable (numeric floors), cozy, and one colour.
- **Pipeline:** scanned CC0 materials (Poly Haven and ambientCG), a thick-acrylic shader (rough transmission, volume
  absorption, polished edges), and modelled shades in place of IES profiles (none were to hand). The view transform was
  measured on the bar frame before choosing. AgX against Khronos PBR Neutral at the same exposure:
  - frame median 27.9 against 19.4;
  - crush 0.07 % against 0.98 %;
  - clipping 0 against 0.3 %;
  - blue median 19 against 2, so whites stay warm-white rather than orange.
  AgX is used. Round 32 left it for PBR Neutral because AgX bleached saturated panels, so the Ember frame is
  checked for that.
- **The products:** Fog at the bar and Ember in the listening room, as before. Bell is in Fog (opal white), so no frame
  carries a second colour.

<!-- VIEWS -->

## The concept

One long concrete room, lit by its own acrylic. You come in by a plain black door under one small neon sign and the
room opens down its length: on the left the bar, a single 8.4 m spectrum of eight back-lit panels in the Atmosphere
colours (Ember, Dust, Acid, Poison, Ice, Haze, Fog, Smoke), under a dark honed stone top; behind it the back-bar, its
bottles on edge-lit acrylic shelves that take the colour of the panel below them, with a Fog pair of speakers standing
among them in two lit niches 3.15 m apart, horns at a seated guest's eye. On the right, four upholstered booths along the long street
window, an Ember Bell on each table. At the far end, open to the bar, the listening lounge: ten
low chairs facing the record wall, an Ember Bell on each of its two side tables, an Atmosphere pair in each corner on low Smoke plinths (Ember in front, Ice either side
of the record wall), each grazed from behind in its complementary colour; the record wall runs floor to ceiling, its
cubbies of uneven depth a diffuser, the DJ desk set into it with Cumulus against a dim Ice glow. Overhead, the whole
ceiling is a back-lit acoustic membrane that keeps time: Fog and Ice at opening, Acid and Dust at sunset, Ember and Haze
late, a dimmed warm grey at last call.

What it borrows (`research.md` has the sources): the four-corner pairs of Brilliant Corners; All Blues' and Gold Line's
speakers among the bottles; Kuramata's back-lit acrylic and Eliasson's spectrum for the bar; Turrell's slow sequences for
the ceiling; Holl's complementary washes; Bar Martha's plain door. What acrylic demands: a stone top (spirits craze
acrylic), and no two acrylic walls facing (the slats go on one lounge wall only, over absorber; the ceiling absorbs).

## Where things are

| | |
|---|---|
| `plan.py` | every dimension of the room, in one frame (metres, x along the room from the door, y from the street window) |
| `../../../studio/engine/kit_ext/planet_room.py` | the room as one kit piece for the engine: shell, membrane, bar, back-bar, bottles, booths, lounge, record wall, street |
| `shots.py` | the views: cameras, the products placed (Atmosphere from `barkhorn-cloud`, Bell from `barkhorn-lamp`, Cumulus from `barkhorn-turntable`), the practical lights; `DEFAULT` the room's settings |
| `card.py` | the critic's card for a frame |
| `sheets.py` | the plan and the long section (A3, 1:50, the fab kit's sheet): `drawings/planet-earf-sheets.pdf` |
| `board.py` | the materials and lighting board: `drawings/board.pdf` |
| `critic/` | every blind pass, verbatim |
| `../../../renders/2026-10-18/barkhorn/planet32/` | the views (finals), and `proofs/` |

    python3 spinoffs/barkhorn/planet/shots.py                       # writes studio/shots/barkhorn/planet32/*.json
    python3 studio/engine/render.py studio/shots/barkhorn/planet32/door.json --out IMG --samples 64 --scale 0.5
    .venv-fab/bin/python spinoffs/barkhorn/planet/sheets.py         # the plan and section
    .venv-fab/bin/python spinoffs/barkhorn/planet/board.py          # the board

The products' render models are built first (they are not kept in git):

    .venv-fab/bin/python studio/fabkit/build.py spinoffs/barkhorn/cloud.py --out spinoffs/barkhorn/out-cloud --skip step,stl,drawings
    .venv-fab/bin/python studio/fabkit/build.py spinoffs/barkhorn/companions/turntable.py --out spinoffs/barkhorn/companions/out-turntable --skip step,stl,drawings
    .venv-fab/bin/python studio/fabkit/build.py spinoffs/barkhorn/companions/lamp.py --out spinoffs/barkhorn/companions/out-lamp --skip step,stl,drawings
    git checkout -- spinoffs/barkhorn/out-cloud spinoffs/barkhorn/companions/out-turntable spinoffs/barkhorn/companions/out-lamp studio/products

## Assumptions (the coordinator's and mine; each one the owner's to overturn)

From the brief:

- **Site:** a Hayes Valley corner storefront, 30 x 60 ft (1,800 sq ft), 14 ft to the slab, a concrete shell; one long
  street window (9.2 m here) and a plain door on the side street.
- **Capacity:** 49, Group B, so no Place of Assembly permit. **38 seats** (the brief's "about 40"): 12 at the bar, 16 in four
  booths, 10 in the lounge (two chairs that stood in front of the Ice pair were taken out in round 6).
- **Use:** quiet, kissa-style listening early, the bar staff playing records; a DJ at the record wall late.
- **Products:** two Atmosphere pairs in the lounge's corners on low Smoke plinths; a Fog pair in back-bar niches; Cumulus
  at the DJ desk; Bell over the bar and on the booth tables.
- **The bar:** eight 20 mm cast panels in spectrum order over a white liner and an LED cavity; a dark honed stone top.
- **Shelves:** 10 mm edge-lit light-guide acrylic, tinted for display, warm white on the working shelves.
- **Walls:** tinted slats over a dark absorber on one wall of each facing pair; the record wall as the diffuser.
- **Ceiling:** a back-lit micro-perforated membrane running the colour clock.
- **Entrance:** a plain door, one small neon sign.

Mine, where the brief left a choice open (all reversible in `plan.py` or `shots.py`):

- **Which pairs:** Ember in the lounge's front corners (warm, nearest the bar), Ice either side of the record wall; the
  Fog pair in the back-bar. Bell in Fog over the bar (each matching the Fog pair behind it), in Ember on the booth tables
  (the nearest pair); Cumulus in Ice (the pair beside it).
- **Bell over the bar** is Bell's shade, hub and strip hung on a cord, its foot and stem left off: a pendant version
  that does not exist yet.
- **The Fog niches' floor at 450 mm**, so the horns sit at a bar-stool guest's eye (about 1.5 m), as Gold Line flips its
  Altecs.
- **No screens** between the bar and the lounge. I first drew chest-high frosted Fog screens there (research move 12);
  in round 2 they hid the Ember pair and read as two brown boxes, so they came out (`plan.SCREENS = False` puts them
  back). The lounge is open to the bar.
- **The Fog niches** sit in the back-bar's third and sixth bays, 3.15 m apart (first drawn 5.5 m apart, at the bar's
  two ends, where no camera could hold both).
- **Bell on the lounge's two side tables** too, in Ember (the brief names the bar and the booth tables only): without
  them the low chairs were silhouettes.
- **The back-bar's display shelves take the colour of the bar panel below them**, bay by bay; its back panel is Fog
  white, softly lit, so the bottles read in silhouette.
- **Complementary washes** behind each corner pair (research move 11): Dust behind Ice, Ice behind Ember.
- **The DJ** stands in the room, facing the record wall, the desk set into it (a massive Smoke-clad block, the
  isolation Nowadays' booth gets from its mass).
- **Finishes:** the shell's concrete floor honed and sealed; the walls painted out dark; oxblood wool velvet booths,
  channel-tufted; black-stained oak cubbies; bronze footrail and window frames; bar stools and lounge chairs are
  scanned CC0 stand-ins (Poly Haven `bar_chair_round_01`, `mid_century_lounge_chair`), not a specification.

## What each choice costs (from `research.md`)

| choice | permits | money |
|---|---|---|
| **49 occupants or fewer** (Group B) | no Fire Department Place of Assembly permit; 50+ is A-2 assembly, a PA permit and possibly one guard per 100 | 40 seats at 49 caps the take; 50+ adds a permit and staff |
| **Records played by staff, early** | pre-recorded music indoors without a performer needs no entertainment permit | none |
| **A DJ, late** | a Place of Entertainment permit (to 2 am) or a Limited Live Performance permit (secondary use, to 10 or 11 pm): a 30-day posted notice and a hearing | permit fees (check whether "First Year Free" is still running past 30 June 2026) |
| **A bar on a Type 48 licence** | the licences are capped by county population, so one is bought secondhand; a transfer may need a public-convenience finding | roughly $150,000 to $500,000 or more |
| **Food-led instead** | a restaurant licence; in the Mission the only practical route (the Alcoholic Beverage SUD) | a kitchen |
| **Bass** | Police Code §2909: 8 dBA (and 8 dBC for permitted venues) over ambient at the property line; 45 dBA inside homes at night. Bass is the binding limit if there are flats above (this mockup draws some) | isolation, and perhaps no subwoofers |
| **Acrylic everywhere** | light-transmitting plastics need a CC1 or CC2 classification and an interior-finish rating (CBC §2606); raise the area of acrylic with DBI early | rated resins (3form Varia reaches Class A) cost more |
| **A back-lit bar front** | as above | no public price for thick tinted cast acrylic was found; back-lit onyx runs $120 to $360 per sq ft installed ($20 to $50 of it the backlighting), so 8.4 m x 0.96 m (87 sq ft) of back-lit front is a $10,000 to $31,000 benchmark before the acrylic itself |
| **A stone top, not acrylic** | | stone or glass; acrylic would craze under spirits |
| **The lit acoustic ceiling** | a stretch-ceiling permit as interior finish | Barrisol-class translucent membrane with absorber over 1,800 sq ft: get quotes |

## The owner's open questions

From the research, still open:

- the site and its size; homes above or beside it (they set the bass);
- capacity: 49, or 50 and over;
- the licence: a Type 48 bar, or food-led;
- etiquette: quiet, a DJ, or both by the hour; where the DJ sits (here: in the record wall);
- how many pairs, which colours, fixed or rotating for sale as a showroom; subwoofers or not;
- colour: all eight (as drawn), one dominant, or a room per colour; static, programmed (as drawn: the clock) or
  sound-reactive;
- whether EARF casts the bar panels and shelves itself, and the budget for acrylic and light;
- the records (how many, which genres, vinyl only) and the hours;
- whether Cumulus and Bell appear (drawn here), and whether a pendant Bell should be made.

New from the mockup:

- Is the spectrum bar the bar, or one colour (say Smoke, lit) with the spectrum kept for the back-bar's shelves? Every
  view shows how strongly the eight colours read.
- Should screens between the bar and the lounge come back (a quieter lounge, but they hid the Ember pair)?
- Should Bell have a pendant version (drawn here as its shade on a cord), and Bell on the lounge's side tables?
- People: no figures are in these views (no scanned people were to hand); every critic asked for some.

<!-- PASSES -->
