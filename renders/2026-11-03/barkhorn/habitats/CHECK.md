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
| Ember (satin) | PASS | PASS | PASS | PASS | rotate_z -1, crack_r on the speaker at 2.0, camera at 0.8 m, 96 samples. At 390 px the ground under the base is 14.8, the base 13.6 and open ground 45.9. The peak along the foot is 60 (it was 181). The woofer, surround, braces, posts and ports show through the front and side, and the driver shows through the horn. The contact band is continuous. |
| Haze (satin) | PASS | PASS | PASS | PASS | 96 samples. Dark violet acrylic: the woofer, ring, ports, braces and left frame show through, and no face is milky. The base sits in the grass with a continuous dark contact shadow. The horn is pale lavender and backlit by the low sun, lighter than the cabinet, the same satin-backlight look as Ember (held for the horn-finish call). The driver and its struts show through it sharply. |
| Ice (satin) | PASS | PASS | PASS | PASS | 64 samples. Clear blue: the woofer, ring, posts, braces, ports and screws show through the front, and the cabin window shows through the side. The bottom batt is clearly visible between the ports with its notch for the lead (`ice-portrait-batt-crop.jpg`, 2x). A dark contact line sits under the bottom panel. The snow in front measures 120.7, against 121.1 and 120.3 to either side, so no glow. The horn is smooth, with a soft haze at the throat. |
| Dust (polished) | PASS | PASS | PASS | PASS | Sand bounce 0.35, no tumbleweed, 64 samples. Amber-red acrylic: the woofer, ring, braces, ports, crossover box, its screws and the desert behind show through. The rail sits on the ripples: luma 81 under the front edge against 107 for open sand. The contact shadow is weak. The red patch is the tinted shadow. The horn is a smooth glassy shell, with the driver showing as a smooth bulb and no X. |
