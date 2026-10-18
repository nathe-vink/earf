"""Fog, concept A: on a summit above a sea of clouds (round 31b; BRIEF.md is the direction, fog.md the notes).

The owner's picture made real: "the speaker sitting on thick ... clouds, with blue skies in the backdrop, a flock of
birds in the distance out of focus". The clear speaker stands on the top of a scanned sandstone cliff in the morning
sun; beyond the edge, far below, a sea of cloud runs to the horizon; a few birds cross the blue far off.
"""
from common import area, asset, camera, finish, ground, piece, portrait_of, scatter, shot as frame, sky, sun_from_sky

SKY, ROT = 'mpumalanga_veld_puresky', 184.0      # a deep blue late-afternoon sky, its sun 8.5 degrees up behind the speaker on the left (az -130)


def birds(cx, y, cz, n=6, span=0.9, seed=2):
    """A loose skein of birds far off over the clouds, dark against the bright deck."""
    import math, random
    r = random.Random(seed); out = []
    for i in range(n):
        k = (i + 1) // 2 * (1 if i % 2 else -1)
        out.append(piece('ext', module='fog_el', fn='bird', span=span * r.uniform(0.85, 1.1), flap=round(r.uniform(-0.8, 0.9), 2),
                         position=[cx + abs(k) * 2.4 + r.uniform(-0.8, 0.8), y + abs(k) * 4.0 + r.uniform(-6, 6),
                                   cz + k * 0.9 + r.uniform(-0.6, 0.6)],
                         rotate=[r.uniform(-6, 6), 0, 90 + r.uniform(-15, 15)]))
    return out


def props():
    p = []
    # the summit: a scanned cliff top (Poly Haven, real scale); its flattest spot near the top, at (3.72, 3.11, 6.91) in
    # the scan, brought to the origin, the speaker's feet 35 mm into it (its stone is uneven by a few cm under them)
    p.append(asset('namaqualand_cliff_02', position=(-3.57, -3.11, -6.870), rotate=(0, 0, 0), scale=1.0, res='8k'))
    # the sea of cloud: near, real cloud (a volume with billows and wisps); far, a heaped deck out to the horizon
    # (the volume's box is held to what the lens sees, with a margin toward the sun, and its noise kept light: a
    # procedural volume is traced by null scattering, so its cost goes with its size, its peak density and its noise)
    p.append(piece('ext', module='fog_el', fn='cloudvol', box=[-400.0, 250.0, -230.0, 2600.0, 2800.0, -50.0],
                   top=-140.0, amp=110.0, scale=220.0, detail=7.0, erode=18.0, soft=0.5, density=0.14,
                   octaves=5, billow_octaves=4, anisotropy=0.65))
    p.append(piece('ext', module='fog_el', fn='cloudsea', near=2600.0, far=40000.0, width=120000.0, z=-170.0,
                   billow=140.0, height=45.0, depth=120.0, x=0.0, lean=0.4, rows=220, cols=480, fan=2.6, seed=3,
                   sss_r=20.0, bump_size=4.0, bump_dist=14.0))
    # a loose flock far off in the open sky, upper right
    p += birds(36.0, 62.0, 13.0, n=5, span=1.0, seed=5)
    return p


def shot():
    cam = camera(height=0.5, distance=6.8, azimuth=-22.0, lens=65.0, target=(0.45, 0.0, 0.75), focus=(0.0, -0.8, 0.5), fstop=11.0)
    s = frame('fog', props(), cam, sky(SKY, ROT, strength=1.0, res='4k'), 'barkhorn, Fog, above the clouds',
              sun=sun_from_sky(SKY, ROT, irradiance=3.5, color='#FFE2BE'),
              lights={'bounce': area(-30, 15, 2.5, 0.4, '#D9B49A', (2.0, 2.0), (0.0, 0.0, 0.6))},   # the warm rock's bounce, a soft lift
              haze={'box_m': [-20000.0, 200.0, -900.0, 50000.0, 40000.0, 300.0], 'density': 0.00014, 'anisotropy': 0.7,
                    'color': '#C9D6E6'},
              rotate_z=-6.0, fin=finish(contrast=0.08, vignette=0.12, saturation=0.12, lift=0.03, lift_color='#3A3530'), exposure=0.0,
              look='AgX - Medium High Contrast')
    s['render']['volume_bounces'] = 6                  # cloud is white because light scatters in it many times
    s['camera']['clip_end'] = 100000.0                  # the sea of cloud runs out to the horizon
    return s


def portrait():
    return portrait_of(shot(), lens=42)
