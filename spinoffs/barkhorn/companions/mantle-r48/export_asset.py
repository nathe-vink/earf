"""Mantle Strata, the approved asset for other lanes' scenes (the coordinator, 2026-11-11): one collection per tint,
all eight, taken from the final day set's own scenes (v3_day.py's .blend beside each frame, commit a1240b77) with the
studio stripped (lamps, camera, cards, flags, sweep). Writes spinoffs/barkhorn/asset/mantle-strata.blend and
mantle-strata.manifest.json.

    python3.11 export_asset.py -- <dir of final2 blends> <dir of final blends (Smoke)> <a scratch dir> [<dirs of the final cover blends, comma-separated>]
"""
import bpy, sys, os, json, hashlib
argv = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else sys.argv[1:]
F2, F1, TMP = argv[0], argv[1], argv[2]
COVER = argv[3] if len(argv) > 3 else None   # dirs of the final cover frames' .blends, comma-separated (v3_day.py --cover solid): each tint's cover-* objects with their own material
# THE COVER PER TINT (the owner, 2026-11-16, "stronger sheet"), as mantle_strata_v3.py's COVER_BY_TINT: loading k and
# stock code; the strong four come from their -cover-strong frames
COVER_BY_TINT = {'ember': (1.0, '2423'), 'poison': (1.0, '2092'), 'haze': (1.0, '2287'), 'fog': (1.0, None),
                 'dust': (2.25, None), 'acid': (2.45, None), 'ice': (3.05, None), 'smoke': (4.30, None)}


def cover_blend(t):
    sx = '-cover-strong' if COVER_BY_TINT[t][0] != 1.0 else '-cover'
    for d in COVER.split(','):
        p_ = os.path.join(d, f'mantle-final-day-{t}{sx}.blend')
        if os.path.exists(p_): return p_
    raise FileNotFoundError(f'no {t}{sx} frame in {COVER}')
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.normpath(os.path.join(HERE, '..', '..', 'asset'))
TINTS = ['ember', 'dust', 'acid', 'poison', 'ice', 'haze', 'fog', 'smoke']
STUDIO = lambda o: o.type in ('LIGHT', 'CAMERA') or o.name == 'focus' or o.name == 'sweep' or o.name.startswith(('card-', 'flag-'))
tmp = []
for t in TINTS:
    src = os.path.join(F2 if t != 'smoke' else F1, f'mantle-final-day-{t}.blend')
    bpy.ops.wm.open_mainfile(filepath=src)
    if False:   # since the black hardware (2026-11-11) every tint's frame was re-rendered from the final build
        m = bpy.data.materials['post-satin-black']
        for n in ('platter-hub', 'platter-inserts', 'bushes'):
            o = bpy.data.objects[n]; o.data.materials.clear(); o.data.materials.append(m)
    for n in ('hinge-blocks', 'hinges'):   # gone from the CAD with the lift-off cover (2026-11-15); scenes rendered before it still carry them
        if bpy.data.objects.get(n): bpy.data.objects.remove(bpy.data.objects[n], do_unlink=True)
    for o in [o for o in bpy.data.objects if STUDIO(o)]:
        bpy.data.objects.remove(o, do_unlink=True)
    col = bpy.data.collections.new(f'Mantle Strata {t.capitalize()}')
    bpy.context.scene.collection.children.link(col)
    for o in list(bpy.context.scene.collection.objects):
        col.objects.link(o); bpy.context.scene.collection.objects.unlink(o)
    if COVER:   # the lift-off cover (2026-11-15) as its own collection inside, off in renders by default: earlier pictures rebuild without it
        with bpy.data.libraries.load(cover_blend(t), link=False) as (a_, b_):   # the cover as rendered in its final frame:
            b_.objects = [n for n in a_.objects if n.startswith('cover-')]          # solid for camera rays, the sheet for shadows
        cc = bpy.data.collections.new(f'Mantle Strata {t.capitalize()} Cover'); col.children.link(cc); cc.hide_render = True
        for o in b_.objects:
            cc.objects.link(o); o.hide_render = False
            if o.name != 'cover-feet':   # named by its sheet, so nobody takes it for the thin-sheet test material
                o.material_slots[0].material.name = f'cover-solid-{COVER_BY_TINT[t][0]:.2f}x'
    for o in col.all_objects:
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


