"""Haze, concept A: a lavender field at dusk (round 31b; BRIEF.md is the direction, haze.md the notes).

The plateau of Valensole in early July, minutes before sunset: rows of lavender run away from the lens toward low hills
that recede in violet haze, the sun sinking behind them. The speaker stands in the path between two rows, on the
field's dry soil, turned a little toward the light; the sun behind it comes through the violet acrylic and lays its
colour on the ground. One light: the low sun and the dusk sky it leaves (the_sky_is_on_fire, its sun 3 degrees up), with a soft bounce
from the path in front, as a photographer's reflector.
"""
from common import asset, camera, finish, piece, portrait_of, scatter, shot as frame, sky

SKY, ROT = 'kiara_9_dusk', -128.0                  # the afterglow turned to stand behind the speaker (azimuth 178)
# the sun has just gone: a faint last light from the glow, low enough that the rows and the hills take most of it
SUN = {'azimuth_deg': 178.0, 'elevation_deg': 1.5, 'irradiance': 2.0, 'angle_deg': 3.0, 'color': '#FFC08A'}
SPEAKER = ['[!p]*', 'po*']                         # the speaker's parts (the set's pieces are all named prop<i>-...)
ROW = 1.7                                          # lavender rows, centre to centre (m); the speaker's path is x = 0


def ext(fn, **k):
    return piece('ext', module='haze_el', fn=fn, **k)


def props():
    P = [
        # the field's dry soil, displaced, under the near rows and the path
        piece('ground', texture='farm_soil', size=[14.0, 22.0], position=[0.0, 5.0, 0.0], displace=0.035, res='4k',
              cells=700, relief=None),
        # clods, pebbles and dry clippings on the path, the litter of a harvest
        ext('litter', area=[-0.5, -9.0, 0.5, 6.0], clods=450, pebbles=160, straws=400, avoid=[[0.0, 0.0, 0.42]], seed=3,
            texture='farm_soil'),
        # beyond it, the field running on to the hills
        ext('plane', rows=True, period=ROW, size=[6000.0, 6000.0], position=[0.0, 3000.0, -0.03], colors={'flower': '#7A5FB0', 'leaf': '#6B775A', 'soil': '#7A6A58'}),
        # the lavender: rows either side of the path, the first sharp, the far ones fading into haze
        ext('field', rows=[-ROW * 9.5, ROW * 9.5, ROW], span=[-11.0, 400.0], step=0.8, near=30.0, detail=140,
            clear=[[0.0, 0.0, 0.62]], seed=7,
            colors={'flower': '#7A5FB0', 'flower2': '#9A7CC4', 'leaf': '#6B775A', 'leaf2': '#8C9478', 'stem': '#5E6B47'}),
        # a lone oak out in the field, and a line of them along a far track: the plateau's own landmarks
        scatter(['island_tree_01', 'island_tree_02', 'island_tree_03'], 28, [-420.0, 780.0, 420.0, 830.0], avoid=(), scale=(0.8, 1.25),
                seed=4, res='1k'),
    ]
    return P


def lights():
    return {
        # a white card under the lens throws a little of the eastern sky back onto the speaker's face, as a photographer would
        'bounce': {'type': 'area', 'size_m': [4.0, 3.0], 'orbit': {'azimuth_deg': -10, 'elevation_deg': 25, 'distance_m': 3.0},
                   'target': [0.0, 0.0, 0.7], 'irradiance': 2.0, 'color': '#E2D8F4', 'receivers': SPEAKER},
        # the afterglow behind, through the acrylic and along its edges
        'glow': {'type': 'area', 'size_m': [2.0, 1.2], 'orbit': {'azimuth_deg': 178, 'elevation_deg': 2, 'distance_m': 4.0},
                 'target': [0.0, 0.0, 0.8], 'irradiance': 2.0, 'color': '#FFC8A0', 'camera': False, 'receivers': SPEAKER},
    }


def shot():
    cam = camera(height=1.0, distance=9.5, azimuth=0.0, lens=85, target=(0.0, 0.0, 0.66), fstop=2.8, shift_y=0.06)
    cam['clip_end'] = 20000.0                      # the hills are kilometres off
    return frame('haze', props(), cam, sky(SKY, ROT, strength=0.12, res='4k'), 'barkhorn, Haze, lavender at dusk', exposure=0.35,
                 lights=lights(), sun=dict(SUN),
                 haze={'box_m': [-8000.0, 25.0, 0.0, 8000.0, 8000.0, 40.0], 'density': 0.0009, 'anisotropy': 0.3,
                       'color': '#B8A4D8'},
                 fin=finish(contrast=0.25, clarity=0.04, bloom=0.4, bloom_px=40, threshold=0.85, vignette=0.1),
                 rotate_z=18.0, position=(0.0, 0.0, -0.025), samples=512,
                 white_balance=(5600, 10))                  # daylight balance: the dusk stays warm, the violet stays true


def portrait():
    # nearer, so the speaker keeps its size in the taller frame; the same lens
    return portrait_of(shot(), **camera(height=1.0, distance=6.2, azimuth=0.0, lens=85, target=(0.0, 0.0, 0.66), fstop=4.0,
                                        shift_y=0.1), clip_end=20000.0)
