"""Stock-tint proof (the owner, 2026-11-01: "I like the darker colors"; the line takes stock sheet's deeper tints).
Core (the 160 ball, a 9 mm shell frosted inside, on its base and dock) and Hemisphere (the 200 shade: a 9 mm tinted
shell, a 3 mm opal liner, a 3 mm tinted skin) in stock TruCast 2423 Red (Ember) and 2092 Green (Poison), lit and
unlit, with scene.py's calibrated acrylic (Beer-Lambert by ray length from the 3 mm chart figure). Eight frames on one
sheet.

    python3.11 spinoffs/barkhorn/companions/strata/tint_proof.py FRAME --out PATH [--samples N]   # one frame
    python3 spinoffs/barkhorn/companions/strata/tint_proof.py --all [sheet|hemi-v2|core-options] [--samples N]

FRAME is {core,hemi}-{ember,poison}-{lit,unlit}. The geometry is the CAD's numbers, built procedurally (spheres), not
the CAD's meshes: a proof of the tint at real thickness, not a hero.
"""
import math, os, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..', '..'))
OUT = os.path.join(ROOT, 'renders', '2026-11-01', 'barkhorn', 'tint-proof')
FRAMES = [f'{p}-{t}-{l}' for p in ('core', 'hemi') for t in ('ember', 'poison') for l in ('unlit', 'lit')]
STOCK = {'ember': ('Ember stock', '2423', 14.1, '#D8283A'), 'poison': ('Poison stock', '2092', 18.6, '#0DA41C')}


