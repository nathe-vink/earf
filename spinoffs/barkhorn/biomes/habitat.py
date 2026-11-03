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
ASSET = os.path.join(HERE, 'assets', 'horn3', 'tropos-strata.blend')   # r33-speaker-horn a6dc9296; not in git


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


def run(shot_path, collection, out, samples, scale, asset=ASSET, root=ROOT, extra=()):
    """Render a prepared shot file through `root`'s engine with the asset linked in."""
    os.chdir(root)
    sys.path.insert(0, os.path.join(root, 'studio', 'engine'))
    import render, product as Pr, lights as Lt
    linked = []
    place0 = Pr.place

    def place(bpy_, pdef, templates, shot_, root_):
        objs, part_of = place0(bpy_, pdef, templates, shot_, root_)
        for o in objs:
            o.hide_render = True
        with bpy_.data.libraries.load(asset, link=True) as (s_, d_):
            d_.collections = [collection]
        col = d_.collections[0]
        if col is None:
            raise SystemExit(f'{collection} is not in {asset}')
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
    ap.add_argument('--collection', default='Tropos Strata {tint}')
    ap.add_argument('--light', action='append', default=[])
    ap.add_argument('--set', action='append', default=[], dest='sets')
    a = ap.parse_args()
    sh = json.load(open(a.shot))
    scale_lights(sh, {k: float(v) for k, v in (x.split('=', 1) for x in a.light)})
    for kv in a.sets:
        k, v = kv.split('=', 1)
        set_path(sh, k, json.loads(v))
    prepared = os.path.splitext(os.path.abspath(a.out))[0] + '.in.json'
    json.dump(sh, open(prepared, 'w'), indent=1)
    run(prepared, a.collection.format(tint=a.tint), a.out, a.samples, a.scale, os.path.abspath(a.asset))


if __name__ == '__main__':
    main()
