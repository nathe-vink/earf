"""Smoke, concept A: woodsmoke backlit in a pine forest at dawn (round 31b; BRIEF.md, notes in smoke.md).

Round C (the owner, 2026-10-18: "Doesn't look like a smokey environment and the speaker is too stark and crisp"): a
smouldering burn pile in frame behind and right of the speaker sends a plume up and across the wood; the whole air is
hazed with its smoke, between the camera and the speaker too, so the speaker sits in the same air as the trees.

The speaker stands on the needle floor of a pine wood just after sunrise. Woodsmoke from a fire out of frame drifts
between the trunks behind it, and the low sun behind the smoke turns it to a glowing wall, cut into shafts by the trunks.
The smoked black speaker stands in front of that glow, so it reads as a clean dark silhouette rimmed in warm light, and
the light that comes through its acrylic shows its tint.
"""
from common import area, asset, point, camera, finish, ground, piece, scatter, shot as frame, sky, portrait_of

PILE = (3.6, 5.0)            # the burn pile
SKY = 'misty_pines'           # a real pine wood in morning mist (Poly Haven, CC0)
SUN = {'azimuth_deg': 150.0, 'elevation_deg': 18.0, 'irradiance': 75.0, 'angle_deg': 0.5, 'color': '#FFCC9A'}


# the speaker's outer parts: the kickers light these alone, so they rim the speaker without outlining the trunks
SHELL = ['left', 'right', 'top', 'bottom', 'front-panel', 'back', 'waveguide', 'waveguide-cap', 'woofer-ring', 'post-*',
         'grip-*', 'port-frame-*']
# every part of the speaker, inside included (the fills a photographer brings light the speaker, not the floor)
SPEAKER = SHELL + ['lining-*', 'woofer-*', 'amp-*', 'brace*', 'rib-*', 'land-*', 'port-*', 'hf-*', 'feet-*', 'tie-rod-*',
                   'top-pad', 'mark-back', 'back-*', 'cap-o-ring', 'lead-*', 'cable-glands', 'rating-plate']


def smoke(position, size, density, seed, **k):
    return piece('ext', module='smoke_el', fn='woodsmoke', position=list(position), size=list(size), density=density,
                 seed=seed, **k)


def plume(n=7):
    """The burn pile's plume: overlapping soft cells of smoke, widening as it rises and drifting off to the left with the
    morning air, densest near the pile."""
    out = []
    for k in range(n):
        w = 1.0 + 0.55 * k
        out.append(smoke((PILE[0] - 0.22 * k ** 1.5, PILE[1] - 0.1 * k, 0.15 + 1.15 * k), (w, w, 2.4), 1.8 * 0.85 ** k,
                         11 + k, scale=0.45 + 0.08 * k, cut=0.38, soft=0.35, anisotropy=0.3,
                         fade=[0.4, 0.4, 0.4], floor=0.3, rise=1.8, color='#E4E2DE'))
    return out


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
    return [piece('ext', module='smoke_el', fn='trunks', trees=t, texture='pine_bark', res='2k', bump=5.0,
                  tint='#1E1A17', tint_mix=0.3)]


