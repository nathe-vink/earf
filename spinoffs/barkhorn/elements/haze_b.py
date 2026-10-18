"""Haze, concept B: ranges at dusk, layer after layer into violet haze. "Dusk, kept indoors."

Real mountain ranges at dusk (a photographed sky, Poly Haven kiara_9_dusk), the sun just gone behind them, its glow a
little left of the speaker; a veil of lavender haze between the near ridge and the ranges, so each ridge is paler than
the one in front. The speaker stands on the near ridge in dry grass, at eye level, the last light behind it.

The first version (passes 1 to 3) modelled the ranges as heightfields; three blind critics in a row scored it 5.5 and
called the hills CG mounds, so the ranges are now the photograph's own (haze_b.md has the history). The set's pieces
are in studio/engine/kit_ext/haze_b_el.py (the ridge, the haze, the dry grass).
"""
import os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common as C                                        # noqa: E402

SKY = 'kiara_9_dusk'                                      # real ranges at dusk, the sun just behind them
SKY_ROT = -113.7                                          # its sun's glow (azimuth 163.5) just above the horn
SKY_RES = '8k'
HAZE = 0.0007                                             # the veil's density (per metre, over about 200 m)
CAM = dict(height=1.0, distance=10.0, azimuth=-15.0, lens=85.0, fstop=5.6)

RIDGE = {'area': [-10.0, -13.0, 9.0, 7.0], 'cell': 0.02, 'crest_y': 1.4, 'drop': 5.0, 'relief': 0.10, 'flat_r': 0.8,
         'slope_front': 0.02}

# a photographer's reflector beside the camera, out of frame, catching the dusk sky, so the speaker's front is not
# lost against the glow behind it
BOUNCE = C.area(-25.0, 25.0, 2.5, 16.0, '#F5D6BC', size=(1.0, 1.0))   # close, so it falls off before the grass

# stiff straw: no curl along the blade (rough 0), a little scatter at the tips only
STRAW = dict(ground=RIDGE, color='#4E3E2C', color2='#3A2E22', tip='#8A7050', value_jitter=0.2, rough=0.0, rough2=0.0,
             rough_end=0.02)


def ext(fn, **k):
    return C.piece('ext', module='haze_b_el', fn=fn, **k)


def props(cam_xy=(-2.6, -9.7)):
    clear = [[0.0, -0.3, 2.2], [-0.5, -2.0, 2.2], [*cam_xy, 1.0]]   # tall grass: off the speaker, its camera side
    return [
        ext('ridge', texture='sparse_grass', res='4k', displace=0.06, tint='#6A5640', tint_mix=0.6, value=0.55,
            matte=True, **RIDGE),
        # one veil between the ridge and the photographed ranges, its far wall short of the camera's clip (300 m) so
        # every ray leaves through it (a wall beyond the clip leaves the angled rays unhazed)
        ext('haze', boxes=[{'box': [-150.0, -30.0, -60.0, 200.0, 200.0, 80.0], 'density': HAZE, 'color': '#D9CCEB',
                            'anisotropy': 0.7}]),
        # dry grass in four hair systems: fine and coarse tall grass round the frame, short grass round the speaker,
        # a denser ring at its feet
        ext('grass', area=[-6.0, -8.5, 6.0, 3.0], avoid=clear, count=6000, children=12, length=[0.15, 0.5], **STRAW,
            seed=3, patchy=0.9, clump=0.4, clump_r=0.05),
        ext('grass', area=[-6.0, -8.5, 6.0, 3.0], avoid=clear, count=2500, children=6, length=[0.15, 0.45], **STRAW,
            seed=8, patchy=0.75, root_mm=1.8, tip_mm=0.35, random=0.2),
        ext('grass', area=[-2.3, -2.6, 2.3, 2.0], within=[0.0, -0.3, 2.3], avoid=[[0.0, 0.0, 0.5]], count=2500,
            children=12, length=[0.06, 0.22], **STRAW, seed=5, patchy=0.9),
        ext('grass', area=[-0.8, -0.8, 0.8, 0.8], within=[0.0, 0.0, 0.8], avoid=[[0.0, 0.0, 0.36], [0.0, -0.4, 0.22]], count=225,
            children=10, length=[0.03, 0.10], **STRAW, seed=6, patchy=1.0, cell=0.04),
    ]


def shot():
    cam = C.camera(target=(0.0, 0.0, 1.09), shift_x=-0.16, **CAM)
    sun = C.sun_from_sky(SKY, SKY_ROT, irradiance=12.0, color='#FFC88A')
    sun['elevation_deg'] = 6.0                            # clears the photographed ridge, so it rims the speaker
    return C.shot('haze_b', props(), cam, C.sky(SKY, SKY_ROT, 1.0, res=SKY_RES), 'Haze in its element: ranges at dusk',
                  sun=sun, lights={'bounce': BOUNCE}, white_balance=(5000, 15), rotate_z=10.0,
                  position=(0.0, 0.0, -0.008), exposure=-3.2, look='AgX - Medium High Contrast',
                  fin=C.finish(contrast=0.10, clarity=0.1, sharpen=0.2, vignette=0.12, saturation=0.12, bloom=0.04,
                               bloom_px=40, threshold=0.8))


def portrait():
    """The 4:5 frame, re-framed: a longer lens from closer, so the speaker keeps its share of the taller frame and
    the ranges stack higher behind it; the sun's glow stays a little left of it."""
    s = C.portrait_of(shot())
    s['camera'] = C.camera(height=1.0, distance=7.5, azimuth=-15.0, lens=105.0, fstop=5.6, target=(0.0, 0.0, 1.26),
                           shift_x=-0.12)
    s['set']['props'] = props(tuple(s['camera']['position'][:2]))
    return s
