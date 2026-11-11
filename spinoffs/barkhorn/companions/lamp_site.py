"""The site's lit lamp pictures, honest (the coordinator, 2026-11-09: the faked ones are pulled). Each lamp is lit by its
own light at its real output, on one photometric scale, on a pale paper sweep lit by real studio lights; nothing hidden
from the camera, from reflections or from view through the acrylic, nothing linked, every part casting shadows.

    python3.11 spinoffs/barkhorn/companions/lamp_site.py FRAME [--samples N] [--scale S]

FRAME:
    dome-<colour>   Hemisphere lit, 1600 x 2000 (4:5)          lamps-domes   the eight in a row, 2400 x 800 (3:1)
    orb-<colour>    Core B lit (the concentric Ø140 opal core, 2026-11-10), 4:5     lamps-orbs    the eight in a row, 2400 x 800
<colour> is the site's key: red amber? see COLOURS. Output: renders/2026-11-09/barkhorn/lamp-site/FRAME.png.
Env: LAMP_OUT (output path), STUDIO (scale of every studio light, default 1), AUDIT=1 (the card audit, no render).

The lamps as drawn: Hemisphere v3 (a 3 mm stock tint R 100-97, a 6 mm clear shell R 96-90, the opal liner R 89-86, its
edge 4 inside the rim, the CAD's rim, collar and hub; the liner the CAD's neutral opal), its Bridgelux Vero SE 10 at
2700 K; Core B (2026-11-10): a 6 mm tinted ball polished both faces round a concentric Ø140 3 mm opal core (GS 041,
one scattering face), the CAD's raised grommet with its bore bright, the clear window, on its signed dock; lit ONLY by
its Ø26 LED disc at 200 lm (CORE_DESIGN=A: Core A, the record).

One photometric scale (lamp_pictures.py, round 13): 0.0065 W of Blender power for each lumen.
  Hemisphere: ~575 lm at the COB (crystal.py), 85 % out: ~490 lm down through the mouth (a 0.17 m disc at the mouth,
  92 deg spread, 3.2 W), and the reflector's spill, a quarter (145 lm), out through the liner (its lit face, ruling 3's
  exception: 11.5 W/m2 on average over its 0.041 m2 outer face, both ways, brighter at the crown).
  Core: its drawn LED, 200 lm at 1.5 W (out-orb-table bom since 2026-11-01; until round 3 the pictures used round 4's
  620 lm), ~180 lm out of the ball (1.2 W), as the lit frosted face (ruling 3's exception): 9.3 W/m2 on its 0.0633 m2,
  both ways, its colour through the whole 9 mm wall.
The thin shells pass shadow rays at their own transmission (lamp_pictures.thin_shadow), so the lamps light the set.
"""
import math, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
OUT = os.path.join(ROOT, 'renders', '2026-11-09', 'barkhorn', 'lamp-site')
WLM = 3.2 / 490.0                                     # Blender W per lumen (the one scale)
CORE_LM = float(os.environ.get('CORE_LM', '200'))     # Core's LED as drawn (bom: 200 lm at 1.5 W)
CORE_OUT = 0.9                                        # out of the ball (the frost's and the port's losses)
CCT = int(os.environ.get('LAMP_CCT', '2700'))
# item 90 (the coordinator's open proposal to the owner, PROPOSAL): each tint at its own colour temperature
CCT_PER_TINT = {'blue': 5700, 'violet': 4000}         # the rest 2700
# the LED colour per tint (the owner, 2026-11-10: "some need warm and some need amber"): amber 2200 K for Ember; 2700 K
# for Dust, Acid (moved from amber 23:50: 2200 K carries almost none of the light their dyes remove, so they read pale),
# Poison, Fog and Smoke; 3000 K for Ice and Haze. Both lamps; LED_K overrides
LED_CCT = {'red': 2200, 'orange': 2700, 'amber': 2700, 'green': 2700, 'ice': 2700, 'black': 2700, 'blue': 3000, 'violet': 3000}
# 2026-11-11 (the owner, "Go", on the Core colour test ae86581b): 4000 K for Dust, Acid, Ice and Smoke; Ember 2200 K,
# Poison and Fog 2700 K, Haze 3000 K
LED_CCT.update({'orange': 4000, 'amber': 4000, 'blue': 4000, 'black': 4000})
# the outer shell's dye loading per tint, as a multiple of the chart figure at the wall (Core's 6 mm at 0.5, Hemisphere's
# 3 mm at 1): Dust, Acid and Ice a custom pour at 3x; Smoke the speakers' own pour (about 54 % through Core's 6 mm),
# 0.3x; the rest 1x
# Core's base options (2026-11-11, for the owner): the turned outside of base and touch ring, (r, z) in mm from the
# base's foot (the dock's pocket floor). A: the CAD's angled base as drawn. B: the same cone, the top edge turned over in
# a 7 mm bullnose where it meets the ball (rim at z 38, as now). C: a classic crystal-ball stand, as narrow as the base allows
# (2026-11-11, the bar: narrower than its ball): a rounded foot ring Ø129, a shallow concave waist Ø118.6 (5 mm outside
# the cells' bays at r 54.2), a rounded rim Ø126.6 rising to z 40.8 that cradles the ball (meeting it at r 53.6, z 40.6). The ball's place is unchanged
BASE_PROFILES = {'B': [(49, 0), (60, 0), (60, 1.5), (71.71, 1.5), (60.0, 30.0), (60.0, 31.0), (59.894, 32.216), (59.578, 33.394), (59.062, 34.5), (58.362, 35.5), (57.5, 36.362), (56.5, 37.062), (55.394, 37.578), (54.216, 37.894), (53.0, 38.0), (50.3, 38.0), (49, 38.0)], 'C': [(49, 0), (60, 0), (60, 1.5), (63, 1.5), (64.2, 2.3), (64.6, 3.8), (64.2, 5.3), (63, 6.3), (61.5, 7.8), (60.3, 10), (59.6, 13), (59.3, 16), (59.4, 19), (59.9, 22), (60.8, 25), (61.9, 28), (62.8, 31), (63.3, 34), (63.2, 36.5), (62.4, 38.5), (60.8, 39.9), (58.6, 40.6), (56, 40.8), (53.6, 40.6), (51, 39.5), (49, 39.5)]}
_iC = BASE_PROFILES['C'].index((62.8, 31))
BASE_LOW = {'A': [(60, 0), (60, 1.5), (71.71, 1.5), (60, 30)], 'B': BASE_PROFILES['B'][1:5], 'C': BASE_PROFILES['C'][1:_iC + 1]}
BASE_UP = {'B': BASE_PROFILES['B'][4:], 'C': BASE_PROFILES['C'][_iC:]}       # the touch ring (A: the CAD's ring)
BASE_ALL = [(68.5, -6.5), (75.0, -6.5), (61.849, 25.5), (61.784, 26.754), (61.588, 27.995), (61.263, 29.208), (60.813, 30.381), (60.242, 31.5), (59.558, 32.553), (58.768, 33.53), (57.88, 34.418), (56.903, 35.208), (55.85, 35.892), (54.731, 36.463), (53.558, 36.913), (52.345, 37.238), (51.104, 37.434), (49.85, 37.5)]   # B all in its own colour (the default, 2026-11-11): the skirt to the floor (r 75 at z -6.5), the lip a bullnose R12 (forms in one piece from 6 mm)
TINT_LOAD = {'orange': 3.0, 'amber': 3.0, 'blue': 3.0, 'black': 0.3}
# the site's colour keys (web.py HABITAT) to the tints
COLOURS = {'red': 'Ember', 'orange': 'Dust', 'amber': 'Acid', 'green': 'Poison', 'blue': 'Ice', 'violet': 'Haze',
           'ice': 'Fog', 'black': 'Smoke dark'}
