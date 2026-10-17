"""Round 28: the mark as the real thing, path-traced as the speakers are, and its one-colour versions traced from it.

The owner, 2026-10-17, of the spins: "It still looks odd when ever the meridian "seams" of the globe are viewed straight
on. I want the semi transparent pieces so it looks like acrylic like the speakers. Maybe it's best to actually render the
object like we did the speakers, so it looks real, and then create the monochromatic fill and stroke versions based on
the real thing."

So the globe is built as an object: earth.py's six discs (its three parallels and three meridians, its lean and its
tip, each disc a slab THICK of the radius thick) cut from the Cloud cabinets' own 20 mm tinted cast acrylic, which
makes the globe 800 mm across, and cemented clear where they cross (or, with --slots, slotted through one another, the
meridian facing us whole and each other disc slotted round those before it, GAP clear). It is rendered in Cycles with
the engine's acrylic (studio/engine/materials.py's clear_resin, polished as the cabinets are), so a face is a clear
tint, crossing faces build their tints, and an edge, seen along the whole sheet, its disc's colour at its deepest. The
tints are the cabinets' through glow(), so each passes its own colour freely and an edge glows instead of going black.
The camera is earth.py's own: square on and orthographic, so a render lies exactly over the flat drawings made from the
same discs (slabs, line_body, fill_body).

The ground is the brand's paper (or night) as a backdrop behind the globe, rendered as exactly that colour, so the
render sits on the page like the flat marks do; a dim studio (Poly Haven's, CC0) and a soft key above left show only
in the acrylic's reflections.

    python3 spinoffs/barkhorn/globe_real.py --still OUT.png [--ground paper|night] [--px 1024] [--samples 128] [--spin DEG]
    python3 spinoffs/barkhorn/globe_real.py --spin-frames DIR [--frames 120] [--px 720] [--samples 24] [--first N --last M]
    python3 spinoffs/barkhorn/globe_real.py --encode DIR OUT          the frames as OUT.mp4 and OUT.webm
    python3 spinoffs/barkhorn/globe_real.py --flat DIR [--flat-spin DIR]   the fill and the line, stills and spins

The still is framed as the flat marks are (their SVGs' view box); the spin's frames as mark.py frames its spins (a quarter
of the globe's width clear round it), half a turn in `frames` frames, so they loop. Times on 4 CPUs: a 1024 px still at
128 samples about 12 minutes, a 720 px spin frame at 24 samples about 35 s.
"""
import argparse, math, os, sys, time

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(ROOT, 'studio', 'engine'))
import earth as E                                        # noqa: E402

R = 0.4                                                  # the globe's radius in metres: discs of the cabinets' 20 mm sheet
T = E.THICK * R                                          # each disc's thickness, the mark's slab (0.05 of the radius)
GAP = 0.0005                                             # the slots' clearance each side
SEG = 360                                                # a disc's segments round
NAMES = ['flare', 'ice', 'acid', 'haze', 'poison', 'dust']           # earth.RING's order: N, equator, S, meridians 30, 90, 150
ACRYLIC = {'flare': '#F2A29C', 'dust': '#F2B184', 'acid': '#F2D06B', 'poison': '#B2C9A2', 'ice': '#B5D9EE',
           'haze': '#BEADD8'}                            # the Cloud cabinets' tints after `DEPTH` (product.py's Clouds)
DEPTH, POLISH = 0.025, 0.05                              # their depth (m) and roughness, polished cast acrylic
MARK_DEPTH = 0.02                                        # the globe's: a little deeper, so a face holds its colour on paper
ORDER = [4, 3, 5, 1, 0, 2]                               # which disc is whole: the meridian facing us, then the others in turn
GROUNDS = {'paper': E.PAPER, 'night': E.NIGHT}


def local_discs():
    """Each disc in the globe's own frame (its axis z; longitude 0 toward -y, the camera, and 90 along +x), in
    earth.rings' order: (centre, normal, radius), of the radius."""
    a, e1, e2 = np.array([0.0, 0.0, 1.0]), np.array([0.0, -1.0, 0.0]), np.array([1.0, 0.0, 0.0])
    out = []
    for phi in (E.LAT, 0.0, -E.LAT):
        p = math.radians(phi)
        out.append((math.sin(p) * a, a, math.cos(p)))
    for lam in E.MERIDIANS:
        l = math.radians(lam)
        u = math.cos(l) * e1 + math.sin(l) * e2
        out.append((np.zeros(3), np.cross(u, a), 1.0))
    return out


