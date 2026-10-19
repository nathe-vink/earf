"""Ember A2: the lava field at blue hour, refined (round 31b; ember.md for the notes and the critic passes).

A's concept, camera and speaker, with what A's critics kept naming put right:
- one main flow, not many cracks: an incandescent toe sweeping in from the left foreground and passing the speaker 2 to 3
  m off, a yellow-orange core in a dark-red skin cracked into plates, black crust at its edges; the rest of the field dark
  crust with a few dimmer glows at other scales; a low steam veil over the flow, lit from below;
- the flow lights the cabinet's front and the ground round it, warm and low; the blue-hour sky is the cool fill; a warm
  rim behind;
- the far ridge is a volcanic cone with a glowing crater and a lit plume, set back in the evening air;
- the crust at several scales: pahoehoe ropes and lobes, slabs and clinker (scanned rocks regraded to basalt);
- a deeper blue hour.
"""
from common import camera, finish, piece, point, portrait_of, shot as frame, sky

SKY = 'qwantani_dusk_2_puresky'
LAVA_LIGHT = '#FF6A22'
# the main flow: in from the left foreground, past the speaker's left 2 to 3 m off, away to the back left
FLOW = [[-7.5, -5.0], [-4.8, -3.2], [-3.0, -1.6], [-2.4, 0.2], [-2.7, 2.2], [-3.8, 4.4], [-5.5, 7.0]]
FLOW_W = 0.75
# a few dimmer glows at other scales: a thin crack to the right, a seam crossing far back
CRACK = [[1.4, 0.9], [2.2, 1.1], [3.0, 0.7], [4.1, 0.9]]
SEAM = [[-14.0, 15.0], [-6.0, 13.5], [3.0, 14.5], [14.0, 13.0]]
CONE = (-6.0, 58.0)


def lamp(position, target, irradiance, size, color='#FF5A18'):
    """A soft lamp placed by position (common.area orbits the speaker): a lava glow at its source."""
    return {'type': 'area', 'size_m': list(size), 'position': list(position), 'target': list(target),
            'irradiance': irradiance, 'color': color}


