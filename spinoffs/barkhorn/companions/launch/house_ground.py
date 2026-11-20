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


def build(bpy, s, dim=1.0, lift=0.0, studio=None):
    """The scaled set, sky and lamps. Returns (camera spec scaled, recipe).
    lift (m): the product hung that much higher (Hemisphere hung free, 2026-11-20); the product's lamps and the camera
    move up with it, the sweep and the lamps that light it alone stay. studio: a factor on every studio lamp and the sky
    apart from dim (the LIT frames: the studio taken down, the exposure set for the lamp); default 1/dim."""
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
    k_st = (1.0 / dim) if studio is None else studio
    sky = dict(R['sky']); sky['strength'] = sky['strength'] * k_st
    Lt.world(bpy, sky)
    centre = Vector(_mul(R['tropos_centre'], s))
    pcentre = centre + Vector((0, 0, lift))
    made = []
    solid = os.environ.get('HOUSE_SOLID', '1') == '1'
    for name, sp in R['lights'].items():
        if not (sp.get('irradiance', 0) > 0 or sp.get('power_w', 0) > 0):
            continue
        sp = json.loads(json.dumps(sp))
        if 'orbit' in sp:
            sp['orbit']['distance_m'] *= s
        for k in ('position', 'target'):
            if k in sp:
                sp[k] = _mul(sp[k], s)
                if not sp.get('receivers'):
                    sp[k][2] += lift
        sp['size_m'] = _mul(sp['size_m'], s)
        if 'power_w' in sp:
            sp['power_w'] *= s * s
        ob = Lt.area(bpy, 'house-' + name, sp, centre if sp.get('receivers') else pcentre)
        ob.data.energy *= k_st
        if solid and not sp.get('receivers') and ob.data.specular_factor > 0:
            softbox(bpy, ob, s)
        if sp.get('receivers'):
            # HOUSE_BG: the lamps that light the sweep alone, times one declared factor, so the paper behind a small
            # lamp reads as it does behind the speaker (whose own bounce lifts it); 1 is the recipe as it stands
            ob.data.energy *= float(os.environ.get('HOUSE_BG', '1'))
        if sp.get('receivers'):
            Lt.link_receivers(bpy, ob, [sweep])
        made.append(ob)
    if os.environ.get('HOUSE_ROOM', '1') == '1':
        room(bpy, s)
    cam = json.loads(json.dumps(R['camera']))
    for k in ('position', 'target', 'focus'):
        cam[k] = _mul(cam[k], s); cam[k][2] += lift
    return cam, R, made


