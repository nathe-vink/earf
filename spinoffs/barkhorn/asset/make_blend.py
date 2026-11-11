"""Tropos as a linkable Blender asset (2026-10-31): the current design, one collection per tint, each marked as an
asset, so another scene can link or append "Tropos Ember" and the rest. The parts, normals and materials are the
render engine's own (studio/engine/product.py: import_model, smooth_parts, normals_from, place), so a linked Tropos
looks as it does in the studio's renders.

    python3.11 spinoffs/barkhorn/asset/make_blend.py [--out spinoffs/barkhorn/asset/tropos.blend]
    python3.11 spinoffs/barkhorn/asset/make_blend.py --design strata --out spinoffs/barkhorn/asset/tropos-strata.blend
    python3.11 spinoffs/barkhorn/asset/make_blend.py --design site --name 'Tropos Strata' --out spinoffs/barkhorn/asset/tropos-strata.blend \
        --manifest spinoffs/barkhorn/asset/tropos-strata.manifest.json      (the approved build, since 2026-11-11)

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
           # and, for a speaker seen across a landscape, the lining's voile webs. The horn is never collapsed (2026-11-03):
           # horn A is clear acrylic with an absorbing volume, and a collapsed mesh can open it, so light would leak out
           'lining-*-web': 0.3}
MIN_FACES = 2000                          # below this a part is never collapsed
COVER = ('cloth-disc', 'disc-frame')
# the designs: each a list of (engine file, parts hidden). Strata (variants/STRATA.md) is the Cloud with its formed
# horn, posts, cloth disc and dyed ring hidden and the proposals' laminated horn, bronze posts and caldera laid on it
STRATA_HIDE = ['cloth-disc', 'horn-throat', 'post-*', 'post-sleeves', 'post-sockets', 'waveguide', 'woofer-ring', 'feet-*']
# Strata stands on base A, the stepped plinth lit from underneath (the owner, 2026-11-01): the variants' options, and
# everything lifted by the plinth's height so its feet stand on z = 0 (variants/BASES.md)
STRATA_OPTIONS, STRATA_LIFT = ['Plinth', 'Plinth uplight'], 0.0385   # the uplight since 2026-11-02 (the owner: the light goes up)
DESIGNS = {'current': [('studio/products/barkhorn-cloud.json', [])],
           'strata': [('studio/products/barkhorn-cloud.json', STRATA_HIDE),
                      ('studio/products/barkhorn-variants.json', ['horn-topo*'])]}
# the owner (2026-11-01): "I love the stepping in the loudspeaker but not sure about the horn. Would like to keep both
# options for the horn but happy to start with the stepped version": Strata's cabinet and caldera with either horn, on
# Strata's bronze posts. --horn smooth puts the formed horn (the Cloud's waveguide and throat) on them instead
HORNS = {'stepped': {}, 'smooth': {'studio/products/barkhorn-cloud.json': ['waveguide', 'horn-throat'],
                                   'studio/products/barkhorn-variants.json': ['horn-strata']}}
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


def load_product(bpy, Pr, path, hide, full, tints=None, options=(), lift=0.0, materials=None, flavours=None):
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
            # a mesh already light is left whole: collapsing lining-top-3-web (a 48-face box with the top rib's notch;
            # the other webs are quilted, 15 to 35 thousand faces) broke its faces into a pale wedge (2026-11-01, README.md)
            if ratio is None or any(Pr._match(pname, h) for h in hide) or len(ob.data.polygons) < MIN_FACES:
                continue
            bpy.context.scene.collection.objects.link(ob)
            m = ob.modifiers.new('lighter', 'DECIMATE'); m.ratio = ratio
            bpy.context.view_layer.objects.active = ob
            bpy.ops.object.modifier_apply(modifier=m.name)
            bpy.context.scene.collection.objects.unlink(ob)
    fls = flavours or [f for _, f in TINTS]
    shot = {'materials': materials or {},
            'product': {'def': path, 'instances': [{'position': [0, 0, lift], 'rotate_z': 0, 'flavour': f, 'hide': hide,
                                                     'options': list(options)} for f in fls]}}
    return Pr.place(bpy, pdef, templates, shot, ROOT)


def site_blocks():
    """The approved build (the coordinator, 2026-11-11 15:05): each tint exactly as rollout.py builds the site's tall
    front, shots.site('front-off-tall', tint) with TROPOS_BASE=A and TROPOS_HORN=polished: base A on its own swivel feet
    (feet-base, feet-stem), the line's tints and linings (Smoke in its grey 50 %, black lining), the polished horn, the
    black rods, no plinth and no light. Returns [(product file, hide, options, flavours by TINTS order, materials)], each
    checked identical across the eight tints but for the flavour."""
    import os
    os.environ['TROPOS_BASE'] = 'A'; os.environ['TROPOS_HORN'] = 'polished'
    sys.path.insert(0, str(ROOT / 'spinoffs' / 'barkhorn' / 'campaign'))
    import shots
    assert shots.ROLLOUT == {'base': 'A', 'horn': 'polished'}, shots.ROLLOUT
    key = {f: t for t, (f, _) in shots.SITE_TINTS.items()}
    refs = [shots.site('front-off-tall', key[f]) for _, f in TINTS]
    out = []
    for b, blk in enumerate(refs[0]['products']):
        i0 = blk['instances'][0]
        hide, opts = sorted(i0.get('hide', [])), list(i0.get('options') or [])
        fls = []
        for r in refs:
            bb = r['products'][b]; ii = bb['instances'][0]
            assert bb['def'] == blk['def'] and sorted(ii.get('hide', [])) == hide and list(ii.get('options') or []) == opts
            assert r['materials'] == refs[0]['materials'], 'the material overrides differ between tints'
            fls.append(ii.get('flavour', bb.get('flavour')))
        out.append((blk['def'], hide, opts, fls, refs[0]['materials']))
    return out


def manifest(bpy, objs, path):
    """Per tint: its parts and each material's key values, for another lane to assert its scenes against (as
    shots._approved does): base colour, roughness, metallic, transmission, IOR, and any volume's colour and density."""
    def val(n, k):
        i = n.inputs.get(k)
        if i is None or i.is_linked:
            return None
        v = i.default_value
        return [round(x, 4) for x in v][:3] if hasattr(v, '__len__') else round(float(v), 4)
    out = {}
    for i, (tint, flavour) in enumerate(TINTS):
        parts, mats = {}, {}
        for o in [o for o in objs if o.get('instance') == i and o.type == 'MESH']:
            part = o.name.split(f' {tint} ', 1)[-1]
            parts[part] = sorted({s.material.name for s in o.material_slots if s.material})
            for s_ in o.material_slots:
                m = s_.material
                if not m or m.name in mats or not m.use_nodes:
                    continue
                e = {}
                for n in m.node_tree.nodes:
                    if n.type == 'BSDF_PRINCIPLED':
                        e.update({k: val(n, k) for k in ('Base Color', 'Roughness', 'Metallic', 'Transmission Weight', 'IOR', 'Emission Strength')})
                    elif n.type in ('VOLUME_ABSORPTION', 'PRINCIPLED_VOLUME'):
                        e.update({'volume ' + k: val(n, k) for k in ('Color', 'Density')})
                mats[m.name] = e
        cloud = json.load(open(ROOT / 'studio' / 'products' / 'barkhorn-cloud.json'))
        lin = {**cloud['materials'].get('lining', {}), **cloud['flavours'][flavour].get('materials', {}).get('lining', {})}
        out[tint] = {'flavour': flavour, 'lining_color': lin.get('color'),    # (the lining's colour runs through nodes: from its file)
                     'parts': dict(sorted(parts.items())), 'materials': dict(sorted(mats.items()))}
    json.dump(out, open(path, 'w'), indent=1)
    print('manifest:', path)


