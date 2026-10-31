# Round 44 critic log: the lantern

| Round | View | Image | Stage 1 | Verdict | If fixed | Notes |
|---|---|---|---|---|---|---|

## Concepts (31 Oct 2026): two fresh critics, the boards only (`CONCEPTS.md`)

| Critic | (a) strata | (b) kit | (c) terrazzo | (d) lantern | Pick |
|---|---|---|---|---|---|
| 1, an architecture panel member | 7/7/5/5/8 | 5/5/7/4/4 | 4/8/3/3/7 | **9/7/8/8/9** | **d** |
| 2, an acoustician and operator | 7/7/5/5/8 | 5/5/6/4/4 | 4/8/3/3/6 | **8/6/8/8/8** | **d** |

The scores are, in order, architected / novel / lasting / realistic / cooler.

**Critic 1 on (d):** "the only concept where the hardest technical requirement (isolating a loud listening room from wood-joisted apartments) produces the identity rather than fighting it."

**Critic 2 on (d):** "the only concept whose big gesture is the acoustic answer the site needs anyway."

**Borrowings, by both critics:**
- From (b): the box bolted and demountable.
- From (a):
  - the deep slotted-oak absorber as a rear bass-trap wall;
  - the accessible seat on the sweet spot;
  - no tiers (critic 2: raised tiers put ears above the tweeter axis; steps in the dark are a liability).
- From (c): the acrylic-offcut terrazzo only as an accent where nothing wears it: Mother's plinth, plus the bar die (critic 1) or the shop threshold (critic 2). Taken: the plinth and the bar die.

**Risks named, and where they are designed out (DESIGN.md):**
- **Low-frequency flanking:** a floated floor on springs at 8 Hz or less, a lid that is never hung from the joists, a second line across the bar, a limiter.
- **Ventilation and heat in a sealed box:** the box's own fan coil, lined silencers, the LEDs serviced from outside the seal.
- **Width, flow and the door:**
  - a 1.52 m+ route;
  - the noisy kit at the shop end;
  - a two-door sound lock with power operators;
  - restroom plumbing outside the box.

## Renders, round 1 (p2; p1 was the p0 look, seen only by me)

| View | Critic | Stage 1 | If fixed | Verdict |
|---|---|---|---|---|
| street | a | 5.0 | 7.0 | iterate |
| street | b | 4.5 | 6.8 | iterate |
| bar | a | 4.5 | 6.5 | iterate |
| bar | b | 4.5 | 6.5 | iterate |

The full JSONs are in `p2-*.json`.

**Converged asks (all four critics):**
- The frame is exposed like a showroom, not night: frame median 69–106.
- The band reads as a clipped pink-white lightbox instead of amber through fins.
- The shelf and back-bar lines read as white neon.
- The lantern's face is washed flat: it needs a graze raking down the slats.
- Fill and route light flatten the room into even light with no pools.
- The terrazzo is too bright and coarse at 1:1.
- There are no signs of life.

**Two critics each:**
- The back bar is one bottle model cloned.
- The porch's oak reads as a smeared texture.
- The street camera's mullion cuts near the center.
- The oak reads mauve.

**Out of scope, named by the critics and left as they are:** the products' tints (fixed as placed). The Tropos and Mother EARF are not visible from the bar or the street; the lantern view shows them.

## Renders, round 2 (p3), and the duels against the earlier heroes

| View | Critic | Stage 1 | If fixed | Verdict |
|---|---|---|---|---|
| street | a | 5.0 | 7.0 | iterate |
| street | b | 4.5 | 7.0 | iterate |
| bar | a | 5.0 | 6.8 | iterate |
| bar | b | 5.0 | 7.0 | iterate |
| lantern (its round 1) | a | 5.0 | 7.0 | iterate |
| lantern (its round 1) | b | 4.5 | 6.8 | iterate |

**Converged asks:**
- The band is still pink and clipping (the 2800 K balance desaturates amber).
- The lantern has no visible foot line, so it does not read as freestanding.
- The baffle is the brightest flat surface.
- The shelf lines read hot.
- There are no pools of light on the counter.
- The ceiling and the right wall are voids.
- The street view has a black table slab on the axis and no glass in the frame.
- The rooms are empty, with repeated stools.
- In the lantern:
  - it is too bright and even;
  - the pair is darker than the walls;
  - Mother's spot washes her colored shadow white and shows a haze shaft;
  - the end-grain floor reads as camouflage;
  - the terrazzo chips are coarse;
  - the view is a flat, symmetric showroom.

**Out of scope, as the critics named it:**
- The products' tints compete with the band. The card fixes them, so they cap the one-color criterion.
- The Tropos are not visible from the bar or the street.

**Duels against the earlier heroes**, at the same size, both orders, using the duel prompt:

| Pair | Order 1 | Order 2 | Result |
|---|---|---|---|
| r41 door hero vs r44 street p3 | r41 (clear) | r41 (clear) | **r41 2–0** |
| r39 door hero vs r44 lantern p3 | r39 (decisive) | r39 (clear) | **r39 2–0** |

The judges read the earlier heroes as lived-in rooms (pendant and lamp pools, a record wall, a timber ceiling). They read r44 as murky or as a CG vignette.

As photographs, the round 39 and round 41 heroes still win. Those frames had five or more look rounds; these have had two.

## Renders, round 3 (p4): the last round for street and bar, the second for the lantern

| View | Critic | Stage 1 | If fixed | Verdict |
|---|---|---|---|---|
| street | a | 5.0 | 7.0 | iterate |
| street | b | **5.5** | 7.5 | iterate |
| bar | a | 5.0 | 6.8 | iterate |
| bar | b | 5.0 | 7.0 | iterate |
| lantern | a | 4.5 | 6.5 | iterate |
| lantern | b | 4.5 | 6.5 | iterate |

