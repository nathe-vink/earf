# Smoke, concept B: high-key (round 31b)

A misty birch wood on a pale winter morning: chalk-white trunks receding into the mist, fresh snow, woodsmoke drifting
in thin sheets from a fire out of frame, soft light from an overcast sky. The smoked-black speaker stands sharp against
the pale mist, black on white. Its line: "Where there's smoke." Set: `smoke_b.py`; its own pieces:
`studio/engine/kit_ext/smoke_b_el.py`.

## Set and assets

- Sky: Poly Haven `snow_field` (overcast snow field, CC0), 4k, turned 200 degrees; no sun lamp (an overcast morning
  has no shadows to sharpen).
- Ground: `snow` piece, Poly Haven `snow_02`'s height and normals (4k, true displacement near the lens) under a clean
  white skin of our own: the scan's colour carries dark twigs that tile. Faint subsurface and a fine sparkle.
- Birches: Poly Haven has no birch, so `birches` builds them: tapered, slightly crooked tubes (some clumps of two or
  three stems from one foot), barked procedurally (chalk white with grey and cream patches, short dark lenticels,
  black scars, a blackened fissured foot) over `bark_willow`'s scanned normals for micro-relief. 9 placed trunks near
  the speaker, 70 more receding to 60 m, one close to the lens at the left edge, out of focus.
- Mist: `mist`, a scattering volume clear in front of the speaker and thickening to 0.07 per metre by 26 m, denser near
  the ground. The engine's homogeneous haze veiled the speaker itself grey (proof 1), so the mist starts behind it.
- Woodsmoke: `smoke`, thin volume sheets (1.4 to 1.8 m deep) of wisps (the ridges of a distorted noise) inside
  broader drifts, banded about a height and fading in from the left. A thick box averaged the wisps into a flat grey
  wall (tests t1 to t6); thin sheets keep the structure.
- Ground cover: Poly Haven `grass_medium_01` scattered and drained to dry straw (`dry_scatter`), and three small
  `dry_branches_medium_01`.
- A black flag (negative fill) out of frame on the camera's side, seen by reflections: the speaker's front mirrors
  black instead of the white wood behind the lens, so the smoked acrylic reads deep (proof 3 read mid-grey).

## Concept proofs (0.3 scale, 32 samples)

- Overcast (`snow_field`) against a low sun through the mist (`birchwood`, sun lamp from its sun). Little to choose at
  this density of mist: the sun gave a touch more modelling and nothing of its own. Chose **overcast**: it is the
  brief's high key (soft, shadowless, black on white), and it stays clear of concept A, which is backlit smoke at dawn.
- Proofs 1 to 5 then fixed the mist veiling the speaker, the invisible smoke, the bark (lenticels too sparse), the
  trunks (too thick and parallel: thinner, leaning, clumps), the snow's tiled dark twigs, the foreground trunk (too big)
  and the branches (scanned pile far too big; now three small ones).

## Critic passes (critic/PROMPT-promo.md; 0.5 scale, 128 samples unless noted)

