# catalogue31: the catalogue views relit

The front view of each of the eight colours, cover on and off, brought to the standard of promotional images for a
$20,000 pair. One rig, written by `catalogue31.py` into `studio/shots/barkhorn/lookbook31/look-{k}-{on,off}.json`; the
colours differ only in the sweep's tint and an exposure trim. Critic passes follow `critic/PROMPT-promo.md`: a fresh,
blind critic per pass, given only the staged proof (half size, 128 samples), its card (`catalogue31.py stage`) and
`critic/measure.py`. Replies: `critic/rounds/2026-10-18/catalogue31-*.json`. Proofs: `renders/2026-10-18/barkhorn/catalogue31/`.

## The rig, and why

Probing what each surface mirrors (`render.py --probe`) came first, because a vertical sheet of clear acrylic seen from
above mirrors the floor, not the studio: the front looks front-left and 4 to 20 degrees down, the side behind-right
(azimuth 158 to 161) and down, the top front-left and level, the horn's upper flank up toward the camera. So:

- **key**: one 1.0 x 1.4 m softbox camera-left (azimuth -55, elevation 38, 1.5 m), gridded to 50 degrees and aimed
  past the speaker's left, so the cover falls off about 25 levels left to right and the side sits a stop under;
- **fill**: a 2 m soft source near the camera's side, low, for the side panel;
- **flags** seen only in reflections (no shadows on the paper): black on the floor and standing behind-right, so the
  side panel mirrors black and reads a clean deep colour instead of the pale paper; black overhead for the horn's top;
- **front scrim**: a graduated card on the floor front-left, bright far and black near, so the front's acrylic carries
  a soft sheen over its top and stays clear below;
- **top line**: a white card far off front-left at the top's height, a crisp line along the top's 20 mm edge;
- **edge**: a 2 cm strip standing in the plane the near vertical edge mirrors (through the camera's mirror image and
  that edge), linked to the cabinet only, so the line lands on the edge at every height and the paper's gloss never
  shows it;
- **rim**: a strip over the horn, linked to the horn;
- **horn fill**: a gridded strip just off the lens into the horn's mouth;
- **paper**: lamps that light only the sweep (`receivers: ["sweep"]`): a glow behind the speaker, the key side lifted,
  the floor washed; a long cove (radius 2.8 m, the wall 5.5 m back, 18 m wide) so the horizon is soft;
- a dark studio (the world at 0.15 of a dark grey), so every light on the product is one of these;
- light-path depth: 32 bounces, 16 glossy, 32 transmission (the black top-edge segment of pass 1 was paths dying
  inside nested 20 mm sheets);
- post: a mild contrast, clarity and sharpening, and film grain (`finish.grain`, new in the engine) at 1 level.

What failed on the way: a flank strip for the horn's right edge, seen through the horn's thick resin throat, drew a
white oval beside the driver (found by switching lamps off one at a time on 30-second crop renders); it is gone. A
strip near the floor showed in the paper's gloss as a streak until it was linked to the cabinet.

## Passes

| pass | frame | score | top notes | what I did |
|---|---|---|---|---|
| 1 | the lookbook21 rig, Ice on | 5.5 | no direction in the light; no reflections on the acrylic; throat crushed; base crowded; flat sweep; a black top-edge segment | the new rig (above) |
| 2 | p2 (`p2-blue-on.png`) | 5.5 | floor dull grey and darker than the wall, a hard horizon, no contact, side navy, a hot oval in the horn, framing tight | brighter wash on the floor, a 2.8 m cove, stronger contact, more fill, 90 mm lens, paper lamp to the key side, the flank strip removed (the oval) |
| 3 | p3 (`p3-blue-on.png`) | 5.5 | a hot stripe on the left floor; side still navy; driver crushed; the edge line clipped; neutral shadow; grain mottling; cover and lining read CG (out of scope) | three passes without half a point: the approach changes (below) |

Three passes held at 5.5, and each critic put the cloth cover and the lining at the top of what keeps it from a 9 (out
of scope for me), estimating 6.5 to 7.5 with every in-scope change made. So the approach changed rather than the
settings: the coordinator's cloth and lining shaders (main, a5192de) are merged, which restarts the count (a different
object), and pass 3's in-scope notes went in with them.

