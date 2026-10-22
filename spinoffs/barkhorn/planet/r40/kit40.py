"""Planet EARF, round 40: the pieces round 40 adds to round 39's room, as kit `ext` pieces by path.

    {"kind": "kit", "shape": "ext", "path": "spinoffs/barkhorn/planet/r40/kit40.py", "fn": "figures", ...}
    {"kind": "kit", "shape": "ext", "path": "spinoffs/barkhorn/planet/r40/kit40.py", "fn": "boards", ...}

- `figures`: people, as a long exposure records them (the owner, 2026-10-22: "Bar pictures: blurred figures allowed").
  Each figure is three bodies (the trunk and legs, the arms, the head), each a skinned skeleton smoothed, each moving
  its own way during the shutter: a seated guest's trunk barely, the head and the hands more, a bartender's pouring
  arm a long arc. Cycles' motion blur draws the movement, so no face is ever sharp. Poses: `stool` (at the counter,
  elbows on the zinc), `chair` (at a table), `bench` (on the banquette), `tub` (in a tub chair, leaning back),
  `pour` (behind the counter, a bottle tipped over a glass), `decks` (at the decks, head down, a hand on a record).
- `boards`: every board of the room's fir its own piece of the scan and its own tone (the p4 critics: "one repeated
  streaky texture with identical tone"): each loose part of a fir mesh gets a random value, which offsets where it
  samples the scan and shifts its tone and hue a little.

Every list is in world metres; anything not listed is not built.
"""
import math, os, random, sys

import bmesh
from mathutils import Euler, Matrix, Vector

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(HERE))))
KX = os.path.join(ROOT, 'studio', 'engine', 'kit_ext')
if KX not in sys.path:
    sys.path.insert(0, KX)
import planet_r37 as K37                                             # noqa: E402

K = K37.K
LK = K.LK
_M = {}

# --- the poses: joints in the figure's own frame (x forward, y to its left, z up from the floor), metres -------------
# each chain is [(joint, radius), ...] skinned as one tube; `head` is the skull's centre; `hands` the palms


def _pose(kind, h):
    """The trunk chains, the arm chains, the head's centre and the hands, for a seat height `h` (or a floor)."""
    if kind == 'stool':        # on a bar stool, leaning in, both elbows on the zinc
        trunk = [[((-.02, 0, h + .10), .15), ((-.03, 0, h + .32), .14), ((.03, 0, h + .50), .165), ((.09, 0, h + .66), .06)]]
        for s in (1, -1):
            trunk.append([((-.02, s * .09, h + .10), .095), ((.40, s * .11, h + .06), .07), ((.40, s * .12, .32), .05), ((.52, s * .12, .29), .04)])
        arms = [[((.04, s * .19, h + .58), .065), ((.36, s * .22, 1.10), .05), ((.50, s * .07, 1.13), .04)] for s in (1, -1)]
        head = (.13, 0, h + .80); hands = [(.52, .05, 1.12), (.53, -.06, 1.11)]
    elif kind == 'chair':      # at a table, forward, one hand round a glass
        trunk = [[((-.02, 0, h + .10), .15), ((-.05, 0, h + .32), .14), ((-.01, 0, h + .50), .165), ((.04, 0, h + .66), .06)]]
        for s in (1, -1):
            trunk.append([((-.02, s * .09, h + .10), .095), ((.42, s * .11, h + .07), .07), ((.46, s * .12, .08), .05), ((.58, s * .12, .04), .04)])
        arms = [[((-.01, s * .19, h + .58), .065), ((.20, s * .24, h + .30), .05), ((.42, s * .12, .78), .04)] for s in (1, -1)]
        head = (.06, 0, h + .81); hands = [(.45, .10, .78), (.46, -.10, .78)]
    elif kind == 'bench':      # on the banquette, back to the wall, leaning a little toward the table
        trunk = [[((-.04, 0, h + .10), .15), ((-.08, 0, h + .32), .14), ((-.06, 0, h + .50), .165), ((-.02, 0, h + .66), .06)]]
        for s in (1, -1):
            trunk.append([((-.04, s * .09, h + .10), .095), ((.40, s * .11, h + .09), .07), ((.44, s * .13, .08), .05), ((.56, s * .13, .04), .04)])
        arms = [[((-.06, s * .19, h + .58), .065), ((.12, s * .25, h + .32), .05), ((.36, s * .14, .78), .04)] for s in (1, -1)]
        head = (-.01, 0, h + .81); hands = [(.39, .12, .78), (.40, -.12, .78)]
    elif kind == 'tub':        # in a tub chair, leaning back, legs out, a hand on the arm
        trunk = [[((0, 0, h + .10), .15), ((-.10, 0, h + .30), .14), ((-.17, 0, h + .47), .165), ((-.16, 0, h + .63), .06)]]
        for s in (1, -1):
            trunk.append([((0, s * .09, h + .10), .095), ((.44, s * .12, h + .12), .07), ((.58, s * .13, .27), .05), ((.68, s * .13, .24), .04)])
        arms = [[((-.15, s * .19, h + .55), .065), ((-.05, s * .30, h + .28), .05), ((.20, s * .30, h + .20), .04)] for s in (1, -1)]
        head = (-.13, 0, h + .76); hands = [(.22, .30, h + .21), (.22, -.30, h + .21)]
    elif kind in ('pour', 'decks'):   # standing behind the counter
        lean = .05 if kind == 'pour' else .10
        trunk = [[((0, 0, .96), .15), ((0, 0, 1.18), .14), ((lean, 0, 1.38), .165), ((lean + .04, 0, 1.54), .06)]]
        for s in (1, -1):
            trunk.append([((0, s * .10, .94), .095), ((.03, s * .11, .50), .07), ((0, s * .11, .08), .05), ((.13, s * .11, .04), .04)])
        if kind == 'pour':     # the left hand holds the glass low, the right tips the bottle over it
            arms = [[((.03, .19, 1.46), .065), ((.14, .23, 1.20), .05), ((.36, .10, 1.12), .04)],
                    [((.03, -.19, 1.46), .065), ((.26, -.26, 1.40), .05), ((.40, -.06, 1.32), .04)]]
            hands = [(.38, .08, 1.12), (.42, -.04, 1.32)]
        else:                  # both hands at the decks, the head bowed over them
            arms = [[((lean, s * .19, 1.44), .065), ((lean + .20, s * .24, 1.20), .05), ((lean + .40, s * .16, 1.13), .04)] for s in (1, -1)]
            hands = [(lean + .42, .15, 1.13), (lean + .42, -.15, 1.13)]
        head = (lean + .10, 0, 1.66) if kind == 'pour' else (lean + .14, 0, 1.62)
    else:
        raise ValueError(kind)
    return trunk, arms, head, hands