def build(frame, out, samples):
    import bpy, bmesh
    sys.path.insert(0, HERE)
    import stack as S
    import scene as SC
    prod, tint, mode, *var = frame.split('-')
    var = var[0] if var else ''
    name, code, lt, hue = STOCK[tint]
    S.TINTS[name] = (code, lt, hue)
    lit = mode == 'lit'
    bpy.ops.wm.read_factory_settings(use_empty=True)
    MM = SC.MM

    def sphere(nm, r, z, mat, inward=False, cut=None):
        bm = bmesh.new()
        bmesh.ops.create_uvsphere(bm, u_segments=192, v_segments=96, radius=r * MM)
        if cut is not None:                       # keep the part above z = cut (mm, sphere frame)
            bmesh.ops.delete(bm, geom=[v for v in bm.verts if v.co.z < cut * MM - 1e-9], context='VERTS')
        if inward:
            bmesh.ops.reverse_faces(bm, faces=bm.faces)
        for f in bm.faces:
            f.smooth = True
        me = bpy.data.meshes.new(nm); bm.to_mesh(me); bm.free()
        ob = bpy.data.objects.new(nm, me); bpy.context.scene.collection.objects.link(ob)
        ob.location = (0, 0, z * MM); me.materials.append(mat)
        return ob

    def tinted(nm, rough, which=None, loading=1.0):
        return SC.acrylic_material(nm, [(-1000.0, 1000.0, which or name)], rough, 'polished', loading=loading, scratch=0.3,
                                   bond=False)
    # the 2026-11-01 options: 'v2' Hemisphere's shell clear (0000), only the 3 mm skin tinted; 'held' Core's 9 mm ball
    # at a third of the chip's dye per mm (a custom pour, or stock 3/8 in sheet if the maker holds LT at thickness);
    # 'two' Core's ball in two layers, 6 mm clear outside and a 3 mm stock skin inside, 1 mm apart
    ld = 1.0 / 3.0 if var == 'held' else 1.0

    table = SC.principled('table', '#8C8780', 0.6)
    SC.plane('table', (4, 4), (0, 0, 0), (0, 0, 0), table)
    SC.plane('wall', (4, 3), (0, 0.9, 1.5), (90, 0, 0), SC.principled('wall', '#D9D4CB', 0.9))
    if prod == 'core':
        dock_h, base_h, ring = 8.0, 30.0, 8.0
        zc = dock_h + base_h + ring + math.sqrt(80.0 ** 2 - 50.0 ** 2)
        black = SC.principled('black-acrylic', '#0B0B0C', 0.05)
        bpy.ops.mesh.primitive_cylinder_add(vertices=128, radius=0.075, depth=dock_h * MM, location=(0, 0, dock_h / 2 * MM))
        bpy.context.object.data.materials.append(black)
        bpy.ops.mesh.primitive_cylinder_add(vertices=128, radius=0.060, depth=base_h * MM, location=(0, 0, (dock_h + base_h / 2) * MM))
        bpy.context.object.data.materials.append(black)
        bpy.ops.mesh.primitive_cylinder_add(vertices=128, radius=0.060, depth=ring * MM, location=(0, 0, (dock_h + base_h + ring / 2) * MM))
        bpy.context.object.data.materials.append(SC.anodised())
        if var == 'two':
            sphere('ball-out', 80.0, zc, tinted('ball-out', 0.0, 'Clear'))
            sphere('ball-out-in', 74.0, zc, tinted('ball-out-in', 0.0, 'Clear'), inward=True)
            sphere('skin-out', 73.0, zc, tinted('skin-out', 0.0))
            sphere('skin-in', 70.0, zc, tinted('skin-frost', 0.55), inward=True)
        else:
            sphere('ball-out', 80.0, zc, tinted('ball-out', 0.0, loading=ld))
            sphere('ball-in', 71.0, zc, tinted('ball-frost', 0.55, loading=ld), inward=True)      # the inside bead-blasted
        if lit:   # the 200 lm warm LED under the window, up into the ball, and the light the frost passes on
            SC.point('led', (0, 0, (zc - 62) * MM), 2.2, '#FFC98A', radius=0.012, caustic=False)
        cam, tgt, lens = (0.0, -0.62, 0.20), (0, 0, zc * 0.9 * MM), 85
    else:
        rim = 300.0                               # the rim 300 above the table: the shade and its pool in one frame
        shw = 'Clear' if var in ('v2', 'v3') else None
        if var == 'v3':     # the tint outside: a 3 mm stock-tint shell over a 6 mm clear one, the opal, a clear skin
            sphere('tint-out', 100.0, rim, tinted('tint', 0.0), cut=0.0)
            sphere('tint-in', 97.0, rim, tinted('tint-in', 0.0), inward=True, cut=0.0)
            sphere('shell-out', 96.0, rim, tinted('shell', 0.0, 'Clear'), cut=0.0)
            sphere('shell-in', 90.0, rim, tinted('shell-in', 0.0, 'Clear'), inward=True, cut=0.0)
        else:
            sphere('shell-out', 100.0, rim, tinted('shell', 0.0, shw), cut=0.0)
            sphere('shell-in', 91.0, rim, tinted('shell-in', 0.0, shw), inward=True, cut=0.0)
        opal = bpy.data.materials.new('opal'); opal.use_nodes = True
        nt = opal.node_tree; nt.nodes.clear()
        o = nt.nodes.new('ShaderNodeOutputMaterial'); tr = nt.nodes.new('ShaderNodeBsdfTranslucent')
        df = nt.nodes.new('ShaderNodeBsdfDiffuse'); mx = nt.nodes.new('ShaderNodeMixShader'); mx.inputs[0].default_value = 0.45
        tr.inputs['Color'].default_value = (0.92, 0.92, 0.9, 1); df.inputs['Color'].default_value = (0.9, 0.9, 0.88, 1)
        nt.links.new(df.outputs[0], mx.inputs[1]); nt.links.new(tr.outputs[0], mx.inputs[2]); nt.links.new(mx.outputs[0], o.inputs['Surface'])
        sphere('liner', 88.5, rim, opal, cut=4.0)
        skw = 'Clear' if var == 'v3' else None
        sphere('skin-out', 86.0, rim, tinted('skin', 0.0, skw), cut=0.0)
        sphere('skin-in', 83.0, rim, tinted('skin-in', 0.0, skw), inward=True, cut=0.0)
        # the rim ring that closes the layers (tinted), the crown and cap in black anodised aluminium, the cord
        bpy.ops.mesh.primitive_torus_add(major_radius=0.0915, minor_radius=0.0045, location=(0, 0, rim * MM))
        bpy.context.object.data.materials.append(tinted('rim', 0.0, shw))
        an = SC.anodised()
        bpy.ops.mesh.primitive_cylinder_add(vertices=96, radius=0.040, depth=0.0115, location=(0, 0, (rim + 106) * MM))
        bpy.context.object.data.materials.append(an)
        bpy.ops.mesh.primitive_cylinder_add(vertices=64, radius=0.020, depth=0.014, location=(0, 0, (rim + 119) * MM))
        bpy.context.object.data.materials.append(an)
        bpy.ops.mesh.primitive_cylinder_add(vertices=24, radius=0.003, depth=1.0, location=(0, 0, (rim + 126) * MM + 0.5))
        bpy.context.object.data.materials.append(SC.principled('cord', '#111111', 0.7))
        if lit:   # the COB, 22 up the bore, about 500 lm out of the fitting, straight down; the reflector's spill
            sp = bpy.data.lights.new('cob', 'SPOT'); sp.energy = 9.0; sp.spot_size = math.radians(92); sp.spot_blend = 0.3
            sp.color = SC.hex_lin('#FFD2A0'); sp.shadow_soft_size = 0.012
            ob = bpy.data.objects.new('cob', sp); bpy.context.scene.collection.objects.link(ob)
            ob.location = (0, 0, (rim + 60) * MM)
            SC.point('spill', (0, 0, (rim + 55) * MM), 1.6, '#FFD2A0', radius=0.02, caustic=False)
        cam, tgt, lens = (0.0, -0.95, 0.30), (0, 0, 0.27), 70
    if lit:
        SC.world(strength=0.02)
        SC.area('fill', (-1.0, -1.0, 1.5), (55, 0, -40), (1.0, 1.0), 6.0, '#A9B8CF')
        exposure = 0.0
    else:
        SC.world(strength=0.5, color='#DCDCDC')
        SC.area('key', (-0.9, -0.8, 1.2), (55, 0, -48), (1.2, 1.2), 140.0, '#FFF6EA')
        SC.area('rim', (0.8, 0.4, 0.6), (70, 0, 120), (0.4, 1.0), 40.0, '#FFFFFF')
        exposure = 0.0
    SC.render_settings(600, 600, samples, 1.0, exposure=exposure, look='AgX - Medium High Contrast')
    # Core has no diffuse surface behind its glass; Hemisphere's opal liner sits behind the shell and the skin, so it is
    # lit only along refracted (caustic) paths: on for Hemisphere (without them the liner renders black)
    bpy.context.scene.cycles.caustics_refractive = prod == 'hemi'
    SC.camera(cam, tgt, lens=lens, fstop=8.0)
    bpy.context.scene.render.filepath = out
    bpy.ops.render.render(write_still=True)


