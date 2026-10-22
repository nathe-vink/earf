"""A simulated smoke plume as a volume in Cycles (round 31b, Smoke E9: the bridge).

plume: the grids from `plume_sim.py` (`cache`, an .npz path from the repo root) as a box of smoke and flame. The fire's
centre sits at `position` (x, y; the box's floor at z), or with `anchor` 'solid' the first solid's (E12: the speaker the
flow went round, whose fire is set behind it), the sim's downwind +x turned `rotate_z` degrees, everything scaled
`scale`. Soot is `color`, scattering forward by `anisotropy`, `density` per metre where the coded soot is
full; `absorb` darkens what it scatters. The flame glows in black-body colour from `cool` to `hot` kelvin, `strength`
bright, and heat glows dull red at `heat_glow`. `detail` pushes the lookups about by a fine noise (`detail_scale`
metres, `detail` in voxels) so the edges tatter below the grid's own size; `edge` [lo, hi] remaps the soot by a
smoothstep so thin margins drop to clear air and the lobes keep firm outlines; `breakup` varies the soot inside by a noise
(1 -/+ b); `tongues` cuts the flame's glow into filaments (`tongue_edge` makes them hard-edged). Each noise runs at
every step of every ray through the box, so their octaves (`detail_octaves`, `breakup_octaves`, `tongue_octaves`) set
what a render costs: p4's 6/5/6 took 3.4 times p3's single 4-octave noise. E10 adds two, off by default: `warp` [voxels,
metres, octaves], a coarser push of the lookups that folds the sim's round lobes into one another; `billow` [amount,
metres, octaves], a fractal noise added to the soot before `edge` remaps it, so its surface carries lumps on lumps
(pyroclastic); and `grain` [amount, metres, octaves], a fine texture in the soot.

There is no VDB writer in this container, so the grids reach the shader as an atlas: each horizontal slice of the box
is one tile of a float image (soot in red, flame in green, heat in blue), and the shader finds the two slices about a
point and blends them.
"""
import math
import os

import bmesh
import numpy as np
from mathutils import Vector

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..'))
_ATLAS = {}


