"""Planet EARF, round 43: Mother EARF at 2 m on an Amsterdam quay, for the Amsterdam Light Festival entry (a proposal:
the design as signed is 1.25 m). Kit `ext` pieces, by path.

    {"kind": "kit", "shape": "ext", "path": "spinoffs/barkhorn/planet/r43/kit43ams.py", "fn": "canal", ...}
    {"kind": "kit", "shape": "ext", "path": "spinoffs/barkhorn/planet/r43/kit43ams.py", "fn": "globe", ...}

The frame: x along the quay, y across the canal (the quay at y < 0, the water from 0 to `width`, the far quay and its
houses beyond), z up from the quay's paving. `canal` builds the quay (brick paving, a stone kerb), the water, the far
quay and a row of gabled canal houses with lit windows. `globe` is round 39's Mother EARF (kit39.mother: six slotted
discs, the axis at 23.4 deg, each disc in its own tint, the rims glowing) at `size`, standing on a blackened-steel
ballast base instead of hanging on its cable.
"""
import math, os, random, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(HERE))))
sys.path.insert(0, os.path.join(ROOT, 'studio', 'engine', 'kit_ext'))
sys.path.insert(0, os.path.join(ROOT, 'spinoffs', 'barkhorn', 'planet', 'r39'))
import planet_r36 as K                                               # noqa: E402
import kit39                                                         # noqa: E402

LK, D, R = K.LK, K.D, K.LK.R
Mesh, principled, emitter, _cyl = R.Mesh, R.principled, R.emitter, R._cyl


def _water(bpy, p):
    if 'ams-water' in R._M:
        return R._M['ams-water']
    m = principled(bpy, 'ams-water', p.get('water', '#0C1216'), rough=p.get('water_rough', 0.06), spec=0.6)
    nt = m.node_tree; b = D._bsdf(m)
    tc = nt.nodes.new('ShaderNodeTexCoord'); mp = nt.nodes.new('ShaderNodeMapping')
    mp.inputs['Scale'].default_value = (1.0, 3.5, 1.0)                # ripples stretched along the canal
    nz = nt.nodes.new('ShaderNodeTexNoise'); nz.inputs['Scale'].default_value = 2.2; nz.inputs['Detail'].default_value = 6.0
    nt.links.new(tc.outputs['Object'], mp.inputs['Vector']); nt.links.new(mp.outputs['Vector'], nz.inputs['Vector'])
    bp = nt.nodes.new('ShaderNodeBump'); bp.inputs['Strength'].default_value = p.get('ripple', 0.25)
    bp.inputs['Distance'].default_value = 0.02
    nt.links.new(nz.outputs['Fac'], bp.inputs['Height']); nt.links.new(bp.outputs['Normal'], b.inputs['Normal'])
    R._M['ams-water'] = m
    return m