| 4 | p4 (`p4-blue-on.png`), the new cloth and lining | 5.5 | no contact; uneven paper (grey top-left, a hot floor patch); the edge line a hard stroke; driver crushed; denoise blotches; no coloured light on the floor; paper the same blue as the speaker; dead space above | stronger contact; wall and wash moved; edge strip wider and dimmer; horn light higher; key behind-left; the paper's tint halved (the owner's tinted sweep kept, a whisper of it); framing lowered |
| 5 | p5 (`p5-blue-on.png`) | 5.5 | the cabinet a dark opaque box, not lit glass; no coloured light on the paper; driver a black hole; a shadow smudge; a grey band behind | the concept changes again (below) |

Five passes at 5.5. Every critic repeats three things: the cabinet reads as a dark navy box rather than glass with
light in it, the driver is a black hole, and the tinted acrylic throws no colour onto the paper. A front-lit cabinet
sends its light through the tint twice (in, off the white lining, out), so it can only go dark; the concept became
**through-light**: a softbox behind the speaker and a kicker on the camera side, both linked to the speaker (no second
shadow on the paper), the paper a bright field behind it. Tried and set aside on the way, by eye: high key (a white
room: flat, no shadows) and a satin floor (no visible gain at proof size). A blind duel (`critic/duel.py`) between the
through-lit frame on the pale paper and the same on a deep paper (#6F8494, the dark-field classic for glass) chose the
pale paper, 5.6 to 5.0: the owner's light tinted sweep holds.

The black mass in the horn's throat is not the driver: hiding the driver leaves it as dark (47 % crushed against 53 %).
It is the tinted resin's own depth where the horn is thickest, so it is the product's, and no lamp moves it (a softbox
behind the driver and one front-left, both linked to it, moved the crush from 53 to 50 %). The card now says so.

| pass | frame | score | top notes | what I did |
|---|---|---|---|---|
| 6 | p6 (`p6-blue-on.png`), through-light, f/6.3 | 5.5 | key on the hidden side, so the seen faces are dark; a cyan cast on the paper; thin contact; denoise smearing; grey top-left | key back to -35 degrees; paper at a third of the look book's tint; denser contact; more wall light; more backlight; **256 samples** (every critic named the denoiser's smearing) |
| 7 | p7 (`p7-blue-on.png`), 256 samples | **6.0** | the top-right corner dissolves into a flat near-white paper; a cyan cast; no coloured pool on the floor; the top pad as bright as the paper; no falloff to the top | the paper falls off behind the right side; warmer paper lights; a diffuse-only backlight on the paper for the pool; key lower; less floor wash; horn light into the throat; grain 1.5 |
| 8 | p8 (`p8-blue-on.png`) | 6.0 | no contact core (the wash fills it); a lopsided paper; the horn's rim lost on near-white; the top band hot; no sheen on the front | less wash, a denser contact; the wall's glow centred; less fill; the top line cooler; a long graduated sheen panel for the front |
| 9 | p9 (`p9-blue-on.png`) | 5.5 | the paper still lopsided (dark left, near-white right); no coloured pool; the front's sheen stops a third down; the top band clips; thin contact | see the duel below; then a continuous scrim, a cooler top line, a wider contact, contrast 0.2, the key gridded to 50 degrees, the paper lamp a little up |

From pass 7 on, the single scores sit inside their own noise (5.5 to 6.0) and the critics contradict each other on the
paper (pass 7: darker behind the right side; pass 8: centre the glow; pass 9: even it out). A blind duel is more
sensitive (two frames side by side), so from here the duel decides which way to go:

- **duel 2:** p9 against p7 (the first 6.0): **p9 wins, 6.0 to 5.5**: the neutral grey paper separates the silhouette,
  the horn's throat shows the phase plug and vanes with a crisp specular, the horn's rim has a moulded highlight, the
  disc has more range; p7's floor was cleaner. p9 is the best Ice frame so far (`critic/best.json`).

