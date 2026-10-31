"""Planet EARF, round 42: the shop wall in the rendered room, as a kit `ext` piece by path (built last).

    {"kind": "kit", "shape": "ext", "path": "spinoffs/barkhorn/planet/r42/kit42.py", "fn": "shopwall", ...}

The left wall by the door, between the street glass and the back bar (x 0.45 to 2.35 in the round 36 frame):
blackened-steel uprights, four oiled oak shelves 360 deep, a warm LED strip under each shelf's front edge, records
in the bottom bay, a price card at every piece, and a low oak plinth for a Tropos beside it. The pieces themselves
(Core, Hemisphere, Mantle, Tropos, the coins) are the products' own models, placed by the shot (r42_shots.py).
"""
import math, random


def _lin(h):
    h = h.lstrip('#'); c = [int(h[i:i + 2], 16) / 255.0 for i in (0, 2, 4)]
    return tuple(((v + 0.055) / 1.055) ** 2.4 if v > 0.04045 else v / 12.92 for v in c) + (1.0,)


def _mat(bpy, name, col, rough=0.5, metal=0.0, emit=None, strength=0.0, coat=0.0):
    m = bpy.data.materials.get(name)
    if m:
        return m
    m = bpy.data.materials.new(name); m.use_nodes = True
    b = m.node_tree.nodes['Principled BSDF']
    b.inputs['Base Color'].default_value = _lin(col); b.inputs['Roughness'].default_value = rough
    b.inputs['Metallic'].default_value = metal
    if coat:
        b.inputs['Coat Weight'].default_value = coat
    if emit:
        b.inputs['Emission Color'].default_value = _lin(emit); b.inputs['Emission Strength'].default_value = strength
    return m


def _box(bpy, name, x0, y0, z0, x1, y1, z1, m, bevel=0.0):
    import bmesh
    me = bpy.data.meshes.new(name); bm = bmesh.new()
    bmesh.ops.create_cube(bm, size=1.0)
    for v in bm.verts:
        v.co.x = (x0 + x1) / 2 + v.co.x * (x1 - x0); v.co.y = (y0 + y1) / 2 + v.co.y * (y1 - y0)
        v.co.z = (z0 + z1) / 2 + v.co.z * (z1 - z0)
    if bevel:
        bmesh.ops.bevel(bm, geom=list(bm.edges), offset=bevel, segments=2, affect='EDGES')
    bm.to_mesh(me); bm.free()
    ob = bpy.data.objects.new(name, me); bpy.context.scene.collection.objects.link(ob)
    me.materials.append(m)
    return ob


