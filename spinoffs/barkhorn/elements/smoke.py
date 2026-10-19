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

PILE = (5.0, 5.2)            # the burn pile (round C)
PILE_D = (5.2, 6.2)          # round D2: the smoke's source, far back between the trunks
FERN = ((-0.55, -0.45, 0.0), 170.0, 0.8)   # D3: the fern clump at the near left corner (position, turn, scale)
SUN_A = {'azimuth_deg': 150.0, 'elevation_deg': 24.0, 'irradiance': 30.0, 'angle_deg': 0.5, 'color': '#FFB978'}
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


def plume(n=10):
    """The burn pile's plume: a column of smoke rising from the pile and leaning off to the left with the morning air,
    narrow and dense low down, widening, thinning and breaking into curling wisps as it rises into the light shafts.
    Overlapping cells of noise at two scales (billows and wisps); the cut rises with height, so the top tears apart."""
    out = []
    for k in range(n):
        t = k / (n - 1)
        w = 0.7 + 3.2 * t ** 1.3
        out.append(smoke((PILE[0] - 2.6 * t ** 1.6, PILE[1] - 0.4 * t, 0.1 + 0.95 * k), (w, w, 2.2), 18.0 * 0.72 ** k,
                         11 + k, scale=0.35 + 0.5 * t, cut=0.42 + 0.12 * t, soft=0.22, anisotropy=0.45,
                         fade=[0.42, 0.42, 0.4], floor=0.2 * (1 - t), rise=2.2 - 0.8 * t, color='#9DA2AA',
                         detail_scale=0.12 + 0.1 * t, detail_weight=0.35 + 0.25 * t))
    return out


def flames(n=6, seed=5):
    """A few low flames licking up out of the pile's heart: thin glowing tongues, hotter at the root."""
    import random
    rnd = random.Random(seed)
    out = []
    for i in range(n):
        x, y = PILE[0] + rnd.uniform(-0.25, 0.25), PILE[1] + rnd.uniform(-0.2, 0.2)
        h, r = rnd.uniform(0.18, 0.45), rnd.uniform(0.035, 0.07)
        out.append(piece('cone', material='glow', color='#FF7A22', emit=rnd.uniform(18, 30), radius=r, height=h,
                         position=[round(x, 3), round(y, 3), 0.12], rotate=[rnd.uniform(-12, 12), rnd.uniform(-12, 12), 0],
                         shadow=False))
        out.append(piece('cone', material='glow', color='#FFC060', emit=45, radius=r * 0.5, height=h * 0.45,
                         position=[round(x, 3), round(y, 3), 0.12], shadow=False))
    return out


ROT = 18.0                   # the speaker's turn (degrees)


