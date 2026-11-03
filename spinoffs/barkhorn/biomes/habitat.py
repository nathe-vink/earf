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
ASSET = os.path.join(HERE, 'assets', 'hornA', 'tropos.blend')   # horn A, built from r33-speaker-horn 4ec3bc96 (make_blend.py --design current); not in git


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


def run(shot_path, collection, out, samples, scale, asset=ASSET, root=ROOT, extra=(), stand='feet', tt=None,
        up=0.0, glass_from=0.12):
    """Render a prepared shot file through `root`'s engine with the asset in. stand 'feet' leaves the stand-in plinth
    out and stands the speaker on four feet; 'plinth' keeps the asset as it is (linked). tt: the cabinet's and horn's
    transmission through 20 mm to render at, from `glass_from` (Smoke's 2074 is 0.12); up: the night uplight (W)."""
    os.chdir(root)
    sys.path.insert(0, os.path.join(root, 'studio', 'engine'))
    import bpy  # noqa: F401  (mathutils comes with it)
    import render, product as Pr, lights as Lt
    linked = []
    place0 = Pr.place
    editable = stand == 'feet' or tt or up      # 'own' and 'plinth': the asset as it is, linked

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
    a = ap.parse_args()
    sh = json.load(open(a.shot))
    scale_lights(sh, {k: float(v) for k, v in (x.split('=', 1) for x in a.light)})
    for kv in a.sets:
        k, v = kv.split('=', 1)
        set_path(sh, k, json.loads(v))
    prepared = os.path.splitext(os.path.abspath(a.out))[0] + '.in.json'
    json.dump(sh, open(prepared, 'w'), indent=1)
    run(prepared, a.collection.format(tint=a.tint), a.out, a.samples, a.scale, os.path.abspath(a.asset), stand=a.stand,
        tt=a.tt, up=a.uplight, glass_from=a.glass_from)


if __name__ == '__main__':
    main()
