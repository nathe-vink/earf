"""Any habitat shot rendered with the linked Tropos asset in place of the engine's model (r48-biomes, 2026-11-03).

    python3.11 spinoffs/barkhorn/biomes/habitat.py SHOT.json TINT --out OUT.png [--samples N] [--scale S]
        [--asset PATH] [--collection 'Tropos Strata {tint}'] [--light NAME=FACTOR ...] [--set KEY=JSON ...]

The owner, 2026-11-03: "All of the images need to be redone" with the latest speaker. The habitats were made through the
studio engine (studio/engine/render.py) with its built-in model; this renders the same shot with the speaker lane's
asset linked in its place, so the model swaps by relinking:
- the engine's own model is still built (the shot's lamps find their parts by name) but hidden from render;
- the asset's tint collection is linked and instanced at each product instance's place and turn;
- each lamp that lights only the product (`receivers`) gets the instance in its light linking.
SHOT is a shot JSON (elements/build.py writes them to studio/shots/barkhorn/element31/). `--set` overrides a shot key
by dotted path, e.g. --set camera.lens_mm=92.
"""
import argparse, json, math, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
ASSET = os.path.join(HERE, 'assets', 'hornA2', 'tropos.blend')   # horn A, built from r33-speaker-horn b9758dd9 (make_blend.py --design current; the horn uncollapsed, its volumes closed); not in git


def set_path(d, path, value):
    keys = path.split('.')
    for k in keys[:-1]:
        d = d[int(k)] if isinstance(d, list) else d.setdefault(k, {})
    last = keys[-1]
    if isinstance(d, list):
        d[int(last)] = value
    else:
        d[last] = value


def scale_lights(sh, scales):
    for k, f in scales.items():
        if k not in sh.get('lights', {}):
            continue
        if f == 0:
            sh['lights'].pop(k)
            continue
        L = sh['lights'][k]
        for key in ('irradiance', 'power_w', 'energy'):
            if key in L:
                L[key] = L[key] * f


SURFACE_GLASS = False                   # --surface-glass: the tint on the faces (not adopted: the speaker lane's volume is the line's material)
WELD = [True]                           # the asset's split vertices welded so its glass volumes close (--no-weld: off)
HORN = {'close': False, 'rough': None}  # --horn-close: fill the horn shells' open seams; --horn-rough R: the satin's roughness (test only)
TT_SURFACE = 0.92                       # the two faces' reflection loss, as tints.py has it


def tt_factor(tt_from, tt_to, mm=20.0):
    """How much to scale an acrylic's absorption so `mm` of it passes tt_to instead of tt_from (fractions)."""
    return math.log(TT_SURFACE / tt_to) / math.log(TT_SURFACE / tt_from)


def feet(bpy_, col, r=0.016, h=0.012, inset=0.05):
    """Four rubber feet under the cabinet, where the speaker stands on its own (the stand-in until the speaker lane's
    final model: the owner, 2026-11-03, isn't convinced a base is needed)."""
    import bmesh
    from mathutils import Vector
    lo = [1e9, 1e9]; hi = [-1e9, -1e9]
    for o in col.all_objects:
        if o.type == 'MESH' and not o.name.split(' ')[-1].startswith('base-plinth') and o.name.split(' ')[-1] in ('bottom', 'left', 'right', 'front-panel', 'back'):
            for v in o.bound_box:
                w = o.matrix_world @ Vector(v)
                lo = [min(lo[0], w.x), min(lo[1], w.y)]; hi = [max(hi[0], w.x), max(hi[1], w.y)]
    m = bpy_.data.materials.new('foot-rubber'); m.use_nodes = True
    bs = m.node_tree.nodes['Principled BSDF']; bs.inputs['Base Color'].default_value = (0.02, 0.02, 0.02, 1)
    bs.inputs['Roughness'].default_value = 0.8
    for x in (lo[0] + inset, hi[0] - inset):
        for y in (lo[1] + inset, hi[1] - inset):
            bm = bmesh.new(); bmesh.ops.create_cone(bm, cap_ends=True, segments=24, radius1=r, radius2=r, depth=h)
            me = bpy_.data.meshes.new('foot'); bm.to_mesh(me); bm.free(); me.materials.append(m)
            f = bpy_.data.objects.new('foot', me); f.location = (x, y, h / 2); col.objects.link(f)


