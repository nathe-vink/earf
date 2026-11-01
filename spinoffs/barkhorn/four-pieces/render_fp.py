"""Render a four-pieces shot through the studio engine, with the Tropos pair linked from the asset file.

    python3 spinoffs/barkhorn/four-pieces/render_fp.py SHOT.json --out IMG.png [render.py's flags]

The engine (studio/engine/render.py) builds the room, Mantle (a product block), Hemisphere and Core (the earf_moon kit
piece), the lights and the camera from the shot. Tropos comes from spinoffs/barkhorn/asset/tropos.blend, one
collection per tint, its cloth cover a hidden child collection (cover off, the woofer showing): the shot's `tropos`
list, each {"tint": "Poison", "position": [x, y], "rotate_z": deg}, is linked in when the set is built. After the
render, IMG.anchors.json holds each product's label anchor in pixels (bpy_extras.object_utils.world_to_camera_view),
at the rendered size and at 1920 x 1080, from the shot's `anchors` (product name -> a world point on it).
"""
import json, math, os, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT / 'studio' / 'engine'))
ASSET = ROOT / 'spinoffs' / 'barkhorn' / 'asset' / 'tropos.blend'

shot_path = sys.argv[1]
SHOT = json.loads(Path(shot_path).read_text())

import bpy  # noqa: E402,F401
import sets  # noqa: E402
_room = sets.room


def _tropos(bpy):
    # `tropos_asset` / `tropos_prefix`: another Tropos file (2026-11-01: the owner starts with Strata,
    # spinoffs/barkhorn/asset/tropos-strata.blend, collections "Tropos Strata <Tint>", no cover)
    pre = SHOT.get('tropos_prefix', 'Tropos')
    asset = ROOT / SHOT['tropos_asset'] if SHOT.get('tropos_asset') else ASSET
    want = sorted({f"{pre} {t['tint']}" for t in SHOT.get('tropos', [])})
    if not want:
        return
    with bpy.data.libraries.load(str(asset), link=True, assets_only=True) as (src, dst):
        dst.collections = want
    for i, t in enumerate(SHOT['tropos']):
        col = bpy.data.collections[f"{pre} {t['tint']}"]
        for ch in col.children:                       # the cover stays off (hidden in the library; checked here)
            assert ch.hide_render, ch.name
        e = bpy.data.objects.new(f'tropos-{i}', None)
        e.instance_type = 'COLLECTION'; e.instance_collection = col
        x, y = t['position'][:2]
        # `tropos_lift`: the asset's origin at the speaker's base, its plinth below (Strata's final form: 38.5 mm)
        e.location = (x, y, SHOT.get('tropos_lift', 0.0)); e.rotation_euler = (0, 0, math.radians(t.get('rotate_z', 0.0)))
        bpy.context.scene.collection.objects.link(e)


def _tweaks(bpy):
    """The shot's `material_tweaks`: {name prefix: {Principled input: value}}, set on every material whose name starts
    with the prefix (the kit's wool at full sheen read white on a rug seen at a grazing angle)."""
    for pre, ins in (SHOT.get('material_tweaks') or {}).items():
        for m in bpy.data.materials:
            if m.name.startswith(pre) and m.node_tree:
                for n in m.node_tree.nodes:
                    if n.type == 'BSDF_PRINCIPLED':
                        for k, v in ins.items():
                            n.inputs[k].default_value = v
                print('tweaked', m.name, ins)


def _part_tints(bpy):
    """The shot's `part_tints`: [{"material": substring, "parts": regex, "sigma": [r, g, b] 1/m}], each object whose name
    matches `parts` and whose material's name holds `material` gets a copy of that material with its volume absorption
    set to `sigma` (Beer-Lambert by path length, as the engine's clear resin: density = the largest channel, colour =
    1 - sigma / density). For a construction a material can't say by itself: Hemisphere's clear shell over its tinted
    skin (the lamps lane's stock-tint proof, r32-lamps-final 64e96820), all three on one `body` material."""
    import re
    made = {}
    for spec in SHOT.get('part_tints') or []:
        rx = re.compile(spec['parts'])
        sig = spec['sigma']; D = max(max(sig), 1e-6)
        for o in bpy.context.scene.objects:
            if o.type != 'MESH' or not rx.search(o.name):
                continue
            for slot in o.material_slots:
                m = slot.material
                if not m or spec['material'] not in m.name:
                    continue
                key = (m.name, tuple(sig))
                if key not in made:
                    c = m.copy(); c.name = f"{m.name}-{spec.get('label', 'tint')}"
                    for n in c.node_tree.nodes:
                        if n.type == 'VOLUME_ABSORPTION':
                            n.inputs['Density'].default_value = D
                            n.inputs['Color'].default_value = tuple(1.0 - x / D for x in sig) + (1.0,)
                    made[key] = c
                slot.link = 'OBJECT'; slot.material = made[key]
                print('part tint', o.name, '->', made[key].name)


def room(bpy, st, mats):
    r = _room(bpy, st, mats)
    _tropos(bpy)
    _tweaks(bpy)
    _part_tints(bpy)
    return r


sets.room = room

import render  # noqa: E402

sys.argv = [str(ROOT / 'studio' / 'engine' / 'render.py')] + sys.argv[1:]
render.main()

# --- the label anchors -------------------------------------------------------------------------------------------
import bpy  # noqa: E402
from bpy_extras.object_utils import world_to_camera_view  # noqa: E402
from mathutils import Vector  # noqa: E402

out = Path(sys.argv[sys.argv.index('--out') + 1])
sc = bpy.context.scene
W, H = sc.render.resolution_x, sc.render.resolution_y
res = {'image': out.name, 'size': [W, H], 'anchors': {}, 'anchors_1920': {}}
for name, p in (SHOT.get('anchors') or {}).items():
    v = world_to_camera_view(sc, sc.camera, Vector(p))
    res['anchors'][name] = [round(v.x * W, 1), round((1 - v.y) * H, 1)]
    res['anchors_1920'][name] = [round(v.x * 1920, 1), round((1 - v.y) * 1080, 1)]
    res.setdefault('world', {})[name] = p
out.with_suffix('.anchors.json').write_text(json.dumps(res, indent=1) + '\n')
print('anchors', json.dumps(res['anchors_1920']))
