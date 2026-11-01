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

## Round 2 (proofs `*-ice-r2`, fresh critics)

| frame | blind | if fixed | the critic's main notes | what was done |
|---|---|---|---|---|
| front-off-tall | 5.5 (+0.5) | 7.0 | still floats (209 under the edge, 210 open floor); a big close key, no cast shadow; horn the darkest mass; a lump on the left sweep | floor 0.15, wash 0, pool 0.2, contact core 0.06 m; key 1.0 x 1.3 m at 2.2 m; horn 5.0, rim 30 W; wall_left 3.0, bg-left 0.9; edge 1.0 W, sidesheen 0.9 |
| front-off-wide | 5.5 (=) | 7.3 | a grey band across the left floor (a fold in the sweep); foreground floor grey; plinth's left corner floats; right backdrop patchy | cove_far 3.0, floor 0.6 spread 80; contact core 0.05 m, distance 0.30, scrim 0.6; wash 0.45; bg-right 1.1 aimed high right; sidesheen 1.0, kick 2.6; topline 2.2 higher |
| hero-light | 5.5 (=) | 7.3 | no dark contact line; front of the cabinet navy; a dirty grey top-left (211 against 248) | contact 1.4 / 0.5 m / core 2.2 at 0.025 m; back-top 45 at azimuth 190, elevation 35; scrim 3.6; bg-left moved out and aimed higher, 3.4; sweep roughness 0.35. Not taken: a white bounce card |
| side | 5.5 (=) | 7.3 | the side face a flat slab (range 7.7); horn navy, throat crushed; little depth | sidesheen moved to the side face's mirror position, 1.4; back light behind and above the horn, 4.0; rim at the throat, 30 W; a diagonal falloff on the set; 5900 K, tint 0; contact core 0.015 m; key 1.4 x 1.8 m at azimuth -45, elevation 28 |
| back | 5.5 (+1.0) | 7.3 | side and top mirror the sweep (grey-white); interior near-black; plate dim; light contact | wash 0.3; glow 5.0 with transmission; fill 1.1 near the camera axis; contact 0.6 at 0.12 m; d-wall 0.25. Not taken: black flags (the rig has none), led.glow 18 (a material) |

Every critic again named the same material limits, for the owner: the plinth's LED as a hard orange or white line
(the back's 12 % clipped), the dark lining making the interior a slab, the blue at the gamut's edge, and (wide) a dark
vertical streak in the lining at the cabinet's top centre, to check in the model.

## Round 3 (proofs `*-ice-r3`, fresh critics): the last round; the gate not passed

| frame | r1 | r2 | r3 | if fixed | the critic's main notes (not applied: three rounds is the limit) |
|---|---|---|---|---|---|
| front-off-tall | 5.0 | 5.5 | 5.0 | 6.8 | denoiser smear at 48 samples the main tell; the front-right edge a flat white bar (edge 1.0 W too strong); horn flat blue; contact spreads right; a dark band back on the left sweep |
| front-off-wide | 5.5 | 5.5 | 5.5 | 7.0 | still floats (the LED glow fills the contact core); the grey cove band on the left (a 27-level dip); horn flat; backdrop uneven |
| hero-light | 5.5 | 5.5 | 5.5 | 7.5 | ground now flat paper white; contact short; back-top 45 throws a blue streak across the floor; the plinth violet from the rig's magenta white-balance tint (7.0): set it to 0 |
| side | 5.5 | 5.5 | 5.5 | 6.8 | the side face still a black slab: **round 2 moved the sidesheen panel behind a black reflect-only flag (`set.flags[2]` at [1.6, -1.2, 1.2])**, so the face still mirrors black; remove the flag. Horn flank crushed |
| back | 4.5 | 5.5 | 5.5 | 7.0 | the left side and top mirror the sweep (white, edge lost); flat backdrop; contact weak; interior navy; a strip rim for the horn's layers |

**Result:** no frame type reached 7.0 in three rounds; every critic's "if fixed" is 6.8 to 7.5. What holds the frames
back is mostly outside this gate:
- **Materials (the owner's):** the plinth's LED, read in all fifteen passes as a hard orange or white line (7 to 12 %
  clipped on the back), which also fills the contact shadow; the dark lining (the interior a navy slab); the blue at the
  gamut's edge; the Ice horn (the site's deep lot, cobalt) and cabinet (stock 2069, teal-navy) reading as two materials.
- **The proofs' 48 samples:** every critic named the denoiser's smear first or second; the finals' count (the critics
  ask 384 to 512) is a time decision: at the plan's rate a 1000 x 1250 frame at 384 samples is about 55 minutes.
- **To check in the model:** a dark vertical streak in the lining at the cabinet's top centre (wide r2) and a small
  bright blue rectangle at the cabinet's upper-left edge from the back (back r3).

The round-3 notes above are the next pass's starting point if the owner keeps these materials.
