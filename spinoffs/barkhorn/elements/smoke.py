"""Smoke, concept A: woodsmoke backlit in a pine forest at dawn (round 31b; BRIEF.md, notes in smoke.md).

The speaker stands on the needle floor of a pine wood just after sunrise. Woodsmoke from a fire out of frame drifts
between the trunks behind it, and the low sun behind the smoke turns it to a glowing wall, cut into shafts by the trunks.
The smoked black speaker stands in front of that glow, so it reads as a clean dark silhouette rimmed in warm light, and
the light that comes through its acrylic shows its tint.
"""
from common import area, asset, camera, finish, ground, piece, scatter, shot as frame, sky, portrait_of

SKY = 'misty_pines'           # a real pine wood in morning mist (Poly Haven, CC0)
SUN = {'azimuth_deg': 150.0, 'elevation_deg': 16.0, 'irradiance': 30.0, 'angle_deg': 0.5, 'color': '#FFB978'}


# the speaker's outer parts: the kickers light these alone, so they rim the speaker without outlining the trunks
SHELL = ['left', 'right', 'top', 'bottom', 'front-panel', 'back', 'waveguide', 'waveguide-cap', 'woofer-ring', 'post-*',
         'grip-*', 'port-frame-*']


BODY = [n for n in SHELL if not n.startswith('waveguide')]          # the cabinet without the horn


def smoke(position, size, density, seed, **k):
    return piece('ext', module='smoke_el', fn='woodsmoke', position=list(position), size=list(size), density=density,
                 seed=seed, **k)


def trees(n=22, seed=3):
    """Pine trunks at real scale near the speaker, where their bark holds up: 2.5 to 14 m behind it, thickest toward the
    sun (back right), so their shadows stripe the sunlit smoke into shafts. Beyond them the photographed pine wood (the
    sky map) carries on into the mist. Two dark trunks close to the camera frame the left edge.
    [x, y, radius, height, lean, lean direction, seed]."""
    import random
    rnd = random.Random(seed)
    t, tries = [[-3.35, -4.3, 0.3, 18, 1.0, 200, 101], [-4.1, -2.4, 0.26, 18, 2.5, 330, 102]], 0
    while len(t) < n and tries < 5000:
        tries += 1
        x, y = rnd.uniform(-9, 12), rnd.uniform(2.5, 14)
        if y < 3.5 and abs(x) < 2.0:                     # clear of the speaker's silhouette and its shadow
            continue
        if any((x - u) ** 2 + (y - v) ** 2 < 1.8 ** 2 for u, v, *_ in t):
            continue
        if x < -2 and rnd.random() < 0.45:               # sparser away from the sun
            continue
        t.append([round(x, 2), round(y, 2), round(rnd.uniform(0.10, 0.42), 3), 18, round(rnd.uniform(0, 6.0), 1),
                  rnd.randrange(360), len(t) + 1])
    # a farther rank, 14 to 25 m back, so the depth under the smoke is trees, not the photograph
    far, tries = [], 0
    while len(far) < 10 and tries < 5000:
        tries += 1
        x, y = rnd.uniform(-14, 18), rnd.uniform(14, 25)
        if any((x - u) ** 2 + (y - v) ** 2 < 2.2 ** 2 for u, v, *_ in t + far):
            continue
        far.append([round(x, 2), round(y, 2), round(rnd.uniform(0.15, 0.4), 3), 18, round(rnd.uniform(0, 4.0), 1),
                    rnd.randrange(360), 200 + len(far)])
    near = [q for q in t if q[1] < 6.0]
    mid = [q for q in t if q[1] >= 6.0]
    bark = dict(texture='pine_bark', res='2k', tint='#1E1A17', tint_mix=0.15, tex_scale=1.6)
    return [piece('ext', module='smoke_el', fn='trunks', trees=near, bump=3.0, displace=0.025, sides=96, rings=180, **bark),
            piece('ext', module='smoke_el', fn='trunks', trees=mid + far, bump=5.0, **bark)]


def shot():
    props = [ground('forest_leaves_04', size=(40.0, 40.0), position=(0.0, 10.0, 0.0), displace=0.06, relief=0.12,
                    res='2k', tint='#4A3626', tint_mix=0.3),
             scatter(['dry_branches_medium_01'], 5, [-5.0, 4.0, 7.0, 12.0], avoid=[(0.0, 0.0, 2.5)], seed=4, res='1k', z=-0.015),
             # the smoke hangs between the trunks; beyond it the photographed wood shows through the mist
             smoke((0.5, 8.5, 0.0), (44.0, 17.0, 14.0), 0.10, 1, scale=3.0, cut=0.5, soft=0.15, anisotropy=0.85,
                   fade=[0.3, 0.35, 0.45], floor=0.06, ground=0.18, ground_h=1.6)]
    props += trees()
    cam = camera(height=0.7, distance=7.2, azimuth=-20, lens=65, target=(0.0, 0.0, 0.7), fstop=4.0, shift_x=0.14)
    lights = {
        # the open sky behind the camera, cool, lifting the shadow side: the woofer and lining just read in the tint
        'skyfill': area(-20, 5, 2.4, 4.0, '#9FB0C8', (4.0, 3.0), (0.0, 0.0, 0.6)),
        # the sunlit litter and the sky bounce into its face: low, broad and cool-neutral
        'bounce': area(-25, 12, 2.0, 7.0, '#C9BBA8', (2.4, 2.4), (0.0, 0.0, 0.6)),
        # the sun's light off the smoke behind, thin warm rims down both edges and over the top
        'kicker': {**area(-150, 30, 3.0, 75.0, '#FFB978', (0.5, 2.8), (0.0, 0.0, 0.8)), 'receivers': SHELL},
        # the glow of the smoke straight behind it, through the tint: amber at the acrylic's edges and between panels
        'through': {**area(160, 10, 1.5, 8.0, '#FFB978', (1.2, 1.2), (0.0, 0.0, 0.5)), 'receivers': BODY},
        'kicker_r': {**area(150, 14, 3.0, 26.0, '#FFB978', (0.6, 2.4), (0.0, 0.0, 0.8)), 'receivers': SHELL},
    }
    return frame('smoke', props, cam, sky(SKY, rotation_deg=0.0, strength=0.08), 'barkhorn, Smoke, woodsmoke at dawn',
                 sun=SUN, lights=lights, rotate_z=18.0, position=(0.0, 0.0, -0.02), samples=512, exposure=0.0,
                 fin=finish(contrast=0.04, clarity=0.03, bloom=0.04, bloom_px=40, threshold=0.85, vignette=0.25))


def portrait():
    return portrait_of(shot(), lens=50)