def orientation():
    """The globe's frame in the world as a 3 x 3 matrix: earth.basis (the lean and the tip) with its screen (x right, y
    up, z toward us) set in a world whose camera looks along +y from -y, z up."""
    a, e1, e2 = E.basis()
    w = lambda v: np.array([v[0], -v[2], v[1]])
    return np.column_stack([w(e2), -w(e1), w(a)])


def _hex_lin(h):
    h = h.lstrip('#')
    c = np.array([int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)])
    return np.where(c <= 0.04045, c / 12.92, ((c + 0.055) / 1.055) ** 2.4)


def slabs(spin=0.0, thick=E.THICK, n=720):
    """Each disc of the real globe as earth.py's camera sees it (the unit globe, y up), in earth.rings' order: its near
    face and its far face (ovals), its outline (the slab's silhouette, the hull of the two), its edge (what of the outline
    the near face leaves, where a line of sight enters the disc through its rim and runs along it inside, so the acrylic
    shows its deepest there: a crescent on one side of an oblique disc, from nothing to its whole thickness; edge on, the
    whole band; face on, nothing) and its middle ring in 3D (x, y and depth toward us)."""
    from shapely.geometry import MultiPoint, Polygon
    s_ = math.radians(spin)
    W = orientation() @ np.array([[math.cos(s_), -math.sin(s_), 0], [math.sin(s_), math.cos(s_), 0], [0, 0, 1]])
    a = np.linspace(0, 2 * math.pi, n, endpoint=False)
    scr = lambda P: (W @ P.T).T[:, [0, 2, 1]] * [1, 1, -1]      # x right, y up, depth toward us (world -y)
    out = []
    for c, nrm, r in local_discs():
        nrm = nrm / np.linalg.norm(nrm)
        u = np.cross(nrm, [1.0, 0.0, 0.0] if abs(nrm[0]) < 0.9 else [0.0, 1.0, 0.0]); u /= np.linalg.norm(u)
        v = np.cross(nrm, u)
        toward = 1.0 if -(W @ nrm)[1] >= 0 else -1.0     # the face nearer the camera
        ring = r * (np.outer(np.cos(a), u) + np.outer(np.sin(a), v))
        near, far = scr(c + toward * thick / 2 * nrm + ring)[:, :2], scr(c - toward * thick / 2 * nrm + ring)[:, :2]
        F = Polygon(near).buffer(0)
        S = MultiPoint(np.vstack([near, far])).convex_hull
        out.append(dict(near=F, far=Polygon(far).buffer(0), outline=S, edge=S.difference(F), ring=scr(c + ring)))
    return out


def line_body(colour, spin=0.0, w=0.024, far=E.W_DEPTH):
    """The line version traced from the real thing: every disc seen through the others, as the acrylic shows it. Its
    middle ring a line `w` of the radius wide on the near side of the globe and `far` of that behind it, seen through
    the discs in front (earth._runs splits each at the outline); and its edge, filled where it shows, so the line swells
    where the disc's thickness faces you, and a disc edge on is one band as wide as the sheet is thick."""
    from shapely.geometry import LineString
    from shapely.ops import unary_union
    parts = []
    for q in slabs(spin):
        for front, k in ((True, 1.0), (False, far)):
            for run in E._runs(q['ring'], front):
                if len(run) > 1:
                    parts.append(LineString(run[:, :2]).buffer(w * k / 2, cap_style=1, join_style=1))
        parts.append(q['edge'])
    return f'<path d="{E._poly_d(unary_union(parts))}" fill="{colour}"/>'


