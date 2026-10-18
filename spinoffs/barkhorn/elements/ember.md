# Ember, concept A: a lava field at blue hour (round 31b)

The owner, on the dioramas: "the diorama looks cheap, like a bad video game. I was hoping for more texture in a lot of
these. The speakers are too stark in contrast to the setting too. ... Maybe don't think about them so much like
dioramas, and think more about placing them in there element." On Ember: "a volcanic cavern", "well lit by lava pools
and lava falls". And: "Continue to do critic passes until you feel it's in a good enough place for promotional images
for a $20K product."

## References

Fagradalsfjall (Geldingadalir, Iceland, 2021 to 2024) and Kīlauea at blue hour and night: black crusted pāhoehoe and
ʻaʻā, glowing seams and channels, steam lit orange from below, a deep-blue sky above. The light is two-sided: the
lava's orange from below and the dusk sky's blue from above. Campaign touchstones for volcanic ground: Chanel Coco Beach
2026 (black volcanic sand as a near-studio backdrop), ICON Italy "Black Salt" (tailoring against basalt).

## Assets and software

- Poly Haven (CC0): dark_rock, dark_rock_02 (basalt), qwantani_dusk_2_puresky (sky).
- ambientCG (CC0): Lava001 (crusted flow), Lava004 (molten), through my own material (`ember_el.lava_material`): the
  set's emission map drives a black, red, orange, yellow-white ramp, so the lava keeps its hue; its colour map, darkened,
  is all that reflects.
- bpy 5.0.1 on python3.11 (setup.sh pins it; this container's python3 is 3.13).

## Critic passes (critic/PROMPT-promo.md, a fresh blind subagent each)

| Pass | Image | Score | Verdict | Top changes | What I did |
|---|---|---|---|---|---|
| 1 | e1: basalt-column gorge, lava fall in a slot, river behind, pool front left (0.5 scale, 96 samples; still under the old 5600 K / tint 3 white balance) | 4.5 | rethink | columns read as masonry with one repeated texture; lava flat decals with stair-stepped edges, no hot cores; no cool sky; the speaker as dim as the ground; embers uniform dots; the fall competes with the speaker. Its advice: narrow the set (pahoehoe foreground, one lava seam behind as a backlight, an open blue-hour sky) | Rebuilt: open lava field under a visible dusk sky, the column wall dropped, lava as a level surface under carved rock (natural shorelines), hot cores, a backlight through the acrylic, streaked sparks, soft steam |
| 2 | e2: open pahoehoe field, lava below the rock, a backlight, steam, sparks; crater rim with a fall 30 m back (0.5 scale, 128 samples) | 5.0 | iterate | near ground glossy salmon (lum 121), brighter than the speaker (58), horn dark (25); sparks uniform dashes everywhere; the fall lights nothing; haze flattens the rim (p5 48); rim has no geology; sky flat lavender; everything equally sharp | Ground albedo 0.10, roughness x0.9, point lights dimmed and raised; a bigger backlight through horn and cabinet plus a low strip; sparks 70 % fewer, near the lava only, varied; the fall brighter with its own light and a splash pool; haze 0.0012, steam in plumes; the rim as basalt columns with flow layering; sky 0.2; f/2 |
| 3 | e3: black basalt, a terraced rim 30 m back with its fall, sparks near the lava, f/2, lights rebuilt (0.5 scale, 128 samples; first render after main's lining and cloth shaders) | 4.5 | iterate | acrylic not glowing (cabinet 22 vs ground 38); lava dim (p95 79); near ground reads as sand; rim a palisade of stretched streaks; fall a blobby column; sky flat and bright; sparks uniform | Three passes at 4.5 to 5.0: by the brief's rule, the approach changes, not the settings. The procedural heightfields read as CG; next: a photographed landscape as the visible background (an HDRI with real rock), scanned rock models in front, darkened to basalt, and only the lava modelled |
| 4 | e4: **concept changed** to a volcanic cavern: Poly Haven scanned rock faces regraded to basalt, a lava river along the back wall, a fall at the left, a crack at the speaker's feet (0.5 scale, 128 samples) | 4.5 | iterate | the fall a flat card and the loudest element (median 103); the arch tan, not basalt; the floor sand dunes with stepped displacement; a hot spot from the hidden lamp (19 % clipped), the horn crushed (median 10); the sky patch flat; the river a thin glittery line; sparks uniform | Soft area lamps hidden behind the cabinet and the horn (no point), the crack light up; rock albedo x0.03, fully desaturated, roughness 0.55; floor displacement cut (no terraces), lobes smaller, ropes sharper; the fall at strength 12, thicker; the river wider with bigger crust plates; the sky turned to show its gradient; sparks clustered at the sources; vignette 0.25 |
| 5 | e5: the cavern after pass 4's changes (lamps hidden behind the acrylic, darker basalt, crusted fall) | 4.5 | iterate | lava not incandescent (fall p95 127, the sky brighter at 167), glossy like plastic; lights nothing (back wall p95 32); the cabinet's core dark (21); the slab warm sandstone; floor like crumpled cloth; sparks tracer dashes | Lava at strength 60 to 70 with a matte crust (roughness 0.85, specular 0.2) and its hottest cracks yellow; the sky at 0.07; grazing river lamps 350 W low by the wall, the crack 200 W; lamps behind the acrylic doubled and lowered; the slab fully desaturated x0.02; steam denser and lower |
