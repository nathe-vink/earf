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
FLOW = [[0.2, -4.6], [-0.6, -2.6], [-1.5, -1.2], [-2.0, 0.6], [-2.6, 2.6], [-4.0, 4.6], [-6.5, 7.5]]
FLOW_W = 0.75
# a few dimmer glows at other scales: a thin crack to the right, a seam crossing far back


def _core(pts, n=6, seed=3):
    """The flow's line densified (n per span, linear), and a core half-height that swells and pinches along it."""
    import random
    rnd = random.Random(seed); out, rad = [], []
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        for k in range(n):
            t = k / n; out.append([x0 + (x1 - x0) * t, y0 + (y1 - y0) * t])
    out.append(list(pts[-1]))
    for i in range(len(out)):
        f = i / (len(out) - 1)
        taper = min(1.0, 4 * f, 3 * (1 - f) + 0.3)
        rad.append(round(0.028 * taper * rnd.uniform(0.55, 1.15), 4))
    return out, rad


CORE, CORE_R = _core(FLOW)
CRACK = [[1.9, -2.8], [1.5, -1.9], [1.65, -1.0], [1.3, -0.1], [1.0, 1.0], [1.3, 2.4], [1.0, 3.6]]
SEAM = [[-14.0, 15.0], [-6.0, 13.5], [3.0, 14.5], [14.0, 13.0]]
CONE = (-30.0, 52.0)
# the core's colour: deep red at its skin, through orange to a yellow heart (no white: it reads as a lamp)
CORE_RAMP = [(0.0, '#100000'), (0.3, '#6A0A00'), (0.55, '#E03A00'), (0.8, '#FF8A10'), (1.0, '#FFC040')]
# skylights and small pools through the crust, out in the field: [x, y, r, depth]
GLOWS = [[0.6, 4.2, 0.2, 0.3], [0.7, 7.2, 0.32, 0.3], [-1.0, 5.6, 0.14, 0.3], [1.15, 3.0, 0.1, 0.3]]


def lamp(position, target, irradiance, size, color='#FF5A18', **kw):
    """A soft lamp placed by position (common.area orbits the speaker): a lava glow at its source."""
    return {'type': 'area', 'size_m': list(size), 'position': list(position), 'target': list(target),
            'irradiance': irradiance, 'color': color, **kw}


def props():
    rock = dict(rock='dark_rock_02', displace=0.06, albedo=0.045, rough_mul=0.85, rock_tint='#2A2A2A', rock_tint_mix=0.6)
    avoid = [[0.0, 0.0, 1.0], [0.0, 1.8, 1.4]] + [[x, y, 1.2] for x, y in FLOW] + [[x, y, 0.3] for x, y in CRACK] + [[x, y, r + 0.3] for x, y, r, _ in GLOWS]
    P = [
        # the near field: pahoehoe ropes and lobes; the flow and the crack carved below a sheet of lava
        piece('ext', module='ember_el', fn='terrain', size=[24.0, 18.0], position=[0.0, 3.0, 0.0], cell=0.02,
              relief=0.15, flat=[0.0, 0.0, 0.6], ropes={'amp': 0.01, 'wave': 0.08, 'dir': 60.0, 'lobes': 0.1},
              channels=[{'points': FLOW, 'width': FLOW_W, 'depth': 0.32, 'bank': 0.3},
                        {'points': CRACK, 'width': 0.07, 'depth': 0.3, 'bank': 0.1}],
              pools=GLOWS,
              lava_below=True, **rock),
        # the flow's skin: big crust plates, dark red, glowing in their cracks
        piece('ext', module='ember_el', fn='lava_surface', size=[24.0, 18.0], position=[0.0, 3.0, -0.2], cell=0.05,
              lava='acg:Lava001', tex_scale=4.5, strength=30.0, gain=1.25, ripple=0.02, crust_rough=0.95, crust_spec=0.0),
        # its core: a ribbon of open, yellow-hot lava down the middle of the flow
        # (sunk into the skin so its ripples break the core's edges; its width swells and pinches along the flow)
        piece('ext', module='ember_el', fn='fall', points=[[x, y, -0.215] for x, y in CORE],
              radius=CORE_R, flat=6.0, lava='acg:Lava004', tex_scale=1.2, strength=4.0, gain=2.4,
              ramp=CORE_RAMP, crust_rough=0.9, crust_spec=0.0, samples=6),
        # the dimmer glows out in the field, under the right-hand crust: the crack and the skylights
        piece('ext', module='ember_el', fn='lava_surface', size=[2.1, 11.6], position=[1.55, 3.2, -0.19], cell=0.05,
              lava='acg:Lava004', tex_scale=1.0, strength=5.0, gain=1.6, ripple=0.01, ramp=CORE_RAMP, crust_rough=0.8),
        # clinker and slabs: scanned rocks regraded to basalt, at two scales
        piece('ext', module='ember_el', fn='rubble', models=['moon_rock_01', 'moon_rock_03', 'moon_rock_05'],
              area=[-7.0, -1.8, 7.0, 9.0], count=90, scale=[1.0, 3.5], avoid=avoid, z=-0.01, seed=5, tilt_deg=30),
        piece('ext', module='ember_el', fn='rubble', models=['rock_09', 'moon_rock_01'],
              area=[-6.0, -0.8, 6.0, 8.0], count=14, scale=[3.5, 7.0], avoid=avoid, z=-0.02, seed=9, tilt_deg=12),
        # the far field, and the volcano: a cone with shoulders, a crater glowing in its top
        piece('ext', module='ember_el', fn='terrain', size=[140.0, 70.0], position=[0.0, 45.0, -0.3], cell=0.15,
              relief=0.7, flat=[0.0, -200.0, 1.0], cones=[[CONE[0], CONE[1], 24.0, 7.5, 4.0]],
              channels=[{'points': SEAM, 'width': 0.35, 'depth': 0.2, 'bank': 0.5, 'lava': 'flow'}],
              flow='acg:Lava001', flow_emit=30.0, flow_gain=1.8, flow_scale=3.0, **{**rock, 'displace': 0.05}),
        # steam: a low veil over the flow, lit from below, and the volcano's plume
        piece('ext', module='ember_el', fn='steam', box=[-6.5, -5.0, -0.1, 0.8, 8.0, 1.0], density=6.0, scale=0.4,
              anisotropy=0.45),
        piece('ext', module='ember_el', fn='steam', box=[CONE[0] - 6.0, CONE[1] - 5.0, 9.0, CONE[0] + 9.0, CONE[1] + 5.0, 30.0],
              density=0.8, scale=1.5, anisotropy=0.4),
        # a few embers lifting off the flow's core
        piece('ext', module='ember_el', fn='sparks_mixed', area=[-2.4, -1.6, -1.2, 1.4], count=40, height=1.2,
              streak=[0.005, 0.06], radius=[0.001, 0.005], drift=[0.3, 0.1], emit=16.0, seed=4),
    ]
    return P