def fill_body(colour, spin=0.0, sheet=0.2):
    """The fill traced from the real thing, in one colour: each disc's face a sheet of `sheet` of the colour (so where
    k discs cross, the colour builds as k sheets of tinted acrylic do), and its edge, seen along the disc, the colour
    whole."""
    ss = slabs(spin)
    faces = ''.join(f'<path d="{E._poly_d(q["near"])}" fill="{colour}" fill-opacity="{sheet}"/>' for q in ss)
    edges = ''.join(f'<path d="{E._poly_d(q["edge"])}" fill="{colour}"/>' for q in ss)
    return faces + edges


def flat_svg(style, colour, bg, spin=0.0, e=1 + E.W_LINE / 2, size=None):
    """A flat version (`style` 'line' or 'fill') as a whole SVG on `bg` (None: transparent), the unit globe framed
    2e across as the marks are."""
    body = line_body(colour, spin) if style == 'line' else fill_body(colour, spin)
    wh = f' width="{size}" height="{size}"' if size else ''
    ground = f'<rect x="{-e:.4f}" y="{-e:.4f}" width="{2 * e:.4f}" height="{2 * e:.4f}" fill="{bg}"/>' if bg else ''
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{-e:.4f} {-e:.4f} {2 * e:.4f} {2 * e:.4f}"{wh}>'
            f'{ground}{body}</svg>')


PASS = {'acid': 'RG'}                                     # glow()'s channels passed whole, beside the least absorbed


def glow(hx, keep=0.97, passed=''):
    """A tint that passes its own colour almost freely, as a dyed acrylic does: each channel's absorbance less `keep` of
    the least absorbed channel's, so a face keeps its tint and an edge, seen along the whole disc, glows its colour
    instead of going black. Over a long path only the freest channel is left, so an amber's edge goes red: `passed`
    channels ('RG' for Acid) pass as freely, so its edge stays yellow."""
    c = np.clip(_hex_lin(hx), 1e-4, 1.0)
    a = -np.log(c)
    a = a - keep * a.min()
    for ch in passed:
        a['RGB'.index(ch)] = a.min()
    v = np.exp(-a)
    s = np.where(v <= 0.0031308, 12.92 * v, 1.055 * v ** (1 / 2.4) - 0.055)
    return '#%02X%02X%02X' % tuple(int(round(255 * min(1.0, x))) for x in s)


def build(bpy, tints=None, fuse=True, depth=MARK_DEPTH):
    """The six discs, cemented clear (one solid where they cross; `fuse` False: slotted), parented to one empty at the
    origin whose matrix turns the globe. `tints`: hex per disc, glow()'s of the cabinets' by default."""
    import bmesh
    from mathutils import Matrix, Vector
    import materials as Mt
    tints = tints or {k: glow(v, passed=PASS.get(k, '')) for k, v in ACRYLIC.items()}
    root = bpy.data.objects.new('globe', None)
    bpy.context.scene.collection.objects.link(root)

    def slab(name, c, n, r, grow=0.0, thick=T):
        me = bpy.data.meshes.new(name)
        bm = bmesh.new()
        bmesh.ops.create_cone(bm, cap_ends=True, cap_tris=False, segments=SEG, radius1=r * R + grow, radius2=r * R + grow,
                              depth=thick)
        m = Matrix.Translation(Vector(c * R)) @ Vector((0, 0, 1)).rotation_difference(Vector(n)).to_matrix().to_4x4()
        bm.transform(m)
        bm.to_mesh(me); bm.free()
        ob = bpy.data.objects.new(name, me)
        bpy.context.scene.collection.objects.link(ob)
        return ob

    discs = local_discs()
    mats = {i: Mt.make(bpy, f'acrylic-{NAMES[i]}', 'clear_resin',
                       {'color': '#FFFFFF', 'deep': tints[NAMES[i]], 'radius': depth, 'roughness': POLISH}) for i in ORDER}
    if fuse:                                             # one solid, each face keeping its own disc's acrylic
        parts = {i: slab(f'disc-{NAMES[i]}', *discs[i]) for i in ORDER}
        for i, ob in parts.items():
            ob.data.materials.append(mats[i])
        base = parts[ORDER[0]]
        for i in ORDER[1:]:
            mod = base.modifiers.new(f'fuse-{NAMES[i]}', 'BOOLEAN')
            mod.operation, mod.solver, mod.object, mod.material_mode = 'UNION', 'EXACT', parts[i], 'TRANSFER'
            parts[i].hide_render = True
        obs, cutters = [(None, base)], [parts[i] for i in ORDER[1:]]
    else:
        cutters = {i: slab(f'cut-{NAMES[i]}', *discs[i], grow=0.002, thick=T + 2 * GAP) for i in ORDER}
        for c in cutters.values():
            c.hide_render = True
        obs = []
        for k, i in enumerate(ORDER):
            ob = slab(f'disc-{NAMES[i]}', *discs[i])
            for j in ORDER[:k]:
                mod = ob.modifiers.new(f'slot-{NAMES[j]}', 'BOOLEAN')
                mod.operation, mod.solver, mod.object = 'DIFFERENCE', 'EXACT', cutters[j]
            obs.append((i, ob))
        cutters = list(cutters.values())
    dg = bpy.context.evaluated_depsgraph_get()
    for i, ob in obs:
        me = bpy.data.meshes.new_from_object(ob.evaluated_get(dg))
        ob.modifiers.clear()
        ob.data = me
        me.shade_smooth()
        me.set_sharp_from_angle(angle=math.radians(25))
        if i is not None:
            me.materials.clear(); me.materials.append(mats[i])
        ob.parent = root
    for c in cutters:
        bpy.data.objects.remove(c, do_unlink=True)
    return root


