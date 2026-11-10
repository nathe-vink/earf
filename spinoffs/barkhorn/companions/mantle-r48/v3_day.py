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


def white_base(wpm):
    """PROPOSAL (the coordinator, 2026-11-10 06:06): v3 as signed, with one change, the base's top lamination in opal
    (Perspex GS 041, 3.0 mm; the smoked base below it 9.7 mm, so the float stays 40 mm). The light: a 2700 K LED strip
    in a small black channel under the deck, 20 mm in from its edge (outside the base's footprint), its face at 45 deg,
    down and in onto the white. Nothing emits but the LED faces. wpm: the strip's watts a metre (0 by day)."""
    from mathutils import Vector
    from bpy_extras.object_utils import world_to_camera_view
    base = bpy.data.objects['base-L1-stack']
    zb0, zb1 = 0.0160, 0.0287; zs = zb1 - 0.003
    def box(name, x0, x1, y0, y1, z0, z1):
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2))
        b = bpy.context.active_object; b.name = name; b.scale = (x1 - x0, y1 - y0, z1 - z0); bpy.ops.object.transform_apply(scale=True)
        return b
    def boolean(t, c, op):
        m = t.modifiers.new('b', 'BOOLEAN'); m.operation = op; m.object = c; m.solver = 'EXACT'
        bpy.context.view_layer.objects.active = t; bpy.ops.object.modifier_apply(modifier=m.name)
    def copy(name):
        o = base.copy(); o.data = base.data.copy(); o.name = name; bpy.context.collection.objects.link(o); return o
    def setmat(o, m):
        o.data.materials.clear(); o.data.materials.append(m)
        for p in o.data.polygons: p.material_index = 0
    lower = copy('wb-base-smoke'); c = box('c', 0, 0.5, 0, 0.4, zb0 - 0.01, zs); boolean(lower, c, 'INTERSECT'); bpy.data.objects.remove(c)
    opal = copy('wb-base-opal'); c = box('c', 0, 0.5, 0, 0.4, zs, zb1 + 0.01); boolean(opal, c, 'INTERSECT'); bpy.data.objects.remove(c)
    # the smoked lamination surface-tinted (its own transmission at 9.7 mm: the absorbing volume needs a closed solid)
    lin = lambda c_: c_ / 12.92 if c_ <= 0.04045 else ((c_ + 0.055) / 1.055) ** 2.4
    sm = [lin(int('787B7E'[i:i + 2], 16) / 255) for i in (0, 2, 4)]          # Smoke 2074, its colour after 10 mm
    T = [x ** (9.7 / 10.0) for x in sm]
    m = bpy.data.materials.new('wb-smoke'); m.use_nodes = True; b = m.node_tree.nodes['Principled BSDF']
    b.inputs['Base Color'].default_value = tuple(t ** 0.5 for t in T) + (1,); b.inputs['Transmission Weight'].default_value = 1.0
    b.inputs['IOR'].default_value = 1.49; b.inputs['Roughness'].default_value = 0.004
    setmat(lower, m)
    om = bpy.data.materials.new('opal-041'); om.use_nodes = True; nt = om.node_tree; nt.nodes.clear()
    d = nt.nodes.new('ShaderNodeBsdfDiffuse'); d.inputs['Color'].default_value = (0.39, 0.39, 0.39, 1)
    t_ = nt.nodes.new('ShaderNodeBsdfTranslucent'); t_.inputs['Color'].default_value = (0.54, 0.54, 0.54, 1)
    g = nt.nodes.new('ShaderNodeBsdfGlossy'); g.inputs['Roughness'].default_value = 0.05; g.inputs['Color'].default_value = (0.04, 0.04, 0.04, 1)
    a1 = nt.nodes.new('ShaderNodeAddShader'); a2 = nt.nodes.new('ShaderNodeAddShader'); o_ = nt.nodes.new('ShaderNodeOutputMaterial')
    nt.links.new(d.outputs[0], a1.inputs[0]); nt.links.new(t_.outputs[0], a1.inputs[1]); nt.links.new(a1.outputs[0], a2.inputs[0])
    nt.links.new(g.outputs[0], a2.inputs[1]); nt.links.new(a2.outputs[0], o_.inputs['Surface'])
    setmat(opal, om)
    base.hide_render = True; base.hide_viewport = True
    # the channel and the strip, round the deck 20 mm in from its edge
    zd = 0.0687; X0, X1, Y0, Y1, IN = 0.01, 0.46, 0.01, 0.37, 0.020
    blk = bpy.data.materials.new('wb-channel'); blk.use_nodes = True; bb = blk.node_tree.nodes['Principled BSDF']
    bb.inputs['Base Color'].default_value = (0.008, 0.008, 0.008, 1); bb.inputs['Roughness'].default_value = 0.6
    led = bpy.data.materials.new('strip'); led.use_nodes = True; lt = led.node_tree; lt.nodes.clear()
    em = lt.nodes.new('ShaderNodeEmission'); em.inputs['Color'].default_value = (1.0, 0.55, 0.25, 1)
    lo = lt.nodes.new('ShaderNodeOutputMaterial'); lt.links.new(em.outputs[0], lo.inputs['Surface'])
    xa, xb, ya, yb = X0 + IN, X1 - IN, Y0 + IN, Y1 - IN
    faces_led = []; length = 0.0
    sides = [((xa, ya), (xb, ya), Vector((0, 1, 0))), ((xb, ya), (xb, yb), Vector((-1, 0, 0))),
             ((xb, yb), (xa, yb), Vector((0, -1, 0))), ((xa, yb), (xa, ya), Vector((1, 0, 0)))]
    for i, (p0, p1, inward) in enumerate(sides):
        p0 = Vector((*p0, 0)); p1 = Vector((*p1, 0)); L = (p1 - p0).length; length += L
        mid = (p0 + p1) / 2; along = (p1 - p0).normalized()
        # the channel: an inverted U, 8 wide x 8 deep, 1 mm walls, its open side down and in; the outer wall full height
        outer = mid - inward * 0.004
        def plate(name, centre, w_in, h, z0):
            bpy.ops.mesh.primitive_cube_add(size=1.0, location=(centre.x, centre.y, z0 + h / 2))
            o = bpy.context.active_object; o.name = name
            o.scale = ((L if abs(along.x) > 0.5 else w_in), (w_in if abs(along.x) > 0.5 else L), h)
            bpy.ops.object.transform_apply(scale=True); setmat(o, blk); return o
        plate(f'wb-channel-top-{i}', mid, 0.009, 0.001, zd - 0.001)
        plate(f'wb-channel-wall-{i}', outer, 0.001, 0.008, zd - 0.008)
        # the LED face: 5 mm wide, 3 mm under the deck, 2 mm in from the outer wall, facing down and in at 45 deg
        c_ = mid - inward * 0.0015 + Vector((0, 0, zd - 0.004))
        n = (inward + Vector((0, 0, -1))).normalized(); w = n.cross(along).normalized()
        vs = [c_ + along * (L / 2) * sa + w * 0.0025 * sb for sa, sb in ((-1, -1), (1, -1), (1, 1), (-1, 1))]
        me = bpy.data.meshes.new(f'led-strip-{i}'); me.from_pydata([tuple(v) for v in vs], [], [(0, 1, 2, 3)]); me.update()
        ob = bpy.data.objects.new(f'led-strip-{i}', me); bpy.context.collection.objects.link(ob); setmat(ob, led); faces_led.append(ob)
    A = sum(p.area for o in faces_led for p in o.data.polygons)
    P = wpm * length
    em.inputs['Strength'].default_value = P / (2 * 3.14159265 * A) if P > 0 else 0.0
    sc = bpy.context.scene; sc.cycles.caustics_refractive = True; sc.cycles.caustics_reflective = True
    # is the strip, or its channel's open side, seen? its face's points ray-cast from the camera
    bpy.context.view_layer.update(); dg = bpy.context.evaluated_depsgraph_get(); cam = sc.camera; co = cam.matrix_world.translation
    seen = tot = 0
    for o in faces_led:
        v = [o.matrix_world @ x.co for x in o.data.vertices]
        for k in range(21):
            for j in range(3):
                pt = v[0].lerp(v[1], k / 20).lerp(v[3].lerp(v[2], k / 20), j / 2)
                f = world_to_camera_view(sc, cam, pt)
                if not (f.z > 0 and 0 <= f.x <= 1 and 0 <= f.y <= 1):
                    continue
                tot += 1; dv = pt - co; dist = dv.length; dv.normalize()
                ok, *_ = sc.ray_cast(dg, co, dv, distance=dist - 1e-4)
                seen += 0 if ok else 1
    print(f'v3_day: WHITE BASE: opal 3.0 over smoke 9.7 mm; LED {length:.2f} m at {wpm} W/m = {P:.1f} W; '
          f'its face seen directly by the camera at {seen} of {tot} points in frame', flush=True)


