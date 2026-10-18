"""Haze, concept A: a lavender field at dusk (round 31b; BRIEF.md is the direction, haze.md the notes).

The plateau of Valensole in early July, minutes before sunset: rows of lavender run away from the lens toward low hills
that recede in violet haze, the sun sinking behind them. The speaker stands in the path between two rows, on the
field's dry soil, turned a little toward the light; the sun behind it comes through the violet acrylic and lays its
colour on the ground. One light: the low sun and the dusk sky it leaves (the_sky_is_on_fire, its sun 3 degrees up), with a soft bounce
from the path in front, as a photographer's reflector.
"""
from common import asset, camera, finish, piece, portrait_of, scatter, shot as frame, sky

SKY, ROT = 'the_sky_is_on_fire', -165.0            # its sun turned to stand behind the speaker's right shoulder
# the sun, where this sky's glow is, turned so (azimuth 176: just right of the speaker; read off the renders: assets.hdri_sun's
# brightest patch is a cloud about 20 degrees left of the glow), a disc sinking into the haze over the hills
SUN = {'azimuth_deg': 176.0, 'elevation_deg': 4.5, 'irradiance': 15.0, 'angle_deg': 0.6, 'color': '#FF9A40'}
DISC_EL = 3.4                                      # the disc sits in the sky's glow; the lamp a little higher, so it reaches over the rows
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
        ext('litter', area=[-0.5, -9.0, 0.5, 6.0], clods=900, pebbles=160, straws=400, avoid=[[0.0, 0.0, 0.42]], seed=3,
            texture='farm_soil'),
        # beyond it, the field running on to the hills
        ext('plane', rows=True, period=ROW, size=[6000.0, 6000.0], position=[0.0, 3000.0, -0.03], colors={'flower': '#5A4A9E', 'leaf': '#6B775A', 'soil': '#7A6A58'}),
        # the lavender: rows either side of the path, the first sharp, the far ones fading into haze
        ext('field', rows=[-ROW * 9.5, ROW * 9.5, ROW], span=[-11.0, 400.0], step=0.8, near=30.0, detail=140,
            clear=[[0.0, 0.0, 0.62]], seed=7,
            colors={'flower': '#5A4A9E', 'flower2': '#8466BC', 'leaf': '#6B775A', 'leaf2': '#8C9478', 'stem': '#5E6B47'}),
        # ranges of low, rounded hills behind (the Luberon's spirit), each a little higher and further, for the haze to layer
        ext('hills', size=[3000.0, 300.0], position=[0.0, 600.0, -0.5], height=10.0, texture='aerial_grass_rock', seed=2,
            tint='#5E5470', tint_mix=0.35, cells=400, scale=500.0, octaves=3, rough=0.03),
        ext('hills', size=[6000.0, 800.0], position=[200.0, 1700.0, -2.0], height=40.0, texture='aerial_grass_rock', seed=5,
            tint='#5E5470', tint_mix=0.35, cells=400, scale=700.0, octaves=3, rough=0.03),
        ext('hills', size=[12000.0, 1500.0], position=[-500.0, 4200.0, -6.0], height=110.0, texture='aerial_grass_rock', seed=9,
            tint='#5E5470', tint_mix=0.35, cells=400, scale=1200.0, octaves=3, rough=0.03),
        # a lone oak out in the field, and a line of them along a far track: the plateau's own landmarks
        asset('island_tree_01', [30.0, 240.0, 0.0], rotate=(0, 0, 40), scale=1.0, res='1k'),
        scatter(['island_tree_01', 'island_tree_02', 'island_tree_03'], 28, [-420.0, 780.0, 420.0, 830.0], avoid=(), scale=(0.8, 1.25),
                seed=4, res='1k'),
        ext('sun', azimuth_deg=SUN['azimuth_deg'], elevation_deg=DISC_EL, distance=20000.0, diameter_deg=0.55,
            strength=60.0, color='#FF6A2A'),
    ]
    return P


def lights():
    return {
        # the light off the dry path in front, warm and soft, as a reflector would throw it
        'bounce': {'type': 'area', 'size_m': [1.6, 1.2], 'orbit': {'azimuth_deg': -20, 'elevation_deg': 8, 'distance_m': 3.0},
                   'target': [0.0, 0.0, 0.7], 'irradiance': 1.2, 'color': '#E8C8D8',
                   'receivers': SPEAKER},
        # the low sun behind the speaker, on its axis, carried through the acrylic and along its edges (the sun lamp alone
        # is mostly stopped by the rows at 2 degrees)
        'through': {'type': 'area', 'size_m': [1.6, 2.4], 'orbit': {'azimuth_deg': 176, 'elevation_deg': 18, 'distance_m': 2.5},
                    'target': [0.0, 0.0, 0.8], 'irradiance': 9.0, 'color': '#FFA860', 'camera': False, 'receivers': SPEAKER},
        # the glow of the sky low behind, grazing both sides so the acrylic's polished edges catch it
        'rim_l': {'type': 'area', 'size_m': [0.6, 1.6], 'orbit': {'azimuth_deg': -140, 'elevation_deg': 6, 'distance_m': 2.2},
                  'target': [0.0, 0.0, 0.7], 'irradiance': 3.0, 'color': '#FFB98A', 'camera': False, 'specular': 0, 'receivers': SPEAKER},
        'rim_r': {'type': 'area', 'size_m': [0.6, 1.6], 'orbit': {'azimuth_deg': 145, 'elevation_deg': 6, 'distance_m': 2.2},
                  'target': [0.0, 0.0, 0.7], 'irradiance': 2.5, 'color': '#F5B0A0', 'camera': False, 'specular': 0, 'receivers': SPEAKER},
        # a card the horn's gloss mirrors instead of the dark ground, unseen by the camera
        'card': {'type': 'panel', 'size_m': [1.5, 1.0], 'position': [0.0, -2.0, 1.15], 'target': [0.0, 0.0, 1.15], 'strength': 0.35,
                 'color': '#C8B0D0', 'diffuse': 0, 'specular': 1, 'receivers': SPEAKER},
    }


def shot():
    cam = camera(height=0.55, distance=9.5, azimuth=0.0, lens=85, target=(0.0, 0.0, 0.66), fstop=4.0, shift_y=0.12)
    cam['clip_end'] = 20000.0                      # the hills are kilometres off
    return frame('haze', props(), cam, sky(SKY, ROT, strength=0.55, res='4k'), 'barkhorn, Haze, lavender at dusk', exposure=0.25,
                 lights=lights(), sun=dict(SUN),
                 haze={'box_m': [-8000.0, 8.0, 0.0, 8000.0, 8000.0, 80.0], 'density': 0.0003, 'anisotropy': 0.3,
                       'color': '#B8A4D8'},
                 fin=finish(contrast=0.25, clarity=0.04, bloom=0.4, bloom_px=40, threshold=0.85, vignette=0.1),
                 rotate_z=18.0, position=(0.0, 0.0, -0.015), samples=512,
                 white_balance=(5600, 3))                  # daylight balance: the dusk stays warm, the violet stays true


def portrait():
    # the same low eye, a little nearer and the frame shifted up, so the speaker keeps its size and the sun stays in
    cam = camera(height=0.55, distance=6.0, azimuth=0.0, lens=85, target=(0.0, 0.0, 0.66), fstop=4.0, shift_y=0.07)
    cam['clip_end'] = 20000.0
    return portrait_of(shot(), **cam)
