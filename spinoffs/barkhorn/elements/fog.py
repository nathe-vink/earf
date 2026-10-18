"""Fog, concept A: on a summit above a sea of clouds (round 31b; BRIEF.md is the direction, fog.md the notes).

The owner's picture made real: "the speaker sitting on thick ... clouds, with blue skies in the backdrop, a flock of
birds in the distance out of focus". The clear speaker stands on a lichened granite summit in the morning; behind it a
dark boulder, so the clear cabinet reads against rock while the horn stands against the blue; beyond the ledge, far
below, a sea of cloud runs to the horizon, lit from the side by a low sun; a few birds cross it far off.
"""
from common import area, asset, camera, finish, ground, piece, portrait_of, scatter, shot as frame, sky, sun_from_sky

SKY, ROT = 'qwantani_puresky', 189.0             # the sun 28 degrees up, behind the speaker on the camera's left (az -135)


def birds(cx, y, cz, n=6, span=0.9, seed=2):
    """A loose skein of birds far off over the clouds, dark against the bright deck."""
    import math, random
    r = random.Random(seed); out = []
    for i in range(n):
        k = (i + 1) // 2 * (1 if i % 2 else -1)
        out.append(piece('ext', module='fog_el', fn='bird', span=span * r.uniform(0.85, 1.1), flap=round(r.uniform(-0.8, 0.9), 2),
                         position=[cx + i * 2.2 + r.uniform(-0.8, 0.8), y + r.uniform(-4, 4),
                                   cz + i * 0.35 + r.uniform(-0.9, 0.9)],
                         rotate=[r.uniform(-6, 6), 0, 90 + r.uniform(-15, 15)]))
    return out


def props():
    p = []
    # the summit: lichened rock at 4k, level where the speaker stands, with broad relief round it
    p.append(ground('lichen_rock', size=(14.0, 7.0), position=(0.5, -0.3, 0.0), displace=0.07, relief=0.15, res='4k',
                    cells=1100))
    # one boulder for scale, camera-left, clear of the cabinet
    p.append(asset('boulder_01', position=(-1.05, 1.7, -0.08), rotate=(0, 0, 200), scale=0.75))
    # the sea of cloud: near, real cloud (a volume with billows and wisps); far, a heaped deck out to the horizon
    p.append(piece('ext', module='fog_el', fn='cloudvol', box=[-3000.0, 250.0, -170.0, 6000.0, 3200.0, -10.0],
                   top=-90.0, amp=110.0, scale=220.0, detail=26.0, erode=28.0, soft=4.0, density=0.09,
                   anisotropy=0.65))
    p.append(piece('ext', module='fog_el', fn='cloudsea', near=2800.0, far=26000.0, width=60000.0, z=-120.0,
                   billow=260.0, height=65.0, depth=120.0, x=3000.0, rows=160, cols=380, fan=2.6, seed=3,
                   sss_r=20.0, bump_size=14.0, bump_dist=5.0))
    # a loose flock far off in the open sky, upper right
    p += birds(26.0, 60.0, 10.5, n=11, span=1.0)
    return p


def shot():
    cam = camera(height=0.75, distance=5.2, azimuth=-22.0, lens=50.0, target=(0.1, 0.0, 0.66), fstop=4.0)
    s = frame('fog', props(), cam, sky(SKY, ROT, strength=1.0, res='4k'), 'barkhorn, Fog, above the clouds',
              sun=sun_from_sky(SKY, ROT, irradiance=3.5),
              lights={'bounce': area(-40, 10, 3.0, 0.25, '#F4F1EC', (1.5, 1.5), (0.0, 0.0, 0.6))},
              haze={'box_m': [-40000.0, -60.0, -900.0, 40000.0, 30000.0, 300.0], 'density': 0.00004, 'anisotropy': 0.6,
                    'color': '#C9DCF0'},
              rotate_z=-6.0, fin=finish(contrast=0.08, vignette=0.12), exposure=0.3,
              look='AgX - Medium High Contrast')
    s['render']['volume_bounces'] = 6                  # cloud is white because light scatters in it many times
    s['camera']['clip_end'] = 40000.0                  # the sea of cloud runs out to the horizon
    return s


def portrait():
    return portrait_of(shot(), lens=42)
