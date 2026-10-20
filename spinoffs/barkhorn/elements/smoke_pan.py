"""Smoke, setting E6: the salt pan, the smoke carrying it (the owner, 2026-10-20: "a smoke canister on a salt flat is so
random. It really comes down to the quality and pervasiveness of the smoke").

No source in sight. Across the white pan three low folds of land stand one behind another, each lighter and bluer with
distance. From behind the far ones a black plume climbs and its top shears off downwind into a layered sheet across a
third of the sky, thinning as it goes; its shadow lies across the far pan as a darker band. The sun comes through the
smoke's thin edge, dimmed and warm, so its shadows are soft. Low smoke rolls across the pan toward the speaker, which
stands on the crust with its contact shadow, its horn reflecting the sky's gradient and the plume.
"""
import math, random

from common import area, camera, finish, ground, piece, shot as frame, portrait_of, sky
from smoke import SHELL, SPEAKER

SKY = 'aarfontein_pan'                      # a real dry lake bed (Poly Haven, CC0); its own hills hidden by the folds
SKY_ROT = 124.0
SOOT = '#5A4E44'                            # soot: low albedo, not zero, brown-grey where the sun catches the billows
# a low warm sun from the front left through thin high haze: a defined shadow with a softened edge
SUN = {'azimuth_deg': -70.0, 'elevation_deg': 22.0, 'irradiance': 9.0, 'angle_deg': 1.75, 'color': '#FFD2A0'}
# the rims light the cabinet, not the horn's mirror top (they burnt it to a white field)
RIM = [s for s in SHELL if s not in ('waveguide', 'waveguide-cap')]


def smoke(position, size, density, seed, **k):
    return piece('ext', module='smoke_el', fn='woodsmoke', position=list(position), size=list(size), density=density,
                 seed=seed, color=k.pop('color', SOOT), **k)


def plume():
    """The tower behind the far folds, its top sheared into a layered sheet downwind (left) across a third of the sky,
    and the layers that roll across the pan toward the speaker."""
    cells = []
    for k in range(7):
        t = k / 6
        w = 90 + 420 * t ** 1.4
        cells.append(smoke((320 - 650 * t ** 1.8, 640 - 120 * t, -10 + 62 * k), (w, 0.6 * w, 95), 0.45 * 0.8 ** k,
                           31 + k, scale=20 + 25 * t, cut=0.42 + 0.06 * t, soft=0.25, anisotropy=0.45,
                           fade=[0.25, 0.25, 0.35], floor=0.0, rise=1.2, detail_scale=4 + 4 * t, detail_weight=0.6,
                           distortion=1.3, detail=8.0))
    # the sheet: three thin layers off the tower's top, drifting left and toward the camera, thinning with distance
    # (it leaves the tower's sheared top and runs on downwind, so nothing hangs apart from the column)
    for i, (dx, y, z, w, d, h, dens) in enumerate([(-650, 480, 330, 700, 420, 70, 0.08), (-950, 430, 300, 800, 520, 60, 0.05)]):
        cells.append(smoke((dx, y, z), (w, d, h), dens, 51 + i, scale=60.0, cut=0.42, soft=0.3, anisotropy=0.4,
                           fade=[0.25, 0.25, 0.4], floor=0.0, rise=0.5, detail_scale=15.0, detail_weight=0.55))
    # layers rolling low toward the speaker, nearer ones lower and finer
    for i, (y, w, d, h, dens, sc) in enumerate([(120, 200, 80, 10, 0.1, 5.0),
                                                 (60, 120, 40, 7.0, 0.4, 2.6), (28, 70, 20, 4.0, 0.48, 1.5),
                                                 (12, 40, 8, 1.6, 0.36, 0.7)]):
        cells.append(smoke((40 - 0.35 * y, y, -0.3), (w, d, h), dens, 41 + i, scale=sc, cut=0.56, soft=0.28,
                           anisotropy=0.3, fade=[0.2, 0.3, 0.55], floor=0.0, rise=1.3, detail_scale=sc / 4,
                           detail_weight=0.5))
    # haze: smoke thinned over the whole pan, which lightens and blues the far folds
    cells.append(smoke((0, 600, -1), (3000, 1200, 60), 0.0007, 49, scale=200.0, cut=0.0, soft=0.9, anisotropy=0.2,
                       fade=[0.1, 0.1, 0.7], floor=0.0007, color='#9AA0A8'))
    return cells


