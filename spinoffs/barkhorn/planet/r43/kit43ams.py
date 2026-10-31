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
    bp = nt.nodes.new('ShaderNodeBump'); bp.inputs['Strength'].default_value = p.get('ripple', 0.5)
    bp.inputs['Distance'].default_value = 0.02
    nt.links.new(nz.outputs['Fac'], bp.inputs['Height']); nt.links.new(bp.outputs['Normal'], b.inputs['Normal'])
    R._M['ams-water'] = m
    return m


def canal(bpy, name, p, kit):
    objs = []
    Wc = p.get('width', 18.0); L0, L1 = -40.0, 40.0; drop = 1.1
    # the near quay: brick paving to the kerb, a stone kerb, the quay wall down to the water
    pv = Mesh('ams-paving'); pv.box(L0, -14.0, -0.2, L1, -0.35, 0.0)
    objs.append(pv.object(bpy, _klinker(bpy) if p.get('klinker') else
                          R._pbr(bpy, kit, p.get('paving_tex', 'concrete_pavement'), res='2k',
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
    brick = Mesh('ams-brick'); trim = Mesh('ams-trim'); dark = Mesh('ams-dark')
    # lit rooms in three warmths and brightnesses (round 43 p1 critics: "flat white panes, identical")
    lits = [Mesh(f'ams-lit{k}') for k in range(3)]
    x = L0 if p.get('old_houses', True) else L1; yf = Wc + 4.0
    while x < L1:
        w = rnd.choice([4.8, 5.4, 6.0, 7.2]); h = rnd.choice([11.0, 12.5, 14.0, 15.5])
        brick.box(x + 0.05, yf, 0.0, x + w - 0.05, yf + 10.0, h)
        # a stepped or neck gable on top
        # a stepped gable: three narrowing tiers, a white coping on each step (p2 critics: "chimney stacks on a block")
        gh = rnd.choice([0.9, 1.1, 1.3])
        for k, f in enumerate((0.92, 0.66, 0.38)):
            gw = w * f; z0 = h + k * gh
            brick.box(x + (w - gw) / 2, yf, z0, x + (w + gw) / 2, yf + 0.5, z0 + gh)
            trim.box(x + (w - gw) / 2 - 0.05, yf - 0.05, z0 + gh, x + (w + gw) / 2 + 0.05, yf + 0.5, z0 + gh + 0.1)
        cols = max(2, int(w / 1.6))
        for fl in range(int(h / 3.1)):
            z0 = 0.9 + fl * 3.1
            for c in range(cols):
                wx = x + 0.45 + c * (w - 0.9) / cols; ww = (w - 0.9) / cols - 0.45
                trim.box(wx - 0.06, yf - 0.05, z0 - 0.06, wx + ww + 0.06, yf - 0.01, z0 + 1.86)
                if rnd.random() < p.get('lit', 0.38):
                    lits[rnd.randrange(3)].box(wx, yf - 0.06, z0, wx + ww, yf - 0.05, z0 + 1.8)
                    # a curtain half across some lit windows
                    if rnd.random() < 0.4:
                        trim.box(wx, yf - 0.07, z0, wx + ww * rnd.uniform(0.25, 0.5), yf - 0.065, z0 + 1.8)
                else:
                    dark.box(wx, yf - 0.06, z0, wx + ww, yf - 0.05, z0 + 1.8)
        x += w
    objs.append(brick.object(bpy, principled(bpy, 'ams-brick', p.get('brick', '#4A2A22'), rough=0.85,
                                             bump=(0.012, 0.6, 0.003))))
    objs.append(trim.object(bpy, principled(bpy, 'ams-trim', '#BDB6AA', rough=0.6)))
    g = p.get('window_glow', 0.35)
    for k, (col, mul) in enumerate((('#FFB070', 1.0), ('#FF9440', 0.55), ('#FFC890', 0.3))):
        objs.append(lits[k].object(bpy, emitter(bpy, f'ams-lit{k}', col, g * mul)))
    objs.append(dark.object(bpy, principled(bpy, 'ams-dark', '#0B0B0D', rough=0.08, spec=0.6)))
    # a row of elms' trunks on the far quay and bollards on ours, for scale
    if not p.get('old_street', True):
        return [o for o in objs if o is not None]
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
    objs.append(bs.object(bpy, principled(bpy, 'ams-plinth-steel', '#2A2622', rough=0.35, metal=0.8,
                                          bump=(0.01, 0.2, 0.0005)), smooth=True, bevel=0.015))
    return objs


# --- the set pass (round 43, look 2): canal houses, Amsterdam street furniture, people ----------------------------------
def _brick_mat(bpy, name, c1, c2):
    """Brick with mortar: Blender's brick texture, two tones per house, a bump in the joints."""
    if name in R._M:
        return R._M[name]
    m = principled(bpy, name, c1, rough=0.88)
    nt = m.node_tree; b = D._bsdf(m)
    tc = nt.nodes.new('ShaderNodeTexCoord'); bk = nt.nodes.new('ShaderNodeTexBrick')
    bk.inputs['Color1'].default_value = R.lin(c1); bk.inputs['Color2'].default_value = R.lin(c2)
    bk.inputs['Mortar'].default_value = R.lin('#3A3530'); bk.inputs['Scale'].default_value = 1.0
    bk.inputs['Mortar Size'].default_value = 0.012; bk.inputs['Brick Width'].default_value = 0.22
    bk.inputs['Row Height'].default_value = 0.065
    mp = nt.nodes.new('ShaderNodeMapping'); mp.inputs['Rotation'].default_value = (math.radians(90), 0.0, 0.0)
    nt.links.new(tc.outputs['Object'], mp.inputs['Vector']); nt.links.new(mp.outputs['Vector'], bk.inputs['Vector'])
    nt.links.new(bk.outputs['Color'], b.inputs['Base Color'])
    bp = nt.nodes.new('ShaderNodeBump'); bp.inputs['Strength'].default_value = 0.4; bp.inputs['Distance'].default_value = 0.004
    nt.links.new(bk.outputs['Fac'], bp.inputs['Height']); nt.links.new(bp.outputs['Normal'], b.inputs['Normal'])
    R._M[name] = m
    return m


def _klinker(bpy):
    """Amsterdam klinker paving (look 2, round 1 critics: "a smooth repeated tile"): fired brick on edge, 20 x 10 cm
    from above, stretcher bond, per-brick tone, dirty joints, a damp sheen varied by a broad noise (roughness 0.3-0.7)."""
    name = 'ams-klinker'
    if name in R._M:
        return R._M[name]
    m = principled(bpy, name, '#4C3A32', rough=0.55)
    nt = m.node_tree; b = D._bsdf(m)
    tc = nt.nodes.new('ShaderNodeTexCoord'); bk = nt.nodes.new('ShaderNodeTexBrick')
    bk.inputs['Color1'].default_value = R.lin('#54403A'); bk.inputs['Color2'].default_value = R.lin('#3E3430')
    bk.inputs['Mortar'].default_value = R.lin('#1E1B19'); bk.inputs['Scale'].default_value = 1.0
    bk.inputs['Mortar Size'].default_value = 0.006; bk.inputs['Brick Width'].default_value = 0.20
    bk.inputs['Row Height'].default_value = 0.10; bk.inputs['Bias'].default_value = 0.0
    nt.links.new(tc.outputs['Object'], bk.inputs['Vector'])
    nz = nt.nodes.new('ShaderNodeTexNoise'); nz.inputs['Scale'].default_value = 0.35; nz.inputs['Detail'].default_value = 6.0
    nt.links.new(tc.outputs['Object'], nz.inputs['Vector'])
    mx = nt.nodes.new('ShaderNodeMix'); mx.data_type = 'RGBA'; mx.inputs['Factor'].default_value = 0.25
    nt.links.new(bk.outputs['Color'], mx.inputs[6]); nt.links.new(nz.outputs['Color'], mx.inputs[7])
    nt.links.new(mx.outputs[2], b.inputs['Base Color'])
    cr = nt.nodes.new('ShaderNodeMapRange'); cr.inputs['To Min'].default_value = 0.28; cr.inputs['To Max'].default_value = 0.72
    nt.links.new(nz.outputs['Fac'], cr.inputs['Value']); nt.links.new(cr.outputs['Result'], b.inputs['Roughness'])
    bp = nt.nodes.new('ShaderNodeBump'); bp.inputs['Strength'].default_value = 0.6; bp.inputs['Distance'].default_value = 0.004
    nt.links.new(bk.outputs['Fac'], bp.inputs['Height']); nt.links.new(bp.outputs['Normal'], b.inputs['Normal'])
    R._M[name] = m
    return m


def houses(bpy, name, p, kit):
    """A row of narrow canal houses on the far quay: varied widths and heights, step, neck and cornice gables with
    white copings, tall sash windows with white frames and glazing bars, rooms lit at varied warmth and level (a
    brighter ceiling band over a dimmer room), some curtained, hoist beams under the gables."""
    objs = []
    Wc = p.get('width', 18.0); yf = Wc + 4.0
    rnd = random.Random(p.get('seed', 27))
    bricks = [('#4A2A22', '#3E231C'), ('#2E211C', '#261B17'), ('#5A3428', '#4A2B21'), ('#3A2E28', '#30251F')]
    meshes = {k: Mesh(f'ams-h-brick{k}') for k in range(len(bricks))}
    trim, dark, lits, curt = Mesh('ams-h-trim'), Mesh('ams-h-dark'), [Mesh(f'ams-h-lit{k}') for k in range(4)], Mesh('ams-h-curt')
    dimr = [Mesh(f'ams-h-room{k}') for k in range(4)]
    x = -40.0
    while x < 40.0:
        w = rnd.choice([4.2, 4.8, 5.4, 6.0, 7.2]); fl = rnd.choice([3, 4, 4, 5]); h = 0.6 + fl * 3.0
        bm_ = meshes[rnd.randrange(len(bricks))]
        bm_.box(x + 0.03, yf, 0.0, x + w - 0.03, yf + 10.0, h)
        kind = rnd.choice(['step', 'neck', 'neck', 'cornice'])
        if kind == 'step':
            gh = 0.75
            for k, f in enumerate((0.95, 0.75, 0.55, 0.35)):
                gw = w * f; z0 = h + k * gh
                bm_.box(x + (w - gw) / 2, yf, z0, x + (w + gw) / 2, yf + 0.5, z0 + gh)
                trim.box(x + (w - gw) / 2 - 0.04, yf - 0.04, z0 + gh, x + (w + gw) / 2 + 0.04, yf + 0.5, z0 + gh + 0.08)
            top = h + 4 * gh
        elif kind == 'neck':
            nw = w * 0.56; nh = 3.0
            bm_.box(x + (w - nw) / 2, yf, h, x + (w + nw) / 2, yf + 0.5, h + nh)
            for s in (-1, 1):                                          # the shoulders, as white scrolls (blocks)
                cx = x + w / 2 + s * (nw / 2 + w * 0.13)
                trim.box(cx - w * 0.13, yf - 0.04, h, cx + w * 0.13, yf + 0.3, h + 0.9)
            trim.box(x + (w - nw) / 2 - 0.1, yf - 0.05, h + nh, x + (w + nw) / 2 + 0.1, yf + 0.5, h + nh + 0.35)
            top = h + nh + 0.35
        else:
            trim.box(x, yf - 0.18, h - 0.1, x + w, yf + 0.5, h + 0.35)             # a deep white cornice
            top = h + 0.35
        # the hoist beam under the top
        trim.box(x + w / 2 - 0.08, yf - 0.9, top - 1.2, x + w / 2 + 0.08, yf, top - 1.0)
        cols = 2 if w < 5.0 else 3
        for f_ in range(fl):
            z0 = 0.9 + f_ * 3.0; wh = 1.95 if f_ else 2.2
            for c in range(cols):
                wx0 = x + 0.5 + c * (w - 1.0) / cols + 0.12; wx1 = wx0 + (w - 1.0) / cols - 0.5
                trim.box(wx0 - 0.08, yf - 0.06, z0 - 0.08, wx1 + 0.08, yf - 0.005, z0 + wh + 0.08)   # the white frame
                r = rnd.random()
                if r < p.get('lit', 0.3):
                    k = rnd.randrange(4)
                    lits[k].box(wx0, yf - 0.065, z0 + wh * 0.62, wx1, yf - 0.062, z0 + wh)          # the ceiling band
                    dimr[k].box(wx0, yf - 0.065, z0, wx1, yf - 0.062, z0 + wh * 0.62)            # the room, same hue, dimmer
                    if rnd.random() < 0.45:
                        cw = (wx1 - wx0) * rnd.uniform(0.2, 0.45)
                        curt.box(wx0, yf - 0.075, z0, wx0 + cw, yf - 0.07, z0 + wh)
                else:
                    dark.box(wx0, yf - 0.065, z0, wx1, yf - 0.062, z0 + wh)
                # the glazing bars: one upright, two crossbars
                xm = (wx0 + wx1) / 2
                trim.box(xm - 0.02, yf - 0.08, z0, xm + 0.02, yf - 0.066, z0 + wh)
                for zz in (z0 + wh * 0.33, z0 + wh * 0.66):
                    trim.box(wx0, yf - 0.08, zz - 0.02, wx1, yf - 0.066, zz + 0.02)
        x += w
    for k, (c1, c2) in enumerate(bricks):
        objs.append(meshes[k].object(bpy, _brick_mat(bpy, f'ams-brick-{k}', c1, c2)))
    objs.append(trim.object(bpy, principled(bpy, 'ams-h-trim', '#D8D2C6', rough=0.55)))
    objs.append(dark.object(bpy, principled(bpy, 'ams-h-dark', '#07080A', rough=0.06, spec=0.7)))
    objs.append(curt.object(bpy, principled(bpy, 'ams-h-curt', '#E6D2B0', rough=0.9, emit='#FFB070',
                                            strength=p.get('window_glow', 0.08) * 0.6)))
    g = p.get('window_glow', 0.08)
    for k, (col, mul) in enumerate((('#FFB070', 1.2), ('#FF9440', 0.6), ('#FFC890', 0.35), ('#FFA860', 0.18))):
        objs.append(lits[k].object(bpy, emitter(bpy, f'ams-h-lit{k}', col, g * mul)))
        objs.append(dimr[k].object(bpy, emitter(bpy, f'ams-h-room{k}', col, g * mul * 0.45)))
    return objs


def street(bpy, name, p, kit):
    """Amsterdammertje bollards (cast iron, dark red-brown, a domed cap and a collar), a bicycle against a bollard, a
    low barrier ring round the globe on eight posts, and a few figures (simple dark-coated silhouettes)."""
    objs = []
    iron = principled(bpy, 'ams-iron', '#2A1410', rough=0.55, metal=0.4, bump=(0.004, 0.3, 0.0004))
    bo = Mesh('ams-amsterdammertjes')
    for (bx, by) in p.get('bollards', []):
        _cyl(bo.bm, bx, by, 0.0, 0.075, 0.78, seg=24)
        _cyl(bo.bm, bx, by, 0.62, 0.085, 0.04, seg=24)
        _cyl(bo.bm, bx, by, 0.78, 0.06, 0.05, seg=24)
        _cyl(bo.bm, bx, by, 0.83, 0.035, 0.04, seg=24)
    objs.append(bo.object(bpy, iron, smooth=True, bevel=0.006))
    # the barrier ring: eight posts and a rope
    cx, cy = p.get('ring_at', [0.0, -3.2]); rr = p.get('ring_r', 1.7)
    rg = Mesh('ams-ring'); steel = principled(bpy, 'ams-ring-steel', '#1C1A18', rough=0.4, metal=0.85)
    for k in range(8):
        a = k * math.pi / 4
        _cyl(rg.bm, cx + rr * math.cos(a), cy + rr * math.sin(a), 0.0, 0.025, p.get('post_h', 0.85), seg=12)
    LK._arc(rg.bm, cx, cy, rr - 0.008, rr + 0.008, 0.0, 2 * math.pi, p.get('rope_z', 0.72), p.get('rope_z', 0.72) + 0.016, seg=96)
    objs.append(rg.object(bpy, steel, smooth=True))
    # a bicycle: two wheels, a frame, leaning on a bollard
    if p.get('bike'):
        bx, by, hd = p['bike']
        c, s = math.cos(math.radians(hd)), math.sin(math.radians(hd))
        blk = principled(bpy, 'ams-bike', '#0E0E0F', rough=0.35, metal=0.6)
        for off in (-0.55, 0.55):
            wm = Mesh(f'ams-bike-wheel{off}'); LK._arc(wm.bm, 0.0, 0.0, 0.31, 0.335, 0.0, 2 * math.pi, -0.02, 0.02, seg=48)
            ob = wm.object(bpy, blk, smooth=True); ob.rotation_euler = (math.radians(90), 0.0, math.radians(hd))
            ob.location = (bx + off * c, by + off * s, 0.335); objs.append(ob)
        fm = Mesh('ams-bike-frame')

        def P(u, z):
            return (bx + u * c, by + u * s, z)
        for a, b in (((-0.55, 0.335), (0.0, 0.42)), ((0.0, 0.42), (0.45, 0.92)), ((0.0, 0.42), (-0.1, 0.9)),
                     ((-0.55, 0.335), (-0.1, 0.9)), ((-0.1, 0.9), (0.40, 0.92)), ((0.45, 0.92), (0.55, 0.335)),
                     ((0.45, 0.92), (0.40, 1.05))):
            LK._rod(fm.bm, P(*a), P(*b), 0.014, 0.014, seg=8)
        objs.append(fm.object(bpy, blk, smooth=True))
    # figures: legs, a coat, shoulders, a head; facing `hd`
    coat_cols = ['#1A1C20', '#2A2622', '#16181A', '#3A2E26', '#22252A']
    for i, (fx, fy, hd, ht) in enumerate(p.get('figures', [])):
        fg = Mesh(f'ams-figure{i}'); sk = Mesh(f'ams-figure-skin{i}')
        c, s = math.cos(math.radians(hd)), math.sin(math.radians(hd)); k = ht / 1.75
        for side in (-1, 1):
            lx, ly = fx - s * side * 0.09 * k, fy + c * side * 0.09 * k
            _cyl(fg.bm, lx, ly, 0.0, 0.065 * k, 0.85 * k, seg=12)
        _cyl(fg.bm, fx, fy, 0.75 * k, 0.21 * k, 0.70 * k, seg=20)                     # the coat
        _cyl(fg.bm, fx, fy, 1.42 * k, 0.17 * k, 0.06 * k, seg=20)                     # the shoulders
        _cyl(fg.bm, fx, fy, 1.48 * k, 0.05 * k, 0.08 * k, seg=12)                     # the neck
        import bmesh
        bmesh.ops.create_uvsphere(sk.bm, u_segments=16, v_segments=10, radius=0.11 * k,
                                  matrix=__import__('mathutils').Matrix.Translation((fx, fy, 1.64 * k)))
        objs.append(fg.object(bpy, principled(bpy, f'ams-coat{i}', coat_cols[i % len(coat_cols)], rough=0.8), smooth=True))
        objs.append(sk.object(bpy, principled(bpy, 'ams-skin', '#6A4A3A', rough=0.6), smooth=True))
    return objs