GLOW_DAY, GLOW_DUSK = 20.0, 40.0


def plinth_glow(bpy, objs):
    """The plinth light's strength as one setting a shot can change (the coordinator, 2026-11-01: 20 by day, 40 at dusk):
    every glowing material reads a custom property `glow` from the object that instances the collection (a linked
    collection's empty) if it has one, else from the strip object itself (set to GLOW_DAY here). So: link a tint's
    collection, add a custom property `glow` = 40.0 to its instance empty for dusk; nothing to make local."""
    mats = {s.material for o in objs if o.type == 'MESH' for s in o.material_slots
            if s.material and s.material.use_nodes and any(n.type == 'BSDF_PRINCIPLED' and n.inputs['Emission Strength'].default_value > 0
                                                          and not n.inputs['Emission Strength'].is_linked for n in s.material.node_tree.nodes)}
    for m in mats:
        nt = m.node_tree
        bsdf = next(n for n in nt.nodes if n.type == 'BSDF_PRINCIPLED' and n.inputs['Emission Strength'].default_value > 0)
        a_obj = nt.nodes.new('ShaderNodeAttribute'); a_obj.attribute_type = 'OBJECT'; a_obj.attribute_name = 'glow'
        a_ins = nt.nodes.new('ShaderNodeAttribute'); a_ins.attribute_type = 'INSTANCER'; a_ins.attribute_name = 'glow'
        gt = nt.nodes.new('ShaderNodeMath'); gt.operation = 'GREATER_THAN'; gt.inputs[1].default_value = 0.0
        sub = nt.nodes.new('ShaderNodeMath'); sub.operation = 'SUBTRACT'
        mad = nt.nodes.new('ShaderNodeMath'); mad.operation = 'MULTIPLY_ADD'      # obj + (inst > 0) * (inst - obj)
        nt.links.new(a_ins.outputs['Fac'], gt.inputs[0])
        nt.links.new(a_ins.outputs['Fac'], sub.inputs[0]); nt.links.new(a_obj.outputs['Fac'], sub.inputs[1])
        nt.links.new(gt.outputs[0], mad.inputs[0]); nt.links.new(sub.outputs[0], mad.inputs[1]); nt.links.new(a_obj.outputs['Fac'], mad.inputs[2])
        nt.links.new(mad.outputs[0], bsdf.inputs['Emission Strength'])
        m['glow_note'] = f'emission = the instancer\'s `glow` if set, else the object\'s ({GLOW_DAY:g} day, {GLOW_DUSK:g} dusk)'
    for o in objs:
        if o.type == 'MESH' and any(s.material in mats for s in o.material_slots):
            o['glow'] = GLOW_DAY
    print('plinth glow:', len(mats), 'materials,', sum(1 for o in objs if 'glow' in o), 'objects')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--out', default=str(HERE / 'tropos.blend'))
    ap.add_argument('--design', default='current', choices=sorted(DESIGNS) + ['site'],
                    help="'site': the approved build, rollout's own site('front-off-tall', tint) (since 2026-11-11)")
    ap.add_argument('--manifest', default=None, help='write the per-tint parts and materials manifest here (JSON)')
    ap.add_argument('--name', default=None, help='the collections\' prefix (default Tropos, Tropos Strata, or Tropos Strata Stepped)')
    ap.add_argument('--horn', default='smooth', choices=sorted(HORNS), help='Strata\'s horn: smooth (the owner\'s pick, 2026-11-03: "Horn: A, smooth"; polished since 15:14) or stepped (the alternative)')
    ap.add_argument('--full', action='store_true', help='keep every triangle (no LIGHTER)')
    ap.add_argument('--tints', default='line', choices=['line', 'site', 'trucast'],
                    help="the line's own (default: the product files as product.py writes them, colors F since "
                         "2026-11-01, TINTS.md), or the old recalibrations: 'site' (the files untouched before the "
                         "stock tints were the line's) and 'trucast' (plain stock sheet, overwriting F and the deep horns)")
    a = ap.parse_args()
    import bpy
    import product as Pr

    bpy.ops.wm.read_factory_settings(use_empty=True)
    a.name = a.name or ('Tropos' if a.design == 'current' else f'Tropos {a.design.title()}'
                        + (' Stepped' if a.horn == 'stepped' else ''))   # the owner's horn (smooth) keeps the plain name
    objs, part_of = [], {}
    if a.design == 'site':
        a.name = 'Tropos Strata' if a.name == 'Tropos Site' else a.name
        for prod_path, hide, opts, fls, mats in site_blocks():
            o, p = load_product(bpy, Pr, prod_path, hide, a.full, options=opts, materials=mats, flavours=fls)
            objs += o; part_of.update(p)
    for prod_path, hide in ([] if a.design == 'site' else DESIGNS[a.design]):
        if a.design != 'current':                 # the smooth horn: its parts shown, the stepped one hidden
            unhide = HORNS[a.horn].get('studio/products/barkhorn-cloud.json', []) if 'cloud' in prod_path else []
            hide = [h for h in hide if h not in unhide] + (HORNS[a.horn].get(prod_path, []) if 'variants' in prod_path else [])
        tints = json.load(open(HERE / 'tints-trucast.json')) if a.tints == 'trucast' else None
        st = a.design == 'strata'
        o, p = load_product(bpy, Pr, prod_path, hide, a.full, tints,
                            options=STRATA_OPTIONS if st and 'variants' in prod_path else (),
                            lift=STRATA_LIFT if st else 0.0)
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
                     + (' The approved build (rollout.py, site front-off-tall): base A on its swivel feet, the polished horn, '
                        'black rods, no plinth, no light.' if a.design == 'site' else '')
                     + ('' if a.design in ('current', 'site') else f' {a.design.title()} (spinoffs/barkhorn/variants/{a.design.upper()}.md, '
                        f'adopted by the owner 2026-11-01) with the {a.horn} horn'
                        + (' (the lead version).' if a.horn == 'stepped' else ' (the option).')))
        col.asset_mark()
        col.asset_data.description = col['note']
        for t in ['EARF', 'Tropos', tint] + ([a.design.title(), f'{a.horn} horn'] if a.design not in ('current', 'site') else ['approved', 'base A']):
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
    plinth_glow(bpy, objs)
    if a.manifest:
        manifest(bpy, objs, a.manifest)
    bpy.context.preferences.filepaths.use_file_compression = True
    bpy.context.preferences.filepaths.save_version = 0          # no .blend1 backup beside it
    bpy.ops.wm.save_as_mainfile(filepath=a.out, compress=True)
    print(a.out, len(objs), 'objects in', len(TINTS), 'collections')


if __name__ == '__main__':
    main()