def canal(bpy, name, p, kit):
    objs = []
    Wc = p.get('width', 18.0); L0, L1 = -40.0, 40.0; drop = 1.1
    # the near quay: brick paving to the kerb, a stone kerb, the quay wall down to the water
    pv = Mesh('ams-paving'); pv.box(L0, -14.0, -0.2, L1, -0.35, 0.0)
    objs.append(pv.object(bpy, R._pbr(bpy, kit, p.get('paving_tex', 'concrete_pavement'), res='2k',
                                     tint=p.get('paving_tint', '#4E4640'), tint_mix=0.45)))
    kb = Mesh('ams-kerb'); kb.box(L0, -0.35, -0.2, L1, 0.0, 0.03)
    kb.box(L0, -0.30, -drop - 1.0, L1, 0.0, -0.2)                         # the quay wall's face
    objs.append(kb.object(bpy, principled(bpy, 'ams-stone', '#5A5650', rough=0.75, bump=(0.01, 0.3, 0.001))))
    # the water
    wt = Mesh('ams-water'); wt.box(L0, 0.0, -drop - 1.0, L1, Wc, -drop)
    objs.append(wt.object(bpy, _water(bpy, p)))
    # the far quay and its houses: brick fronts, white-framed windows, some lit, gables
    fq = Mesh('ams-far-quay'); fq.box(L0, Wc, -drop - 1.0, L1, Wc + 6.0, 0.0)
    objs.append(fq.object(bpy, principled(bpy, 'ams-far-quay', '#3E3934', rough=0.85)))
    rnd = random.Random(p.get('seed', 16))
    brick = Mesh('ams-brick'); trim = Mesh('ams-trim'); lit = Mesh('ams-lit'); dark = Mesh('ams-dark')
    x = L0; yf = Wc + 4.0
    while x < L1:
        w = rnd.choice([4.8, 5.4, 6.0, 7.2]); h = rnd.choice([11.0, 12.5, 14.0, 15.5])
        brick.box(x + 0.05, yf, 0.0, x + w - 0.05, yf + 10.0, h)
        # a stepped or neck gable on top
        gw = w * 0.55; gh = rnd.choice([2.2, 2.8, 3.4])
        brick.box(x + (w - gw) / 2, yf, h, x + (w + gw) / 2, yf + 0.4, h + gh)
        trim.box(x + (w - gw) / 2 - 0.05, yf - 0.06, h + gh, x + (w + gw) / 2 + 0.05, yf + 0.4, h + gh + 0.12)
        cols = max(2, int(w / 1.6))
        for fl in range(int(h / 3.1)):
            z0 = 0.9 + fl * 3.1
            for c in range(cols):
                wx = x + 0.45 + c * (w - 0.9) / cols; ww = (w - 0.9) / cols - 0.45
                trim.box(wx - 0.06, yf - 0.05, z0 - 0.06, wx + ww + 0.06, yf - 0.01, z0 + 1.86)
                (lit if rnd.random() < p.get('lit', 0.38) else dark).box(wx, yf - 0.06, z0, wx + ww, yf - 0.05, z0 + 1.8)
        x += w
    objs.append(brick.object(bpy, principled(bpy, 'ams-brick', p.get('brick', '#3A2621'), rough=0.85,
                                             bump=(0.02, 0.25, 0.002))))
    objs.append(trim.object(bpy, principled(bpy, 'ams-trim', '#BDB6AA', rough=0.6)))
    objs.append(lit.object(bpy, emitter(bpy, 'ams-lit', '#FFC27A', p.get('window_glow', 3.0))))
    objs.append(dark.object(bpy, principled(bpy, 'ams-dark', '#0B0B0D', rough=0.08, spec=0.6)))
    # a row of elms' trunks on the far quay and bollards on ours, for scale
    tr = Mesh('ams-trunks')
    for k in range(-6, 7):
        _cyl(tr.bm, k * 6.5 + 1.3, Wc + 2.0, 0.0, 0.22, 6.0, seg=16)
    objs.append(tr.object(bpy, principled(bpy, 'ams-bark', '#1E1A17', rough=0.9), smooth=True))
    bo = Mesh('ams-bollards')
    for k in range(-8, 9):
        _cyl(bo.bm, k * 3.2 + 0.7, -0.75, 0.0, 0.09, 0.7, seg=20)
    objs.append(bo.object(bpy, principled(bpy, 'ams-bollard', '#3B1716', rough=0.4, metal=0.2), smooth=True))
    return objs


def globe(bpy, name, p, kit):
    """Mother EARF at `size` on a ballast base: kit39.mother without its cable or core, then the base."""
    size = p.get('size', 2.0); r = size / 2
    cx, cy = p.get('at', [0.0, -3.2]); base_h, post = p.get('base_h', 0.45), p.get('post', 0.25)
    cz = base_h + post + r * 0.94
    q = {'centre': [cx, cy, cz], 'size': size, 't': p.get('t', 0.0127), 'core': 0.0, 'rim': p.get('rim', 0.03),
         'radius': p.get('radius', 0.07), 'ceiling': cz + r + 0.1, 'heading': p.get('heading', 55.0),
         'rim_par': p.get('rim_par', 1.0)}
    objs = kit39.mother(bpy, name, q, kit)
    for ob in list(objs):                                               # no cable outdoors: it stands
        if ob.name.startswith(f'{name}-cable'):
            bpy.data.objects.remove(ob, do_unlink=True); objs.remove(ob)
    # the base: a blackened-steel drum filled with ballast, a short post to the south pole's cradle
    bs = Mesh(f'{name}-base')
    _cyl(bs.bm, cx, cy, 0.0, p.get('base_r', 0.75), base_h, seg=64)
    _cyl(bs.bm, cx, cy, base_h, 0.06, post + 0.12, seg=24)
    objs.append(bs.object(bpy, K.blackened_steel(bpy), smooth=True, bevel=0.01))
    return objs