def grounding():
    """The speaker set into the floor rather than on it: needles and duff drifted against the base on all four sides
    (low mounds in the ground's own texture, hugging each face), a fern clump just over the front corner nearest the
    camera, and roots, a stump and fallen branches about it, so the floor is uneven and lived-in."""
    import math
    c, s_ = math.cos(math.radians(ROT)), math.sin(math.radians(ROT))
    def at(lx, ly):
        return [round(lx * c - ly * s_, 4), round(lx * s_ + ly * c, 4)]
    out = []
    # (local centre, half-length along the face, which axis the face runs along)
    for lx, ly, half, along_x in ((0.0, -0.25, 0.36, True), (0.0, 0.25, 0.36, True), (-0.32, 0.0, 0.27, False),
                                  (0.32, 0.0, 0.27, False)):
        x, y = at(lx, ly)
        sc = [half, 0.14, 0.15] if along_x else [0.14, half, 0.15]
        out.append(piece('sphere', material='pbr', texture='forest_leaves_04', tex_res='2k', position=[x, y, -0.03],
                         scale=sc, rotate=[0, 0, ROT], tint='#4A3626', tint_mix=0.3))
    # damp, darker duff in the cabinet's own shade: the contact shadow a photograph would show under the plinth line
    out.append(piece('cylinder', material='pbr', texture='forest_leaves_04', tex_res='2k', radius=0.62, height=0.012,
                     position=[0.0, 0.0, -0.004], scale=[1.0, 0.8, 1.0], rotate=[0, 0, ROT], tint='#15100C', tint_mix=0.7))
    out += [asset('fern_02', (-0.75, -0.75, 0.0), (0, 0, 35), 0.5, res='1k'),
            asset('pine_roots', (1.6, 1.2, -0.02), (0, 0, 120), 1.0, res='1k'),
            asset('tree_stump_01', (-2.2, 2.4, -0.05), (0, 0, 60), 0.9, res='1k'),
            scatter(['dry_branches_medium_01'], 4, [-2.0, -1.5, 2.5, 1.8], avoid=[(0.0, 0.0, 1.0), (-0.75, -0.75, 0.8)],
                    seed=21, res='1k', z=-0.015, scale=(0.5, 0.8))]
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
    """Round D2 (the owner, 2026-10-19: "The speaker appears to be floating ... there's no smoke in the background"): A's
    rig and composition, which won every duel, with only what the owner asked for: the camera up to 1.0 m so the
    contact line and the cast shadows read, a fern over the near front corner, a few twigs, a shaft of sun onto the
    speaker so it throws its own shadow; and far back between the trunks a small smouldering pile whose thin column of
    woodsmoke rises and drifts left, so the smoke has a source."""
    props = [ground('forest_leaves_04', size=(40.0, 40.0), position=(0.0, 10.0, 0.0), displace=0.06, relief=0.12,
                    res='2k', tint='#4A3626', tint_mix=0.3),
             scatter(['dry_branches_medium_01'], 5, [-5.0, 4.0, 7.0, 12.0], avoid=[(0.0, 0.0, 2.5)], seed=4, res='1k', z=-0.015),
             smoke((0.5, 7.5, 0.0), (30.0, 19.0, 12.0), 0.15, 1, scale=3.0, cut=0.4, soft=0.3, anisotropy=0.85,
                   fade=[0.12, 0.33, 0.4], floor=0.06, ground=0.18, ground_h=1.6),
             piece('ext', module='smoke_el', fn='canopy', size=[120.0, 200.0], z=13.0, position=[0.0, 70.0], scale=1.4,
                   open=0.35, seed=2),
             piece('ext', module='smoke_el', fn='canopy', size=[120.0, 200.0], z=10.0, position=[0.0, 70.0], scale=0.9,
                   open=0.65, seed=5)]
    props += trees()
    # grounding: a fern clump just over the front corner nearest the camera, a few small twigs about the base
    props += [asset('fern_02', FERN[0], (0, 0, FERN[1]), FERN[2], res='1k'),
              scatter(['dry_branches_medium_01'], 3, [-1.8, -1.6, 2.0, 1.2], avoid=[(0.0, 0.0, 0.9), (-0.75, -0.75, 0.8)],
                      seed=21, res='1k', z=-0.015, scale=(0.18, 0.28))]
    # the smoke's source, far back between the trunks: a small smouldering pile and its thin leaning column
    props += [piece('ext', module='smoke_el', fn='burnpile', position=[PILE_D[0], PILE_D[1], 0.0], radius=0.5, seed=3,
                    ember=0.0, logs=10)]
    # D3: a fuller, backlit drift of the same woodsmoke crossing the far shafts at head height
    props.append(smoke((4.0, 10.5, 1.5), (14.0, 3.5, 4.0), 2.5, 41, scale=0.8, cut=0.58, soft=0.2, anisotropy=0.8,
                       fade=[0.3, 0.4, 0.45], floor=0.0, color='#C9CCD1', detail_scale=0.2, detail_weight=0.55,
                       rise=1.5))
    for k in range(8):
        t = k / 7
        w = 0.35 + 2.2 * t ** 1.2
        props.append(smoke((PILE_D[0] - 3.5 * t, PILE_D[1] + 0.5 * t, 0.05 + 0.85 * k), (w, w, 2.0), 10.0 * 0.8 ** k,
                           21 + k, scale=0.3 + 0.45 * t, cut=0.45 + 0.12 * t, soft=0.22, anisotropy=0.75,
                           fade=[0.42, 0.42, 0.4], floor=0.1 * (1 - t), rise=2.2 - 0.8 * t, color='#E4E4E6',
                           detail_scale=0.12 + 0.1 * t, detail_weight=0.4 + 0.25 * t))
    cam = camera(height=1.0, distance=7.2, azimuth=-20, lens=65, target=(0.0, 0.0, 0.7), fstop=4.0, shift_x=0.14,
                 shift_y=0.0)
    lights = {
        'skyfill': {**area(-20, 5, 2.4, 2.0, '#A9B4C2', (4.0, 3.0), (0.0, 0.0, 0.6)), 'receivers': SPEAKER},
        'bounce': {**area(-25, 12, 2.0, 7.0, '#C9BBA8', (2.4, 2.4), (0.0, 0.0, 0.6)), 'receivers': SPEAKER},
        'kicker': {**area(-150, 22, 3.0, 42.0, '#FFB978', (0.5, 2.4), (0.0, 0.0, 0.8)), 'receivers': SHELL},
        'kicker_r': {**area(150, 14, 3.0, 26.0, '#FFB978', (0.6, 2.4), (0.0, 0.0, 0.8)), 'receivers': SHELL},
        # a shaft of sun through a canopy gap onto the speaker, so it throws its own shadow across the needles
        'sungap': {'type': 'spot', 'position': [5.4, 9.36, 4.73], 'target': [0.0, 0.0, 0.3], 'power_w': 60000,
                   'cone_deg': 9.0, 'blend': 0.5, 'color': '#FFB978', 'radius_m': 0.15},
    }
    return frame('smoke', props, cam, sky(SKY, rotation_deg=0.0, strength=0.15), 'barkhorn, Smoke, woodsmoke at dawn',
                 sun=SUN_A, lights=lights, rotate_z=18.0, position=(0.0, 0.0, -0.03), samples=512, exposure=0.0,
                 fin=finish(contrast=0.04, clarity=0.03, bloom=0.04, bloom_px=40, threshold=0.85, vignette=0.25))


def portrait():
    """The 4:5 frame: the same set and light, the camera nearer (5.5 m) on the same lens and line."""
    sh = shot()
    cam = camera(height=1.0, distance=5.5, azimuth=-20, lens=65, target=(0.0, 0.0, 0.7), fstop=4.0, shift_x=0.04,
                 shift_y=0.06)
    return portrait_of(sh, **cam)
