"""Hiddencast for the bpy-direct lamp rigs (the coordinator's rule, 2026-11-09 19:13): NO light, card or panel may stand
in frame hidden from the camera, except a practical's bulb inside its own opal or frosted fitting. A hidden object
outside the frame is fine.

`hiddencast(scene)` ray-casts a 96 x 96 grid through the scene camera's frame, padded 3 % past each edge (as the speaker
lane's shots.card_coverage), and returns, for every object the camera cannot see, the share of those rays that would hit
its whole shape, occlusion ignored:
  - meshes with camera visibility off (their own BVH);
  - every lamp with camera visibility off: an AREA lamp as its square, rectangle, disc or ellipse; a POINT or SPOT lamp
    as its sphere (shadow_soft_size); a SUN has no place and is left out. (A lamp with camera visibility on is drawn by
    Cycles, as its shape, and is not hidden.)
A lamp whose name starts with one of PRACTICAL is the practical's bulb inside its own fitting (the Hemisphere's COB in
its reflector and liner, Core's LED under its frosted ball): reported, marked, not counted.

    from hiddencast_bpy import hiddencast, report
    print(report(frame, hiddencast(bpy.context.scene)))
"""
import math

PRACTICAL = ('cob', 'led')                                            # cob, cob-<tint>, led-<tint>, ledface


def _rays(sc, n=96, pad=0.03):
    cam = sc.camera
    mw = cam.matrix_world
    fr = [mw @ v for v in cam.data.view_frame(scene=sc)]             # tr, br, bl, tl (lens shift included)
    o = mw.translation.copy()
    out = []
    for j in range(n):
        v = -pad + (1 + 2 * pad) * (j + 0.5) / n
        for i in range(n):
            u = -pad + (1 + 2 * pad) * (i + 0.5) / n
            top = fr[3].lerp(fr[0], u); bot = fr[2].lerp(fr[1], u)
            out.append((top.lerp(bot, v) - o).normalized())
    return o, out


def _hit_light(ob, o, d):
    L = ob.data
    mi = ob.matrix_world.inverted()
    lo = mi @ o; ld = mi.to_3x3() @ d                                 # object space (scale carried in ld)
    if L.type == 'AREA':
        if abs(ld.z) < 1e-12:
            return False
        t = -lo.z / ld.z
        if t <= 0:
            return False
        x = lo.x + t * ld.x; y = lo.y + t * ld.y
        a = L.size / 2; b = (L.size_y if L.shape in ('RECTANGLE', 'ELLIPSE') else L.size) / 2
        if L.shape in ('DISK', 'ELLIPSE'):
            return (x / a) ** 2 + (y / b) ** 2 <= 1.0
        return abs(x) <= a and abs(y) <= b
    if L.type in ('POINT', 'SPOT'):
        r = max(L.shadow_soft_size, 1e-4)
        c = ob.matrix_world.translation
        oc = o - c; bq = oc.dot(d); cq = oc.dot(oc) - r * r
        disc = bq * bq - cq
        return disc >= 0 and (-bq + math.sqrt(disc)) > 0
    return None                                                       # SUN: nowhere


def hiddencast(sc):
    """[(kind, name, share 0-1, practical)] for every object hidden from the camera."""
    # 2026-11-09 23:40 (the cast check): the world matrices are stale until the depsgraph updates; without this the
    # camera sat at its rest pose and the audit's numbers were wrong (the orb row's 4 m key: 0 % read, 24 % real)
    import bpy
    bpy.context.view_layer.update()
    o, rays = _rays(sc)
    rows = []
    for ob in sc.objects:
        if ob.type == 'MESH' and not ob.visible_camera:
            mi = ob.matrix_world.inverted(); lo = mi @ o; m3 = mi.to_3x3()
            hit = sum(1 for d in rays if ob.ray_cast(lo, (m3 @ d).normalized())[0])
            rows.append(('hidden mesh', ob.name, hit / len(rays), False))
        elif ob.type == 'LIGHT' and ob.data.type != 'SUN' and not ob.visible_camera:
            hit = sum(1 for d in rays if _hit_light(ob, o, d))
            kind = f"{ob.data.type.lower()} lamp" + (f" ({ob.data.shape.lower()})" if ob.data.type == 'AREA' else '')
            rows.append((kind, ob.name, hit / len(rays), ob.name.startswith(PRACTICAL)))
    return rows


def report(frame, rows):
    bad = [r for r in rows if r[2] > 0 and not r[3]]
    lines = [f"HIDDENCAST {frame}: {len(rows)} hidden, {len(bad)} in frame"]
    for k, n, s, p in rows:
        tag = 'IN FRAME' if s > 0 and not p else ('practical' if p else 'out')
        lines.append(f"   {tag:9s} {s * 100:5.1f} %  {k} {n}")
    return '\n'.join(lines)


def coverage(sc, ob):
    o, rays = _rays(sc)
    return sum(1 for d in rays if _hit_light(ob, o, d)) / len(rays)