**Smoke**, pass 1 (`s1-black-on.png`, the p13 rig): **5.5**: the side panel a dead black slab (it mirrors the black
flag), the paper's top-left muddy, little weight at the right-back corner, the horn's bowl a void with thin streaks,
the floor cooler than the wall. Smoke needs the flag's mirror to carry some light where the clear colours want black:
a faint graduated sheen in front of the side flag (`sidesheen`, 0.4 peak; at the side's 68 degree incidence a clear
colour barely shows it), and the wall, pool, horn light and the fill's and ambient's colour as it asked.
| 10 | p10 (`p10-blue-on.png`) | 6.0 | denoise smear; the lining the brightest thing on the speaker; muddy upper-left paper; weak footprint; no coloured pool | a deeper footprint, the paper's upper left lifted, the lining off the backlight and kicker (`SHELL`), the side opened, the floor flag smaller |
| 11 | p12 (`p12-blue-on.png`, with Smoke 2's changes) | 5.5 | right backdrop near white; the top's edge lost; a violet fringe at the throat's lip; denoise | lost its duel (below): Smoke 2's changes reverted |

- **duel 3:** p10 against p9: **p10 wins, 6.0 to 5.5** (crisper frame edges and top rail, deeper inner shadow, a cleaner top backdrop).
- **duel 4:** p11 (the p16 rig, `p11-blue-on.png`) against p10: **p11 wins, 6.0 to 5.7** (a brighter top falling off further, a darker floor grounding the base, a more glass-like gradient down the side).
- **duel 5:** p12 against p11: **p11 stays, 5.5 to 5.0**: Smoke 2's lower white point and dimmer floor lights made the frame a third of a stop darker and muddier, and the lowered side flag drew a hard edge on the side panel. Reverted; **the p16 rig (p11's frame) is the finals rig.**

**Smoke**, pass 2 (`s2-black-on.png`): 5.5: a faint contact, the side panel's lower half still crushing, the paper beside
it near white, a steep diagonal on the paper, the horn's left bowl flat, a step in the side's reflection. Its changes
went into p12 and lost the duel on Ice; Smoke's side sheen at 0.6 stays.

## Where it stands

The bar (two Ice passes in a row at 8.5, Smoke at 8.5) is **not reached**: eleven Ice passes ran 5.5, 5.5, 5.5, 5.5,
5.5, 5.5, 6.0, 6.0, 5.5, 6.0, 5.5 and two Smoke passes 5.5, 5.5; the critics' own estimates with every in-scope change
made run 6.5 to 7.6. What holds it under, in their words, every pass:

1. **The product's own surfaces** (out of scope here): the cloth disc reads as a flat matte plate and the lining as
   smooth foam blocks, even after main's new shaders (a5192de); every critic names them first or second in what keeps
   it from a 9. The weave shows at full size (1.6 mm a pixel at proof size hides it), the batting does not.
2. **The horn's throat**: a dark mass that is the resin's depth, not the driver (hiding the driver leaves it as dark);
   no lamp moves it. A product question for the owner: a lighter `horn_deep` or a thinner throat section.
3. **Denoise smear** at proof size, 256 samples; the critics ask for 1024 at full size, about four hours a frame on this
   four-core container. The finals run at 256 full size.

The concept is not the limit, the duels show: each round from p7 to p11 beat the one before side by side, and the
final rig beat the current catalogue frame (finals31 before this round, `finals31-before-blue-on.png`, the full frame
halved to match) **5.5 to 4.5**: grounded on a modelled sweep instead of floating on a flat field, the acrylic lit and
luminous instead of muddy navy, balanced margins; the old frame was crisper at 3x (a full frame halved against a proof).
The owner's tinted paper holds (duel 1); at a third of the look book's chroma, so the speaker is the only saturated
colour in the frame.

## Would the rig lift the other sweep views?

- **back** (`site30/back-{k}`): mostly yes, with work. The paper lamps (receivers `sweep`), the dark studio, the grain,
  the depth and the 256 samples carry over as they are. The reflection cards do not: they were placed from where the
  front, side and top mirror for this camera, and a camera behind the speaker mirrors other directions, so the flags,
  scrim, top line and edge strip would need placing again with `--probe` (about an hour's work).
- **horn-side, horn-back** (`horn21`): partly. The horn is resin with no lining, so the backlight and the paper falloff
  would help most (the through-light is what the critics praised on the horn); the edge and flank strips must be
  checked against the throat (a flank strip seen through the throat drew a white oval here).

## The finals

The coordinator (08:18) moved the stopping line, since scores across every session sit between 4.5 and 6.0: stop when
two passes in a row gain under half a point, render the finals from the best rig, duel, report honestly. The passes
had already met it. Before the finals, main's cover changes were merged (b394ba1, the cloth rolled round a 5 mm edge,
the model rebuilt; 5747f1c, a melange cloth); the finals' shots are at 4b0fe16. Ice and Smoke rendered here; the six
other colours in six helper sessions (branches `r31-catalogue-<k>`), all with
`finals.py render --only <k> --views front-on,front-off --force` at the templates' own settings: 256 samples, full
size, about 65 minutes a frame on four cores (Ice cover-on: 3913 s, 2.6 MB).