SETS = {'sheet': (FRAMES, 'tint-proof-sheet', 'Stock tints at real thickness: Ember = TruCast 2423 Red, Poison = TruCast '
                   '2092 Green (calibrated from the 3 mm chart, Beer-Lambert by path length)'),
        'hemi-v2': ([f'hemi-{t}-{l}-v2' for t in ('ember', 'poison') for l in ('unlit', 'lit')], 'tint-proof-hemi-v2',
                    'Hemisphere, proposed: the 9 mm shell clear (0000), only the 3 mm skin in stock 2423 / 2092'),
        'hemi-v3': ([f'hemi-{t}-{l}-v3' for t in ('ember', 'poison') for l in ('unlit', 'lit')], 'tint-proof-hemi-v3',
                    'Hemisphere, alternative: the 3 mm stock tint outside (over 6 mm clear), the opal and a clear skin inside'),
        'core-options': ([f'core-{t}-{l}-{v}' for v in ('held', 'two') for t in ('ember', 'poison') for l in ('unlit', 'lit')],
                         'tint-proof-core-options', 'Core: top, the 9 mm ball at 1/3 of the chip\'s dye (stock 3/8 in if held, '
                         'or a custom pour); bottom, two layers: 6 mm clear + 3 mm stock skin')}


def sheet(which='sheet'):
    frames, fname, title = SETS[which]
    from PIL import Image, ImageDraw, ImageFont
    W = 600
    rows = (len(frames) + 3) // 4
    im = Image.new('RGB', (4 * W + 50, rows * (W + 40) + 60), '#F4F1EC')
    d = ImageDraw.Draw(im)
    try:
        f = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 22)
        fs = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 16)
    except OSError:
        f = fs = ImageFont.load_default()
    d.text((20, 18), title, fill='#1C1A18', font=f)
    for i, fr in enumerate(frames):
        p = os.path.join(OUT, fr + '.png')
        x, y = 10 + (i % 4) * (W + 10), 60 + (i // 4) * (W + 40)
        if os.path.exists(p):
            im.paste(Image.open(p).convert('RGB').resize((W, W)), (x, y))
        prod, tint, mode, *var = fr.split('-')
        var = var[0] if var else ''
        what = {'': 'Core, ball 9 mm' if prod == 'core' else 'Hemisphere, 9 + 3 mm tint', 'v2': 'Hemisphere, clear + 3 mm skin',
                'held': 'Core, 9 mm at 1/3 dye', 'two': 'Core, 6 clear + 3 mm skin',
                'v3': 'Hemisphere, 3 mm tint outside'}[var]
        lab = f"{what}  ·  {STOCK[tint][1]}  ·  {mode}"
        d.text((x + 4, y + W + 6), lab, fill='#1C1A18', font=fs)
    path = os.path.join(OUT, fname + '.png')
    im.save(path, optimize=True)
    print(os.path.relpath(path, ROOT))


if __name__ == '__main__':
    a = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else sys.argv[1:]
    if a and a[0] == '--sheet':
        sheet(a[1] if len(a) > 1 else 'sheet')
    elif a and a[0] == '--all':
        os.makedirs(OUT, exist_ok=True)
        which = a[1] if len(a) > 1 and not a[1].startswith('--') else 'sheet'
        spp = a[a.index('--samples') + 1] if '--samples' in a else '96'
        for fr in SETS[which][0]:
            subprocess.run(['python3.11', __file__, fr, '--out', os.path.join(OUT, fr + '.png'), '--samples', spp], check=True)
        sheet(which)
    else:
        build(a[0], os.path.abspath(a[a.index('--out') + 1]), int(a[a.index('--samples') + 1]) if '--samples' in a else 96)
