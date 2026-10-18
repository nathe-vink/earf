"""Round 31b: the speakers in their element, on location at real scale and photographed as a campaign would be
(BRIEF.md is the direction). What every set shares: the shot (the speaker in its flavour, standing in a set built from
photographed assets under a photographed sky), a real camera at eye level, a sun lamp matched to the sky's own sun, a
photographic finish, and the two frames (landscape 2400 x 1600, portrait 1600 x 2000).

Each colour's set is a module beside this one (ember.py, dust.py, acid.py, poison.py, ice.py, haze.py, fog.py, smoke.py;
a second concept for a colour is <name>_b.py), with `shot()` returning its landscape frame and `portrait()` its 4:5 frame;
build.py writes them to studio/shots/barkhorn/element31/. The pieces are kit pieces (studio/engine/kit.py), above all
its photographic ones (studio/engine/assets.py: Poly Haven's environments, textures and scanned models, fetched and
cached); anything else a set needs is a kit_ext module of its own.
"""
import copy, json, math, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
BARK = os.path.dirname(HERE)
ROOT = os.path.dirname(os.path.dirname(BARK))
sys.path.insert(0, os.path.join(ROOT, 'studio', 'engine'))
import assets                                             # noqa: E402

OUT = os.path.join(ROOT, 'studio', 'shots', 'barkhorn', 'element31')
RENDERS = os.path.join(ROOT, 'renders', '2026-10-18', 'barkhorn', 'element31')
BASE = os.path.join(ROOT, 'studio', 'shots', 'barkhorn', 'lookbook21', 'look-amber-on.json')
# the colours: module name -> (the speaker's key, its flavour in studio/products/barkhorn-cloud.json, its name)
COLOURS = {'ember': ('red', 'cloud-red', 'Ember'), 'dust': ('orange', 'cloud-orange', 'Dust'),
           'acid': ('amber', 'cloud-amber', 'Acid'), 'poison': ('green', 'eucalyptus-y2k-green', 'Poison'),
           'ice': ('blue', 'cloud-blue', 'Ice'), 'haze': ('violet', 'cloud-violet', 'Haze'),
           'fog': ('ice', 'birch-fog-clear', 'Fog'), 'smoke': ('black', 'cloud-black', 'Smoke')}
SPEAKER_H = 1.293                                         # its height (m); its front faces -y, its feet stand at z 0
FOOTPRINT = 0.42                                          # half its diagonal at the feet (m): keep props outside this
LANDSCAPE, PORTRAIT = (2400, 1600), (1600, 2000)


# --- pieces ------------------------------------------------------------------------------------------------------
def piece(shape, **k):
    """A kit piece (studio/engine/kit.py documents every shape and material)."""
    return {'kind': 'kit', 'shape': shape, **k}


def ground(texture, size=(30.0, 30.0), position=(0.0, 0.0, 0.0), displace=0.02, relief=None, res='2k', **k):
    """A patch of real ground: a Poly Haven texture at its real size, displaced by its height map, level under the
    speaker. Make it big enough to meet the sky's horizon behind (or hide the edge in haze, terrain or the frame)."""
    return piece('ground', texture=texture, size=list(size), position=list(position), displace=displace, relief=relief,
                 res=res, **k)


def asset(model, position, rotate=(0.0, 0.0, 0.0), scale=1.0, res='2k'):
    """A scanned model (Poly Haven id), placed, turned (degrees) and scaled; its own materials come with it."""
    return piece('asset', model=model, position=list(position), rotate=list(rotate), scale=scale, res=res)


def scatter(models, count, area, avoid=((0.0, 0.0, 0.9),), scale=(0.8, 1.2), seed=1, res='1k', **k):
    """Many copies of scanned models over an area [x0, y0, x1, y1], clear of the speaker (its footprint by default)."""
    return piece('scatter_assets', models=list(models), count=count, area=list(area), avoid=[list(a) for a in avoid],
                 scale=list(scale), seed=seed, res=res, **k)


# --- camera, light, finish ------------------------------------------------------------------------------------------
def camera(height=1.0, distance=5.5, azimuth=-15.0, lens=50.0, target=(0.0, 0.0, 0.66), focus=None, fstop=4.0,
           level=True, shift_x=0.0, shift_y=0.0, roll=0.0):
    """A real camera at eye level: its lens `height` metres up, `distance` metres (on the ground) from `target`, from
    `azimuth` degrees (0 straight on from the front, negative from the speaker's left), a `lens` mm lens at f/`fstop`
    focused on `focus` (default the speaker's front face). `level` keeps verticals vertical by lens shift, as a
    photographer with a shift lens would; shift_x/shift_y move the frame after that (composition, room for type)."""
    az = math.radians(azimuth)
    tx, ty, tz = target
    pos = [tx + distance * math.sin(az), ty - distance * math.cos(az), height]
    f = list(focus) if focus else [tx, ty - 0.21, tz]
    cam = {'position': [round(v, 4) for v in pos], 'target': [round(v, 4) for v in target], 'lens_mm': lens,
           'level': level, 'fstop': fstop, 'focus': [round(v, 4) for v in f]}
    if shift_x or shift_y:
        cam['shift_x'], cam['shift_y'] = shift_x, shift_y
    if roll:
        cam['roll_deg'] = roll
    return cam