ROW = ['red', 'orange', 'amber', 'green', 'blue', 'violet', 'ice', 'black']        # spectrum order, Ember to Smoke


def lum(c):
    return 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2]


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
    kind0 = 'dome' if frame.startswith(('lamps-domes', 'trio-', 'cluster')) else 'orb' if frame.startswith(('lamps-orbs', 'baseopts')) else frame.split('-')[0]
    # the studio's brightness and the exposure move together, so the paper holds its tone while the lamp, at its real
    # output, comes out of clipping: a brighter studio, one scale
    # round 3 (the gate, wf_5760aeac-7cd): Hemisphere's studio x1 with the camera at -2 EV (the lamp up 1 EV against the
    # studio, the paper held at K x 2^EV = 0.25); Core's studio unchanged, its camera at -5 (b, as round 2) or -5.7 (a)
    K = float(os.environ.get('STUDIO', {'dome': '1.0', 'orb': '8.0', 'lamps': '4.0'}[kind0]))
    # round 2 (the gate, 2026-11-09, wf_a02e1a2a-b5e): the camera 2 EV down, the studio unchanged, so the faces leave
    # AgX's shoulder and hold their tint; the paper falls to about L 0.5-0.6 (both heroes' papers K x 2^EV match)
    EVD = {'dome': '-2.0', 'orb': '-5.0'}[kind0]

    def acrylic(nm, rough, tname, loading=1.0):
        return SC.acrylic_material(nm, [(-1e4, 1e4, tname)], rough, 'polished', loading=loading, scratch=0.0, bond=False)

    def shell_T(tint, loading, mm):
        return tuple(math.exp(-a * mm / 1000.0) * 0.96 for a in SC.absorption(tint, loading))

    def thin_shadow(m, T, T_back=None):
        if os.environ.get('THIN', '1') == '0':        # (THIN=0: plain glass, the light only by refraction, unbiased)
            return m
        # round 3 (2026-11-09): T_back, if given, is what a shadow ray meets leaving the shell from inside (Backfacing):
        # Core A's ball passes a studio light's or the sun's light to its frost only through the dye (T9), and the frost
        # face's own light out at 0.96 (its emission already carries T9). At 0.96 both ways, A returned undyed light
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
    # Core's base and dock SATIN (the owner, 2026-11-11: "satin or matte instead of shiny plastic. It looks cheap
    # otherwise"): black cast acrylic bead-blasted, close to matte, no mirror highlights; the touch ring satin black
    # anodized to match. CORE_GLOSS=1 for the old polished base
    satin_black = black_acrylic if os.environ.get('CORE_GLOSS') else SC.principled('satin-black', '#0B0B0C', 0.6)
    satin_an = an if os.environ.get('CORE_GLOSS') else SC.principled('satin-anodised', '#0C0C0D', 0.5, 1.0)
    an = SC.anodised()
    steel = SC.principled('steel', '#C9C9C6', 0.25, 1.0, bump=(2500.0, 0.6))
    # the bore's reflector: high-reflectance aluminium, faceted (crystal.py): a bright, low-roughness metal
    refl = SC.principled('reflector', os.environ.get('REFL_COL', '#F2F2F0'), float(os.environ.get('REFL_R', '0.12')), 1.0)
    # 2026-11-11 (the bar: one hardware finish, satin black): the cap's turned parts satin black anodized, a soft
    # sheen so each eased edge catches a highlight (was a flat dark grey, read as a lump)
    cap = SC.principled('cap', '#161618', 0.38, metallic=1.0, bump=(4000.0, 0.08))

    oc_ = (0.93, 0.93, 0.92)                      # the CAD's neutral opal
    def opal(nm):
        m = bpy.data.materials.new(nm); m.use_nodes = True; nt = m.node_tree; nt.nodes.clear()
        o = nt.nodes.new('ShaderNodeOutputMaterial'); tr = nt.nodes.new('ShaderNodeBsdfTranslucent')
        gl = nt.nodes.new('ShaderNodeBsdfGlossy'); gl.inputs['Roughness'].default_value = 0.08
        # 2026-11-10 (the coordinator: the opal decides how bright the as-drawn dome reads): the opal at a stocked
        # grade's datasheet, Perspex GS Opal/White 041, 3 mm (Perspex technical data sheet, section 5, ASTM D1003,
        # Illuminant C): T 54 %, R 39 %, so A 7 %. Here: a 4 % glossy face, then 60.5 % translucent at 0.93 (T 0.54)
        # and 39.5 % diffuse at 0.923 (R 0.04 + 0.35). Until now T 0.44, R 0.47, A 0.09 (OPAL=old for that)
        old_ = os.environ.get('OPAL') == 'old'
        df = nt.nodes.new('ShaderNodeBsdfDiffuse'); m1 = nt.nodes.new('ShaderNodeMixShader'); m1.inputs[0].default_value = 0.5 if old_ else 0.605
        m2 = nt.nodes.new('ShaderNodeMixShader'); m2.inputs[0].default_value = 0.06 if old_ else 0.04
        tr.inputs['Color'].default_value = (*oc_, 1)
        df.inputs['Color'].default_value = (*(v * 0.97 for v in oc_), 1) if old_ else (0.923, 0.923, 0.915, 1)
        nt.links.new(df.outputs[0], m1.inputs[1]); nt.links.new(tr.outputs[0], m1.inputs[2])
        nt.links.new(m1.outputs[0], m2.inputs[1]); nt.links.new(gl.outputs[0], m2.inputs[2]); nt.links.new(m2.outputs[0], o.inputs['Surface'])
        return m

    def hemisphere(tint, x, rim_z, y=0.0):
        """Hemisphere v3 as drawn, lit, its rim's centre at (x, y, rim_z)."""
        tname = COLOURS[tint]; bb = bbt(tint)
        c = (x, y, rim_z); H = 48.2
        if os.environ.get('HEMI_BARE'):   # (flux check: the COB alone, no fitting: the 100 % reference)
            ld = bpy.data.lights.new(f'cob-{tint}', 'AREA'); ld.shape = 'DISK'; ld.size = 0.011; ld.energy = float(os.environ.get('COB_LM', '430')) * WLM
            ld.color = bb; ob = bpy.data.objects.new(f'cob-{tint}', ld); bpy.context.scene.collection.objects.link(ob)
            ob.location = (x, y, rim_z + 0.0815)
            return
        if os.environ.get('HEMI_ENGINE', 'ring') == 'ring':
            # OPTION 3 (the owner, 2026-11-10: "it should work like core cut in half ... downward cast light will be the
            # colour of the bulb"): the CAD's ring board at the mouth's centre facing up, 24 mid-power LEDs, about
            # 1,000 lm, 2700 K (3000 K for Ice and Haze); BARE (no stock ring optic with an IES file was found: no
            # invented lobe). The ONLY emitters are the 24 LED faces. No thin_shadow, no liner emission, no clamp, no
            # denoiser. The opal one scattering face (its outside, GS 041), a closed solid to the rim: its inside and its
            # edge plain clear acrylic
            bl = blackbody(int(os.environ.get('LED_K', 0)) or LED_CCT.get(tint, 2700))   # its tint's LED colour
            lt_ = float(os.environ.get('HEMI_LOAD', TINT_LOAD.get(tint, 1.0)))     # the 3 mm shade's loading (2026-11-11)
            sphere(f'tint-{tint}', 100.0, c, acrylic(f'tint-{tint}', 0.0, tname, lt_), cut=0.0, hole=H)
            sphere(f'tint-in-{tint}', 97.0, c, acrylic(f'tint-in-{tint}', 0.0, tname, lt_), inward=True, cut=0.0, hole=H)
            sphere(f'clear-{tint}', 96.0, c, acrylic(f'clear-{tint}', 0.0, 'Clear'), cut=4.0, hole=H)
            sphere(f'clear-in-{tint}', 90.0, c, acrylic(f'clear-in-{tint}', 0.0, 'Clear'), inward=True, cut=4.0, hole=H)
            # the scattering face is the opal's INSIDE (facing the LEDs, so its light is sampled directly; a clear inside
            # face would block every shadow ray to them and leave only caustic paths); its outside and edge clear
            clr = acrylic(f'opal-face-{tint}', 0.0, 'Clear')
            sphere(f'opal-{tint}', 89.0, c, clr, cut=0.0, hole=H)
            sphere(f'opal-in-{tint}', 86.0, c, opal(f'opal-{tint}'), inward=True, cut=0.0, hole=H)
            bm = bmesh.new(); n_ = 256
            ra = [bm.verts.new((0.086 * math.cos(2 * math.pi * k / n_), 0.086 * math.sin(2 * math.pi * k / n_), 0.0)) for k in range(n_)]
            rb = [bm.verts.new((0.089 * math.cos(2 * math.pi * k / n_), 0.089 * math.sin(2 * math.pi * k / n_), 0.0)) for k in range(n_)]
            for k in range(n_):
                bm.faces.new((ra[k], rb[k], rb[(k + 1) % n_], ra[(k + 1) % n_]))
            for f_ in bm.faces:
                if f_.normal.z > 0:
                    f_.normal_flip()
            me = bpy.data.meshes.new(f'opal-edge-{tint}'); bm.to_mesh(me); bm.free(); me.materials.append(clr)
            eo = bpy.data.objects.new(f'opal-edge-{tint}', me); bpy.context.scene.collection.objects.link(eo); eo.location = c
            part('out-dome-pendant', 'rim', acrylic(f'rim-{tint}', 0.0, tname, 0.5), c)   # (polished, chamfered: the bar)
            for nm in ('clamp', 'crown', 'gland', 'hub'):
                part('out-dome-pendant', nm, cap, c)
            white = SC.principled('crown-white', '#EEEEEA', 0.55)
            # the collar: its flange face inside the shade white (below z 80 in the shade's frame), the rest black
            cm = bpy.data.materials.new(f'collar-{tint}'); cm.use_nodes = True; nt = cm.node_tree
            mx = nt.nodes.new('ShaderNodeMixShader'); tc = nt.nodes.new('ShaderNodeTexCoord'); sx = nt.nodes.new('ShaderNodeSeparateXYZ')
            lt = nt.nodes.new('ShaderNodeMath'); lt.operation = 'LESS_THAN'; lt.inputs[1].default_value = 0.080
            nt.links.new(tc.outputs['Object'], sx.inputs[0]); nt.links.new(sx.outputs['Z'], lt.inputs[0]); nt.links.new(lt.outputs[0], mx.inputs[0])
            b1 = nt.nodes.new('ShaderNodeBsdfPrincipled'); b1.inputs['Base Color'].default_value = (0.012, 0.012, 0.013, 1); b1.inputs['Roughness'].default_value = 0.45
            b2 = nt.nodes.new('ShaderNodeBsdfPrincipled'); b2.inputs['Base Color'].default_value = (0.85, 0.85, 0.82, 1); b2.inputs['Roughness'].default_value = 0.55
            nt.links.new(b1.outputs[0], mx.inputs[1]); nt.links.new(b2.outputs[0], mx.inputs[2])
            nt.links.new(mx.outputs[0], nt.nodes['Material Output'].inputs['Surface'])
            part('out-dome-pendant', 'collar', cm, c)
            part('out-dome-pendant', 'white-disc', white, c)
            part('out-dome-pendant', 'ring', SC.principled('peek', '#151515', 0.6), c)
            part('out-dome-pendant', 'pins', steel, c)
            part('out-dome-pendant', 'gaskets', SC.principled('silicone', '#111111', 0.7), c)
            part('out-dome-pendant', 'cord', SC.principled('braid', '#121212', 0.75, bump=(1200.0, 0.5)), c)
            part('out-dome-pendant', 'carrier', an, c)
            part('out-dome-pendant', 'stem', an, c)
            part('out-dome-pendant', 'board', SC.principled('board', '#E6E4DE', 0.5), c)
            lm = float(os.environ.get('HEMI_LM', '1000')) * (0.0 if os.environ.get('LIGHTS_OFF') else 1.0)
            for k in range(24):
                a_ = 2 * math.pi * k / 24
                ld = bpy.data.lights.new(f'led-{tint}-{k}', 'AREA'); ld.shape = 'SQUARE'; ld.size = 0.0026
                ld.energy = lm / 24 * WLM / lum(bl); ld.color = bl   # (its lumens at the colour's luminance)
                ob = bpy.data.objects.new(f'led-{tint}-{k}', ld); bpy.context.scene.collection.objects.link(ob)
                ob.location = (x + 0.019 * math.cos(a_), y + 0.019 * math.sin(a_), rim_z + 0.00492)   # just over the LED's top (4.9)
                ob.rotation_euler = (math.pi, 0.0, 0.0)                                                 # facing up
                ob.visible_camera = ob.visible_glossy = ob.visible_diffuse = ob.visible_transmission = True
            return
        Tt, Tc = shell_T(tname, 1.0, 1.5), shell_T('Clear', 1.0, 3.0)
        sphere(f'tint-{tint}', 100.0, c, thin_shadow(acrylic(f'tint-{tint}', 0.0, tname), Tt), cut=0.0, hole=H)
        sphere(f'tint-in-{tint}', 97.0, c, thin_shadow(acrylic(f'tint-in-{tint}', 0.0, tname), Tt), inward=True, cut=0.0, hole=H)
        sphere(f'clear-{tint}', 96.0, c, thin_shadow(acrylic(f'clear-{tint}', 0.0, 'Clear'), Tc), cut=4.0, hole=H)
        sphere(f'clear-in-{tint}', 90.0, c, thin_shadow(acrylic(f'clear-in-{tint}', 0.0, 'Clear'), Tc), inward=True, cut=4.0, hole=H)
        oc = 4.0
        lit = opal(f'opal-lit-{tint}'); nt = lit.node_tree
        # (round 2, the gate: the liner passed all 145 lm; a real opal of about 55 % passes about half outward, the rest
        # back into the shade and out through the mouth)
        S0 = float(os.environ.get('LINER_LM', '145')) * float(os.environ.get('OPAL_T', '0.55')) * WLM / (2 * 0.041)   # LINER_LM=0: the liner lit by the COB alone (the photometry audit)
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
        if os.environ.get('HEMI_REFL', '1') == '1':   # (diagnostic switch)
            part('out-dome-pendant', 'reflector', refl, c)
        part('out-dome-pendant', 'cord', SC.principled('braid', '#121212', 0.75, bump=(1200.0, 0.5)), c)
        # round 3 (the Mantle lane's flag, the coordinator 18:13): the COB as the CAD builds it, a Vero SE 10's ~11 mm
        # emitting face at the top of the 46 bore (its face 82 above the rim, 22 up from the bore's mouth at 60), the
        # faceted reflector round it, the cut-off from that geometry, not a spread setting. Of the COB's ~575 lm, the
        # liner's 145 lm is its own emission above; the other ~430 lm leave the COB here, and the bore and reflector
        # take what they really take
        # COB_DZ (mm, a PROPOSAL for the owner, 2026-11-09): the COB and its carrier lowered down the bore, so its
        # cut-off widens from the drawn 47 deg (22 up the 46 bore) and the light between the mouth's 46 deg and the new
        # cut-off falls on the opal liner: a real path to the glow (8.2: 13.3 up the bore, 60 deg)
        cdz = float(os.environ.get('COB_DZ', '0')) * MM
        cob_ob = part('out-dome-pendant', 'cob', SC.principled('cob-body', '#2A2A2A', 0.5), c)
        if cdz and cob_ob is not None:
            cob_ob.location.z -= cdz
        ld = bpy.data.lights.new(f'cob-{tint}', 'AREA'); ld.shape = 'DISK'; ld.size = 0.011; ld.energy = float(os.environ.get('COB_LM', '430')) * WLM
        ld.color = bb
        ob = bpy.data.objects.new(f'cob-{tint}', ld); bpy.context.scene.collection.objects.link(ob)
        ob.location = (x, y, rim_z + 0.0815 - cdz)
        rl = float(os.environ.get('RING_LM', '0'))
        if rl > 0:
            # PROPOSAL (2026-11-09, for the owner): a ring of mid-power LEDs, 2700 K, on a band round the hub's outside
            # (r 32, z 64 to 72 above the rim), facing out onto the opal liner's inside: the glow's own light, a real
            # part (in the CAD it would be a flex board on the hub, its driver beside the COB's)
            bm = bmesh.new(); r_, z0r, z1r = 0.032, 0.064, 0.072
            nled = int(os.environ.get('RING_N', '24'))   # discrete LEDs (2835 class, 2.8 x 3.5 mm), even pitch
            if nled > 0:
                # each LED a small emitting face on the band (its light-emitting area), facing out; the band itself
                # a white board between them (not emitting)
                for i in range(nled):
                    a0 = 2 * math.pi * i / nled; hw = 0.0014 / r_
                    p_ = [bm.verts.new(((r_ + 0.0005) * math.cos(a0 + sa * hw), (r_ + 0.0005) * math.sin(a0 + sa * hw), 0.068 + sz * 0.00175))
                          for sa, sz in ((-1, -1), (1, -1), (1, 1), (-1, 1))]
                    bm.faces.new(p_)
                area = nled * 0.0028 * 0.0035
            else:
                n = 64
                vs = [(bm.verts.new((r_ * math.cos(2 * math.pi * i / n), r_ * math.sin(2 * math.pi * i / n), z0r)),
                       bm.verts.new((r_ * math.cos(2 * math.pi * i / n), r_ * math.sin(2 * math.pi * i / n), z1r))) for i in range(n)]
                for i in range(n):
                    a_, b_ = vs[i], vs[(i + 1) % n]
                    bm.faces.new((a_[0], b_[0], b_[1], a_[1]))
                area = 2 * math.pi * r_ * (z1r - z0r)
            bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
            me = bpy.data.meshes.new(f'ring-led-{tint}'); bm.to_mesh(me); bm.free()
            ro = bpy.data.objects.new(f'ring-led-{tint}', me); bpy.context.scene.collection.objects.link(ro); ro.location = c
            em = bpy.data.materials.new(f'ring-led-em-{tint}'); em.use_nodes = True
            bsdf = em.node_tree.nodes['Principled BSDF']; bsdf.inputs['Base Color'].default_value = (0.9, 0.9, 0.88, 1)
            bsdf.inputs['Emission Color'].default_value = (*bb, 1); bsdf.inputs['Emission Strength'].default_value = rl * WLM / area
            em.cycles.emission_sampling = 'FRONT'
            me.materials.append(em)

    def core(tint, x, floor_z, y=0.0, rot=0.0, base=None):
        """Core A as drawn, on its dock, lit, the dock's underside on floor_z at (x, y)."""
        tname = COLOURS[tint]; bb = bbt(tint)
        z0 = floor_z + 0.0065                         # the dock's underside on the floor (as lamp_pictures: the CAD's
                                                      # dock underside sits 6.5 below its origin)
        objs = []
        base = base or os.environ.get('CORE_BASE', 'B')   # B, the rounded lip: the owner's pick (2026-11-11)
        def revolve(nm, prof, mat, flip=False, off=0.0):
            # a turned surface: the (r, z) profile in mm (material on its left as it is walked) spun about the axis,
            # its normals outward (flip: inward), the profile moved in by `off` mm
            bm = bmesh.new(); n_ = 192
            pr = [(max(r_ - off, 0.1), z_) for r_, z_ in prof]
            rings = [[bm.verts.new((r_ * MM * math.cos(2 * math.pi * k / n_), r_ * MM * math.sin(2 * math.pi * k / n_), z_ * MM))
                      for k in range(n_)] for r_, z_ in pr]
            for i in range(len(pr) - 1):
                dr, dz = pr[i + 1][0] - pr[i][0], pr[i + 1][1] - pr[i][1]
                if abs(dr) + abs(dz) < 1e-9:
                    continue
                o2 = (dz, -dr)                                     # outward in (r, z): the right of the walk
                for k in range(n_):
                    k2 = (k + 1) % n_
                    f_ = bm.faces.new((rings[i][k], rings[i][k2], rings[i + 1][k2], rings[i + 1][k]))
                    f_.normal_update(); a_ = 2 * math.pi * (k + 0.5) / n_
                    want = (o2[0] * math.cos(a_), o2[0] * math.sin(a_), o2[1])
                    if (f_.normal.x * want[0] + f_.normal.y * want[1] + f_.normal.z * want[2] < 0) != flip:
                        f_.normal_flip()
                    f_.smooth = True
            me = bpy.data.meshes.new(nm); bm.to_mesh(me); bm.free(); me.materials.append(mat)
            ob_ = bpy.data.objects.new(nm, me); bpy.context.scene.collection.objects.link(ob_); ob_.location = (x, y, z0)
            return ob_
        bm_ = os.environ.get('BASE_MAT', 'own_all')   # the default (2026-11-11): the whole base in its own colour
        own = bm_ in ('own', 'own_all')
        own_all = bm_ == 'own_all'
        if base in BASE_PROFILES or own:
            # base options for the owner (2026-11-11: "the base should look like the base of a crystal ball"; "the same
            # color acrylic for the base ... in satin"): the turned outside as a revolved profile (r, z in mm from the
            # base's foot). Satin black, or OWN COLOUR: the lower part (below the touch ring) a 6 mm skin of the shell's
            # own pour (the same loading as the ball's 6 mm wall), satin outside, over a white opal liner that hides the
            # battery, board and contacts; the touch ring stays satin black anodized. Only the outside is seen
            lo_, up_ = BASE_LOW[base], BASE_UP.get(base)
            if own_all:
                # B all in its own colour (the coordinator, 2026-11-11 16:37): one skin from the ball's seat down to the
                # floor, the bullnose lip included, the dock hidden under the skirt, the touch electrode under the skin
                lo_, up_ = BASE_ALL, None
            if own and base == 'C':
                # C in its own colour grows 3 mm in radius below the touch ring, so the 6 mm skin and liner clear the
                # cells' bays (the coordinator, 2026-11-11: "C may grow 3 mm for it")
                lo_ = [(r_ + 3.0 if 0 < i < len(lo_) - 1 else r_, z_) for i, (r_, z_) in enumerate(lo_)]
                up_ = [(up_[0][0] + 3.0, up_[0][1])] + up_[1:]
            if own:
                ld_ = float(os.environ.get('CORE_LOAD', 0.5 * TINT_LOAD.get(tint, 1.0)))
                sk = acrylic(f'base-skin-{tint}', 0.55, tname, ld_)        # satin outside: a fine bead-blast, as rough glass
                revolve(f'base-skin-{base}-{tint}', lo_, sk)
                revolve(f'base-skin-in-{base}-{tint}', lo_, acrylic(f'base-skin-in-{tint}', 0.0, tname, ld_), flip=True, off=6.0)
                revolve(f'base-liner-{base}-{tint}', lo_, SC.principled('base-liner', '#EDEDEA', 0.8), off=6.4)
            else:
                revolve(f'base-{base}-{tint}', lo_, satin_black)
            if up_:
                revolve(f'base-ring-{base}-{tint}', up_, satin_an)
        for nm, m in tuple(p_ for p_ in (('dock', satin_black), ('base', satin_black), ('ring', satin_an), ('seat', SC.principled('si', '#111111', 0.6)),
                      ('dock-cable', SC.principled('braid', '#121212', 0.75, bump=(1200.0, 0.5)))) + \
                     (('grommet', an),) if not (((base in BASE_PROFILES or own) and p_[0] in ('base', 'ring') and not (base == 'A' and p_[0] == 'ring' and not own_all)) or (own_all and p_[0] == 'dock'))):
            objs.append(part('out-orb-table', nm, m, (x, y, z0)))   # (the base and dock angled, the owner, 2026-11-10)
        # the light well, white PTFE round the window (2026-11-10)
        part('out-orb-table', 'well', SC.principled('ptfe', '#F7F7F5', 0.7), (x, y, z0))
        # the window over the LED (the CAD's clear acrylic plug, Ø29.6 x 5.7): clear, its shadow rays at its transmission
        # WINDOW: filter (default: a clear filter at its transmission for every ray, no refraction: the enclosing
        # sensor showed thin_shadow on this solid plug counting the LED's light twice, once by the shadow ray and once
        # by the refracted caustic, 27 lm against 15.5 with no window), thin, glass (plain: caustics only), none
        wmode = os.environ.get('WINDOW', 'filter')
        if wmode != 'none':
            wm_ = acrylic(f'window-{tint}', 0.0, 'Clear')
            if wmode == 'filter':
                wm_ = bpy.data.materials.new(f'window-{tint}'); wm_.use_nodes = True; nt_ = wm_.node_tree; nt_.nodes.clear()
                tb = nt_.nodes.new('ShaderNodeBsdfTransparent'); tb.inputs['Color'].default_value = (*shell_T('Clear', 1.0, 5.7), 1)
                nt_.links.new(tb.outputs[0], nt_.nodes.new('ShaderNodeOutputMaterial').inputs['Surface'])
            part('out-orb-table', 'window', thin_shadow(wm_, shell_T('Clear', 1.0, 5.7)) if wmode == 'thin' else wm_, (x, y, z0))
        zc = z0 + 100.45 * MM
        if os.environ.get('CORE_DESIGN', 'B') == 'B':
            # Core B, CONCENTRIC (the owner, 2026-11-10 00:28: "the outer core should be the same depth around the whole
            # inner core"; the coordinator's 02:24 brief): the 6 mm outer ball in the speaker's dye, polished both faces,
            # its Ø40 port; the white opal core on the same centre (CORE_R: 60, 65 or 70, the size the owner picks),
            # ONE scattering face of Perspex GS 041 (T 0.54, R 0.39; two full faces would act as T 0.34), no emission;
            # the grommet raised to suit: its shoulder where the core's Ø40 opening meets it, a 3 mm spigot above
            # CORE_LOAD: the outer ball's dye loading (0.5: the chart figure at its 6 mm wall; the speakers' own pour at 6 mm
            # is about 0.15, since their chart figure is at 20 mm). A test switch (2026-11-11), the default unchanged
            ld_ = float(os.environ.get('CORE_LOAD', 0.5 * TINT_LOAD.get(tint, 1.0)))
            Tb = shell_T(tname, ld_, 3.0)
            sphere(f'ball-{tint}', 80.0, (x, y, zc), thin_shadow(acrylic(f'ball-{tint}', 0.0, tname, ld_), Tb), hole_below=20.0)
            sphere(f'ball-in-{tint}', 74.0, (x, y, zc), thin_shadow(acrylic(f'ball-in-{tint}', 0.0, tname, ld_), Tb), inward=True, hole_below=20.0)
            ri = float(os.environ.get('CORE_R', '70')); zi = zc - float(os.environ.get('CORE_DZ', '0')) * MM
            sphere(f'core-{tint}', ri, (x, y, zi), opal(f'core-opal-{tint}'), hole_below=20.0)
            # the grommet, raised (base frame: its foot at z 23.0; the core's opening meets r 20 at zf)
            zf = (zi - z0) / MM - math.sqrt(ri ** 2 - 20.0 ** 2)
            def tube(nm, r_out, r_in, za, zb, mat):
                bm = bmesh.new(); seg = 96
                for (ra, rb) in ((r_out, r_out), (r_in, r_in)):
                    pass
                prof = [(r_in, za), (r_out, za), (r_out, zb), (r_in, zb)]
                rings = [[bm.verts.new((rr * MM * math.cos(2 * math.pi * k / seg), rr * MM * math.sin(2 * math.pi * k / seg), zz * MM))
                          for k in range(seg)] for (rr, zz) in prof]
                for a_ in range(4):
                    r0, r1 = rings[a_], rings[(a_ + 1) % 4]
                    for k in range(seg):
                        bm.faces.new((r0[k], r0[(k + 1) % seg], r1[(k + 1) % seg], r1[k]))
                bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
                me = bpy.data.meshes.new(nm); bm.to_mesh(me); bm.free()
                ob = bpy.data.objects.new(nm, me); bpy.context.scene.collection.objects.link(ob); ob.location = (x, y, z0)
                me.materials.append(mat)
                for f_ in me.polygons:
                    f_.use_smooth = True
                return ob
            bore = SC.principled(f'bore-{tint}', '#F2F2F0', 0.12, 1.0)      # machined bright after anodizing (the brief)
            tube(f'grommet-bore-{tint}', 16.97, 16.95, 23.05, zf + 2.95, bore)   # its bore, bright, a hair inside the CAD's
        else:
            # Core A, the record (CORE_DESIGN=A)
            T9 = shell_T(tname, 1 / 3, 9.0)

            sphere(f'ball-{tint}', 80.0, (x, y, zc), thin_shadow(acrylic(f'ball-{tint}', 0.0, tname, 1 / 3), (0.96, 0.96, 0.96), T9), hole_below=20.0)
            # round 3: the frost's diffuse lobe takes the wall's tint (SC.frosted; it was a flat grey: untinted light)
            fm = SC.frosted(acrylic(f'frost-{tint}', 0.6, tname, 1 / 3))
            # the drawn LED (out-orb-table bom, since the review of 2026-11-01): 200 lm at 1.5 W, warm-dim 2200/2700 K;
            # about 90 % of it out of the ball (round 3, 2026-11-09: it was 620 lm at the LED, round 4's figure, three times
            # the drawn part's output, against the rule "never brighten a lamp past its real output")
            S = CORE_LM * CORE_OUT * WLM / (2 * 0.0633)
            add_emission(fm, tuple(bb[i] * T9[i] / 0.96 for i in range(3)), S)
            sphere(f'frost-{tint}', 71.0, (x, y, zc), fm, inward=True, hole_below=20.0)
        if os.environ.get('CORE_DESIGN', 'B') == 'B':
            # the ONLY emitter (the coordinator, 02:24): the Ø26 LED disc at its face, 200 lm on the one scale (1.306 W),
            # facing up, visible to every ray type; no emission on the opal
            ld = bpy.data.lights.new(f'led-{tint}', 'AREA'); ld.shape = 'DISK'; ld.size = 0.026
            # (2026-11-10, the enclosing sensor: a lamp colour has its LARGEST channel 1, so 2700 K carries luminance 0.52
            # and the lamp gave 52 % of its lumens; the energy now divided by the colour's luminance)
            ld.energy = float(os.environ.get('CORE_LM', CORE_LM)) * WLM / lum(bb) * (0.0 if os.environ.get('LIGHTS_OFF') else 1.0)
            ld.color = bb = blackbody(int(os.environ.get('LED_K', 0)) or LED_CCT.get(tint, 2700))   # its tint's LED colour
            ld.energy = float(os.environ.get('CORE_LM', CORE_LM)) * WLM / lum(bb) * (0.0 if os.environ.get('LIGHTS_OFF') else 1.0)
            lo = bpy.data.objects.new(f'led-{tint}', ld); bpy.context.scene.collection.objects.link(lo)
            lo.location = (x, y, z0 + 0.0147)          # area lamps face -Z: turn it over to face up
            lo.rotation_euler = (math.pi, 0.0, 0.0)
            lo.visible_camera = lo.visible_glossy = lo.visible_diffuse = lo.visible_transmission = True   # (Blender 5 makes a new lamp camera-hidden)
        else:
            # the LED's own face under the window (the CAD's Ø26), as in lamp_pictures: seen through the port where the
            # line of sight allows; it lights nothing itself (the frost face is the light, ruling 3's exception)
            bm = bmesh.new(); bmesh.ops.create_circle(bm, cap_ends=True, segments=48, radius=0.013)
            led = bpy.data.meshes.new(f'led-{tint}'); bm.to_mesh(led); bm.free()
            lo = bpy.data.objects.new(f'led-{tint}', led); bpy.context.scene.collection.objects.link(lo)
            lo.location = (x, y, z0 + 0.0147)
            em = bpy.data.materials.new(f'led-em-{tint}'); em.use_nodes = True
            b = em.node_tree.nodes['Principled BSDF']; b.inputs['Emission Color'].default_value = (*bb, 1)
            b.inputs['Emission Strength'].default_value = 8.0
            led.materials.append(em); lo.visible_diffuse = False
        if rot:
            for o in objs:   # turn the dock's cable away from the camera, about the lamp's axis (the parts' origin)
                o.rotation_euler[2] = math.radians(rot)

    # --- the set: a pale paper sweep (floor, cove, back) and real studio lights out of frame, unlinked ---------------
    paper = SC.principled('paper', os.environ.get('PAPER', '#EDE8E1'), 0.9)   # PAPER: a test backdrop (2026-11-11)
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
    SC.world(color=os.environ.get('WORLD', '#C8C4BE'), strength=0.02 * K)
    # round 2 (the gate): the studio at 3000 K, and the camera's white point at 3000 K; the lamps stay at 2700 K (spec)
    # round 3 (the gate's polish): a larger, higher key, so the two round highlights (key and fill) read as one soft one:
    # 4.0 m across (was 1.2; at 2 and 3 m the two reflections, the outer face's and the inner wall's, stay apart), higher and more frontal, its power grown with the square of its distance to
    # hold the light at the lamps
    kp = tuple(eval(os.environ['KEY_POS'])) if os.environ.get('KEY_POS') else (-1.0, -2.1, 2.6); kd0 = (Vector((-1.4, -1.6, 1.9)) - Vector((0, 0.1, 0.5))).length
    kd = (Vector(kp) - Vector((0, 0.1, 0.5))).length
    # (2026-11-09, the cast check: at 4 m the key's back stood in the orb row's frame, 24 %; 3 m clears it)
    ks = float(os.environ.get('KEY_SIZE', '3.0' if frame.startswith('lamps-orbs') else '4.0'))
    # KEY_STRIP 'w,h' (2026-11-11): the key as a rectangular strip softbox of w x h m at the same power per area as the
    # round key, for one long highlight along a shell (the Ember off and cap details)
    kst = os.environ.get('KEY_STRIP')
    if kst:
        kw_, kh_ = (float(v) for v in kst.split(','))
        key = SC.area('key', kp, (0, 0, 0), (kw_, kh_), 60.0 * K * (kd / kd0) ** 2 * (kw_ * kh_) / (3.14159 * ks * ks / 4), '#FFF4E8'); key.data.shape = 'RECTANGLE'
    else:
        key = SC.area('key', kp, (0, 0, 0), (ks, ks), 60.0 * K * (kd / kd0) ** 2, '#FFF4E8'); key.data.shape = 'ELLIPSE'
    key.data.color = blackbody(int(os.environ.get('STUDIO_K', '3000')))
    # KEY_AIM (2026-11-11, the coordinator: Ember off, one large overhead softbox, so the shell carries one long soft
    # highlight, not two ovals): where the key points; default the lamps' middle as before
    key.rotation_euler = (Vector(tuple(eval(os.environ.get('KEY_AIM', '(0, 0.1, 0.5)')))) - key.location).to_track_quat('-Z', 'Y').to_euler()
    fill = SC.area('fill', (1.8, -1.2, 1.2), (0, 0, 0), (1.6, 1.6), 20.0 * K, '#EEF2F8'); fill.data.shape = 'ELLIPSE'
    fill.data.color = blackbody(int(os.environ.get('STUDIO_K', '3000')))
    fill.rotation_euler = (Vector((0, 0.1, 0.4)) - fill.location).to_track_quat('-Z', 'Y').to_euler()
    # round 3 (the gate: 88 % of the dock's pixels at 3 or less): a kicker, low behind and to the right, out of frame
    # (the audit holds it there), that draws the dock's and the cap's edges; real, unlinked, its own reflection honest
    # (the heroes only: in the wide rows it grazed the sweep's cove, a bright streak, and a narrow beam raked the floor)
    kick = None if frame.startswith(('lamps', 'cluster')) else SC.area('kicker', (0.9, 0.9, 0.35 if kind0 == 'orb' else 0.9), (0, 0, 0), (0.3, 0.6), 6.0 * K, '#FFF4E8')
    if kick:
        kick.data.color = blackbody(int(os.environ.get('STUDIO_K', '3000')))
        kick.rotation_euler = (Vector((0, 0, 0.05 if kind0 == 'orb' else 0.62)) - kick.location).to_track_quat('-Z', 'Y').to_euler()

    for nm_ in os.environ.get('LIGHTS_OFF', '').split(','):      # a probe: a studio light switched off
        if nm_ and nm_ in bpy.data.objects:
            bpy.data.objects.remove(bpy.data.objects[nm_], do_unlink=True)

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
    elif frame.startswith('baseopts'):
        # core-base-options (2026-11-11): three Cores side by side, Ember, bases A, B, C; 2400 x 1000
        W, H = 2400, 1000
        dx_ = float(os.environ.get('BASE_DX', '0.24'))          # the spacing (the daylight grid: 0.18, closer)
        for b_, x_ in (('A', -dx_), ('B', 0.0), ('C', dx_)):
            core(tint or 'red', x_, 0.0, base=b_)
        cam = tuple(eval(os.environ['BASECAM'])) if os.environ.get('BASECAM') else ((0.0, -1.10, 0.36), (0.0, 0.0, 0.085), 58.0)
    elif frame == 'cluster':
        # hemisphere-cluster (the owner, 2026-11-11: "different colors at variable heights, all clustered together"): all
        # eight hung close in two staggered rows (plan centres 0.24 m or more apart, the shades Ø200: no cord passes through a shade),
        # no two at the same height, neighbours set off by colour; seen a little from below and to one side; 2000 x 2000
        # (2026-11-11 21:20: neighbours across the rows 0.24 m or more apart in height so no shade stacks on another;
        # no kicker here: from this camera it sat in frame, a bright wedge at the right edge)
        W, H = 2000, 2000
        for t, (x_, y_, z_) in zip(('red', 'blue', 'amber', 'violet', 'green', 'black', 'orange', 'ice'),
                                   ((-0.42, 0.12, 0.84), (-0.18, 0.12, 0.72), (0.06, 0.12, 0.80), (0.30, 0.12, 0.88),
                                    (-0.30, -0.12, 0.48), (-0.06, -0.12, 0.42), (0.18, -0.12, 0.54), (0.42, -0.12, 0.62))):
            hemisphere(t, x_, z_, y=y_)
        cam = tuple(eval(os.environ['DOMECAM'])) if os.environ.get('DOMECAM') else ((0.30, -1.50, 0.36), (0.0, 0.0, 0.67), 46.0)
    elif frame.startswith('trio-'):
        # trio-<k1>-<k2>-<k3> (the owner, 2026-11-11: "I like having to pair multiple"): three Hemispheres hung close
        # over a table at slightly different heights, seen a little from below and to one side; 2000 x 1600
        W, H = 2000, 1600
        ks = frame.split('-')[1:4]
        for t, (x_, z_, y_) in zip(ks, ((-0.235, 0.56, 0.03), (0.0, 0.50, -0.02), (0.235, 0.535, 0.02))):
            hemisphere(t, x_, z_, y=y_)
        cam = tuple(eval(os.environ['DOMECAM'])) if os.environ.get('DOMECAM') else ((0.30, -0.82, 0.28), (0.02, 0.0, 0.49), 38.0)
    elif frame.startswith('lamps-orbs'):
        # round 2 (the gate): the camera 15 deg up, so each lamp's glow on the paper is its own; '-7' leaves Smoke out
        W, H = 2400, 800
        row = ROW[:7] if frame.endswith('-7') else ROW
        for i, t in enumerate(row):
            core(t, (i - (len(row) - 1) / 2) * 0.22, 0.0)
        # round 3 (the gate's base band): the camera at 22 deg, so the docks read from above
        cam = ((0.0, -4.4, 0.10 + 4.4 * math.tan(math.radians(22))), (0.0, 0.0, 0.10), 85.0)
    elif kind == 'dome':
        W, H = 1600, 2000
        hemisphere(tint, 0.0, 0.50)                    # the rim 500 above the paper: the dome and its pool in one frame
        # round 3 (the gate: the dome 40-50 % of the card, the pool's front edge inside): higher and closer, looking
        # down past the dome to the pool's near half-maximum (r 0.38 at the rim's 0.50; launch/HIDDENCAST.md's pool note)
        cam = tuple(eval(os.environ['DOMECAM'])) if os.environ.get('DOMECAM') else ((0.06, -0.90, 1.20), (0.0, -0.15, 0.385), 58.0)
    elif kind == 'orb':
        W, H = 1600, 2000
        core(tint, 0.0, 0.0)
        # ORBCAM: e.g. October's framing (p4-lamp-orb-*, its orb 40 mm up): ((-0.16,-0.62,0.128),(0,0,0.108),75)
        cam = tuple(eval(os.environ['ORBCAM'])) if os.environ.get('ORBCAM') else ((0.10, -0.95, 0.22), (0.0, 0.0, 0.11), 70.0)
    else:
        raise SystemExit('unknown frame ' + frame)
    SC.render_settings(W, H, samples, scale, exposure=float(os.environ.get('EV', EVD)), look=os.environ.get('LOOK', 'AgX - Punchy'))   # round 2: AgX Punchy (the gate)
    sc = bpy.context.scene
    sc.cycles.caustics_refractive = True; sc.cycles.sample_clamp_indirect = float(os.environ.get('CLAMP', '0' if kind0 in ('dome', 'orb') else '20')) * 2.0 ** (-sc.view_settings.exposure)   # a radiance, in display terms   # round 3: the clamp cut the bore reflector's share (78 % out unclamped, 57 % clamped); sc.cycles.blur_glossy = 1.0
    # round 3 (the coordinator's photometry check): the bore's reflector sends light to the floor by reflection, a
    # reflective caustic; render_settings turns those off, which threw the reflector's share away
    sc.cycles.caustics_reflective = os.environ.get('REFL_CAUSTICS', '1') == '1'
    # 2026-11-10 (the coordinator: at least 32 of each): render_settings gives 4 diffuse and 8 glossy bounces, short for
    # the opal cavities (the enclosing sensor: Hemisphere 218 lm out at those, 229 at 64)
    sc.cycles.max_bounces = 64; sc.cycles.diffuse_bounces = sc.cycles.glossy_bounces = sc.cycles.transmission_bounces = 32
    vs = sc.view_settings; vs.use_white_balance = True; vs.white_balance_temperature = float(os.environ.get('WB', '3000'))
    vs.white_balance_tint = 0.0
    SC.camera(cam[0], cam[1], lens=cam[2], fstop=float(os.environ.get('FSTOP', '8.0')),   # FSTOP, FOCUS: a detail's shallow focus
              focus=tuple(eval(os.environ['FOCUS'])) if os.environ.get('FOCUS') else None)
    for nm_ in os.environ.get('STUDIO_OFF', '').split(','):   # e.g. the view from straight below: the key, hidden from
        if nm_ and nm_ in bpy.data.objects:                   # the camera, stands in its frame (hiddencast), so it goes
            bpy.data.objects.remove(bpy.data.objects[nm_], do_unlink=True)
    if os.environ.get('FLUX'):
        # the flux check: the sweep and studio gone, a 3 x 3 m translucent white sensor 30 mm under the rim, seen from
        # below by an orthographic camera in linear light; flux (W) = mean radiance x pi x area
        for o in list(sc.objects):
            if o.name in ('sweep', 'key', 'fill', 'kicker'):
                bpy.data.objects.remove(o, do_unlink=True)
        sc.world.node_tree.nodes['Background'].inputs['Strength'].default_value = 0.0
        sm = bpy.data.materials.new('sensor'); sm.use_nodes = True; nt = sm.node_tree; nt.nodes.clear()
        o_ = nt.nodes.new('ShaderNodeOutputMaterial'); tr = nt.nodes.new('ShaderNodeBsdfTranslucent')
        tr.inputs['Color'].default_value = (1, 1, 1, 1); nt.links.new(tr.outputs[0], o_.inputs['Surface'])
        zs = float(os.environ.get('FLUX_Z', '0.47'))
        SC.plane('sensor', (3.0, 3.0), (0, 0, zs), (0, 0, 0), sm)
        cd = bpy.data.cameras.new('fluxcam'); cd.type = 'ORTHO'; cd.ortho_scale = 3.0
        co = bpy.data.objects.new('fluxcam', cd); sc.collection.objects.link(co); co.location = (0, 0, zs - 1.0)
        co.rotation_euler = (math.pi, 0, 0); sc.camera = co
        sc.render.resolution_x = sc.render.resolution_y = 300; sc.render.resolution_percentage = 100
        sc.view_settings.view_transform = 'Standard'; sc.view_settings.look = 'None'; sc.view_settings.exposure = 0
        sc.view_settings.use_white_balance = False; sc.cycles.use_denoising = False
        sc.render.image_settings.file_format = 'OPEN_EXR'
        sc.render.filepath = os.environ.get('LAMP_OUT', '/tmp/flux.exr')
        bpy.ops.render.render(write_still=True)
        img = bpy.data.images.load(sc.render.filepath); px = img.pixels[:]
        n = len(px) // 4
        Y = sum(0.2126 * px[4 * i] + 0.7152 * px[4 * i + 1] + 0.0722 * px[4 * i + 2] for i in range(n)) / n
        print('FLUX', frame, 'mean Y', round(Y, 5), 'flux W', round(Y * math.pi * 9.0, 4), 'emitted COB W', round(430 * WLM, 3))
        return
    if os.environ.get('AUDIT'):
        hidden = [o for o in sc.objects if o.type == 'MESH' and not o.visible_camera]
        print('AUDIT', frame, 'hidden', [o.name for o in hidden],
              'no-shadow', [o.name for o in sc.objects if o.type == 'MESH' and not o.visible_shadow],
              'lights', [(o.name, o.data.type, round(o.data.energy, 3)) for o in sc.objects if o.type == 'LIGHT'])
        # the coordinator's 19:13 rule: no light, card or panel in frame hidden from the camera (hiddencast_bpy)
        sys.path.insert(0, os.path.join(HERE, 'launch'))
        from hiddencast_bpy import hiddencast, report
        print(report(frame, hiddencast(sc)))
        if os.environ.get('MASK'):                    # the cast check with Blender's own camera, rendered
            from hiddencast_bpy import mask_check
            print('CASTCHECK', frame, {k: round(v * 100, 2) for k, v in mask_check(sc, os.environ['MASK']).items()})
        return
    os.makedirs(OUT, exist_ok=True)
    if os.environ.get('LUXPROBE'):
        # the table's lux under the lamp: the studio and the world off, an orthographic camera 0.25 above the paper
        # looking straight down at a 1 m square of it, linear light; E = pi L / rho (rho the paper's albedo), lux = E / WLM
        for o in list(sc.objects):
            if o.name in ('key', 'fill', 'kicker'):
                bpy.data.objects.remove(o, do_unlink=True)
        if sc.world:
            for n_ in sc.world.node_tree.nodes:
                if n_.type == 'BACKGROUND':
                    n_.inputs['Strength'].default_value = 0.0
        cm_ = sc.camera; cm_.location = (0.0, 0.0, 0.25); cm_.rotation_euler = (0.0, 0.0, 0.0)
        cm_.data.type = 'ORTHO'; cm_.data.ortho_scale = 1.0; cm_.data.dof.use_dof = False
        sc.render.resolution_x = sc.render.resolution_y = 200; sc.render.resolution_percentage = 100
        sc.view_settings.view_transform = 'Standard'; sc.view_settings.look = 'None'; sc.view_settings.exposure = 0.0
        sc.view_settings.use_white_balance = False
        sc.render.image_settings.file_format = 'OPEN_EXR'; sc.render.filepath = os.environ['LUXPROBE']
        bpy.ops.render.render(write_still=True)
        img = bpy.data.images.load(os.environ['LUXPROBE'], check_existing=False); px = img.pixels[:]
        rho = sum(paper.node_tree.nodes['Principled BSDF'].inputs['Base Color'].default_value[i] * w for i, w in enumerate((0.2126, 0.7152, 0.0722)))
        def lux(r0, r1):
            v = []
            for j in range(200):
                for i in range(200):
                    rr = math.hypot((i + 0.5) / 200 - 0.5, (j + 0.5) / 200 - 0.5)
                    if r0 <= rr < r1:
                        k = 4 * (j * 200 + i); v.append(0.2126 * px[k] + 0.7152 * px[k + 1] + 0.0722 * px[k + 2])
            return sum(v) / len(v) * math.pi / rho / WLM
        print('LUX', frame, 'centre r<0.05', round(lux(0, 0.05)), 'r 0.15-0.2', round(lux(0.15, 0.2)), 'r 0.3-0.35', round(lux(0.3, 0.35)), 'albedo', round(rho, 3))
        return
    if kind0 == 'dome' and os.environ.get('HEMI_ENGINE', 'ring') == 'ring':
        sc.cycles.use_denoising = os.environ.get('DENOISE') == '1'   # (option 3: no denoiser on the lamp; DENOISE=1 for the row and Smoke, the coordinator 23:50)
        # path guiding (Cycles' OpenPGL, CPU): the light that reaches the paper through the shade's clear layers is a
        # caustic of 24 small LEDs; guiding samples it better (no clamp, no denoiser: an unbiased estimator still)
        sc.cycles.use_guiding = os.environ.get('GUIDING', '1') == '1'; sc.cycles.use_surface_guiding = True
    sc.render.filepath = os.environ.get('LAMP_OUT') or os.path.join(OUT, frame + '.png')
    lg = os.environ.get('LIGHTGROUPS')           # a path: the LEDs in their own light group, the rest in 'studio'
    if lg:
        vl = sc.view_layers[0]
        print('LG view layer', vl.name, 'context', bpy.context.view_layer.name, 'scene', sc.name, [s_.name for s_ in bpy.data.scenes])
        for nm_ in ('lamp', 'studio'):
            if nm_ not in vl.lightgroups:
                vl.lightgroups.add(name=nm_)
        for o in sc.objects:
            if o.type == 'LIGHT':
                o.lightgroup = 'lamp' if o.name.startswith('led-') else 'studio'
            elif o.type == 'MESH':
                o.lightgroup = 'studio'           # (no emissive meshes; any would be named and counted with the studio)
        if sc.world:
            sc.world.lightgroup = 'studio'
    if lg:
        # the passes as a 32-bit uncompressed multilayer EXR written by the render itself (scratch, not the repo);
        # launch/lightcolor.py recolours the lamp's pass. The PNG is then saved from the result
        out_png = sc.render.filepath; fmt = sc.render.image_settings
        fmt.media_type = 'MULTI_LAYER_IMAGE'; fmt.file_format = 'OPEN_EXR_MULTILAYER'; fmt.color_depth = '32'; fmt.exr_codec = 'NONE'
        sc.render.filepath = lg
        bpy.ops.render.render(write_still=True)
        fmt.media_type = 'IMAGE'; fmt.file_format = 'PNG'; fmt.color_depth = '8'; fmt.color_mode = 'RGB'
        sc.render.filepath = out_png
        bpy.data.images['Render Result'].save_render(out_png, scene=sc)
    else:
        bpy.ops.render.render(write_still=True)
    # the scene-linear EXR beside the PNG, so exposure and look can change without a re-render (the coordinator)
    if os.environ.get('EXR', '1') == '1':
        img = bpy.data.images['Render Result']; fmt = sc.render.image_settings
        fmt.media_type = 'IMAGE'; fmt.file_format = 'OPEN_EXR'; fmt.color_depth = '16'; fmt.exr_codec = 'DWAA'
        img.save_render(os.path.splitext(sc.render.filepath)[0] + '.exr', scene=sc)


if __name__ == '__main__':
    a = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else sys.argv[1:]
    build(a[0], int(a[a.index('--samples') + 1]) if '--samples' in a else 256,
          float(a[a.index('--scale') + 1]) if '--scale' in a else 1.0)
