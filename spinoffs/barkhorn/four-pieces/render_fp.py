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
    want = sorted({f"Tropos {t['tint']}" for t in SHOT.get('tropos', [])})
    if not want:
        return
    with bpy.data.libraries.load(str(ASSET), link=True, assets_only=True) as (src, dst):
        dst.collections = want
    for i, t in enumerate(SHOT['tropos']):
        col = bpy.data.collections[f"Tropos {t['tint']}"]
        for ch in col.children:                       # the cover stays off (hidden in the library; checked here)
            assert ch.hide_render, ch.name
        e = bpy.data.objects.new(f'tropos-{i}', None)
        e.instance_type = 'COLLECTION'; e.instance_collection = col
        x, y = t['position'][:2]
        e.location = (x, y, 0.0); e.rotation_euler = (0, 0, math.radians(t.get('rotate_z', 0.0)))
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


def room(bpy, st, mats):
    r = _room(bpy, st, mats)
    _tropos(bpy)
    _tweaks(bpy)
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
