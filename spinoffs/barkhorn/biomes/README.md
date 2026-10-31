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
