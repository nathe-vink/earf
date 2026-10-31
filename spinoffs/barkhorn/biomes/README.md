# Planet EARF: the eight biomes in one world (r48-biomes)

The owner, 2026-10-31: "One thing that might be cool is an environmental image that blends each biome together,
showing speakers in each." And: "I mostly want to nail design, make it realistic, make it cooler".

## The idea

One world, one camera, one day. The eight habitats stand in a ring round the camera, each a 45-degree sector with its
Tropos on the sector's centre line, 3.6 m out, facing the lens and turned a little. Neighbours meet as geography does:
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
| `world.py` | Builds the world in Blender (Cycles) and renders the slices: the ground as eight wedge meshes carrying the weights, one ground material mixing eight Poly Haven ground sets at real size, redwoods, firs, ferns, oaks, desert shrubs and boulders, the city's blocks with lit windows and streetlights, one volume of air whose density and colour follow the biomes, the fog's sea, the volcano's plume. The speakers are **linked** collection instances: `--tropos other.blend` swaps the model. |
| `composite.py` | Lays the slices together (position pass -> field weights; sky by direction), each at its slice's exposure, and cuts the panorama and the planet, toned through AgX. |

Run:

    python3.11 spinoffs/barkhorn/biomes/tropos_lib.py
    python3.11 spinoffs/barkhorn/biomes/world.py --out OUT --width 2048 --samples 32
    python3.11 spinoffs/barkhorn/biomes/composite.py OUT --planet 1600

## Rounds

(below, newest last)
