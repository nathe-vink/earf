"""Product pictures of the lamps as drawn today (2026-11-03): Hemisphere v3, the color outside (b868feeb), and the
cordless Core on its signed dock with the base's notch closed (ef23b82d). For the site's launch-film home and the deck's
light slide. The owner's rule for every light: off by day, on at night, glowing through the acrylic, never thrown down.

    python3.11 spinoffs/barkhorn/companions/lamp_pictures.py FRAME [--samples N] [--scale S]

FRAME is {core,hemi}-{tint}-{day,night}, e.g. core-ice-night. Output: renders/2026-11-03/barkhorn/lamp-pictures/.

How:
- The hardware is the CAD's own meshes (out-orb-table/stl, out-dome-pendant/stl; build them first with fabkit).
- The acrylic layers are built as smooth spheres at the CAD's radii (Core's ball R 80, 9 thick, frosted inside;
  Hemisphere's shade: a 3 mm stock-tint shell R 100 to 97, a 6 mm clear shell R 96 to 90, the opal R 89 to 86), with
  strata/scene.py's calibrated acrylic: Beer-Lambert by path length from the TruCast chart at 3 mm, IOR 1.49.
- At night the glow is an emitter inside the acrylic that only the camera sees (and mirrors): it lights nothing, so no
  light falls on the table or the floor. The room is lit by a dim cool fill.
- By day: a window to the left, its sky and a low sun; the lamp is off.
"""
import math, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
OUT = os.path.join(ROOT, 'renders', '2026-11-03', 'barkhorn', 'lamp-pictures')
CCT = int(os.environ.get('LAMP_CCT', '2700'))       # the LED's colour temperature (K)
LED_W = float(os.environ.get('LED_W', '24.0'))         # Core's LED, about 620 lm at full [E: radiant watts]
COB_W = float(os.environ.get('COB_W', '8.0'))         # Hemisphere's COB beam, about 500 lm out of the fitting [E]
SPILL_W = float(os.environ.get('SPILL_W', '0.35'))    # the reflector's spill onto the opal, about a quarter


def blackbody(T):
    """Linear sRGB of a blackbody at T K, its largest channel 1 (CIE 1931 fits, Wyman 2013)."""
    def g(x, mu, s1, s2):
        return math.exp(-0.5 * ((x - mu) / (s1 if x < mu else s2)) ** 2)
    X = Y = Z = 0.0
    for l in range(380, 781, 5):
        p = 1.0 / ((l * 1e-9) ** 5 * (math.exp(1.4388e-2 / (l * 1e-9 * T)) - 1))
        X += p * (1.056 * g(l, 599.8, 37.9, 31.0) + 0.362 * g(l, 442.0, 16.0, 26.7) - 0.065 * g(l, 501.1, 20.4, 26.2))
        Y += p * (0.821 * g(l, 568.8, 46.9, 40.5) + 0.286 * g(l, 530.9, 16.3, 31.1))
        Z += p * (1.217 * g(l, 437.0, 11.8, 36.0) + 0.681 * g(l, 459.0, 26.0, 13.8))
    X, Z = X / Y, Z / Y
    r = [3.2406 * X - 1.5372 - 0.4986 * Z, -0.9689 * X + 1.8758 + 0.0415 * Z, 0.0557 * X - 0.2040 + 1.0570 * Z]
    m = max(r)
    return tuple(max(v, 0.0) / m for v in r)


TINT = {'ice': 'Ice', 'ember': 'Ember', 'dust': 'Dust', 'acid': 'Acid', 'poison': 'Poison', 'haze': 'Haze', 'fog': 'Fog',
        'smoke': 'Smoke dark'}


