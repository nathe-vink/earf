"""The night pictures (the coordinator, 2026-11-03 23:04): Tropos at night, lit only by the room's own lights.

The speaker is built by the speaker lane's own engine, unchanged (r33-speaker-horn: studio/engine/render.py, its
products, tints, the polished horn and base A). This wrapper swaps the engine's set builder for an evening room and
puts EARF's own lamps in it as the practicals, appended from lamp_export.py's .blend files: the lamps lane's own parts,
acrylic and lights (r32-lamps-final, lamp_pictures.py). Nothing else lights the frame:
- no studio lamp: the shot's `lights` is empty and its sky is black (`kind: none`); the room is closed, so no ambient;
- one dim evening window at most: a curtain lit from behind, an emitting plane (the lamps lane's dusk curtain);
- rulings 1-3: no specular multiplier, no light or shadow linking, nothing hidden from any ray through the resin.
  Each lamp keeps exactly the visibility its own rig gives it (lamp_export.py's object list).

    python3.11 spinoffs/barkhorn/night-pictures/night_room.py ENGINE_ROOT SHOT.json --out OUT.png [--samples N --scale S]
        ENGINE_ROOT: a checkout of r33-speaker-horn (its two render models built, HELPERS.md step 3)
        SHOT.json: a shot with `set: {kind: sweep, night: {...}}`, `lights: {}` and `sky: {kind: none}`; the `night`
        block places the room, the window and the lamps (see `night_set`)

Runs on python3.11 (bpy 5.0).
"""
import json
import math
import os
import sys

NIGHT = None


def _mesh(bpy, name, verts, faces, mat):
    me = bpy.data.meshes.new(name); me.from_pydata(verts, [], faces); me.update()
    ob = bpy.data.objects.new(name, me); bpy.context.scene.collection.objects.link(ob)
    if mat:
        me.materials.append(mat)
    return ob


def _box(bpy, name, c, s, mat):
    x0, y0, z0 = c[0] - s[0] / 2, c[1] - s[1] / 2, c[2] - s[2] / 2
    x1, y1, z1 = x0 + s[0], y0 + s[1], z0 + s[2]
    v = [(x0, y0, z0), (x1, y0, z0), (x1, y1, z0), (x0, y1, z0), (x0, y0, z1), (x1, y0, z1), (x1, y1, z1), (x0, y1, z1)]
    f = [(0, 3, 2, 1), (4, 5, 6, 7), (0, 1, 5, 4), (1, 2, 6, 5), (2, 3, 7, 6), (3, 0, 4, 7)]
    return _mesh(bpy, name, v, f, mat)