def uplight(bpy_, col, watts=40.0, color=(1.0, 0.9, 0.8)):
    """The night layer: light shining up through the speaker from inside its bottom (the site's uplit look), never
    down or out onto the floor. A small area lamp facing up, just above the bottom panel."""
    from mathutils import Vector
    zb, lo, hi = 0.0, [1e9, 1e9], [-1e9, -1e9]
    for o in col.all_objects:
        if o.type == 'MESH' and o.name.endswith(' bottom'):
            for v in o.bound_box:
                w = o.matrix_world @ Vector(v)
                zb = max(zb, w.z); lo = [min(lo[0], w.x), min(lo[1], w.y)]; hi = [max(hi[0], w.x), max(hi[1], w.y)]
    L = bpy_.data.lights.new('uplight', 'AREA'); L.shape = 'RECTANGLE'
    L.size = (hi[0] - lo[0]) * 0.6; L.size_y = (hi[1] - lo[1]) * 0.6; L.energy = watts; L.color = color
    o = bpy_.data.objects.new('uplight', L); o.location = ((lo[0] + hi[0]) / 2, (lo[1] + hi[1]) / 2, zb + 0.004)
    col.objects.link(o)                     # an area lamp shines along its -z: turned over, it faces up
    o.rotation_euler = (math.pi, 0, 0)


def settle(bpy_, linked, sink=0.002):
    """Stand each speaker on the ground under it: a ray down through each of its feet (the asset's lowest points) onto
    the set, and the instance raised or lowered so the lowest foot touches the highest hit, sunk `sink` m."""
    from mathutils import Vector
    dg = bpy_.context.evaluated_depsgraph_get()
    sc = bpy_.context.scene
    for e in linked:
        col = e.instance_collection
        pts = []
        for o in col.all_objects:
            if o.type != 'MESH':
                continue
            for v in o.bound_box:
                w = o.matrix_world @ Vector(v)
                pts.append(w)
        if not pts:
            continue
        zmin = min(p.z for p in pts)
        feet_ = [p for p in pts if p.z < zmin + 0.01]
        xs = [p.x for p in feet_]; ys = [p.y for p in feet_]
        corners = [(min(xs), min(ys)), (min(xs), max(ys)), (max(xs), min(ys)), (max(xs), max(ys)), (sum(xs) / len(xs), sum(ys) / len(ys))]
        # the speaker itself, the hidden engine copy and the volumes out of the rays' way while they look for ground
        hide = [o for o in sc.objects if o.hide_render or o.get('volume') or o in linked]
        was = [(o, o.hide_viewport) for o in hide]
        for o in hide:
            o.hide_viewport = True
        dg = bpy_.context.evaluated_depsgraph_get(); dg.update()
        hits = []
        for cx, cy in corners:
            wp = e.matrix_world @ Vector((cx, cy, 0.0))
            ok, loc, nrm, idx, obj, mat = sc.ray_cast(dg, Vector((wp.x, wp.y, wp.z + 3.0)), Vector((0, 0, -1)), distance=6.0)
            if ok:
                hits.append(loc.z)
        for o, v in was:
            o.hide_viewport = v
        if hits:
            z_new = max(hits) - zmin - sink
            print(f'ground: {e.name} feet on the set at z {max(hits):.4f} (from {e.location.z:.4f} to {z_new:.4f}; hits {[round(h, 4) for h in hits]})')
            e.location.z = z_new


