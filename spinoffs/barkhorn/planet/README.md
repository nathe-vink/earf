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

## Round 39: the house

*A proposal, written as the house would describe itself to a landlord, a licensing officer and a first hire. Numbers
marked (est.) are estimates; (unconfirmed) means a rule or fee I could not check against its source tonight. Every
choice is the owner's to overturn.*

### What it is

Planet EARF is a listening bar for 49 people, staff included, in a concrete shell in San Francisco: 104 m² (1,116 sq ft) of room, 6.1 m
across and 17 m deep, 3.4 m to the fir deck. It is EARF's showroom, run as a bar. Four Atmosphere speakers, the Hemisphere
North pendants, the Core lamps and EARF's Mantle record players are all for sale, and all swap tints, so the room is one
configuration of the catalogue on any given night (the house configuration is Smoke).

### From the door to last call

- **The door.** A plain blackened-steel door on the side street, a small etched disc for the name, no queue rope. Inside
  the door, the host stand: a dark-oak top on a steel post, and on it the bowl of EARFcoins. The host greets you, finds
  you a seat and puts one coin in your hand: "That's your song."
- **The bar.** Eight chairs at a zinc-topped racetrack counter with a fluted oak front. Behind it the back bar's record
  wall, the decks between the bar pair (raised on ledges at counter height, Ginza's way), and the request column. The
  Hemisphere North pendants hang low over the zinc; everything else is lit from what you can see.
- **The banquette.** Along the street wall, four small round tables and a chair opposite each, a Core lamp on every table,
  the frosted screens above (hands on fogged glass, the dancer, the Arrival-like shell).
- **The listening room.** Up one 200 mm step, behind the smoked partition: six low tub chairs facing the altar pair,
  side tables between. Quiet is the rule here (a card on each table says so, once). This is where the sessions happen.
- **Last call.** Called by the record, not by a bell: the selector plays the house's closing side (the same track every
  night, announced nowhere), the Hemisphere Norths come down a stop over its length, and the coins left in the column are played or
  returned with the bill.

### The listening programme

| | when | who plays | what it is |
|---|---|---|---|
| **Opening hours** | 5 to 8 pm | the bar staff | records from the house shelves, side by side; the coins start at 6 |
| **The Session** | Tue to Thu, 8 pm, about 50 min | the house | one album, start to finish, in the listening room, no talking; announced a week ahead; four of the six chairs booked, two kept for the door |
| **Selectors** | Fri and Sat, 9 pm to close | a guest selector at the decks | vinyl only, at bar level; the coins still play (the selector fits them in) |
| **Mother EARF Sunday** | Sun, 3 to 7 pm | a different guest each week | an afternoon of a person's records and why they own them; the one session with talking |

