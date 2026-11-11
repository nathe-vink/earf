"""Mantle Strata, the approved asset for other lanes' scenes (the coordinator, 2026-11-11): one collection per tint,
all eight, taken from the final day set's own scenes (v3_day.py's .blend beside each frame, commit a1240b77) with the
studio stripped (lamps, camera, cards, flags, sweep). Writes spinoffs/barkhorn/asset/mantle-strata.blend and
mantle-strata.manifest.json.

    python3.11 export_asset.py -- <dir of final2 blends> <dir of final blends (Smoke)> <a scratch dir>
"""
import bpy, sys, os, json, hashlib
argv = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else sys.argv[1:]
F2, F1, TMP = argv[0], argv[1], argv[2]
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.normpath(os.path.join(HERE, '..', '..', 'asset'))
TINTS = ['ember', 'dust', 'acid', 'poison', 'ice', 'haze', 'fog', 'smoke']
STUDIO = lambda o: o.type in ('LIGHT', 'CAMERA') or o.name == 'focus' or o.name == 'sweep' or o.name.startswith(('card-', 'flag-'))
tmp = []
for t in TINTS:
    src = os.path.join(F2 if t != 'smoke' else F1, f'mantle-final-day-{t}.blend')
    bpy.ops.wm.open_mainfile(filepath=src)
    if t == 'smoke':   # its frame was not re-rendered (the hub did not show); the asset carries the final build: the hub black
        m = bpy.data.materials['post-satin-black']
        for n in ('platter-hub', 'platter-inserts', 'bushes'):
            o = bpy.data.objects[n]; o.data.materials.clear(); o.data.materials.append(m)
    for o in [o for o in bpy.data.objects if STUDIO(o)]:
        bpy.data.objects.remove(o, do_unlink=True)
    col = bpy.data.collections.new(f'Mantle Strata {t.capitalize()}')
    bpy.context.scene.collection.children.link(col)
    for o in list(bpy.context.scene.collection.objects):
        col.objects.link(o); bpy.context.scene.collection.objects.unlink(o)
    for o in col.objects:
        o.name = f'{o.name}.{t}'
        if o.data is not None and hasattr(o.data, 'name'): o.data.name = f'{o.data.name}.{t}'
    for m in bpy.data.materials:
        if not m.name.endswith('.' + t): m.name = f'{m.name}.{t}'
    bpy.ops.outliner.orphans_purge(do_recursive=True)
    p = os.path.join(TMP, f'mantle-asset-{t}.blend'); bpy.ops.wm.save_as_mainfile(filepath=p, copy=True); tmp.append((t, p, src))

bpy.ops.wm.read_factory_settings(use_empty=True)
for t, p, _ in tmp:
    with bpy.data.libraries.load(p, link=False) as (a, b):
        b.collections = [f'Mantle Strata {t.capitalize()}']
    for c in b.collections:
        bpy.context.scene.collection.children.link(c)


def val(sock):
    if sock is None: return None
    if sock.is_linked:
        n = sock.links[0].from_node; d = {'linked_from': n.type}
        if n.type == 'VALTORGB':
            d['stops'] = [[round(e.position, 4), [round(x, 5) for x in e.color]] for e in n.color_ramp.elements]
        for i in n.inputs:
            if not i.is_linked and hasattr(i, 'default_value') and i.enabled:
                try: d[i.name] = [round(x, 5) for x in i.default_value]
                except TypeError: d[i.name] = round(i.default_value, 5)
            elif i.is_linked and i.type == 'RGBA':
                d[i.name] = val(i)
        return d
    v = sock.default_value
    try: return [round(x, 5) for x in v]
    except TypeError: return round(v, 5)


man = {'asset': 'mantle-strata.blend', 'source_commit': 'a1240b77 (frames), 450064b8 (model)', 'units': 'm, z up, the shelf at z 0',
       'build': 'no light of any kind; base Smoke 2074 solid; posts, bearing housing, nut, washer, platter hub, inserts and bushes satin black (post-satin-black, #18181A); the deck underside satin; a record on the platter; the lid and hinges present but hidden from render, as in the frames',
       'tints': {}}
for t, p, src in tmp:
    c = bpy.data.collections[f'Mantle Strata {t.capitalize()}']
    parts, mats = [], {}
    for o in sorted(c.objects, key=lambda o: o.name):
        ms = [s.material.name for s in o.material_slots if s.material]
        parts.append({'object': o.name, 'type': o.type, 'hidden_render': o.hide_render, 'materials': ms})
        for mn in ms:
            if mn in mats: continue
            m = bpy.data.materials[mn]; e = {}
            if m.node_tree:
                for n in m.node_tree.nodes:
                    if n.type == 'BSDF_PRINCIPLED' and 'base_color' not in e:
                        e.update(base_color=val(n.inputs['Base Color']), roughness=val(n.inputs['Roughness']),
                                 transmission=val(n.inputs['Transmission Weight']), ior=val(n.inputs['IOR']),
                                 metallic=val(n.inputs['Metallic']))
                    if n.type == 'VOLUME_ABSORPTION':
                        e.update(volume_color=val(n.inputs['Color']), volume_density=val(n.inputs['Density']))
                    if n.type == 'PRINCIPLED_VOLUME':
                        e.update(volume_color=val(n.inputs['Color']), volume_density=val(n.inputs['Density']))
                    if n.type == 'EMISSION' and n.inputs['Strength'].default_value > 0:
                        e['EMISSION'] = val(n.inputs['Strength'])
            mats[mn] = e
    man['tints'][t] = {'collection': c.name, 'scene_source': os.path.basename(src), 'parts': parts, 'materials': mats,
                       'emitting_materials': [k for k, v in mats.items() if 'EMISSION' in v]}
bpy.ops.file.pack_all()
os.makedirs(OUT, exist_ok=True)
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(OUT, 'mantle-strata.blend'), compress=True)
json.dump(man, open(os.path.join(OUT, 'mantle-strata.manifest.json'), 'w'), indent=1)
print('wrote', OUT, {t: len(man['tints'][t]['parts']) for t in TINTS})