def black_flag(bpy_, linked, size):
    """A photographer's negative fill: a large black card behind and above the camera, out of frame, seen only in
    reflections (glossy rays), so the speaker's front faces mirror black instead of the bright sky; it casts no
    shadow and lights nothing."""
    import bmesh
    from mathutils import Vector
    sc = bpy_.context.scene
    cam = sc.camera
    if not linked or cam is None:
        return
    t = linked[0].location
    c = cam.location
    d = (c - Vector((t.x, t.y, c.z))).normalized()
    pos = c + d * 1.2 + Vector((0, 0, 1.4))
    w, h = size
    bm = bmesh.new(); bmesh.ops.create_grid(bm, x_segments=1, y_segments=1, size=0.5)
    me = bpy_.data.meshes.new('black-flag'); bm.to_mesh(me); bm.free()
    m = bpy_.data.materials.new('black-flag'); m.use_nodes = True
    bs = m.node_tree.nodes['Principled BSDF']; bs.inputs['Base Color'].default_value = (0.0, 0.0, 0.0, 1)
    bs.inputs['Roughness'].default_value = 1.0; bs.inputs['Specular IOR Level'].default_value = 0.0
    me.materials.append(m)
    f = bpy_.data.objects.new('black-flag', me); sc.collection.objects.link(f)
    f.location = pos; f.scale = (w, h, 1.0)
    f.rotation_euler = (Vector((t.x, t.y, t.z + 0.7)) - pos).to_track_quat('Z', 'Y').to_euler()
    f.visible_camera = False; f.visible_diffuse = False; f.visible_shadow = False
    f.visible_transmission = False; f.visible_volume_scatter = False
    print(f'black flag: {w} x {h} m at {[round(v, 2) for v in pos]}')
    # and a card each side of the speaker, square to the camera's line, out of frame: the side walls mirror them, not
    # the sky, at the grazing angles where acrylic reflects most
    side = Vector((-d.y, d.x, 0.0))
    for k, sgn in enumerate((1, -1)):
        p_ = Vector((t.x, t.y, 0.9)) + side * sgn * 1.8 - d * 0.6
        c_ = f.copy(); c_.data = me; sc.collection.objects.link(c_)
        c_.location = p_; c_.scale = (2.6, 2.4, 1.0)
        c_.rotation_euler = (Vector((t.x, t.y, 0.7)) - p_).to_track_quat('Z', 'Y').to_euler()
    print('side cards: 2.6 x 2.4 m, 1.8 m each side')


