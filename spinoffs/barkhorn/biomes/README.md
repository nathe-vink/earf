# Planet EARF: the eight biomes in one world (r48-biomes)

The owner, 2026-10-31: "One thing that might be cool is an environmental image that blends each biome together,
showing speakers in each." And: "I mostly want to nail design, make it realistic, make it cooler".

## The idea

One world, one camera, one day. The eight habitats stand in a ring round the camera, each a 45-degree sector with its
Tropos on the sector's center line, 3.6 m out, facing the lens and turned a little. Neighbours meet as geography does:
snow country thins into redwood floor, the redwoods open onto a coastal headland above a sea of fog, the headland's
grass dries into golden hills, the hills into desert sand under mesas, the sand into black lava wet with rain, the wet
rock into a lava field still glowing, the lava into the city's asphalt; and round the back the city's edge meets the
snow again.

Each biome keeps its own light because the picture is a **day-to-night time slice**, made the way photographers make
them from a fixed camera (Stephen Wilkes' "Day to Night"): the same world is rendered once per hour, each slice under
that hour's sky and sun, and the slices are laid together where the ground changes. Dawn over the snow, morning in the
redwoods, the fog burning off mid-morning, afternoon on the hills, golden hour in the desert, sunset in the rain, blue
hour over the lava, night in the city.

Two pictures come from the one render:
- **(A) the panorama**: the band round the horizon, as a rotating panoramic camera (a Roundshot) makes it: a
  cylindrical projection, about 5:1.
- **(B) Planet EARF**: the full sphere as a little planet (a stereographic projection from the nadir), the eight
  biomes wrapped round a small globe with the speakers standing on it, the day running round its sky.

## How it is built

| file | what |
|---|---|
| `field.py` | The world's field, numpy only: each point's biome weights (sectors with noise-bent boundaries, blended over 7 degrees each side) and the ground's height, biome by biome (mountains behind the snow, the headland's cliff, layered ranges, mesas, volcanic cones, a volcano for Ember). The scene and the compositor both read it, so light changes exactly where the ground does. |
| `tints.py`, `tints.json` | The eight tints calibrated to A&C Plastics' TruCast light-transmission chart (TT % held at the sheet's thickness, the Tropos session's `stock_tints.py` method), IOR 1.49. The TruCast code for each tint is a proposal. |
| `tropos_lib.py` | Writes `assets/tropos-current.blend` (not committed; 20 s to rebuild): one collection per tint, `Tropos.Ember` ... `Tropos.Smoke`, feet at z 0, front to -y. |
| `world.py` | Builds the world in Blender (Cycles) and renders the slices: the ground as eight wedge meshes carrying the weights, one ground material mixing eight Poly Haven ground sets at real size, redwoods, firs, ferns, oaks, desert shrubs and boulders, the city's blocks with lit windows and streetlights, one volume of air whose density and color follow the biomes, the fog's sea, the volcano's plume. The speakers are **linked** collection instances: `--tropos other.blend` swaps the model. |
| `composite.py` | Lays the slices together (position pass -> field weights; sky by direction), each at its slice's exposure, and cuts the panorama and the planet, toned through AgX. |

Run:

    python3.11 spinoffs/barkhorn/biomes/tropos_lib.py
    python3.11 spinoffs/barkhorn/biomes/world.py --out OUT --width 2048 --samples 32
    python3.11 spinoffs/barkhorn/biomes/composite.py OUT --planet 1600

## Rounds

(below, newest last)

### Pass 1 (proofs 1 to 3, 1440 px equirect, 16 samples)

- Proof 1 ran out of the container's memory (14 GB). The fir scan alone is 7 M polygons, and Cycles copies each tint's
  speaker (its materials sit on the objects). The fixes: `flora_lib.py` decimates the scans once into a library, and
  the world's Tropos library leaves out the back's plate, prints and screws, which never face the camera. It also
  thins the screws, lining webs and driver internals; the waveguide, cabinet and horn keep every polygon. The peak is
  now 8.2 GB.
- Proof 2: each slice is metered (its own ground's median to the hour's key, night darkest). There is a granite knob
  under the camera, the Ember cracks are narrower and sparser, and the city starts further back.
- Proof 3: redwood crowns (the fir scan stretched to a spire), Haze's sun at 8 degrees, warmer sand, wider joins.