def slide_out(sc, ob, target, ok=lambda loc: True, kmax=8.0):
    """Slide a hidden AREA lamp away from `target` along the line through it until no ray of the frame meets it,
    its size grown by k to hold its angle at the target and its power by k squared (its radiance, so the irradiance at
    the target, held), as the speaker lane's realize_hidden. `ok(location)` keeps it inside the room. Returns k, or None
    (the lamp left where it was) if it cannot leave the frame."""
    from mathutils import Vector
    t = Vector(target); p0 = ob.location.copy(); s0 = (ob.data.size, ob.data.size_y); e0 = ob.data.energy
    for k10 in range(11, int(kmax * 10) + 1):
        k = k10 / 10
        loc = t + (p0 - t) * k
        if not ok(loc):
            break
        ob.location = loc; ob.data.size, ob.data.size_y = s0[0] * k, s0[1] * k; ob.data.energy = e0 * k * k
        bpy_update(sc)
        if coverage(sc, ob) == 0.0:
            return k
    ob.location = p0; ob.data.size, ob.data.size_y = s0; ob.data.energy = e0
    bpy_update(sc)
    return None


def bpy_update(sc):
    import bpy
    bpy.context.view_layer.update()


def mask_check(sc, out_png):
    """The cast check with Blender's own camera (the coordinator, 2026-11-09 23:11, after the speaker lane's audit
    built its camera differently from the renderer): every object hidden from the camera made visible (meshes as a
    flat white emission, lamps as themselves), everything else held out, the world black, 1 sample, at the picture's
    own resolution and crop; returns {name: share of the frame's pixels it covers} and writes the mask. Run it on a
    built scene, in place of the render (it changes the scene)."""
    import bpy
    bpy.context.view_layer.update()
    hidden = [o for o in sc.objects if (o.type == 'MESH' and not o.visible_camera)
              or (o.type == 'LIGHT' and o.data.type != 'SUN' and not o.visible_camera)]
    em = bpy.data.materials.new('castcheck'); em.use_nodes = True; nt = em.node_tree; nt.nodes.clear()
    e = nt.nodes.new('ShaderNodeEmission'); e.inputs['Strength'].default_value = 1.0
    o_ = nt.nodes.new('ShaderNodeOutputMaterial'); nt.links.new(e.outputs[0], o_.inputs['Surface'])
    for o in sc.objects:
        if o.type == 'MESH':
            if o in hidden:
                o.visible_camera = True; o.data.materials.clear(); o.data.materials.append(em)
                for s in o.material_slots:
                    s.link = 'DATA'
            else:
                o.is_holdout = True
        elif o.type == 'LIGHT':
            o.hide_render = True
    # a hidden lamp as a two-sided card (or sphere) of its own shape at its own place: Cycles draws an area lamp only
    # from its emitting side, so one facing away from the lens would read 0 % while it stands in frame
    import bmesh
    proxies = {}
    for h in [o for o in hidden if o.type == 'LIGHT']:
        L = h.data; bm = bmesh.new()
        if L.type == 'AREA':
            a = L.size / 2; b = (L.size_y if L.shape in ('RECTANGLE', 'ELLIPSE') else L.size) / 2
            if L.shape in ('DISK', 'ELLIPSE'):
                bmesh.ops.create_circle(bm, cap_ends=True, segments=48, radius=1.0)
                for v in bm.verts:
                    v.co.x *= a; v.co.y *= b
            else:
                bmesh.ops.create_grid(bm, x_segments=1, y_segments=1, size=1.0)
                for v in bm.verts:
                    v.co.x *= a; v.co.y *= b
        else:
            bmesh.ops.create_uvsphere(bm, u_segments=24, v_segments=12, radius=max(L.shadow_soft_size, 1e-3))
        me = bpy.data.meshes.new('cc-' + h.name); bm.to_mesh(me); bm.free(); me.materials.append(em)
        po = bpy.data.objects.new('cc-' + h.name, me); sc.collection.objects.link(po); po.matrix_world = h.matrix_world.copy()
        proxies[h.name] = po
    targets = [(h.name, proxies.get(h.name, h)) for h in hidden]
    if sc.world:
        sc.world.use_nodes = True
        for n in sc.world.node_tree.nodes:
            if n.type == 'BACKGROUND':
                n.inputs['Strength'].default_value = 0.0
    sc.cycles.samples = 1; sc.cycles.use_denoising = False; sc.render.film_transparent = True
    sc.render.dither_intensity = 0.0                  # (the 8-bit dither set stray pixels to 1/255)
    sc.render.image_settings.file_format = 'PNG'; sc.render.image_settings.color_mode = 'RGBA'
    sc.view_settings.view_transform = 'Standard'; sc.view_settings.look = 'None'; sc.view_settings.exposure = 0.0
    sc.render.filepath = out_png
    res = {}
    for name, h in targets:                           # one object at a time, so each one's share is its own
        for _, o in targets:
            o.hide_render = (o is not h)
        f = out_png.rsplit('.', 1)[0] + '-' + name + '.png'       # each object's own mask
        sc.render.filepath = f
        bpy.ops.render.render(write_still=True)
        img = bpy.data.images.load(f, check_existing=False); px = img.pixels[:]
        n = len(px) // 4
        lit = sum(1 for i in range(n) if max(px[4 * i], px[4 * i + 1], px[4 * i + 2]) > 0.02)
        res[name] = lit / n
        bpy.data.images.remove(img)
    return res
