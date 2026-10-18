"""Dust B, in its element (round 31b, the owner's second note on Dust; dust_b.md has the concept and the passes):
Monument Valley under a blue afternoon sky with fair-weather cumulus. Red sand and stony ground; sagebrush, yucca and
prickly pear; and behind, at their real size and distance, the flat-topped red buttes everyone knows: sheer sandstone
cliffs over pale talus aprons, two of them with the Mittens' slender thumbs. A tumbleweed has fetched up against a
sagebrush. (No saguaros: they do not grow here.)
"""
import math, os

from common import area, camera, finish, piece, portrait_of, shot as frame, sky, sun_from_sky

HDRI = 'kloppenheim_06_puresky'
ROT = float(os.environ.get('DUSTB_ROT', 330.0))          # the sky's sun 21 degrees up at azimuth 92 (the speaker's right)
SAND = dict(material='pbr', texture='red_sand', tex_scale=1.6, tint='#C0633A', tint_mix=0.6, res='4k', bump=0.8)
STONY = dict(texture='red_mud_stones', tex_scale=1.5, tint='#B8603A', tint_mix=0.8, mask=[5.0, 0.25], bump=1.0)
CLIFF = dict(material='pbr', texture='rock_face', tex_scale=30.0, tint='#C04A24', tint_mix=0.92, res='4k',
             vary=[180.0, 0.3], beds=[18.0, 0.18], streaks=[7.0, 0.5], albedo=1.9)
TALUS = dict(material='pbr', texture='red_mud_stones', tex_scale=25.0, tint='#A85E44', tint_mix=0.55, res='2k',
             vary=[120.0, 0.3], albedo=1.3, beds=[9.0, 0.4])
CAM = dict(height=0.5, distance=6.5, azimuth=-12.0, lens=50.0, target=(0.0, 0.0, 0.66), fstop=5.6, shift_x=0.08)
CLIP = 12000.0


def _eye(cam):
    az = math.radians(cam['azimuth'])
    tx, ty, _ = cam['target']
    return tx + cam['distance'] * math.sin(az), ty - cam['distance'] * math.cos(az)


def at(dist, ang, cam=CAM):
    """A ground point `dist` metres from the camera, `ang` degrees right of its line of sight."""
    ex, ey = _eye(cam)
    tx, ty, _ = cam['target']
    h = math.atan2(ty - ey, tx - ex) - math.radians(ang)
    return round(ex + dist * math.cos(h), 1), round(ey + dist * math.sin(h), 1)


def butte(dist, ang, radius, height, seed, turn=0.0, thumbs=(), squash=0.6, spread=2.0, talus_h=0.38):
    x, y = at(dist, ang)
    return piece('ext', module='dust_b_el', fn='butte', position=[x, y, -3.0], rotate=[0, 0, turn], radius=radius,
                 height=height, seed=seed, thumbs=[list(t) for t in thumbs], squash=squash, spread=spread,
                 talus_h=talus_h, cliff_mat=CLIFF, talus_mat=TALUS)