def build(frame, samples, scale):
    import bpy, bmesh
    sys.path.insert(0, os.path.join(HERE, 'strata'))
    import scene as SC
    prod, tint, mode, *var = frame.split('-')
    var = var[0] if var else ''
    tname = TINT[tint]
    night = mode == 'night'
    cct = CCT
    bpy.ops.wm.read_factory_settings(use_empty=True)
    MM = SC.MM
    tz = 0.62                                                           # the table's top

    def sphere(nm, r, z, mat, inward=False, cut=None, loc=(0, 0), hole=None):
        bm = bmesh.new()
        bmesh.ops.create_uvsphere(bm, u_segments=256, v_segments=128, radius=r * MM)
        if cut is not None:
            bmesh.ops.delete(bm, geom=[v for v in bm.verts if v.co.z < cut * MM - 1e-9], context='VERTS')
        if hole is not None:                      # the collar's hole at the crown (the CAD's: Ø96.4)
            bmesh.ops.delete(bm, geom=[v for v in bm.verts if math.hypot(v.co.x, v.co.y) < hole * MM and v.co.z > 0],
                             context='VERTS')
        if inward:
            bmesh.ops.reverse_faces(bm, faces=bm.faces)
        for f in bm.faces:
            f.smooth = True
        me = bpy.data.meshes.new(nm); bm.to_mesh(me); bm.free()
        ob = bpy.data.objects.new(nm, me); bpy.context.scene.collection.objects.link(ob)
        ob.location = (loc[0], loc[1], z); me.materials.append(mat)
        return ob

    def acrylic(nm, rough, which=None, loading=1.0):
        return SC.acrylic_material(nm, [(-1e4, 1e4, which or tname)], rough, 'polished', loading=loading, scratch=0.25,
                                   bond=False)

    def light(nm, kind, loc, watts, radius, rot=(0, 0, 0), spot=None):
        """A real light at the LED's colour temperature (round 4, 2026-11-03, the coordinator's brief: the light reaches
        the room through the acrylic; the tint's lit hue is the source's through the glass)."""
        ld = bpy.data.lights.new(nm, kind); ld.energy = watts; ld.shadow_soft_size = radius
        ld.color = blackbody(cct); ld.cycles.is_caustics_light = True
        if spot:
            ld.spot_size = math.radians(spot); ld.spot_blend = 0.6
        ob = bpy.data.objects.new(nm, ld); bpy.context.scene.collection.objects.link(ob)
        ob.location = loc; ob.rotation_euler = [math.radians(a) for a in rot]
        return ob

    def glow(nm, color, strength, z_lo, z_hi, s_lo, s_hi):
        """An emitter whose strength runs from s_lo at z_lo to s_hi at z_hi (object space, m): the light source's side
        brighter, as a lamp lit from one point is (round 1's flat fill read as opal plastic)."""
        m = bpy.data.materials.new(nm); m.use_nodes = True
        nt = m.node_tree; nt.nodes.clear()
        o = nt.nodes.new('ShaderNodeOutputMaterial'); em = nt.nodes.new('ShaderNodeEmission')
        em.inputs['Color'].default_value = (*SC.hex_lin(color), 1)
        tc = nt.nodes.new('ShaderNodeTexCoord'); sep = nt.nodes.new('ShaderNodeSeparateXYZ')
        mr = nt.nodes.new('ShaderNodeMapRange'); mr.clamp = True
        mr.inputs['From Min'].default_value = z_lo; mr.inputs['From Max'].default_value = z_hi
        mr.inputs['To Min'].default_value = s_lo * strength; mr.inputs['To Max'].default_value = s_hi * strength
        nt.links.new(tc.outputs['Object'], sep.inputs[0]); nt.links.new(sep.outputs['Z'], mr.inputs['Value'])
        nt.links.new(mr.outputs['Result'], em.inputs['Strength']); nt.links.new(em.outputs[0], o.inputs['Surface'])
        return m

    def part(folder, name, mat, z0):
        ob = SC.stl(os.path.join(HERE, folder, 'stl', name + '.stl'), mat, name)
        ob.location = (ob.location[0], ob.location[1], ob.location[2] + z0)
        return ob

    an = SC.anodised()
    black_acrylic = SC.principled('black-acrylic', '#0A0A0B', 0.04, coat=0.0)
    steel = SC.principled('steel', '#C9C9C6', 0.25, 1.0, bump=(2500.0, 0.6))
    SC.set_room(tz, wall_y=0.55 if prod == 'core' else 0.75)
    if prod == 'core':
        z0 = tz + 0.0065                                                # the dock's underside on the table
        for nm, m in (('dock', black_acrylic), ('base', black_acrylic), ('ring', an), ('seat', SC.principled('si', '#111111', 0.6)),
                      ('dock-cable', SC.principled('braid', '#121212', 0.75, bump=(1200.0, 0.5))), ('grommet', an)):
            part('out-orb-table', nm, m, z0)
        zc = z0 + 100.45 * MM                                           # the ball's centre (crystal.orb_geometry)
        # round 2: the ball at a third of the chip's dye per mm, as stock 3/8 in sheet is if the maker holds the chart's
        # figure at thickness ("held"; Ice is single-layer stock either way, launch/stock-tints-lamps.md), and the
        # inside a fine glass-bead blast (roughness 0.3) rather than a coarse one, so the far wall reads through it
        # round 4 (the coordinator, 2026-11-03): by night the ball clear inside, as the coordinator reads the design, or
        # ('frost' variant) with the fine bead-blast; by day as passed in round 2
        inner = {'frost': 0.6, 'fine': 0.3}.get(var, 0.0) if night else 0.3   # 'frost': the CAD's coarse bead-blast
        sphere('ball', 80.0, zc, acrylic('ball', 0.0, loading=1 / 3))
        inner_mat = acrylic('ball-in', inner, loading=1 / 3)
        if night and var == 'frost':
            # bead-blasted acrylic diffuses nearly evenly: half of the frosted face a diffuse transmission (round 4;
            # rough glass alone only blurs forward)
            nt = inner_mat.node_tree; outn = next(n for n in nt.nodes if n.type == 'OUTPUT_MATERIAL')
            glass = outn.inputs['Surface'].links[0].from_node
            tl = nt.nodes.new('ShaderNodeBsdfTranslucent'); tl.inputs['Color'].default_value = (0.9, 0.9, 0.9, 1)
            mx = nt.nodes.new('ShaderNodeMixShader'); mx.inputs[0].default_value = 0.3   # round 5: more forward, a gradient
            nt.links.new(glass.outputs[0], mx.inputs[1]); nt.links.new(tl.outputs[0], mx.inputs[2])
            nt.links.new(mx.outputs[0], outn.inputs['Surface'])
        sphere('ball-in', 71.0, zc, inner_mat, inward=True)
        if night:   # round 4: the LED itself under the window (its face 14.8 above the base's foot), about 620 lm
            # at full: a real light, up into the ball; its light reaches the room only through the acrylic
            light('led', 'SPOT', (0, 0, z0 + 0.0148), LED_W, 0.012, spot=160.0)
            led = bpy.data.meshes.new('led-face'); bm = bmesh.new()
            bmesh.ops.create_circle(bm, cap_ends=True, segments=48, radius=0.013); bm.to_mesh(led); bm.free()
            lo = bpy.data.objects.new('led-face', led); bpy.context.scene.collection.objects.link(lo)
            lo.location = (0, 0, z0 + 0.0147)
            em = bpy.data.materials.new('led-em'); em.use_nodes = True
            b = em.node_tree.nodes['Principled BSDF']; b.inputs['Emission Color'].default_value = (*blackbody(cct), 1)
            b.inputs['Emission Strength'].default_value = 40.0
            led.materials.append(em); lo.visible_diffuse = False; lo.visible_shadow = False
        cam = ((0.12, -1.02, tz + 0.235), (0.0, 0.0, tz + 0.098), 85.0)
    else:
        rim = tz + 0.70                                                 # the rim 700 above the table
        H = 48.2                                  # the collar's hole (round 1: the closed tops left a dark seam)
        sphere('tint', 100.0, rim, acrylic('tint', 0.0), cut=0.0, hole=H)
        sphere('tint-in', 97.0, rim, acrylic('tint-in', 0.0), inward=True, cut=0.0, hole=H)
        sphere('clear', 96.0, rim, acrylic('clear', 0.0, 'Clear'), cut=4.0, hole=H)
        sphere('clear-in', 90.0, rim, acrylic('clear-in', 0.0, 'Clear'), inward=True, cut=4.0, hole=H)
        opal = bpy.data.materials.new('opal'); opal.use_nodes = True
        nt = opal.node_tree; nt.nodes.clear()
        o = nt.nodes.new('ShaderNodeOutputMaterial'); tr = nt.nodes.new('ShaderNodeBsdfTranslucent')
        gl = nt.nodes.new('ShaderNodeBsdfGlossy'); gl.inputs['Roughness'].default_value = 0.08
        df = nt.nodes.new('ShaderNodeBsdfDiffuse'); m1 = nt.nodes.new('ShaderNodeMixShader'); m1.inputs[0].default_value = 0.5
        m2 = nt.nodes.new('ShaderNodeMixShader'); m2.inputs[0].default_value = 0.06
        for n_, c in ((tr, (0.93, 0.93, 0.92, 1)), (df, (0.90, 0.90, 0.88, 1))):
            n_.inputs['Color'].default_value = c
        nt.links.new(df.outputs[0], m1.inputs[1]); nt.links.new(tr.outputs[0], m1.inputs[2])
        nt.links.new(m1.outputs[0], m2.inputs[1]); nt.links.new(gl.outputs[0], m2.inputs[2]); nt.links.new(m2.outputs[0], o.inputs['Surface'])
        # round 5 (the gate: an electric-blue line at the mouth, the diffuser's light piping out of the polished cut
        # edge): the proposed fix, modelled at night: the opal ends 4 inside the rim, as the clear shell does, and the
        # rim's exposed edge is satin (bead-blasted), so no lit polished edge faces the room
        oc = 4.0 if night else 0.0
        sphere('opal', 89.0, rim, opal, cut=oc, hole=H)
        sphere('opal-in', 86.0, rim, opal, inward=True, cut=oc, hole=H)
        part('out-dome-pendant', 'rim', acrylic('rim', 0.45 if night else 0.0), rim)
        for nm in ('collar', 'clamp', 'crown', 'gland', 'hub'):
            part('out-dome-pendant', nm, an, rim)
        part('out-dome-pendant', 'reflector', steel, rim)
        part('out-dome-pendant', 'cord', SC.principled('braid', '#121212', 0.75, bump=(1200.0, 0.5)), rim)
        if night:
            # the reflector's spill lights the opal from the crown: brightest at the top, falling to the rim; it may
            # light the wall and the crown, and there is no table or floor in frame
            # round 4: real lights instead. The COB 22 up the bore, about 500 lm out of the fitting, down onto the
            # table (a pendant's job) within the louvre's cut-off; the reflector's spill, about a quarter, lights the
            # opal from the crown, so the dome glows in its tint and lights the wall
            light('cob', 'SPOT', (0, 0, rim + 0.060), COB_W, 0.014, spot=92.0)
            light('spill', 'POINT', (0, 0, rim + 0.050), SPILL_W, 0.03)
            # round 5: the day frame's viewpoint (the pair one scene), a wider lens to keep the table's pool and the
            # whole cable; a stoneware bowl on the table
            cam = ((0.0, -1.22, rim - 0.17), (0.0, 0.0, tz + 0.40), 30.0)
            bowl_m = SC.principled('stoneware', '#C9C2B6', 0.5, bump=(1500.0, 0.25))
            bm = bmesh.new(); bmesh.ops.create_uvsphere(bm, u_segments=96, v_segments=48, radius=0.11)
            bmesh.ops.delete(bm, geom=[v for v in bm.verts if v.co.z > -0.035], context='VERTS')
            bmesh.ops.solidify(bm, geom=bm.faces[:], thickness=0.005)
            for f in bm.faces:
                f.smooth = True
            me = bpy.data.meshes.new('bowl'); bm.to_mesh(me); bm.free()
            bo = bpy.data.objects.new('bowl', me); bpy.context.scene.collection.objects.link(bo)
            bo.location = (0.06, 0.04, tz + 0.11); me.materials.append(bowl_m)
        else:
            cam = ((0.0, -1.22, rim - 0.17), (0.0, 0.0, rim + 0.02), 85.0)   # round 2: a little below, into the mouth
    if night:
        # round 4: a white ceiling at 2.5 m, so the lamp's light that leaves upward comes back into the room, as at home
        SC.plane('ceiling', (4.3, 4.0), (0.85, 0.0, 2.5), (180, 0, 0), SC.principled('ceiling', '#E8E4DC', 0.9))
        SC.world(hdri='kiara_9_dusk', strength=0.02, rotation=200)   # round 3: soft natural reflections, no shapes
        moon = SC.area('moon', (-1.3, -0.4, 1.6), (0, -70, 0), (1.2, 1.6), 2.0, '#9FB2D6')   # round 4: the lamp leads
        moon.visible_glossy = False               # round 1: no daylight-window shapes reflected at night
        if prod == 'core':   # round 5: a crisp, dim window in the outer gloss, so the clear skin reads as its own layer
            win = SC.area('window-glint', (-0.55, -0.95, tz + 0.55), (62, 0, -30), (0.35, 0.55), 1.2, '#B9C7DD')
            win.visible_diffuse = False
        # round 3: a large soft fill far off, for a curved soft reflection on the glass (round 2's small one read as a
        # hard square sticker)
        fill = SC.area('fill', (1.4, -2.2, 1.9), (55, 0, 32), (1.4, 0.9), 2.0, '#8FA0BE')
        fill.visible_glossy = False
        exposure = float(os.environ.get('NIGHT_EV', '1.5'))   # round 4: exposed for the lamp, as a night photograph is
    else:
        SC.world(hdri='kiara_9_dusk', strength=0.35, rotation=200)
        SC.window_gobo(-1.3, -1.3, 0.9, 0.75, 2.4, panes=(2, 2))
        SC.area('window-sky', (-1.25, -0.2, 1.55), (0, -90, 0), (1.5, 2.0), 90.0, '#DCE6F5')
        SC.sun_lamp('sun', (0.86, -0.25, -0.34), strength=10.0, color='#FFE7C8', angle=1.5)
        exposure = 0.0
    SC.render_settings(1800, 1200, samples, scale, exposure=exposure, look='AgX - Medium High Contrast')
    bpy.context.scene.cycles.caustics_refractive = True
    SC.camera(cam[0], cam[1], lens=cam[2], fstop=5.6)
    os.makedirs(OUT, exist_ok=True)
    out = os.environ.get('LAMP_OUT') or os.path.join(OUT, frame + '.png')
    bpy.context.scene.render.filepath = out
    bpy.ops.render.render(write_still=True)


if __name__ == '__main__':
    a = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else sys.argv[1:]
    build(a[0], int(a[a.index('--samples') + 1]) if '--samples' in a else 256,
          float(a[a.index('--scale') + 1]) if '--scale' in a else 1.0)