def shopwall(bpy, name, p, kit):
    x0, x1 = p.get('x', [0.45, 2.35])
    yw = p.get('wall', 6.10)                       # the wall's face
    d = p.get('depth', 0.36)
    shelves = p.get('shelves', [0.32, 0.80, 1.28, 1.70])
    t = 0.030
    steel = _mat(bpy, 'r42-steel', '#1c1b1a', 0.45, 0.85)
    oak = _mat(bpy, 'r42-oak', '#5b4330', 0.42, coat=0.15)
    back = _mat(bpy, 'r42-back', '#2a2420', 0.85)
    led = _mat(bpy, 'r42-led', '#ffd29a', 0.5, emit='#ffb565', strength=p.get('led', 9.0))
    card = _mat(bpy, 'r42-card', '#efe9de', 0.8)
    objs = []
    objs.append(_box(bpy, f'{name}-back', x0, yw - 0.012, 0.0, x1, yw - 0.002, shelves[-1] + 0.12, back))
    for i, xu in enumerate([x0, (x0 + x1) / 2, x1]):
        objs.append(_box(bpy, f'{name}-upright{i}', xu - 0.02, yw - d, 0.0, xu + 0.02, yw - 0.012, shelves[-1] + 0.12, steel))
    for k, z in enumerate(shelves):
        objs.append(_box(bpy, f'{name}-shelf{k}', x0 + 0.02, yw - d, z - t, x1 - 0.02, yw - 0.012, z, oak, bevel=0.003))
        # the LED strip under the shelf's front edge, facing down and back (no source seen from a seat)
        if k:
            objs.append(_box(bpy, f'{name}-led{k}', x0 + 0.04, yw - d + 0.03, z - t - 0.006, x1 - 0.04, yw - d + 0.045,
                             z - t - 0.001, led))
    # the records, in the bottom bay of the right half: sleeves on edge, spines out
    rnd = random.Random(p.get('seed', 42))
    sleeve_cols = ['#1d1b19', '#c9bfae', '#8a2f22', '#2f4a5e', '#d8c27a', '#3c3a36', '#e7e2d8', '#6b4a2e', '#24302a']
    xs = (x0 + x1) / 2 + 0.05
    z = shelves[0]
    while xs < x1 - 0.06:
        w = 0.004 + rnd.random() * 0.004
        lean = 0.0
        c = rnd.choice(sleeve_cols)
        objs.append(_box(bpy, f'{name}-lp', xs, yw - 0.33, z, xs + w, yw - 0.02, z + 0.312, _mat(bpy, f'r42-lp-{c}', c, 0.7)))
        xs += w + 0.0015
    # three sleeves face out on the top shelf
    for i, c in enumerate(p.get('covers', ['#c8452f', '#e9e4d8', '#1d1b19'])):
        xc = x0 + 0.20 + i * 0.36
        ob = _box(bpy, f'{name}-cover{i}', xc, yw - 0.06, shelves[-1], xc + 0.315, yw - 0.055, shelves[-1] + 0.315,
                  _mat(bpy, f'r42-cover{i}', c, 0.6))
        ob.rotation_euler[0] = math.radians(-8)
        objs.append(ob)
    # price cards, leaning at the shelf fronts
    for (cx, cz) in p.get('cards', []):
        cw, ch = p.get('card_size', [0.06, 0.042])
        ob = _box(bpy, f'{name}-card', cx - cw / 2, yw - d + 0.015, cz, cx + cw / 2, yw - d + 0.017, cz + ch, card)
        ob.rotation_euler[0] = math.radians(-14)
        objs.append(ob)
    # the plinth for a Tropos beside the shelves
    if p.get('plinth'):
        px, py, pw, pd, ph = p['plinth']
        objs.append(_box(bpy, f'{name}-plinth', px - pw / 2, py - pd / 2, 0.0, px + pw / 2, py + pd / 2, ph, oak, bevel=0.006))
    return objs


def flatten(bpy, name, p, kit):
    """A scanned finish's stains calmed (the round 42 critics: "blotchy dark puddles", "oval blobs that read as stains"):
    a Bright/Contrast node between the scan's colour and the BSDF, its contrast `contrast` (negative flattens), for every
    material whose name holds `match`."""
    for m in [m for m in bpy.data.materials if p.get('match', 'Concrete044A') in m.name and m.use_nodes and not m.get('r42flat')]:
        b = next((n for n in m.node_tree.nodes if n.type == 'BSDF_PRINCIPLED'), None)
        if not b or not b.inputs['Base Color'].is_linked:
            continue
        m['r42flat'] = 1
        nt = m.node_tree
        src = b.inputs['Base Color'].links[0].from_socket
        bc = nt.nodes.new('ShaderNodeBrightContrast')
        c = p.get('contrast', -0.35)
        # out = (1 + c) x + bright - c / 2: hold the scan's mean (`mean`, linear) where it is, pull the stains toward it
        bc.inputs['Bright'].default_value = c * (0.5 - p.get('mean', 0.15))
        bc.inputs['Contrast'].default_value = c
        nt.links.new(src, bc.inputs['Color']); nt.links.new(bc.outputs['Color'], b.inputs['Base Color'])
    return []