def shot():
    props = [ground('forest_leaves_04', size=(40.0, 40.0), position=(0.0, 10.0, 0.0), displace=0.06, relief=0.12,
                    res='2k', tint='#4A3626', tint_mix=0.3),
             scatter(['dry_branches_medium_01'], 5, [-5.0, 4.0, 7.0, 12.0], avoid=[(0.0, 0.0, 2.5)], seed=4, res='1k', z=-0.015),
             # the smoke hangs between the trunks; beyond it the photographed wood shows through the mist
             smoke((0.5, 7.5, 0.0), (30.0, 19.0, 12.0), 0.15, 1, scale=3.0, cut=0.4, soft=0.3, anisotropy=0.85,
                   fade=[0.12, 0.33, 0.4], floor=0.06, ground=0.18, ground_h=1.6),
             # the crowns overhead, out of frame: the sun comes down through their gaps in shafts
             piece('ext', module='smoke_el', fn='canopy', size=[120.0, 200.0], z=13.0, position=[0.0, 70.0], scale=1.4,
                   open=0.35, seed=2),
             piece('ext', module='smoke_el', fn='canopy', size=[120.0, 200.0], z=10.0, position=[0.0, 70.0], scale=0.9,
                   open=0.65, seed=5)]
    props += trees()
    # the burn pile, 3 m behind and right of the speaker, and its plume: a dense column that leans off toward the left
    props += [piece('ext', module='smoke_el', fn='burnpile', position=[PILE[0], PILE[1], 0.0], radius=0.9, seed=3),
              # the bed of grey-white ash the pile has burnt down into
              piece('cylinder', material='sand', color='#8E8A85', tint2='#5E5A56', radius=1.15, height=0.025,
                    position=[PILE[0], PILE[1], -0.01])]
    pl = plume()
    plume_names = [f'prop{i}-kit' for i in range(len(props), len(props) + len(pl))]
    props += pl
    props += [
              # where the plume flattens and drifts: a layer across the wood at 2 to 5 m, thinning toward the camera
              smoke((-1.0, 3.0, 1.6), (16.0, 8.0, 4.0), 0.5, 9, scale=1.2, cut=0.45, soft=0.3, anisotropy=0.75,
                    fade=[0.3, 0.4, 0.5], floor=0.02, rise=0.6, color='#CFCBC6'),
              # low wisps drifting between the camera and the speaker, veiling its lower half a little
              smoke((0.0, -1.6, 0.0), (9.0, 3.0, 1.8), 0.45, 13, scale=0.8, cut=0.48, soft=0.3, anisotropy=0.6,
                    fade=[0.3, 0.35, 0.6], floor=0.02, rise=0.5, color='#D6D0C8')]
    cam = camera(height=0.7, distance=6.2, azimuth=-20, lens=65, target=(0.0, 0.0, 0.7), fstop=2.8, shift_x=0.14)
    lights = {
        # the open sky behind the camera, cool, lifting the shadow side: the woofer and lining just read in the tint
        'skyfill': {**area(-20, 5, 2.4, 2.0, '#B8B4AE', (4.0, 3.0), (0.0, 0.0, 0.6)), 'receivers': SPEAKER},
        # the sunlit litter and the sky bounce into its face: low, broad and cool-neutral
        'bounce': {**area(-25, 12, 2.0, 14.0, '#C9BBA8', (2.4, 2.4), (0.0, 0.0, 0.6)), 'receivers': SPEAKER},
        # the sun's light off the smoke behind, thin warm rims down both edges and over the top
        'kicker': {**area(-150, 10, 3.0, 95.0, '#FFB978', (0.5, 2.4), (0.0, 0.0, 0.9)), 'receivers': SHELL},
        'kicker_r': {**area(144, 2, 3.0, 120.0, '#FF8A40', (1.0, 0.5), (0.0, 0.0, 0.4)), 'receivers': SHELL},
        # the pile's embers, under the plume
        'embers': point([PILE[0], PILE[1], 0.3], 250, '#FF6A20', 0.4),
        'emberglow': {'type': 'area', 'size_m': [1.0, 1.0], 'position': [PILE[0], PILE[1], 0.06], 'target': [PILE[0], PILE[1], 2.0],
                      'power_w': 150, 'color': '#FF7A30'},
        # the open sky behind the camera on the plume's face (it would be a dark column lit from behind alone)
        'plumefill': {'type': 'area', 'size_m': [6.0, 6.0], 'position': [PILE[0] - 5.0, PILE[1] - 11.0, 2.5],
                      'target': [PILE[0] - 0.6, PILE[1], 3.0], 'irradiance': 22.0, 'color': '#C9CED6',
                      'receivers': plume_names},
    }
    return frame('smoke', props, cam, sky(SKY, rotation_deg=0.0, strength=0.7), 'barkhorn, Smoke, woodsmoke at dawn',
                 sun=SUN, lights=lights, rotate_z=18.0, position=(0.0, 0.0, -0.02), samples=512, exposure=0.3,
                 # the whole air hazed with the pile's smoke, the camera inside it, so the speaker sits in the same air
                 haze={'box_m': [-15.0, -15.0, 0.0, 18.0, 30.0, 14.0], 'density': 0.012, 'anisotropy': 0.7,
                       'color': '#BCC4CE'},
                 # no clarity and no sharpening: the speaker as soft as the set around it
                 fin=finish(contrast=0.15, clarity=0.0, sharpen=0.0, bloom=0.06, bloom_px=40, threshold=0.85,
                            vignette=0.18))


def portrait():
    """The 4:5 frame: the same set and light, the camera nearer (5.5 m) on the same lens and line, the speaker a little
    left of centre and low, the glowing smoke and the trunks above it."""
    sh = shot()
    cam = camera(height=0.7, distance=5.5, azimuth=-20, lens=65, target=(0.0, 0.0, 0.7), fstop=4.0, shift_x=0.04,
                 shift_y=0.1)
    return portrait_of(sh, **cam)