def lights():
    return {
        # the flow's glow, low from the speaker's left: on the cabinet's front and the ground round it
        'flow_near': lamp([-1.6, -1.2, 0.3], [0.0, -0.1, 0.6], 4.0, (0.4, 1.5), '#FF6A22', specular=0.0),
        'flow_far': lamp([-2.1, 1.0, 0.15], [0.0, 0.3, 0.7], 1.0, (0.5, 2.0), '#FF6A22', specular=0.0),
        # the lava's light across the slab to the speaker's right, grazing
        'graze': lamp([-1.4, -0.6, 0.12], [1.5, -0.4, 0.0], 2.5, (0.4, 1.5), '#FF6A22', specular=0.0),
        # behind the speaker: the warm rim and the light through the acrylic
        # (no specular: their reflections in the horn and down the cabinet's edge read as hidden lamps)
        'through': lamp([-0.8, 1.0, 0.4], [0.0, 0.0, 0.6], 3.5, (2.0, 1.5), specular=0.0),
        'horn': lamp([-0.4, 0.8, 1.2], [0.0, -0.1, 1.12], 1.0, (1.2, 0.6), specular=0.0),
        # the cabinet's red light on the rock at its foot
        'pool': lamp([0.0, -0.3, 0.3], [0.0, -0.45, 0.0], 2.0, (1.2, 0.6), '#C8281E', specular=0.0),
        # the crater, lighting its plume from below
        'crater': point([CONE[0], CONE[1], 6.8], 15000, LAVA_LIGHT, 2.0),
    }


def shot():
    cam = camera(height=0.95, distance=6.5, azimuth=22.0, lens=60.0, target=(0.0, 0.0, 0.66), fstop=2.8)
    return frame('ember', props(), cam, sky(SKY, rotation_deg=0.0, strength=0.10), 'barkhorn, Ember A2, a lava field at blue hour',
                 lights=lights(), rotate_z=15.0, exposure=0.0, position=(0.0, 0.0, -0.003),
                 haze={'box_m': [-70.0, -10.0, -0.5, 70.0, 82.0, 35.0], 'density': 0.0025, 'anisotropy': 0.4,
                       'color': '#C8D6FF'},
                 fin=finish(bloom=0.18, bloom_px=34, threshold=0.88, vignette=0.2),
                 white_balance=(4400, 10))           # a deeper blue hour, the lava still orange


def portrait():
    cam = camera(height=0.95, distance=6.5, azimuth=22.0, lens=92.0, target=(0.0, 0.0, 0.9), fstop=2.8,
                 focus=(0.0, -0.21, 0.66))
    return portrait_of(shot(), **cam)
