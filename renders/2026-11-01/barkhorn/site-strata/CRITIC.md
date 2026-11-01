# The site set in the final design: critic log

Prompt: `critic/PROMPT-promo.md`, staged by `spinoffs/barkhorn/critic/stage_site.py`: a fresh blind subagent per frame,
given only the image, a card and `critic/measure.py`. The gate (the coordinator, 2026-11-01): **framing and light only**;
the tints, the lining and the plinth's glow are fixed in the card while the owner decides them. Proofs at half size,
48 samples (the denoiser's smear at that count is expected and not acted on). Up to three rounds per frame type, on Ice.

| round | frame (proof) | blind | if fixed | the critic's main notes | what was done |
|---|---|---|---|---|---|
| 1 | front-off-tall (`front-off-tall-ice-r1`) | 5.0 | 7.0 | no contact shadow (floor by the plinth 241 = open floor); flat ground; busy lit interior; horn electric and smeared; posts dull | floor 0.35, wash 0.2, pool 0.4; contact 1.0 / 0.45 m / core 0.03 m; bg-right 0.8, bg-high 0, wall_left 3.6; horn 3.2, rim 18 W; back 1.6; topline 2.6 |
| 1 | front-off-wide (`-r1`) | 5.5 | 7.0 | floats; flat ground (range 7); murky interior; 32 mm leans the verticals; fringes on the plinth's edges | as the tall front's ground and horn; 50 mm from [1.86, -3.87, 0.95]; sharpen 0.15. Not taken: back 4.5 (the tall front's critic asked the opposite) |
| 1 | hero-light (`-r1`) | 5.5 | 7.3 | weak contact (225 on 249); flat 249 void; speaker centred with no room for the heading; cabinet near-opaque | contact 1.0 / core 1.0 / 0.04 m; scrim 2.6; bg lamps 2.8 aimed low, mirrored; back-top 30 at 45 deg; camera target x -0.55 (speaker to the right third); sweep roughness 0.6. Not taken: a new backlight panel |
| 1 | side (`side-ice-r1b`) | 5.5 | 7.3 | the side panel a dead navy slab (a black flag at its mirror angle); floats; horn crushed 8.7 %; floor brighter than the wall | as the tall front's ground and horn; kick 2.8 at azimuth 75, elevation 25. Not taken: replacing the flag |
| 1 | back (`back-ice-r1b`) | 4.5 | 6.5 | no contact shadow; flat sweep; EARF mark and amplifier plate dim; bottom-heavy framing | d-floor 0, fill 0.6; d-wall 0.2 aimed low; key 2.6 at azimuth -60, elevation 32; glow 2.4 behind the horn; camera target z 0.52. Not taken: a rake light for the mark |

**Out of scope, for the owner** (every critic): the horn's and cabinet's blue near the gamut's edge (red channel about
0), the dark lining making the interior muddy, and the plinth LED reading as an orange fringe. The hero-light critic
also read the card's "gray plinth" against a blue one: the card was wrong (the plinth is in the flavour's tint, as the
model has it), corrected in `stage_site.py`.

The critics also asked for 384 to 768 samples; the finals' count is decided when the gate passes.
