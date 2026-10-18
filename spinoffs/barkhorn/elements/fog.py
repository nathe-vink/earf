"""Fog, concept A: on a summit above a sea of clouds (round 31b; BRIEF.md is the direction, fog.md the notes).

The owner's picture made real: "the speaker sitting on thick ... clouds, with blue skies in the backdrop, a flock of
birds in the distance out of focus". The clear speaker stands on the top of a scanned sandstone cliff in the morning
sun; beyond the edge, far below, a sea of cloud runs to the horizon; a few birds cross the blue far off.
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
    # the summit: a scanned cliff top (Poly Haven, real scale); its flattest spot near the top, at (3.72, 3.11, 6.91) in
    # the scan, brought to the origin, the speaker's feet 35 mm into it (its stone is uneven by a few cm under them)
    p.append(asset('namaqualand_cliff_02', position=(-3.72, -3.11, -6.875), rotate=(0, 0, 0), scale=1.0, res='4k'))
    # the sea of cloud: near, real cloud (a volume with billows and wisps); far, a heaped deck out to the horizon
    # (the volume's box is held to what the lens sees, with a margin toward the sun, and its noise kept light: a
    # procedural volume is traced by null scattering, so its cost goes with its size, its peak density and its noise)
    p.append(piece('ext', module='fog_el', fn='cloudvol', box=[-400.0, 250.0, -170.0, 2600.0, 2800.0, -10.0],
                   top=-90.0, amp=110.0, scale=220.0, detail=12.0, erode=18.0, soft=1.2, density=0.14,
                   octaves=4, billow_octaves=3, anisotropy=0.65))
    p.append(piece('ext', module='fog_el', fn='cloudsea', near=2600.0, far=40000.0, width=90000.0, z=-120.0,
                   billow=260.0, height=65.0, depth=120.0, x=3000.0, rows=170, cols=380, fan=2.6, seed=3,
                   sss_r=20.0, bump_size=14.0, bump_dist=5.0))
    # a loose flock far off in the open sky, upper right
    p += birds(26.0, 60.0, 10.5, n=11, span=1.0)
    return p


def shot():
    cam = camera(height=0.82, distance=6.8, azimuth=-22.0, lens=65.0, target=(0.1, 0.0, 0.7), fstop=4.0)
    s = frame('fog', props(), cam, sky(SKY, ROT, strength=1.0, res='4k'), 'barkhorn, Fog, above the clouds',
              sun=sun_from_sky(SKY, ROT, irradiance=3.5),
              lights={'bounce': area(-60, 18, 2.5, 0.5, '#F2EAE0', (2.0, 2.0), (0.0, 0.0, 0.6))},
              haze={'box_m': [-40000.0, 200.0, -900.0, 40000.0, 45000.0, 300.0], 'density': 0.00008, 'anisotropy': 0.6,
                    'color': '#BFD3EA'},
              rotate_z=-6.0, fin=finish(contrast=0.08, vignette=0.12), exposure=0.3,
              look='AgX - Medium High Contrast')
    s['render']['volume_bounces'] = 6                  # cloud is white because light scatters in it many times
    s['camera']['clip_end'] = 60000.0                  # the sea of cloud runs out to the horizon
    return s


def portrait():
    return portrait_of(shot(), lens=42)