man = {'asset': 'mantle-strata.blend', 'source_commit': 'the house-ground scenes (2026-11-20, v3_day.py --house): the arm parked on its rest 20 mm clear of the record, the label blank, the rear plate black nickel with its legends, the deck's top polished, its underside and outer edge satin, the 1 mm chamfer polished (the faces remapped to the signed finish), the cue lift turned with the arm onto its rest, the acrylic passing tinted light to shadow rays (--glass-shadows); built from tiny renders of those scenes, the studio stripped', 'units': 'm, z up, the shelf at z 0',
       'build': 'no light of any kind; base Smoke 2074 solid; every visible piece of hardware satin black (post-satin-black, #18181A, roughness 0.5; the list in black_hardware), bright only the parts in bright_by_necessity; the deck underside satin; a record on the platter; no lid or hinges: the lift-off cover is in its own collection, off by default',
       'edge': 'C: a 1 mm even chamfer on the outer edges of the deck and base (in the CAD), the chamfer polished; the deck\'s outer edge satin, the base\'s diamond-polished, as signed (the owner, 2026-11-11)',
       'cover': 'lift-off, 3 mm cell-cast sheet, 448 x 358 x 100 on four clear 2.2 mm feet; per tint (the owner, 2026-11-16, his words: "stronger sheet") in cover_by_tint; its objects (cover-*) in the child collection "Mantle Strata <Tint> Cover", off in renders by default (collection hide_render): turn it on to show the cover. Its material is the final frames\' own: a Glass BSDF (IOR 1.49) with the sheet\'s Volume Absorption for camera and glossy rays, and on shadow rays the slant-tinted thin sheet with no volume (Light Path, Is Shadow Ray). Render it with glossy and transmission bounces at 128 or more (the polished rims guide light: at 12 they render black) and refractive caustics off, as the finals',
       'cover_by_tint': {t_: {'loading_x_deck_dye': k_, 'sheet': (f'stock TruCast {c_}' if c_ else 'custom cast'), 'frame': f'mantle-final-day-{t_}' + ('-cover-strong' if k_ != 1.0 else '-cover') + '.png'} for t_, (k_, c_) in COVER_BY_TINT.items()},
       'black_hardware': ['arm-puck', 'puck-screw-0', 'puck-screw-1', 'puck-screw-2', 'feet', 'foot-studs', 'pulley',
                          'platter-screws', 'motor-screws', 'bearing-spring', 'rear-hardware', 'arm-axle', 'arm-axle.001',
                          'arm-bias', 'arm-cw', 'hs-screw', 'hs-screw.001', 'hs-washer', 'hs-washer.001', 'cart-screw',
                          'cart-screw.001', 'post-1', 'post-2', 'post-3', 'post-4', 'bearing-housing', 'bearing-nut',
                          'bearing-washer', 'platter-hub', 'platter-inserts', 'bushes'],
       'bright_by_necessity': {'spindle': 'hardened, ground 440C; its tip locates the record and a coat would wear off it',
                               'cart-cantilever': 'the cartridge maker\'s aluminum tube (bought, working)',
                               'cart-pin': 'gold signal pins (bought, contacts)', 'cart-diamond': 'the stylus',
                               'ball': 'the bearing\'s carbide ball, a working surface, hidden in the housing',
                               'thrust-plate': 'the bearing\'s thrust face, working, hidden in the housing'},
       'tints': {}}
for t, p, src in tmp:
    c = bpy.data.collections[f'Mantle Strata {t.capitalize()}']
    parts, mats = [], {}
    for o in sorted(c.all_objects, key=lambda o: o.name):
        ms = [s.material.name for s in o.material_slots if s.material]
        parts.append({'object': o.name, 'type': o.type, 'hidden_render': o.hide_render, 'materials': ms, 'cover': o.name.startswith('cover-')})
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
for t in man['tints']:   # the asset checks itself: every black_hardware part in the satin black, no emitter
    P = {p_['object'].rsplit('.', 1)[0]: p_ for p_ in man['tints'][t]['parts']}
    bad = [n for n in man['black_hardware'] if n in P and not all(m_.startswith('post-satin-black') for m_ in P[n]['materials'])]
    assert not bad and not man['tints'][t]['emitting_materials'], (t, bad)
bpy.ops.file.pack_all()
os.makedirs(OUT, exist_ok=True)
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(OUT, 'mantle-strata.blend'), compress=True)
json.dump(man, open(os.path.join(OUT, 'mantle-strata.manifest.json'), 'w'), indent=1)
print('wrote', OUT, {t: len(man['tints'][t]['parts']) for t in TINTS})
