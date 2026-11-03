# Core's ball: the frost and the options (design note, 2026-11-03)

**A note for the owner's decision. Nothing in the CAD changes until the owner chooses.** It answers the coordinator's
gate on round 7, where Core failed the glass test 3/3 on both frames:
- **By day:** it read as "milk glass, lacquered plastic", with the silhouette lighter, not deeper.
- **At night:** it read as "a flat cyan disc".

Mantle has the same finding.

**The proxy pair:**
- `renders/2026-11-03/barkhorn/lamp-pictures/core-ice-day-nested.png`
- `renders/2026-11-03/barkhorn/lamp-pictures/core-ice-night-nested.png`

Both are at 0.6 scale, rendered by `lamp_pictures.py` (variant `nested`). They show option B beside the frosted ball as
drawn today (`core-ice-day.png`, `core-ice-night-frost.png`).

## Is it inherent to the frost?

Yes, for any frost on the ball's own wall.

**By day:** the frost is the first surface that scatters light. It sits 9 mm behind the polished face of a 160 mm
ball, too close to read as depth. So the eye takes the frost for the ball's surface: a pale, even skin under a clear
gloss. That is what milk glass and lacquer look like. A finer or coarser blast changes how milky it looks, not the
fact.

**At night:**
- A frosted sphere lit from inside sends out about the same light at every point and in every direction, so it shows
  no depth cues: it reads as a flat disc.
- The gradient that does show is the LED's near field, a bright cone at the base just above the window.
- The clear outer 9 mm adds only a thin rim, which reads as a ring, the "seam".

## The options

| | A. Frosted inside (today) | B. Ball in a ball | C. Lower half frosted | D. Finer frost |
|---|---|---|---|---|
| What it is | 9 mm tinted ball, its whole inside bead-blasted | a 6 mm tinted outer ball, clear and polished both faces; inside it, across a clear air gap, a Ø90 clear diffuser ball, 3 mm, frosted inside, seated on the grommet's ring | today's ball, blasted only below the equator | today's ball, a fine glass-bead blast |
| By day | milk glass (the gate) | real depth: a tinted glass ball with a pale sphere floating low in it (the proxy) | the top half reads as glass; the lower half reads as a frosted bowl inside it, a "fill line" | slightly glassier, still a frosted skin |
| At night | an even, flat disc; a cone at the base | a glowing core inside dark tinted glass; the outer ball catches the glow at its rim (the proxy) | the LED shines straight up through the clear top: a hot spot on the ceiling, and the LED die visible from above or from a seat beside it (glare) | less diffusion: the cone at the base grows and the top dims; the LED shows as a bright blob |
| Can you see the emitter? | no | no: the inner frost hides it | **yes, from above** | partly: a bright blob at the base |
| Cost a ball [E] | about $47 (the BOM's shell) | about $55 to $70: the outer ball about $33 (447 of 634 cm3), the inner $15 to $25 formed (or a stock Ø90 clear sphere pair, [check] supplier), $5 to $10 to fit and join | +$3 to $5 (masking for the blast) | $0 |
| Tooling [E] | the $1,500 mould | the same outer mould [check with the former: the 6 mm wall must form on the 9 mm wall's mould, i.e. a female mould setting the outside], plus about $1,200 for the inner's mould, or $0 with stock spheres | none | none |
| Weight | 754 g ball | about 620 g (532 + 85) | 754 g | 754 g |
| Risks | the gate's finding | the outer's equator joint is now seen against the glow: a polymerised joint, turned and polished, must be judged on the first sample; dust in the gap (the port's grommet seals it; the gap is closed for life) | glare; the masked line must be crisp | doesn't fix the finding |

### B in detail (the proxy)

- **Outer ball:** R 80 outside, R 74 inside, polished both faces. Two halves formed from 6 mm tinted cast and joined
  at the equator as today, with the 40 port below.
- **Inner diffuser:**
  - A clear acrylic ball, R 45 outside and 3 mm thick, bead-blasted inside. The frost faces air, so it scatters.
  - It sits on the grommet's upper ring, its center about 31 below the outer's (27.8 in the proxy, drawn on the 9 mm
    wall's grommet). Its gap to the outer wall is about 24 at its equator, closing to about 3 at the seat.
  - It is captive once the outer halves are joined round it. Each color ball carries its own inner (+$15 to $25), so
    swapping balls by hand is unchanged.
- **The LED** stays where it is, under the window. Its light reaches the room only through the inner frost and then
  the clear tinted wall. The glow comes from the core, and the tint is seen as clear glass around it.
- **Color:**
  - The outer wall is 6 mm, not 9, so at the "held" loading Ice reads a little paler by day.
  - Deep tints gain depth.
  - The earlier two-layer option (a clear outer and a tinted inner 1 mm apart, `out-orb-table/bom.csv`) keeps the
    frost 1 mm behind the surface. It would still read as milk glass, so it is not an answer to this finding.
- **Not proposed: B with the inner kept on the base.** The inner diffuser could stay on the base, with one per lamp
  and only the outer swapped. That needs the port opened from Ø40 to about Ø92, against the cup's contact at r 50. That
  is a change to the drawn base and cup, so the owner decides.

### Fixes made regardless (round 8, on the frosted frames too)

- **The pin-dot:** it was round 5's window glint in the outer gloss. It is gone.
- **The hotspot cone:** the LED is now modeled as a Lambertian disc the window's size, not a 160-degree spot. It is
  weaker but still there in A: it is the frost's near field over the LED, inherent to A. B moves it inside the core.
- **The seam-like ring:** this is the clear outer 9 mm of A seen edge-on, inherent to A. In B, the boundary is the
  real gap between the two balls.
- **The dark nub at the right edge:** a refraction of the room through the silhouette (sub-millimeter, at the
  grazing edge). It is to judge in the new frames.

## Recommendation

**B, the ball in a ball:**
- It is the only option that fixes both frames without showing the LED.
- It costs about $10 to $25 a ball and up to $1,200 of tooling.
- It weighs less.
- It keeps the hand swap.

**The one risk to judge on a sample:** the outer ball's equator joint, now seen against the glow.

**C is not recommended:** it puts the LED in view.

**D is not recommended:** it doesn't change the finding.
