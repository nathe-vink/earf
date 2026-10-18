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