def props():
    rock = dict(rock='dark_rock_02', displace=0.03, albedo=0.06, rough_mul=0.55, rock_tint='#2A2A2A', rock_tint_mix=0.6)
    avoid = [[0.0, 0.0, 1.0]] + [[x, y, 1.3] for x, y in FLOW]
    P = [
        # the near field: pahoehoe ropes and lobes; the flow and the crack carved below a sheet of lava
        piece('ext', module='ember_el', fn='terrain', size=[24.0, 18.0], position=[0.0, 3.0, 0.0], cell=0.02,
              relief=0.07, flat=[0.0, 0.0, 0.6], ropes={'amp': 0.018, 'wave': 0.09, 'dir': 60.0, 'lobes': 0.07},
              channels=[{'points': FLOW, 'width': FLOW_W, 'depth': 0.3, 'bank': 0.35},
                        {'points': CRACK, 'width': 0.03, 'depth': 0.2, 'bank': 0.05}],
              lava_below=True, **rock),
        # the flow's skin: big crust plates, dark red, glowing in their cracks
        piece('ext', module='ember_el', fn='lava_surface', size=[24.0, 18.0], position=[0.0, 3.0, -0.12], cell=0.05,
              lava='acg:Lava001', scale=4.5, strength=30.0, gain=1.6, ripple=0.015, crust_rough=0.8, crust_spec=0.25),
        # its core: a ribbon of open, yellow-hot lava down the middle of the flow
        piece('ext', module='ember_el', fn='fall', points=[[x, y, -0.105] for x, y in FLOW],
              radius=[0.012, 0.03, 0.035, 0.035, 0.03, 0.025, 0.015], flat=7.0, lava='acg:Lava004', scale=1.6,
              strength=90.0, gain=2.4, samples=16),
        # clinker and slabs: scanned rocks regraded to basalt, at two scales
        piece('ext', module='ember_el', fn='rubble', models=['moon_rock_01', 'moon_rock_03', 'moon_rock_05'],
              area=[-7.0, -3.5, 7.0, 9.0], count=90, scale=[1.0, 3.5], avoid=avoid, z=-0.01, seed=5, tilt_deg=30),
        piece('ext', module='ember_el', fn='rubble', models=['rock_09', 'moon_rock_01'],
              area=[-6.0, -2.5, 6.0, 8.0], count=14, scale=[3.5, 7.0], avoid=avoid, z=-0.02, seed=9, tilt_deg=12),
        # the far field, and the volcano: a cone with shoulders, a crater glowing in its top
        piece('ext', module='ember_el', fn='terrain', size=[140.0, 70.0], position=[0.0, 45.0, -0.3], cell=0.15,
              relief=0.5, flat=[0.0, -200.0, 1.0], cones=[[CONE[0], CONE[1], 26.0, 13.0, 4.0], [22.0, 64.0, 18.0, 6.0, 0.0]],
              channels=[{'points': SEAM, 'width': 0.35, 'depth': 0.2, 'bank': 0.5, 'lava': 'flow'}],
              flow='acg:Lava001', flow_emit=30.0, flow_gain=1.8, flow_scale=3.0, **{**rock, 'displace': 0.05}),
        # steam: a low veil over the flow, lit from below, and the volcano's plume
        piece('ext', module='ember_el', fn='steam', box=[-6.5, -4.0, -0.1, -0.8, 6.0, 1.0], density=1.6, scale=0.7,
              anisotropy=0.45),
        piece('ext', module='ember_el', fn='steam', box=[CONE[0] - 6.0, CONE[1] - 5.0, 9.0, CONE[0] + 9.0, CONE[1] + 5.0, 30.0],
              density=0.12, scale=4.0, anisotropy=0.4),
        # a few embers lifting off the flow's core
        piece('ext', module='ember_el', fn='sparks_mixed', area=[-3.4, -1.8, -2.2, 1.0], count=10, height=1.8,
              streak=[0.01, 0.08], radius=[0.001, 0.003], drift=[0.3, 0.1], emit=16.0, seed=4),
    ]
    return P


def lights():
    return {
        # the flow's glow, low from the speaker's left: on the cabinet's front and the ground round it
        'flow_near': lamp([-2.3, -0.4, 0.2], [0.0, -0.1, 0.55], 2.4, (0.5, 2.2), '#FF6A22'),
        'flow_far': lamp([-2.6, 2.0, 0.2], [0.0, 0.3, 0.7], 1.2, (0.5, 2.0), '#FF6A22'),
        # behind the speaker: the warm rim and the light through the acrylic
        'through': lamp([0.15, 0.9, 0.5], [0.0, -0.6, 0.3], 2.0, (0.6, 1.2)),
        'horn': lamp([0.1, 0.8, 1.25], [0.0, -0.2, 1.12], 2.0, (0.9, 0.5)),
        # the crater, lighting its plume from below
        'crater': point([CONE[0], CONE[1], 12.0], 60000, LAVA_LIGHT, 2.0),
    }


def shot():
    cam = camera(height=0.95, distance=6.5, azimuth=22.0, lens=60.0, target=(0.0, 0.0, 0.66), fstop=2.8)
    return frame('ember', props(), cam, sky(SKY, rotation_deg=0.0, strength=0.12), 'barkhorn, Ember A2, a lava field at blue hour',
                 lights=lights(), rotate_z=15.0, exposure=0.0, position=(0.0, 0.0, -0.003),
                 haze={'box_m': [-70.0, -10.0, -0.5, 70.0, 82.0, 35.0], 'density': 0.004, 'anisotropy': 0.4,
                       'color': '#FFFFFF'},
                 fin=finish(bloom=0.18, bloom_px=34, threshold=0.88, vignette=0.2),
                 white_balance=(4400, 10))           # a deeper blue hour, the lava still orange


def portrait():
    cam = camera(height=0.95, distance=6.5, azimuth=22.0, lens=92.0, target=(0.0, 0.0, 0.9), fstop=2.8,
                 focus=(0.0, -0.21, 0.66))
    return portrait_of(shot(), **cam)
