"""The house ground for the lamps (2026-11-20, the coordinator: Hemisphere and Core on the same light ground as the eight
Tropos fronts, off and on).

The recipe is the Tropos fronts' own (house-ground.json, copied verbatim from the speaker lane's shot): the warm white
sweep #F7F0E8 with its contact shading, the gradient sky at 0.15, every lamp of theirs with a light in it (key from
camera left at 40 degrees up, fill, kick, the big front softbox `horn`, and the four lamps linked to the sweep alone that
shape its tone), the camera, Khronos PBR Neutral, and their finish. A lamp is a fifth to a sixth of a speaker's size, so
the whole set is built at a scale s: every length (sweep, lamp positions, orbits, sizes, targets, camera) times s,
every irradiance unchanged (an area lamp's watts follow irradiance x pi x d^2, so at a fifth of the distance it puts
the same light on the subject). The camera's view of the set is then the Tropos frame's, and only the product differs.

Left out on purpose: the Tropos set's black flags and its white bounce card (cards for a speaker's gloss; out of frame,
and none is needed by a lamp), and the lamps at zero light (back, pool, edge, rim, paper, wall, wash, floor, through).

ON frames: every studio lamp and the sky divided by one declared factor DIM, the exposure raised by log2(DIM), so the
ground reads as in the OFF frame and the lamp's own light, at its real output, is what changed.
"""
import json, math, os, sys

from mathutils import Vector

HERE = os.path.dirname(os.path.abspath(__file__))
ENGINE = os.path.join(HERE, '..', '..', '..', '..', 'studio', 'engine')


def recipe():
    return json.load(open(os.path.join(HERE, 'house-ground.json')))


def _mul(v, s):
    return [x * s for x in v]


def build(bpy, s, dim=1.0):
    """The scaled set, sky and lamps. Returns (camera spec scaled, recipe)."""
    sys.path.insert(0, os.path.abspath(ENGINE))
    import sets as St, lights as Lt
    R = recipe()
    st = dict(R['set'])
    for k in ('width', 'front', 'depth', 'radius', 'height'):
        st[k] = st[k] * s
    ct = dict(st.get('contact') or {})
    for k in ('distance_m', 'core_distance_m'):
        if k in ct:
            ct[k] = ct[k] * s
    st['contact'] = ct
    st['flags'] = []; st['bounces'] = []
    sweep = St.sweep(bpy, st, {})[0]
    sky = dict(R['sky']); sky['strength'] = sky['strength'] / dim
    Lt.world(bpy, sky)
    centre = Vector(_mul(R['tropos_centre'], s))
    made = []
    for name, sp in R['lights'].items():
        if not (sp.get('irradiance', 0) > 0 or sp.get('power_w', 0) > 0):
            continue
        sp = json.loads(json.dumps(sp))
        if 'orbit' in sp:
            sp['orbit']['distance_m'] *= s
        for k in ('position', 'target'):
            if k in sp:
                sp[k] = _mul(sp[k], s)
        sp['size_m'] = _mul(sp['size_m'], s)
        if 'power_w' in sp:
            sp['power_w'] *= s * s
        ob = Lt.area(bpy, 'house-' + name, sp, centre)
        ob.data.energy /= dim
        if sp.get('receivers'):
            # HOUSE_BG: the lamps that light the sweep alone, times one declared factor, so the paper behind a small
            # lamp reads as it does behind the speaker (whose own bounce lifts it); 1 is the recipe as it stands
            ob.data.energy *= float(os.environ.get('HOUSE_BG', '1'))
        if sp.get('receivers'):
            Lt.link_receivers(bpy, ob, [sweep])
        made.append(ob)
    cam = json.loads(json.dumps(R['camera']))
    for k in ('position', 'target', 'focus'):
        cam[k] = _mul(cam[k], s)
    return cam, R, made


def camera(bpy, sc, cam, W, H, lens=None, fstop_equiv=True, s=1.0):
    """The engine's level camera: horizontal sensor fit, looking level, the lens shifted so the target lands where a
    tilted camera would put it (verticals stay vertical). The depth of field as at full size (f-number / s)."""
    cd = bpy.data.cameras.new('cam'); ob = bpy.data.objects.new('cam', cd); sc.collection.objects.link(ob); sc.camera = ob
    cd.sensor_fit = 'HORIZONTAL'; cd.sensor_width = 36.0; cd.lens = lens or cam['lens_mm']; cd.clip_start = 0.005
    C = Vector(cam['position']); T = Vector(cam['target'])
    d = T - C; flat = Vector((d.x, d.y, 0))
    ob.rotation_euler = flat.to_track_quat('-Z', 'Y').to_euler()
    tilt = math.atan2(d.z, flat.length)
    cd.shift_y = math.tan(tilt) * cd.lens / cd.sensor_width * (1.0 if W >= H else W / H)
    ob.location = C
    cd.shift_x += cam.get('shift_x', 0.0); cd.shift_y += cam.get('shift_y', 0.0)
    if cam.get('fstop', 0) > 0:
        cd.dof.use_dof = True; cd.dof.aperture_fstop = cam['fstop'] / (s if fstop_equiv else 1.0)
        F = Vector(cam.get('focus', cam['target']))
        cd.dof.focus_distance = (F - C).dot((T - C).normalized())
    return ob
