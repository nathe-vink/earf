"""Ember, concept A: a lava field at blue hour (round 31b; BRIEF.md, ember.md for the notes and the critic passes).

An open field of black pahoehoe under a deep-blue dusk sky. A seam of lava runs behind the speaker and opens into a pool
at its back left, so the acrylic is lit through from behind and below; steam rises off it, sparks lift. Far back, the
field runs to a crater rim with a thin lava fall spilling down it and a glowing seam crossing the plain, softened by the
evening haze. The rock is Poly Haven's black basalt, carved as one piece of ground with ropes and lobes at the scale of
real pahoehoe; the lava is ambientCG's, through a ramp that keeps its colour (studio/engine/kit_ext/ember_el.py).
"""
from common import area, camera, finish, piece, point, portrait_of, shot as frame, sky

SKY = 'qwantani_dusk_2_puresky'
LAVA_LIGHT = '#FF6A22'
SEAM = [[5.0, 6.5], [2.6, 3.7], [0.9, 2.45], [-1.0, 2.05], [-3.4, 2.7], [-7.5, 3.3]]
POOL = (-0.95, -0.95, 0.55, 0.35)


def props():
    rock = dict(rock='dark_rock', displace=0.03, albedo=0.25, rough_mul=0.55)
    P = [
        # the near field: pahoehoe, the seam and the pool carved below the lava's level
        piece('ext', module='ember_el', fn='terrain', size=[16.0, 13.0], position=[0.0, 2.5, 0.0], cell=0.02,
              relief=0.12, flat=[0.0, 0.0, 0.6], ropes={'amp': 0.01, 'wave': 0.1, 'dir': 70.0, 'lobes': 0.09},
              channels=[{'points': SEAM, 'width': 0.5, 'depth': 0.35, 'bank': 0.45}], pools=[list(POOL)],
              lava_below=True, **rock),
        piece('ext', module='ember_el', fn='lava_surface', size=[16.0, 10.0], position=[0.0, 2.5, -0.05], cell=0.05,
              lava='acg:Lava001', scale=1.3, strength=12.0, gain=1.25, ripple=0.012),
        # the far field and the crater rim, coarser, with a seam of its own and a thin fall down the rim
        piece('ext', module='ember_el', fn='terrain', size=[80.0, 52.0], position=[-8.0, 34.5, -0.25], cell=0.12,
              relief=0.5, flat=[0.0, -200.0, 1.0], cliff={'y0': 24.0, 'rise': 9.0, 'height': 6.0, 'rough': 0.4},
              channels=[{'points': [[12.0, 13.0], [2.0, 15.5], [-8.0, 14.0], [-22.0, 16.5]], 'width': 0.6, 'depth': 0.2,
                         'bank': 0.6, 'lava': 'flow'}],
              falls=[{'points': [[-5.0, 32.0], [-5.3, 28.0], [-5.0, 25.5], [-4.8, 24.0]], 'width': 0.28, 'notch': 0.3}],
              flow='acg:Lava001', flow_emit=10.0, flow_scale=2.5, molten='acg:Lava004', molten_emit=6.0,
              molten_scale=3.0, **{**rock, 'displace': 0.06}),
        # steam off the seam and the pool, lit from below
        piece('ext', module='ember_el', fn='steam', box=[-6.5, -1.6, -0.1, 4.5, 4.8, 2.2], density=2.0, scale=0.9,
              anisotropy=0.45),
        # sparks lifting off the lava
        piece('ext', module='ember_el', fn='sparks', area=[-2.6, -1.3, 1.8, 3.0], count=50, height=1.2,
              streak=[0.012, 0.07], radius=[0.0008, 0.0024], drift=[0.35, 0.15], emit=14.0, color='#FF6A1A', seed=4),
    ]
    return P


def lights():
    L = {
        # the seam and the pool behind: a low glow through the acrylic toward the lens
        'seam': area(165, 8, 1.5, 9.0, '#FF5A1A', (1.6, 0.4), target=(0.0, 0.0, 0.6)),
        'pool': point([POOL[0] + 0.25, POOL[1] + 0.1, 0.35], 160, LAVA_LIGHT, 0.4),
        'seam_r': point([1.6, 2.9, 0.4], 90, LAVA_LIGHT, 0.4),
    }
    return L


def shot():
    cam = camera(height=0.95, distance=6.5, azimuth=22.0, lens=60.0, target=(0.0, 0.0, 0.66), fstop=4.0)
    return frame('ember', props(), cam, sky(SKY, rotation_deg=0.0, strength=0.35), 'barkhorn, Ember, a lava field at blue hour',
                 lights=lights(), rotate_z=15.0, exposure=0.0,
                 haze={'box_m': [-40.0, -10.0, -0.5, 30.0, 60.0, 12.0], 'density': 0.003, 'anisotropy': 0.4, 'color': '#FFFFFF'},
                 fin=finish(bloom=0.18, bloom_px=34, threshold=0.88, vignette=0.15))


def portrait():
    return portrait_of(shot())