def stage(bpy, ground, px, e, samples, env='dim', adaptive=0.01):
    """The camera (earth.py's view, orthographic, the frame 2e radii across), the ground as a backdrop of exactly its
    colour, and the studio seen in the acrylic: a soft key above left, the room round it."""
    from mathutils import Vector
    import lights as Lt
    scene = bpy.context.scene
    cd = bpy.data.cameras.new('camera'); cam = bpy.data.objects.new('camera', cd)
    scene.collection.objects.link(cam); scene.camera = cam
    cd.type = 'ORTHO'; cd.ortho_scale = 2 * e * R; cd.clip_start = 0.01; cd.clip_end = 100
    cam.location = (0.0, -6.0, 0.0); cam.rotation_euler = (math.pi / 2, 0.0, 0.0)
    # the ground: a plane far behind, glowing its colour, so the camera and anything seen through the acrylic meet it
    me = bpy.data.meshes.new('ground'); s = 12.0
    me.from_pydata([(-s, 3.0, -s), (s, 3.0, -s), (s, 3.0, s), (-s, 3.0, s)], [], [(0, 1, 2, 3)])
    gob = bpy.data.objects.new('ground', me); scene.collection.objects.link(gob)
    m = bpy.data.materials.new('ground'); m.use_nodes = True; nt = m.node_tree; nt.nodes.clear()
    em = nt.nodes.new('ShaderNodeEmission'); out = nt.nodes.new('ShaderNodeOutputMaterial')
    em.inputs['Color'].default_value = (*_hex_lin(GROUNDS[ground]), 1.0); em.inputs['Strength'].default_value = 1.0
    nt.links.new(em.outputs['Emission'], out.inputs['Surface'])
    me.materials.append(m)
    # the room: a studio photographed (Poly Haven, CC0), seen only in reflections, a plain grey, or a dark room
    Lt.world(bpy, {'studio': {'kind': 'hdri', 'file': 'studio_small_03_1k', 'strength': 0.6},
                   'dim': {'kind': 'hdri', 'file': 'studio_small_03_1k', 'strength': 0.25},
                   'grey': {'kind': 'gradient', 'zenith': '#6E6C68', 'horizon': '#8A8884', 'ground': '#3A3835', 'strength': 1.0},
                   'dark': {'kind': 'gradient', 'zenith': '#2A2927', 'horizon': '#33322F', 'ground': '#1E1D1B', 'strength': 1.0}}[env])
    Lt.area(bpy, 'key', {'type': 'area', 'size_m': [3.2, 2.4], 'target': [0, 0, 0], 'irradiance': 2.0, 'color': '#FFF4E6',
                         'orbit': {'azimuth_deg': -40, 'elevation_deg': 40, 'distance_m': 6.0}}, Vector((0, 0, 0)))
    r = scene.render
    r.engine = 'CYCLES'; r.resolution_x = r.resolution_y = px; r.resolution_percentage = 100; r.film_transparent = False
    cy = scene.cycles
    cy.device = 'CPU'; cy.samples = samples; cy.use_adaptive_sampling = True; cy.adaptive_threshold = adaptive
    cy.use_denoising = True; cy.denoiser = 'OPENIMAGEDENOISE'; cy.denoising_input_passes = 'RGB_ALBEDO_NORMAL'
    # light trapped in a sheet runs along it by total internal reflection, each reflection a glossy bounce: cut short,
    # an edge seen along its disc goes black (the first proofs, at 8)
    cy.max_bounces = 96; cy.transmission_bounces = 96; cy.glossy_bounces = 96; cy.diffuse_bounces = 2
    cy.transparent_max_bounces = 32; cy.volume_bounces = 2
    cy.caustics_reflective = False; cy.caustics_refractive = False; cy.sample_clamp_indirect = 10.0; cy.blur_glossy = 0.5
    vs = scene.view_settings; vs.view_transform = 'Standard'; vs.look = 'None'; vs.exposure = 0.0; vs.gamma = 1.0
    r.image_settings.file_format = 'PNG'; r.image_settings.color_mode = 'RGB'; r.image_settings.color_depth = '8'
    r.use_persistent_data = True


