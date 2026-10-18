"""Ember, concept A: a lava field at blue hour (round 31b; BRIEF.md, ember.md for the notes and the critic passes).

An open field of black pahoehoe crust under a deep-blue dusk sky. Incandescent cracks open in the crust round the
speaker; a slow river of lava crosses the midground behind it; far off, a vent glows under its own steam plume. The
speaker takes the lava's warm light from below and behind and the sky's cool light from above. The rock is Poly Haven's
black basalt, displaced at its true scale, carved as one piece of ground; the lava is ambientCG's, through a ramp that
keeps its colour and a matte crust (studio/engine/kit_ext/ember_el.py). The volcanic cavern of passes 4 to 7 is in git
history (8bb08b1) and ember.md.
"""
from common import camera, finish, piece, point, portrait_of, shot as frame, sky

SKY = 'qwantani_dusk_2_puresky'
LAVA_LIGHT = '#FF6A22'
# the river crosses the midground behind the speaker, from the far left to the right
RIVER = [[-9.0, 6.0], [-4.5, 4.4], [-1.5, 3.4], [1.0, 3.0], [3.6, 3.6], [8.0, 5.2]]
# cracks in the crust round the speaker: thin, branching, incandescent
CRACKS = [([[-3.2, -1.4], [-2.2, -0.9], [-1.3, -0.95], [-0.7, -0.6]], 0.05),
          ([[-1.3, -0.95], [-1.5, -0.2], [-1.2, 0.6], [-0.6, 1.3], [-0.6, 2.6]], 0.04),
          ([[0.7, 0.55], [1.4, 0.7], [2.1, 0.3], [3.2, 0.5]], 0.04),
          ([[1.4, 0.7], [1.6, 1.6], [1.3, 2.7]], 0.03),
          ([[0.4, -1.6], [0.9, -2.4], [1.9, -2.9]], 0.07)]
VENT = (-7.5, 26.0)


def lamp(position, target, irradiance, size, color='#FF5A18'):
    """A soft lamp placed by position, hidden behind the speaker: the lava's light coming through the acrylic."""
    return {'type': 'area', 'size_m': list(size), 'position': list(position), 'target': list(target),
            'irradiance': irradiance, 'color': color}


def props():
    rock = dict(rock='dark_rock_02', displace=0.03, albedo=0.09, rough_mul=0.85)
    P = [
        # the near field: crust, the cracks and the river carved below a level sheet of lava
        piece('ext', module='ember_el', fn='terrain', size=[22.0, 16.0], position=[0.0, 3.0, 0.0], cell=0.02,
              relief=0.14, flat=[0.0, 0.0, 0.6],
              channels=[{'points': RIVER, 'width': 0.8, 'depth': 0.35, 'bank': 0.5}]
                       + [{'points': pts, 'width': w, 'depth': 0.09, 'bank': w * 1.2} for pts, w in CRACKS],
              lava_below=True, **rock),
        piece('ext', module='ember_el', fn='lava_surface', size=[22.0, 16.0], position=[0.0, 3.0, -0.06], cell=0.05,
              lava='acg:Lava001', scale=2.2, strength=40.0, gain=2.2, ripple=0.012, crust_rough=0.85, crust_spec=0.2),
        # the far field: coarser rock running to a low ridge, a vent glowing on it
        piece('ext', module='ember_el', fn='terrain', size=[90.0, 50.0], position=[0.0, 36.0, -0.25], cell=0.12,
              relief=0.6, flat=[0.0, -200.0, 1.0],
              cliff={'y0': 34.0, 'rise': 12.0, 'height': 3.5, 'rough': 1.0},
              pools=[[VENT[0], VENT[1], 1.2, 0.3]],
              channels=[{'points': [[14.0, 16.0], [5.0, 14.5], [-4.0, 16.0], [-16.0, 14.0]], 'width': 0.5, 'depth': 0.2,
                         'bank': 0.6, 'lava': 'flow'}],
              flow='acg:Lava001', flow_emit=40.0, flow_gain=2.2, flow_scale=2.5, molten='acg:Lava004', molten_emit=30.0,
              molten_scale=3.0, **{**rock, 'displace': 0.05}),
        # steam: low over the river, and a plume rising from the vent, lit from below
        piece('ext', module='ember_el', fn='steam', box=[-6.0, 2.4, -0.1, 5.0, 4.6, 1.4], density=0.9, scale=0.8,
              anisotropy=0.45),
        piece('ext', module='ember_el', fn='steam', box=[VENT[0] - 3.0, VENT[1] - 2.5, 0.0, VENT[0] + 4.0, VENT[1] + 2.5, 9.0],
              density=0.25, scale=2.5, anisotropy=0.45),
        # a handful of embers off the river
        piece('ext', module='ember_el', fn='sparks_mixed', area=[-2.0, 3.0, 0.5, 3.6], count=6, height=1.8,
              streak=[0.01, 0.08], radius=[0.001, 0.003], drift=[0.3, 0.1], emit=16.0, seed=4),
    ]
    return P


def lights():
    return {
        # hidden behind the speaker: the river's light coming through the acrylic, the cabinet and the horn
        'through': lamp([0.15, 0.9, 0.5], [0.0, -0.6, 0.3], 2.0, (0.6, 1.2)),
        'horn': lamp([0.1, 0.75, 1.3], [0.0, -0.2, 1.12], 2.4, (0.6, 0.3)),
        # the cracks beside its feet, low
        'crack_l': point([-1.25, -0.4, 0.12], 40, LAVA_LIGHT, 0.2),
        'crack_r': point([1.0, 0.6, 0.12], 30, LAVA_LIGHT, 0.2),
        # the river's glow in the steam over it
        'river': point([1.0, 3.2, 0.5], 120, LAVA_LIGHT, 0.3),
        # the vent, far off, lighting its plume
        'vent': point([VENT[0], VENT[1], 1.0], 3000, LAVA_LIGHT, 0.8),
    }


def shot():
    cam = camera(height=0.95, distance=6.5, azimuth=22.0, lens=60.0, target=(0.0, 0.0, 0.66), fstop=2.8)
    return frame('ember', props(), cam, sky(SKY, rotation_deg=0.0, strength=0.3), 'barkhorn, Ember, a lava field at blue hour',
                 lights=lights(), rotate_z=15.0, exposure=0.0,
                 haze={'box_m': [-45.0, -10.0, -0.5, 45.0, 62.0, 14.0], 'density': 0.0015, 'anisotropy': 0.4,
                       'color': '#FFFFFF'},
                 fin=finish(bloom=0.18, bloom_px=34, threshold=0.88, vignette=0.2),
                 white_balance=(4500, 10))           # a cool blue hour: the sky blue, the lava still orange


def portrait():
    return portrait_of(shot())