def warm_room():
    # the dim room's ambient neutral-warm (the coordinator: the blue one read strongly blue at 4000 K)
    for o in bpy.data.objects:
        if o.type == 'LIGHT':
            o.data.color = (1.0, 0.90, 0.78)
    w = bpy.context.scene.world
    if w and w.node_tree:
        for nd in w.node_tree.nodes:
            if nd.type == 'BACKGROUND':
                nd.inputs['Color'].default_value = (0.028, 0.025, 0.021, 1)
    print('v3_day: the room ambient neutral-warm', flush=True)


def frosted(load, scat_mm, wpm):
    """PROPOSAL (the coordinator, 2026-11-10 14:54; the owner's references are milky, light-dispersing acrylic): the plinth
    AND the base in one frosted colour, a real scattering volume: the speakers' tint's own dye at `load` of its load
    (absorption x load) plus a diffuser, a scattering length of `scat_mm`. The surface: a Fresnel-weighted gloss
    (glossy faces 0.004, the satin edges 0.35) over a non-refracting boundary (inside a milky body refraction is lost after
    a few millimetres; a refracting boundary would leave the lit interior reachable by caustic paths only). The light: a
    2700 K strip loop inside the plinth, 25 mm in from its edge, 5 mm over its underside, facing up into the body, in a black
    channel open upward; wpm watts a metre (0 by day). Nothing emits but the LED faces."""
    from mathutils import Vector
    SP = {'sp-ember': '#CF0913', 'sp-ice': '#92CCF7', 'sp-dust': '#FBBD77', 'sp-acid': '#F1EE7F', 'sp-poison': '#12AA24',
          'sp-haze': '#9F61E4', 'sp-fog': '#FCFCFC', 'sp-smoke': '#ACACAC'}
    key = args[args.index('--colour') + 1]
    import math
    lin = lambda c: c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
    sig = [-math.log(max(lin(int(SP[key].lstrip('#')[i:i + 2], 16) / 255), 0.002)) / 0.025 * load for i in (0, 2, 4)]
    D = max(sig) * 1.0001
    def frost(name, rough):
        m = bpy.data.materials.new(name); m.use_nodes = True; nt = m.node_tree; nt.nodes.clear()
        out = nt.nodes.new('ShaderNodeOutputMaterial')
        tr = nt.nodes.new('ShaderNodeBsdfTransparent')
        gl = nt.nodes.new('ShaderNodeBsdfGlossy'); gl.inputs['Roughness'].default_value = rough
        fr = nt.nodes.new('ShaderNodeFresnel'); fr.inputs['IOR'].default_value = 1.49
        mx = nt.nodes.new('ShaderNodeMixShader'); nt.links.new(fr.outputs[0], mx.inputs['Fac'])
        nt.links.new(tr.outputs[0], mx.inputs[1]); nt.links.new(gl.outputs[0], mx.inputs[2]); nt.links.new(mx.outputs[0], out.inputs['Surface'])
        sc_ = nt.nodes.new('ShaderNodeVolumeScatter'); sc_.inputs['Density'].default_value = 1000.0 / scat_mm
        sc_.inputs['Color'].default_value = (1, 1, 1, 1)
        ab = nt.nodes.new('ShaderNodeVolumeAbsorption'); ab.inputs['Density'].default_value = D
        ab.inputs['Color'].default_value = tuple(1 - x / D for x in sig) + (1,)
        ad = nt.nodes.new('ShaderNodeAddShader'); nt.links.new(sc_.outputs[0], ad.inputs[0]); nt.links.new(ab.outputs[0], ad.inputs[1])
        nt.links.new(ad.outputs[0], out.inputs['Volume'])
        return m
    for oname in ('plinth-L1-stack', 'base-L1-stack'):
        o = bpy.data.objects[oname]
        for i, sl in enumerate(o.material_slots):
            sl.link = 'OBJECT'; sl.material = frost(f'frost-{oname[:4]}-{i}', 0.35 if i == 1 else 0.004)
        if oname == 'base-L1-stack':
            for sl in o.material_slots:
                sl.material = frost(f'frost-base', 0.004)
    # the strip and its channel inside the plinth
    X0, X1, Y0, Y1, IN, zb = 0.01, 0.46, 0.01, 0.37, 0.025, 0.0687
    blk = bpy.data.materials.new('fr-channel'); blk.use_nodes = True; bb = blk.node_tree.nodes['Principled BSDF']
    bb.inputs['Base Color'].default_value = (0.008, 0.008, 0.008, 1); bb.inputs['Roughness'].default_value = 0.6
    led = bpy.data.materials.new('strip'); led.use_nodes = True; lt = led.node_tree; lt.nodes.clear()
    em = lt.nodes.new('ShaderNodeEmission'); em.inputs['Color'].default_value = (1.0, 0.55, 0.25, 1)
    lo = lt.nodes.new('ShaderNodeOutputMaterial'); lt.links.new(em.outputs[0], lo.inputs['Surface'])
    xa, xb, ya, yb = X0 + IN, X1 - IN, Y0 + IN, Y1 - IN; faces = []; length = 0
    for i, ((x0, y0), (x1, y1)) in enumerate((((xa, ya), (xb, ya)), ((xb, ya), (xb, yb)), ((xb, yb), (xa, yb)), ((xa, yb), (xa, ya)))):
        L = math.hypot(x1 - x0, y1 - y0); length += L; cx, cy = (x0 + x1) / 2, (y0 + y1) / 2; horiz = abs(y1 - y0) < 1e-9
        # the channel: a black U, 7 wide, 5 deep, 0.8 walls, open upward, its floor 1 mm over the plinth's underside
        for nm, w, h, dz, off in (('floor', 0.007, 0.0008, 0.001, 0.0), ('wall-a', 0.0008, 0.005, 0.001, -0.0035), ('wall-b', 0.0008, 0.005, 0.001, 0.0035)):
            bpy.ops.mesh.primitive_cube_add(size=1.0, location=(cx + (0 if horiz else off), cy + (off if horiz else 0), zb + dz + h / 2))
            c = bpy.context.active_object; c.name = f'fr-channel-{nm}-{i}'
            c.scale = ((L, w, h) if horiz else (w, L, h)); bpy.ops.object.transform_apply(scale=True)
            c.data.materials.append(blk)
        # the LED face: 5 mm wide on the channel's floor, facing up
        z = zb + 0.0019
        vs = [(x0, y0 - 0.0025, z), (x1, y1 - 0.0025, z), (x1, y1 + 0.0025, z), (x0, y0 + 0.0025, z)] if horiz else \
             [(x0 - 0.0025, y0, z), (x0 + 0.0025, y0, z), (x1 + 0.0025, y1, z), (x1 - 0.0025, y1, z)]
        me = bpy.data.meshes.new(f'led-strip-{i}'); me.from_pydata(vs, [], [(0, 1, 2, 3)]); me.update()
        ob = bpy.data.objects.new(f'led-strip-{i}', me); bpy.context.collection.objects.link(ob); ob.data.materials.append(led); faces.append(ob)
    A = sum(p.area for o in faces for p in o.data.polygons); P = wpm * length
    em.inputs['Strength'].default_value = P / (2 * math.pi * A) if P > 0 else 0.0
    sc = bpy.context.scene.cycles; sc.volume_bounces = 64; sc.max_bounces = 128; sc.transparent_max_bounces = 64
    T25 = [math.exp(-x * 0.025) for x in sig]
    print(f'v3_day: FROSTED {key}: dye x {load} (direct T through 25 mm, dye only: {T25[0]:.3f} {T25[1]:.3f} {T25[2]:.3f}), '
          f'scattering length {scat_mm} mm; LED {length:.2f} m at {wpm} W/m = {P:.1f} W', flush=True)


