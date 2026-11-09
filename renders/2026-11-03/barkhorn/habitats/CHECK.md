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
| Acid (polished, sun 35, +0.75 EV, the shared split; 2026-11-09) | PASS | PASS | PASS | PASS | Sun irradiance 35, exposure +0.75 EV, the rim unlinked, the bark and horn re-split 0.085 / 0.10 / 1.00 with luminance held (horn OKLCH 0.601 / 0.126 / 101.8, matching the speaker lane). Sink 0.015 (3 mm under the water). 64 samples, peak memory 10.4 GB. Crease 6.1 / 9.2 (Dust 7.8, Ice 7.2). Against the row below (`acid-ab-split-ev075.jpg`): frame 98.6 -> 129.0, speaker 58.2 -> 75.9, sky 135.9 -> 162.4; speaker RGB (85, 65, 24) -> (98, 94, 36), amber to the lane's yellow. Gate: the woofer, rings, braces, posts, ports and crossover block show through; the reflection starts at the base edge; faint flare-corner creases at 3x, not visible at phone size. |
| Acid (polished, 4 deg off) | PASS | PASS | PASS | PASS | rotate_z -8, sink 0.03 (18 mm into the puddle), 64 samples. Crease 5.9 / 10.8 (Dust 7.8, Ice 7.2; it was 26.7 at 28 deg off). The woofer, frames, braces, ports, posts and screws show through. The reflection starts at the base edge. The horn is smooth, with very faint creases invisible at phone size. |
| Fog (polished, reframed, real cards) | PASS | PASS | PASS | PASS | Camera 0.30 m lower (lens rise 0.18), azimuth -10, f/4. rotate_z -5 (5 deg off; at 20 deg off the side face read as a cream sheet, see held/). The sun neutral white at 110. Real flag and card: the sun-side card left out, the other out of frame at 2.2 m. 96 samples. Crease 1.9 / 2.3 (Dust 7.8, Ice 7.2): the whole horn on plain sky. The left cut-edge strip is still warm, b* median 9.7 (p90 17.2) against the sky's -3.6; the target was 5 or less. Clear: the woofer, braces, posts, ports and the terminal block, with the grass and rock behind, show through. |
| Haze (polished, sun front side, real cards) | PASS | PASS | PASS | PASS | Sun 70, 6 deg up, the HDRI turned to 338.8, the set's sun disk at 70 (all out of frame). rotate_z -10 (5 deg off), lens rise -0.13, a 4 x 3 m real flag, the sun-side card left out and the other out of frame at 2.6 m. 96 samples. Upper box max channel 47.5 (target 45-60). Horn to box 2.8x. Horn and box hue both 239. Crease 6.1 / 7.3. The woofer, ring, braces, ports and the block show through the front, and the hills through the side. |
| Ice (polished, real cards; the owner: "Yes it looks right", 2026-11-04 01:13) | PASS | PASS | PASS | PASS | It replaces 27911a44 (retired), whose reflect-only cards sat in the frame (11.1 %). Real flag and cards out of frame (1.8 / 2.4 m). The A/B against 27911a44 (`ice-ab-glossy-vs-real-cards.jpg`): speaker mean change 11.4, p95 26, largest 40 px block 24.2. The whole scene is about -0.15 EV (speaker 72.5 -> 64.7, snow 119.8 -> 111.2, sky unchanged), because the real 8 x 6 m flag and the card block part of the sky dome that lights Ice. The batt is still clearly in view. |
| Dust (polished, real cards; the coordinator's critics SHOW 3/3, 2026-11-04 01:47) | PASS | PASS | PASS | PASS | It replaces 0a356de1 (retired) (reflect-only cards in frame, 10.1 / 5.6 %). Real flag; the sun-side card left out, the other out of frame at 2.4 m. The A/B: speaker mean change 4.6, p95 33, largest 40 px block 64.3 on the left side face, which had mirrored the old black card and now mirrors sky and reads paler (`dust-ab-side-face-crop.jpg`). Speaker level 98.0 -> 100.2. Clear orange-red: the woofer, ring, frames, braces, box, ports and posts show through. |
| Ember (polished, real cards) | PASS | PASS | PASS | PASS | It replaces 45225a29 (reflect-only cards in frame, 4.5 % each). Real flag and cards out of frame at 2.2 m. The A/B: speaker mean change 4.9, p95 14, largest block 16.0. Speaker level 27.8 -> 25.4. Dark ruby: the woofer, braces, frames and ports show through, with lava through the side; it reads almost opaque at phone size (Ember passes 10 % through the box). |
