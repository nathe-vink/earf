"""Ice, concept A: snow country at blue hour (round 31b; ice.md has the concept, the passes and the finals).

The speaker stands in deep fresh snow at the edge of a fir wood after sunset. The sky is a photographed dusk, its last
glow low behind the trees, the light everywhere the cold blue of the sky on snow. A log cabin stands far back among the
firs with one warm window, the frame's only warm note (the owner's nod: "a snow covered wood cabin in the back").
"""
import math, random

from common import area, asset, camera, finish, ground, piece, portrait_of, shot as frame, sky

SKY = 'kiara_9_dusk'
WB_K = 5400
CAM = (-2.5, -7.76)     # the camera on the ground (camera(distance=8.0, azimuth=-14) from the target)
TURN = -10.0
PRODUCT = ['left', 'right', 'top', 'bottom', 'front-panel', 'back', 'rib-*', 'brace*', 'port-*', 'waveguide*', 'woofer-*',
           'land-*', 'top-pad', 'grip-*']
SKY_ROT = 110.0         # the sunset behind the lens (and the wood there): ahead, the deep blue sky away from the sun


def forest(seed=31):
    """The wood behind: firs in depth, thinning toward the cabin's clearing, saplings at its edge."""
    rnd = random.Random(seed)
    trees = []
    # the wood's edge, 14 to 32 m back, left and right of the clearing the cabin stands in
    for _ in range(110):
        x = rnd.uniform(-30, 30); y = rnd.uniform(15, 55)
        if 2.0 < x < 11.5 and y < 76:                         # the cabin's clearing
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
    return piece('ext', module='ice_el', fn='firs', trees=trees, snow=0.75, res='1k')


def props():
    p = []
    # the snowfield: fine displaced snow where the speaker stands, broad drifts around it; a coarser field beyond
    p.append(piece('ext', module='ice_el', fn='snowfield', size=[32.0, 30.0], position=[0.0, 6.0, 0.0], displace=0.03,
                   ripple=0.004, relief=0.5, sparkle=4.0, res='2k', cells=1500, bank=[0.0, 0.0, 0.56, 0.42, TURN, 0.06]))
    p.append(ground('snow_02', size=(220.0, 220.0), position=(0.0, 60.0, -0.7), displace=0.0, relief=1.2, res='1k',
                    cells=440, flat=False))
    p.append(forest())
    p.append(piece('ext', module='ice_el', fn='cabin', position=[6.8, 72.0, 0.0], turn=-6, size=[6.5, 4.8],
                   window_emit=35.0, lamp_w=2500.0, window_color='#FF9A3C', res='1k'))
    return p


def lights():
    # the snow's bounce onto the speaker's front: one big, very soft card low at the camera's left (a reflector a
    # photographer would lay on the snow), on the speaker alone
    return {'bounce': {**area(-25, 5, 4.0, 0.7, '#C8D8EA', (3.0, 1.0), (0.0, 0.0, 0.8)), 'receivers': PRODUCT},
            # and the bright sky behind at the right, through the horn and the side walls (a white card held up)
            'back': {**area(160, 15, 4.0, 0.35, '#DCE6F4', (1.5, 2.0), (0.0, 0.0, 0.8)), 'receivers': PRODUCT},
            # a small white card held in front at the horn's height, so its throat reads as acrylic, not a hole
            'throat': {**area(-12, 8, 3.0, 0.5, '#E6EEF8', (1.0, 0.6), (0.0, -0.1, 1.12)), 'receivers': ['waveguide*']}}


def grain(fin, amount):
    fin.setdefault('dream', {'bloom': 0.0, 'saturation': 0.0, 'lift': 0.0, 'vignette': 0.0})
    fin['dream']['grain'] = amount
    return fin


def shot():
    cam = camera(height=0.45, distance=8.0, azimuth=-14, lens=85, target=(-0.56, 0.0, 0.66), fstop=2.8)
    s = frame('ice', props(), cam, sky(SKY, SKY_ROT, strength=1.0, res='4k'), 'barkhorn, Ice, snow country at blue hour',
                 lights=lights(), rotate_z=TURN, position=(0.0, 0.0, -0.04), exposure=-1.1, samples=512,
                 haze={'box_m': [-40, -12, -1, 40, 60, 20], 'density': 0.009, 'anisotropy': 0.2, 'color': '#C8D8EA'},
                 fin=grain(finish(contrast=0.10, clarity=0.06, sharpen=0.35, vignette=0.2), 0.006),
                 white_balance=(WB_K, 13.0))          # the white point a photographer sets at blue hour: the snow cold, not grey
    s['render']['caustics_refractive'] = True   # the sky's light reaches the lining through the acrylic (render.py)
    return s


def portrait():
    return portrait_of(shot(), lens_mm=80)