def _skin(bpy, nm, chains, mat):
    """Tubes along each chain of (joint, radius), skinned and smoothed, as one object."""
    me = bpy.data.meshes.new(nm); vs, es, rad = [], [], []
    for ch in chains:
        i0 = len(vs)
        for k, (co, r) in enumerate(ch):
            vs.append(co); rad.append(r)
            if k:
                es.append((i0 + k - 1, i0 + k))
    me.from_pydata(vs, es, [])
    ob = bpy.data.objects.new(nm, me); bpy.context.scene.collection.objects.link(ob)
    sk = ob.modifiers.new('skin', 'SKIN'); sk.use_smooth_shade = True
    roots = set()
    i = 0
    for ch in chains:
        roots.add(i); i += len(ch)
    for k, sv in enumerate(me.skin_vertices[0].data):
        sv.radius = (rad[k], rad[k] * 0.92)
        sv.use_root = k in roots
    sd = ob.modifiers.new('soft', 'SUBSURF'); sd.levels = 1; sd.render_levels = 2
    me.materials.append(mat)
    return ob


def _blob(bpy, nm, co, size, mat, seg=24):
    bm = bmesh.new(); bmesh.ops.create_uvsphere(bm, u_segments=seg, v_segments=seg // 2, radius=1.0)
    bmesh.ops.transform(bm, matrix=Matrix.Translation(co) @ Matrix.Diagonal((*size, 1.0)), verts=bm.verts[:])
    me = bpy.data.meshes.new(nm); bm.to_mesh(me); bm.free()
    for f in me.polygons:
        f.use_smooth = True
    me.materials.append(mat)
    ob = bpy.data.objects.new(nm, me); bpy.context.scene.collection.objects.link(ob)
    return ob


def _skin_mat(bpy, tone):
    key = 'skin-' + tone
    if key not in _M:
        m = K.principled(bpy, 'skin-40-' + tone[1:], tone, rough=0.5)
        b = next(n for n in m.node_tree.nodes if n.type == 'BSDF_PRINCIPLED')
        if 'Subsurface Weight' in b.inputs:
            b.inputs['Subsurface Weight'].default_value = 0.25
            b.inputs['Subsurface Radius'].default_value = (0.010, 0.004, 0.002)
        _M[key] = m
    return _M[key]


def _cloth(bpy, col):
    key = 'cloth-' + col
    if key not in _M:
        m = K.principled(bpy, 'cloth-40-' + col[1:], col, rough=0.88)     # (the room's wool scan read pale pink)
        b = next(n for n in m.node_tree.nodes if n.type == 'BSDF_PRINCIPLED')
        if 'Sheen Weight' in b.inputs:
            b.inputs['Sheen Weight'].default_value = 0.35
        _M[key] = m
    return _M[key]


def _move(ob, d, spin, tilt=0.0):
    """Key the object's travel during the shutter: from -d/2 to +d/2 (metres) and turning `spin` degrees about z
    (and `tilt` about its own x), linear, centred on frame 1 so the shutter sees the middle of it."""
    base = ob.location.copy(); r0 = ob.rotation_euler.copy()
    for f, s in ((0, -0.5), (2, 0.5)):
        ob.location = base + Vector(d) * s
        ob.rotation_euler = Euler((r0.x + math.radians(tilt) * s, r0.y, r0.z + math.radians(spin) * s))
        ob.keyframe_insert('location', frame=f); ob.keyframe_insert('rotation_euler', frame=f)
    ob.location = base; ob.rotation_euler = r0


def _piece(bpy, ob, pivot, W):
    """Re-centre a piece built in the figure's frame on `pivot` and place it in the world by W."""
    ob.data.transform(Matrix.Translation(-Vector(pivot)))
    ob.matrix_world = W @ Matrix.Translation(Vector(pivot))
    return ob


def figures(bpy, name, p, kit):
    """[{"pose": "stool", "at": [x, y, floor z], "heading": deg, "seat": h, "cloth": hex, "skin": hex, "hair": hex,
    "move": [dx, dy, dz] (the trunk's travel), "head": [dx, dy, dz, spin], "arms": [dx, dy, dz, spin], "seed": n}]"""
    sc = bpy.context.scene
    sc.render.use_motion_blur = True
    sc.render.motion_blur_shutter = p.get('shutter', 1.0)
    sc.frame_set(1)
    bpy.context.preferences.edit.keyframe_new_interpolation_type = 'LINEAR'
    objs = []
    for i, f in enumerate(p.get('people', [])):
        rnd = random.Random(f.get('seed', 400 + i))
        trunk, arms, head, hands = _pose(f['pose'], f.get('seat', 0.46))
        x, y, z = f['at']
        W = Matrix.Translation((x, y, z)) @ Matrix.Rotation(math.radians(f.get('heading', 0.0)), 4, 'Z')
        R = W.to_3x3()
        cloth = _cloth(bpy, f.get('cloth', '#2E2A27')); sleeve = _cloth(bpy, f.get('sleeve', f.get('cloth', '#2E2A27')))
        skin = _skin_mat(bpy, f.get('skin', '#9A6A4E'))
        hair = K.principled(bpy, 'hair-40-' + f.get('hair', '#1A1410')[1:], f.get('hair', '#1A1410'), rough=0.6)
        nm = f'{name}-p{i}'
        tb = _piece(bpy, _skin(bpy, nm + '-trunk', trunk, cloth), trunk[0][0][0], W)
        mv = f.get('move', [0.02, 0.02, 0.0])
        _move(tb, R @ Vector(mv), f.get('spin', 4.0))
        sh = (arms[0][0][0][0], 0.0, arms[0][0][0][2])
        ar = _piece(bpy, _skin(bpy, nm + '-arms', arms, sleeve), sh, W)
        for k, hco in enumerate(hands):          # the hands ride with the arms
            hd = _blob(bpy, f'{nm}-hand{k}', Vector(hco) - Vector(sh), (.045, .035, .022), skin)
            hd.parent = ar
        if f['pose'] == 'pour':                  # the bottle, tipped over the glass in the left hand
            bt = K.Mesh(f'{nm}-bottle')
            K._lathe(bt.bm, [(0, 0), (.036, 0), (.036, .19), (.014, .25), (.012, .30), (0, .30)], seg=32, z0=0.0, cx=0.0, cy=0.0)
            M_ = Matrix.Translation(Vector(hands[1]) - Vector(sh) + Vector((0, 0, .02))) @ Matrix.Rotation(math.radians(115), 4, 'X') @ Matrix.Translation((0, 0, -.12))
            bmesh.ops.transform(bt.bm, matrix=M_, verts=bt.bm.verts[:])
            bo = bt.object(bpy, K.principled(bpy, 'bottle-40', '#2A3A2A', rough=0.05, trans=0.6, ior=1.5), smooth=True)
            bo.parent = ar
        a = f.get('arms', [0.05, 0.03, 0.02, 10.0])
        _move(ar, R @ Vector(a[:3]), a[3])
        hd = _blob(bpy, nm + '-head', Vector(head), (.095, .078, .115), skin)
        hr = _blob(bpy, nm + '-hair', Vector(head) + Vector((-.012, 0, .025)), (.100, .086, .105), hair)
        hd = _piece(bpy, hd, head, W)
        hr.data.transform(Matrix.Translation(-Vector(head))); hr.parent = hd
        hm = f.get('head', [0.06, 0.04, 0.01, 18.0])
        _move(hd, R @ Vector(hm[:3]), hm[3], tilt=rnd.uniform(-8, 8))
        objs += [tb, ar, hd]
    return objs


# --- the fir, board by board ---------------------------------------------------------------------------------------
def boards(bpy, name, p, kit):
    """Each loose part of every mesh whose material is the fir scan (`brown_planks`) gets its own random value
    (attribute `board`), which moves where it samples the scan (`offset` metres) and scales its tone (`tone` +/-)
    and warmth (`hue` +/-)."""
    tone, hue, off = p.get('tone', 0.10), p.get('hue', 0.015), p.get('offset', 3.0)
    rnd = random.Random(p.get('seed', 401))
    mats = [m for m in bpy.data.materials if 'brown_planks' in m.name or m.name.startswith('fir-')]
    for ob in [o for o in bpy.data.objects if o.type == 'MESH' and any(s.material in mats for s in o.material_slots)]:
        me = ob.data
        if 'board' in me.attributes:
            continue
        bm = bmesh.new(); bm.from_mesh(me); bm.verts.ensure_lookup_table()
        val = [0.0] * len(bm.verts); seen = set()
        for v in bm.verts:
            if v.index in seen:
                continue
            part, stack = [], [v]
            while stack:
                u = stack.pop()
                if u.index in seen:
                    continue
                seen.add(u.index); part.append(u.index)
                stack.extend(e.other_vert(u) for e in u.link_edges if e.other_vert(u).index not in seen)
            r = rnd.random()
            for k in part:
                val[k] = r
        bm.free()
        at = me.attributes.new('board', 'FLOAT', 'POINT')
        at.data.foreach_set('value', val)
    for m in mats:
        if m.get('boards40'):
            continue
        m['boards40'] = 1
        nt = m.node_tree
        mp = next((n for n in nt.nodes if n.type == 'MAPPING'), None)
        b = next(n for n in nt.nodes if n.type == 'BSDF_PRINCIPLED')
        an = nt.nodes.new('ShaderNodeAttribute'); an.attribute_name = 'board'
        if mp and mp.inputs['Vector'].is_linked:     # sample a different stretch of the scan per board
            src = mp.inputs['Vector'].links[0].from_socket
            va = nt.nodes.new('ShaderNodeVectorMath'); va.operation = 'MULTIPLY_ADD'
            va.inputs[1].default_value = (off, off * 0.61, off * 0.37)
            nt.links.new(an.outputs['Fac'], va.inputs[0]); nt.links.new(src, va.inputs[2]); nt.links.new(va.outputs['Vector'], mp.inputs['Vector'])
        inp = b.inputs['Base Color']
        if inp.is_linked:                            # tone and warmth per board
            src = inp.links[0].from_socket
            hsv = nt.nodes.new('ShaderNodeHueSaturation')
            mr = nt.nodes.new('ShaderNodeMapRange'); mr.inputs['To Min'].default_value = 1 - tone; mr.inputs['To Max'].default_value = 1 + tone
            nt.links.new(an.outputs['Fac'], mr.inputs['Value']); nt.links.new(mr.outputs['Result'], hsv.inputs['Value'])
            mh = nt.nodes.new('ShaderNodeMapRange'); mh.inputs['To Min'].default_value = 0.5 - hue; mh.inputs['To Max'].default_value = 0.5 + hue
            mx = nt.nodes.new('ShaderNodeMath'); mx.operation = 'PINGPONG'; mx.inputs[1].default_value = 1.0
            nt.links.new(an.outputs['Fac'], mx.inputs[0]); nt.links.new(mx.outputs[0], mh.inputs['Value'])
            nt.links.new(mh.outputs['Result'], hsv.inputs['Hue'])
            nt.links.new(src, hsv.inputs['Color']); nt.links.new(hsv.outputs['Color'], inp)
    return []
