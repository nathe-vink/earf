# Planet EARF, round 44: the lantern

**The owner, 31 October 2026:** "I mostly want to nail design, make it realistic, make it cooler … same with the bar. Make it well architected, novel, lasting."

This round redraws the bar as an architectural scheme that a contractor could price and an acoustician could take on. Everything here is a proposal. Nothing has been reviewed by an architect, an acoustician, an engineer or the city. *(est.)* marks my estimates; *(inference)* marks reasoning a source does not state.

**Files**
- `plan44.py`: the geometry and all the numbers.
- `kit44.py`: the model, used for both the renders and the axonometric.
- `drawings44.py` → `drawings/`: A-101 to A-401, plus the PDF.
- `r44_shots.py`: the rendered views.
- `CONCEPTS.md` and `critic/LOG.md`: how the idea was chosen.

## The idea

**The listening room's isolation becomes the building's one object.** A listening room under apartments has to be a room within the room. Here that inner room is a freestanding oak box: the lantern.
- It stands on its own floated floor at the end of the bar room.
- Its face to the bar is a slotted oak baffle, like the front of a loudspeaker cabinet.
- Under the ceiling, a 450 mm band of lit Smoke acrylic fins runs around its two visible faces, so the street sees a lantern at the end of a long dark room.
- Inside is a calm, tuned room: 20 seats, the Tropos pair, and Mother EARF on her plinth between them.

**Why this concept.** Four concepts went to two critics, each in a fresh context with the boards only (`CONCEPTS.md`). Both picked (d), the lantern:

| | well architected | novel | lasting | realistic | cooler |
|---|---|---|---|---|---|
| (a) the strata room | 7 / 7 | 7 / 7 | 5 / 5 | 5 / 5 | 8 / 8 |
| (b) the room as a kit | 5 / 5 | 5 / 5 | 7 / 6 | 4 / 4 | 4 / 4 |
| (c) offcut terrazzo | 4 / 4 | 8 / 8 | 3 / 3 | 3 / 3 | 7 / 6 |
| **(d) the lantern** | **9 / 8** | **7 / 6** | **8 / 8** | **8 / 8** | **9 / 8** |

One critic put it this way: the lantern is "the only concept where the hardest technical requirement … produces the identity rather than fighting it."

**What it takes from the other three.** Each borrowing was named by both critics.
- **From (b), the kit:** the box is bolted and demountable. The oak panels, the leaves and the lid are numbered panels, so the biggest investment can leave with the lease. Nothing else from the kit was taken: no grid and no infill system.
- **From (a), the strata room:**
  - The strata's deep absorber, as a 900 mm slotted-oak bass-trap wall at the back of the room, with a bench built into its face.
  - Its principle that **the accessible seat is the best seat:** the wheelchair space sits on the sweet spot.
  - The terraces were not taken. Raised tiers put ears above the speakers' axis, and steps in the dark are a liability in a drinking room.
- **From (c), offcut terrazzo:** the acrylic offcuts appear only as 15% of the chips in the terrazzo of Mother EARF's plinth and the bar's die, where nothing wears them. They are never in the floor's walking surface or on the bar top, because acrylic is only 3H pencil hardness.

## The shell

A typical San Francisco ground-floor storefront, drawn generic and fitted to whichever shell is leased:
- 25 ft wide inside the party walls and 80 ft deep (2,000 sq ft).
- 14 ft to the underside of a wood-joisted floor, with flats above.
- A slab on grade, a glazed front and a rear door to a yard.

Of the round 43 shortlist, 564 Market St (about 25 x 74 ft) and 311 Grant Ave (about 22 x 53 ft, which would need a shorter bar) are the nearest.

## The plan (A-101)

From the street to the back:

