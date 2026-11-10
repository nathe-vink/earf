"""Mantle as signed (Strata Float v3, the owner's pick of 2026-11-01, rebuilt at 71d3163e), by day, the light off
(the coordinator, 2026-11-10 01:06): scene.py's day studio, real out-of-frame lamps and cards only, no emitter of any kind.

    python3.11 v3_day.py OUT.png [--cards] [--hide-cards] -- SCENE.PY ARGS...

--cards (the coordinator's set, 01:06): a black card above and behind the camera (the glassy top mirrors black, so it
reads as tinted glass, not gray) and the 'top' scrim lamp off (it whitened the top). A white card low behind the plinth
cannot stand out of frame from this camera; the sweep is the white surface behind and below. --hide-cards hides the
card from the camera, for gt_audit.py to prove it out of frame (0 px).

Before the render: the two black flags (scene.py hides them from the camera) are made ordinary camera-visible cards (they
stand out of frame, so nothing changes in the picture but their status), and the run stops if any material emits.
The scene is saved beside OUT as .blend (for gt_audit.py) and the linear result as .exr.
"""
import os
import runpy
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
out = sys.argv[1]
mine = sys.argv[2:sys.argv.index('--')]
args = sys.argv[sys.argv.index('--') + 1:]
import bpy
real = bpy.ops


def cards():
    from mathutils import Vector
    sc = bpy.context.scene; cam = sc.camera
    pl = [o for o in bpy.data.objects if o.name.startswith('plinth-L1')]
    pts = [o.matrix_world @ Vector(c) for o in pl for c in o.bound_box]
    lo = Vector((min(p.x for p in pts), min(p.y for p in pts), min(p.z for p in pts)))
    hi = Vector((max(p.x for p in pts), max(p.y for p in pts), max(p.z for p in pts)))
    C = (lo + hi) / 2
    print(f'v3_day: the plinth {tuple(round(v, 3) for v in lo)} to {tuple(round(v, 3) for v in hi)}', flush=True)

    def card(name, w, h, loc, target, col, rough):
        bpy.ops.mesh.primitive_plane_add(size=1.0, location=loc)
        o = bpy.context.active_object; o.name = name; o.scale = (w, h, 1)
        o.rotation_euler = (Vector(target) - Vector(loc)).to_track_quat('Z', 'Y').to_euler()
        m = bpy.data.materials.new(name); m.use_nodes = True; b = m.node_tree.nodes['Principled BSDF']
        b.inputs['Base Color'].default_value = col + (1,); b.inputs['Roughness'].default_value = rough
        o.data.materials.append(m)
        if '--hide-cards' in mine:
            o.visible_camera = False
        return o
    # black: above and a little behind the camera, 1.6 x 1.0 m, black velvet-like (rough, 2 %)
    cl = cam.matrix_world.translation; up = cam.matrix_world.to_3x3() @ Vector((0, 1, 0)); back = cam.matrix_world.to_3x3() @ Vector((0, 0, 1))
    # (the first placement, up 0.45 and back 0.25, crossed the lens's view: gt_audit, 20 % of the frame)
    # (up 0.95 back 0.55 still 6 %): behind the camera's image plane, 0.4 back and 0.35 up in world z, so never in frame
    card('card-black-top', 1.6, 1.0, cl + back * 0.4 + Vector((0, 0, 0.35)), C, (0.02, 0.02, 0.02), 0.95)
    # no white card: from this camera the ground behind and under the plinth is in frame, so a card there is seen
    # (gt_audit: 47 % of the frame). The seamless sweep is the real white surface behind and below; the studio's lamps
    # light it
    t = bpy.data.objects.get('top')
    if t is not None:
        t.hide_render = True
        print('v3_day: the top scrim lamp off', flush=True)


