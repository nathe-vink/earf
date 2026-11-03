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
| Haze (satin) | PASS | PASS | PASS | PASS | 96 samples. Dark violet acrylic: the woofer, ring, ports, braces and left frame show through, and no face is milky. The base sits in the grass with a continuous dark contact shadow. The horn is pale lavender and backlit by the low sun, lighter than the cabinet, the same satin-backlight look as Ember (held for the horn-finish call). The driver and its struts show through it sharply. |
| Dust (polished) | PASS | PASS | PASS | PASS | Sand bounce 0.35, no tumbleweed, 64 samples. Amber-red acrylic: the woofer, ring, braces, ports, crossover box, its screws and the desert behind show through. The rail sits on the ripples: luma 81 under the front edge against 107 for open sand. The contact shadow is weak. The red patch is the tinted shadow. The horn is a smooth glassy shell, with the driver showing as a smooth bulb and no X. |
| Ice (polished) | PASS | PASS | PASS | PASS | Bedded 22 mm, 64 samples. The woofer, ring, braces, ports and posts show through the front, and the cabin window shows through the side. The bottom batt is clearly in view (`ice-portrait-batt-crop.jpg`, 2x). A dark contact band: luma 108 under the base against 121-123 for open snow. No glow. The horn is a smooth glassy shell with the driver at its throat and no X. |
| Fog (polished) | PASS | PASS | PASS | PASS | Sun at 110 (side, not behind), 96 samples, 48 min. Clear birch: the woofer frame, braces, shelves, ports, terminal plate, and the rock and grass behind show through. The base sits down in the grass with a dark shadow, the contact line mostly hidden by blades. No glow. The polished horn is clear, with faint corner creases and refraction, no X. |
| Acid (polished, horn held) | PASS | PASS | PASS | PASS | Sink 0.03, 18 mm into the puddle: the reflection starts at the waterline. The woofer, braces, posts, ports and box show through the amber. The horn passed the four tests, but its crease span is 26.7 (`flare.py`, the flare clear of the driver) against 7.8 for Dust and 7.2 for Ice: the sky mirrored as a diagonal wedge at 28 deg off the camera's line. Re-render at rotate_z -2 (10 deg off) to follow. |
| Ember (polished, turned) | PASS | PASS | PASS | PASS | rotate_z 12 (10 deg off the camera line), crack_r 2.0, camera at 0.8 m, 96 samples. Crease 8.3 / 4.3, left and right of the driver (`flare.py`; Dust 7.8, Ice 7.2): the sky wedge is gone. The 12 o'clock ring glint is gone (red max 233 -> 62). The woofer, braces and ports show through, and the lava through the side. Contact: luma 12 under the base against 26 beside it. |
