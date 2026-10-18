"""Fog, concept A: on a summit above a sea of clouds (round 31b; BRIEF.md is the direction, fog.md the notes).

The owner's picture made real: "the speaker sitting on thick ... clouds, with blue skies in the backdrop, a flock of
birds in the distance out of focus". The clear speaker stands on the top of a scanned sandstone cliff in the morning
sun; beyond the edge, far below, a sea of cloud runs to the horizon; a few birds cross the blue far off.
"""
from common import area, asset, camera, finish, ground, piece, portrait_of, scatter, shot as frame, sky, sun_from_sky

SKY, ROT = 'qwantani_puresky', 354.0             # the sun 28 degrees up at the front right (az 60): raking light, the sky behind at its bluest


def birds(cx, y, cz, n=6, span=0.9, seed=2):
    """A loose flock far off over the clouds: different sizes, some gliding, some flapping, one banked, spread in depth,
    so no two read alike."""
    import random
    r = random.Random(seed); out = []
    flaps = [0.0, 0.85, -0.6, 0.0, 0.4, -0.25, 0.7]
    for i in range(n):
        k = (i + 1) // 2 * (1 if i % 2 else -1)
        d = r.uniform(0.75, 1.5)                                   # depth: nearer birds bigger and lower
        out.append(piece('ext', module='fog_el', fn='bird', span=span * r.uniform(0.6, 1.4), flap=flaps[i % len(flaps)],
                         position=[(cx + abs(k) * 2.4 + r.uniform(-0.8, 0.8)) * d, y * d,
                                   (cz + k * 0.9 + r.uniform(-0.6, 0.6)) * d],
                         rotate=[r.uniform(-8, 8) + (25 if i == 3 else 0), r.uniform(-10, 10), 90 + r.uniform(-25, 25)]))
    return out


def props():
    p = []
    # the summit: a scanned cliff top (Poly Haven, real scale); its flattest spot near the top, at (3.72, 3.11, 6.91) in
    # the scan, brought to the origin, the speaker's feet 35 mm into it (its stone is uneven by a few cm under them)
    # (round 2: the flattest standing place on the scan, found by ray casts over the footprint: (4.35, 3.30), level
    # within 4.8 cm, off the crack between two slabs; a fine grain bump on the scan so the stone holds texture at 1:1)
    p.append(piece('ext', module='fog_el', fn='scan', model='namaqualand_cliff_02', res='8k',
                   position=[-4.35, -3.30, -6.862], rotate=[0, 0, 0], scale=1.0, grain=0.006, strength=0.3))
    # the sea of cloud: near, real cloud (a volume with billows and wisps); far, a heaped deck out to the horizon
    # (the volume's box is held to what the lens sees, with a margin toward the sun, and its noise kept light: a
    # procedural volume is traced by null scattering, so its cost goes with its size, its peak density and its noise)
    p.append(piece('ext', module='fog_el', fn='cloudvol', box=[-400.0, 250.0, -230.0, 2600.0, 2800.0, -50.0],
                   top=-140.0, amp=110.0, scale=220.0, detail=7.0, erode=18.0, soft=0.5, density=0.14,
                   octaves=5, billow_octaves=4, anisotropy=0.65))
    p.append(piece('ext', module='fog_el', fn='cloudsea', near=2600.0, far=40000.0, width=90000.0, z=-170.0,
                   billow=260.0, height=65.0, depth=120.0, x=3000.0, rows=170, cols=380, fan=2.6, seed=3,
                   sss_r=8.0, bump_size=40.0, bump_dist=15.0, **{'break': 0.35}))
    # a loose flock far off in the open sky, upper right
    p += birds(36.0, 64.0, 11.5, n=7, span=1.0, seed=5)        # up to the right, clear of the horn
    return p


def shot():
    cam = camera(height=0.6, distance=6.8, azimuth=-22.0, lens=65.0, target=(0.1, 0.0, 0.7), fstop=8.0)
    s = frame('fog', props(), cam, sky(SKY, ROT, strength=1.0, res='4k'), 'barkhorn, Fog, above the clouds',
              sun=sun_from_sky(SKY, ROT, irradiance=3.5),
              lights={'bounce': area(-40, 0, 2.5, 0.3, '#D9B49A', (2.0, 2.0), (0.0, 0.0, 0.6))},   # the warm rock's bounce, low and gentle
              haze={'box_m': [-40000.0, 200.0, -900.0, 40000.0, 45000.0, 300.0], 'density': 0.00008, 'anisotropy': 0.6,
                    'color': '#BFD3EA'},
              rotate_z=-6.0, fin=finish(contrast=0.08, vignette=0.12, saturation=0.12, lift=0.03, lift_color='#3A3530'), exposure=0.0,
              look='AgX - Medium High Contrast')
    s['render']['volume_bounces'] = 6                  # cloud is white because light scatters in it many times
    s['camera']['clip_end'] = 60000.0                  # the sea of cloud runs out to the horizon
    return s


def portrait():
    # the same place on a longer lens, aimed a little higher: the speaker large in the tall frame, sky above it for type
    cam = camera(height=0.6, distance=6.8, azimuth=-22.0, lens=100.0, target=(0.1, 0.0, 0.82), fstop=8.0)
    return portrait_of(shot(), **cam)