About 4,000 records to open with (the record wall's cells hold about 4,600 at 25 a cell; est.), vinyl only, bought for
the room: jazz, soul, ambient, Japanese city pop, dub, minimal and the West Coast. A shelf a month goes to the guest
selectors' picks.

### The coin ritual

- **One coin a guest**, handed over at the door. It is an EARFcoin: cast acrylic in one of the eight tints, the EARF
  globe on its face. The colour is random; nobody chooses.
- **A coin is a request.** Write the song on the house's small card, hand both to the bartender. The card goes on the
  rail at the decks, in turn, and the coin into the request column. The column is the queue: the selector plays the
  oldest card on the rail and takes the coin at the bottom, and anyone can see how long the wait is.
- **The coin comes back to the bowl** once its song has played. A guest who keeps it keeps it (it is on the bill at
  cost, est. $6 to $9). Lost coins are re-cast in batches.
- **The rules, kept short:** one request a guest a night; the selector may hold a request that would break a session;
  no requests in the listening room during the Session.

### The menu (a concept, short)

Drinks are named for the house's own words: the eight tints, the sides of a record, the parts of the system. About
twelve cocktails, a short natural wine list, two beers on tap, two non-alcoholic drinks given as much care as the rest.

| drink | what it is |
|---|---|
| **Smoke** | the house drink: mezcal and rye, stirred, over one clear cube |
| **Ember** | Campari, blood orange and sparkling wine, in a coupe |
| **Ice** | gin, dry vermouth and a drop of eucalyptus, very cold, up |
| **Fog** | a milk-clarified punch, crystal clear (the Fog tint: water-clear) |
| **Acid** | yuzu, shochu and soda, long |
| **Haze** | a violet highball: blanco tequila, butterfly pea, tonic |
| **Side A / Side B** | two small pours of the same spirit, two ages, side by side |
| **Needle Drop** | the bartender's choice for the record on now |
| **Mother** | a punch for four, from the bowl, Sundays only |
| **Run-out Groove** | the closing drink: an amaro and a short espresso |

Food is snacks only, bought in ready to serve (olives, rice crackers, a Japanese-style sando from a bakery nearby),
which a Type 48 bar may serve without a kitchen.

### Capacity, hours and sound

- **Capacity: 49 occupants, staff included** (about 45 guests and 4 staff; est. 28 seats: 8 at the counter, 12 at the
  banquette, 2 at the window table, 6 in the listening room, plus standing at the counter). Under 50 keeps the room
  Group B, with one exit and no Fire Department Place of Assembly permit (CBC §303, research.md). That rests on DBI
  accepting the seating plan's count: by area alone (15 sq ft net a person at tables) the room could count higher, so
  the plan goes to DBI first.
- **Hours:** Tuesday to Thursday 5 pm to midnight; Friday and Saturday 5 pm to 1:30 am; Sunday 3 to 10 pm; closed
  Monday.
- **Sound levels (targets, est.):** the bar at 60 to 65 dBA Leq while records play, so two people talk across a table
  at an ordinary voice (ISO 9921: normal speech is about 60 dBA at 1 m); the listening room at 78 to 82 dBA Leq in a Session, peaks to about 90; selector nights
  at 80 to 85 dBA at the counter. Outside, Police Code §2909 for a venue with a POE or LLP permit on commercial property:
  no more than 8 dBA, and 8 dBC in the bass, above ambient at the property line; 5 dBA if the building has homes; 45 dBA inside any home at night. Bass is the binding limit if there are flats above: no
  subwoofers until a measured site says so.

### The licences San Francisco needs for it

| licence or permit | who | why | notes |
|---|---|---|---|
| **Type 48, on-sale general (public premises)** | California ABC | spirits, wine and beer; 21 and over | San Francisco is closed to new and intercounty licences, so an existing SF licence is bought and transferred to the premises: about $75,000 to $150,000 (est.; NBC, 20 May 2026, quotes a broker at "around $100,000", sales as low as $70,000 to $85,000, down from about $250,000 in 2022); a public-convenience-or-necessity finding by the Board of Supervisors only in an over-licensed or high-crime tract |
| **Place of Entertainment permit** | SF Entertainment Commission | guest selectors to 2 am | application $2,579 for July 2024 to June 2025, $2,708 from July 2026, annual licence $863 in 2024 to 2025, indexed to inflation since (Ord. 193-24); a 30-day posted notice and a hearing |
| or **Limited Live Performance permit** | SF Entertainment Commission | selectors as a secondary use, ending by 10 or 11 pm | $612, the performance area at most 200 sq ft; Planning still counts the use as a bar; would end the selector nights early |
| **Building permit, tenant improvements** | DBI | the fit-out | light-transmitting plastics need a CC1 or CC2 classification and an interior-finish rating (CBC §2606): the frosted screens and the sink should be raised with DBI early. Mother EARF is likely a hanging combustible decoration under CFC §807 (a flame test, at most 10 % of the ceiling); cast acrylic burns, so it goes to SFFD as well as DBI |
| **Planning** | SF Planning | a bar, or Nighttime Entertainment | with a POE permit the use is "Nighttime Entertainment" (Planning Code §102), barred or restricted in many districts; with an LLP it stays a bar. Whether a conditional use is needed depends on the site |
| **Health permit** | SFDPH | glasswashing, ice, garnish prep; snacks | snacks bought in ready to serve keep food handling to a minimum (unconfirmed which category) |
| **Music licences** | ASCAP, BMI, SESAC, GMR | playing recorded music in public | needed even when no permit is: four licences, a few thousand dollars a year in all (est.) |
| **Business registration, seller's permit, sign permit** | Treasurer, CDTFA, Planning | | "First Year Free" runs to 30 June 2027 (Ord. 134-26): first-year City fees waived, the Entertainment Commission's included; state fees (ABC, CDTFA) are not |

### Fit-out budget (est.)

For the room as drawn, 1,116 sq ft, in a cold concrete shell with services at the street. National guides put bar
build-outs at $200 to $550 a sq ft and one San Francisco restaurant renovation at about $560 (web search, 2026-10-22;
anecdotal); this room sits at the top of that range because of its joinery, acoustic isolation and acrylic.

| | low | high | basis |
|---|---|---|---|
| Shell and services: HVAC, plumbing, power, sprinklers, the accessible restroom | $210,000 | $310,000 | $190 to $280 a sq ft (est.) |
| Acoustic isolation: the listening room's box, the ceiling absorber, door seals, the party walls | $60,000 | $110,000 | (est.) |
| Joinery: the racetrack counter (zinc top, fluted oak), the back bar, the record wall, the banquette, the altar | $120,000 | $185,000 | (est.) |
| Acrylic: four frosted screens with displays behind them, the Smoke sink, the request column, 300 coins, Mother EARF | $54,000 | $102,000 | research.md: no public price for thick cast acrylic; back-lit onyx runs $120 to $360 a sq ft installed |
| Lighting: Hemisphere North pendants, Core lamps, spots and their control | $35,000 | $60,000 | (est.; the companions at cost) |
| The system: four Atmosphere, amplification, two Mantle record players, a rotary mixer, cartridges | at EARF's cost | | not yet priced |
| Bar equipment: ice machine, glasswasher, under-counter refrigeration, an espresso machine, the bar die | $78,000 | $130,000 | (est.) |
| Furniture, glassware, the first 4,000 records | $70,000 | $120,000 | records at about $12 to $18 used (est.) |
| Design, engineering, permits and fees | $60,000 | $100,000 | about 10 % (est.) |
| Contingency | $103,000 | $168,000 | 15 % (est.) |
| **Fit-out, without the licence** | **$790,000** | **$1,285,000** | |
| Type 48 licence | $75,000 | $150,000 | NBC, 20 May 2026, a broker (est.) |
| Pre-opening and six months' working capital | $120,000 | $180,000 | (est.) |
| **All in** | **$0.99 M** | **$1.62 M** | |

Mother EARF (in the acrylic line above; drop it if not chosen) is about $9,000 to $12,000: main's 1 m globe in 25 mm clear tints is costed at about $6,500
one-off (round 33c), and sheet and polishing scale with area, so 1.3 m is about 1.7 times the sheet (est.).

### The pictures (the current heroes and details)

The owner, 2026-10-22: "Bar people: empty rooms, as round 39" and "Bar globe: the site's multicolour". Paths under
`renders/2026-10-22/barkhorn/`.

| frame | picture | from |
|---|---|---|
| hero: the room from the door, Mother EARF in the site's multicolour | `planet41/finals/door-mother-colour-p3.png` (2400 x 1600; also `-2400.jpg`, `-1200.jpg`) | round 41 p3 |
| hero: the bar counter | `planet39/proofs-p2/bar.png` (1200 x 800) | round 39 |
| hero: the listening room | `planet39/proofs-p3/listening.png` (1200 x 800) | round 39 |
| detail: the decks | `../2026-10-20/barkhorn/planet38/finals-best/coins-decks.png` | round 38 |
| detail: the door and the bowl of coins | `planet39/proofs-p3/bowl.png` (1200 x 800) | round 39 |
| detail: the shopfront at blue hour | `planet39/finals/street-final.png` (2400 x 1600; JPEGs beside it) | round 39 |

**Round 42 (2026-10-31), the house as a business:** four new interior views of the rendered room, each through three
critic rounds and a blind duel, in `renders/2026-10-31/barkhorn/planet42/finals/` (2400 x 1600): `night.png` (the room
at night, p2), `counter.png` (the counter, p1 with the floor's defect fixed), `shop.png` (the shop wall, p3) and
`listening.png` (the listening room, p1). Scores and every critic's words: `r42/critic/LOG.md`. The plan, the numbers,
the licences, the sites and the pop-up: `r42/README.md`.

The Smoke globe's door frame (`planet39/finals/door-mother.png`) and the empty door (`planet39/finals/door.png`) stay
for comparison. Scores and every critic's words: `r39/FINALS.md`, `r40/FINALS.md`, `r41/critic/LOG.md`.

### Mother EARF in the bar (an option)

The owner, 2026-10-22: "Also wondering if there's any opportunity to tie in Mother EARF."

**The owner's choice (2026-10-22): the site's multicolour.** Round 41 hangs round 33c's globe in its six tints, each
rim glowing its colour, no core, in the same place and size (`r41/r41_colour.py`; the door hero above). The Smoke
version below was the first proposal.

**The proposal rendered first:** Mother EARF is round 33b's one-colour globe made at architectural scale: the brand
globe's six slotted discs (three meridians and three parallels, the axis leaning 23.4 degrees) cut from 25 mm cast
acrylic in Smoke, 1.25 m across. Its faces are see-through smoked glass and its polished rims read dark. It hangs low
over a banquette table, 1.1 m above it and between two beams, under one hard spot on the deck behind it, so
its shadow draws the globe a second time, ring inside ring, on the bare concrete wall between the two frosted screens.
Round 33b's own text recommended exactly this: "a 1 m piece for the bar's back bar under a hard spot". Because it is
in the house's tint, it adds no colour to the room: the products stay the only colour. (`r39/kit39.py`, `mother`;
the frames `door` and `door-mother`, so the owner can compare.)

- **Why not over the listening room or at the hinge:** over the listening room the partition's header hid it from
  the door; at the hinge between the counter and the step, 9 m from the door, it read as nothing (both rendered,
  round 39 looks 2 and 5).
- **Its cost:** about $9,000 to $12,000 one-off (est.; scaled from main's 1 m piece in clear tints, about $6,500), and
  about 190 kg of acrylic in 25 mm at this size, 208 kg if the cast sheet runs 10 % thick (four great circles of
  4.91 m² and two ±40° parallels of 1.44 m², 6.35 m² × 25 mm × 1190 kg/m³; main's 160 kg at 1 m is sheet bought, offcut
  included): it hangs from the slab on a rated
  fixing, not from the fir deck, and needs an engineer. Cast acrylic burns, and CFC §807 may class it as a hanging
  decoration (a flame test, at most 10 % of the ceiling): the first question for SFFD.
- **Over a table, not a walkway:** its foot is 1.85 m above the floor, which is fine over a table and its banquette,
  not over the aisle.

**The multicolour variant, kept for comparison only** (`door-mother-colour`): round 33c's six tinted discs round a
glowing opal core, the rims lit. Rendered first (p1), it read as "a glowing multicoloured neon wireframe globe" to a
judge told nothing, and both critics called it a nightclub cue. The owner on colour: "I also don't love the overt
rainbow coloring. It's too Castro for SF" and "lots of acrylic features, just not rainbow everywhere". So it is not
recommended.

**Other ways the name could live in the bar, a sentence each:**

- **Mother, the house system.** The altar pair and the amplification are called Mother on the menu and the website,
  as clubs name their rigs; "on Mother tonight" is what the Session list says.
- **The coin's mother.** The bowl at the door is Mother EARF: every coin starts there and goes back there, and the
  host's line is "take one from Mother".
- **Mother EARF Sunday.** The one listening session with talking: a guest brings the records that raised them and
  says why (the programme above).
- **Mother, the drink.** A punch for four served from a bowl on Sundays, the only shared drink on the menu.
- **The mother tape.** Every record played in a night is logged, and the month's log becomes a printed sheet guests
  take home, "from Mother", the house's memory.
- **The sign.** The small etched disc by the door carries the globe, and the room's name under it reads "Planet EARF,
  under Mother", if the owner wants the globe kept out of the room itself.