**The final's blind pass** (Ice, cover on, full size, `catalogue31-final-blue-on-full.json`): **6.0**, "a clean,
well-controlled studio packshot ... reads as a high-end render rather than a photograph". With the new cloth the cover
reads as cloth at full size; what the critic still names: the contact line faint (no weight); no coloured pool from the
acrylic; hot streaks on the horn and a violet glow at the throat's lip (the rim lamp); the top face as bright as the
wall behind; the paper without tooth; then the throat's dark mass, the lining, the internal streaks (the product's).

Next, if the rig is opened again: the rim lamp to about 5 W (the violet glow, named by three critics), the top line
to 1.0, the horn light's specular to 0.5, a darker floor under the cabinet (wash 0.2, contact 0.45 m), and a paper
tooth (a material on the sweep: an engine change, not made here). A coloured pool needs either refractive caustics
(noisy at these samples) or light linking that lets the backlight reach the paper through the acrylic without its
glossy streak; neither was worth a re-render of all sixteen.

All sixteen finals, merged from the helpers' branches (`r31-catalogue-<k>`) and this session's (Ice, Smoke), at
1080 x 2160, 256 samples; `finals.py check` passes them (a grip in frame, the right colour; its other 42 "stale" are
the other views, older than this container's model rebuild by file time only), and every PNG is 2.4 to 2.7 MB:

| colour | cover on | cover off |
|---|---|---|
| Ember (red) | 44 min, 2.61 MB | 43 min, 2.56 MB |
| Dust (orange) | 63 min, 2.64 MB | 64 min, 2.60 MB |
| Acid (amber) | 69 min, 2.62 MB | 67 min, 2.60 MB |
| Poison (green) | 66 min, 2.55 MB | 68 min, 2.51 MB |
| Ice (blue) | 65 min, 2.60 MB | 66 min, 2.57 MB |
| Haze (violet) | 42 min, 2.54 MB | 40 min, 2.51 MB |
| Fog (ice) | 70 min, 2.55 MB | 67 min, 2.57 MB |
| Smoke (black) | 50 min, 2.42 MB | 49 min, 2.42 MB |

The sheet: `renders/2026-10-18/barkhorn/catalogue31/front-sheet.jpg` (the sixteen, cover on above, off below) and
`finals31/sheet.jpg` (every view). Looked at side by side they read as one set: the same framing, light and paper
falloff, each colour on a whisper of its own tint; Fog's white cloth holds its weave at -0.6 EV, Smoke's dark acrylic
shows its lining and a surface on its side panel.

## The gallery's frames (3:2 and 4:5)

The owner, on the speaker pages: the 1:2 fronts "feel odd and out of place because they aren't the same proportions of
the other images and feel cheap" (the gallery's stage is 3:2 on desktop, 4:5 on phones). The rig is reframed, not
relit: the same camera position (the same perspective) and the same lamps, a new lens and lens shift per frame
(`catalogue31.py`'s `FRAMES`; the engine fits the sensor's 36 mm to the frame's width, so the lens follows the
frame's height-to-width ratio), each centred by its box in the frame:

- **3:2** (`-wide`, 1920 x 1280, 32.3 mm): the speaker at 70 % of the height and 24 % of the width, centred (38 % each
  side, 15 % above and below). Its wider view ran past the sweep's end and showed a dark, unlit third of paper on the
  key side; the sweep is wider for it (40 m, 9 m tall) and a lamp of its own lifts that paper (`wall_left`, 4 W/m2).
- **4:5** (`-tall`, 1440 x 1800, 60.5 mm): the speaker at 70 % of the height, centred across, a little low (16 % above,
  14 % below).

Each is about the 1:2's pixel count (12 and 14 minutes at proof size against 15). The 1:2 shots are unchanged.
Proofs: `renders/2026-10-18/barkhorn/catalogue31/frame-{wide,tall}-blue-on.png`. `finals.py`'s views
`front-on-wide`, `front-off-wide`, `front-on-tall`, `front-off-tall` render them as
`finals31/front-{on,off}-{wide,tall}-<k>.png`; its `--views` now matches a view by its whole name, so `front-on`
does not also take `front-on-wide`.

## The paper (one backdrop for the site)

The coordinator, after a full-site critic pass: the product pictures carried four studio looks (a warm hero, a white
studio band, this sweep in grey with a 44-level vignette, the details pastel per colour), and the home cards take
their panel colour from these frames' foot, so they read a dingy grey (#8B908F to #ABA3A1). The catalogue moves onto
the studio's warm pale paper (round 31c's bright field): one neutral backdrop for all eight, no tint per colour.

- **The speaker's light is the rig's, as it won.** Only the paper changed: `#F7F0E8` (the studio's `#F3F1EE`, warmed so
  it renders warm under the rig's white balance and not faintly green), lit high-key by lamps linked to the paper alone:
  31c's two broad lamps on the cove behind, a gridded overhead lamp for the floor, a lamp for the far left and the
  upper wall that every frame sees, and for the 3:2 two more (its far-left wall and the foot of its cove). The tinted
  look's paper lamps are retuned (the glow behind and the key-side wall off: they drove the wall past white).
- **Measured** (proofs, cover off, 3:2): the floor at the feet 241 to 243 (RGB about 246/242/235, `#F2EFEA` asked), the
  wall 240 to 241 (242/236/226, `#EDE9E3` asked), the corners and edges 236 to 244: within eight levels across the
  frame. The 4:5 at quarter size: 229 to 242.
- **One paper for every colour:** a colour's exposure trim (Fog's -0.6 EV, for its white cloth) is made good on the
  paper's lamps, so Fog stands on the same paper as the others (it had gone grey).
- **Smoke and Fog part from the ground** by the rig's own black cards, which the side and the edges mirror. 31c's tall
  dark strip was tried and dropped: its shadow drew a streak on the cove.
- **The cabinets against the approved finals** (90eaf89, same light; ΔE 2000, median colour of the part): through the
  front, Ice 0.2, Fog 0.5, Smoke 1.2; Smoke's side 0.8; Ice's side 5.6 and Fog's 12.6 lighter, as the side now looks
  through to bright paper instead of grey. Fog's acrylic keeps its faint cool green (the water-clear material's own);
  the paper under it is neutral.
