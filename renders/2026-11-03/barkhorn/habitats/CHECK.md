# Habitats on horn A, blind four-test gate

Horn A is `tropos-strata.blend` from r33-speaker-horn 0936e6d: Strata's cabinet, the caldera, the bronze posts, and the
smooth formed horn, satin outside, with closed volumes.

The habitats are rendered by `spinoffs/barkhorn/biomes/habitats.py`, with:
- the speaker on its own M8 feet, bedded 12 mm into the ground (the sets' displacement is invisible to the ray cast), with base A and its uplight left out;
- the welded volume glass;
- `--horn-front`;
- the horn polished since 15:14 (the owner: roughness 0.05 outside, `--horn-rough 0.05`); rows marked (satin) were rendered before that;
- the black flag and side cards;
- the speaker fills off and the light off by day.

Each is rendered at 1200 x 1500, with 96 samples for the dark scenes and 64 for the rest. Each image is checked blind
by a fresh agent that sees only that image (`scratchpad/check/PROMPT.md`).

Withdrawn:
- the first Ember (3de248cd) and Dust (c96fb96a) were rendered on the Cloud design, not horn A;
- Ember fa1271ef and Dust 426996f1 stood over displaced ground with a gap under the base (the coordinator's gate).

| Habitat | see_through | grounded | no_light_down | smooth_horn | Notes |
|---|---|---|---|---|---|
| Dust (polished) | PASS | PASS | PASS | PASS | Sand bounce 0.35, no tumbleweed, 64 samples. Amber-red acrylic: the woofer, ring, braces, ports, crossover box, its screws and the desert behind show through. The rail sits on the ripples: luma 81 under the front edge against 107 for open sand. The contact shadow is weak. The red patch is the tinted shadow. The horn is a smooth glassy shell, with the driver showing as a smooth bulb and no X. |
| Ember (polished, turned) | PASS | PASS | PASS | PASS | rotate_z 12 (10 deg off the camera line), crack_r 2.0, camera at 0.8 m, 96 samples. Crease 8.3 / 4.3, left and right of the driver (`flare.py`; Dust 7.8, Ice 7.2): the sky wedge is gone. The 12 o'clock ring glint is gone (red max 233 -> 62). The woofer, braces and ports show through, and the lava through the side. Contact: luma 12 under the base against 26 beside it. |
| Acid (polished, 4 deg off) | PASS | PASS | PASS | PASS | rotate_z -8, sink 0.03 (18 mm into the puddle), 64 samples. Crease 5.9 / 10.8 (Dust 7.8, Ice 7.2; it was 26.7 at 28 deg off). The woofer, frames, braces, ports, posts and screws show through. The reflection starts at the base edge. The horn is smooth, with very faint creases invisible at phone size. |
| Fog (polished, reframed, real cards) | PASS | PASS | PASS | PASS | Camera 0.30 m lower (lens rise 0.18), azimuth -10, f/4. rotate_z -5 (5 deg off; at 20 deg off the side face read as a cream sheet, see held/). The sun neutral white at 110. Real flag and card: the sun-side card left out, the other out of frame at 2.2 m. 96 samples. Crease 1.9 / 2.3 (Dust 7.8, Ice 7.2): the whole horn on plain sky. The left cut-edge strip is still warm, b* median 9.7 (p90 17.2) against the sky's -3.6; the target was 5 or less. Clear: the woofer, braces, posts, ports and the terminal block, with the grass and rock behind, show through. |
| Haze (polished, sun front side, real cards) | PASS | PASS | PASS | PASS | Sun 70, 6 deg up, the HDRI turned to 338.8, the set's sun disk at 70 (all out of frame). rotate_z -10 (5 deg off), lens rise -0.13, a 4 x 3 m real flag, the sun-side card left out and the other out of frame at 2.6 m. 96 samples. Upper box max channel 47.5 (target 45-60). Horn to box 2.8x. Horn and box hue both 239. Crease 6.1 / 7.3. The woofer, ring, braces, ports and the block show through the front, and the hills through the side. |
| Ice (polished, real cards) | PASS | PASS | PASS | PASS | It replaces 27911a44, whose reflect-only cards sat in the frame (11.1 %). Real flag and cards out of frame (1.8 / 2.4 m). The A/B against 27911a44 (`ice-ab-glossy-vs-real-cards.jpg`): speaker mean change 11.4, p95 26, largest 40 px block 24.2. The whole scene is about -0.15 EV (speaker 72.5 -> 64.7, snow 119.8 -> 111.2, sky unchanged), because the real 8 x 6 m flag and the card block part of the sky dome that lights Ice. The batt is still clearly in view. |