def encode(frames, out):
    """A directory of spin frames (f0000.png ...) as a seamless loop, OUT.mp4 and OUT.webm, as mark.spin encodes."""
    import subprocess
    import mark as K
    src = ['ffmpeg', '-v', 'error', '-y', '-framerate', str(K.SPIN['fps']), '-i', os.path.join(frames, 'f%04d.png')]
    subprocess.run(src + ['-c:v', 'libx264', '-preset', 'slow', '-crf', '18', '-tune', 'animation', '-pix_fmt', 'yuv420p',
                          '-movflags', '+faststart', out + '.mp4'], check=True)
    subprocess.run(src + ['-c:v', 'libvpx-vp9', '-b:v', '0', '-crf', '30', '-row-mt', '1', '-pix_fmt', 'yuv420p',
                          '-fflags', '+bitexact', '-flags:v', '+bitexact', out + '.webm'], check=True)
    return [out + '.mp4', out + '.webm']


FLATS = [('line', E.INK, E.PAPER, 'black'), ('fill', E.INK, E.PAPER, 'black'), ('line', E.WHITE, E.NIGHT, 'white'),
         ('fill', E.WHITE, E.NIGHT, 'white')]


def flat_files(out, px=1024):
    """The flat versions as files: earf-real-<line|fill>-<black|white>.svg, transparent, and a PNG of each on its
    ground."""
    import subprocess
    os.makedirs(out, exist_ok=True)
    files = []
    for style, ink, bg, tag in FLATS:
        f = os.path.join(out, f'earf-real-{style}-{tag}')
        open(f + '.svg', 'w').write(flat_svg(style, ink, None))
        open(f + '.ground.svg', 'w').write(flat_svg(style, ink, bg))
        subprocess.run(['rsvg-convert', '-w', str(px), '-h', str(px), f + '.ground.svg', '-o', f + '.png'], check=True)
        os.unlink(f + '.ground.svg')
        files += [f + '.svg', f + '.png']
    return files


def _flat_frame(job):
    import subprocess
    import mark as K
    path, style, ink, bg, spin = job
    open(path[:-4] + '.svg', 'w').write(flat_svg(style, ink, bg, spin=spin, e=1 + 2 * K.SPIN['clear']))
    subprocess.run(['rsvg-convert', '-w', str(K.SPIN['px']), '-h', str(K.SPIN['px']), path[:-4] + '.svg', '-o', path], check=True)
    os.unlink(path[:-4] + '.svg')


def flat_spins(out, frames=120):
    """The flat versions spinning, black on paper: earf-real-<line|fill>-black-spin.mp4 and .webm, half a turn."""
    import tempfile
    from multiprocessing import Pool
    import mark as K
    os.makedirs(out, exist_ok=True)
    files = []
    for style, ink, bg, tag in FLATS[:2]:
        with tempfile.TemporaryDirectory() as tmp:
            jobs = [(os.path.join(tmp, f'f{k:04d}.png'), style, ink, bg, K.SPIN['turn'] * k / frames) for k in range(frames)]
            with Pool() as pool:
                pool.map(_flat_frame, jobs)
            files += encode(tmp, os.path.join(out, f'earf-real-{style}-{tag}-spin'))
    return files


