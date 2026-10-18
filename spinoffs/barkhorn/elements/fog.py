"""Fog, concept A: on a summit above a sea of clouds (round 31b; BRIEF.md is the direction, fog.md the notes).

The owner's picture made real: "the speaker sitting on thick ... clouds, with blue skies in the backdrop, a flock of
birds in the distance out of focus". The clear speaker stands on a lichened granite summit in the morning; behind it a
dark boulder, so the clear cabinet reads against rock while the horn stands against the blue; beyond the ledge, far
below, a sea of cloud runs to the horizon, lit from the side by a low sun; a few birds cross it far off.
"""
from common import area, asset, camera, finish, ground, piece, portrait_of, scatter, shot as frame, sky, sun_from_sky

SKY, ROT = 'qwantani_puresky', 169.0             # the sun 28 degrees up at the front right (az 65): the sky behind at its bluest


def birds(cx, y, cz, n=6, span=0.9, seed=2):
    """A loose skein of birds far off over the clouds, dark against the bright deck."""
    import math, random
    r = random.Random(seed); out = []
    for i in range(n):
        k = (i + 1) // 2 * (1 if i % 2 else -1)
        out.append(piece('ext', module='fog_el', fn='bird', span=span * r.uniform(0.85, 1.1), flap=round(r.uniform(-0.8, 0.9), 2),
                         position=[cx + abs(k) * 1.6 + r.uniform(-0.3, 0.3), y + abs(k) * 2.0 + r.uniform(-1, 1),
                                   cz + k * 0.7 + r.uniform(-0.2, 0.2)],
                         rotate=[r.uniform(-6, 6), 0, 90 + r.uniform(-15, 15)]))
    return out


def props():
    p = []
    # the summit: lichened rock, level where the speaker stands, its far edge the drop 2.4 m behind it
    p.append(ground('lichen_rock', size=(18.0, 5.4), position=(1.0, -0.3, 0.0), displace=0.03, relief=0.12, res='2k',
                    cells=800))
    # a dark boulder right behind the cabinet: the clear acrylic reads against rock, the horn against the sky
    p.append(asset('boulder_01', position=(0.2, 1.4, -0.06), rotate=(0, 0, 200), scale=1.12))
    # the ledge's broken lip: a few boulders along the drop, gaps between them for the clouds
    p.append(scatter(['boulder_01'], 6, [-5.0, 2.2, 7.0, 2.6], avoid=[[0.2, 1.4, 1.6]], scale=(0.35, 0.8), seed=4, z=-0.12))
    # far below and away to the horizon, the sea of cloud
    p.append(piece('ext', module='fog_el', fn='cloudsea', near=250.0, far=26000.0, width=60000.0, z=-130.0,
                   billow=170.0, height=85.0, depth=140.0, x=3000.0, rows=300, cols=420, fan=2.6, seed=3,
                   sss_r=14.0, bump_size=10.0, bump_dist=4.0))
    # a peak standing out of it far off at the right, an island in the sea, blue with distance
    p.append(asset('mountainside', position=(7400.0, 9800.0, -640.0), rotate=(0, 0, -120), scale=85.0, res='1k'))
    # a skein of birds out over it, on the right, low against the sky
    p += birds(34.0, 60.0, 1.9, span=1.0)
    return p


def shot():
    cam = camera(height=0.75, distance=5.2, azimuth=-22.0, lens=50.0, target=(0.1, 0.0, 0.66), fstop=4.0)
    s = frame('fog', props(), cam, sky(SKY, ROT, strength=1.0, res='4k'), 'barkhorn, Fog, above the clouds',
              sun=sun_from_sky(SKY, ROT, irradiance=3.5),
              lights={'bounce': area(-40, 10, 3.0, 0.5, '#F4F1EC', (1.5, 1.5), (0.0, 0.0, 0.6))},
              haze={'box_m': [-40000.0, -60.0, -900.0, 40000.0, 30000.0, 300.0], 'density': 0.00004, 'anisotropy': 0.6,
                    'color': '#C9DCF0'},
              rotate_z=-6.0, fin=finish(contrast=0.05, vignette=0.12))
    s['render']['volume_bounces'] = 2
    s['camera']['clip_end'] = 40000.0                  # the sea of cloud runs out to the horizon
    return s


def portrait():
    return portrait_of(shot(), lens=42)
