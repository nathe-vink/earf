"""Ember, concept A: a volcanic cavern (round 31b; BRIEF.md, ember.md for the notes and the critic passes).

A pit crater at dusk, a collapsed lava tube open to the sky: walls of scanned rock (Poly Haven) regraded to black
basalt tower behind and close in at the sides; a river of lava runs along their foot and a lava fall pours down the back
wall into it; a crack of lava opens at the speaker's feet. The red speaker stands on the black pahoehoe floor, lit
through from behind and from below by the lava; steam rises off the river, sparks lift; a deep-blue sky shows above the
rim. The lava is ambientCG's, through a ramp that keeps its colour (studio/engine/kit_ext/ember_el.py)."""
from common import camera, finish, piece, point, portrait_of, shot as frame, sky

SKY = 'qwantani_dusk_2_puresky'
LAVA_LIGHT = '#FF6A22'
# the river runs along the foot of the back wall; a hairline crack opens in front of the speaker's left foot
RIVER = [[-7.5, 2.4], [-4.0, 3.4], [-1.5, 3.2], [1.0, 3.6], [3.5, 3.3], [7.5, 4.0]]
CRACK = [[-2.4, -1.6], [-1.6, -1.05], [-0.9, -0.85], [-0.5, -0.55]]
FALL = [[-3.0, 4.6, 4.6], [-2.95, 4.3, 3.9], [-3.0, 4.05, 2.9], [-2.9, 3.85, 1.8], [-2.95, 3.65, 0.8], [-3.0, 3.35, 0.0]]


def rock(model, position, rotate=(0.0, 0.0, 0.0), scale=1.0, albedo=0.055, saturation=0.2, rough_mul=0.8):
    """A scanned rock face (Poly Haven), regraded to black basalt (studio/engine/kit_ext/ember_el.py)."""
    return piece('ext', module='ember_el', fn='rock', model=model, position=list(position), rotate=list(rotate),
                 scale=scale, albedo=albedo, saturation=saturation, rough_mul=rough_mul)


def props():
    ground = dict(rock='dark_rock', displace=0.03, albedo=0.10, rough_mul=0.8)
    P = [
        # the crater floor: pahoehoe, ropes and lobes; seams carved below a level sheet of lava
        piece('ext', module='ember_el', fn='terrain', size=[16.0, 12.0], position=[0.0, 2.0, 0.0], cell=0.02,
              relief=0.1, flat=[0.0, 0.0, 0.6], ropes={'amp': 0.02, 'wave': 0.07, 'dir': 70.0, 'lobes': 0.12},
              channels=[{'points': RIVER, 'width': 0.55, 'depth': 0.35, 'bank': 0.4},
                        {'points': CRACK, 'width': 0.07, 'depth': 0.3, 'bank': 0.12}],
              lava_below=True, **ground),
        piece('ext', module='ember_el', fn='lava_surface', size=[16.0, 12.0], position=[0.0, 2.0, -0.05], cell=0.05,
              lava='acg:Lava001', scale=1.1, strength=26.0, gain=1.3, ripple=0.012),
        # the crater's walls: scanned rock faces regraded to basalt, towering behind and closing in at the sides
        rock('mountainside', (0.5, 6.2, -0.6), (0.0, 0.0, 4.0), 1.15),
        rock('rock_face_01', (-5.0, 2.2, -0.3), (0.0, 0.0, -62.0), 1.5),
        rock('rock_face_02', (5.4, 3.0, -0.3), (0.0, 0.0, 55.0), 1.8),
        # the lava fall pouring down the back wall into the river
        piece('ext', module='ember_el', fn='fall', points=FALL, radius=[0.12, 0.16, 0.15, 0.19, 0.22, 0.36], flat=0.4,
              lava='acg:Lava004', scale=[1.0, 1.0, 4.0], strength=30.0, gain=1.2),
        # steam rising off the river and at the fall's foot
        piece('ext', module='ember_el', fn='steam', box=[-4.5, 2.2, -0.1, 4.0, 4.6, 3.0], density=0.35, scale=0.8,
              anisotropy=0.45),
        # sparks lifting off the lava
        piece('ext', module='ember_el', fn='sparks_mixed', area=[-3.5, 2.6, 3.0, 3.8], count=30, height=2.2,
              streak=[0.01, 0.12], radius=[0.001, 0.004], drift=[0.3, -0.1], emit=16.0, seed=4),
        piece('ext', module='ember_el', fn='sparks_mixed', area=[-1.6, -1.2, -0.6, -0.4], count=8, height=1.4,
              streak=[0.01, 0.08], radius=[0.001, 0.003], drift=[0.4, 0.1], emit=16.0, seed=9),
    ]
    return P


def lights():
    L = {
        # hidden behind the cabinet: the lava's light coming through the acrylic
        'through': point([0.08, 0.5, 0.6], 140, LAVA_LIGHT, 0.12),
        # the crack in front, low: the lava's light rising onto the cabinet's foot
        'crack': point([-0.9, -0.85, 0.15], 40, LAVA_LIGHT, 0.08),
        # the river and the fall, lighting the walls from their foot
        'river_l': point([-1.0, 3.2, 0.35], 110, LAVA_LIGHT, 0.3),
        'river_r': point([2.2, 3.4, 0.35], 110, LAVA_LIGHT, 0.3),
        'fall': point([FALL[-1][0] + 0.3, FALL[-1][1] - 0.5, 1.2], 200, LAVA_LIGHT, 0.4),
    }
    return L


def shot():
    cam = camera(height=0.95, distance=6.5, azimuth=22.0, lens=60.0, target=(0.0, 0.0, 0.66), fstop=2.0)
    return frame('ember', props(), cam, sky(SKY, rotation_deg=0.0, strength=0.12), 'barkhorn, Ember, a volcanic cavern',
                 lights=lights(), rotate_z=15.0, exposure=0.0,
                 haze={'box_m': [-12.0, -10.0, -0.5, 12.0, 12.0, 12.0], 'density': 0.0015, 'anisotropy': 0.4, 'color': '#FFFFFF'},
                 fin=finish(bloom=0.18, bloom_px=34, threshold=0.88, vignette=0.15))


def portrait():
    return portrait_of(shot())