def land():
    """The pan: fine crust near the camera, the same crust at a larger cell beyond, salt patches, and three folds."""
    out = [ground('dry_ground_01', size=(40.0, 40.0), position=(0.0, 14.0, 0.0), displace=0.0, relief=0.05, res='4k',
                  tint='#F0EEEA', tint_mix=0.95, bump=2.0, tex_scale=7.0, cells=1100),
           # beyond: the pan to the folds, the crust at a cell three times as large (no repeat to read at distance)
           piece('box', size=[3000.0, 1400.0, 0.2], position=[0.0, 733.0, -0.21], material='pbr', texture='dry_ground_01',
                 tex_scale=22.0, tint='#ECEAE6', tint_mix=0.95)]
    # salt-crust patches: whiter, a larger crack, on the mid-pan where depth of field softens their margins
    rnd = random.Random(12)
    for k in range(14):
        cx, cy = (rnd.uniform(-8, 10), rnd.uniform(3, 15)) if k >= 7 else (rnd.uniform(-25, 30), rnd.uniform(16, 60))
        rx, ry = rnd.uniform(3, 9), rnd.uniform(2, 5)
        ph = [rnd.uniform(0, 6.28) for _ in range(3)]
        outline = []
        for i in range(40):
            a = 2 * math.pi * i / 40
            r = 1.0 + 0.2 * math.sin(3 * a + ph[0]) + 0.1 * math.sin(7 * a + ph[1]) + 0.05 * math.sin(13 * a + ph[2])
            outline.append([round(rx * r * math.cos(a), 3), round(ry * r * math.sin(a), 3)])
        out.append(piece('extrude', outline=outline, depth=0.004, position=[cx, cy, 0.001], rotate=[90.0, 0.0, rnd.uniform(0, 180)],
                         material='pbr', texture='dry_ground_01', tex_scale=13.0, tint='#F6F5F2', tint_mix=0.97,
                         ease=0.001))
    # the folds: nearest darkest, each further one lighter and bluer
    for i, (y, h, col, col2) in enumerate([(330, [4, 14], '#6C6863', '#4C4842'), (540, [22, 50], '#83837F', '#686763'),
                                           (860, [55, 110], '#999DA3', '#868A90')]):
        out.append(piece('ext', module='smoke_el', fn='ridge', position=[0.0, y], width=3000.0, depth=120.0 + 60 * i,
                         height=h, scale=260.0 + 100 * i, seed=3 + i, color=col, color2=col2, mottle=4.0 + 12 * i,
                         gullies=3.0 if i == 0 else 0.0, gully_scale=14.0, cells=[1500, 24] if i == 0 else [600, 8]))
    return out


def shot():
    props = land() + plume() + [
        # the plume's shadow: a high band of smoke between the sun and the far pan (shadow only, unseen)
        piece('ext', module='smoke_el', fn='canopy', size=[900.0, 260.0], z=90.0, position=[-120.0, 200.0],
              scale=60.0, open=0.35, seed=9),
        # a black flag high behind the camera, out of frame, so the horn's polished resin mirrors dark there, not a
        # white field of sky (an ordinary object, as a photographer would rig it)
        piece('box', size=[1.2, 0.02, 1.2], position=[-2.1, -5.9, 1.9], rotate=[-20.0, 0.0, -20.0], material='clay',
              color='#050505'),
        # the contact shadow: a shadow-only disc in the cabinet's base, blocking the sky over the crust beneath it
        piece('ext', module='smoke_el', fn='occluder', position=[0.0, 0.0, 0.03], radius=0.36, sx=1.0, sy=0.9, rotate_z=18.0)]
    cam = camera(height=0.8, distance=4.4, azimuth=-20, lens=40, target=(0.0, 0.0, 0.85), fstop=4.0, shift_x=0.08,
                 shift_y=0.06)
    cam['clip_end'] = 3000
    lights = {
        'skyfill': {**area(-20, 5, 2.4, 2.4, '#DCE2EA', (4.0, 3.0), (0.0, 0.0, 0.6)), 'receivers': SPEAKER},
        'bounce': {**area(-25, 12, 2.0, 6.0, '#E6E2DA', (2.4, 2.4), (0.0, 0.0, 0.6)), 'receivers': SPEAKER},
        'kicker': {**area(-150, 22, 3.0, 22.0, '#FFE2C4', (0.5, 2.4), (0.0, 0.0, 0.8)), 'receivers': RIM},
        'kicker_r': {**area(150, 14, 3.0, 16.0, '#FFE2C4', (0.6, 2.4), (0.0, 0.0, 0.8)), 'receivers': RIM},
    }
    return frame('smoke_pan', props, cam, {**sky(SKY, rotation_deg=SKY_ROT, strength=0.8), 'grade': {'horizon': '#FFE9D2', 'zenith': '#C8D0DC', 'height_deg': 35.0}},
                 'barkhorn, Smoke, black smoke over a salt pan', sun=SUN, lights=lights, rotate_z=18.0,
                 position=(0.0, 0.0, -0.01), samples=512, exposure=0.3,
                 fin={**finish(contrast=0.06, clarity=0.04, saturation=-0.55, vignette=0.15), 'grain': 2.5})


def portrait():
    sh = shot()
    return portrait_of(sh, **camera(height=0.8, distance=4.6, azimuth=-20, lens=50, target=(0.0, 0.0, 0.85), fstop=4.0,
                                    shift_y=-0.05))