| Zone | x (m) | What |
|---|---|---|
| **Vestibule** | 0.9–3.2 | Two doors in series, 2.3 m apart (ADA 404.2.6: 48 in plus a 36 in leaf). It keeps street noise out and the room's sound in. |
| **Shop** | 0–6.1 (20 ft) | Oak shelves to 10'-6" on the left wall, lit along their front edges; a terrazzo window plinth; an oak and steel table with the till. |
| **Bar** | 6.1–13.0 (22'-8") | **The counter** runs along the left wall: a terrazzo die, a 30 mm honed quartzite top and a brass foot rail, with a 60 in accessible run at 34 in at its near end. **The back bar** is oak with three steel shelves. **The ice machine and glasswasher** sit behind a gasketed door in an alcove at the shop end, 6.5 m from the lantern. **Seating:** a leather banquette with four tables on the right, its back to the route. |
| **Porch** | 11.4–13.0 | A small oak sound lock outside the box's seal. Door 1 is off the route, door 2 is the box's own acoustic door set, and a 60 in turning circle fits between them. |
| **The lantern** | 13.0–20.9 (25'-11") | Inside it measures 7.30 x 5.34 x 3.40 m (24'-0" x 17'-6" x 11'-2"). **Layout:** the Tropos pair 2.80 m apart; Mother EARF on her plinth between them and behind their line; the selector's desk in the front corner. **Seats, 20 in all:** the wheelchair space and its companion seat on the sweet spot, then a row of six, a bench of eight in the trap, and two at the sides. The rug and loose lounge chairs complete it. |
| **Rear** | 20.9–24.4 | A lobby off the route; three single-user all-gender rooms, one with a urinal; a plant deck above them for the lantern's fan coil; the rear exit. |

**One straight route** runs 5'-4" clear down the right-hand wall from the front door to the rear exit. It is the accessible route, the exit access and the service corridor in one, and there is no level change anywhere.

| Number | Value | Basis |
|---|---|---|
| Gross area | 185.8 m² (2,000 sq ft) | 25 x 80 ft |
| Shop / bar / lantern (outside) / lantern (inside) / rear | 46.5 / 52.6 / 46.9 / 39.0 / 26.5 m² | `plan44.areas()` |
| Occupant load | **about 53**: shop 9 (60 sq ft gross), bar 24 (15 sq ft net), lantern 20 (its seats) | CBC Table 1004.5 |
| Exits | 2, about 24 m apart (front and rear) | CBC 1006.2.1: more than 49 needs two |
| Sprinklers | not required for the A-2 at fewer than 100 occupants (CBC 903.2.1.2); recommended in the lantern anyway (below) | |
| Seats | bar 20 (6 stools, 2 at the low end, 4 two-tops at the banquette), lantern 20 | |

The bar is smaller than round 42's 2,800 sq ft house (55 seats, a load of 133). This is the 25 ft grain the owner is likely to lease.

## Acoustics

### Reverberation

The target is **Tm = 0.25 (V / 100 m³)^(1/3) s**, measured from 200 Hz to 4 kHz, with ±0.05 s tolerance. The band may rise by up to +0.3 s at 63 Hz. The source is [ITU-R BS.1116-3](https://www.itu.int/dms_pubrec/itu-r/rec/bs/R-REC-BS.1116-3-201502-I!!PDF-E.pdf) §8.2.3.1 (02/2015). EBU Tech 3276 gives the same formula, within 0.2 to 0.4 s.

| | Value |
|---|---|
| Volume | 132.5 m³ |
| Tm (target) | **0.27 s** (0.22–0.32) |
| RT at 500 Hz, Sabine *(est.)* | **0.26 s**, in band |
| RT at 125 Hz, Sabine *(est.)* | 0.37 s, inside the low-frequency allowance |
| Proportions (BS.1116: 1.1 w/h ≤ l/h ≤ 4.5 w/h − 4) | l/h 2.15 between 1.73 and 3.07: **passes** |
| Floor area | 39 m², inside BS.1116's 20–60 m² for stereo |

**The treatment that gets there** (typical absorption coefficients, to be replaced by the acoustician's):
- **Side walls:** oak slats over 50 mm wool on 35% of the area, above a 1.2 m oak wainscot.
- **Lid:** oak slats over 100 mm wool on 70% of the area.
- **Back wall:** the 900 mm slotted trap across its whole width.
- **Floor and seats:** a 12 m² wool rug, and 24 people in upholstered chairs.

A 24-seat bar with people in it is not a reference room, so this is a design target, not a certificate.

### Bass

The axial modes are 23.5, 32.1, 47.0, 50.4, 64.2 and 70.5 Hz. The 47 and 50 Hz pair is the one to watch.
- **The back wall** is a 900 mm deep slotted-oak trap filled with wool, which is broadband down to about 40 Hz *(est.)*.
- **Corner traps,** 300–600 mm, in the two front vertical corners behind the selector's desk and the door.
- **The pair** sits 2.2 m from the front wall and 1.7 m from the side walls, symmetric about the room's center line.
- **Final placement** is by measurement after the box is built, with a house limiter.

### Isolation: the box in the box

**Floor.** The existing slab is sawn out 175 mm under the box. A 100 mm concrete slab sits on spring jack-up mounts at about 7 Hz, with end-grain oak on top, so it finishes flush with the bar's terrazzo. (One critic asked for 8 Hz or lower; pads alone are not enough.)

**Walls.** Two leaves, 300 mm overall:
- the oak skin;
- the band's 60 mm cavity;
- an outer leaf of 2 × 5/8 in gypsum on 3-5/8 in studs;
- 50 mm of air;
- an inner leaf of 2 × 5/8 in gypsum on 2-1/2 in studs with 50 mm wool;
- the oak slats inside.

A 60 mm gap runs to the party wall, with no rigid tie anywhere.

**Lid.** 200 mm CLT, 2 × 5/8 in gypsum, 100 mm wool and oak slats. It spans 5.34 m wall to wall on the box and is **never hung from the joists**. A 60 mm gap runs to the ceiling above.

**Penetrations.**
- **Doors:** two gasketed acoustic door sets with drop seals, door 2 through both leaves.
- **Air:** supply and return through lined silencers and flexible connectors at the back wall.
- **Power and signal:** through sealed sleeves.

**The band** sits wholly in the outer cavity, in front of a continuous outer leaf. Its LEDs and drivers are serviced from the route through removable outer fin panels, never through the seal.

**A second line over the bar and shop.** A resilient ceiling of clips, hat channel, 2 × 5/8 in gypsum and wool, finished in acoustic plaster at 13 ft. Comparable lab tests give STC 58–62 / IIC 50–56 under wood joists, about 5–10 points lower on site. That is not enough for bass; the box does that work. The bar's own system gets a limiter too.

Sources for the ceiling figures:
- [ClarkDietrich](https://www.clarkdietrich.com/node/1381): STC 58 / IIC 50, one layer, bare floor.
- [Kinetics](https://kineticsnoise.com/wave-hanger/testing-results.html): STC 60 / IIC 56, a vendor figure.

**The limits it has to meet** ([SF Police Code Art. 29](https://www.sf.gov/sites/default/files/2024-02/21_CACOSF_2023_Article29RegulationofNoiseGuidelines.pdf), PDF of 28 Sep 2023):

| Rule | Limit |
|---|---|
| §2909(b), for a place the Entertainment Commission regulates | no more than **8 dBC** above the low-frequency ambient |
| §2909(a)(2), inside a dwelling unit | no more than **5 dBA** above the local ambient, 3 ft from any wall, floor or ceiling |
| §2909(d), fixed sources such as the fan coil | **45 dBA** in a bedroom from 10 pm to 7 am, 55 dBA by day |
| §2901 interior ambient floors | ambient is never taken below **35 dBA** or **45 dBC** |

So the music in the flats at night has to stay under about **40–43 dBA and about 53 dBC** *(inference)*. The Entertainment Commission writes its own permit limits as dBA/dBC pairs at a set point, with a limiter ([EC memo, 6 Oct 2026](https://media.api.sf.gov/documents/10-6-26_Enforcement_Memo_for_Commissioners_vAWb27Q.pdf)).

- **Proposed house limit:** about 95 dBC Leq at the sweet spot, set by test *(est.)*.
- **The acoustician's model** must show the box's 31–63 Hz transmission. No lab number covers that range, since STC starts at 125 Hz.

### Quiet air

| Space | NC target | Air |
|---|---|---|
| The lantern | **NC 15–20**, near BS.1116's NR 15 | Its own fan coil on the plant deck, outside the box. Grilles in the lid at under 1.5 m/s face velocity; lined bends at both penetrations. Sized for 24 people plus the amplifiers and lighting, about 3 kW sensible *(est.)*. |
| The bar | NC 30–35 | Slot diffusers under 2 m/s. |

Sources: [Commercial Acoustics NC chart](https://commercial-acoustics.com/sound-advice/nc-rating-chart/), updated 22 Jul 2026; Price return-grille data: NC 16 at 400 fpm.

### The noisy kit

The ice machine and glasswasher sit in a gasketed alcove at the shop end of the back bar. That puts the whole bar between them and the lantern, and they are not on the box's structure. The dump sink and the speed rail stay at the bar.

## Structure and services

| Topic | Note |
|---|---|
| **Floor** | Sawcut and remove about 50 m² of slab to 175 mm; pour the floated slab on spring mounts. Check the subgrade and any slab reinforcement first. The epoxy terrazzo elsewhere needs the slab flat to ¼ in in 10 ft ([NTMA](https://ntma.com/tech-specs/types-systems/epoxy-terrazzo/)). |
| **The box** | Self-supporting. The CLT lid spans 5.34 m (200 mm CLT spans this comfortably *(est.)*, to the engineer). It adds nothing to the building's structure except its floor load on grade. |
| **Ceiling over the bar** | Its clips hang about 25 kg/m² from the existing joists. The structural engineer checks the joists. |
| **Plumbing** | Three rooms and the bar's sinks need trenches to the building sewer. The rooms sit at the rear, near where the lateral usually leaves. The bar's grease and floor sinks per SF Public Health. |
| **HVAC** | The bar's packaged or split units have condensers in the yard or on the roof, by the landlord's rules. The lantern has its own fan coil and an HRV for outside air (sized per the California Mechanical Code), on the plant deck over the rear rooms. |
| **Power** | Dedicated audio circuits (an isolated ground, kept away from the dimming); DALI dimming throughout; the band's drivers on their own circuit, serviced from the route. |
| **Fire** | Alarm, exit signs and emergency lighting. Sprinklers are recommended inside the lantern even if not required: it is a closed room of oak and wool, and the band's acrylic is a light-transmitting plastic under CBC Chapter 26, whose limits ease where a building is sprinklered. Run the sprinkler drops through flexible connections. Confirm the oak's flame-spread class (Class A or fire-retardant-treated veneer on the inner leaf). |

## Accessibility

- **Route:** 5'-4" clear from the door to the rear exit, with no steps anywhere. The lantern's floor finishes flush.
- **Doors:**
  - The vestibule's doors in series are 2.3 m apart.
  - The porch holds a 60 in turning circle.
  - Both acoustic doors get low-energy power operators with push plates, because gasketed doors exceed the 5 lbf opening force.
- **The bar:** a 60 in run at 34 in at its near end (CBC 11B-902.3; LA County's 2023 checklist: "a main counter 60 inches minimum in length").
- **The lantern** has one wheelchair space (30 x 48 in) and a companion seat ([ADA 2010 Standards](https://www.ada.gov/assets/pdfs/2010-design-standards.pdf)):
  - 221.2.1.1 requires one for 4 to 25 seats.
  - 221.2.3.2 Exception 1 waives vertical dispersion under 300 seats where the view is as good as the average.
  - 221.3 requires the companion seat.
  - The space is on the sweet spot, so it is the best seat in the room.
- **The rooms:** three single-user all-gender rooms (AB 1732), each with a 60 in circle (304.3), the WC 17 in off its side wall (604.2: 16 to 18 in) and grab bars.

## Fixtures

California Plumbing Code §422.1.1 counts fixtures at 50% male and 50% female, and single-use rooms count toward the total (§422.1.2).
- **Required** at a load of about 53 (the A-2 row as adopted elsewhere; [UpCodes](https://up.codes/s/fixture-count)): male 1 WC + 1 urinal, female 2 WCs, so **3 WCs + 1 urinal**, plus lavatories.
- **Provided:** three rooms, one with a urinal.
- **To confirm with SF DBI before design development:**
  - §422.2's "separate facilities for each sex", where all rooms are single-user;
  - whether the 2024 all-gender multi-user amendment reaches a private bar.

## Materials and finishes (chosen to last)

| Element | Material | Why it lasts | Care |
|---|---|---|---|
| Floor, shop and bar | Honed epoxy terrazzo, 3/8 in, marble and glass chips in a warm gray ground | Decades in restaurants; NTMA quotes $0.85/sq ft/year over 40 years | Neutral cleaner daily; reseal yearly; hone every 5–10 years |
| Floor, the lantern | End-grain white oak blocks, oiled, on the floated slab | Wears into a patina; re-sandable many times | Re-oil yearly; spot-sand |
| Bar top | Honed quartzite, 30 mm, eased nosing | Hard; honed hides wear | Seal every 6–12 months; test a sample for etching (lemon, vinegar) before buying |
| Bar die, Mother's plinth, window plinth | Terrazzo; the die and Mother's plinth with 15% acrylic-offcut chips | Vertical or untouched: no wear on the acrylic | As the floor |
| Joinery | Oiled white oak, fumed a shade; blackened steel | Repairable, re-oilable, ages warm | Re-oil touch surfaces yearly |
| The lantern's skin | Slotted oak baffle (60 mm battens, 12 mm slots), 140 mm boards on the route side | Bolted panels: replaceable one at a time | As joinery |
| The band | Cast Smoke acrylic fins, 20 mm on a 28 mm pitch, 60 mm deep, IOR 1.49 | Behind the oak line, out of reach; cast sheet keeps its color guarantee because it is cut flat, never formed | Dust twice a year with a damp microfiber (no solvents: they craze acrylic) |
| Walls | Lime plaster on the party walls | Breathable; patches invisibly | Limewash every few years |
| Ceiling | Acoustic plaster on resilient clips | Seamless; repairable | Repaint over its life only with the maker's acoustic paint |
| Seating | Oxblood leather banquette; mohair chairs and bench in the lantern | Leather and mohair outlast synthetics | Condition the leather twice a year; clean mohair professionally |

## Cost *(est., 2026 San Francisco, to be replaced by a contractor's)*

| Item | Low | High |
|---|---:|---:|
| Demolition, the slab cut under the box, trenching for the rear rooms | $25,000 | $45,000 |
| The lantern: floated floor on springs, double-leaf walls, CLT lid, the porch, two acoustic door sets | $150,000 | $260,000 |
| The lantern's oak: baffle, inner slats, the bass-trap wall, the bench | $45,000 | $80,000 |
| The acrylic band: about 15 m of cast fins, LEDs, drivers, hatch panels | $18,000 | $35,000 |
| Resilient ceiling over the shop and bar (about 120 m²), insulation, acoustic plaster | $35,000 | $60,000 |
| Shopfront: the vestibule, new glass, the entry alcove | $30,000 | $70,000 |
| The bar: counter, back bar, the kit alcove, underbar stainless | $70,000 | $130,000 |
| Shop and bar joinery: shelves, the shop table, the banquette | $45,000 | $80,000 |
| Floors: terrazzo (about 105 m²), end-grain oak | $35,000 | $65,000 |
| Three all-gender rooms and plumbing | $55,000 | $90,000 |
| HVAC: the bar's units, the lantern's fan coil, silencers, lined ducts | $70,000 | $130,000 |
| Electrical, lighting, controls, audio power | $55,000 | $100,000 |
| Fire: sprinklers, alarm | $25,000 | $60,000 |
| Design fees: architect, acoustician, structural and MEP engineers, testing | $90,000 | $150,000 |
| **Subtotal** | **$748,000** | **$1,355,000** |
| Contingency (10% / 15%) | $74,800 | $203,250 |
| **Total** | **$822,800** | **$1,558,250** |
| **Per sq ft, all in** | **$411** | **$779** |

**Benchmarks.**
- Restaurant tenant improvements run $200–480 per gross sq ft in hard costs, plus 30–40% soft costs ([Terrapin CG 2026](https://terrapincg.com/news/average-cost-to-build-high-end-restaurant)).
- Northern California in-line retail runs about $211/sq ft (Cushman & Wakefield 2025, secondary).

**What's extra.** The lantern accounts for about $210k–375k, roughly a quarter. The box is the one room nothing in a normal bar build prepares for.

**What it saves.** It is demountable, so at the next site it is re-erected rather than rebuilt: a new floor cut, the services and the reassembly, about a third of its first cost *(est.)*.

These figures replace round 42's construction line, which was $560k–$1.26M for 2,800 sq ft. They do not include the license, the sound system, the products, furniture or pre-opening.

## Maintenance (what keeps it looking new in ten years)

| When | What |
|---|---|
| Daily | Terrazzo: neutral cleaner. Bar top: wiped dry. |
| Monthly | Check the acoustic doors' seals and the power operators. Clean the HVAC filters. |
| Twice a year | Dust the band through its hatch panels. Condition the leather. Seal the bar top as its test shows. |
| Yearly | Re-oil the oak touch surfaces and the end-grain floor. Re-measure the lantern (RT, the limiter's level at the flats). Service the springs' inspection points. |
| Every 5–10 years | Hone the terrazzo. Re-sand the end grain. Re-limewash the walls. |

## Risks and next steps

1. **Hire an acoustician at schematic design.** Fix numeric targets in the contract and test before and after the fit-out.
2. **Go to DBI before design development,** with questions on:
   - fixture counts and all-gender rooms;
   - the band's plastic (CBC Chapter 26) and the interior finish class of the oak;
   - whether the lantern is sprinklered.
3. **Get the structural engineer's view** on the slab cut, the floated slab, the CLT lid and the joists carrying the resilient ceiling.
4. **Settle the band's tint.** The renders use the house's Smoke, warm and quiet at rest. The owner may want it to change in service. Make a 1 m mock-up with the chosen sheet and measure its transmission; A&C's TruCast table is the starting point.