def uplit(wpm):
    """PROPOSAL (the coordinator, 2026-11-10 15:05, the owner: "the LED should maybe be between the base and the top. It's
    the top that should light up"): v3 as signed, two changes. 1. The plinth's underside satin, as its edges (slot 1);
    the top stays glassy. 2. The signed LED loop moved from under the base to the base's top: a loop 20 mm in from the
    base's edge, recessed flush in a black channel (7 wide, 5 deep) cut into the base, facing straight up across the
    40 mm gap. Nothing in the gap but the posts; the channel's black walls keep the light out of the base's body.
    wpm: watts a metre (0 by day)."""
    import math
    from mathutils import Vector
    from bpy_extras.object_utils import world_to_camera_view
    pl = bpy.data.objects['plinth-L1-stack']; M = pl.matrix_world
    zb = min((M @ v.co).z for v in pl.data.vertices); n_sat = 0
    for p in pl.data.polygons:
        nw = (M.to_3x3() @ p.normal).normalized()
        if nw.z < -0.9 and abs((M @ p.center).z - zb) < 0.0005:
            p.material_index = 1; n_sat += 1
    for o in bpy.data.objects:                       # the signed loop under the base: moved, so off here
        if o.name == 'led-strip':
            o.hide_render = True
    base = bpy.data.objects['base-L1-stack']
    bx0, bx1, by0, by1, bz1 = 0.045, 0.425, 0.045, 0.335, 0.0287; IN, W, DEP = 0.020, 0.007, 0.008   # 5 deep let the camera see the face (4 of 492 points)
    xa, xb, ya, yb = bx0 + IN, bx1 - IN, by0 + IN, by1 - IN
    def box(name, x0, x1, y0, y1, z0, z1):
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2))
        b = bpy.context.active_object; b.name = name; b.scale = (x1 - x0, y1 - y0, z1 - z0); bpy.ops.object.transform_apply(scale=True)
        return b
    ring = box('groove', xa - W / 2, xb + W / 2, ya - W / 2, yb + W / 2, bz1 - DEP, bz1 + 0.002)
    inner = box('c', xa + W / 2, xb - W / 2, ya + W / 2, yb - W / 2, bz1 - DEP - 0.001, bz1 + 0.003)
    m = ring.modifiers.new('b', 'BOOLEAN'); m.operation = 'DIFFERENCE'; m.object = inner; m.solver = 'EXACT'
    bpy.context.view_layer.objects.active = ring; bpy.ops.object.modifier_apply(modifier=m.name); bpy.data.objects.remove(inner)
    m = base.modifiers.new('b', 'BOOLEAN'); m.operation = 'DIFFERENCE'; m.object = ring; m.solver = 'EXACT'
    bpy.context.view_layer.objects.active = base; bpy.ops.object.modifier_apply(modifier=m.name)
    # the channel lining: the ring groove's walls and floor in black, a hair inside the groove
    # the channel flocked matte black (a pure diffuse 1 %): a glossy black wall mirrored the bright LED face beside it as
    # a lit line round the loop (the second test)
    blk = bpy.data.materials.new('ul-channel'); blk.use_nodes = True; nt_ = blk.node_tree; nt_.nodes.clear()
    dfs = nt_.nodes.new('ShaderNodeBsdfDiffuse'); dfs.inputs['Color'].default_value = (0.01, 0.01, 0.01, 1)
    oo = nt_.nodes.new('ShaderNodeOutputMaterial'); nt_.links.new(dfs.outputs[0], oo.inputs['Surface'])
    ring.scale = (1, 1, 1)
    # (the lining stopping 0.2 under the base's top let light into the smoked acrylic at the groove's rim: a lit line; it
    # now stands 0.3 proud of the top, a black lip)
    lin_ = box('ul-channel', xa - W / 2 + 0.0002, xb + W / 2 - 0.0002, ya - W / 2 + 0.0002, yb + W / 2 - 0.0002, bz1 - DEP + 0.0002, bz1 + 0.0003)
    c2 = box('c', xa + W / 2 - 0.0002, xb - W / 2 + 0.0002, ya + W / 2 - 0.0002, yb - W / 2 + 0.0002, bz1 - DEP - 0.001, bz1 + 0.003)
    m = lin_.modifiers.new('b', 'BOOLEAN'); m.operation = 'DIFFERENCE'; m.object = c2; m.solver = 'EXACT'
    bpy.context.view_layer.objects.active = lin_; bpy.ops.object.modifier_apply(modifier=m.name); bpy.data.objects.remove(c2)
    c3 = box('c', xa - W / 2 + 0.0006, xb + W / 2 - 0.0006, ya - W / 2 + 0.0006, yb + W / 2 - 0.0006, bz1 - DEP + 0.0006, bz1 + 0.003)
    c4 = box('c4', xa + W / 2 - 0.0006, xb - W / 2 + 0.0006, ya + W / 2 - 0.0006, yb - W / 2 + 0.0006, bz1 - DEP - 0.001, bz1 + 0.004)
    m = c3.modifiers.new('b', 'BOOLEAN'); m.operation = 'DIFFERENCE'; m.object = c4; m.solver = 'EXACT'
    bpy.context.view_layer.objects.active = c3; bpy.ops.object.modifier_apply(modifier=m.name); bpy.data.objects.remove(c4)
    m = lin_.modifiers.new('b', 'BOOLEAN'); m.operation = 'DIFFERENCE'; m.object = c3; m.solver = 'EXACT'
    bpy.context.view_layer.objects.active = lin_; bpy.ops.object.modifier_apply(modifier=m.name); bpy.data.objects.remove(c3)
    lin_.data.materials.append(blk); bpy.data.objects.remove(ring)
    # the base must not glow: light the satin underside sends down enters the smoked base's top and leaves its polished
    # edges as a lit outline (the first tests). Its outer edge faces painted the posts' satin black
    bk = bpy.data.materials.get('post-satin-black')
    if bk is None:
        black_posts(); bk = bpy.data.materials['post-satin-black']
    base.data.materials.append(bk); bi = len(base.data.materials) - 1; MB = base.matrix_world; ne = 0
    for p in base.data.polygons:
        c = MB @ p.center; nw = (MB.to_3x3() @ p.normal).normalized()
        if abs(nw.z) < 0.3 and min(c.x - bx0, bx1 - c.x, c.y - by0, by1 - c.y) < 0.0015:
            p.material_index = bi; ne += 1
    print(f'v3_day: the base edge black ({ne} faces)', flush=True)
    # the LED face: 5 mm wide on the channel's floor, facing up
    led = bpy.data.materials.new('strip'); led.use_nodes = True; lt = led.node_tree; lt.nodes.clear()
    em = lt.nodes.new('ShaderNodeEmission'); em.inputs['Color'].default_value = (1.0, 0.55, 0.25, 1)
    lo = lt.nodes.new('ShaderNodeOutputMaterial'); lt.links.new(em.outputs[0], lo.inputs['Surface'])
    z = bz1 - DEP + 0.0008; faces = []; length = 0
    for i, ((x0, y0), (x1, y1)) in enumerate((((xa, ya), (xb, ya)), ((xb, ya), (xb, yb)), ((xb, yb), (xa, yb)), ((xa, yb), (xa, ya)))):
        L = math.hypot(x1 - x0, y1 - y0); length += L; h = abs(y1 - y0) < 1e-9
        vs = [(x0, y0 - 0.0025, z), (x1, y1 - 0.0025, z), (x1, y1 + 0.0025, z), (x0, y0 + 0.0025, z)] if h else \
             [(x0 - 0.0025, y0, z), (x0 + 0.0025, y0, z), (x1 + 0.0025, y1, z), (x1 - 0.0025, y1, z)]
        me = bpy.data.meshes.new(f'led-strip-{i}'); me.from_pydata(vs, [], [(0, 1, 2, 3)]); me.update()
        ob = bpy.data.objects.new(f'led-strip-{i}', me); bpy.context.collection.objects.link(ob); ob.data.materials.append(led); faces.append(ob)
    A = sum(p.area for o in faces for p in o.data.polygons); P = wpm * length
    em.inputs['Strength'].default_value = P / (2 * math.pi * A) if P > 0 else 0.0
    sc = bpy.context.scene; sc.cycles.caustics_refractive = True; sc.cycles.caustics_reflective = True
    bpy.context.view_layer.update(); dg = bpy.context.evaluated_depsgraph_get(); cam = sc.camera; co = cam.matrix_world.translation
    seen = tot = 0
    for o in faces:
        v = [o.matrix_world @ x.co for x in o.data.vertices]
        for k in range(41):
            for j in range(3):
                pt = v[0].lerp(v[1], k / 40).lerp(v[3].lerp(v[2], k / 40), j / 2) + Vector((0, 0, 0.0001))
                f = world_to_camera_view(sc, cam, pt)
                if not (f.z > 0 and 0 <= f.x <= 1 and 0 <= f.y <= 1):
                    continue
                tot += 1; dv = pt - co; dist = dv.length; dv.normalize()
                ok, *_ = sc.ray_cast(dg, co, dv, distance=dist - 2e-4)
                seen += 0 if ok else 1
    print(f'v3_day: UPLIT: the plinth underside satin ({n_sat} faces); LED loop on the base top, {IN * 1000:.0f} mm in, '
          f'recessed {DEP * 1000:.0f} mm, {length:.2f} m at {wpm} W/m = {P:.1f} W; its face seen directly at {seen} of {tot} points in frame', flush=True)


