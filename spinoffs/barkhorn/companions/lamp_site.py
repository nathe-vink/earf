"""The site's lit lamp pictures, honest (the coordinator, 2026-11-09: the faked ones are pulled). Each lamp is lit by its
own light at its real output, on one photometric scale, on a pale paper sweep lit by real studio lights; nothing hidden
from the camera, from reflections or from view through the acrylic, nothing linked, every part casting shadows.

    python3.11 spinoffs/barkhorn/companions/lamp_site.py FRAME [--samples N] [--scale S]

FRAME:
    dome-<colour>   Hemisphere lit, 1600 x 2000 (4:5)          lamps-domes   the eight in a row, 2400 x 800 (3:1)
    orb-<colour>    Core lit (as drawn: frosted inside), 4:5     lamps-orbs    the eight in a row, 2400 x 800
<colour> is the site's key: red amber? see COLOURS. Output: renders/2026-11-09/barkhorn/lamp-site/FRAME.png.
Env: LAMP_OUT (output path), STUDIO (scale of every studio light, default 1), AUDIT=1 (the card audit, no render).

The lamps as drawn: Hemisphere v3 (a 3 mm stock tint R 100-97, a 6 mm clear shell R 96-90, the opal liner R 89-86, its
edge 4 inside the rim, the CAD's rim, collar and hub; the liner the CAD's neutral opal), its Bridgelux Vero SE 10 at
2700 K; Core A (one 9 mm tinted ball, its inside bead-blasted, the 40 port over the window) on its signed dock, its LED
at 2700 K (the warm end of its warm-dim range).

One photometric scale (lamp_pictures.py, round 13): 0.0065 W of Blender power for each lumen.
  Hemisphere: ~575 lm at the COB (crystal.py), 85 % out: ~490 lm down through the mouth (a 0.17 m disc at the mouth,
  92 deg spread, 3.2 W), and the reflector's spill, a quarter (145 lm), out through the liner (its lit face, ruling 3's
  exception: 11.5 W/m2 on average over its 0.041 m2 outer face, both ways, brighter at the crown).
  Core: ~620 lm, ~560 lm out of the ball (3.6 W), as the lit frosted face (ruling 3's exception): 28.7 W/m2 on its
  0.0633 m2, both ways, its colour through the whole 9 mm wall.
The thin shells pass shadow rays at their own transmission (lamp_pictures.thin_shadow), so the lamps light the set.
"""
import math, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
OUT = os.path.join(ROOT, 'renders', '2026-11-09', 'barkhorn', 'lamp-site')
WLM = 3.2 / 490.0                                     # Blender W per lumen (the one scale)
CCT = int(os.environ.get('LAMP_CCT', '2700'))
# item 90 (the coordinator's open proposal to the owner, PROPOSAL): each tint at its own colour temperature
CCT_PER_TINT = {'blue': 5700, 'violet': 4000}         # the rest 2700
# the site's colour keys (web.py HABITAT) to the tints
COLOURS = {'red': 'Ember', 'orange': 'Dust', 'amber': 'Acid', 'green': 'Poison', 'blue': 'Ice', 'violet': 'Haze',
           'ice': 'Fog', 'black': 'Smoke dark'}
ROW = ['red', 'orange', 'amber', 'green', 'blue', 'violet', 'ice', 'black']        # spectrum order, Ember to Smoke


def blackbody(T):
    sys.path.insert(0, HERE)
    import lamp_pictures as LP
    return LP.blackbody(T)


