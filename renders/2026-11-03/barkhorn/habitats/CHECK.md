# Habitats on horn A, blind four-test gate

Horn A is `tropos-strata.blend` from r33-speaker-horn 0936e6d: Strata's cabinet, the caldera, the bronze posts, and the
smooth formed horn, satin outside, with closed volumes.

The habitats are rendered by `spinoffs/barkhorn/biomes/habitats.py`, with:
- the speaker on its own M8 feet, bedded 12 mm into the ground (the sets' displacement is invisible to the ray cast), with base A and its uplight left out;
- the welded volume glass;
- `--horn-front`;
- the black flag and side cards;
- the speaker fills off and the light off by day.

Each is rendered at 1200 x 1500, with 96 samples for the dark scenes and 64 for the rest. Each image is checked blind
by a fresh agent that sees only that image (`scratchpad/check/PROMPT.md`).

Withdrawn:
- the first Ember (3de248cd) and Dust (c96fb96a) were rendered on the Cloud design, not horn A;
- Ember fa1271ef and Dust 426996f1 stood over displaced ground with a gap under the base (the coordinator's gate).

| Habitat | see_through | grounded | no_light_down | smooth_horn | Notes |
|---|---|---|---|---|---|
| Ember | PASS | PASS | PASS | PASS | rotate_z -1, crack_r on the speaker at 2.0, camera at 0.8 m, 96 samples. At 390 px the ground under the base is 14.8, the base 13.6 and open ground 45.9. The peak along the foot is 60 (it was 181). The woofer, surround, braces, posts and ports show through the front and side, and the driver shows through the horn. The contact band is continuous. |
| Dust | PASS | PASS | PASS | PASS | Sand bounce at 0.35 (0.77), tumbleweed dropped, 64 samples. The bottom edge is in the ripples with a dark contact line: luma 62-69 under the base against 90+ for open sand, and no feet or gap show. The woofer, ring, braces, ports, amp box and screws show through. The red in the shadow is light through the tint. The horn is smooth, with faint soft creases toward the corners and no bold X. |
