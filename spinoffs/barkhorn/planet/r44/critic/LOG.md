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