def _principled(bpy, name, hexc, rough, spec=0.5):
    m = bpy.data.materials.new(name); m.use_nodes = True
    b = m.node_tree.nodes['Principled BSDF']
    h = hexc.lstrip('#'); rgb = [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    lin = [c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4 for c in rgb]
    b.inputs['Base Color'].default_value = (*lin, 1); b.inputs['Roughness'].default_value = rough
    b.inputs['Specular IOR Level'].default_value = spec
    return m


def _curtain(bpy, nb, hexc, strength, loc, size, target):
    """The lamps lane's dusk curtain (lamp_pictures.py, round 12): a curtain over a window, lit from behind by the
    evening sky; an emitting plane, brightest at its middle and feathered to its edges, so it reads as cloth lit
    through, not a panel. A real surface: every ray sees it."""
    from mathutils import Vector
    m = bpy.data.materials.new('dusk-curtain'); m.use_nodes = True
    nt = m.node_tree; nt.nodes.clear()
    o = nt.nodes.new('ShaderNodeOutputMaterial'); em = nt.nodes.new('ShaderNodeEmission')
    h = hexc.lstrip('#'); rgb = [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    em.inputs['Color'].default_value = (*[c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4 for c in rgb], 1)
    tc = nt.nodes.new('ShaderNodeTexCoord'); gr = nt.nodes.new('ShaderNodeTexGradient'); gr.gradient_type = 'QUADRATIC_SPHERE'
    pw = nt.nodes.new('ShaderNodeMath'); pw.operation = 'POWER'; pw.inputs[1].default_value = 1.5
    mu = nt.nodes.new('ShaderNodeMath'); mu.operation = 'MULTIPLY'; mu.inputs[1].default_value = strength
    nt.links.new(tc.outputs['Object'], gr.inputs['Vector']); nt.links.new(gr.outputs['Fac'], pw.inputs[0])
    nt.links.new(pw.outputs[0], mu.inputs[0]); nt.links.new(mu.outputs[0], em.inputs['Strength'])
    nt.links.new(em.outputs[0], o.inputs['Surface'])
    ob = _mesh(bpy, 'dusk-curtain', [(-1, -1, 0), (1, -1, 0), (1, 1, 0), (-1, 1, 0)], [(0, 1, 2, 3)], m)
    ob.location = loc; ob.scale = (size[0] / 2, size[1] / 2, 1)
    ob.rotation_euler = (Vector(target) - Vector(loc)).to_track_quat('Z', 'Y').to_euler()
    return ob


# what lamp_export.py's scenes hold that is the lamps lane's room or rig, not the lamp: left behind
_ROOM = ('wall', 'floor', 'table', 'leg', 'ceiling', 'fill', 'kicker', 'dusk', 'bowl', 'camera', 'sun', 'side-back', 'curtain')


def _append_lamp(bpy, blend, offset, keep_table=False, led_up=False):
    with bpy.data.libraries.load(blend, link=False) as (src, dst):
        dst.objects = list(src.objects)
    got = []
    for o in dst.objects:
        if o is None:
            continue
        low = o.name.lower()
        is_room = any(low.startswith(r) or low == r for r in _ROOM)
        if o.type == 'CAMERA' or (is_room and not (keep_table and (low.startswith('table') or low.startswith('leg')))):
            continue
        bpy.context.scene.collection.objects.link(o)
        if o.parent is None:
            o.location = (o.location[0] + offset[0], o.location[1] + offset[1], o.location[2] + offset[2])
        if led_up and o.type == 'LIGHT' and o.data.type == 'SPOT' and o.name.startswith('led'):
            # the Core's LED shines up through the dock's window into the ball; lamp_pictures.py creates the spot with
            # no rotation, which in Blender points it down (-Z), into the dock (flagged to the coordinator, 2026-11-03)
            o.rotation_euler = (math.pi, 0.0, 0.0)
        got.append(o.name)
    return got


def night_set(bpy, spec, mats):
    """The evening room. spec['night']:
       room: {x0, x1, y_back, y_front, height} (m; the speaker at the origin facing -y),
       floor/wall/ceiling colours, the window {loc, size, target, color, strength},
       lamps: [{blend, offset, keep_table}]."""
    n = spec['night']
    r = n['room']
    x0, x1, yb, yf, h = r['x0'], r['x1'], r['y_back'], r['y_front'], r['height']
    import assets as PH
    try:
        wall_m = PH.pbr(bpy, 'beige_wall_001', '2k', bump=0.25, name='plaster')
    except Exception as e:                       # the cache or the network: a plain plaster, said in the log
        print('night_room: plaster texture unavailable, plain colour:', e, flush=True)
        wall_m = _principled(bpy, 'plaster', n.get('wall', '#CFC8BC'), 0.85, 0.3)
    try:
        floor_m = PH.pbr(bpy, n.get('floor_pbr', 'american_walnut_veneer'), '2k', rough_mul=n.get('floor_rough_mul', 0.9), name='floor')
    except Exception as e:
        print('night_room: floor texture unavailable, plain colour:', e, flush=True)
        floor_m = _principled(bpy, 'floor', n.get('floor', '#3A3029'), 0.45)
    ceil_m = _principled(bpy, 'ceiling', n.get('ceiling', '#E8E4DC'), 0.9, 0.2)
    t = 0.05
    _box(bpy, 'night-floor', ((x0 + x1) / 2, (yb + yf) / 2, -t / 2), (x1 - x0 + 2 * t, yb - yf + 2 * t, t), floor_m)
    _box(bpy, 'night-ceiling', ((x0 + x1) / 2, (yb + yf) / 2, h + t / 2), (x1 - x0 + 2 * t, yb - yf + 2 * t, t), ceil_m)
    _box(bpy, 'night-wall-back', ((x0 + x1) / 2, yb + t / 2, h / 2), (x1 - x0 + 2 * t, t, h), wall_m)
    op = n.get('opening')
    if op:
        # ruling 4 (the coordinator, 23:43): light reaches the room only through a real opening. The left wall is
        # built round a window (y0..y1, z0..z1); outside it the evening sky, an emitting plane; in it a sheer curtain
        oy0, oy1, oz0, oz1 = op['y0'], op['y1'], op['z0'], op['z1']
        _box(bpy, 'night-wall-left-front', (x0 - t / 2, (oy0 + yf) / 2, h / 2), (t, oy0 - yf, h), wall_m)
        _box(bpy, 'night-wall-left-back', (x0 - t / 2, (yb + oy1) / 2, h / 2), (t, yb - oy1, h), wall_m)
        _box(bpy, 'night-wall-left-sill', (x0 - t / 2, (oy0 + oy1) / 2, oz0 / 2), (t, oy1 - oy0, oz0), wall_m)
        _box(bpy, 'night-wall-left-head', (x0 - t / 2, (oy0 + oy1) / 2, (h + oz1) / 2), (t, oy1 - oy0, h - oz1), wall_m)
        # the evening sky outside: an emitting plane facing the window, a little larger than it, 0.6 m out
        sky = bpy.data.materials.new('evening-sky'); sky.use_nodes = True
        snt = sky.node_tree; snt.nodes.clear()
        so = snt.nodes.new('ShaderNodeOutputMaterial'); se = snt.nodes.new('ShaderNodeEmission')
        hx = op.get('sky_color', '#9FB2D6').lstrip('#'); rgb = [int(hx[i:i + 2], 16) / 255 for i in (0, 2, 4)]
        se.inputs['Color'].default_value = (*[c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4 for c in rgb], 1)
        se.inputs['Strength'].default_value = op['sky_strength']
        snt.links.new(se.outputs[0], so.inputs['Surface'])
        sx = x0 - 0.6; m_ = 0.5
        _mesh(bpy, 'evening-sky', [(sx, oy0 - m_, oz0 - m_), (sx, oy1 + m_, oz0 - m_), (sx, oy1 + m_, oz1 + m_), (sx, oy0 - m_, oz1 + m_)],
              [(0, 1, 2, 3)], sky)
        if op.get('curtain', True):
            # a sheer curtain in the opening: a thin cloth that lets the sky through, diffused (translucent), a little
            # straight through (the weave's gaps), its room side a pale fabric
            cm = bpy.data.materials.new('sheer'); cm.use_nodes = True
            cnt = cm.node_tree; cnt.nodes.clear()
            co = cnt.nodes.new('ShaderNodeOutputMaterial'); tl = cnt.nodes.new('ShaderNodeBsdfTranslucent')
            tl.inputs['Color'].default_value = (0.80, 0.80, 0.78, 1)
            df = cnt.nodes.new('ShaderNodeBsdfDiffuse'); df.inputs['Color'].default_value = (0.55, 0.55, 0.53, 1)
            tp = cnt.nodes.new('ShaderNodeBsdfTransparent')
            m1 = cnt.nodes.new('ShaderNodeMixShader'); m1.inputs[0].default_value = 0.35
            cnt.links.new(tl.outputs[0], m1.inputs[1]); cnt.links.new(df.outputs[0], m1.inputs[2])
            m2 = cnt.nodes.new('ShaderNodeMixShader'); m2.inputs[0].default_value = op.get('curtain_open', 0.15)
            cnt.links.new(m1.outputs[0], m2.inputs[1]); cnt.links.new(tp.outputs[0], m2.inputs[2])
            cnt.links.new(m2.outputs[0], co.inputs['Surface'])
            cx_ = x0 + 0.06
            _mesh(bpy, 'sheer-curtain', [(cx_, oy0 - 0.05, oz0 - 0.05), (cx_, oy1 + 0.05, oz0 - 0.05), (cx_, oy1 + 0.05, oz1 + 0.05),
                                          (cx_, oy0 - 0.05, oz1 + 0.05)], [(0, 1, 2, 3)], cm)
    else:
        _box(bpy, 'night-wall-left', (x0 - t / 2, (yb + yf) / 2, h / 2), (t, yb - yf, h), wall_m)
    _box(bpy, 'night-wall-right', (x1 + t / 2, (yb + yf) / 2, h / 2), (t, yb - yf, h), wall_m)
    _box(bpy, 'night-wall-front', ((x0 + x1) / 2, yf - t / 2, h / 2), (x1 - x0 + 2 * t, t, h), wall_m)
    w = n.get('window')
    if w and w.get('strength', 0) > 0:
        _curtain(bpy, None, w.get('color', '#9FB2D6'), w['strength'], w['loc'], w['size'], w['target'])
    for f in n.get('furniture', []):
        _box(bpy, f['name'], f['center'], f['size'], _principled(bpy, f['name'], f['color'], f.get('rough', 0.5)))
    for L in n.get('lamps', []):
        got = _append_lamp(bpy, L['blend'], L['offset'], L.get('keep_table', False), L.get('led_up', False))
        print('night_room: lamp', os.path.basename(L['blend']), 'objects:', ', '.join(sorted(got)), flush=True)


def main():
    root = os.path.abspath(sys.argv[1])
    eng = os.path.join(root, 'studio', 'engine')
    sys.path.insert(0, eng)
    os.chdir(root)
    import bpy  # noqa: F401  (bmesh, which the engine's modules import, loads only after bpy)
    import sets as St
    St.sweep = night_set                      # the engine's set builder for kind 'sweep': the evening room instead
    import render as R
    args = sys.argv[2:]
    blend = None
    if '--save-blend' in args:
        # the scene as it will render, saved first for scene_audit.py (the coordinator's card and rig checks)
        i = args.index('--save-blend'); blend = os.path.abspath(args[i + 1]); del args[i:i + 2]
        real_ops = bpy.ops

        class _Render:
            def __getattr__(self, n):
                if n != 'render':
                    return getattr(real_ops.render, n)

                def render(*a, **k):
                    real_ops.wm.save_as_mainfile(filepath=blend, copy=True)
                    return real_ops.render.render(*a, **k)
                return render

        class _Ops:
            def __getattr__(self, n):
                return _Render() if n == 'render' else getattr(real_ops, n)
        bpy.ops = _Ops()
    sys.argv = [os.path.join(eng, 'render.py')] + args
    R.main()


if __name__ == '__main__':
    main()
