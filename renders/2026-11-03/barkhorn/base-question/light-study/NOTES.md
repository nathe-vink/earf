# B's night light: what the real uplight reaches (2026-11-03)

The coordinator's gate on d5da71cb failed B (the plate, night):
- the glow is trapped in the port chamber;
- the woofer reads as a hole;
- a lavender patch on the right wall;
- the bottom panel's front edge blazes, with a pool on the floor.

These proxies test each cause at matched settings: 360 x 450, 24 samples, B's camera and grade. Numbers are mean gray levels (0-255) on fixed crops:
- edge: the bottom panel's front edge (max/mean);
- floor: the floor in front;
- wall: the right wall;
- port: the port chamber's lining;
- up: the upper chamber's back lining beside the woofer.

| proxy | edge | floor | wall | port | up | up / port |
|---|---|---|---|---|---|---|
| 1 as gated, moon fill on | 236/62 | 38 | 104 | 105 | 33 | 0.31 |
| 1, brace hidden | | | | | (side lining unchanged) | |
| 1, caustics on | | | | | (side lining +5) | |
| 2 moon off | 236/63 | 39 | 108 | 117 | 22 | 0.19 |
| 3 = 2, edge strips off | 236/60 | 31 | 48 | 95 | 19 | 0.20 |
| 4 = 3, panel aimed 40° | 224/33 | 18 | 0 | 125 | 35 | 0.28 |
| 5 = 4 at 60°, plus a 6 W strip on the brace | 225/35 | 23 | 0 | 154 | 59 | 0.38 |

## Findings

1. **The acrylic isn't trapping the light.** Hiding the first shelf (the brace, 20 mm clear acrylic) changes nothing, and the asset's volumes close (`spinoffs/barkhorn/asset/README.md`). The top is dark because it is far from a 40 W panel under the floor, behind the bottom batt and the woofer's basket.
2. **The lavender patch is the moon fill** (#C4D0F0 from the right), and the pale wall wash is the edge strips. Their 4000 K light leaves through the plate's frame and the walls' feet without crossing much tinted acrylic. With both off, the wall turns the speaker's own blue (3).
3. **The front-edge line is the bottom panel**, lit from below by the centre panel's wide spread. Aiming the panel (a louvre light-control film over its diffuser; area lamp of the same flux, 40° spread) halves the edge, cuts the floor pool, and nearly doubles the upper chamber against the port (4).
4. **The cost of aiming:** nothing leaves sideways, so the wall wash and the horn go black. The site's blue fan on the wall was light leaving the cabinet, which is the "out" the rule forbids.
5. **What it would take to reach the judges' 2× (up / port about 0.5):** a second source in the woofer chamber. A 6 W LED strip on top of the brace, aimed up, brings 0.38 (5); about 10-12 W there should reach 0.5. This is a design proposal for the owner, not a render setting.
6. **The woofer's face stays black** in every proxy. Nothing in the cabinet lights a forward-facing cone. Only the room can: a night photograph shows the cone only by the room's own light (a lamp, or the speaker's light off a near wall).
