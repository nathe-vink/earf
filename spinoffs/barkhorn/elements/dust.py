"""Dust, in its element (round 31b; dust.md has the concept, the references and the critic passes): the American
Southwest at golden hour. Wind-rippled red sand, the big flat sandstone plateaus behind (mesas and buttes in Monument
Valley's spirit, as the owner asked), a tumbleweed, dust hanging in the low raking light that comes through the orange
acrylic, and long shadows.

The engine's camera sees 300 m, so the plateaus stand at 180 to 280 m at a tenth of Monument Valley's size: a butte
30 m tall at 280 m fills the same angle as a 300 m butte at 2.8 km, and a lens focused at 6 m sees both at infinity.
"""
import math, os

from common import area, camera, finish, piece, portrait_of, shot as frame, sky, sun_from_sky

HDRI, ROT = 'qwantani_sunset_puresky', float(os.environ.get('DUST_ROT', 264.0))           # a clear evening, the sky's sun 6 degrees up at azimuth 150 (behind the speaker's right)
SAND = dict(material='pbr', texture='red_sand', tex_scale=0.6, tint='#B4704A', tint_mix=0.7, res='4k',
            rough_mul=1.0, bump=0.8)
ROCK = dict(material='pbr', texture='cliff_side', tex_scale=3.0, tint='#6E321C', tint_mix=0.6, res='2k', vary=[30.0, 0.45],
            displace=4.0, beds=[1.6, 0.9])
WB = (float(os.environ.get('DUST_WB', 6200)), 10.0)    # a photographer's warm white balance at golden hour
CAM = dict(height=0.6, distance=7.4, azimuth=-20.0, lens=65.0, target=(0.0, 0.0, 0.66), fstop=2.8, shift_x=0.1, shift_y=0.03)


def _eye(cam):
    az = math.radians(cam['azimuth'])
    tx, ty, _ = cam['target']
    return tx + cam['distance'] * math.sin(az), ty - cam['distance'] * math.cos(az)


def at(dist, ang, cam=CAM):
    """A ground point `dist` metres from the camera, `ang` degrees right of its line of sight."""
    ex, ey = _eye(cam)
    tx, ty, _ = cam['target']
    h = math.atan2(ty - ey, tx - ex) - math.radians(ang)
    return round(ex + dist * math.cos(h), 2), round(ey + dist * math.sin(h), 2)


def plateau(dist, ang, radius, height, seed, squash=0.55, cliff=0.4, wander=0.22, turn=0.0):
    x, y = at(dist, ang)
    return piece('ext', module='dust_el', fn='mesa', position=[x, y, -0.5], rotate=[0, 0, turn], radius=radius, height=height, seed=seed,
                 squash=squash, cliff=cliff, wander=wander, ledge=0.014, **ROCK)


def props():
    ex, ey = _eye(CAM)
    tx, ty, _ = CAM['target']
    heading = math.degrees(math.atan2(ty - ey, tx - ex))
    out = [piece('ext', module='dust_el', fn='terrain', eye=[round(ex, 3), round(ey, 3)], heading=round(heading, 2),
                 half_angle=42.0, r0=1.2, r1=292.0, segments=460, flat=[0.0, 0.0, 2.2], swell=0.35, swell_size=16.0,
                 rim=1.6, vary=[20.0, 0.4], duals=[], ripples=[0.09, 0.32, 30.0, 2.5, 15.0],
                 swell2=[0.15, 5.0], albedo=0.95, spec=0.05, **SAND),
           # under everything, out of the camera's sight: ground for the light to bounce off on every side
           piece('box', size=[700.0, 700.0, 0.1], position=[0.0, 0.0, -0.45], **SAND)]
    # the plateaus: a broad mesa to the right, a slim butte and a long low mesa to the left, one more far off
    out += [plateau(260, 12, 30, 19, 1, squash=0.45, turn=45.0),
            plateau(225, -9, 6, 17, 2, squash=0.9, cliff=0.45),
            plateau(288, -22, 36, 11, 3, squash=0.35),
            plateau(285, 1, 22, 7, 4, squash=0.4, cliff=0.5)]
    # the tumbleweed, rolling past farther back on the gust, its dust trailing behind it
    out += [piece('ext', module='dust_el', fn='tumbleweed', diameter=0.55, seed=11, position=[4.5, 4.0, 0.27], snap=0.02,
                  stems=40, branches=8, twigs=6, rotate=[8, 14, 30], scale=[1.0, 1.0, 0.9], color='#A89070')]
    # veils of dust lifting off the flat between the speaker and the sun, glowing in the backlight
    out += [piece('ext', module='dust_el', fn='dust', size=[10.0, 4.0, 1.5], position=[4.0, 14.0, -0.05], density=0.15,
                  wisp=1.5, anisotropy=0.7, color='#EDC29A'),
            piece('ext', module='dust_el', fn='dust', size=[14.0, 5.0, 1.5], position=[9.0, 22.0, -0.05], density=0.15,
                  wisp=2.0, anisotropy=0.7, color='#EDC29A')]
    return out


def lights():
    # the sun on the sand in front bounces back into the speaker's face: a photographer's warm reflector, low
    return {'bounce': area(-25, 3, 4.0, 5.0, '#F2B07E', (10.0, 2.0), (0.0, 0.0, 0.55))}


def shot():
    return frame('dust', props(), camera(**CAM), dict(sky(HDRI, ROT, strength=0.45, res='4k'), grade={'horizon': '#F4B98C', 'zenith': '#A8AEC2', 'height_deg': 20.0}),
                 'barkhorn, Dust, the Southwest at golden hour', lights=lights(),
                 sun=dict(sun_from_sky(HDRI, ROT, irradiance=24.0, angle_deg=0.5), elevation_deg=7.0),
                 fin=finish(contrast=0.18, clarity=0.04, saturation=0.0, vignette=0.18, bloom=0.07, threshold=0.95),
                 haze={'box_m': [-320.0, -30.0, -1.0, 320.0, 320.0, 70.0], 'density': 0.0005, 'anisotropy': 0.4,
                       'color': '#E8DCD0'},
                 rotate_z=0.0, position=(0.0, 0.0, -0.015), white_balance=WB, exposure=0.5)


def portrait():
    c = dict(CAM, distance=5.2, lens=55.0)
    return portrait_of(shot(), **camera(**c))
