# Render queue: the honest site lamp pictures (2026-11-09)

**Rig:** `spinoffs/barkhorn/companions/lamp_site.py`, on branch `r32-lamps-final`. Use the SHA this file was sent with.

**Split:**
- **Hemisphere** (`dome-*`, `lamps-domes`): rendered by the lamps lane.
- **Core** (`orb-*`, `lamps-orbs`): split between the two helpers below.

## What a helper needs

1. **A checkout** of `r32-lamps-final` at the given SHA:
   ```
   git fetch origin r32-lamps-final && git checkout <SHA>
   ```
2. **Python 3.11 with Blender's `bpy` wheel, version 5.0:**
   ```
   python3.11 -m pip install bpy==5.0.*
   ```
   - It's about 350 MB and renders with Cycles on the CPU.
   - Install it in a Python with numpy 1. `bpy` needs numpy 1; never install the CAD packages into the same Python.
3. **Nothing else.**
   - The CAD meshes ship on the branch in `spinoffs/barkhorn/companions/lamp-site-meshes/` (17 STLs, 3.4 MB).
   - These are copies of the fabkit builds of 2026-11-03: `orb_table.py` at 10:01 UTC and `dome_pendant.py` at 10:42 UTC. The CAD source last changed at 10:42:06; that change was to the notes only.
   - No HDRI, textures or other assets. The world is a flat colour and the set is built in code.
   - No network access is needed.

**Check before rendering:**
```
AUDIT=1 python3.11 spinoffs/barkhorn/companions/lamp_site.py orb-red --samples 1 --scale 0.2
```
It must print:
```
AUDIT orb-red hidden [] no-shadow [] lights [('key', 'AREA', 480.0), ('fill', 'AREA', 160.0)]
```
That is, no hidden meshes, no meshes without shadows, and the studio key and fill at ×8.

## The commands

Run each from the repository root, one frame per command, one at a time (Cycles uses every core).
- Each frame writes `renders/2026-11-09/barkhorn/lamp-site/<frame>.png`.
- Leave `LAMP_OUT` unset.
- Leave `STUDIO` and `EV` unset: each frame's defaults are part of the rig.

**Helper 1 (c3)**, about 2.5 hours:
```
python3.11 spinoffs/barkhorn/companions/lamp_site.py orb-red    --samples 384
python3.11 spinoffs/barkhorn/companions/lamp_site.py orb-orange --samples 384
python3.11 spinoffs/barkhorn/companions/lamp_site.py orb-amber  --samples 384
python3.11 spinoffs/barkhorn/companions/lamp_site.py orb-green  --samples 384
python3.11 spinoffs/barkhorn/companions/lamp_site.py lamps-orbs --samples 384
```

**Helper 2 (c4)**, about 2 hours:
```
python3.11 spinoffs/barkhorn/companions/lamp_site.py orb-blue   --samples 384
python3.11 spinoffs/barkhorn/companions/lamp_site.py orb-violet --samples 384
python3.11 spinoffs/barkhorn/companions/lamp_site.py orb-ice    --samples 384
python3.11 spinoffs/barkhorn/companions/lamp_site.py orb-black  --samples 384
```

**The lamps lane** (Hemisphere, already running here):
```
python3.11 spinoffs/barkhorn/companions/lamp_site.py dome-<colour> --samples 256   (x8: red orange amber green blue violet ice black)
python3.11 spinoffs/barkhorn/companions/lamp_site.py lamps-domes --samples 256
```

## Expected output

| Frame | Size | Notes |
|---|---|---|
| `orb-<colour>.png` | 1600 x 2000 | Core A lit on its dock, on the paper sweep |
| `lamps-orbs.png` | 2400 x 800 | the eight in a row, Ember to Smoke |
| `dome-<colour>.png` | 1600 x 2000 | Hemisphere lit, its pool on the paper |
| `lamps-domes.png` | 2400 x 800 | the eight in a row |

Each PNG is about 2-4 MB, under the repository's 5 MB limit.

**Hand-back:** commit the PNGs to your own branch, add a log line with each frame's wall time, and send the SHA. The lamps lane fetches them and then:
- checks each against the proxies;
- cuts the 640 x 800 cards and the 1200 x 400 rows;
- copies them by name into `renders/2026-10-31/barkhorn/lamps-cordless/site-img/`;
- sends one SHA for the set.

**Colour keys** (the site's `web.py`):

| Key | Tint |
|---|---|
| red | Ember |
| orange | Dust |
| amber | Acid |
| green | Poison |
| blue | Ice |
| violet | Haze |
| ice | Fog |
| black | Smoke (the dark grade) |
