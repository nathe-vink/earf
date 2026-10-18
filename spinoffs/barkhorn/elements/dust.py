"""Dust, in its element (round 31b; dust.md has the concept, the references and the critic passes): the American
Southwest at golden hour. Wind-rippled red sand, the big flat sandstone plateaus behind (mesas and buttes in Monument
Valley's spirit, as the owner asked), a tumbleweed, dust hanging in the low raking light that comes through the orange
acrylic, and long shadows.

The engine's camera sees 300 m, so the plateaus stand at 180 to 280 m at a tenth of Monument Valley's size: a butte
30 m tall at 280 m fills the same angle as a 300 m butte at 2.8 km, and a lens focused at 6 m sees both at infinity.
"""
import math, os

from common import area, camera, finish, piece, portrait_of, shot as frame, sky, sun_from_sky

HDRI, ROT = 'qwantani_sunset_puresky', float(os.environ.get('DUST_ROT', 264.0))           # a clear evening, the sky's sun 6 degrees up at azimuth 150
SAND = dict(material='pbr', texture='aerial_beach_01', tex_scale=2.6, tint='#B9592A', tint_mix=0.8, res='4k',
            rough_mul=1.0, bump=1.0)
ROCK = dict(material='pbr', texture='cliff_side', tex_scale=8.0, tint='#7A3A22', tint_mix=0.4, res='2k', vary=[30.0, 0.45])
CAM = dict(height=0.78, distance=6.0, azimuth=-20.0, lens=50.0, target=(0.0, 0.0, 0.66), fstop=4.0, shift_x=0.1)


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


def plateau(dist, ang, radius, height, seed, squash=0.55, cliff=0.4, wander=0.22):
    x, y = at(dist, ang)
    return piece('ext', module='dust_el', fn='mesa', position=[x, y, -0.5], radius=radius, height=height, seed=seed,
                 squash=squash, cliff=cliff, wander=wander, **ROCK)


def props():
    ex, ey = _eye(CAM)
    tx, ty, _ = CAM['target']
    heading = math.degrees(math.atan2(ty - ey, tx - ex))
    out = [piece('ext', module='dust_el', fn='terrain', eye=[round(ex, 3), round(ey, 3)], heading=round(heading, 2),
                 half_angle=42.0, r0=1.2, r1=292.0, segments=460, flat=[0.0, 0.0, 2.2], swell=0.6, swell_size=16.0,
                 rim=1.6, vary=[14.0, 0.55], dual=[1.55, 27.0, 9.0], **SAND),
           # under everything, out of the camera's sight: ground for the light to bounce off on every side
           piece('box', size=[700.0, 700.0, 0.1], position=[0.0, 0.0, -0.45], **SAND)]
    # the plateaus: a broad mesa to the right, a slim butte and a long low mesa to the left, one more far off
    out += [plateau(250, 15, 34, 24, 1, squash=0.45),
            plateau(215, -15, 7, 22, 2, squash=0.9, cliff=0.45),
            plateau(285, -27, 40, 14, 3, squash=0.35),
            plateau(280, 0, 26, 9, 4, squash=0.4, cliff=0.5)]
    # the tumbleweed, come to rest against a ripple to the speaker's right, and the dust it kicked up
    out += [piece('ext', module='dust_el', fn='tumbleweed', diameter=0.62, seed=11, position=[1.35, 1.1, 0.2], stems=46, branches=8, twigs=6,
                  rotate=[8, 14, 30], color='#B6976F'),
            piece('ext', module='dust_el', fn='dust', size=[3.2, 1.6, 0.9], position=[2.6, 1.6, -0.02], density=0.8,
                  wisp=0.5, color='#E9BC94'),
            # a low sheet of dust blowing across the flat behind, lit from behind by the sun
            piece('ext', module='dust_el', fn='dust', size=[30.0, 14.0, 0.6], position=[6.0, 16.0, -0.05], density=0.5,
                  wisp=1.8, color='#EDC29A')]
    return out


def lights():
    # the sun on the sand in front bounces back into the speaker's face: a photographer's warm reflector, low
    return {'bounce': area(-10, 10, 4.0, 1.2, '#F2B07E', (4.0, 1.5), (0.0, 0.0, 0.55))}


def shot():
    return frame('dust', props(), camera(**CAM), sky(HDRI, ROT, strength=0.5, res='4k'),
                 'barkhorn, Dust, the Southwest at golden hour', lights=lights(),
                 sun=dict(sun_from_sky(HDRI, ROT, irradiance=9.0, angle_deg=0.6), elevation_deg=11.0),
                 fin=finish(contrast=0.05, clarity=0.04, saturation=0.0, vignette=0.12, bloom=0.08, threshold=0.95),
                 haze={'box_m': [-320.0, -30.0, -1.0, 320.0, 320.0, 70.0], 'density': 0.0007, 'anisotropy': 0.35,
                       'color': '#F4D2B0'},
                 rotate_z=0.0, position=(0.0, 0.0, -0.008))


def portrait():
    c = dict(CAM, distance=5.2, lens=55.0)
    return portrait_of(shot(), **camera(**c))
