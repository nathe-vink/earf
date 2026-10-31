"""Tropos as a linkable Blender asset (2026-10-31): the current design, one collection per tint, each marked as an
asset, so another scene can link or append "Tropos Ember" and the rest. The parts, normals and materials are the
render engine's own (studio/engine/product.py: import_model, smooth_parts, normals_from, place), so a linked Tropos
looks as it does in the studio's renders.

    python3.11 spinoffs/barkhorn/asset/make_blend.py [--out spinoffs/barkhorn/asset/tropos.blend]
    python3.11 spinoffs/barkhorn/asset/make_blend.py --design strata --out spinoffs/barkhorn/asset/tropos-strata.blend

Needs the Cloud's render model, spinoffs/barkhorn/out-cloud/render/barkhorn-cloud.glb (written by the Cloud's
fabkit build; not in git), and for Strata the proposals' render model too (spinoffs/barkhorn/variants/render_model.py). Each speaker stands at the origin, its feet on z = 0, its front facing -y, in metres;
the collections are hidden from the view layer except Ember, so the file opens on one speaker.

In another file (bpy):

    with bpy.data.libraries.load('/path/tropos.blend', link=True, assets_only=True) as (src, dst):
        dst.collections = ['Tropos Smoke']
    inst = bpy.data.objects.new('Tropos', None); inst.instance_type = 'COLLECTION'
    inst.instance_collection = bpy.data.collections['Tropos Smoke']; bpy.context.scene.collection.objects.link(inst)

or the Asset Browser, with the file's folder added as an asset library.
"""
import argparse, json, sys
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
COVER = ('cloth-disc', 'disc-frame')
# the designs: each a list of (engine file, parts hidden). Strata (variants/STRATA.md) is the Cloud with its formed
# horn, posts, cloth disc and dyed ring hidden and the proposals' laminated horn, bronze posts and caldera laid on it
STRATA_HIDE = ['cloth-disc', 'horn-throat', 'post-*', 'post-sleeves', 'post-sockets', 'waveguide', 'woofer-ring']
DESIGNS = {'current': [('studio/products/barkhorn-cloud.json', [])],
           'strata': [('studio/products/barkhorn-cloud.json', STRATA_HIDE),
                      ('studio/products/barkhorn-variants.json', ['horn-topo*'])]}
TINTS = [('Ember', 'cloud-red'), ('Dust', 'cloud-orange'), ('Acid', 'cloud-amber'), ('Poison', 'eucalyptus-y2k-green'),
         ('Ice', 'cloud-blue'), ('Haze', 'cloud-violet'), ('Fog', 'birch-fog-clear'), ('Smoke', 'cloud-black')]


def calibrate(pdef, tints):
    """Stock TruCast tints (tints-trucast.json, TINTS.md) in place of the site's: every cabinet part (and Strata's
    caldera) in its code held at 20 mm, Strata's laminated horn in stock 1/2 in held at 12.7 mm; the formed horn keeps
    its deep lot, a custom cast."""
    for t in tints.values():
        m = pdef['flavours'][t['flavour']].setdefault('materials', {})
        m['bark'] = {**m.get('bark', {}), 'deep': t['cabinet_deep'], 'radius': t['cabinet_radius_m'], 'ior': t['ior']}
        if 'horn-strata' in json.dumps(pdef.get('assign', [])):
            m['horn-lot'] = {**m.get('horn-lot', {}), 'deep': t['strata_horn_deep'], 'radius': t['horn_radius_m'],
                             'ior': t['ior']}