def black_posts():
    # the owner, 2026-11-10: the posts black, the lamps' satin black (companions/common.py: #18181A, roughness 0.5,
    # specular 0.3); in the parts list: 303 stainless, hot black oxide for stainless, satin, oiled
    m = bpy.data.materials.new('post-satin-black'); m.use_nodes = True; b = m.node_tree.nodes['Principled BSDF']
    c = [int('18181A'[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    b.inputs['Base Color'].default_value = tuple(x / 12.92 if x <= 0.04045 else ((x + 0.055) / 1.055) ** 2.4 for x in c) + (1,)
    b.inputs['Roughness'].default_value = 0.5; b.inputs['Specular IOR Level'].default_value = 0.3
    for o in bpy.data.objects:
        if o.name.startswith('post-') and o.type == 'MESH':
            o.data.materials.clear(); o.data.materials.append(m)
            print('v3_day: satin black', o.name, flush=True)


def side_fix():
    # the coordinator, 2026-11-10: the side strip's highlight turned the posts' lit half pale (about 205). Narrowed to
    # 0.03 m and raised to the deck's middle it still reached them (its 50 deg spread: post luma p95 231 in a crop); off,
    # the posts read black (median 14, p95 26). So the side strip is OFF for the set
    o = bpy.data.objects.get('side')
    if o is not None:
        o.hide_render = True
        print('v3_day: side strip off (it lit the posts)', flush=True)


def black_bearing():
    # VARIANT for the owner: the bearing's visible brass (housing, nut, washer) satin black; the parts list stays brass
    m = bpy.data.materials.get('post-satin-black')
    if m is None:
        black_posts(); m = bpy.data.materials['post-satin-black']
    for n in ('bearing-housing', 'bearing-nut', 'bearing-washer'):
        o = bpy.data.objects.get(n)
        if o is not None:
            o.data.materials.clear(); o.data.materials.append(m); print('v3_day: satin black', n, flush=True)


def strip_watts(w):
    # the light on: the LED strip (the drawing's light) emits w watts in all, both faces of its mesh (Cycles' mesh
    # emission is two-sided): radiance = w / (2 pi A)
    obs = [o for o in bpy.data.objects if o.name.startswith('led-strip') and o.type == 'MESH']
    A = sum(p.area for o in obs for p in o.data.polygons) * (obs[0].matrix_world.to_3x3().determinant() ** (2 / 3) if obs else 1)
    for o in obs:
        for sl in o.material_slots:
            for nd in sl.material.node_tree.nodes:
                if nd.type == 'EMISSION':
                    nd.inputs['Strength'].default_value = w / (2 * 3.14159265 * A)
    print(f'v3_day: led-strip {w} W over {A * 1e4:.1f} cm2: radiance {w / (2 * 3.14159265 * max(A, 1e-9)):.1f}', flush=True)


def lamps_off(names):
    for n in names.split(','):
        o = bpy.data.objects.get(n)
        if o is not None and o.type == 'LIGHT':
            o.hide_render = True; print('v3_day: lamp off', n, flush=True)


def backlit(wpm):
    """PROPOSAL (the coordinator, 2026-11-10 05:06): the backlit plinth, on the lamps' principle (colour over white opal,
    lit from behind). The signed plinth's outline, holes, float and posts kept; its 25.4 mm stack becomes, top down:
    6.0 tinted top (thinned from the whole 25.4), 3.0 opal (Perspex GS 041: T 54 %, R 39 %), a 12.0 tray lined white with
    2700 K LED strip runs on its floor at 25 mm pitch, a 4.4 tinted floor. A 10 mm tinted frame closes the edge from the
    floor to the top's underside, its inner face lined white, so no white line shows and no light reaches the edge.
    White-painted sleeves round the bearing (r 15.5 to 22), the arm (28.5 to 35) and the motor (38 to 44) holes; the opal
    and the strips are cut round them. wpm: the strip's watts a metre."""
    from mathutils import Vector
    pl = bpy.data.objects['plinth-L1-stack']
    Z0, Z1 = 0.0687, 0.0941
    zf, zc, zo = Z0 + 0.0044, Z0 + 0.0044 + 0.012, Z0 + 0.0044 + 0.012 + 0.003     # floor top, cavity top, opal top
    X0, X1, Y0, Y1, IN = 0.01, 0.46, 0.01, 0.37, 0.010
    holes = [((0.210, 0.178), 0.0155, 0.022), ((0.405, 0.284), 0.0285, 0.035), ((0.074, 0.303), 0.0380, 0.044)]

    def box(name, x0, x1, y0, y1, z0, z1):
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2))
        b = bpy.context.active_object; b.name = name; b.scale = (x1 - x0, y1 - y0, z1 - z0); bpy.ops.object.transform_apply(scale=True)
        return b

    def cyl(name, c, r, z0, z1):
        bpy.ops.mesh.primitive_cylinder_add(vertices=96, radius=r, depth=z1 - z0, location=(c[0], c[1], (z0 + z1) / 2))
        o = bpy.context.active_object; o.name = name; return o

    def boolean(target, cutter, op):
        m = target.modifiers.new('b', 'BOOLEAN'); m.operation = op; m.object = cutter; m.solver = 'EXACT'
        bpy.context.view_layer.objects.active = target; bpy.ops.object.modifier_apply(modifier=m.name)

    def copy(name):
        o = pl.copy(); o.data = pl.data.copy(); o.name = name; bpy.context.collection.objects.link(o)
        for md in list(o.modifiers):
            o.modifiers.remove(md)
        return o

    def kill(o):
        bpy.data.objects.remove(o, do_unlink=True)

    def mat(name, build):
        m = bpy.data.materials.new(name); m.use_nodes = True; nt = m.node_tree; nt.nodes.clear()
        out = nt.nodes.new('ShaderNodeOutputMaterial'); nt.links.new(build(nt), out.inputs['Surface']); return m

    white = mat('lining-white', lambda nt: (lambda d: (d.inputs['Color'].default_value.__setitem__(slice(0, 4), (0.85, 0.85, 0.85, 1)), d.outputs[0])[1])(nt.nodes.new('ShaderNodeBsdfDiffuse')))

    def opal_bsdf(nt):
        d = nt.nodes.new('ShaderNodeBsdfDiffuse'); d.inputs['Color'].default_value = (0.39, 0.39, 0.39, 1)
        t = nt.nodes.new('ShaderNodeBsdfTranslucent'); t.inputs['Color'].default_value = (0.54, 0.54, 0.54, 1)
        a = nt.nodes.new('ShaderNodeAddShader'); nt.links.new(d.outputs[0], a.inputs[0]); nt.links.new(t.outputs[0], a.inputs[1])
        return a.outputs[0]
    opal = mat('opal-041', opal_bsdf)

    def setmat(o, m):
        o.data.materials.clear(); o.data.materials.append(m)
        for p in o.data.polygons:
            p.material_index = 0
    # the tinted parts: the signed plinth cut by slabs (they keep its materials, holes and outline)
    top = copy('bl-top'); c = box('c', X0 - 0.01, X1 + 0.01, Y0 - 0.01, Y1 + 0.01, zo, Z1 + 0.01); boolean(top, c, 'INTERSECT'); kill(c)
    frame = copy('bl-frame'); c = box('c', X0 - 0.01, X1 + 0.01, Y0 - 0.01, Y1 + 0.01, Z0 - 0.01, zo); boolean(frame, c, 'INTERSECT'); kill(c)
    c = box('c', X0 + IN, X1 - IN, Y0 + IN, Y1 - IN, zf, zo + 0.001); boolean(frame, c, 'DIFFERENCE'); kill(c)
    # the floor stays in the frame above (the frame's cut leaves the floor below zf); the opal over the cavity, cut round sleeves
    op = box('bl-opal', X0 + IN, X1 - IN, Y0 + IN, Y1 - IN, zc, zo)
    for (cc, r0, r1) in holes:
        k = cyl('c', cc, r1, zf - 0.001, zo + 0.001); boolean(op, k, 'DIFFERENCE'); kill(k)
    setmat(op, opal)
    # white linings: the floor's top, the frame's inner walls, the sleeves (painted white outside)
    fl = box('bl-floor-lining', X0 + IN, X1 - IN, Y0 + IN, Y1 - IN, zf, zf + 0.0003)
    for (cc, r0, r1) in holes:
        k = cyl('c', cc, r1, zf - 0.001, zf + 0.001); boolean(fl, k, 'DIFFERENCE'); kill(k)
    setmat(fl, white)
    wl = box('bl-wall-lining', X0 + IN - 0.0003, X1 - IN + 0.0003, Y0 + IN - 0.0003, Y1 - IN + 0.0003, zf, zc)
    k = box('c', X0 + IN, X1 - IN, Y0 + IN, Y1 - IN, zf - 0.001, zc + 0.001); boolean(wl, k, 'DIFFERENCE'); kill(k); setmat(wl, white)
    for i, (cc, r0, r1) in enumerate(holes):
        sl = cyl(f'bl-sleeve-{i}', cc, r1, zf, zo); k = cyl('c', cc, r0, zf - 0.001, zo + 0.001); boolean(sl, k, 'DIFFERENCE'); kill(k); setmat(sl, white)
    # the LED strip: 5 mm wide runs along x at 25 mm pitch on the floor lining, 1 mm thick, cut round the sleeves
    led = bpy.data.materials.new('strip'); led.use_nodes = True; nt = led.node_tree; nt.nodes.clear()
    em = nt.nodes.new('ShaderNodeEmission'); em.inputs['Color'].default_value = (1.0, 0.55, 0.25, 1)
    o_ = nt.nodes.new('ShaderNodeOutputMaterial'); nt.links.new(em.outputs[0], o_.inputs['Surface'])
    runs = []; y = Y0 + IN + 0.0125
    while y < Y1 - IN - 0.006:
        r = box(f'led-strip-{len(runs)}', X0 + IN + 0.006, X1 - IN - 0.006, y - 0.0025, y + 0.0025, zf + 0.0003, zf + 0.0013)
        for (cc, r0, r1) in holes:
            k = cyl('c', cc, r1 + 0.003, zf - 0.001, zf + 0.003); boolean(r, k, 'DIFFERENCE'); kill(k)
        setmat(r, led); runs.append(r); y += 0.025
    length = sum(sum(p.area for p in r.data.polygons if abs(p.normal.z) > 0.9 and p.normal.z > 0) / 0.005 for r in runs)
    P = wpm * length
    A = sum(p.area for r in runs for p in r.data.polygons)
    em.inputs['Strength'].default_value = P / (2 * 3.14159265 * A) if P > 0 else 0.0
    # the cut pieces as surface-tinted acrylic: the plinth's absorbing volume needs a closed solid, and the boolean cuts
    # left rays 'inside' it (a 6 mm top rendered near black over a lit opal). Each sheet's own transmission instead, per
    # channel from the colour's 'deep' after 25 mm, split over its two faces (sqrt): the top at 6 mm, the frame at 10 mm
    SP = {'sp-ember': '#CF0913', 'sp-dust': '#FBBD77', 'sp-acid': '#F1EE7F', 'sp-poison': '#12AA24', 'sp-ice': '#92CCF7',
          'sp-haze': '#9F61E4', 'sp-fog': '#FCFCFC', 'sp-smoke': '#ACACAC'}
    key = args[args.index('--colour') + 1]
    lin = lambda c: c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
    deep = [lin(int(SP[key].lstrip('#')[i:i + 2], 16) / 255) for i in (0, 2, 4)]

    def sheet(name, d, rough):
        T = [max(x, 1e-4) ** (d / 0.025) for x in deep]
        m = bpy.data.materials.new(name); m.use_nodes = True; b = m.node_tree.nodes['Principled BSDF']
        b.inputs['Base Color'].default_value = tuple(t ** 0.5 for t in T) + (1,)
        b.inputs['Transmission Weight'].default_value = 1.0; b.inputs['IOR'].default_value = 1.49
        b.inputs['Roughness'].default_value = rough
        print(f'v3_day: {name}: {d * 1000:.1f} mm of {key}, T {T[0]:.3f} {T[1]:.3f} {T[2]:.3f}', flush=True)
        return m
    setmat(top, sheet('bl-tint-top', 0.006, 0.004))
    setmat(frame, sheet('bl-tint-frame', 0.010, 0.35))
    # the edge closed with a black band: the plinth's outer edge faces (the top's 6 mm and the frame's 19.4 mm) in the
    # posts' satin black, so the light guided along the top does not leave its rim as a pale line (the first test did)
    bk = bpy.data.materials.get('post-satin-black')
    if bk is None:
        black_posts(); bk = bpy.data.materials['post-satin-black']
    for o in (top, frame):
        o.data.materials.append(bk)
        M = o.matrix_world
        for p in o.data.polygons:
            c = M @ p.center; n = (M.to_3x3() @ p.normal).normalized()
            if abs(n.z) < 0.3 and min(c.x - X0, X1 - c.x, c.y - Y0, Y1 - c.y) < 0.0015:
                p.material_index = 1
    # the opal's light leaves through the glass top: Cycles counts that path as a refractive caustic, which the scene
    # turns off (with it off the deck read 0.008 over a lit opal, on 0.050); on, as the night pictures render
    sc_ = bpy.context.scene.cycles; sc_.caustics_refractive = True; sc_.caustics_reflective = True
    pl.hide_render = True; pl.hide_viewport = True
    for o in (top, frame):
        o['caustic'] = True
    print(f'v3_day: BACKLIT plinth: top 6.0 / opal 3.0 / tray 12.0 / floor 4.4 mm; {len(runs)} LED runs, {length:.2f} m at '
          f'{wpm} W/m = {P:.1f} W', flush=True)


def prepare():
    if '--backlit' in mine:
        backlit(float(mine[mine.index('--backlit') + 1]))
    if '--wb' in mine:
        vs = bpy.context.scene.view_settings; vs.use_white_balance = True
        vs.white_balance_temperature = float(mine[mine.index('--wb') + 1]); vs.white_balance_tint = 0.0
        print('v3_day: camera white balance', vs.white_balance_temperature, 'K', flush=True)
    if '--lamps-off' in mine:
        lamps_off(mine[mine.index('--lamps-off') + 1])
    if '--cards' in mine:
        cards()
    if '--black-posts' in mine:
        black_posts()
    if '--side-fix' in mine:
        side_fix()
    if '--black-bearing' in mine:
        black_bearing()
    if '--strip-watts' in mine:
        strip_watts(float(mine[mine.index('--strip-watts') + 1]))
    for o in bpy.data.objects:
        if o.name.startswith('flag-'):
            o.visible_camera = True
            print('v3_day: card', o.name, 'camera-visible', flush=True)
    for m in bpy.data.materials:
        if not m.node_tree:
            continue
        for nd in m.node_tree.nodes:
            if nd.type == 'EMISSION' and (nd.inputs['Strength'].is_linked or nd.inputs['Strength'].default_value > 0):
                users = [o.name for o in bpy.data.objects if hasattr(o.data, 'materials') and m.name in [s.material.name for s in o.material_slots if s.material]]
                if users and not all(u.startswith('led-strip') for u in users):
                    raise SystemExit(f'v3_day: {m.name} emits on {users}: no emitter allowed (the LED strip alone may)')
    bpy.ops.wm.save_as_mainfile(filepath=os.path.splitext(out)[0] + '.blend', copy=True)


class _R:
    def __getattr__(self, n):
        if n != 'render':
            return getattr(real.render, n)

        def render(*a, **k):
            prepare()
            r = real.render.render(*a, **k)
            sc = bpy.context.scene; im = sc.render.image_settings
            f, d = im.file_format, im.color_depth
            im.file_format = 'OPEN_EXR'; im.color_depth = '32'
            bpy.data.images['Render Result'].save_render(os.path.splitext(out)[0] + '.exr', scene=sc)
            im.file_format, im.color_depth = f, d
            return r
        return render


class _O:
    def __getattr__(self, n):
        return _R() if n == 'render' else getattr(real, n)


bpy.ops = _O()
sys.argv = [os.path.join(HERE, 'scene.py')] + args + ['--out', out]
os.chdir(HERE)
runpy.run_path(os.path.join(HERE, 'scene.py'), run_name='__main__')