**Blind critic, round 1** (fresh agents, `critic/PROMPT-promo.md`, the image and a card only):
- **Panorama: 3.0, iterate.** The joins are hard vertical cuts in the sky and on the ground. The 16-sample denoise is
  mush. The speakers float, and the night and dark tints vanish (Smoke's median luminance is 0.6). The fog, haze and
  rain don't read. A shrub row floats on the desert horizon, and the city is boxes with tiled windows. The critic
  prescribed:
  - joins of 6 to 8 degrees, shaped as geography;
  - a motivated light per speaker;
  - 512 samples;
  - contact shadows;
  - the weather present;
  - no repeats;
  - the lava's exposure brought down;
  - the speakers placed by hand.

  Estimated score if fixed: 6.5.
- **Planet: 3.0, rethink.** Eight speakers round a small planet makes each a 100 px thumbnail seen from above. The
  knob is split dark and light by the slices. The snow reads as plaster, and the sky ring clips. Estimated score if
  fixed: 6.5, capped near 6 to 7 by the projection itself ("a gimmick, not a photograph").

What was done (proof 5):
- A reflector per speaker, rendered only in its own hour (`BOUNCE`).
- Joins of 21 degrees on the ground and 34 in the sky, and the knob's hours blended over 40 degrees.
- The city from 110 m back.
- The desert shrubs kept within 22 m.
- The ferns kept off the snow.
- The cracks' emission cut a third.
- Each speaker nudged by hand (`field.JITTER`) and turned 4 to 22 degrees.
- 32 samples at proof size.

### Pass 2 (proofs 5 and 6, 32 samples)

Proof 6 has these changes:
- **Photographed skies, one per hour.** Most are from Poly Haven's Qwantani series, one place shot through one day:
  dawn, morning, late afternoon, sunset, dusk and night. Fog has Kloofendal's misty morning, and Acid has
  Kloofendal's overcast. Each sky is turned so its sun stands in its biome's sector (`hdri_rotation`).
- **A lower lens and closer speakers.** The lens is at 1.0 m and the speakers at 2.8 m, so each stands up to its
  horizon and is about 40% of the panorama's height.

**Blind critic, round 2:**
- **Panorama: 3.0, rethink.**
  - The joins read as vertical dissolves, not geography.
  - The midday sky clips (12.6%).
  - The night city stands under a pale sky, and it shows behind the snow at the wrap.
  - The fog, golden haze and rain don't read.
  - Smoke is crushed.
  - The ground materials are smooth.
  - "Composited vertical time slices in a 266 px band of eight scenes cannot read as one photograph": the critic
    asks for the joins on physical features, or a sequence of frames.
- **Planet: 3.0, rethink.** The sky ring is open (a white void), the knob is the hero, the speakers are small, and the
  projection caps the score.

**What was done (proof 7):**
- Tropos is now the speaker lane's asset (r33-speaker-horn 8e44484e, cover off), linked from a gitignored path.
- Smoke's sky is at 0.12 strength, so the windows and street lamps carry the night, with a lamp 2 m behind and left of
  the speaker.
- The city is kept inside its own sector.
- The fog sea is its own volume below the headland.
- The grass is golden.
- The midday hours are trimmed by 0.7 EV.

**Option C**, from the critics: rectilinear "seam" frames from the same world, two neighbors and their two speakers
through a real lens (`composite.py --view`).

### The final panorama (2026-10-31, 4800 x 888, 48 samples, 86 minutes for eight slices)

`renders/2026-10-31/barkhorn/biomes/planet-earf-pano-master-4800.jpg` is the master. The web versions are
`-2400.jpg` and `-1200.jpg`. The PNG was 5.4 MB, so the master is a JPEG.

- **Blind critic, round 3: 3.5, rethink.** The critic finds "the idea of a single day running across the eight
  worlds clear and charming", but says the image reads as a game-engine level:
  - low-detail terrain, and a visible tile on the mesa;
  - a hard redwood wall;
  - the midday sky clipped, with the sun mid-frame;
  - the joins read as 2D cross-fades;
  - Smoke still crushed at 2400 px;
  - box towers.

  Estimated score if fixed: 6.5.
- **Blind duel against the live Fog headland** (`site/img/ice-habitat.jpg`): the headland 6.5, the panorama 3.0. The
  judge: "a contact sheet, not a composed campaign frame"; the speakers are about 100 px wide in a 444 px strip.
- **The gate (7.0, or beating the best habitat) is not met.** Three rounds have been run on this look, which is the
  protocol's limit.

**What it would take to reach 6.5 to 7**, from all five critiques:
- A physical divider at each seam, with the composite blend hidden behind it (a ridge, a tree line, a fog bank's top,
  a road). Today the blends are by azimuth.
- Scan-quality ground and rock at speaker distance.
- One sky arc without a clipped midday.
- A real low-rise city.
- 256 samples or more at the master.

At this container's speed that is roughly a day of work and rendering, not an evening.

### Option C in the CG world: Acid | Ember seam frame (2026-11-01)

This is `world.py --persp 247.5:1.5:40:1800:1200:3.0 --only 5 6`, at 48 samples. The output is
`renders/2026-10-31/barkhorn/biomes/seam-acid-ember-cg-1800.jpg`. It was not critiqued: the coordinator stopped the
CG-terrain method first.

### The coordinator's test: a seam frame on photographed plates (2026-11-01, `seam_plate.py`)

The test asked for one rectilinear seam frame, each side a photographed Poly Haven place, with two speakers rendered
in and the join hidden behind a divider.
- **The two plates:** Poison in `misty_pines`, a conifer forest in morning mist with a fern floor; Fog on
  `white_cliff_top`, a rock headland above the sea, the plate turned 180 degrees so the speaker stands on its rock.
- **The divider:** a redwood trunk on the join, with ferns at its foot.
- **The speakers:** each lit by its own plate, standing on a shadow catcher; the speaker lane's asset, cover off.
- **The camera:** 35 mm, 1.45 m high, 3 degrees down, f/5.6. 1800 x 1200, 96 samples, about 12 minutes for the pair.

The output is `renders/2026-10-31/barkhorn/biomes/seam-poison-fog-plates-1800.jpg`.

- **Blind critic: 3.5, rethink.** The critic saw "two different photographs cross-faded behind a CG redwood trunk":
  - the speakers small, at the edges, flat-lit and nearly without contact shadows;
  - the trunk as the hero;
  - the projected plate ground soft at the frame's foot;
  - two horizons;
  - a person in the headland plate.

  Estimated score if fixed: 6.5. The fixes it named:
  - modelled ground with a hard rock lip at the join;
  - speakers on the thirds at 60% of the frame's height, with a 50 mm lens at 1.0 m;
  - a shared soft key and rim cards;
  - one haze over both sides.
- **Blind duel against the Fog headland:** the headland 6.0, the plate frame 3.5. The judge: the speakers "look pasted
  onto the backplate".
- **Below the coordinator's bar of 6.0, so the method stops here.** Photographed plates fixed the "game level" look
  of the sky and the distance. They did not fix the near ground or the speakers' contact: an HDRI's ground is a
  projection at infinity, and a speaker stood on it reads as pasted. Passing that bar would take modelled foreground
  ground at scan quality under every speaker. That is what the single habitat pictures that score 6 to 6.7 have.

## Where this stands

| picture | file | blind | duel against the Fog headland |
|---|---|---|---|
| A, the eight-biome panorama (final) | `planet-earf-pano-master-4800.jpg`, `-2400`, `-1200` | 3.5 | 3.0 to 6.5 |
| B, Planet EARF (proof 7) | `proof7-planet.png` | 3.0 | - |
| C, a seam frame in the CG world | `seam-acid-ember-cg-1800.jpg` | - | - |
| C, a seam frame on photographed plates | `seam-poison-fog-plates-1800.jpg` | 3.5 | 3.5 to 6.0 |

The gate (7.0, or beating the best habitat) was not met by any of them. The phone frame was not made; the method it
would have used stopped first.

## Smoke aligned with the other seven (2026-11-01, the owner's note)

The owner, on seeing the eight habitats side by side: "The smoke image looks like the odd one out now, in terms of
speaker positioning in its setting. Anyway to align it with the rest? Maybe the fire in front is preventing it from
looking right."

**Measured** on the seven live portraits (`site/img/<key>-habitat-portrait.jpg`, 1200 x 1500), as fractions of the
frame:

| | Ember | Dust | Acid | Poison | Ice | Haze | Fog | median |
|---|---|---|---|---|---|---|---|---|
| center x | 0.50 | 0.47 | 0.51 | 0.50 | 0.64 | 0.63 | 0.51 | **0.51** |
| height | 0.40 | 0.36 | 0.42 | 0.37 | 0.43 | 0.41 | 0.41 | **0.41** |
| foot line | 0.79 | 0.68 | 0.73 | 0.79 | 0.77 | 0.88 | 0.79 | **0.79** |

Every camera sits at about eye level, with the horizon near the middle. The live Smoke had the speaker 0.25 of the
frame's height, in its crater, with flames and rubble in front of it.

**Re-composed** (`smoke_align.py`, from E12r p19's own shots in a worktree of r31-element-smoke-e10 at d55e7570):
- The speaker stands up out of its crater onto the intact road, 2.4 m toward the camera, upright and turned 22
  degrees toward it.
- The crater, the fire, the plume and the trench stay where they were, so the fire rises behind it and over its top,
  and the trench runs in from behind.
- The slab field thrown forward and the debris spread ahead of the crater are left out. Nothing stands in front of
  the speaker or its base.
- The heat shimmer is a 2D haze in the finish. It is kept off the speaker's new box; its old exclusion warped the
  speaker's edges.
- The camera is the other habitats': 60 mm from 6.5 m at 0.95 m for the landscape, 92 mm for the portrait.
- The speaker is linked from the speaker lane's asset at r33-speaker-horn c77460f0 (`assets/horn2/`, gitignored),
  cover off. The engine's own model is still built, so the shot's lamps find their parts by name, but it is hidden;
  the linked instance stands in its place in each lamp's light linking.

**Result** (48 samples, proofs), measured on the portrait: center x 0.50, height 0.41, feet at 0.78, which is the
median. The files are in `renders/2026-11-01/barkhorn/smoke-aligned/`:
- `smoke-aligned-2400x1600.jpg`;
- `smoke-aligned-portrait-1200x1500.jpg`;
- their shots;
- `strip-eight-4870x750.jpg`, the seven as they are and the new Smoke (`strip.py`).

The linked Smoke reads pale gray, with its white lining showing through the TruCast-2064 gray. The old model was near
black.