def softbox(bpy, ob, s):
    """A solid softbox for an area lamp's reflection (the coordinator, 2026-11-20: the bare area lamps read as flat
    rectangles with razor edges whose overlaps add). The lamp keeps lighting the scene but is no longer seen in
    reflections; in its place a face of the same size and mean radiance, brightest at its middle and falling to about a
    third at its edges (a diffuser's hot centre), in a black housing a little larger: seen only by glossy rays, casting
    no shadow, so a nearer box hides a farther one and the light on the set is unchanged."""
    L = ob.data; w, h = L.size, L.size_y
    rad = L.energy * L.specular_factor / (math.pi * w * h)            # an area lamp's radiance, P / (pi A)
    L.specular_factor = 0.0
    def plane(nm, ww, hh, dz):
        me = bpy.data.meshes.new(nm)
        me.from_pydata([(-ww / 2, -hh / 2, dz), (-ww / 2, hh / 2, dz), (ww / 2, hh / 2, dz), (ww / 2, -hh / 2, dz)], [], [(0, 1, 2, 3)])
        me.uv_layers.new(); o = bpy.data.objects.new(nm, me); bpy.context.scene.collection.objects.link(o)
        o.parent = ob; o.matrix_parent_inverse.identity()
        o.visible_camera = o.visible_diffuse = o.visible_shadow = o.visible_volume_scatter = False
        o.visible_glossy = o.visible_transmission = True
        return o
    face = plane(ob.name + '-face', w, h, 0.0)
    m = bpy.data.materials.new(ob.name + '-face'); m.use_nodes = True; nt = m.node_tree; nt.nodes.clear()
    em = nt.nodes.new('ShaderNodeEmission'); tc = nt.nodes.new('ShaderNodeTexCoord'); sep = nt.nodes.new('ShaderNodeSeparateXYZ')
    nt.links.new(tc.outputs['UV'], sep.inputs[0])
    def fall(ch):               # 1 - 0.65 (2u - 1)^2: 1 at the middle, 0.35 at the edge; its mean 0.783
        a = nt.nodes.new('ShaderNodeMath'); a.operation = 'MULTIPLY_ADD'; a.inputs[1].default_value = 2.0; a.inputs[2].default_value = -1.0
        nt.links.new(sep.outputs[ch], a.inputs[0])
        q = nt.nodes.new('ShaderNodeMath'); q.operation = 'POWER'; q.inputs[1].default_value = 2.0; nt.links.new(a.outputs[0], q.inputs[0])
        f = nt.nodes.new('ShaderNodeMath'); f.operation = 'MULTIPLY_ADD'; f.inputs[1].default_value = -0.65; f.inputs[2].default_value = 1.0
        nt.links.new(q.outputs[0], f.inputs[0]); return f
    fx, fy = fall('X'), fall('Y')
    pr = nt.nodes.new('ShaderNodeMath'); pr.operation = 'MULTIPLY'; nt.links.new(fx.outputs[0], pr.inputs[0]); nt.links.new(fy.outputs[0], pr.inputs[1])
    st = nt.nodes.new('ShaderNodeMath'); st.operation = 'MULTIPLY'; st.inputs[1].default_value = rad / (0.7833 ** 2)
    nt.links.new(pr.outputs[0], st.inputs[0]); nt.links.new(st.outputs[0], em.inputs['Strength'])
    em.inputs['Color'].default_value = (*L.color, 1)
    nt.links.new(em.outputs[0], nt.nodes.new('ShaderNodeOutputMaterial').inputs['Surface'])
    face.data.materials.append(m)
    hous = plane(ob.name + '-housing', w * 1.12, h * 1.12, 0.004 * s / 0.2)        # behind the face (a lamp faces -z)
    hm = bpy.data.materials.new('softbox-housing'); hm.use_nodes = True
    hb = hm.node_tree.nodes['Principled BSDF']; hb.inputs['Base Color'].default_value = (0.01, 0.01, 0.01, 1); hb.inputs['Roughness'].default_value = 0.6
    hous.data.materials.append(hm)


def room(bpy, s):
    """The studio's walls and ceiling, seen only in reflections (the coordinator, 2026-11-20: surfaces facing away from
    the lights read pure black; a satin black part in a white studio is charcoal). White walls left, right and behind the
    sweep's top, a white ceiling, a mid-grey wall behind the camera; lit by the studio's lamps, they light nothing on the
    set (glossy rays only, no shadow), so the ground is as measured. Full-size room 9 x 9 x 5 m, times s."""
    def wall(nm, verts, col):
        me = bpy.data.meshes.new(nm); me.from_pydata([tuple(c * s for c in v) for v in verts], [], [(0, 1, 2, 3)])
        o = bpy.data.objects.new(nm, me); bpy.context.scene.collection.objects.link(o)
        o.visible_camera = o.visible_diffuse = o.visible_shadow = o.visible_volume_scatter = False
        o.visible_glossy = True; o.visible_transmission = False
        m = bpy.data.materials.new(nm); m.use_nodes = True; b = m.node_tree.nodes['Principled BSDF']
        b.inputs['Base Color'].default_value = (col, col, col * 0.97, 1); b.inputs['Roughness'].default_value = 1.0
        b.inputs['Specular IOR Level'].default_value = 0.0
        o.data.materials.append(m)
    X, Yf, Yb, Z = 4.5, -4.5, 4.5, 5.0
    wall('room-left', [(-X, Yf, 0), (-X, Yb, 0), (-X, Yb, Z), (-X, Yf, Z)], 0.8)
    wall('room-right', [(X, Yf, 0), (X, Yf, Z), (X, Yb, Z), (X, Yb, 0)], 0.8)
    wall('room-back', [(-X, Yb, 0), (X, Yb, 0), (X, Yb, Z), (-X, Yb, Z)], 0.8)
    wall('room-ceiling', [(-X, Yf, Z), (-X, Yb, Z), (X, Yb, Z), (X, Yf, Z)], 0.8)
    wall('room-front', [(-X, Yf, 0), (-X, Yf, Z), (X, Yf, Z), (X, Yf, 0)], 0.25)


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
