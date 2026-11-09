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
# One photometric scale (round 13, 2026-11-03): the COB disc's 3.2 W (env COB_W 2.0 x 1.6, at the cob light below) stands
# for its ~490 lm out of the fitting (Bridgelux Vero SE 10 at 180 mA, ~575 lm at the COB, crystal.py; x 0.85 out), so
# 0.0065 W a lumen; the liner's spill (145 lm) is emitted on that scale. The three globals below are round-4 leftovers,
# no longer read by the night rigs: do not take COB_W 8 as the Hemisphere's output.
LED_W = float(os.environ.get('LED_W', '55.0'))         # (round 4, unused since round 12: Core's light is its emitter)
COB_W = float(os.environ.get('COB_W', '8.0'))         # (round 4, stale: the cob light reads its own default, 2.0 x 1.6 W)
SPILL_W = float(os.environ.get('SPILL_W', '0.08'))    # (round 4, unused since round 13: the spill is the liner's emission)


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
    # Core's drawn LED (out-orb-table bom since 2026-11-01): 200 lm, about 180 out; B's core emits it from both faces of
    # its 0.0408 m2 (14.4 W/m2 a side), A's frost the same power on its 0.0633 m2. Until 2026-11-09 it was 44.6, round
    # 4's 620 lm, three times the part (the coordinator: never brighter than the part)
    CORE_EMIT0 = '14.4'
    prod, tint, mode, *var = frame.split('-')
    var = var[0] if var else ''
    tname = TINT[tint]
    night = mode == 'night'
    cct = CCT
    bpy.ops.wm.read_factory_settings(use_empty=True)
    MM = SC.MM
    tz = 0.62                                                           # the table's top

    def sphere(nm, r, z, mat, inward=False, cut=None, loc=(0, 0), hole=None, hole_below=None):
        bm = bmesh.new()
        bmesh.ops.create_uvsphere(bm, u_segments=256, v_segments=128, radius=r * MM)
        if cut is not None:
            bmesh.ops.delete(bm, geom=[v for v in bm.verts if v.co.z < cut * MM - 1e-9], context='VERTS')
        if hole is not None:                      # the collar's hole at the crown (the CAD's: Ø96.4)
            bmesh.ops.delete(bm, geom=[v for v in bm.verts if math.hypot(v.co.x, v.co.y) < hole * MM and v.co.z > 0],
                             context='VERTS')
        if hole_below is not None:                # an opening at the bottom (Core B's core over the window)
            bmesh.ops.delete(bm, geom=[v for v in bm.verts if math.hypot(v.co.x, v.co.y) < hole_below * MM and v.co.z < 0],
                             context='VERTS')
        if inward:
            bmesh.ops.reverse_faces(bm, faces=bm.faces)
        for f in bm.faces:
            f.smooth = True
        me = bpy.data.meshes.new(nm); bm.to_mesh(me); bm.free()
        ob = bpy.data.objects.new(nm, me); bpy.context.scene.collection.objects.link(ob)
        ob.location = (loc[0], loc[1], z); me.materials.append(mat)
        return ob

    def acrylic(nm, rough, which=None, loading=1.0, scratch=0.25):
        return SC.acrylic_material(nm, [(-1e4, 1e4, which or tname)], rough, 'polished', loading=loading, scratch=scratch,
                                   bond=False)

    def thin_shadow(m, T, T_back=None):
        # round 3 (2026-11-09): T_back, if given, is what a shadow ray meets leaving the shell from inside (Backfacing):
        # Core A's ball passes a studio light's or the sun's light to its frost only through the dye (T9), and the frost
        # face's own light out at 0.96 (its emission already carries T9). At 0.96 both ways, A returned undyed light
        """Round 12: a thin clear shell lets light through to what's behind it; Cycles' shadow rays stop at glass, so a
        lamp shut in a glass ball lit nothing outside (the coordinator's gate, point 7). For shadow rays only, the shell
        passes its own transmission T (per channel); camera and bounce rays still refract. It drops only the shell's
        small refractive offset."""
        nt = m.node_tree; outn = next(n for n in nt.nodes if n.type == 'OUTPUT_MATERIAL')
        prev = outn.inputs['Surface'].links[0].from_node
        lp = nt.nodes.new('ShaderNodeLightPath'); tb = nt.nodes.new('ShaderNodeBsdfTransparent')
        tb.inputs['Color'].default_value = (*T, 1); mx = nt.nodes.new('ShaderNodeMixShader')
        if T_back is not None:
            gm = nt.nodes.new('ShaderNodeNewGeometry'); cm = nt.nodes.new('ShaderNodeMix'); cm.data_type = 'RGBA'
            cm.inputs['A'].default_value = (*T, 1); cm.inputs['B'].default_value = (*T_back, 1)
            nt.links.new(gm.outputs['Backfacing'], cm.inputs['Factor']); nt.links.new(cm.outputs['Result'], tb.inputs['Color'])
        nt.links.new(lp.outputs['Is Shadow Ray'], mx.inputs[0]); nt.links.new(prev.outputs[0], mx.inputs[1])
        nt.links.new(tb.outputs[0], mx.inputs[2]); nt.links.new(mx.outputs[0], outn.inputs['Surface'])
        return m

    def shell_T(tint, loading, mm):
        return tuple(math.exp(-a * mm / 1000.0) * 0.96 for a in SC.absorption(tint, loading))   # 4 % lost at each face

    def gobo(*a, **k):
        # round 14 (the card audit): the window wall is a real wall, seen by the camera too, not a reflect-only card
        obs = SC.window_gobo(*a, **k)
        for o_ in obs:
            o_.visible_camera = True
        return obs

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
        inner = 0.6   # round 6: the CAD's coarse bead-blast, by day and by night (the pair one object)

        def frosted(m):
            # bead-blasted acrylic diffuses nearly evenly: half of the frosted face a diffuse transmission (round 4;
            # rough glass alone only blurs forward)
            # 2026-11-09 (round 3, the Core A/B critics): the diffuse lobe takes the wall's tint (SC.frosted); at a flat
            # grey it returned light that never crossed the dye
            return SC.frosted(m, float(os.environ.get('FROST_MIX', '0.5')))   # round 6: more forward, a gradient
        if var == 'nested':
            # round 8 PROPOSAL (the coordinator, 2026-11-03: the frosted-inside ball reads as milk glass by day and a
            # flat disc lit; launch/core-frost-options.md): a ball in a ball. The outer ball 6 mm tinted cast, polished
            # both faces (the existing mould); inside it, with a clear air gap, a 3 mm clear diffuser ball R 45 frosted
            # inside, seated on the grommet's ring (its centre 27.8 below the outer's) and captive once the outer
            # halves are joined round it
            # (round 9: no hairline wear here; at 1024 samples the light bouncing between the two balls drew it as a
            # crumpled caustic net over the core)
            # (2026-11-09, the gate: B put out 1.36x A's light, its 6 mm outer carrying less dye than A's 9 mm wall: the
            # same dye path as A, 0.5 of the chip a mm over 6 mm)
            bl = float(os.environ.get('B_LOAD', '0.5'))
            Tb = shell_T(tname, bl, 3.0)        # each face carries half the 6 mm wall's absorption
            # 2026-11-09 (the Core A/B tally, point 7: how B's core is held): the outer keeps A's Ø40 port at its foot,
            # as core-frost-options.md draws it; the core's own Ø40 opening seats on the grommet's upper ring through it
            sphere('ball', 80.0, zc, thin_shadow(acrylic('ball', 0.0, loading=bl, scratch=0.0), Tb), hole_below=20.0)
            sphere('ball-in', 74.0, zc, thin_shadow(acrylic('ball-in', 0.0, loading=bl, scratch=0.0), Tb), inward=True, hole_below=20.0)
            # round 9 (the gate: the Ø90 core too small, "an LED orb in a black bubble"): Ø120, its center 12 below the
            # outer's, on a short spacer ring on the grommet; a 13 gap at its equator
            ri = float(os.environ.get('CORE_IN_R', '60.0')); zi = zc - float(os.environ.get('CORE_IN_DZ', '12.0')) * MM   # as drawn (12): its Ø40 opening on the grommet's top (2026-11-09; at 10 it floated 1.6 above)
            # round 9: the core open at its base, Ø40 over the window, seated on the grommet's ring: the LED lights the
            # frost directly (closed, all its light reached the frost through the polished shell, a caustic: noise)
            sphere('core', ri, zi, thin_shadow(acrylic('core', 0.0, 'Clear', scratch=0.0), shell_T('Clear', 1.0, 3.0)), hole_below=20.0)
            if os.environ.get('CORE_OPAL', '1') == '1':
                # round 11 PROPOSAL (the gate on B's day: the core lost, within 10 % of its surround): the core in 3 mm
                # opal (white, volume-diffusing) cast acrylic, as Hemisphere's liner, rather than bead-blasted clear: it
                # scatters daylight back and reads as a pale core inside the tinted glass, and glows evenly at night
                cm = bpy.data.materials.new('core-opal'); cm.use_nodes = True; nt = cm.node_tree; nt.nodes.clear()
                o_ = nt.nodes.new('ShaderNodeOutputMaterial'); tr_ = nt.nodes.new('ShaderNodeBsdfTranslucent')
                df_ = nt.nodes.new('ShaderNodeBsdfDiffuse'); m1_ = nt.nodes.new('ShaderNodeMixShader')
                m1_.inputs[0].default_value = float(os.environ.get('CORE_OPAL_T', '0.5'))
                tr_.inputs['Color'].default_value = (0.93, 0.93, 0.92, 1); df_.inputs['Color'].default_value = (0.90, 0.90, 0.88, 1)
                nt.links.new(df_.outputs[0], m1_.inputs[1]); nt.links.new(tr_.outputs[0], m1_.inputs[2])
                nt.links.new(m1_.outputs[0], o_.inputs['Surface'])
            else:
                cm = frosted(acrylic('core-in', inner, 'Clear', scratch=0.0))
            # round 9: the printed dot over the LED, modelled in the frost itself (a separate surface beside the frost
            # made hard paths that the denoiser blotched): within 25 of the axis at the bottom the frost passes about
            # 40 %, the rest going back into the core (here: absorbed, a conservative stand-in)
            nt = cm.node_tree; outn = next(n for n in nt.nodes if n.type == 'OUTPUT_MATERIAL')
            prev = outn.inputs['Surface'].links[0].from_node
            tc_ = nt.nodes.new('ShaderNodeTexCoord'); sx = nt.nodes.new('ShaderNodeSeparateXYZ')
            nt.links.new(tc_.outputs['Object'], sx.inputs[0])
            mr_ = nt.nodes.new('ShaderNodeMapRange'); mr_.clamp = True
            zd = -math.sqrt((ri - 3.0) ** 2 - 32.0 ** 2) * MM   # the dot Ø64 round the opening
            mr_.inputs['From Min'].default_value = zd - 0.001; mr_.inputs['From Max'].default_value = zd + 0.006
            mr_.inputs['To Min'].default_value = 0.6; mr_.inputs['To Max'].default_value = 0.0
            nt.links.new(sx.outputs['Z'], mr_.inputs['Value'])
            # round 11 (the gate: a navy petal at the seat by day): the dot is white, so a white diffuse face, which by
            # night sends the LED's light back up into the core rather than through
            dk = nt.nodes.new('ShaderNodeBsdfDiffuse'); dk.inputs['Color'].default_value = (0.88, 0.88, 0.86, 1)
            mx2 = nt.nodes.new('ShaderNodeMixShader')
            nt.links.new(mr_.outputs['Result'], mx2.inputs[0]); nt.links.new(prev.outputs[0], mx2.inputs[1])
            nt.links.new(dk.outputs[0], mx2.inputs[2]); nt.links.new(mx2.outputs[0], outn.inputs['Surface'])
            if night:
                # round 12 (the gate, point 7: the lamp's light landed nowhere): the core's lit opal face is the light,
                # as the coordinator's ruling 3 allows for a bulb inside its own opal fitting (the LED below stays as its
                # visible face only). Brightest at the crown, as the LED aims up (point 10); the dot's ring dimmer
                outn = next(n for n in nt.nodes if n.type == 'OUTPUT_MATERIAL'); prev = outn.inputs['Surface'].links[0].from_node
                emn = nt.nodes.new('ShaderNodeEmission'); emn.inputs['Color'].default_value = (*blackbody(cct), 1)
                gz = nt.nodes.new('ShaderNodeMapRange'); gz.clamp = True
                gz.inputs['From Min'].default_value = -(ri - 3.0) * MM; gz.inputs['From Max'].default_value = (ri - 3.0) * MM
                E = float(os.environ.get('CORE_EMIT', CORE_EMIT0))
                gz.inputs['To Min'].default_value = 0.75 * E; gz.inputs['To Max'].default_value = 1.15 * E
                nt.links.new(sx.outputs['Z'], gz.inputs['Value'])
                dim = nt.nodes.new('ShaderNodeMath'); dim.operation = 'MULTIPLY'
                inv = nt.nodes.new('ShaderNodeMath'); inv.operation = 'SUBTRACT'; inv.inputs[0].default_value = 1.0
                nt.links.new(mr_.outputs['Result'], inv.inputs[1])
                nt.links.new(gz.outputs['Result'], dim.inputs[0]); nt.links.new(inv.outputs[0], dim.inputs[1])
                nt.links.new(dim.outputs[0], emn.inputs['Strength'])
                ad = nt.nodes.new('ShaderNodeAddShader')
                nt.links.new(prev.outputs[0], ad.inputs[0]); nt.links.new(emn.outputs[0], ad.inputs[1])
                nt.links.new(ad.outputs[0], outn.inputs['Surface'])
                cm.cycles.emission_sampling = os.environ.get('EMIS_SAMP', 'FRONT_BACK')   # round 14: it faces in; the room sees its back
            sphere('core-in', ri - 3.0, zi, cm, inward=True, hole_below=20.0)
            # round 9 PROPOSAL (the gate: the LED hotspot): a white dot printed inside the core over the LED, Ø50, that
            # sends about half the near light back up into the core, as LED globes do
            if os.environ.get('CORE_DOT', '0') == '1':   # round 9: as a surface it blotched (see below)
                bm = bmesh.new(); bmesh.ops.create_uvsphere(bm, u_segments=128, v_segments=64, radius=(ri - 3.5) * MM)
                zcut = -math.sqrt((ri - 3.5) ** 2 - 25.0 ** 2) * MM
                bmesh.ops.delete(bm, geom=[v for v in bm.verts if v.co.z > zcut], context='VERTS')
                for f_ in bm.faces:
                    f_.smooth = True
                me = bpy.data.meshes.new('dot'); bm.to_mesh(me); bm.free()
                do = bpy.data.objects.new('dot', me); bpy.context.scene.collection.objects.link(do); do.location = (0, 0, zi)
                dm = bpy.data.materials.new('dot'); dm.use_nodes = True; nt = dm.node_tree; nt.nodes.clear()
                o_ = nt.nodes.new('ShaderNodeOutputMaterial'); t_ = nt.nodes.new('ShaderNodeBsdfTranslucent')
                d_ = nt.nodes.new('ShaderNodeBsdfDiffuse'); m_ = nt.nodes.new('ShaderNodeMixShader'); m_.inputs[0].default_value = 0.45
                t_.inputs['Color'].default_value = (0.95, 0.95, 0.95, 1); d_.inputs['Color'].default_value = (0.92, 0.92, 0.92, 1)
                nt.links.new(d_.outputs[0], m_.inputs[1]); nt.links.new(t_.outputs[0], m_.inputs[2]); nt.links.new(m_.outputs[0], o_.inputs['Surface'])
                me.materials.append(dm)
        else:
            # round 15 (the coordinator: Core A "as drawn", fairly against B): the ball has its 40 port over the window,
            # as in the CAD, and at night the same honest rig as B: the frosted face is the light (ruling 3's exception,
            # the LED inside its own frosted fitting), at the same total power as B's core, near even (a Lambertian LED
            # at the sphere's foot lights its inside about evenly); the outer wall passes shadow rays at its transmission
            # the frost face emits on the wall's inner face, where the wall's absorption is not applied to it: so its
            # colour carries the whole 9 mm wall's transmission, and the outer face passes shadow rays at its surface loss
            T9 = shell_T(tname, 1 / 3, 9.0)
            sphere('ball', 80.0, zc, thin_shadow(acrylic('ball', 0.0, loading=1 / 3), (0.96, 0.96, 0.96), shell_T(tname, 1 / 3, 9.0)), hole_below=20.0)
            fm = frosted(acrylic('ball-in', inner, loading=1 / 3))
            if night:
                ntf = fm.node_tree; outf = next(n for n in ntf.nodes if n.type == 'OUTPUT_MATERIAL')
                pf = outf.inputs['Surface'].links[0].from_node
                ef = ntf.nodes.new('ShaderNodeEmission'); bbf = blackbody(cct)
                ef.inputs['Color'].default_value = (*(bbf[i] * T9[i] / 0.96 for i in range(3)), 1)
                # B's core: 0.05 W/m2 a side on 0.0408 m2; the same power on A's 0.0633 m2 frost
                ef.inputs['Strength'].default_value = float(os.environ.get('CORE_EMIT', CORE_EMIT0)) * 0.0408 / 0.0633
                af = ntf.nodes.new('ShaderNodeAddShader')
                ntf.links.new(pf.outputs[0], af.inputs[0]); ntf.links.new(ef.outputs[0], af.inputs[1])
                ntf.links.new(af.outputs[0], outf.inputs['Surface'])
                fm.cycles.emission_sampling = 'FRONT_BACK'
            sphere('ball-in', 71.0, zc, fm, inward=True, hole_below=20.0)
        if night:   # round 4: the LED itself under the window (its face 14.8 above the base's foot), about 620 lm
            # at full: a real light, up into the ball; its light reaches the room only through the acrylic
            # round 8 (the gate: a hotspot cone at the base): the LED behind the window as a Lambertian disc the
            # window's size, not a 160 deg spot
            # (the disc speckled at full samples: back to a point source, a full hemisphere with a soft edge)
            if False:   # round 12: in B the core's opal face is the light; round 15: in A the frost's (above)
                # (round 14, the Mantle lane's flag: a Blender spot points down, -Z; this one had no rotation, so in A it
                # shone into the base, not the ball. Aimed up now. Core A's frames of rounds 4 to 8 carry that error)
                light('led', 'SPOT', (0, 0, z0 + 0.0148), LED_W, 0.012, rot=(180, 0, 0), spot=160.0)
            led = bpy.data.meshes.new('led-face'); bm = bmesh.new()
            bmesh.ops.create_circle(bm, cap_ends=True, segments=48, radius=0.013); bm.to_mesh(led); bm.free()
            lo = bpy.data.objects.new('led-face', led); bpy.context.scene.collection.objects.link(lo)
            lo.location = (0, 0, z0 + 0.0147)
            em = bpy.data.materials.new('led-em'); em.use_nodes = True
            b = em.node_tree.nodes['Principled BSDF']; b.inputs['Emission Color'].default_value = (*blackbody(cct), 1)
            # (on the one scale the night exposure fell 9.8 EV; the LED's visible face keeps its look with it)
            b.inputs['Emission Strength'].default_value = 8.0 * 2.0 ** (1.8 - float(os.environ.get('NIGHT_EV', '-8.0')))
            led.materials.append(em); lo.visible_diffuse = False   # round 14 (ruling 4): it casts shadows
        cam = ((0.12, -1.02, tz + float(os.environ.get('CORE_CAM_Z', '0.36'))), (0.0, 0.0, tz + 0.098), 85.0)
    else:
        rim = tz + 0.70                                                 # the rim 700 above the table
        H = 48.2                                  # the collar's hole (round 1: the closed tops left a dark seam)
        # round 13 (the coordinator: the dome lit nothing, Core's renderer gap): at night the thin shells pass shadow
        # rays at their own transmission (the tint 3 mm at full dye, the clear 6 mm; half each face)
        tsh = thin_shadow   # round 14 (the coordinator): by day too, so the dome's wall shadow is tinted
        Tt, Tc = shell_T(tname, 1.0, 1.5), shell_T('Clear', 1.0, 3.0)
        sphere('tint', 100.0, rim, tsh(acrylic('tint', 0.0), Tt), cut=0.0, hole=H)
        sphere('tint-in', 97.0, rim, tsh(acrylic('tint-in', 0.0), Tt), inward=True, cut=0.0, hole=H)
        sphere('clear', 96.0, rim, tsh(acrylic('clear', 0.0, 'Clear'), Tc), cut=4.0, hole=H)
        sphere('clear-in', 90.0, rim, tsh(acrylic('clear-in', 0.0, 'Clear'), Tc), inward=True, cut=4.0, hole=H)
        opal = bpy.data.materials.new('opal'); opal.use_nodes = True
        nt = opal.node_tree; nt.nodes.clear()
        o = nt.nodes.new('ShaderNodeOutputMaterial'); tr = nt.nodes.new('ShaderNodeBsdfTranslucent')
        gl = nt.nodes.new('ShaderNodeBsdfGlossy'); gl.inputs['Roughness'].default_value = 0.08
        df = nt.nodes.new('ShaderNodeBsdfDiffuse'); m1 = nt.nodes.new('ShaderNodeMixShader'); m1.inputs[0].default_value = 0.5
        m2 = nt.nodes.new('ShaderNodeMixShader'); m2.inputs[0].default_value = 0.06
        oc_ = tuple(float(x) for x in os.environ.get('OPAL', '0.80,0.89,0.98').split(','))   # round 9: a cool-white opal grade (PROPOSAL)
        for n_, c in ((tr, (*oc_, 1)), (df, (*(v * 0.97 for v in oc_), 1))):
            n_.inputs['Color'].default_value = c
        nt.links.new(df.outputs[0], m1.inputs[1]); nt.links.new(tr.outputs[0], m1.inputs[2])
        nt.links.new(m1.outputs[0], m2.inputs[1]); nt.links.new(gl.outputs[0], m2.inputs[2]); nt.links.new(m2.outputs[0], o.inputs['Surface'])
        # round 5 (the gate: an electric-blue line at the mouth, the diffuser's light piping out of the polished cut
        # edge): the proposed fix, modelled at night: the opal ends 4 inside the rim, as the clear shell does, and the
        # rim's exposed edge is satin (bead-blasted), so no lit polished edge faces the room
        oc = float(os.environ.get('OPAL_CUT', '1.5'))   # round 6: 4 (the proposed rim); round 10 (the gate: close the dark seam at the lip): 1.5
        opal_out = opal
        if night:
            # round 13 (ruling 3's exception: the bulb inside its own opal fitting): the liner's lit face is the
            # reflector's spill, about a quarter of the COB's 575 lm (145 lm), on one photometric scale with the COB
            # (3.2 W for its 490 lm out of the fitting: 0.0065 W a lumen). The liner's outer face, 0.041 m2, emits both
            # ways: 145 lm x 0.0065 / (2 x 0.041) = 11.5 W/m2 on average, brighter at the crown, where the reflector
            # throws it, than at the rim; in the liner's own colour (its transmittance)
            lm = float(os.environ.get('SPILL_LM', '145')); Wlm = 3.2 / 490.0
            S0 = lm * Wlm / (2 * 0.041)
            opal_out = opal.copy(); opal_out.name = 'opal-lit'; nt2 = opal_out.node_tree
            outn = next(n for n in nt2.nodes if n.type == 'OUTPUT_MATERIAL'); prev = outn.inputs['Surface'].links[0].from_node
            emn = nt2.nodes.new('ShaderNodeEmission')
            bb = blackbody(cct); emn.inputs['Color'].default_value = (*(bb[i] * oc_[i] for i in range(3)), 1)
            tc2 = nt2.nodes.new('ShaderNodeTexCoord'); sx2 = nt2.nodes.new('ShaderNodeSeparateXYZ')
            nt2.links.new(tc2.outputs['Object'], sx2.inputs[0])
            gz2 = nt2.nodes.new('ShaderNodeMapRange'); gz2.clamp = True
            gz2.inputs['From Min'].default_value = oc * MM; gz2.inputs['From Max'].default_value = 0.075
            gz2.inputs['To Min'].default_value = 0.6 * S0; gz2.inputs['To Max'].default_value = 1.4 * S0
            nt2.links.new(sx2.outputs['Z'], gz2.inputs['Value']); nt2.links.new(gz2.outputs['Result'], emn.inputs['Strength'])
            ad2 = nt2.nodes.new('ShaderNodeAddShader')
            nt2.links.new(prev.outputs[0], ad2.inputs[0]); nt2.links.new(emn.outputs[0], ad2.inputs[1])
            nt2.links.new(ad2.outputs[0], outn.inputs['Surface'])
            opal_out.cycles.emission_sampling = 'FRONT_BACK'
        sphere('opal', 89.0, rim, opal_out, cut=oc, hole=H)
        sphere('opal-in', 86.0, rim, opal, inward=True, cut=oc, hole=H)
        part('out-dome-pendant', 'rim', acrylic('rim', 0.6, loading=float(os.environ.get('RIM_LOAD', '0.5'))), rim)   # round 9: backed off (the gate: a royal-blue outline)   # round 6: satin, a deeper shade, never bright
        capobs = []
        cap = SC.principled('cap-matte', os.environ.get('CAP', '#4A4A50'), 0.5, metallic=0.2, bump=(4000.0, 0.15))   # round 11: a satin dark grey (no kicker)   # round 8: no glints; round 9: lifted off black
        for nm in ('collar', 'clamp', 'crown', 'gland', 'hub'):
            capobs.append(part('out-dome-pendant', nm, cap, rim))
        # round 8 (the gate: two "LED eyes" on the cap): the PEEK pin carrier, its pins and the silicone gaskets were
        # missing, so the lit bore showed through the collar's slots
        part('out-dome-pendant', 'ring', SC.principled('peek', '#151515', 0.6), rim)
        part('out-dome-pendant', 'pins', steel, rim)
        part('out-dome-pendant', 'gaskets', SC.principled('silicone', '#111111', 0.7), rim)
        # (2026-11-09: the bore's reflector in the CAD's high-reflectance aluminium; its light reaches the table only as a
        # reflective caustic, so those are on and unclamped for Hemisphere, below)
        part('out-dome-pendant', 'reflector', SC.principled('reflector', '#F2F2F0', 0.12, 1.0), rim)
        part('out-dome-pendant', 'cord', SC.principled('braid', '#121212', 0.75, bump=(1200.0, 0.5)), rim)
        if night:
            # the reflector's spill lights the opal from the crown: brightest at the top, falling to the rim; it may
            # light the wall and the crown, and there is no table or floor in frame
            # round 4: real lights instead. The COB 22 up the bore, about 500 lm out of the fitting, down onto the
            # table (a pendant's job) within the louvre's cut-off; the reflector's spill, about a quarter, lights the
            # opal from the crown, so the dome glows in its tint and lights the wall
            # round 6: the table lit from a disc the size of the opal's mouth (a broad source: a soft bowl shadow), within
            # the louvre's cut-off
            # (2026-11-09, the Mantle lane's flag: the COB as the CAD builds it, not a 170 mm disc at the mouth: a Vero
            # SE 10's ~11 mm face at the top of the 46 bore, 82 above the rim, the reflector round it giving the
            # cut-off. Of ~575 lm, the liner's 145 is its emission; ~430 lm leave the COB here, 0.0065 W a lumen)
            part('out-dome-pendant', 'cob', SC.principled('cob-body', '#2A2A2A', 0.5), rim)
            ld = bpy.data.lights.new('cob', 'AREA'); ld.shape = 'DISK'; ld.size = 0.011; ld.energy = 430.0 * 3.2 / 490.0
            ld.color = blackbody(cct)
            ob = bpy.data.objects.new('cob', ld); bpy.context.scene.collection.objects.link(ob)
            ob.location = (0, 0, rim + 0.0815)
            # (round 13: the spill is now the liner's own emission, above)
            pass
        # round 6 (the coordinator, 2026-11-03: the pendant too small): one shared camera for the day and the night,
        # steeper and closer: about 45 deg down from 0.95 m out and 0.93 m above the rim, a 54 mm lens, so the
        # pendant is about a quarter of the width, the crown clear of the top with the cable running out of it, and
        # the table's pool and a stoneware bowl below
        # round 14 (the coordinator): one shared camera, low, just under the rim, so the dome and a glimpse of the
        # white liner at the mouth lead; the table is below the frame
        cam = (tuple(float(v) for v in os.environ.get('HCAM', '0.12,-1.0,0.62').split(',')),
               tuple(float(v) for v in os.environ.get('HTGT', '0.0,0.0,0.69').split(',')), float(os.environ.get('HLENS', '60')))
        cam = ((cam[0][0], cam[0][1], tz + cam[0][2]), (cam[1][0], cam[1][1], tz + cam[1][2]), cam[2])
        bowl_m = SC.principled('stoneware', '#A8A196', 0.28, bump=(1500.0, 0.25))   # round 10: a glaze, so its inside shades   # round 9: under the lamp
        bm = bmesh.new(); bmesh.ops.create_uvsphere(bm, u_segments=96, v_segments=48, radius=0.11)
        bmesh.ops.delete(bm, geom=[v for v in bm.verts if v.co.z > -0.035], context='VERTS')
        bmesh.ops.solidify(bm, geom=bm.faces[:], thickness=0.005)
        for f in bm.faces:
            f.smooth = True
        me = bpy.data.meshes.new('bowl'); bm.to_mesh(me); bm.free()
        bo = bpy.data.objects.new('bowl', me); bpy.context.scene.collection.objects.link(bo)
        bo.location = tuple(float(v) for v in os.environ.get('BOWL_XY', '0.05,0.13').split(',')) + (tz + 0.11,); me.materials.append(bowl_m)   # round 6: in frame
    if night:
        # round 4: a white ceiling at 2.5 m, so the lamp's light that leaves upward comes back into the room, as at home
        # (2026-11-09, item 107 pending: every picture inside the 600 mm drawn drop; with the cap's 126 and the canopy's
        # 50 the rim hangs 776 below the ceiling, so Hemisphere's ceiling is at rim + 0.776; Core's room keeps 2.5 m)
        ceil_z = (tz + 0.70 + 0.776) if prod == 'hemi' else 2.5
        SC.plane('ceiling', (4.3, 4.0), (0.85, 0.0, ceil_z), (180, 0, 0), SC.principled('ceiling', '#E8E4DC', 0.9))
        # 2026-11-09 (the Core A/B tally: finals at about 30 % room and +1 EV; Core at its drawn 200 lm, 1.6 EV under
        # round 4's 620): -8 + 1 + 1.6 = -5.4
        ev = float(os.environ.get('NIGHT_EV', '-5.4' if prod == 'core' else '-3.0'))
        k = 2.0 ** (0.6 - ev)                     # round 9: one evening room for the family, the same fill at each exposure
        # round 14 (the coordinator: the dome must plainly be the room's main light): the room's fill scaled down until the
        # lamp gives most of the light on the wall near it (measured: lamp only against all lights)
        # (2026-11-09, the gate: Core's room from 5 % to 15-20 %, so the dock and table read; Hemisphere's as gated)
        rk = float(os.environ.get('ROOM_K', '0.30' if prod == 'core' else '0.05'))   # 2026-11-09: 30 % (the A/B tally)
        k *= rk
        # round 11 (the coordinator's rulings 1 to 3, 2026-11-03: nothing in the room hidden from the glass's
        # reflections or from view through it; no light linking): the night room is a flat, dim evening ambient (no
        # dusk HDRI, so no daylight windows to mirror), one large soft fill that the glass mirrors as it is, and no
        # moon (its 1.2 x 1.6 panel would mirror as a window)
        SC.world(color=os.environ.get('NIGHT_SKY', '#8A96B0'), strength=float(os.environ.get('NIGHT_AMB', '0.15')) * k)
        fill = SC.area('fill', (1.4, -2.2, 1.9), (55, 0, 32), tuple(float(v) for v in os.environ.get('FILL_SIZE', '5.0,3.4').split(',')), float(os.environ.get('NIGHT_FILL', '3.5')) * k, '#8FA0BE')
        fill.data.shape = 'ELLIPSE'               # a soft round room highlight in the glass
        # (2026-11-09, the gate: one real source reflected in Core's glossy outer ball: the dusk window too)
        # round 12 (the gate: round 10's strip read as a hard white bar, a lit tube, in a dark room): instead a dim
        # dusk window far off to the left, broad and tall, a real light, so the dome shows one long soft reflection
        from mathutils import Vector
        # (round 12: an area light's edge is hard in the glass; so a sheer curtain lit by the dusk outside, an emitting
        # surface brightest at its middle and fading to its edges, out of frame to the left)
        # round 14 (ruling 4: light reaches the subject only through a real opening): the dusk comes in through two
        # real openings, each with a sheer curtain in it, lit by a dim dusk sky outside: the front part of the left
        # wall (the day's window), and a narrow one in the back wall whose curtain shows at the frame's left
        sheer = bpy.data.materials.new('sheer'); sheer.use_nodes = True; nts = sheer.node_tree; nts.nodes.clear()
        os_ = nts.nodes.new('ShaderNodeOutputMaterial'); tl_ = nts.nodes.new('ShaderNodeBsdfTranslucent')
        tp_ = nts.nodes.new('ShaderNodeBsdfTransparent'); mx_ = nts.nodes.new('ShaderNodeMixShader')
        tl_.inputs['Color'].default_value = (0.86, 0.87, 0.88, 1); tp_.inputs['Color'].default_value = (0.55, 0.55, 0.55, 1)
        mx_.inputs[0].default_value = 0.35
        nts.links.new(tl_.outputs[0], mx_.inputs[1]); nts.links.new(tp_.outputs[0], mx_.inputs[2])
        nts.links.new(mx_.outputs[0], os_.inputs['Surface'])
        # the dusk outside follows the exposure as the fill does (k), so the room reads the same at any exposure
        dW = float(os.environ.get('DUSK_W', '20')) * rk * 2.0 ** ({'core': 1.8, 'hemi': -3.0}[prod] - ev)   # tuned at those exposures
        # 2026-11-09 (the Core A/B tally, point 5: give B's shell something real to read against): WIN_DY slides the
        # night window's opening back along the left wall, so its reflection moves out toward the ball's silhouette
        wd = float(os.environ.get('WIN_DY', '0.9' if prod == 'core' else '0'))   # Core: its reflection on B's outer ring
        gobo(-1.3, -1.3 + wd, -0.35 + wd, 0.75, 2.4, panes=(1, 2))
        SC.plane('sheer-left', (0.95, 1.65), (-1.27, -0.825 + wd, 1.575), (90, 0, 90), sheer)
        dl = SC.area('dusk-left', (-1.75, -0.825 + wd, 1.575), (0, 0, 0), (1.0, 1.7), dW, '#9FB2D6')
        dl.rotation_euler = (Vector((0.0, -0.825 + wd, 1.575)) - dl.location).to_track_quat('-Z', 'Y').to_euler()
        if prod != 'core':
            wall = bpy.data.objects['wall']; wm = wall.active_material; wy = wall.location[1]
            bpy.data.objects.remove(wall, do_unlink=True)
            x0, x1, z0w, z1w = -1.05, -0.58, tz + 0.15, tz + 1.55
            for nm_, xa, xb, za, zb in (('wall-a', -1.3, x0, -0.5, 3.5), ('wall-b', x1, 3.0, -0.5, 3.5),
                                        ('wall-c', x0, x1, -0.5, z0w), ('wall-d', x0, x1, z1w, 3.5)):
                SC.plane(nm_, (xb - xa, zb - za), ((xa + xb) / 2, wy, (za + zb) / 2), (90, 0, 0), wm)
            SC.plane('sheer-back', (x1 - x0, z1w - z0w), ((x0 + x1) / 2, wy - 0.005, (z0w + z1w) / 2), (90, 0, 0), sheer)
            db = SC.area('dusk-back', ((x0 + x1) / 2, wy + 0.35, (z0w + z1w) / 2), (0, 0, 0), (0.6, 1.5), dW * 0.25, '#9FB2D6')
            db.rotation_euler = (Vector(((x0 + x1) / 2, 0.0, (z0w + z1w) / 2)) - db.location).to_track_quat('-Z', 'Y').to_euler()
            # 2026-11-09 19:13 (the coordinator: no light in frame hidden from the camera): the dusk sky behind the back
            # wall's opening stands in frame through it (22 % of the frame), so it is real: seen, as a sky through a sheer
            db.visible_camera = True
            # round 11: a small, dim real light behind and above the pendant, between it and the wall, facing the camera
            # side (no light linking): it catches the cap's tiers and is seen in the gloss for what it is
            kk = SC.area('kicker', (0.25, 0.45, tz + 1.05), (0, 0, 0), (0.25, 0.25), float(os.environ.get('KICK_W', '1.5')) * rk, '#D8DCE4')
            kk.rotation_euler = (Vector((0.0, 0.0, tz + 0.80)) - kk.location).to_track_quat('-Z', 'Y').to_euler()
        exposure = ev   # round 4: exposed for the lamp, as a night photograph is
    else:
        SC.world(hdri='kiara_9_dusk', strength=0.35, rotation=200)
        if prod == 'core':
            # 2026-11-09 (the Core A/B tally: A's shadow fell right-front, B's right-back, B's wall a stop darker): ONE
            # day room for A and B, B's: one sun, one sky, one window
            # round 11 (the coordinator: the core lit, the wall behind it in shade): the same window, its opening the
            # front part of the left wall, and the sun in through it from the front left, onto the ball's face; the
            # wall behind the ball takes no sun (the window wall shades it), as a room by a window does
            gobo(-1.3, -1.3, -0.35, 0.75, 2.4, panes=(1, 2))
            # round 12 (the gate: the window a flat grey card in the glass): the sky behind the frame, so its bars show
            SC.area('window-sky', (-1.45, -0.82, 1.55), (0, -90, 0), (0.9, 1.6), float(os.environ.get('CSKY', '60')), '#DCE6F5')
            SC.sun_lamp('sun', (0.75, 0.45, -0.45), strength=float(os.environ.get('CSUN', '10')), color='#FFE7C8', angle=3.0)
        else:
            gobo(-1.3, -1.3, 0.9, 0.75, 2.4, panes=(2, 2))
            SC.area('window-sky', (-1.45, -0.2, 1.55), (0, -90, 0), (1.5, 2.0), 90.0, '#DCE6F5')   # round 14 (ruling 4): outside, through the opening
            SC.sun_lamp('sun', (0.86, -0.25, -0.34), strength=10.0, color='#FFE7C8', angle=1.5)
        if prod == 'core' and var == 'nested' and float(os.environ.get('SIDEBACK_W', '0')) > 0:
            # round 11 (the gate's lever: glass is shot with a side-back light): a tall soft strip behind and to the left,
            # a real light seen in the glass for what it is, so the edges and the gap read
            from mathutils import Vector
            sb = SC.area('side-back', (-0.45, 0.40, tz + 0.30), (0, 0, 0), (0.18, 0.7), float(os.environ.get('SIDEBACK_W', '0')), '#F2EEE6')
            sb.rotation_euler = (Vector((0.0, 0.0, tz + 0.10)) - sb.location).to_track_quat('-Z', 'Y').to_euler()
        exposure = 0.0
    if os.environ.get('GLOSSY_HIDE_WINDOW'):
        # DIAGNOSTIC ONLY, never a final (the Core A/B tally, point 2: is A's crescent the window's reflection?): the
        # window's opening, its sheer and its light hidden from glossy rays
        for o_ in bpy.data.objects:
            if o_.name.startswith(('sheer', 'dusk', 'window', 'mullion', 'transom')):
                o_.visible_glossy = False
                print('GLOSSY-HIDDEN', o_.name)
    SC.render_settings(1800, 1200, samples, scale, exposure=exposure,
                       look=os.environ.get('LOOK', 'AgX - Punchy' if prod == 'core' else 'AgX - Medium High Contrast'))   # 2026-11-09: Punchy for Core (the gate)
    bpy.context.scene.cycles.caustics_refractive = True
    if prod == 'hemi':
        bpy.context.scene.cycles.caustics_reflective = True; bpy.context.scene.cycles.sample_clamp_indirect = 0.0
    if night and prod == 'core':   # round 8: rare bright caustic paths speckled the frost (the denoiser blotched them)
        bpy.context.scene.cycles.sample_clamp_indirect = float(os.environ.get('CLAMP', '20')) * 2.0 ** (1.8 - exposure)   # a radiance: it follows the one scale; bpy.context.scene.cycles.blur_glossy = 1.0
        # (round 9: the crumpled net was caustic noise, the core lit through its own shell; with the core open at its
        # base the default guides are clean again)
    SC.camera(cam[0], cam[1], lens=cam[2], fstop=5.6)
    if night and prod == 'hemi' and 'kicker' in bpy.data.objects:
        # 2026-11-09 19:13 (no light in frame hidden from the camera): the kicker stood in frame (4 %); it slides away
        # from the cap along the line through it, grown to hold its angle there, and stays under the ceiling and in front
        # of the back wall (hiddencast_bpy.slide_out)
        sys.path.insert(0, os.path.join(HERE, 'launch'))
        from hiddencast_bpy import slide_out
        kk_ = bpy.data.objects['kicker']
        kf = slide_out(bpy.context.scene, kk_, (0.0, 0.0, tz + 0.80),
                       ok=lambda p: p.z + kk_.data.size_y / 2 < ceil_z - 0.02 and p.y < wy - 0.05)
        if kf is None:
            bpy.data.objects.remove(kk_, do_unlink=True)
            print('KICKER cannot leave the frame: removed')
        else:
            print('KICKER out of frame at x%.1f' % kf, tuple(round(v, 3) for v in kk_.location))
    if os.environ.get('CARD_AUDIT'):
        # round 14 (the coordinator's card audit): ray-cast the frame (every max(W,H)/240 px) and report, for each object
        # hidden from the camera, the share of rays whose first hit it would be; then each object that casts no shadow
        from mathutils import Vector
        bpy.context.view_layer.update()               # 2026-11-09: the world matrices are stale until updated
        sc = bpy.context.scene; cam_ob = sc.camera
        hidden = [o for o in sc.objects if o.type == 'MESH' and not o.visible_camera]
        dg = bpy.context.evaluated_depsgraph_get()
        W, H = sc.render.resolution_x, sc.render.resolution_y
        step = max(W, H) / 240.0
        fr = [cam_ob.matrix_world @ v for v in cam_ob.data.view_frame(scene=sc)]   # tr, br, bl, tl
        o = cam_ob.matrix_world.translation
        hits = {h.name: 0 for h in hidden}; n = 0
        y = step / 2
        while y < H:
            x = step / 2
            while x < W:
                u, v = x / W, y / H
                top = fr[3].lerp(fr[0], u); bot = fr[2].lerp(fr[1], u); pt = top.lerp(bot, v)
                d = (pt - o).normalized(); n += 1
                for h in hidden:   # each card alone, as a real card there would be: occlusion ignored
                    mi = h.matrix_world.inverted(); lo = mi @ o; ld = (mi.to_3x3() @ d).normalized()
                    if h.ray_cast(lo, ld)[0]:
                        hits[h.name] += 1
                x += step
            y += step
        print('CARD-AUDIT', frame, {k: round(100.0 * v / n, 1) for k, v in hits.items()}, 'rays', n)
        # the coordinator's 19:13 rule: the lamps too (hiddencast_bpy: every hidden mesh and lamp, by ray-cast)
        sys.path.insert(0, os.path.join(HERE, 'launch'))
        from hiddencast_bpy import hiddencast, report
        print(report(frame, hiddencast(sc)))
        print('NO-SHADOW', frame, [o.name for o in sc.objects if o.type == 'MESH' and not o.visible_shadow])
        print('LIGHTS', frame, [(o.name, o.data.type, round(o.data.energy, 3)) for o in sc.objects if o.type == 'LIGHT'])
        return
    os.makedirs(OUT, exist_ok=True)
    out = os.environ.get('LAMP_OUT') or os.path.join(OUT, frame + '.png')
    bpy.context.scene.render.filepath = out
    bpy.ops.render.render(write_still=True)


if __name__ == '__main__':
    a = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else sys.argv[1:]
    build(a[0], int(a[a.index('--samples') + 1]) if '--samples' in a else 256,
          float(a[a.index('--scale') + 1]) if '--scale' in a else 1.0)