def _atlas(bpy, path):
    if path in _ATLAS:
        return _ATLAS[path]
    z = np.load(path)
    NX, NY, NZ = (int(v) for v in z['size'])
    grids = [(z[k].astype(np.float32) / 255.0) ** 2 for k in ('rho', 'flame', 'heat')]
    # fade to nothing over the sim's sponges (the domain's downwind ends, its sides and its lid), so the box never shows
    def ramp(n, band):
        t = np.clip(np.minimum(np.arange(n), np.arange(n)[::-1]) / max(band, 1), 0, 1)
        return (t * t * (3 - 2 * t)).astype(np.float32)
    fx, fy = ramp(NX, int(0.12 * NX)), ramp(NY, int(0.1 * NY))
    fz = np.clip((NZ - 1 - np.arange(NZ)) / max(int(0.16 * NZ), 1), 0, 1).astype(np.float32)
    fz = fz * fz * (3 - 2 * fz)
    fade = fx[:, None, None] * fy[None, :, None] * fz[None, None, :]
    grids = [g * fade for g in grids]
    TX = max(1, int(round(math.sqrt(NZ * NY / NX))))
    TY = -(-NZ // TX)
    W, H = TX * NX, TY * NY
    a = np.zeros((H, W, 4), np.float32)
    a[..., 3] = 1.0
    for k in range(NZ):
        tx, ty = k % TX, k // TX
        for c, g in enumerate(grids):
            a[ty * NY:(ty + 1) * NY, tx * NX:(tx + 1) * NX, c] = g[:, :, k].T      # rows run along y, columns along x
    img = bpy.data.images.new(os.path.basename(path), W, H, alpha=True, float_buffer=True)
    img.colorspace_settings.name = 'Non-Color'
    img.pixels.foreach_set(a.ravel())
    img.pack()
    info = dict(img=img, NX=NX, NY=NY, NZ=NZ, TX=TX, TY=TY, dx=float(z['dx']), source=[float(v) for v in z['source']],
                solids=z['solids'].tolist() if 'solids' in z.files else [])
    _ATLAS[path] = info
    return info


def plume(bpy, name, p, kit):
    path = os.path.join(ROOT, p['cache'])
    A = _atlas(bpy, path)
    NX, NY, NZ, TX, TY = A['NX'], A['NY'], A['NZ'], A['TX'], A['TY']
    sc = p.get('scale', 1.0)
    dx = A['dx'] * sc
    Lx, Ly, Lz = NX * dx, NY * dx, NZ * dx
    cx, cy = A['solids'][0][:2] if p.get('anchor') == 'solid' else A['source'][:2]
    sx, sy = cx * sc, cy * sc
    # the box, with the fire's centre (or the solid's) at the object's origin
    bm = bmesh.new()
    g = bmesh.ops.create_cube(bm, size=1.0)
    for v in g['verts']:
        v.co = Vector(((v.co.x + 0.5) * Lx - sx, (v.co.y + 0.5) * Ly - sy, (v.co.z + 0.5) * Lz))
    me = bpy.data.meshes.new(name); bm.to_mesh(me); bm.free()
    ob = bpy.data.objects.new(name, me); bpy.context.scene.collection.objects.link(ob)
    px, py = p.get('position', [0.0, 0.0])[:2]
    pz = p.get('position', [0.0, 0.0, 0.0])[2] if len(p.get('position', [])) > 2 else 0.0
    ob.location = Vector((px, py, pz))
    ob.rotation_euler.z = math.radians(p.get('rotate_z', 0.0))
    # `through_glass` False: the fire and smoke unseen by rays that came through a clear part (E12r: the fire behind
    # the speaker glowed in its smoked horn like a screen, "a vintage CRT television")
    if p.get('through_glass') is False:
        ob.visible_transmission = False

    m = bpy.data.materials.new(name); m.use_nodes = True; nt = m.node_tree; nt.nodes.clear()
    N = nt.nodes.new
    L = nt.links.new

    def math_(op, a, b=None, c=None):
        n = N('ShaderNodeMath'); n.operation = op
        for k, x in enumerate((a, b, c)):
            if x is None:
                continue
            if isinstance(x, (int, float)):
                n.inputs[k].default_value = x
            else:
                L(x, n.inputs[k])
        return n.outputs[0]

    out = N('ShaderNodeOutputMaterial')
    vol = N('ShaderNodeVolumePrincipled')
    vol.inputs['Color'].default_value = kit.M.hex_lin(p.get('color', '#2A2724'))
    vol.inputs['Absorption Color'].default_value = kit.M.hex_lin(p.get('absorb', '#000000'))
    vol.inputs['Anisotropy'].default_value = p.get('anisotropy', 0.35)
    tc = N('ShaderNodeTexCoord')
    co = tc.outputs['Generated']                          # 0..1 across the box
    mp = N('ShaderNodeMapping'); L(tc.outputs['Object'], mp.inputs['Vector'])     # metres, moved by the seed
    mp.inputs['Location'].default_value = (p.get('seed', 0) * 5.3, p.get('seed', 0) * 2.9, 0.0)
    if p.get('detail', 1.5) > 0:
        # tatter the edges: shift each lookup by a fine noise, `detail` voxels at most
        nz = N('ShaderNodeTexNoise'); nz.noise_dimensions = '3D'
        nz.inputs['Scale'].default_value = 1.0 / p.get('detail_scale', 0.35)
        nz.inputs['Detail'].default_value = p.get('detail_octaves', 4.0)
        nz.inputs['Distortion'].default_value = 0.6
        L(mp.outputs['Vector'], nz.inputs['Vector'])
        off = N('ShaderNodeVectorMath'); off.operation = 'SUBTRACT'
        L(nz.outputs['Color'], off.inputs[0]); off.inputs[1].default_value = (0.5, 0.5, 0.5)
        amp = N('ShaderNodeVectorMath'); amp.operation = 'MULTIPLY'
        L(off.outputs[0], amp.inputs[0])
        d = p.get('detail', 1.5) * 2.0
        amp.inputs[1].default_value = (d / NX, d / NY, d / NZ)
        add = N('ShaderNodeVectorMath'); add.operation = 'ADD'
        L(co, add.inputs[0]); L(amp.outputs[0], add.inputs[1])
        co = add.outputs[0]
    if p.get('warp'):
        # Smoke E10: a second, coarser push of the lookups, `warp` [voxels, metres, octaves], so the sim's lobes lose
        # their roundness, fold into one another and shear into streaks (E9's critics: "cotton-ball", "metaball lobes")
        wa, ws, wo = p['warp']
        nw = N('ShaderNodeTexNoise'); nw.noise_dimensions = '3D'
        nw.inputs['Scale'].default_value = 1.0 / ws; nw.inputs['Detail'].default_value = wo
        nw.inputs['Distortion'].default_value = 0.3
        L(mp.outputs['Vector'], nw.inputs['Vector'])
        wof = N('ShaderNodeVectorMath'); wof.operation = 'SUBTRACT'
        L(nw.outputs['Color'], wof.inputs[0]); wof.inputs[1].default_value = (0.5, 0.5, 0.5)
        wam = N('ShaderNodeVectorMath'); wam.operation = 'MULTIPLY'
        L(wof.outputs[0], wam.inputs[0]); wam.inputs[1].default_value = (2 * wa / NX, 2 * wa / NY, 2 * wa / NZ)
        wad = N('ShaderNodeVectorMath'); wad.operation = 'ADD'
        L(co, wad.inputs[0]); L(wam.outputs[0], wad.inputs[1])
        co = wad.outputs[0]
    sep = N('ShaderNodeSeparateXYZ'); L(co, sep.inputs['Vector'])
    gx = math_('MAXIMUM', math_('MINIMUM', sep.outputs['X'], 1.0 - 0.5 / NX), 0.5 / NX)
    gy = math_('MAXIMUM', math_('MINIMUM', sep.outputs['Y'], 1.0 - 0.5 / NY), 0.5 / NY)
    f = math_('MAXIMUM', math_('MINIMUM', math_('MULTIPLY_ADD', sep.outputs['Z'], float(NZ), -0.5), NZ - 1.0), 0.0)
    k0 = math_('FLOOR', f)
    t = math_('SUBTRACT', f, k0)
    k1 = math_('MINIMUM', math_('ADD', k0, 1.0), NZ - 1.0)
    looks = []
    for k in (k0, k1):
        tx = math_('FLOORED_MODULO', k, float(TX))
        ty = math_('FLOOR', math_('DIVIDE', k, float(TX)))
        U = math_('DIVIDE', math_('ADD', tx, gx), float(TX))
        V = math_('DIVIDE', math_('ADD', ty, gy), float(TY))
        cxyz = N('ShaderNodeCombineXYZ'); L(U, cxyz.inputs['X']); L(V, cxyz.inputs['Y'])
        im = N('ShaderNodeTexImage'); im.image = A['img']; im.interpolation = 'Linear'; im.extension = 'EXTEND'
        L(cxyz.outputs['Vector'], im.inputs['Vector'])
        looks.append(im.outputs['Color'])
    mix = N('ShaderNodeMix'); mix.data_type = 'RGBA'
    L(t, mix.inputs['Factor']); L(looks[0], mix.inputs[6]); L(looks[1], mix.inputs[7])
    rgb = N('ShaderNodeSeparateColor'); L(mix.outputs[2], rgb.inputs['Color'])
    rho, fl, ht = rgb.outputs['Red'], rgb.outputs['Green'], rgb.outputs['Blue']
    bl = p.get('billow')
    if bl:
        # Smoke E10: pyroclastic billows, `billow` [amount, metres, octaves]: the soot pushed up and down by a fractal
        # noise before the edge's remap, so the surface the remap draws carries lumps on the sim's lumps, down to the
        # noise's finest octave (E9's lobes were one size and smooth). Gated by the soot itself, so clear air stays clear
        ba, bs, bo = bl
        nbl = N('ShaderNodeTexNoise'); nbl.inputs['Scale'].default_value = 1.0 / bs
        nbl.inputs['Detail'].default_value = bo; nbl.inputs['Roughness'].default_value = 0.58
        nbl.inputs['Distortion'].default_value = 0.0
        L(mp.outputs['Vector'], nbl.inputs['Vector'])
        gate = math_('MINIMUM', math_('DIVIDE', rho, 0.06), 1.0)
        rho = math_('MAXIMUM', math_('ADD', rho, math_('MULTIPLY', math_('MULTIPLY_ADD', nbl.outputs['Fac'], 2.0 * ba, -ba), gate)), 0.0)
    if p.get('edge'):
        # crisper billows (p4's critics: "mushy, soft edges"): the soot remapped by a smoothstep, so thin margins drop
        # to clear air and the lobes keep firm outlines
        lo, hi = p['edge']
        er = N('ShaderNodeMapRange'); er.interpolation_type = 'SMOOTHSTEP'; er.clamp = True
        er.inputs['From Min'].default_value = lo; er.inputs['From Max'].default_value = hi
        L(rho, er.inputs['Value'])
        rho = er.outputs['Result']
    dens = math_('MULTIPLY', rho, p.get('density', 6.0))
    b = p.get('breakup', 0.0)
    if b:
        # uneven soot: the density scaled by a noise between 1 - b and 1 + b, so the lumps differ inside and thin unevenly
        nb = N('ShaderNodeTexNoise'); nb.inputs['Scale'].default_value = 1.0 / p.get('breakup_scale', 0.6)
        nb.inputs['Detail'].default_value = p.get('breakup_octaves', 2.0); nb.inputs['Distortion'].default_value = 0.8
        L(mp.outputs['Vector'], nb.inputs['Vector'])
        dens = math_('MULTIPLY', dens, math_('MAXIMUM', math_('MULTIPLY_ADD', nb.outputs['Fac'], 2.0 * b, 1.0 - b), 0.0))
    gr = p.get('grain')
    if gr:
        # Smoke E10: a fine grain in the soot, `grain` [amount, metres, octaves]: the texture of turbulence on a lit
        # billow, far below the grid's size
        ng = N('ShaderNodeTexNoise'); ng.inputs['Scale'].default_value = 1.0 / gr[1]
        ng.inputs['Detail'].default_value = gr[2] if len(gr) > 2 else 3.0; ng.inputs['Distortion'].default_value = 0.4
        L(mp.outputs['Vector'], ng.inputs['Vector'])
        dens = math_('MULTIPLY', dens, math_('MAXIMUM', math_('MULTIPLY_ADD', ng.outputs['Fac'], 2.0 * gr[0], 1.0 - gr[0]), 0.0))
    L(dens, vol.inputs['Density'])
    # the flame: black-body colour by how hot, as bright as it is strong; the heat a dull red glow in the smoke above it
    tk = math_('MULTIPLY_ADD', fl, p.get('hot', 1700.0) - p.get('cool', 1000.0), p.get('cool', 1000.0))
    bb = N('ShaderNodeBlackbody'); L(tk, bb.inputs['Temperature'])
    L(bb.outputs['Color'], vol.inputs['Emission Color'])
    # flames only where the gas is truly burning: nothing below `flame_floor`, rising to full strength
    fo = p.get('flame_floor', 0.3)
    fk = math_('MAXIMUM', math_('DIVIDE', math_('SUBTRACT', fl, fo), 1.0 - fo), 0.0)
    em = math_('MULTIPLY', math_('POWER', fk, p.get('flame_gamma', 1.3)), p.get('strength', 40.0))
    tg = p.get('tongues', 0.0)
    if tg:
        # licking tongues: the flame's glow cut by a noise stretched upward, so it breaks into filaments
        mt = N('ShaderNodeMapping'); L(mp.outputs['Vector'], mt.inputs['Vector'])
        mt.inputs['Scale'].default_value = (1.0, 1.0, 0.35)
        nf = N('ShaderNodeTexNoise'); nf.inputs['Scale'].default_value = 1.0 / p.get('tongue_scale', 0.22)
        nf.inputs['Detail'].default_value = p.get('tongue_octaves', 3.0); nf.inputs['Distortion'].default_value = 1.5
        L(mt.outputs['Vector'], nf.inputs['Vector'])
        if p.get('tongue_edge'):
            lo, hi = p['tongue_edge']
            tr = N('ShaderNodeMapRange'); tr.interpolation_type = 'SMOOTHSTEP'; tr.clamp = True
            tr.inputs['From Min'].default_value = lo; tr.inputs['From Max'].default_value = hi
            tr.inputs['To Min'].default_value = 1.0 - tg; tr.inputs['To Max'].default_value = 1.0 + tg
            L(nf.outputs['Fac'], tr.inputs['Value'])
            em = math_('MULTIPLY', em, tr.outputs['Result'])
        else:
            em = math_('MULTIPLY', em, math_('MAXIMUM', math_('MULTIPLY_ADD', nf.outputs['Fac'], 2.0 * tg, 1.0 - tg), 0.0))
    if p.get('heat_glow', 0.0):
        em = math_('MULTIPLY_ADD', math_('MULTIPLY', ht, rho), p['heat_glow'], em)
    L(em, vol.inputs['Emission Strength'])
    vol.inputs['Blackbody Intensity'].default_value = 0.0
    L(vol.outputs['Volume'], out.inputs['Volume'])
    me.materials.append(m)
    return [ob]
