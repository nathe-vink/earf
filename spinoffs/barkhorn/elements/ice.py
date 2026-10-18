"""Ice, concept A: snow country at blue hour (round 31b; ice.md has the concept, the passes and the finals).

The speaker stands in deep fresh snow at the edge of a fir wood after sunset. The sky is a photographed dusk, its last
glow low behind the trees, the light everywhere the cold blue of the sky on snow. A log cabin stands far back among the
firs with one warm window, the frame's only warm note (the owner's nod: "a snow covered wood cabin in the back").
"""
import math, random

from common import area, asset, camera, finish, ground, piece, portrait_of, shot as frame, sky

SKY = 'kloppenheim_02_puresky'     # a clear night under a moon 17 deg up, stars faint
WB_K = 5400
CAM = (-2.5, -7.76)     # the camera on the ground (camera(distance=8.0, azimuth=-14) from the target)
TURN = -10.0
CABIN = [5.5, 58.0, 0.0]    # far back at the left, through the trees
WINDOW = 28.0
PRODUCT = ['left', 'right', 'top', 'bottom', 'front-panel', 'back', 'rib-*', 'brace*', 'port-*', 'waveguide*', 'woofer-*',
           'land-*', 'top-pad', 'grip-*']
SKY_ROT = 279.0         # the moon behind the wood at the right rear (azimuth 135): it rims the speaker and rakes the snow


def forest(seed=31):
    """The wood behind: firs in depth, thinning toward the cabin's clearing, saplings at its edge."""
    rnd = random.Random(seed)
    trees = []
    # the wood's edge, 14 to 32 m back, left and right of the clearing the cabin stands in
    for _ in range(110):
        x = rnd.uniform(-30, 30); y = rnd.uniform(15, 55)
        if 1.5 < x < 9.5 and y < 62:                         # the cabin's clearing
            continue
        if abs(math.degrees(math.atan2(x - CAM[0], y - CAM[1])) - 17.9) < 10.0 and y < 70:
            continue                                         # a gap behind the speaker, so the last light shows through it
        if rnd.random() < 0.6:
            trees.append([round(x, 2), round(y, 2), round(rnd.uniform(0, 360), 1), round(rnd.uniform(0.9, 1.5), 2),
                          'fir_sapling_medium:' + rnd.choice('abc')])
        else:
            trees.append([round(x, 2), round(y, 2), round(rnd.uniform(0, 360), 1), round(rnd.uniform(0.6, 0.9), 2),
                          'fir_tree_01:' + rnd.choice('abc')])
    # the wood behind the lens, out of frame: it shades the clearing from the last direct sun (the light is the sky's)
    for _ in range(40):
        x = rnd.uniform(-40, 30); y = rnd.uniform(-38, -18)
        trees.append([round(x, 2), round(y, 2), round(rnd.uniform(0, 360), 1), round(rnd.uniform(0.8, 1.0), 2),
                      'fir_tree_01:' + rnd.choice('abc')])
    # younger firs at the wood's edge, nearer
    for x, y, s, v in [(4.5, 9.5, 0.55, 'a'), (7.5, 11.0, 0.7, 'b'), (-12.0, 10.5, 0.65, 'a'), (11.0, 8.0, 0.5, 'c')]:
        trees.append([x, y, round(rnd.uniform(0, 360), 1), s, 'fir_sapling_medium:' + v])
    # a young fir near the lens at the left, soft, framing
    # dry grass through the snow near the lens, bottom left, soft
    for x, y, t, s, v in [(-3.3, -3.6, 20, 1.4, 'mid_a'), (-3.0, -3.9, 140, 1.2, 'small_b')]:
        trees.append([x, y, t, s, 'grass_medium_01:' + v])
    return piece('ext', module='ice_el', fn='firs', trees=trees, snow=0.75, res='1k')


def props():
    p = []
    # the snowfield: fine displaced snow where the speaker stands, broad drifts around it; a coarser field beyond
    p.append(piece('ext', module='ice_el', fn='snowfield', size=[32.0, 30.0], position=[0.0, 6.0, 0.0], displace=0.03,
                   ripple=0.01, relief=0.5, sparkle=4.0, res='2k', cells=1500, bank=[0.0, 0.0, 0.56, 0.42, TURN, 0.06]))
    p.append(ground('snow_02', size=(220.0, 220.0), position=(0.0, 60.0, -0.7), displace=0.0, relief=1.2, res='1k',
                    cells=440, flat=False))
    p.append(forest())
    # the cabin close behind, soft: its window glowing just right of the speaker, its warmth behind the cold acrylic
    p.append(piece('ext', module='ice_el', fn='cabin', position=CABIN, turn=-6, size=[6.5, 4.8],
                   window_emit=WINDOW, lamp_w=1500.0, window_color='#FF9A3C', res='1k'))
    # hills far off under snow, closing the horizon (the sky is a pure sky)
    for x, y, sx, sy, sz in [(-90, 320, 140, 50, 22), (60, 360, 170, 60, 30), (210, 300, 110, 50, 18), (-260, 340, 130, 50, 26)]:
        p.append(piece('sphere', material='pbr', texture='snow_02', tex_scale=6.0, position=[x, y, -sz * 0.35],
                       scale=[sx, sy, sz], segments=64))
    return p


def lights():
    # the snow's bounce onto the speaker's front: one big, very soft card low at the camera's left (a reflector a
    # photographer would lay on the snow), on the speaker alone
    return {'bounce': {**area(-45, 3, 4.0, 0.8, '#C8D8EA', (4.0, 1.0), (0.0, 0.0, 0.5)), 'receivers': PRODUCT},
            # and the bright sky behind at the right, through the horn and the side walls (a white card held up)
            'back': {**area(150, 15, 4.0, 1.6, '#D8E2F0', (2.0, 3.0), (0.0, 0.0, 0.8)), 'receivers': PRODUCT}}


def grain(fin, amount):
    fin.setdefault('dream', {'bloom': 0.0, 'saturation': 0.0, 'lift': 0.0, 'vignette': 0.0})
    fin['dream']['grain'] = amount
    return fin


def shot():
    cam = camera(height=0.45, distance=8.0, azimuth=-14, lens=85, target=(-0.56, 0.0, 0.66), fstop=2.8)
    s = frame('ice', props(), cam, sky(SKY, SKY_ROT, strength=1.0, res='4k'), 'barkhorn, Ice, snow country at blue hour',
                 lights=lights(), rotate_z=TURN, position=(0.0, 0.0, -0.04), exposure=-0.6, samples=512,
                 haze={'box_m': [-40, -12, -1, 40, 60, 20], 'density': 0.003, 'anisotropy': 0.2, 'color': '#C8D8EA'},
                 fin=grain(finish(contrast=0.14, clarity=0.04, sharpen=0.35, vignette=0.2), 0.005),
                 white_balance=(WB_K, 10.0))          # the white point a photographer sets at blue hour: the snow cold, not grey
    s['render']['caustics_refractive'] = True   # the sky's light reaches the lining through the acrylic (render.py)
    return s


def portrait():
    return portrait_of(shot(), lens_mm=80)