def build(frame, samples, scale):
    import bpy, bmesh
    from mathutils import Vector
    sys.path.insert(0, os.path.join(HERE, 'strata'))
    import scene as SC
    bpy.ops.wm.read_factory_settings(use_empty=True)
    MM = SC.MM
    pertint = os.environ.get('CCT_MODE') == 'pertint'
    def bbt(tint):
        return blackbody(CCT_PER_TINT.get(tint, 2700) if pertint else CCT)
    bb = blackbody(CCT)
    kind0 = 'dome' if frame.startswith('lamps-domes') else 'orb' if frame.startswith('lamps-orbs') else frame.split('-')[0]
    # the studio's brightness and the exposure move together, so the paper holds its tone while the lamp, at its real
    # output, comes out of clipping: a brighter studio, one scale
    K = float(os.environ.get('STUDIO', {'dome': '2.0', 'orb': '8.0', 'lamps': '4.0'}[kind0]))
    # round 2 (the gate, 2026-11-09, wf_a02e1a2a-b5e): the camera 2 EV down, the studio unchanged, so the faces leave
    # AgX's shoulder and hold their tint; the paper falls to about L 0.5-0.6 (both heroes' papers K x 2^EV match)
    EVD = {'dome': '-3.0', 'orb': '-5.0'}[kind0]

    def acrylic(nm, rough, tname, loading=1.0):
        return SC.acrylic_material(nm, [(-1e4, 1e4, tname)], rough, 'polished', loading=loading, scratch=0.0, bond=False)

    def shell_T(tint, loading, mm):
        return tuple(math.exp(-a * mm / 1000.0) * 0.96 for a in SC.absorption(tint, loading))

    def thin_shadow(m, T):
        nt = m.node_tree; outn = next(n for n in nt.nodes if n.type == 'OUTPUT_MATERIAL')
        prev = outn.inputs['Surface'].links[0].from_node
        lp = nt.nodes.new('ShaderNodeLightPath'); tb = nt.nodes.new('ShaderNodeBsdfTransparent')
        tb.inputs['Color'].default_value = (*T, 1); mx = nt.nodes.new('ShaderNodeMixShader')
        nt.links.new(lp.outputs['Is Shadow Ray'], mx.inputs[0]); nt.links.new(prev.outputs[0], mx.inputs[1])
        nt.links.new(tb.outputs[0], mx.inputs[2]); nt.links.new(mx.outputs[0], outn.inputs['Surface'])
        return m

    def add_emission(m, color, strength_node_or_value):
        nt = m.node_tree; outn = next(n for n in nt.nodes if n.type == 'OUTPUT_MATERIAL')
        prev = outn.inputs['Surface'].links[0].from_node
        em = nt.nodes.new('ShaderNodeEmission'); em.inputs['Color'].default_value = (*color, 1)
        if isinstance(strength_node_or_value, (int, float)):
            em.inputs['Strength'].default_value = strength_node_or_value
        else:
            nt.links.new(strength_node_or_value, em.inputs['Strength'])
        ad = nt.nodes.new('ShaderNodeAddShader')
        nt.links.new(prev.outputs[0], ad.inputs[0]); nt.links.new(em.outputs[0], ad.inputs[1])
        nt.links.new(ad.outputs[0], outn.inputs['Surface'])
        m.cycles.emission_sampling = 'FRONT_BACK'
        return m

    def sphere(nm, r, c, mat, inward=False, cut=None, hole=None, hole_below=None):
        bm = bmesh.new()
        bmesh.ops.create_uvsphere(bm, u_segments=256, v_segments=128, radius=r * MM)
        if cut is not None:
            bmesh.ops.delete(bm, geom=[v for v in bm.verts if v.co.z < cut * MM - 1e-9], context='VERTS')
        if hole is not None:
            bmesh.ops.delete(bm, geom=[v for v in bm.verts if math.hypot(v.co.x, v.co.y) < hole * MM and v.co.z > 0],
                             context='VERTS')
        if hole_below is not None:
            bmesh.ops.delete(bm, geom=[v for v in bm.verts if math.hypot(v.co.x, v.co.y) < hole_below * MM and v.co.z < 0],
                             context='VERTS')
        if inward:
            bmesh.ops.reverse_faces(bm, faces=bm.faces)
        for f in bm.faces:
            f.smooth = True
        me = bpy.data.meshes.new(nm); bm.to_mesh(me); bm.free()
        ob = bpy.data.objects.new(nm, me); bpy.context.scene.collection.objects.link(ob)
        ob.location = c; me.materials.append(mat)
        return ob

    def part(folder, name, mat, at):
        # the meshes ship with the branch (lamp-site-meshes/, a copy of the fabkit builds), so a helper needs no CAD venv
        path = os.path.join(HERE, 'lamp-site-meshes', folder, 'stl', name + '.stl')
        ob = SC.stl(path if os.path.exists(path) else os.path.join(HERE, folder, 'stl', name + '.stl'), mat, name)
        ob.location = (ob.location[0] + at[0], ob.location[1] + at[1], ob.location[2] + at[2])
        return ob

    black_acrylic = SC.principled('black-acrylic', '#0A0A0B', 0.04)
    an = SC.anodised()
    steel = SC.principled('steel', '#C9C9C6', 0.25, 1.0, bump=(2500.0, 0.6))
    cap = SC.principled('cap', '#3A3A3E', 0.45, metallic=0.3, bump=(4000.0, 0.15))

    def hemisphere(tint, x, rim_z, y=0.0):
        """Hemisphere v3 as drawn, lit, its rim's centre at (x, y, rim_z)."""
        tname = COLOURS[tint]; bb = bbt(tint)
        c = (x, y, rim_z); H = 48.2
        Tt, Tc = shell_T(tname, 1.0, 1.5), shell_T('Clear', 1.0, 3.0)
        sphere(f'tint-{tint}', 100.0, c, thin_shadow(acrylic(f'tint-{tint}', 0.0, tname), Tt), cut=0.0, hole=H)
        sphere(f'tint-in-{tint}', 97.0, c, thin_shadow(acrylic(f'tint-in-{tint}', 0.0, tname), Tt), inward=True, cut=0.0, hole=H)
        sphere(f'clear-{tint}', 96.0, c, thin_shadow(acrylic(f'clear-{tint}', 0.0, 'Clear'), Tc), cut=4.0, hole=H)
        sphere(f'clear-in-{tint}', 90.0, c, thin_shadow(acrylic(f'clear-in-{tint}', 0.0, 'Clear'), Tc), inward=True, cut=4.0, hole=H)
        oc_ = (0.93, 0.93, 0.92)                      # the CAD's neutral opal
        def opal(nm):
            m = bpy.data.materials.new(nm); m.use_nodes = True; nt = m.node_tree; nt.nodes.clear()
            o = nt.nodes.new('ShaderNodeOutputMaterial'); tr = nt.nodes.new('ShaderNodeBsdfTranslucent')
            gl = nt.nodes.new('ShaderNodeBsdfGlossy'); gl.inputs['Roughness'].default_value = 0.08
            df = nt.nodes.new('ShaderNodeBsdfDiffuse'); m1 = nt.nodes.new('ShaderNodeMixShader'); m1.inputs[0].default_value = 0.5
            m2 = nt.nodes.new('ShaderNodeMixShader'); m2.inputs[0].default_value = 0.06
            tr.inputs['Color'].default_value = (*oc_, 1); df.inputs['Color'].default_value = (*(v * 0.97 for v in oc_), 1)
            nt.links.new(df.outputs[0], m1.inputs[1]); nt.links.new(tr.outputs[0], m1.inputs[2])
            nt.links.new(m1.outputs[0], m2.inputs[1]); nt.links.new(gl.outputs[0], m2.inputs[2]); nt.links.new(m2.outputs[0], o.inputs['Surface'])
            return m
        oc = 4.0
        lit = opal(f'opal-lit-{tint}'); nt = lit.node_tree
        # (round 2, the gate: the liner passed all 145 lm; a real opal of about 55 % passes about half outward, the rest
        # back into the shade and out through the mouth)
        S0 = 145.0 * float(os.environ.get('OPAL_T', '0.55')) * WLM / (2 * 0.041)
        tc = nt.nodes.new('ShaderNodeTexCoord'); sx = nt.nodes.new('ShaderNodeSeparateXYZ'); nt.links.new(tc.outputs['Object'], sx.inputs[0])
        gz = nt.nodes.new('ShaderNodeMapRange'); gz.clamp = True
        gz.inputs['From Min'].default_value = oc * MM; gz.inputs['From Max'].default_value = 0.075
        gz.inputs['To Min'].default_value = 0.6 * S0; gz.inputs['To Max'].default_value = 1.4 * S0
        nt.links.new(sx.outputs['Z'], gz.inputs['Value'])
        add_emission(lit, tuple(bb[i] * oc_[i] for i in range(3)), gz.outputs['Result'])
        sphere(f'opal-{tint}', 89.0, c, lit, cut=oc, hole=H)
        sphere(f'opal-in-{tint}', 86.0, c, opal(f'opal-in-{tint}'), inward=True, cut=oc, hole=H)
        part('out-dome-pendant', 'rim', acrylic(f'rim-{tint}', 0.6, tname, 0.5), c)
        for nm in ('collar', 'clamp', 'crown', 'gland', 'hub'):
            part('out-dome-pendant', nm, cap, c)
        part('out-dome-pendant', 'ring', SC.principled('peek', '#151515', 0.6), c)
        part('out-dome-pendant', 'pins', steel, c)
        part('out-dome-pendant', 'gaskets', SC.principled('silicone', '#111111', 0.7), c)
        part('out-dome-pendant', 'reflector', steel, c)
        part('out-dome-pendant', 'cord', SC.principled('braid', '#121212', 0.75, bump=(1200.0, 0.5)), c)
        ld = bpy.data.lights.new(f'cob-{tint}', 'AREA'); ld.shape = 'DISK'; ld.size = 0.17; ld.energy = 490.0 * WLM
        ld.spread = math.radians(92.0); ld.color = bb
        ob = bpy.data.objects.new(f'cob-{tint}', ld); bpy.context.scene.collection.objects.link(ob)
        ob.location = (x, y, rim_z + 0.004)

    def core(tint, x, floor_z, y=0.0, rot=0.0):
        """Core A as drawn, on its dock, lit, the dock's underside on floor_z at (x, y)."""
        tname = COLOURS[tint]; bb = bbt(tint)
        z0 = floor_z + 0.0065                         # the dock's underside on the floor (as lamp_pictures: the CAD's
                                                      # dock underside sits 6.5 below its origin)
        objs = []
        for nm, m in (('dock', black_acrylic), ('base', black_acrylic), ('ring', an), ('seat', SC.principled('si', '#111111', 0.6)),
                      ('dock-cable', SC.principled('braid', '#121212', 0.75, bump=(1200.0, 0.5))), ('grommet', an)):
            objs.append(part('out-orb-table', nm, m, (x, y, z0)))
        zc = z0 + 100.45 * MM
        T9 = shell_T(tname, 1 / 3, 9.0)
        sphere(f'ball-{tint}', 80.0, (x, y, zc), thin_shadow(acrylic(f'ball-{tint}', 0.0, tname, 1 / 3), (0.96, 0.96, 0.96)), hole_below=20.0)
        fm = acrylic(f'frost-{tint}', 0.6, tname, 1 / 3)
        nt = fm.node_tree; outn = next(n for n in nt.nodes if n.type == 'OUTPUT_MATERIAL'); glass = outn.inputs['Surface'].links[0].from_node
        tl = nt.nodes.new('ShaderNodeBsdfTranslucent'); tl.inputs['Color'].default_value = (0.9, 0.9, 0.9, 1)
        mx = nt.nodes.new('ShaderNodeMixShader'); mx.inputs[0].default_value = 0.5
        nt.links.new(glass.outputs[0], mx.inputs[1]); nt.links.new(tl.outputs[0], mx.inputs[2]); nt.links.new(mx.outputs[0], outn.inputs['Surface'])
        S = 560.0 * WLM / (2 * 0.0633)
        add_emission(fm, tuple(bb[i] * T9[i] / 0.96 for i in range(3)), S)
        sphere(f'frost-{tint}', 71.0, (x, y, zc), fm, inward=True, hole_below=20.0)
        if rot:
            for o in objs:   # turn the dock's cable away from the camera, about the lamp's axis (the parts' origin)
                o.rotation_euler[2] = math.radians(rot)

    # --- the set: a pale paper sweep (floor, cove, back) and real studio lights out of frame, unlinked ---------------
    paper = SC.principled('paper', '#EDE8E1', 0.9)
    bm = bmesh.new(); Wd = 6.0; R = 0.6; yb = 1.0          # the floor to y = yb - R, a cove of radius R, the back at y = yb
    verts = []
    prof = [(-3.0, 0.0), (yb - R, 0.0)] + [(yb - R + R * math.sin(a), R - R * math.cos(a)) for a in [i * math.pi / 2 / 16 for i in range(1, 17)]] + [(yb, 3.0)]
    for (py, pz) in prof:
        verts.append((bm.verts.new((-Wd / 2, py, pz)), bm.verts.new((Wd / 2, py, pz))))
    for i in range(len(verts) - 1):
        a, b = verts[i], verts[i + 1]
        bm.faces.new((a[0], a[1], b[1], b[0]))
    for f in bm.faces:
        f.smooth = True
    me = bpy.data.meshes.new('sweep'); bm.to_mesh(me); bm.free()
    so = bpy.data.objects.new('sweep', me); bpy.context.scene.collection.objects.link(so); me.materials.append(paper)
    SC.world(color='#C8C4BE', strength=0.02 * K)
    # round 2 (the gate): the studio at 3000 K, and the camera's white point at 3000 K; the lamps stay at 2700 K (spec)
    key = SC.area('key', (-1.4, -1.6, 1.9), (0, 0, 0), (1.2, 1.2), 60.0 * K, '#FFF4E8'); key.data.shape = 'ELLIPSE'
    key.data.color = blackbody(3000)
    key.rotation_euler = (Vector((0, 0.1, 0.5)) - key.location).to_track_quat('-Z', 'Y').to_euler()
    fill = SC.area('fill', (1.8, -1.2, 1.2), (0, 0, 0), (1.6, 1.6), 20.0 * K, '#EEF2F8'); fill.data.shape = 'ELLIPSE'
    fill.data.color = blackbody(3000)
    fill.rotation_euler = (Vector((0, 0.1, 0.4)) - fill.location).to_track_quat('-Z', 'Y').to_euler()

    # --- the frames ---------------------------------------------------------------------------------------------
    kind, _, tint = frame.partition('-')
    if frame.startswith('lamps-domes'):
        # round 2 (the gate: the pools merged into one bar that read as LED strip; small domes under a bare third of
        # cable): framed above the floor, the domes larger, the cables cropped; '-7' leaves Smoke out, re-spaced
        W, H = 2400, 800
        row = ROW[:7] if frame.endswith('-7') else ROW
        for i, t in enumerate(row):
            hemisphere(t, (i - (len(row) - 1) / 2) * 0.25, 0.45, y=0.0)
        cam = ((0.0, -2.9, 0.47), (0.0, 0.0, 0.45), 50.0)
    elif frame.startswith('lamps-orbs'):
        # round 2 (the gate): the camera 15 deg up, so each lamp's glow on the paper is its own; '-7' leaves Smoke out
        W, H = 2400, 800
        row = ROW[:7] if frame.endswith('-7') else ROW
        for i, t in enumerate(row):
            core(t, (i - (len(row) - 1) / 2) * 0.22, 0.0)
        cam = ((0.0, -4.4, 0.12 + 4.4 * math.tan(math.radians(15))), (0.0, 0.0, 0.10), 85.0)
    elif kind == 'dome':
        W, H = 1600, 2000
        hemisphere(tint, 0.0, 0.50)                    # the rim 500 above the paper: the dome and its pool in one frame
        cam = ((0.08, -1.25, 0.45), (0.0, 0.0, 0.36), 50.0)
    elif kind == 'orb':
        W, H = 1600, 2000
        core(tint, 0.0, 0.0)
        cam = ((0.10, -0.95, 0.22), (0.0, 0.0, 0.11), 70.0)
    else:
        raise SystemExit('unknown frame ' + frame)
    SC.render_settings(W, H, samples, scale, exposure=float(os.environ.get('EV', EVD)), look=os.environ.get('LOOK', 'AgX - Punchy'))   # round 2: AgX Punchy (the gate)
    sc = bpy.context.scene
    sc.cycles.caustics_refractive = True; sc.cycles.sample_clamp_indirect = 20.0; sc.cycles.blur_glossy = 1.0
    vs = sc.view_settings; vs.use_white_balance = True; vs.white_balance_temperature = float(os.environ.get('WB', '3000'))
    vs.white_balance_tint = 0.0
    SC.camera(cam[0], cam[1], lens=cam[2], fstop=8.0)
    if os.environ.get('AUDIT'):
        hidden = [o for o in sc.objects if o.type == 'MESH' and not o.visible_camera]
        print('AUDIT', frame, 'hidden', [o.name for o in hidden],
              'no-shadow', [o.name for o in sc.objects if o.type == 'MESH' and not o.visible_shadow],
              'lights', [(o.name, o.data.type, round(o.data.energy, 3)) for o in sc.objects if o.type == 'LIGHT'])
        return
    os.makedirs(OUT, exist_ok=True)
    sc.render.filepath = os.environ.get('LAMP_OUT') or os.path.join(OUT, frame + '.png')
    bpy.ops.render.render(write_still=True)
    # the scene-linear EXR beside the PNG, so exposure and look can change without a re-render (the coordinator)
    if os.environ.get('EXR', '1') == '1':
        img = bpy.data.images['Render Result']; fmt = sc.render.image_settings
        fmt.file_format = 'OPEN_EXR'; fmt.color_depth = '16'; fmt.exr_codec = 'DWAA'
        img.save_render(os.path.splitext(sc.render.filepath)[0] + '.exr', scene=sc)


if __name__ == '__main__':
    a = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else sys.argv[1:]
    build(a[0], int(a[a.index('--samples') + 1]) if '--samples' in a else 256,
          float(a[a.index('--scale') + 1]) if '--scale' in a else 1.0)