- With the drivers merged (01267eb) and the model rebuilt.

Proofs: `renders/2026-10-18/barkhorn/catalogue31/paper-{blue,ice,black}-off-wide.png`.

### The detail views on the paper

finals.py's horn-side, horn-back, back, amp and inside now come from `details31/<view>-<k>.json`, written by
`catalogue31.py` from their own templates (horn21, site30): the camera and the light as each was tuned, the same paper
(`#F7F0E8`) under it, lit by two lamps on the paper alone (the cove's wall and its gridded floor) set per view to the
catalogue's paper (233 to 240 across the frame on the three views with paper in frame; the amp view is the plate close
and shows almost none). The cutaway takes each colour's flavour; its old per-colour tint (finals.py's recolour, from
lookbook21) now applies to the old template only. With the drivers: the horn views show the new HF driver through the
pod, the cutaway the new woofer's motor. Proof: Ice's set, `catalogue31/paper-detail-*-blue.png` (half size, 1 to 3
minutes each).

**The gland's notch (round 31, approved by the lead):** the pale tab under the R of the back's EARF, on back and amp in
every colour, was the notch cut in the back's upper batt (lining-back-c) for the HF lead's gland, 85 deep (its floor
`max(60, t_top + 10)` under the top), seen through the tinted back. It is now sized from the gland: the M12 gland's 22
mm body below the 20 mm pad, plus 10 for the lead to turn up into it (floor at z 808, 27 deep), behind the letters; the
lead runs up the batt's inner face in the 10 between it and the top's batts, hidden from behind, and turns into the
notch only at the top (product.py `lining()` and `lead-hf`). Full build: 0 clashes; lining-back-c's cut file, its nest
and its area in the parts list change, nothing else (the rest of the rebuild was timestamps and the drawings' issue
date, reverted). Before and after: `catalogue31/gland-notch-before-after.png`.