def turn(root, spin):
    """The globe at `spin` degrees on its own axis (earth.rings' meridians at their longitudes plus spin)."""
    from mathutils import Matrix
    M = Matrix([list(row) for row in orientation()]).to_4x4()
    root.matrix_world = M @ Matrix.Rotation(math.radians(spin), 4, 'Z')


def main():
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    ap.add_argument('--still', help='one frame, framed as the flat marks are, to this PNG')
    ap.add_argument('--spin-frames', help='the half turn, framed as the spins are, as f0000.png ... in this directory')
    ap.add_argument('--spin', type=float, default=0.0, help='with --still, the globe turned this far on its axis')
    ap.add_argument('--frames', type=int, default=120)
    ap.add_argument('--ground', default='paper', choices=sorted(GROUNDS))
    ap.add_argument('--px', type=int)
    ap.add_argument('--samples', type=int)
    ap.add_argument('--env', default='dim', choices=['studio', 'dim', 'grey', 'dark'])
    ap.add_argument('--tint', default='glow', choices=['cabinet', 'glow'], help="glow()'s tints, or the cabinets' own")
    ap.add_argument('--slots', action='store_true', help='the discs slotted through one another, not cemented clear')
    ap.add_argument('--depth', type=float, default=MARK_DEPTH, help='the path (m) after which the acrylic is its tint')
    ap.add_argument('--first', type=int, default=0, help='with --spin-frames, start at this frame (a resumed run)')
    ap.add_argument('--last', type=int, help='with --spin-frames, stop before this frame')
    ap.add_argument('--adaptive', type=float, help='the noise Cycles stops sampling at (0.01 a still, 0.02 the spin)')
    ap.add_argument('--encode', nargs=2, metavar=('FRAMES', 'OUT'), help='spin frames to OUT.mp4 and OUT.webm, as mark.py encodes')
    ap.add_argument('--flat', help='the flat line and fill versions, black on paper and white on night, as SVG and PNG here')
    ap.add_argument('--flat-spin', help='the flat versions spinning, black on paper, as MP4 and WebM here')
    a = ap.parse_args()
    if a.encode:
        for f in encode(*a.encode):
            print(f)
    if a.flat:
        for f in flat_files(a.flat):
            print(f)
    if a.flat_spin:
        for f in flat_spins(a.flat_spin):
            print(f)
    if not (a.still or a.spin_frames):
        return
    import bpy
    bpy.ops.wm.read_factory_settings(use_empty=True)
    bpy.ops.preferences.addon_enable(module='cycles')
    t0 = time.time()
    root = build(bpy, ACRYLIC if a.tint == 'cabinet' else {k: glow(v, passed=PASS.get(k, '')) for k, v in ACRYLIC.items()},
                 not a.slots, a.depth)
    if a.still:
        stage(bpy, a.ground, a.px or 1024, 1 + E.W_LINE / 2, a.samples or 128, a.env, a.adaptive or 0.01)
        turn(root, a.spin)
        bpy.context.scene.render.filepath = os.path.abspath(a.still)
        bpy.ops.render.render(write_still=True)
        print(f'{a.still}  {time.time() - t0:.0f} s')
    if a.spin_frames:
        os.makedirs(a.spin_frames, exist_ok=True)
        import mark as K
        stage(bpy, a.ground, a.px or K.SPIN['px'], 1 + 2 * K.SPIN['clear'], a.samples or 24, a.env, a.adaptive or 0.02)
        for k in range(a.first, a.last or a.frames):
            t1 = time.time()
            turn(root, K.SPIN['turn'] * k / a.frames)
            bpy.context.scene.render.filepath = os.path.join(os.path.abspath(a.spin_frames), f'f{k:04d}.png')
            bpy.ops.render.render(write_still=True)
            print(f'frame {k}  {time.time() - t1:.0f} s', flush=True)


if __name__ == '__main__':
    main()