def props():
    ex, ey = _eye(CAM)
    tx, ty, _ = CAM['target']
    heading = math.degrees(math.atan2(ty - ey, tx - ex))
    out = [piece('ext', module='dust_b_el', fn='terrain', eye=[round(ex, 3), round(ey, 3)], heading=round(heading, 2),
                 half_angle=44.0, r0=1.2, r1=CLIP * 0.8, segments=460, flat=[0.0, 0.0, 2.2], swell=0.45,
                 swell_size=18.0, rim=60.0, vary=[14.0, 0.35], ripples=[0.11, 0.25, 20.0, 6.0, 6.0],
                 swell2=[0.12, 5.0], albedo=0.92, spec=0.05, mixes=[STONY], **SAND),
           piece('box', size=[600.0, 600.0, 0.1], position=[0.0, 0.0, -0.5], **SAND)]
    # the buttes, at their real size: the Mittens to the left and right of the horn, a long mesa beyond
    out += [butte(3000, -6, 230, 300, 1, turn=10, thumbs=[(185, 1.38, 30, 0.86)], squash=0.55),
            butte(3600, 15, 260, 290, 2, turn=-15, thumbs=[(-5, 1.35, 32, 0.84)], squash=0.5),
            butte(5200, 27, 900, 320, 3, turn=5, squash=0.3, spread=1.6),
            butte(8200, -32, 1100, 260, 4, turn=0, squash=0.25, spread=1.5)]
    # the near ground's plants: prickly pear beside the speaker, a yucca behind it, sagebrush, the tumbleweed
    out += [piece('ext', module='dust_b_el', fn='prickly_pear', position=[1.05, 0.2, -0.01], size=0.2, pads=22, seed=3, color='#677A52', color2='#7F8460'),
            piece('ext', module='dust_b_el', fn='yucca', position=[-1.6, 1.5, -0.01], length=0.6, width=0.022, leaves=64,
                  seed=5),
            piece('ext', module='dust_b_el', fn='sagebrush', position=[2.9, 4.2, -0.02], size=[1.0, 0.9, 0.75], seed=7),
            piece('ext', module='dust_b_el', fn='tumbleweed', diameter=0.55, seed=11, position=[2.35, 3.7, 0.27],
                  snap=0.03, stems=40, branches=8, twigs=6, rotate=[8, 14, 30], color='#A89070'),
            piece('ext', module='dust_b_el', fn='sagebrush', position=[-3.2, 6.5, -0.02], size=[1.1, 1.0, 0.8], seed=8),
            piece('ext', module='dust_b_el', fn='sagebrush', position=[6.5, 12.0, -0.02], size=[1.2, 1.0, 0.8], seed=9),
            piece('ext', module='dust_b_el', fn='sagebrush', position=[-8.0, 16.0, -0.02], size=[1.0, 0.9, 0.7], seed=10),
            piece('ext', module='dust_b_el', fn='yucca', position=[4.5, 8.5, -0.01], length=0.5, width=0.02, leaves=50,
                  seed=12),
            piece('ext', module='dust_b_el', fn='sagebrush', position=[11.0, 22.0, -0.02], size=[1.0, 0.9, 0.7], seed=21, leaves=3000),
            piece('ext', module='dust_b_el', fn='sagebrush', position=[-14.0, 28.0, -0.02], size=[1.2, 1.0, 0.8], seed=22, leaves=3000),
            piece('ext', module='dust_b_el', fn='sagebrush', position=[3.0, 35.0, -0.02], size=[1.0, 0.9, 0.7], seed=23, leaves=3000),
            piece('ext', module='dust_b_el', fn='sagebrush', position=[20.0, 45.0, -0.02], size=[1.1, 1.0, 0.8], seed=24, leaves=2500),
            piece('ext', module='dust_b_el', fn='sagebrush', position=[-25.0, 55.0, -0.02], size=[1.0, 0.9, 0.7], seed=25, leaves=2500),
            piece('ext', module='dust_b_el', fn='yucca', position=[-6.5, 10.0, -0.01], length=0.55, width=0.02, leaves=50, seed=26),
            piece('ext', module='dust_b_el', fn='prickly_pear', position=[-4.0, 3.5, -0.01], size=0.2, pads=14, seed=27,
                  color='#677A52', color2='#7F8460'),
            piece('ext', module='dust_b_el', fn='prickly_pear', position=[2.2, -3.0, -0.01], size=0.24, pads=26, seed=13, color='#677A52', color2='#7F8460')]
    return out


def lights():
    # a soft bounce off the sunlit sand into the speaker's front, as a reflector would give
    return {'bounce': area(-30, 8, 4.0, 0.6, '#F3D6BE', (4.0, 2.0), (0.0, 0.0, 0.6))}


def _cam(**k):
    c = camera(**dict(CAM, **k))
    c['clip_end'] = CLIP
    return c


def shot():
    return frame('dust', props(), _cam(), sky(HDRI, ROT, strength=float(os.environ.get('DUSTB_SKY', 0.6)), res='4k'),
                 'barkhorn, Dust, Monument Valley in the afternoon', lights=lights(),
                 sun=sun_from_sky(HDRI, ROT, irradiance=float(os.environ.get('DUSTB_SUN', 9.0)), angle_deg=0.53, color='#FFC98E'),
                 fin=finish(contrast=0.08, clarity=0.05, saturation=0.04, vignette=0.12),
                 haze={'box_m': [-8000.0, -60.0, -5.0, 8000.0, 8000.0, 500.0], 'density': 0.000025,
                       'anisotropy': 0.3, 'color': '#DCD9D6'},
                 rotate_z=20.0, position=(0.0, 0.0, -0.012), exposure=float(os.environ.get('DUSTB_EXP', 0.0)))


def portrait():
    return portrait_of(shot(), **_cam(distance=5.6, lens=60.0, shift_x=0.0))
