"""Tropos as a linkable Blender asset (2026-10-31): the current design, one collection per tint, each marked as an
asset, so another scene can link or append "Tropos Ember" and the rest. The parts, normals and materials are the
render engine's own (studio/engine/product.py: import_model, smooth_parts, normals_from, place), so a linked Tropos
looks as it does in the studio's renders.

    python3.11 spinoffs/barkhorn/asset/make_blend.py [--out spinoffs/barkhorn/asset/tropos.blend] [--product ...]

Needs the Cloud's render model, spinoffs/barkhorn/out-cloud/render/barkhorn-cloud.glb (written by the Cloud's
fabkit build; not in git). Each speaker stands at the origin, its feet on z = 0, its front facing -y, in metres;
the collections are hidden from the view layer except Ember, so the file opens on one speaker.

In another file (bpy):

    with bpy.data.libraries.load('/path/tropos.blend', link=True, assets_only=True) as (src, dst):
        dst.collections = ['Tropos Smoke']
    inst = bpy.data.objects.new('Tropos', None); inst.instance_type = 'COLLECTION'
    inst.instance_collection = bpy.data.collections['Tropos Smoke']; bpy.context.scene.collection.objects.link(inst)

or the Asset Browser, with the file's folder added as an asset library.
"""
import argparse, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT / 'studio' / 'engine'))

# the eight tints, by the site's names, and the flavours that are them (the line-up, studio31/lineup.json)
# small detail that is millions of triangles and invisible past arm's length (the plates' printed text, the screws'
# threads): collapsed to these ratios, so the file stays small enough to keep in git; --full keeps everything
LIGHTER = {'amp-plate-print': 0.15, 'rating-plate-print': 0.15, 'amp-plate-ink': 0.25, 'back-screws': 0.1,
           'amp-plate-screws': 0.25, 'woofer-screws': 0.25, 'woofer-spider': 0.5, 'woofer-cap': 0.5,
           # and, for a speaker seen across a landscape, the horn's dense tessellation and the lining's voile webs
           'waveguide': 0.35, 'horn-throat': 0.4, 'waveguide-cap': 0.4, 'lining-*-web': 0.3}
TINTS = [('Ember', 'cloud-red'), ('Dust', 'cloud-orange'), ('Acid', 'cloud-amber'), ('Poison', 'eucalyptus-y2k-green'),
         ('Ice', 'cloud-blue'), ('Haze', 'cloud-violet'), ('Fog', 'birch-fog-clear'), ('Smoke', 'cloud-black')]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--out', default=str(HERE / 'tropos.blend'))
    ap.add_argument('--product', default='studio/products/barkhorn-cloud.json')
    ap.add_argument('--name', default='Tropos')
    ap.add_argument('--full', action='store_true', help='keep every triangle (no LIGHTER)')
    a = ap.parse_args()
    import bpy
    import product as Pr

    bpy.ops.wm.read_factory_settings(use_empty=True)
    pdef = Pr.load_def(a.product, ROOT)
    templates = Pr.import_model(bpy, Path(ROOT, pdef['model']), pdef['origin_mm'], pdef.get('axes', 'gltf'))
    if pdef.get('smooth'):
        Pr.smooth_parts(bpy, templates, pdef['smooth'])
    if pdef.get('normals_from'):              # the shading normals; the waveguide's refinement onto its true surface (a
        rules = pdef['normals_from']          # few tenths of a millimetre, for macros) only with --full, as render.py's
        if not a.full:                        # "normals_refine": false does for small copies
            rules = [dict(r, refine=0) for r in rules]
        Pr.normals_from(bpy, templates, rules, pdef['origin_mm'], ROOT)
    if not a.full:
        for pname, ob in templates.items():
            ratio = next((r for k, r in LIGHTER.items() if Pr._match(pname, k)), None)
            if ratio is None:
                continue
            bpy.context.scene.collection.objects.link(ob)
            m = ob.modifiers.new('lighter', 'DECIMATE'); m.ratio = ratio
            bpy.context.view_layer.objects.active = ob
            bpy.ops.object.modifier_apply(modifier=m.name)
            bpy.context.scene.collection.objects.unlink(ob)
    shot = {'product': {'def': a.product, 'instances': [{'position': [0, 0, 0], 'rotate_z': 0, 'flavour': f}
                                                         for _, f in TINTS]}}
    objs, part_of = Pr.place(bpy, pdef, templates, shot, ROOT)
    scene = bpy.context.scene
    for i, (tint, flavour) in enumerate(TINTS):
        col = bpy.data.collections.new(f'{a.name} {tint}')
        scene.collection.children.link(col)
        for ob in [o for o in objs if o.get('instance') == i]:
            for c in list(ob.users_collection):
                c.objects.unlink(ob)
            col.objects.link(ob)
            ob.name = f'{a.name} {tint} {part_of.get(ob.name, ob.name).split("#")[0]}'
        col['tint'] = tint; col['flavour'] = flavour
        col['note'] = (f'{a.name} in {tint} ({flavour}): EARF\'s horn loudspeaker in tinted cast acrylic, 1293 mm tall, '
                       'metres, z up, front -y, feet on z = 0. Materials are Cycles (volume absorption in the acrylic).')
        col.asset_mark()
        col.asset_data.description = col['note']
        col.asset_data.tags.new('EARF'); col.asset_data.tags.new(a.name); col.asset_data.tags.new(tint)
        if i:
            bpy.context.view_layer.layer_collection.children[col.name].exclude = True
    for img in bpy.data.images:                   # decals and any textures travel with the file
        if img.source == 'FILE' and not img.packed_file:
            try:
                img.pack()
            except RuntimeError:
                pass
    bpy.context.preferences.filepaths.use_file_compression = True
    bpy.ops.wm.save_as_mainfile(filepath=a.out, compress=True)
    print(a.out, len(objs), 'objects in', len(TINTS), 'collections')


if __name__ == '__main__':
    main()
