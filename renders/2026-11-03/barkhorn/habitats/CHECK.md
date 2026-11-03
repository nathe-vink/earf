# Habitats on horn A, blind four-test gate

Horn A is `tropos-strata.blend` from r33-speaker-horn 0936e6d: Strata's cabinet, the caldera, the bronze posts, and the
smooth formed horn, satin outside, with closed volumes.

The habitats are rendered by `spinoffs/barkhorn/biomes/habitats.py`, with:
- the speaker on its own M8 feet, settled onto the set, with base A and its uplight left out;
- the welded volume glass;
- `--horn-front`;
- the black flag and side cards;
- the speaker fills off and the light off by day.

Each is rendered at 1200 x 1500, with 96 samples for the dark scenes and 64 for the rest. Each image is checked blind
by a fresh agent that sees only that image (`scratchpad/check/PROMPT.md`).

Withdrawn: the first Ember (3de248cd) and Dust (c96fb96a) were rendered on the Cloud design, not horn A.

| Habitat | see_through | grounded | no_light_down | smooth_horn | Notes |
|---|---|---|---|---|---|
| Ember | PASS | PASS | PASS | PASS | Three-quarter view (rotate_z -5), crack_r on the speaker at 2.0, camera at 0.8 m. The woofer, frame, ports, braces and the side panel's frame show through, with lava through the side. The contact shadow is dark on dark and only just reads at phone size. A bright strip at the bottom right is lava light inside the side panel, not a spill. The dark disc in the horn is the driver seen through it. |
| Dust | PASS | PASS | PASS | PASS | Orange acrylic throughout: the woofer, its ring, braces, ports and the amp box show through. It stands on four short feet with faint contact shadows. The red streak in the shadow is sun through the tint, darker than the sand. The horn is smooth, with soft diagonal shading from the throat toward the corners and no X. |
