"""Smoke, setting E6: the salt pan, the smoke carrying it (the owner, 2026-10-20: "a smoke canister on a salt flat is so
random. It really comes down to the quality and pervasiveness of the smoke").

No source in sight. Beyond the low rise at the horizon a towering black plume climbs and shears off to the left in the
wind, spreading across half the sky. Its lower edge rolls across the pan toward the speaker in layers: far billows
merging into the plume, mid billows a few hundred metres off, and near wisps drifting low over the crust just behind the
speaker. The smoke's shadow lies across part of the crust; a low sun breaks through a gap and grazes the foreground,
where the speaker stands crisp on the white crust with its contact shadow.
"""
from common import area, camera, finish, ground, piece, shot as frame, portrait_of, sun_from_sky, sky
from smoke import SHELL, SPEAKER

SKY = 'aarfontein_pan'                      # a real dry lake bed with a low rise at its horizon (Poly Haven, CC0)
SKY_ROT = 124.0                             # its low sun to the front-left
SOOT = '#4A4744'                            # soot, but with enough albedo that the sunlit sides of the billows show


def smoke(position, size, density, seed, **k):
    return piece('ext', module='smoke_el', fn='woodsmoke', position=list(position), size=list(size), density=density,
                 seed=seed, color=k.pop('color', SOOT), **k)


def plume():
    """The tower: stacked cells rising from behind the rise, each wider and further left (the wind shear), black and
    dense low, torn and thinner high; then the layers that roll toward the speaker."""
    cells = []
    for k in range(7):
        t = k / 6
        w = 45 + 170 * t ** 1.4
        cells.append(smoke((150 - 200 * t ** 1.5, 300 - 40 * t, -5 + 42 * k), (w, 0.6 * w, 60), 0.9 * 0.8 ** k,
                           31 + k, scale=10 + 15 * t, cut=0.42 + 0.06 * t, soft=0.25, anisotropy=0.3,
                           fade=[0.25, 0.25, 0.35], floor=0.0, rise=1.2, detail_scale=3 + 4 * t, detail_weight=0.55))
    # the plume's head: a broad sheet sheared off the top, spreading across half the sky toward and over the camera
    cells.append(smoke((-320, 760, 200), (1000, 640, 130), 0.05, 39, scale=55.0, cut=0.4, soft=0.35, anisotropy=0.3,
                       fade=[0.15, 0.2, 0.45], floor=0.0, rise=0.6, detail_scale=18.0, detail_weight=0.5))
    # layers rolling low toward the speaker, nearer ones lower and finer
    for i, (y, w, d, h, dens, sc) in enumerate([(170, 200, 90, 26, 0.25, 9.0), (85, 120, 50, 12, 0.35, 4.0),
                                                 (45, 80, 26, 6.0, 0.5, 2.2), (22, 60, 20, 4.0, 0.6, 1.4),
                                                 (11, 40, 8, 1.6, 0.45, 0.7)]):
        cells.append(smoke((20 - 0.25 * y, y, -0.3), (w, d, h), 0.8 * dens, 41 + i, scale=sc, cut=0.56, soft=0.28,
                           anisotropy=0.3, fade=[0.2, 0.3, 0.55], floor=0.0, rise=1.3, detail_scale=sc / 4,
                           detail_weight=0.5))
    # haze toward the horizon: smoke thinned out over the whole pan
    cells.append(smoke((0, 500, -1), (1600, 900, 45), 0.0025, 49, scale=200.0, cut=0.0, soft=0.9, anisotropy=0.2,
                       fade=[0.1, 0.1, 0.7], floor=0.0025, color='#8C8C8C'))
    return cells


def shot():
    props = [ground('dry_ground_01', size=(40.0, 40.0), position=(0.0, 14.0, 0.0), displace=0.0, relief=0.05,
                    res='4k', tint='#F0EEEA', tint_mix=0.95, bump=2.0, tex_scale=7.0),
             # the plume's shadow across part of the pan, and the gap the sun comes through onto the foreground
             piece('ext', module='smoke_el', fn='canopy', size=[600.0, 600.0], z=20.0, position=[-60.0, 60.0],
                   scale=15.0, open=0.35, seed=7)] + plume() + [
        # the contact shadow: a shadow-only disc in the cabinet's base, blocking the sky over the crust beneath it
        piece('ext', module='smoke_el', fn='occluder', position=[0.0, 0.0, 0.03], radius=0.36, sx=1.0, sy=0.9, rotate_z=18.0)]
    cam = camera(height=0.8, distance=4.4, azimuth=-20, lens=40, target=(0.0, 0.0, 0.85), fstop=4.0, shift_x=0.08,
                 shift_y=0.06)
    cam['clip_end'] = 3000
    lights = {
        'skyfill': {**area(-20, 5, 2.4, 2.0, '#DCE2EA', (4.0, 3.0), (0.0, 0.0, 0.6)), 'receivers': SPEAKER},
        'bounce': {**area(-25, 12, 2.0, 6.0, '#E6E2DA', (2.4, 2.4), (0.0, 0.0, 0.6)), 'receivers': SPEAKER},
        'kicker': {**area(-150, 22, 3.0, 22.0, '#FFE6CC', (0.5, 2.4), (0.0, 0.0, 0.8)), 'receivers': SHELL},
        'kicker_r': {**area(150, 14, 3.0, 16.0, '#FFE6CC', (0.6, 2.4), (0.0, 0.0, 0.8)), 'receivers': SHELL},
    }
    return frame('smoke_pan', props, cam, sky(SKY, rotation_deg=SKY_ROT, strength=0.8),
                 'barkhorn, Smoke, black smoke over a salt pan', sun={**sun_from_sky(SKY, SKY_ROT, irradiance=9.0),
                                                                     'elevation_deg': 22.0, 'angle_deg': 1.5},
                 lights=lights, rotate_z=18.0, position=(0.0, 0.0, -0.01), samples=512, exposure=0.3,
                 fin=finish(contrast=0.06, clarity=0.04, saturation=-0.85, vignette=0.15))


def portrait():
    sh = shot()
    return portrait_of(sh, **camera(height=0.8, distance=4.6, azimuth=-20, lens=50, target=(0.0, 0.0, 0.85), fstop=4.0,
                                    shift_y=-0.05))
