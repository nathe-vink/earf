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


def _scale_base(m, k):
    """Multiplies a material's base colour by k (the engine's pbr tint is a COLOR blend, which keeps the texture's
    lightness: a white fleece stays white; this darkens it as a dyed one would be)."""
    nt = m.node_tree
    bs = next(n for n in nt.nodes if n.type == 'BSDF_PRINCIPLED')
    sock = bs.inputs['Base Color']
    mul = nt.nodes.new('ShaderNodeMix'); mul.data_type = 'RGBA'; mul.blend_type = 'MULTIPLY'
    mul.inputs['Factor'].default_value = 1.0; mul.inputs['B'].default_value = (k, k, k, 1.0)
    if sock.is_linked:
        nt.links.new(sock.links[0].from_socket, mul.inputs['A'])
    else:
        mul.inputs['A'].default_value = sock.default_value
    nt.links.new(mul.outputs['Result'], sock)


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
_ROOM = ('wall', 'floor', 'table', 'leg', 'ceiling', 'fill', 'kicker', 'dusk', 'bowl', 'camera', 'sun', 'side-back', 'curtain',
         'mullion', 'transom', 'sheer')     # the lamps lane's window (26400e7c): its frame, its sheers and its sky lamps


def _append_lamp(bpy, blend, offset, keep_table=False, led_up=False, cord_to=None, canopy=None, honest_cob=None):
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
    if honest_cob:
        # the coordinator, 18:13: the Hemisphere's real emitter, not the lamps lane's 17 cm stand-in disk (lamp_pictures
        # round 6, for a soft bowl shadow). The Vero SE 10's light-emitting surface, a disk of honest_cob metres, at the
        # top of the 46 bore 22 up from its mouth (crystal.py: just under the COB's face, where the CAD's faceted
        # reflector cone ends), emitting a full hemisphere: the bore and the reflector make the 46 deg cut-off, not a
        # spread setting. Its power stays the lamps lane's 3.2 W (0.0065 W a lumen)
        bpy.context.view_layer.update()
        cob = next((bpy.data.objects[n] for n in got if n.startswith('cob') and bpy.data.objects[n].type == 'LIGHT'), None)
        refl = next((bpy.data.objects[n] for n in got if n.startswith('reflector')), None)
        if cob and refl:
            zt = max((refl.matrix_world @ v.co).z for v in refl.data.vertices)
            cob.data.size = honest_cob; cob.data.spread = math.pi
            # the reflector in the CAD's high-reflectance aluminium, not the picture rig's steel (the coordinator, 18:43;
            # the lamps lane's flux check, r32 5c319549: about 78-85 % of the COB's light out of the bore)
            al = bpy.data.materials.new('reflector-aluminium'); al.use_nodes = True
            bs = al.node_tree.nodes['Principled BSDF']
            bs.inputs['Base Color'].default_value = (0.888, 0.888, 0.871, 1.0)    # #F2F2F0, linear
            bs.inputs['Metallic'].default_value = 1.0; bs.inputs['Roughness'].default_value = 0.12
            refl.data.materials.clear(); refl.data.materials.append(al)
            cob.location = (cob.location[0], cob.location[1], zt - 0.0005)
            print(f'night_room: the COB a {honest_cob * 1000:.0f} mm disk at z {zt - 0.0005:.4f} (the bore\'s top), '
                  f'{cob.data.energy:.2f} W, spread 180 deg', flush=True)
    if cord_to is not None:
        # a pendant's cord is cut to the room (the lamps lane's CAD gives one length): its mesh stretched along z
        # from its bottom so its top meets the ceiling
        c = next((bpy.data.objects[n] for n in got if n.startswith('cord')), None)
        bpy.context.view_layer.update()        # the offsets above are not in matrix_world until the view layer updates
        if c is not None:
            from mathutils import Vector
            Mw = c.matrix_world; Mi = Mw.inverted()
            zs = [(Mw @ v.co).z for v in c.data.vertices]
            z0, z1 = min(zs), max(zs)
            k = (cord_to - z0) / (z1 - z0)
            for v in c.data.vertices:
                w = Mw @ v.co; w.z = z0 + (w.z - z0) * k; v.co = Mi @ w
            c.data.update()
            if canopy:
                # the pendant's own ceiling canopy (the lamps lane's CAD: out-dome-pendant/stl/canopy.stl, which their
                # picture rig leaves out), centred on the cord at the ceiling, in the cap's matte finish
                bpy.ops.wm.stl_import(filepath=canopy, global_scale=0.001)     # the CAD's millimetres, as the lamps lane imports it
                cn = bpy.context.selected_objects[0]; cn.name = 'canopy'
                bpy.context.view_layer.update()
                cz = [(cn.matrix_world @ v.co).z for v in cn.data.vertices]
                cx_ = sum((cn.matrix_world @ v.co).x for v in cn.data.vertices) / len(cn.data.vertices)
                cy_ = sum((cn.matrix_world @ v.co).y for v in cn.data.vertices) / len(cn.data.vertices)
                cords = [Mw @ v.co for v in c.data.vertices]
                ccx = sum(w.x for w in cords) / len(cords); ccy = sum(w.y for w in cords) / len(cords)
                cn.location = (cn.location[0] + ccx - cx_, cn.location[1] + ccy - cy_, cn.location[2] + cord_to - max(cz))
                cap = next((m for m in bpy.data.materials if m.name.startswith('cap-matte')), None)
                if cap:
                    cn.data.materials.clear(); cn.data.materials.append(cap)
                got.append('canopy')
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
        if n.get('wall_plain'):
            raise RuntimeError('a plain wall asked for')
        wall_m = PH.pbr(bpy, n.get('wall_pbr', 'beige_wall_001'), '2k', bump=0.25, name='plaster',
                        tint=n.get('wall_tint'), tint_mix=n.get('wall_tint_mix', 0.0))
    except Exception as e:                       # the cache or the network: a plain plaster, said in the log
        print('night_room: plain wall:', e, flush=True)
        wall_m = _principled(bpy, 'plaster', n.get('wall', '#CFC8BC'), 0.88, 0.3)
    try:
        if n.get('floor_plain'):
            raise RuntimeError('a plain floor asked for')
        floor_m = PH.pbr(bpy, n.get('floor_pbr', 'american_walnut_veneer'), '2k', rough_mul=n.get('floor_rough_mul', 0.9), name='floor',
                         tint=n.get('floor_tint'), tint_mix=n.get('floor_tint_mix', 0.0))
    except Exception as e:
        print('night_room: plain floor:', e, flush=True)
        floor_m = _principled(bpy, 'floor', n.get('floor', '#3A3029'), n.get('floor_rough', 0.45))
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
    sk = n.get('skirting')
    if sk:
        # a skirting board along the back and side walls, a dark matte paint (the formats: the pendant's cone meets
        # the wall's foot beside the speaker, inside the lower text zones)
        skm = _principled(bpy, 'skirting', sk.get('color', '#2A2826'), 0.9, 0.2)
        hh, dd = sk.get('height', 0.15), 0.015
        _box(bpy, 'skirting-back', ((x0 + x1) / 2, yb - dd / 2, hh / 2), (x1 - x0, dd, hh), skm)
        _box(bpy, 'skirting-right', (x1 - dd / 2, (yb + yf) / 2, hh / 2), (dd, yb - yf, hh), skm)
    w = n.get('window')
    if w and w.get('strength', 0) > 0:
        _curtain(bpy, None, w.get('color', '#9FB2D6'), w['strength'], w['loc'], w['size'], w['target'])
    for md in n.get('models', []):
        # Poly Haven scans (CC0), fetched and cached by the engine's assets.py: furniture that gives the lamp a reason
        try:
            PH.place(bpy, md['id'], md.get('res', '2k'), location=md['location'], rotation_deg=md.get('rotation_deg', (0, 0, 0)),
                     scale=md.get('scale', 1.0), name=md.get('name'))
        except Exception as e:
            print('night_room: model unavailable:', md['id'], e, flush=True)
    rg = n.get('rug')
    if rg:
        # a wool rug with pile (a Poly Haven fabric, its own bump), a bound edge in a darker tape, 12 mm thick
        try:
            rm = PH.pbr(bpy, rg['pbr'], '2k', name='rug', tint=rg.get('tint'), tint_mix=rg.get('tint_mix', 0.0),
                        bump=rg.get('bump', 1.0), scale=rg.get('tile_m'))
        except Exception as e:
            print('night_room: rug texture unavailable, plain:', e, flush=True)
            rm = _principled(bpy, 'rug', rg.get('tint', '#3A3632'), 0.98, 0.1)
        if rg.get('value'):
            _scale_base(rm, rg['value'])
        bw = rg.get('border_w', 0.04); bm_ = _principled(bpy, 'rug-binding', rg.get('border_color', '#1E1C1A'), 0.9, 0.15)
        (cx_, cy_), (sx_, sy_), th = rg['center'], rg['size'], 0.012
        _box(bpy, 'rug', (cx_, cy_, th / 2), (sx_ - 2 * bw, sy_ - 2 * bw, th), rm)
        for nm_, c_, s_ in (('rug-bind-f', (cx_, cy_ - sy_ / 2 + bw / 2), (sx_, bw)), ('rug-bind-b', (cx_, cy_ + sy_ / 2 - bw / 2), (sx_, bw)),
                            ('rug-bind-l', (cx_ - sx_ / 2 + bw / 2, cy_), (bw, sy_ - 2 * bw)), ('rug-bind-r', (cx_ + sx_ / 2 - bw / 2, cy_), (bw, sy_ - 2 * bw))):
            _box(bpy, nm_, (c_[0], c_[1], th / 2 + 0.0005), (s_[0], s_[1], th + 0.001), bm_)
    ol = n.get('outside_light')
    if ol:
        # a light outside the window (a streetlight across the road, far enough to be parallel): it reaches the room
        # only through the opening and the sheer (ruling 4), a soft cool shape on the floor and the wall
        ld = bpy.data.lights.new('outside-light', 'SUN'); ld.energy = ol['irradiance']; ld.angle = math.radians(ol.get('angle_deg', 2.0))
        h = ol.get('color', '#C9D3E6').lstrip('#'); rgb = [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]
        ld.color = [c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4 for c in rgb]
        ob = bpy.data.objects.new('outside-light', ld); bpy.context.scene.collection.objects.link(ob)
        from mathutils import Vector
        ob.rotation_euler = Vector(ol['direction']).normalized().to_track_quat('-Z', 'Y').to_euler()
    for f in n.get('furniture', []):
        _box(bpy, f['name'], f['center'], f['size'], _principled(bpy, f['name'], f['color'], f.get('rough', 0.5)))
    for L in n.get('lamps', []):
        got = _append_lamp(bpy, L['blend'], L['offset'], L.get('keep_table', False), L.get('led_up', False),
                           r['height'] if L.get('cord_to_ceiling') else None, L.get('canopy'), L.get('honest_cob'))
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