| Pass | Frame | Score | Top changes | What I did |
|---|---|---|---|---|
| 1 | p6 (`smoke_b-critic/pass1.json`) | 5.0 | grey not high-key (snow median 196): exposure +0.45, white_in 228; no contact (sink, snow lip, lower flag); acrylic a flat slab (a soft light behind); cold cast (warm ~400 K); one grass model cloned 70 times; edge trunk and twigs; smoke invisible (one dense warmer wisp behind the speaker); right trunks pinch it | All made: exposure 1.55, white_in 228, white balance 7000 K, lift 0.02 warm; feet at -0.025; the flag lowered and smaller; `mistglow`, a soft area behind (165°, 1.2 x 1.8 m) standing for the bright mist; grass from two models in clumps at the trunks' feet (35); edge trunk and branches gone; the first smoke sheet denser and warmer; nearest trunk moved out. Proof p7: the horn blew out white (the mist glow came through its resin, measured with the mirror map and a test without it), so the glow lights the cabinet alone (receivers), a second flag overhead, a snow lip at the foot (`snow_lip`), feet at -0.03, exposure 1.6. |
| 2 | p8 (`smoke_b-critic/pass2.json`) | 5.0 | still grey (snow 209, p99 218): white_in 212, contrast 0.12; cabinet mid-grey (73): flag closer and bigger; no contact shadow, the lip a pedestal (sink 6 cm, narrower broken lip); no smoke (darker, warmer, denser sheet at horn height); no light through the resin (mist glow 3.2); flat foreground (relief 0.45, displace 0.035); grass stickers (sunk, fewer, grouped); knife-hard edges (sharpen 0.12, bloom 0.08) | All made except the horn's glow: any light from behind the horn, even 0.25, turned its resin white (tests t11, t15), so it takes none. The smoke was the critic's top complaint twice: added a `plume`, a column of woodsmoke rising behind the left clump and bent over toward the speaker (it rendered alone, but the mist in front washed it out at density 4: now 12, nearer at 7.3 m). The darker warm sheet read as dirty fog, so the smoke is a cooler blue-grey (#A3A8AF) at density 16. |
| 3 | p9 (`smoke_b-critic/pass3.json`) | 5.5 | no contact shadow (overhead flag, sink 9 cm, wider lip); a muddy brown band in the mist; mist grey not pale (thinner, exposure 1.75); no tint through the acrylic (mist glow 7); the near smoke sheet smears the left trunk (move it behind); trunks are poles (limbs, stubs, twigs); smooth plastic snow (relief, glints); grass in a line of copies | Three passes gained half a point (5.0, 5.0, 5.5), and the complaints kept coming back to the flat overcast light: no shadow to seat the speaker, nothing to model the snow or the trunks, the smoke and mist the same grey. **Concept revised (B2): the same high-key wood under a pale low winter sun through the mist** (`birchwood` sky turned 135 degrees, its sun lamp from the left and a little behind at 14 degrees, 4.0, 2 degree disc), so the speaker casts a shadow on the snow, the trunks and snow are modelled, and the smoke catches the light. Made pass 3's changes with it. Found the brown band's cause: a replace in pass 2 had missed, leaving the sheet at #8C857D; all smoke is now neutral. Birches got limbs (dark grey-brown, 3 to 6 a trunk, stubs low, longer higher). The snow's scanned height map showed its twigs' holes as rows of dots under the low sun, so the snow's relief is now procedural (wind ripples, grain). The scanned grass, sunk in snow, showed only rows of dots: removed. |
| 4 | p11, concept B2 (`smoke_b-critic/pass4.json`) | 5.5 | snow like crumpled satin (finer, sparkle); a hard crease across the foreground (a lone trunk's shadow); no contact or cast shadow (sink 12 cm, a bigger lip); the sun leaves no trace (9.0, 4 degree disc); acrylic flat (mist glow 14 at 28 degrees); a trunk grows out of the horn (moved); a white rim down the cabinet's right edge (the bounce card greyer, smaller, further round); trunk bases cut flat (collars) | All but the collars made: the snow at 1 m a tile, bump 0.8, relief 0.6, displace 0.03; the trunk behind the horn moved to x -0.6. Collars at the trunks' feet floated as white discs where the ground's relief rises under them; dropped. Gain 0 after the concept change: if pass 5 also gains under half a point, stop (coordinator's rule, 08:20) and render finals from the best rig. |
| 5 | p13, concept B2 (`smoke_b-critic/pass5.json`) | 5.0 | overexposed, the snow clipped (6.3 %, median 249): exposure 0.85, white_in 236; no sun shadows (sun 16, less ground mist); weak contact; the smoke a grey smudge (plume nearer, denser, darker); speaker small (85 mm, nearer); acrylic grey (mist glow 26); a sapling tangent to the horn; bloom and lift veil the blacks | **Stopped** (coordinator's rule of 08:20: after a concept change, two passes in a row gained under half a point, 5.5 then 5.0). Not made. Finals from the best rig by blind duel (below). |

## Duels and the finals' rig

Blind side-by-side duels (`critic/ab/PROMPT-DUEL.txt`, fresh judges, neutral names, random sides):

- p13 (pass 5's frame) against p11 (pass 4's): **p11**, 5.5 to 5.0: deeper blacks and crisper edges on the cabinet, the
  base and ports read; against it, the straight shadow band across the foreground.
- p11 against p9 (pass 3's, the overcast concept): **p11**, 5.0 to 4.4: a clean, crisp winter palette against p9's
  muddy grey-beige; the woofer and edges separate; better contact. Against it, the snow's swirls.

So the finals are p11's rig (commit 9f992f4) with one defect fix and no other change: the three flags shade only the
mist glow (`lights`), so the negative flag no longer throws the sun's ruler-straight shadow across the foreground that
both p11's critic and its duel judge marked. The portrait is the same set on an 80 mm lens from 5.4 m.

## Finals

- `renders/2026-10-18/barkhorn/element31/smoke_b.png`: 2400 x 1600, 512 samples, denoised, 4 h 41 min on 4 CPUs (this
  session), 3.1 MB.
- `smoke_b-portrait.png`: 1600 x 2000, 512 samples, 3 h 36 min (the coordinator's helper session, on 6e95bdd; merged
  from r31-element-smoke-b-portrait).
- Blind pass on the landscape final (`smoke_b-critic/final.json`): **5.5**, "iterate".

## An honest note

The frame does what the concept asks at a glance: a black speaker sharp against a pale birch wood, high-key, with room
for type. Every critic said so, and the thumbnail read the owner asked for is there. What holds it at 5.5 is the same
handful of things, in every pass since the overcast light was dropped:

- **The sun barely shows.** A low sun through mist that thick is mostly extinguished before it reaches the snow, so
  there are no long trunk shadows to model the ground and tie the speaker to it. A stronger, lower sun, or a thinner
  mist near the ground, is the next lever (the last critic asked for a sun from -125 degrees at 9 degrees, 9.0).
- **Contact.** The speaker sits in a soft lip of snow but casts little occlusion in such diffuse light; it can read as
  set on top.
- **The snow and the bark are close but not photographic.** ambientCG's Snow003 reads as snow at a distance and as
  brushed streaks near the lens. The birches are procedural; Poly Haven has no birch bark, and a scanned silver-birch
  bark would help most.
- **The woodsmoke never became a visible element.** Thin volume sheets and a plume read as haze or a smudge. A legible
  backlit ribbon of smoke behind the speaker remains the open idea, and it is the one that would carry the line.
- **The smoked tint.** Through the front the acrylic reads near neutral; light from behind lifts the cabinet's
  interior, but the horn's resin blows white under any backlight, so it takes none.

Render time is the constraint here: a half-scale, 128-sample proof with the volumes took about 24 minutes, so each pass
cost close to an hour with its tests.

## Software and assets

No new software. Assets (all CC0, fetched to the ignored cache): Poly Haven `snow_field`, `birchwood` (HDRIs), `snow_02`,
`bark_willow` (normals), `grass_medium_01` and `_02`, `dry_branches_medium_01` (the last three tried and dropped);
ambientCG `Snow003`. No engine core changes; the set's own pieces are `studio/engine/kit_ext/smoke_b_el.py` (birches
with limbs, smoke sheets, a plume, graded mist, snow, a snow lip, dry scatter).