def sky(polyhaven, rotation_deg=0.0, strength=1.0, res='4k', visible=True, backdrop=None):
    """A photographed sky (a Poly Haven environment id), turned about the vertical and scaled in strength. At 4k it can
    stand behind the set in a frame's soft background; at 8k it holds up sharper (heavier)."""
    s = {'kind': 'hdri', 'polyhaven': polyhaven, 'rotation_deg': rotation_deg, 'strength': strength, 'res': res}
    if not visible:
        s['visible'] = False
        s['backdrop'] = backdrop or '#808080'
    return s


def sun_from_sky(polyhaven, rotation_deg=0.0, irradiance=4.0, angle_deg=0.53, color=None):
    """A sun lamp where the sky's own sun is (measured from the map: assets.hdri_sun), so shadows, highlights and the
    sky agree. The map's sun lights the set already; this lamp sharpens its shadows and highlights, so keep it modest
    and check the two agree (one shadow, not two)."""
    s = assets.hdri_sun(polyhaven, rotation_deg)
    return {'azimuth_deg': s['azimuth_deg'], 'elevation_deg': max(0.5, s['elevation_deg']), 'irradiance': irradiance,
            'angle_deg': angle_deg, 'color': color or s['color']}


def area(azimuth, elevation, distance, irradiance, color='#FFFFFF', size=(2.0, 2.0), target=(0.0, 0.0, 0.7)):
    """An area lamp on an orbit round the speaker: on location, a reflector or a bounce a photographer would bring,
    never a studio key. Keep it motivated by the scene's light, and soft."""
    return {'type': 'area', 'size_m': list(size), 'orbit': {'azimuth_deg': azimuth, 'elevation_deg': elevation, 'distance_m': distance},
            'target': list(target), 'irradiance': irradiance, 'color': color}


def point(position, power_w, color='#FFB070', radius=0.05):
    """A practical light in the scene (a lava vent, a lantern, a window), placed where its source is."""
    return {'type': 'point', 'position': list(position), 'power_w': power_w, 'color': color, 'radius_m': radius}


def spot(position, target, power_w, cone=30.0, blend=0.4, color='#FFFFFF', radius=0.05):
    return {'type': 'spot', 'position': list(position), 'target': list(target), 'power_w': power_w, 'cone_deg': cone,
            'blend': blend, 'color': color, 'radius_m': radius}


def finish(contrast=0.05, clarity=0.04, sharpen=0.25, saturation=0.0, bloom=0.0, bloom_px=30, threshold=0.92,
           lift=0.0, lift_color='#000000', vignette=0.12):
    """A photographic post (studio/engine/finish.py): restrained, one grade over the whole frame, so the speaker and
    its setting sit in the same light. Bloom only where something truly glows (lava, a low sun); no dreamy lift."""
    f = {'enabled': True, 'white_in': 240, 'white_out': 240, 'contrast': contrast, 'clarity': clarity,
         'sharpen': sharpen, 'sharpen_px': 0.6}
    if bloom or saturation or lift or vignette:
        f['dream'] = {'bloom': bloom, 'bloom_px': bloom_px, 'bloom_threshold': threshold, 'saturation': saturation,
                      'lift': lift, 'lift_color': lift_color, 'vignette': vignette}
    return f


def shot(name, props, camera, sky, title, lights=None, sun=None, size=LANDSCAPE, samples=512, fin=None, haze=None,
         rotate_z=15.0, position=(0.0, 0.0, 0.0), view='AgX', look='AgX - Base Contrast', exposure=0.0, cover=False,
         clamp=10.0):
    """A frame: the speaker in `name`'s colour at `position`, turned `rotate_z` degrees (positive turns its front
    toward +x), cover off unless `cover`, standing in `props` (kit pieces), under `sky`, lit by the sky, `sun` and
    `lights`, seen by `camera`."""
    key, flavour, _ = COLOURS[name.split('_')[0]]
    s = copy.deepcopy(json.load(open(BASE)))
    inst = {'flavour': flavour, 'position': list(position), 'rotate_z': rotate_z}
    if not cover:
        inst['hide'] = ['cloth-disc']
    s['product'] = {'def': 'studio/products/barkhorn-cloud.json', 'flavour': flavour, 'instances': [inst]}
    s['set'] = {'kind': 'stage', 'props': props}
    s['lights'] = lights or {}
    if sun:
        s['sun'] = sun
    else:
        s.pop('sun', None)
    s['camera'] = camera
    s['size'] = list(size)
    s['title'] = title
    s['sky'] = sky
    s['render'] = {**s['render'], 'samples': samples, 'exposure': exposure, 'clamp': clamp, 'view': view}
    if look:
        s['render']['look'] = look
    s['finish'] = fin or finish()
    s.pop('haze', None)
    if haze:
        s['haze'] = haze
    return s


def portrait_of(landscape, **camera):
    """The 4:5 frame of a landscape shot: the same set, light and finish, the camera changed by `camera`'s keys."""
    s = copy.deepcopy(landscape)
    s['size'] = list(PORTRAIT)
    s['camera'].update(camera)
    s['title'] = s['title'] + ' (4:5)'
    return s