def lighttable(watts, cct):
    """PROPOSAL (the coordinator, 2026-11-10 16:50), the LIGHT-TABLE BASE: the base keeps its signed outline and smoke; its
    top carries a pocket 15 mm in from its edges, 10 mm deep, islands left round the posts (r 22), the bearing (r 30) and
    the motor (r 32), holding, bottom up: a white reflector (floor and walls), dotless COB strip runs at 12 mm pitch (5 mm
    wide), 5.2 mm of air, a 2.0 opal diffuser (Perspex 041: T 54 %, R 39 %), and a 2.0 cover of the base's own Smoke 2074,
    flush with the base's top (a dead front). The plinth as signed plus the satin underside. `watts` over all the runs
    (both faces of each emitting quad, Cycles' mesh emission), `cct` 2200 or 3000 (the strip's colour)."""
    import math
    from mathutils import Vector
    from bpy_extras.object_utils import world_to_camera_view
    # the plinth's underside satin (as the uplit proposal)
    pl = bpy.data.objects['plinth-L1-stack']; M = pl.matrix_world
    zb = min((M @ v.co).z for v in pl.data.vertices)
    for p in pl.data.polygons:
        if (M.to_3x3() @ p.normal).normalized().z < -0.9 and abs((M @ p.center).z - zb) < 0.0005:
            p.material_index = 1
    for o in bpy.data.objects:
        if o.name == 'led-strip':
            o.hide_render = True                       # the signed loop under the base: replaced by the panel
    base = bpy.data.objects['base-L1-stack']
    bx0, bx1, by0, by1, bz1 = 0.045, 0.425, 0.045, 0.335, 0.0287; IN = 0.015; DEP = 0.010
    px0, px1, py0, py1 = bx0 + IN, bx1 - IN, by0 + IN, by1 - IN; zf = bz1 - DEP
    islands = [((0.155, 0.085), 0.022), ((0.315, 0.085), 0.022), ((0.155, 0.295), 0.022), ((0.315, 0.295), 0.022),
               ((0.210, 0.178), 0.030), ((0.074, 0.303), 0.032)]
    def box(name, x0, x1, y0, y1, z0, z1):
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2))
        b = bpy.context.active_object; b.name = name; b.scale = (x1 - x0, y1 - y0, z1 - z0); bpy.ops.object.transform_apply(scale=True)
        return b
    def cyl(name, c, r, z0, z1):
        bpy.ops.mesh.primitive_cylinder_add(vertices=96, radius=r, depth=z1 - z0, location=(c[0], c[1], (z0 + z1) / 2))
        o = bpy.context.active_object; o.name = name; return o
    def boolean(t, c, op):
        m = t.modifiers.new('b', 'BOOLEAN'); m.operation = op; m.object = c; m.solver = 'EXACT'
        bpy.context.view_layer.objects.active = t; bpy.ops.object.modifier_apply(modifier=m.name)
    def pocket_shape(name, z0, z1, grow=0.0):
        b = box(name, px0 - grow, px1 + grow, py0 - grow, py1 + grow, z0, z1)
        for c, r in islands:
            k = cyl('c', c, r - grow, z0 - 0.001, z1 + 0.001); boolean(b, k, 'DIFFERENCE'); bpy.data.objects.remove(k)
        return b
    def mat_bsdf(name, build):
        m = bpy.data.materials.new(name); m.use_nodes = True; nt = m.node_tree; nt.nodes.clear()
        o_ = nt.nodes.new('ShaderNodeOutputMaterial'); nt.links.new(build(nt), o_.inputs['Surface']); return m
    def setmat(o, m):
        o.data.materials.clear(); o.data.materials.append(m)
    cut = pocket_shape('cut', zf, bz1 + 0.002); boolean(base, cut, 'DIFFERENCE'); bpy.data.objects.remove(cut)
    white = mat_bsdf('lt-reflector', lambda nt: (lambda d: (d.inputs['Color'].__setattr__('default_value', (0.92, 0.92, 0.92, 1)), d.outputs[0])[1])(nt.nodes.new('ShaderNodeBsdfDiffuse')))
    def opal_b(nt):
        d = nt.nodes.new('ShaderNodeBsdfDiffuse'); d.inputs['Color'].default_value = (0.39, 0.39, 0.39, 1)
        t = nt.nodes.new('ShaderNodeBsdfTranslucent'); t.inputs['Color'].default_value = (0.54, 0.54, 0.54, 1)
        a = nt.nodes.new('ShaderNodeAddShader'); nt.links.new(d.outputs[0], a.inputs[0]); nt.links.new(t.outputs[0], a.inputs[1]); return a.outputs[0]
    opal = mat_bsdf('lt-opal', opal_b)
    lin = lambda c: c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
    sm = [lin(int('787B7E'[i:i + 2], 16) / 255) for i in (0, 2, 4)]; Tc = [x ** (2.0 / 10.0) for x in sm]
    cover = bpy.data.materials.new('lt-cover'); cover.use_nodes = True; cb = cover.node_tree.nodes['Principled BSDF']
    cb.inputs['Base Color'].default_value = tuple(t ** 0.5 for t in Tc) + (1,); cb.inputs['Transmission Weight'].default_value = 1.0
    cb.inputs['IOR'].default_value = 1.49; cb.inputs['Roughness'].default_value = 0.004
    # the reflector: the pocket's floor and walls, a hair inside the cut
    fl = pocket_shape('lt-reflector-floor', zf + 0.0001, zf + 0.0004, grow=-0.0002); setmat(fl, white)
    wl = pocket_shape('lt-reflector-wall', zf + 0.0001, bz1 - 0.0041, grow=-0.0002)
    inner = pocket_shape('c', zf, bz1, grow=-0.0006); boolean(wl, inner, 'DIFFERENCE'); bpy.data.objects.remove(inner); setmat(wl, white)
    op = pocket_shape('lt-opal', bz1 - 0.0040, bz1 - 0.0020, grow=-0.0002); setmat(op, opal)
    cv = pocket_shape('lt-cover', bz1 - 0.0020 + 0.00005, bz1 - 0.00005, grow=-0.0002); setmat(cv, cover)
    # the strip: dotless COB runs along x at 12 mm pitch on the reflector, cut round the islands (a gap of 3 mm)
    col = {2200: (1.0, 0.45, 0.15), 3000: (1.0, 0.62, 0.33)}.get(int(cct), (1.0, 0.55, 0.25))
    led = bpy.data.materials.new('strip'); led.use_nodes = True; lt = led.node_tree; lt.nodes.clear()
    em = lt.nodes.new('ShaderNodeEmission'); em.inputs['Color'].default_value = col + (1,)
    lo = lt.nodes.new('ShaderNodeOutputMaterial'); lt.links.new(em.outputs[0], lo.inputs['Surface'])
    zl = zf + 0.0006; quads = []; y = py0 + 0.006
    while y < py1 - 0.003:
        xs = [(px0 + 0.003, px1 - 0.003)]
        for (c, r) in islands:
            if abs(y - c[1]) < r + 0.0055:
                h = math.sqrt(max((r + 0.003) ** 2 - (y - c[1]) ** 2, 0)) + 0.0025
                nxs = []
                for a, b in xs:
                    lo_, hi_ = c[0] - h, c[0] + h
                    if hi_ <= a or lo_ >= b:
                        nxs.append((a, b)); continue
                    if a < lo_: nxs.append((a, lo_))
                    if hi_ < b: nxs.append((hi_, b))
                xs = nxs
        for a, b in xs:
            if b - a > 0.004:
                quads.append([(a, y - 0.0025, zl), (b, y - 0.0025, zl), (b, y + 0.0025, zl), (a, y + 0.0025, zl)])
        y += 0.012
    me = bpy.data.meshes.new('led-strip-grid')
    verts = [v for q in quads for v in q]; faces = [(4 * i, 4 * i + 1, 4 * i + 2, 4 * i + 3) for i in range(len(quads))]
    me.from_pydata(verts, [], faces); me.update()
    ob = bpy.data.objects.new('led-strip-grid', me); bpy.context.collection.objects.link(ob); ob.data.materials.append(led)
    A = sum(p.area for p in me.polygons); length = A / 0.005
    em.inputs['Strength'].default_value = watts / (2 * math.pi * A) if watts > 0 else 0.0
    sc = bpy.context.scene; sc.cycles.caustics_refractive = True; sc.cycles.caustics_reflective = True
    # seen? the LED faces and the cover's top, ray-cast from the camera
    bpy.context.view_layer.update(); dg = bpy.context.evaluated_depsgraph_get(); cam = sc.camera; co = cam.matrix_world.translation
    def seen_pts(pts):
        s_ = t_ = 0
        for pt in pts:
            f = world_to_camera_view(sc, cam, pt)
            if not (f.z > 0 and 0 <= f.x <= 1 and 0 <= f.y <= 1):
                continue
            t_ += 1; dv = pt - co; dist = dv.length; dv.normalize()
            ok, loc, *_ = sc.ray_cast(dg, co, dv, distance=dist - 2e-4)
            s_ += 0 if ok else 1
        return s_, t_
    lp = [Vector(((q[0][0] + q[1][0]) / 2 + (q[1][0] - q[0][0]) * k / 10, q[0][1] + 0.0025, zl + 0.0001)) for q in quads for k in range(-4, 5)]
    cpts = [Vector((x, y_, bz1 + 0.00002)) for x in [px0 + (px1 - px0) * i / 30 for i in range(31)] for y_ in [py0 + (py1 - py0) * j / 20 for j in range(21)]]
    ls, lt_ = seen_pts(lp); cs, ct = seen_pts(cpts)
    print(f'v3_day: LIGHT-TABLE base: pocket 15 mm in, 10 deep; {len(quads)} COB runs, {length:.2f} m, {watts:.1f} W, '
          f'{int(cct)} K; LED faces seen at {ls} of {lt_} points; the panel face (cover top) seen at {cs} of {ct}', flush=True)


def prepare():
    if '--lighttable' in mine:
        i = mine.index('--lighttable'); lighttable(float(mine[i + 1]), float(mine[i + 2]))
    if '--uplit' in mine:
        uplit(float(mine[mine.index('--uplit') + 1]))
    if '--frosted' in mine:
        i = mine.index('--frosted'); frosted(float(mine[i + 1]), float(mine[i + 2]), float(mine[i + 3]))
    if '--white-base' in mine:
        white_base(float(mine[mine.index('--white-base') + 1]))
    if '--warm-room' in mine:
        warm_room()
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