def run(shot_path, collection, out, samples, scale, asset=ASSET, root=ROOT, extra=(), stand='feet', tt=None,
        up=0.0, glass_from=0.12, ground=True, flag=(8.0, 6.0), lining=None, glass_shadows=True):
    """Render a prepared shot file through `root`'s engine with the asset in. stand 'feet' leaves the stand-in plinth
    out and stands the speaker on four feet; 'plinth' keeps the asset as it is (linked). tt: the cabinet's and horn's
    transmission through 20 mm to render at, from `glass_from` (Smoke's 2074 is 0.12); up: the night uplight (W)."""
    os.chdir(root)
    sys.path.insert(0, os.path.join(root, 'studio', 'engine'))
    import bpy  # noqa: F401  (mathutils comes with it)
    import render, product as Pr, lights as Lt
    linked = []
    place0 = Pr.place
    editable = stand == 'feet' or tt or up or lining or glass_shadows or HORN['close'] or HORN['rough'] is not None   # else the asset as it is, linked

    def place(bpy_, pdef, templates, shot_, root_):
        objs, part_of = place0(bpy_, pdef, templates, shot_, root_)
        for o in objs:
            o.hide_render = True
        with bpy_.data.libraries.load(asset, link=not editable) as (s_, d_):
            d_.collections = [collection]
        col = d_.collections[0]
        if col is None:
            raise SystemExit(f'{collection} is not in {asset}')
        if stand == 'feet':
            drop = []
            for o in list(col.all_objects):
                if 'base-plinth' in o.name:
                    col.objects.unlink(o); drop.append(o)
            feet(bpy_, col)
            print('stand: on four feet; left out', [o.name for o in drop])
        if tt:
            f = tt_factor(glass_from, tt)
            done = set()
            for o in col.all_objects:
                for sl in getattr(o, 'material_slots', []):
                    m = sl.material
                    if not m or m.name in done or not m.name.split('@')[0] in ('bark', 'horn-lot') or not m.node_tree:
                        continue
                    done.add(m.name)
                    for n in m.node_tree.nodes:
                        if n.type in ('VOLUME_ABSORPTION', 'PRINCIPLED_VOLUME') and 'Density' in n.inputs:
                            n.inputs['Density'].default_value *= f
            print(f'glass: {glass_from:.0%} -> {tt:.0%} through 20 mm (absorption x {f:.3f}) on', sorted(done))
        if WELD[0]:
            # the asset's panels arrive from glTF with their vertices split at every seam, which leaves each glass
            # volume open (the speaker lane, 2026-11-03: welded, every panel closes, normals out); weld them
            import bmesh
            seen = set(); nw = 0
            for o in col.all_objects:
                if o.type != 'MESH' or o.data.name in seen:
                    continue
                seen.add(o.data.name)
                bm = bmesh.new(); bm.from_mesh(o.data)
                n0 = len(bm.verts)
                bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=1e-5)
                if len(bm.verts) < n0:
                    nw += 1
                    bm.to_mesh(o.data)
                    flat = any(sl.material and sl.material.name.split('@')[0] == 'bark' for sl in o.material_slots)
                    o.data.polygons.foreach_set('use_smooth', [not flat] * len(o.data.polygons))
                bm.free()
            print(f'weld: {nw} meshes welded')
        if HORN['close']:
            # the horn's shells (throat, waveguide, cap) stay open after the weld (seams 0.6-1.1 m long): a glass volume
            # with a gap leaks, rays inside stay "in the resin". Fill each hole so the volume closes
            import bmesh
            for o in col.all_objects:
                if o.type == 'MESH' and any(k in o.name for k in ('horn-throat', 'waveguide')):
                    bm = bmesh.new(); bm.from_mesh(o.data)
                    bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=1e-4)
                    r = bmesh.ops.holes_fill(bm, edges=bm.edges, sides=0)
                    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
                    left = sum(1 for e in bm.edges if len(e.link_faces) == 1)
                    bm.to_mesh(o.data); bm.free()
                    print('horn close:', o.name, len(r['faces']), 'faces filled,', left, 'open edges left')
        if HORN['rough'] is not None:
            for m in {sl.material for o in col.all_objects for sl in getattr(o, 'material_slots', []) if sl.material}:
                if m.name.split('@')[0] == 'horn-satin' and m.node_tree:
                    for n in m.node_tree.nodes:
                        if n.type == 'BSDF_PRINCIPLED':
                            n.inputs['Roughness'].default_value = HORN['rough']
            print('horn satin roughness ->', HORN['rough'])
        if glass_shadows:
            # light through the glass: Cycles renders without refractive caustics, so no lamp lights anything inside or
            # behind a clear wall and the inside reads black whatever the tint. Shadow rays pass each acrylic wall
            # tinted by what that wall transmits (its absorption over its thickness), the rest of the shading untouched
            done = {}
            for o in col.all_objects:
                for sl in getattr(o, 'material_slots', []):
                    m = sl.material
                    base = m.name.split('@')[0] if m else ''
                    if not m or not m.node_tree or base not in ('bark', 'horn-formed', 'horn-satin', 'horn-lot') or m.name in done:
                        continue
                    nt = m.node_tree
                    out = next((n for n in nt.nodes if n.type == 'OUTPUT_MATERIAL' and n.is_active_output), None)
                    absn = next((n for n in nt.nodes if n.type == 'VOLUME_ABSORPTION'), None)
                    if out is None or absn is None or not out.inputs['Surface'].links:
                        continue
                    mm = 0.020 if base == 'bark' else 0.0127
                    c = absn.inputs['Color'].default_value; dens = absn.inputs['Density'].default_value
                    tr = [math.exp(-(1 - c[i]) * dens * mm) for i in range(3)]
                    if SURFACE_GLASS:
                        # the tint on the faces instead of in a volume: the asset's panels don't close the volume
                        # (rays inside the cabinet stay "in the glass" and the inside reads black whatever the
                        # tint); each face takes the square root of its wall's transmission, two faces a wall
                        for l in list(out.inputs['Volume'].links):
                            nt.links.remove(l)
                        bs = next((n for n in nt.nodes if n.type == 'BSDF_PRINCIPLED'), None)
                        if bs is not None:
                            bs.inputs['Base Color'].default_value = (*[math.sqrt(x) for x in tr], 1)
                    src = out.inputs['Surface'].links[0].from_socket
                    lp = nt.nodes.new('ShaderNodeLightPath'); tp = nt.nodes.new('ShaderNodeBsdfTransparent')
                    tp.inputs['Color'].default_value = (*tr, 1)
                    mx = nt.nodes.new('ShaderNodeMixShader')
                    nt.links.new(lp.outputs['Is Shadow Ray'], mx.inputs[0])
                    nt.links.new(src, mx.inputs[1]); nt.links.new(tp.outputs[0], mx.inputs[2])
                    nt.links.new(mx.outputs[0], out.inputs['Surface'])
                    done[m.name] = [round(x, 3) for x in tr]
            print('glass shadows:', done)
        if lining:
            # the lining's color (colors F: Smoke on black, the others white): the asset, appended, takes it
            h = lining.lstrip('#'); rgb = [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]
            rgb = [c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4 for c in rgb]
            done = set()
            for o in col.all_objects:
                for sl in getattr(o, 'material_slots', []):
                    m = sl.material
                    if m and m.name.split('@')[0] == 'lining' and m.name not in done and m.node_tree:
                        done.add(m.name)
                        for n in m.node_tree.nodes:
                            if n.type == 'BSDF_PRINCIPLED':
                                n.inputs['Base Color'].default_value = (*rgb, 1)
            print('lining:', lining, sorted(done))
        if up:
            uplight(bpy_, col, up)
        for inst in shot_['product']['instances']:
            e = bpy_.data.objects.new(collection, None)
            e.instance_type = 'COLLECTION'; e.instance_collection = col
            e.location = inst.get('position', (0, 0, 0)); e.rotation_euler = (0, 0, math.radians(inst.get('rotate_z', 0)))
            bpy_.context.scene.collection.objects.link(e)
            linked.append(e)
        return objs, part_of
    Pr.place = place
    link0 = Lt.link_receivers

    def link_receivers(bpy_, light_ob, objects):
        link0(bpy_, light_ob, objects)
        col = light_ob.light_linking.receiver_collection
        for e in linked:
            if e.name not in col.objects:
                col.objects.link(e)
    Lt.link_receivers = link_receivers
    world0 = Lt.world

    def world(bpy_, sky, sun_spec=None):
        r = world0(bpy_, sky, sun_spec)
        if ground:
            settle(bpy_, linked)
        if flag:
            black_flag(bpy_, linked, flag)
        return r
    Lt.world = world
    sys.argv = ['render.py', shot_path, '--out', os.path.abspath(out), '--samples', str(samples), '--scale', str(scale), *extra]
    render.main()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('shot'); ap.add_argument('tint')
    ap.add_argument('--out', required=True); ap.add_argument('--samples', type=int, default=64)
    ap.add_argument('--scale', type=float, default=1.0)
    ap.add_argument('--asset', default=ASSET)
    ap.add_argument('--collection', default='Tropos {tint}')
    ap.add_argument('--light', action='append', default=[])
    ap.add_argument('--set', action='append', default=[], dest='sets')
    ap.add_argument('--stand', choices=['own', 'feet', 'plinth'], default='own')
    ap.add_argument('--tt', type=float, help="the glass's transmission through 20 mm to render at (e.g. 0.29)")
    ap.add_argument('--glass-from', type=float, default=0.12, help="the asset's own (Smoke 2074: 0.12)")
    ap.add_argument('--uplight', type=float, default=0.0, help='the night uplight, W (0: off, the day)')
    ap.add_argument('--no-ground', action='store_true', help="don't settle the speaker onto the set")
    ap.add_argument('--no-weld', action='store_true'); ap.add_argument('--surface-glass', action='store_true')
    ap.add_argument('--lining', help="the lining's color, hex (colors F: Smoke '#0B0B0B')")
    ap.add_argument('--horn-close', action='store_true'); ap.add_argument('--horn-rough', type=float)
    ap.add_argument('--flag', type=float, nargs=2, default=(8.0, 6.0), help='the black flag behind the camera, m (0 0: none)')
    a = ap.parse_args()
    global SURFACE_GLASS
    WELD[0] = not a.no_weld; SURFACE_GLASS = a.surface_glass
    HORN['close'] = a.horn_close; HORN['rough'] = a.horn_rough
    sh = json.load(open(a.shot))
    scale_lights(sh, {k: float(v) for k, v in (x.split('=', 1) for x in a.light)})
    for kv in a.sets:
        k, v = kv.split('=', 1)
        set_path(sh, k, json.loads(v))
    prepared = os.path.splitext(os.path.abspath(a.out))[0] + '.in.json'
    json.dump(sh, open(prepared, 'w'), indent=1)
    run(prepared, a.collection.format(tint=a.tint), a.out, a.samples, a.scale, os.path.abspath(a.asset), stand=a.stand,
        tt=a.tt, up=a.uplight, glass_from=a.glass_from, ground=not a.no_ground, flag=tuple(a.flag) if a.flag[0] > 0 else None,
        lining=a.lining)


if __name__ == '__main__':
    main()
