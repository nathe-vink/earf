"""Planet EARF, round 41 p4: two finishing touches for the door hero, as kit `ext` pieces by path (built last).

    {"kind": "kit", "shape": "ext", "path": "spinoffs/barkhorn/planet/r41/kit41.py", "fn": "concrete", ...}
    {"kind": "kit", "shape": "ext", "path": "spinoffs/barkhorn/planet/r41/kit41.py", "fn": "seats", ...}

- `concrete`: the walls' and the floor's concrete given the variation a real slab and a real pour have (the p3
  critics: "flat concrete"): a broad, soft mottle of tone (stains, the trowel's passes), `tone` +/- about its mean,
  and a roughness that wanders with it (`rough` +/-), so the sheen breaks up. Subtle, not grunge: the scans' own
  detail (tie holes, pour panels) stays as it is.
- `seats`: every seat's leather its own tone and a little wear (each loose part of the seat meshes gets a random value
  that scales its tone by `tone` +/-), so one model repeated down the room stops reading as one copy.
"""
import os, random, sys

import bmesh

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(HERE))))
KX = os.path.join(ROOT, 'studio', 'engine', 'kit_ext')
if KX not in sys.path:
    sys.path.insert(0, KX)


def _mottle(nt, scale, detail=6.0):
    tc = nt.nodes.new('ShaderNodeTexCoord'); nz = nt.nodes.new('ShaderNodeTexNoise')
    nz.inputs['Scale'].default_value = scale; nz.inputs['Detail'].default_value = detail
    if 'Roughness' in nz.inputs:
        nz.inputs['Roughness'].default_value = 0.55
    nt.links.new(tc.outputs['Object'], nz.inputs['Vector'])
    return nz.outputs['Fac']


def _scale_input(nt, inp, fac, lo, hi, colour):
    """`inp` multiplied by `fac` mapped to [lo, hi], whether it is linked or a value."""
    mr = nt.nodes.new('ShaderNodeMapRange'); mr.inputs['To Min'].default_value = lo; mr.inputs['To Max'].default_value = hi
    mr.inputs['From Min'].default_value = 0.3; mr.inputs['From Max'].default_value = 0.7      # a noise's real range
    nt.links.new(fac, mr.inputs['Value'])
    if colour:
        mx = nt.nodes.new('ShaderNodeMix'); mx.data_type = 'RGBA'; mx.blend_type = 'MULTIPLY'; mx.inputs['Factor'].default_value = 1.0
        if inp.is_linked:
            nt.links.new(inp.links[0].from_socket, mx.inputs[6])
        else:
            mx.inputs[6].default_value = inp.default_value[:]
        cc = nt.nodes.new('ShaderNodeCombineColor')
        for k in ('Red', 'Green', 'Blue'):
            nt.links.new(mr.outputs['Result'], cc.inputs[k])
        nt.links.new(cc.outputs['Color'], mx.inputs[7]); nt.links.new(mx.outputs[2], inp)
    else:
        mu = nt.nodes.new('ShaderNodeMath'); mu.operation = 'MULTIPLY'
        if inp.is_linked:
            nt.links.new(inp.links[0].from_socket, mu.inputs[0])
        else:
            mu.inputs[0].default_value = inp.default_value
        nt.links.new(mr.outputs['Result'], mu.inputs[1]); nt.links.new(mu.outputs[0], inp)


def concrete(bpy, name, p, kit):
    tone, rough = p.get('tone', 0.07), p.get('rough', 0.18)
    for m in [m for m in bpy.data.materials if 'concrete' in m.name.lower() and m.use_nodes and not m.get('r41')]:
        b = next((n for n in m.node_tree.nodes if n.type == 'BSDF_PRINCIPLED'), None)
        if not b:
            continue
        m['r41'] = 1
        nt = m.node_tree
        broad = _mottle(nt, p.get('scale', 0.45))                 # stains and the pour's tide marks, about 2 m across
        trowel = _mottle(nt, p.get('trowel', 2.6), 3.0)           # the trowel's passes, a few hand-spans across
        mix = nt.nodes.new('ShaderNodeMix'); mix.data_type = 'FLOAT'; mix.inputs['Factor'].default_value = 0.35
        nt.links.new(broad, mix.inputs[2]); nt.links.new(trowel, mix.inputs[3])
        fac = mix.outputs[0]
        _scale_input(nt, b.inputs['Base Color'], fac, 1 - tone, 1 + tone * 0.6, True)
        _scale_input(nt, b.inputs['Roughness'], fac, 1 + rough, 1 - rough, False)   # darker stain, a little glossier
    return []


def seats(bpy, name, p, kit):
    tone = p.get('tone', 0.10)
    rnd = random.Random(p.get('seed', 411))
    names = p.get('meshes', ['chairs-leather', 'tub-cushions', 'banquette36', 'banq-cushions'])
    mats = set()
    for ob in [o for o in bpy.data.objects if o.type == 'MESH' and o.name.split('.')[0] in names]:
        me = ob.data
        if 'seat41' in me.attributes:
            continue
        bm = bmesh.new(); bm.from_mesh(me); bm.verts.ensure_lookup_table()
        val = [0.5] * len(bm.verts); seen = set()
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
        me.attributes.new('seat41', 'FLOAT', 'POINT').data.foreach_set('value', val)
        mats.update(s.material for s in ob.material_slots if s.material)
    for m in mats:
        if m.get('seat41') or not m.use_nodes:
            continue
        b = next((n for n in m.node_tree.nodes if n.type == 'BSDF_PRINCIPLED'), None)
        if not b:
            continue
        m['seat41'] = 1
        nt = m.node_tree
        an = nt.nodes.new('ShaderNodeAttribute'); an.attribute_name = 'seat41'
        mr = nt.nodes.new('ShaderNodeMapRange'); mr.inputs['To Min'].default_value = 1 - tone; mr.inputs['To Max'].default_value = 1 + tone
        nt.links.new(an.outputs['Fac'], mr.inputs['Value'])
        inp = b.inputs['Base Color']
        hsv = nt.nodes.new('ShaderNodeHueSaturation')
        if inp.is_linked:
            nt.links.new(inp.links[0].from_socket, hsv.inputs['Color'])
        else:
            hsv.inputs['Color'].default_value = inp.default_value[:]
        nt.links.new(mr.outputs['Result'], hsv.inputs['Value']); nt.links.new(hsv.outputs['Color'], inp)
        # the wear: a seat that has been sat in more is a little glossier
        r = b.inputs['Roughness']
        mw = nt.nodes.new('ShaderNodeMapRange'); mw.inputs['To Min'].default_value = 1.08; mw.inputs['To Max'].default_value = 0.88
        nt.links.new(an.outputs['Fac'], mw.inputs['Value'])
        mu = nt.nodes.new('ShaderNodeMath'); mu.operation = 'MULTIPLY'
        if r.is_linked:
            nt.links.new(r.links[0].from_socket, mu.inputs[0])
        else:
            mu.inputs[0].default_value = r.default_value
        nt.links.new(mw.outputs['Result'], mu.inputs[1]); nt.links.new(mu.outputs[0], r)
    return []