**Duels in both orders against the earlier heroes:**
- r41 door hero against street p4: r41 wins 2–0 (clear). The judges named murk and the ghost squares the glass reflects.
- r39 door hero against lantern p4: r39 wins 2–0 (clear). The judges said "CG product scene", citing the self-lit red cabinets and the neon globe.

**Converged asks left:**
- The band still reads salmon. The red-orange source, filtered by the Smoke fins, lands red, and AgX turns bright saturated orange-red pink. A yellower source (about #FFB040) and lighter fins are the fix. It was not made, because no round is left for street and bar.
- The glass reflections are flat squares: the opposite facade's unlit windows.
- The ceiling is a void.
- The bar top has no pools.
- The oak is uniform board to board.
- The terrazzo chips are coarse.
- The rooms are empty.
- The lantern view has these issues:
  - the cabinets glow flat red;
  - the floor pool is the brightest broad surface;
  - a blurred chair cuts the bottom edge.

**Out of scope throughout:** the products' tints, which compete with the band (the card fixes them), and the Tropos being invisible from the bar and the street.

## Finals

| View | Final | Critics | Against the hero |
|---|---|---|---|
| street | `finals/street-p4.png` (1200 × 800 proof) | 5.0 / 5.5 | r41 door wins 2–0 |
| bar | `finals/bar-p4.png` | 5.0 / 5.0 | not dueled (no bar hero at this angle) |
| lantern | `finals/lantern-p3.png` (p4 scored lower, 4.5 / 4.5) | 5.0 / 4.5 | r39 door wins 2–0 |

**The verdict, plainly:** the architecture won its own contest. Both concept critics picked it, and it is drawn, numbered and costed. The pictures of it did not beat the house's best pictures. The round 39 and round 41 heroes had five or more look rounds each; these have had two or three. The owner's next look at the lantern should be a picture pass in its own right:
- the band's color;
- real reflections in the glass;
- board-to-board oak;
- props;
- the lantern seen through its open porch from the bar, which shows the Tropos.

## Look 2 (the picture pass): round 1, p2 proofs

Look 2 changed the plan and the model (the in-line porch, the pair facing the door, a yellower band source, downlight lenses, per-board oak, a street, people), so the count restarts. p1 was checked before judging and fixed without a critic: the band at 0.3 still clipped to cream, the near guests read as mannequins, the lantern's near listener read as a dummy, the porch view at 24 mm was half door leaf. The critics judged p2 (`renders/2026-10-31/barkhorn/planet44/look2/*-p2.png`).

| View | Critic a | Critic b | Verdicts | If fixed |
|---|---|---|---|---|
| street p2 | 4.5 | 4.5 | iterate / iterate | 6.8 / 6.5 |
| bar p2 | 5.5 | 5.0 | iterate / iterate | 7.0 / 7.0 |
| porch p2 (new) | 3.5 | 4.5 | rethink / iterate | 6.5 / 7.5 |
| lantern p2 | 4.5 | 5.0 | rethink / iterate | 6.5 / 7.0 |

JSONs: `critic/L2R1-*.json`.

**Converged:**
- The band reads as a flat beige or gold lightbox. Both bar critics want it dimmer (0.05–0.06), both street critics want it more amber: the source color, not its level, is the fault.
- The figures read as translucent ghosts or mannequins at shutter 1.0. Three critics ask for a shorter shutter (0.15–0.35) with smaller movements, backs to the camera.
- The pair's covers clip pink while their bodies sit dark: wider, softer spots on the cabinets.
- Mother's spot lands as a hard white ellipse on the floor (all four lantern and porch critics).
- The right wall in the bar and street is a dead dark plane: scallops on the plaster above the banquette.
- The porch view shows mostly door jamb, with no bar and no band (both critics: pull back to the bar).

**Out of scope throughout:** Mother EARF's multicolored rims (a product as placed), the horn's reflections and the cabinets' edges (the speaker's geometry).

## Look 2: round 2, p3 proofs

p3 applied round 1:
- amber fins and a lower band source;
- wider, softer spots on the pair and on Mother;
- scallops on the plaster;
- the porch view from x 9.6 (at 8.8 the leaves of pair 2 cut the speakers);
- the porch shut in the bar and street views (the pair, seen cut by its jamb, broke the owner's whole-speaker rule);
- shutter 0.8 with smaller movements.

| View | Critic a | Critic b | Verdicts | If fixed |
|---|---|---|---|---|
| street p3 | 5.0 | 5.5 | iterate / iterate | 7.5 / 7.0 |
| bar p3 | 4.0 | 4.0 | iterate / iterate | 6.5 / 6.5 |
| porch p3 | 4.5 | 4.5 | iterate / iterate | 6.5 / 6.8 |
| lantern p3 | 4.5 | 5.0 | iterate / iterate | 6.5 / 7.0 |

**Converged:**
- **The figures:** every critic still reads them as mannequins. The bar critics prefer none, with signs of life instead.
- **The street band:** both street critics want it brighter and more amber, the brightest thing in the far room.
- **The bar band:** both bar critics want it dimmer, with edge light; the bar frame is orange throughout (WB 2750–2850).
- **The porch:** both critics find the porch soffit and the near leaf brighter than the room (graze down, route and fill down, the pair up).
- **The lantern:** both critics find the upper slat wall brighter than the speakers, the inner faces clipping, and Mother's plinth sunk.

The bar view lost its glimpse of the pair by closing the porch, and its score fell with it.
