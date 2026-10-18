"""Ember, concept A: a lava field at blue hour (round 31b; BRIEF.md, ember.md for the notes and the critic passes).

Black basalt, photographed (Poly Haven), carved as one piece of ground: a crater wall behind with a lava fall pouring
down a notch in it, a river of crusted lava (ambientCG) winding from the fall's foot past the speaker, a pool of molten
lava at its front left. The speaker stands on level rock on the near bank, lit from below and behind by the lava; a
blue-hour sky above the crater rim; steam over the lava carries its light; embers rise.
"""
from common import camera, finish, piece, point, portrait_of, shot as frame, sky

SKY = 'qwantani_dusk_2_puresky'
LAVA_LIGHT = '#FF6A20'

RIVER = [[2.4, 4.3], [1.9, 3.6], [0.6, 2.2], [-1.0, 1.7], [-3.2, 0.9], [-6.5, -0.4]]
POOL = (-1.55, -0.65, 0.55, 0.1)
FALL = [[2.6, 5.4, 6.5], [2.62, 5.15, 4.8], [2.66, 5.05, 3.2], [2.6, 5.0, 1.8], [2.62, 4.95, 0.8], [2.55, 4.75, 0.02]]


def props():
    P = [piece('ext', module='ember_el', fn='terrain', size=[18.0, 14.0], position=[0.0, 2.0, 0.0], cell=0.03,
               rock='dark_rock', displace=0.03, rock_tint='#0C0B0A', rock_tint_mix=0.6, relief=0.1, flat=[0.0, 0.0, 0.75],
               channels=[{'points': RIVER, 'width': 0.42, 'depth': 0.12, 'bank': 0.35, 'lava': 'flow'}],
               pools=[list(POOL), [2.55, 4.55, 0.65, 0.1]],
               flow='acg:Lava001', flow_emit=9.0, flow_scale=1.6, molten='acg:Lava004', molten_emit=10.0, molten_scale=2.0)]
    # the wall behind: basalt columns, stepping up away from the river, a gap where the lava pours through
    P.append(piece('ext', module='ember_el', fn='columns', area=[-9.0, 5.3, 9.0, 9.5], r=0.45, r_jitter=[0.75, 1.0],
                   heights=[2.4, 6.0], rough=1.2, steps=0.0, gaps=[[2.6, 5.4, 1.0]], rock='dark_rock_02', displace=0.015, tint='#0C0B0A', tint_mix=0.65, seed=3))
    # the lava fall: molten lava pouring over the columns' lip into the river's head
    P.append(piece('ext', module='ember_el', fn='fall', points=FALL, radius=[0.3, 0.32, 0.34, 0.36, 0.4, 0.5], flat=0.25,
                   lava='acg:Lava004', scale=1.2, strength=10.0))
    # embers rising from the lava, drifting with the heat
    for seed, (x, y), lean in ((1, POOL[:2], (0.4, 0.3)), (2, (-0.9, 1.75), (0.5, 0.4)), (3, (1.7, 3.4), (0.3, 0.5)),
                               (4, (2.62, 5.6), (0.6, 0.3))):
        P.append(piece('scatter', material='glow', color='#FF7A1E', position=[x, y, 0.0], count=30,
                       radius=[0.002, 0.005], seed=seed, emit=14.0, shadow=False,
                       plume={'height': 2.8, 'spread': [0.25, 1.1], 'lean': list(lean), 'taper': 0.4, 'power': 1.6}))
    return P


def lights():
    # practicals over the lava, high enough to light the rock and the speaker rather than the lava's own crust
    L = {'pool': point([POOL[0] + 0.2, POOL[1], 0.5], 70, LAVA_LIGHT, 0.4),
         'river': point([0.4, 2.0, 0.4], 40, LAVA_LIGHT, 0.4),
         'fall_low': point([2.5, 4.5, 0.6], 90, LAVA_LIGHT, 0.5),
         'fall_high': point([2.5, 4.6, 1.8], 60, LAVA_LIGHT, 0.5)}
    return L


def shot():
    cam = camera(height=1.0, distance=5.6, azimuth=-15.0, lens=50.0, target=(0.0, 0.0, 0.7), fstop=4.0)
    s = frame('ember', props(), cam, sky(SKY, rotation_deg=0.0, strength=0.18), 'barkhorn, Ember, a lava field at blue hour',
                 lights=lights(), rotate_z=15.0, exposure=0.0,
                 haze={'box_m': [-9.0, -8.0, -0.2, 9.0, 13.0, 5.0], 'density': 0.006, 'anisotropy': 0.5, 'color': '#FFFFFF'},
                 fin=finish(bloom=0.2, bloom_px=36, threshold=0.85, vignette=0.15))
    return s


def portrait():
    return portrait_of(shot())