def load_product(bpy, Pr, path, hide, full, tints=None):
    """One engine file's parts, lightened, placed once per tint with `hide` left out: (objects, part_of)."""
    pdef = Pr.load_def(path, ROOT)
    if tints:
        calibrate(pdef, tints)
    templates = Pr.import_model(bpy, Path(ROOT, pdef['model']), pdef['origin_mm'], pdef.get('axes', 'gltf'))
    if pdef.get('smooth'):
        Pr.smooth_parts(bpy, templates, pdef['smooth'])
    if pdef.get('normals_from'):              # the shading normals; the waveguide's refinement onto its true surface (a
        rules = pdef['normals_from']          # few tenths of a millimetre, for macros) only with --full, as render.py's
        if not full:                          # "normals_refine": false does for small copies
            rules = [dict(r, refine=0) for r in rules]
        Pr.normals_from(bpy, templates, rules, pdef['origin_mm'], ROOT)
    if not full:
        for pname, ob in templates.items():
            ratio = next((r for k, r in LIGHTER.items() if Pr._match(pname, k)), None)
            if ratio is None or any(Pr._match(pname, h) for h in hide):
                continue
            bpy.context.scene.collection.objects.link(ob)
            m = ob.modifiers.new('lighter', 'DECIMATE'); m.ratio = ratio
            bpy.context.view_layer.objects.active = ob
            bpy.ops.object.modifier_apply(modifier=m.name)
            bpy.context.scene.collection.objects.unlink(ob)
    shot = {'product': {'def': path, 'instances': [{'position': [0, 0, 0], 'rotate_z': 0, 'flavour': f, 'hide': hide}
                                                    for _, f in TINTS]}}
    return Pr.place(bpy, pdef, templates, shot, ROOT)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--out', default=str(HERE / 'tropos.blend'))
    ap.add_argument('--design', default='current', choices=sorted(DESIGNS))
    ap.add_argument('--name', default=None, help='the collections\' prefix (default Tropos, or Tropos Strata)')
    ap.add_argument('--full', action='store_true', help='keep every triangle (no LIGHTER)')
    ap.add_argument('--tints', default='site', choices=['site', 'trucast'],
                    help="the site's tints (default) or stock TruCast sheet's (tints-trucast.json, TINTS.md)")
    a = ap.parse_args()
    import bpy
    import product as Pr

    bpy.ops.wm.read_factory_settings(use_empty=True)
    a.name = a.name or ('Tropos' if a.design == 'current' else f'Tropos {a.design.title()}')
    objs, part_of = [], {}
    for prod_path, hide in DESIGNS[a.design]:
        tints = json.load(open(HERE / 'tints-trucast.json')) if a.tints == 'trucast' else None
        o, p = load_product(bpy, Pr, prod_path, hide, a.full, tints)
        objs += o; part_of.update(p)
    scene = bpy.context.scene
    for i, (tint, flavour) in enumerate(TINTS):
        col = bpy.data.collections.new(f'{a.name} {tint}')
        scene.collection.children.link(col)
        for ob in [o for o in objs if o.get('instance') == i]:
            for c in list(ob.users_collection):
                c.objects.unlink(ob)
            col.objects.link(ob)
            ob.name = f'{a.name} {tint} {part_of.get(ob.name, ob.name).split("#")[0]}'
        # the cover (the cloth disc on its frame) in a child collection of its own, hidden by default: EARF shows Tropos
        # with its cover off (the owner, 2026-10-31); show it with `hide_render = hide_viewport = False`
        cover = bpy.data.collections.new(f'{a.name} {tint} cover')
        col.children.link(cover)
        for ob in [o for o in col.objects if any(o.name.endswith(' ' + k) or (' ' + k + '.') in o.name for k in COVER)]:
            col.objects.unlink(ob); cover.objects.link(ob)
        cover.hide_render = True; cover.hide_viewport = True
        if not cover.objects:                     # Strata has no cover: its woofer sits in the caldera
            col.children.unlink(cover); bpy.data.collections.remove(cover)
        col['tint'] = tint; col['flavour'] = flavour; col['tints'] = a.tints
        col['note'] = (f'{a.name} in {tint} ({flavour}): EARF\'s horn loudspeaker in tinted cast acrylic, 1293 mm tall, '
                       'metres, z up, front -y, feet on z = 0. Materials are Cycles (volume absorption in the acrylic).'
                     + ('' if a.design == 'current' else f' The {a.design.title()} proposal (spinoffs/barkhorn/variants/'
                                                         f'{a.design.upper()}.md), not the design on sale.'))
        col.asset_mark()
        col.asset_data.description = col['note']
        for t in ['EARF', 'Tropos', tint] + ([a.design.title(), 'proposal'] if a.design != 'current' else []):
            col.asset_data.tags.new(t)
        if i:
            bpy.context.view_layer.layer_collection.children[col.name].exclude = True
    keep = set(objs)                              # the templates and the parts a design hides stay out of the file
    for ob in [o for o in bpy.data.objects if o not in keep]:
        bpy.data.objects.remove(ob, do_unlink=True)
    for me in [m for m in bpy.data.meshes if m.users == 0]:
        bpy.data.meshes.remove(me)
    for img in bpy.data.images:                   # decals and any textures travel with the file
        if img.source == 'FILE' and not img.packed_file:
            try:
                img.pack()
            except RuntimeError:
                pass
    bpy.context.preferences.filepaths.use_file_compression = True
    bpy.context.preferences.filepaths.save_version = 0          # no .blend1 backup beside it
    bpy.ops.wm.save_as_mainfile(filepath=a.out, compress=True)
    print(a.out, len(objs), 'objects in', len(TINTS), 'collections')


if __name__ == '__main__':
    main()
