"""Tropos as a linkable asset: one .blend with a collection per tint, for scenes that link it (world.py).

    python3.11 spinoffs/barkhorn/biomes/tropos_lib.py [--out spinoffs/barkhorn/biomes/assets/tropos-current.blend]

The interface a swapped-in model must keep (the Tropos session's .blend, when it comes, replaces this file):
- one collection per tint, named `Tropos.Ember`, `Tropos.Dust`, ... `Tropos.Smoke`;
- each in metres, its feet at z 0, centred on x and y, its front facing -y (the studio engine's frame).
world.py links (not appends) the collections, so the model can change without touching the scene.

This build is the current design as the element scripts render it (studio/products/barkhorn-cloud.json, built by
studio/fabkit from spinoffs/barkhorn/cloud.py), cover off, with the tints of tints.json (TruCast, IOR 1.49).
"""
import json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
sys.path.insert(0, os.path.join(ROOT, 'studio', 'engine'))


def main():
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument('--out', default=os.path.join(HERE, 'assets', 'tropos-current.blend'))
    ap.add_argument('--uncalibrated', action='store_true', help="the site's tints instead of tints.json")
    ap.add_argument('--keep-back', action='store_true', help='keep the back plate, its prints and screws')
    a = ap.parse_args()
    import bpy
    from pathlib import Path
    import product as Pr
    bpy.ops.wm.read_factory_settings(use_empty=True)
    bpy.ops.preferences.addon_enable(module='cycles')
    pdef = Pr.load_def('studio/products/barkhorn-cloud.json', ROOT)
    tints = json.load(open(os.path.join(HERE, 'tints.json')))
    if not a.uncalibrated:
        for t in tints.values():
            fl = pdef['flavours'][t['flavour']]
            fl['horn_deep'] = t['horn_deep']
            m = fl.setdefault('materials', {})
            m['bark'] = {**m.get('bark', {}), 'deep': t['cabinet_deep'], 'radius': t['cabinet_radius_m'], 'ior': t['ior']}
            m['horn'] = {**m.get('horn', {}), 'radius': t['horn_radius_m'], 'ior': t['ior']}
    templates = Pr.import_model(bpy, Path(ROOT, pdef['model']), pdef['origin_mm'], pdef.get('axes', 'gltf'))
    if pdef.get('smooth'):
        Pr.smooth_parts(bpy, templates, pdef['smooth'])
    if pdef.get('normals_from'):
        Pr.normals_from(bpy, templates, pdef['normals_from'], pdef['origin_mm'], ROOT)
    names = list(tints)
    # the world shows every speaker from the front; the back's plate, prints and screws (830 k of its 1.76 M polygons)
    # are never seen, and Cycles copies each tint's geometry (its materials are per object), so they stay out
    hide = ['cloth-disc'] + ([] if a.keep_back else ['amp-plate*', 'rating-plate*', 'back-screws', 'amp-box*'])
    inst = [{'flavour': tints[n]['flavour'], 'position': [0, 0, 0], 'rotate_z': 0, 'hide': hide} for n in names]
    objs, part_of = Pr.place(bpy, pdef, templates, {'product': {'instances': inst}}, ROOT)
    # small or hidden parts thinned (screws, the lining's webs, the drivers' insides): a few pixels each in the world
    # picture, and Cycles copies each tint's geometry. The waveguide, the cabinet and the horn keep every polygon.
    if not a.keep_back:
        import re
        thin = re.compile(r'screw|lining|spider|surround|woofer-cap|web|gasket|terminal')
        dg = bpy.context.evaluated_depsgraph_get()
        done = set()
        for o in objs:
            me = o.data
            if me.name in done or len(me.polygons) < 4000 or not thin.search(part_of[o.name]):
                continue
            done.add(me.name)
            tmp = bpy.data.objects.new('tmp', me); bpy.context.scene.collection.objects.link(tmp)
            md = tmp.modifiers.new('d', 'DECIMATE'); md.ratio = 0.2
            dg.update(); new = bpy.data.meshes.new_from_object(tmp.evaluated_get(dg))
            bpy.data.objects.remove(tmp)
            for o2 in objs:
                if o2.data == me:
                    o2.data = new
    cols = {}
    for n in names:
        c = bpy.data.collections.new(f'Tropos.{n}'); bpy.context.scene.collection.children.link(c); cols[n] = c
    for o in objs:
        c = cols[names[o['instance']]]
        for uc in list(o.users_collection):
            uc.objects.unlink(o)
        c.objects.link(o)
        o['part'] = part_of[o.name]
    for n, c in cols.items():
        c['tint'] = n; c['source'] = 'studio/products/barkhorn-cloud.json + biomes/tints.json'
    os.makedirs(os.path.dirname(a.out), exist_ok=True)
    bpy.ops.wm.save_as_mainfile(filepath=os.path.abspath(a.out), compress=True)
    print(a.out, {n: len(c.objects) for n, c in cols.items()})


if __name__ == '__main__':
    main()
