"""A product block taken whole from an approved .blend asset (2026-11-11: Mantle comes only from r48-mantle-design's
mantle-strata.blend; the engine's own Mantle file, written from the CAD's finishes, still had steel posts, brass bushes
and its lid on).

    {"asset_blend": "studio/assets/cache/mantle/<sha>/mantle-strata.blend", "collection": "Mantle Strata Smoke",
     "manifest": ".../mantle-strata.manifest.json", "tint": "smoke", "forbid": ["brass"],
     "instances": [{"position": [x, y, z], "rotate_z": deg}]}

The collection is appended (real objects, not a link) once per instance under an empty at the instance's place. Before
anything renders, every object is checked against the asset's manifest: the same parts, each with the same materials
and the same render visibility; no material whose name contains a `forbid` word. Any difference stops the build.
"""
import json, math
from pathlib import Path


def _strip(name):
    """Blender appends .001 to a name already taken: the manifest's names are the file's own."""
    base, _, tail = name.rpartition('.')
    return base if tail.isdigit() and len(tail) == 3 and base else name


def place(bpy, blk, root):
    path = Path(root, blk['asset_blend'])
    man = json.load(open(Path(root, blk['manifest']))) if blk.get('manifest') else None
    want = None
    if man:
        want = {p['object']: p for p in man['tints'][blk['tint']]['parts']}
        assert man['tints'][blk['tint']]['collection'] == blk['collection'], 'the collection is not the manifest\'s'
    objs, part_of = [], {}
    for k, inst in enumerate(blk.get('instances', [{}])):
        before = set(bpy.data.objects)
        with bpy.data.libraries.load(str(path), link=False) as (src, dst):
            assert blk['collection'] in src.collections, f"{blk['collection']} not in {path}"
            dst.collections = [blk['collection']]
        col = dst.collections[0]
        new = [o for o in bpy.data.objects if o not in before]
        # the check, against the file's own names (the first copy only: the rest are the same file)
        if want is not None and k == 0:
            got = {}
            for o in new:
                got[_strip(o.name)] = {'type': o.type, 'hidden_render': bool(o.hide_render),
                                       'materials': [_strip(s.material.name) for s in o.material_slots if s.material]}
            bad = []
            for n_, p_ in want.items():
                g = got.get(n_)
                if g is None:
                    bad.append(f'missing {n_}')
                elif g['hidden_render'] != p_['hidden_render'] or sorted(g['materials']) != sorted(p_['materials']):
                    bad.append(f'{n_}: {g} != {p_}')
            bad += [f'extra {n_}' for n_ in got if n_ not in want and got[n_]['type'] == 'MESH']
            for o in new:
                for s in o.material_slots:
                    if s.material and any(w in s.material.name.lower() for w in blk.get('forbid', [])) and not o.hide_render:
                        bad.append(f'forbidden material {s.material.name} on {o.name}')
            if bad:
                raise SystemExit('blendasset: ' + blk['collection'] + ' does not match its manifest: ' + '; '.join(bad[:8]))
            print('blendasset:', blk['collection'], len(want), 'parts match the manifest')
        holder = bpy.data.objects.new(f"{blk['collection']} #{k}", None)
        bpy.context.scene.collection.objects.link(holder)
        bpy.context.scene.collection.children.link(col)
        for o in new:
            if o.parent is None:
                o.parent = holder
        x, y, z = (list(inst.get('position', [0, 0, 0])) + [0, 0, 0])[:3]
        holder.location = (x, y, z); holder.rotation_euler = (0.0, 0.0, math.radians(inst.get('rotate_z', 0.0)))
        for o in new:
            if o.type == 'MESH' and not o.hide_render:
                objs.append(o); part_of[o.name] = _strip(o.name).rsplit('.', 1)[0]
    return objs, part_of
