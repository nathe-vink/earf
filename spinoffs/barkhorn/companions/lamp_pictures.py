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
TINT = {'ice': 'Ice', 'ember': 'Ember', 'dust': 'Dust', 'acid': 'Acid', 'poison': 'Poison', 'haze': 'Haze', 'fog': 'Fog',
        'smoke': 'Smoke dark'}


def build(frame, samples, scale):
    import bpy, bmesh
    sys.path.insert(0, os.path.join(HERE, 'strata'))
    import scene as SC
    prod, tint, mode = frame.split('-')
    tname = TINT[tint]
    night = mode == 'night'
    bpy.ops.wm.read_factory_settings(use_empty=True)
    MM = SC.MM
    tz = 0.62                                                           # the table's top

    def sphere(nm, r, z, mat, inward=False, cut=None, loc=(0, 0)):
        bm = bmesh.new()
        bmesh.ops.create_uvsphere(bm, u_segments=256, v_segments=128, radius=r * MM)
        if cut is not None:
            bmesh.ops.delete(bm, geom=[v for v in bm.verts if v.co.z < cut * MM - 1e-9], context='VERTS')
        if inward:
            bmesh.ops.reverse_faces(bm, faces=bm.faces)
        for f in bm.faces:
            f.smooth = True
        me = bpy.data.meshes.new(nm); bm.to_mesh(me); bm.free()
        ob = bpy.data.objects.new(nm, me); bpy.context.scene.collection.objects.link(ob)
        ob.location = (loc[0], loc[1], z); me.materials.append(mat)
        return ob

    def acrylic(nm, rough, which=None):
        return SC.acrylic_material(nm, [(-1e4, 1e4, which or tname)], rough, 'polished', scratch=0.25, bond=False)

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
        sphere('ball', 80.0, zc, acrylic('ball', 0.0))
        sphere('ball-frost', 71.0, zc, acrylic('ball-frost', 0.6), inward=True)
        if night:
            sphere('glow', 70.4, zc, SC.emitter('glow', '#FFC890', 2.6, mirror_only=True))
        cam = ((0.12, -1.02, tz + 0.235), (0.0, 0.0, tz + 0.098), 85.0)
    else:
        rim = tz + 0.70                                                 # the rim 700 above the table
        sphere('tint', 100.0, rim, acrylic('tint', 0.0), cut=0.0)
        sphere('tint-in', 97.0, rim, acrylic('tint-in', 0.0), inward=True, cut=0.0)
        sphere('clear', 96.0, rim, acrylic('clear', 0.0, 'Clear'), cut=4.0)
        sphere('clear-in', 90.0, rim, acrylic('clear-in', 0.0, 'Clear'), inward=True, cut=4.0)
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
        sphere('opal', 89.0, rim, opal, cut=0.0)
        sphere('opal-in', 86.0, rim, opal, inward=True, cut=0.0)
        part('out-dome-pendant', 'rim', acrylic('rim', 0.0), rim)
        for nm in ('collar', 'clamp', 'crown', 'gland', 'hub'):
            part('out-dome-pendant', nm, an, rim)
        part('out-dome-pendant', 'reflector', steel, rim)
        part('out-dome-pendant', 'cord', SC.principled('braid', '#121212', 0.75, bump=(1200.0, 0.5)), rim)
        if night:
            sphere('glow', 85.4, rim, SC.emitter('glow', '#FFC890', 3.5, mirror_only=True), cut=2.0)
        cam = ((0.0, -1.28, rim + 0.0), (0.0, 0.0, rim + 0.045), 85.0)
    if night:
        SC.world(strength=0.03, color='#1B2230')
        SC.area('moon', (-1.3, -0.4, 1.6), (0, -70, 0), (1.2, 1.6), 9.0, '#9FB2D6')
        SC.area('fill', (0.6, -1.4, 1.5), (60, 0, 25), (1.0, 1.0), 4.0, '#8FA0BE')
        exposure = 0.0
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
    bpy.context.scene.render.filepath = os.path.join(OUT, frame + '.png')
    bpy.ops.render.render(write_still=True)


if __name__ == '__main__':
    a = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else sys.argv[1:]
    build(a[0], int(a[a.index('--samples') + 1]) if '--samples' in a else 256,
          float(a[a.index('--scale') + 1]) if '--scale' in a else 1.0)
