"""Smoke, concept A: woodsmoke backlit in a pine forest at dawn (round 31b; BRIEF.md, notes in smoke.md).

The speaker stands on the needle floor of a pine wood just after sunrise. Woodsmoke from a fire out of frame drifts
between the trunks behind it, and the low sun behind the smoke turns it to a glowing wall, cut into shafts by the trunks.
The smoked black speaker stands in front of that glow, so it reads as a clean dark silhouette rimmed in warm light, and
the light that comes through its acrylic shows its tint.
"""
from common import area, asset, camera, finish, ground, piece, scatter, shot as frame, sky, portrait_of

SKY = 'misty_pines'           # a real pine wood in morning mist (Poly Haven, CC0)
SUN = {'azimuth_deg': 164.0, 'elevation_deg': 8.0, 'irradiance': 24.0, 'angle_deg': 0.5, 'color': '#FFB978'}


def smoke(position, size, density, seed, **k):
    return piece('ext', module='smoke_el', fn='woodsmoke', position=list(position), size=list(size), density=density,
                 seed=seed, **k)


def trees(n=46, seed=3):
    """Pine trunks at real scale behind and beside the speaker, thickest toward the sun (back right), so their shadows
    stripe the sunlit smoke into shafts; none within 2.5 m behind the speaker, none in front of it.
    [x, y, radius, height, lean, lean direction, seed]."""
    import random
    rnd = random.Random(seed)
    t, tries = [], 0
    while len(t) < n and tries < 5000:
        tries += 1
        x, y = rnd.uniform(-12, 16), rnd.uniform(2.5, 30)
        if y < 3.5 and abs(x) < 2.0:                     # clear of the speaker's silhouette and its shadow
            continue
        if any((x - u) ** 2 + (y - v) ** 2 < 1.6 ** 2 for u, v, *_ in t):
            continue
        if x < -2 and rnd.random() < 0.45:               # sparser away from the sun
            continue
        t.append([round(x, 2), round(y, 2), round(rnd.uniform(0.15, 0.27), 3), 18, round(rnd.uniform(0, 2.5), 1),
                  rnd.randrange(360), len(t) + 1])
    return [piece('ext', module='smoke_el', fn='trunks', trees=t, texture='pine_bark', res='2k', bump=2.2,
                  tint='#1E1A17', tint_mix=0.75)]


def shot():
    props = [ground('forest_leaves_04', size=(40.0, 40.0), position=(0.0, 10.0, 0.0), displace=0.02, res='2k'),
             scatter(['pine_roots'], 3, [-2.5, 0.5, 3.0, 3.5], avoid=[(0.0, 0.0, 1.2), (0.6, -2.0, 1.5)], seed=4, res='1k'),
             smoke((2.5, 7.5, 0.0), (20.0, 12.0, 6.0), 0.22, 1, scale=3.0, cut=0.55, soft=0.3, anisotropy=0.85,
                   fade=[0.12, 0.2, 0.55], floor=0.012)]
    props += trees()
    cam = camera(height=0.8, distance=7.2, azimuth=-20, lens=65, target=(0.0, 0.0, 0.7), fstop=4.0, shift_x=0.14)
    lights = {
        # the sunlit litter in front of the speaker bounces warm light up into its face: a low, broad source
        'bounce': area(-30, 8, 2.2, 0.35, '#C89A6A', (1.6, 1.6), (0.0, 0.0, 0.6)),
        # the sun's light off the smoke behind-left, a thin warm rim down the cabinet's left edge
        'kicker': area(-150, 10, 3.0, 6.0, '#FFB978', (0.5, 2.0), (0.0, 0.0, 0.8)),
    }
    return frame('smoke', props, cam, sky(SKY, rotation_deg=0.0, strength=0.12), 'barkhorn, Smoke, woodsmoke at dawn',
                 sun=SUN, lights=lights, rotate_z=18.0, position=(0.0, 0.0, -0.006), samples=512,
                 fin=finish(contrast=0.04, clarity=0.10, bloom=0.08, bloom_px=40, threshold=0.85, vignette=0.15))


def portrait():
    return portrait_of(shot(), lens=50)
