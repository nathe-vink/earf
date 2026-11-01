"""A seam frame on photographed plates (r48-biomes, the coordinator's test of 2026-10-31).

    python3.11 spinoffs/barkhorn/biomes/seam_plate.py --out DIR [--scale 0.5] [--samples 64]

Two neighbors through one real lens (35 mm, 3:2). Each half of the frame is a photographed place, a Poly Haven HDRI
seen as the backplate: misty_pines (a conifer forest in morning mist, its floor in ferns) for Poison on the left,
white_cliff_top (a coastal headland of pale rock above the sea, cloud on the far peak) for Fog on the right. The
speakers are rendered into the plates, each lit by its own half's environment (its light and reflections), on a
shadow catcher for its contact shadow. A redwood trunk stands in the midground on the join and hides it; it is
rendered in the forest's light. Two renders, one per place, laid together at the trunk's axis (composite step below).
Tropos is linked from the speaker lane's asset (assets/horn/tropos.blend), cover off.
"""
import argparse, math, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(ROOT, 'studio', 'engine'))
import numpy as np                                        # noqa: E402

TROPOS = os.path.join(HERE, 'assets', 'horn', 'tropos.blend')
CAM = dict(z=1.45, lens=35.0, pitch=-3.0)
LEFT = dict(tint='Poison', hdri='misty_pines', rot=0.0, x=-1.75, y=4.6, turn=16.0, strength=1.0)
RIGHT = dict(tint='Fog', hdri='white_cliff_top', rot=180.0, x=1.75, y=4.6, turn=-16.0, strength=1.0)
TRUNK = dict(x=0.0, y=8.5, d=1.7)


def lin(h):
    h = h.lstrip('#'); c = [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    return tuple(x / 12.92 if x <= 0.04045 else ((x + 0.055) / 1.055) ** 2.4 for x in c)


def build(bpy, a):
    import bmesh, world as Wd
    bpy.ops.wm.read_factory_settings(use_empty=True)
    bpy.ops.preferences.addon_enable(module='cycles')
    sc = bpy.context.scene
    # the speakers, linked
    with bpy.data.libraries.load(TROPOS, link=True) as (src, dst):
        dst.collections = [f'Tropos {LEFT["tint"]}', f'Tropos {RIGHT["tint"]}']
    for side, col in zip((LEFT, RIGHT), dst.collections):
        e = bpy.data.objects.new(f'tropos.{side["tint"]}', None)
        e.instance_type = 'COLLECTION'; e.instance_collection = col
        e.location = (side['x'], side['y'], -0.005); e.rotation_euler = (0, 0, math.radians(side['turn']))
        sc.collection.objects.link(e)
    # the ground: a shadow catcher, so the plate's own ground shows with the speakers' shadows on it
    bm = bmesh.new(); bmesh.ops.create_grid(bm, x_segments=1, y_segments=1, size=40.0)
    me = bpy.data.meshes.new('catcher'); bm.to_mesh(me); bm.free()
    g = bpy.data.objects.new('catcher', me); sc.collection.objects.link(g); g.is_shadow_catcher = True
    m = bpy.data.materials.new('catcher'); m.use_nodes = True
    m.node_tree.nodes['Principled BSDF'].inputs['Base Color'].default_value = (0.25, 0.25, 0.22, 1)
    me.materials.append(m)
    # the redwood on the join: fluted at its foot, rising out of frame
    mat = Wd.bark_material(bpy)
    bm = bmesh.new(); seg, rows, hgt = 48, 30, 40.0
    prev = None
    for j in range(rows + 1):
        z = -0.3 + hgt * (j / rows) ** 1.4
        rad = TRUNK['d'] / 2 * (1 - 0.15 * z / hgt) * (1 + 0.55 * math.exp(-max(z, 0) / 0.9))
        ring = [bm.verts.new((TRUNK['x'] + rad * (1 + 0.07 * math.sin(7 * 2 * math.pi * s / seg + 1.3) * math.exp(-max(z, 0) / 2.5)) * math.cos(2 * math.pi * s / seg),
                              TRUNK['y'] + rad * (1 + 0.07 * math.sin(7 * 2 * math.pi * s / seg + 1.3) * math.exp(-max(z, 0) / 2.5)) * math.sin(2 * math.pi * s / seg), z))
                for s in range(seg)]
        if prev:
            for s in range(seg):
                bm.faces.new((prev[s], prev[(s + 1) % seg], ring[(s + 1) % seg], ring[s]))
        prev = ring
    me = bpy.data.meshes.new('trunk'); bm.to_mesh(me); bm.free()
    me.polygons.foreach_set('use_smooth', [True] * len(me.polygons)); me.materials.append(mat)
    t = bpy.data.objects.new('trunk', me); sc.collection.objects.link(t)
    # ferns at the trunk's foot, so it stands in the forest floor
    import random
    R = random.Random(3)
    pts = [(TRUNK['x'] + R.uniform(-1.6, 1.2), TRUNK['y'] + R.uniform(-1.4, 0.4)) for _ in range(9)]
    # and a line of them down the join toward the lens, so the two places' ground meets under fronds
    pts += [(R.uniform(-0.6, 0.6), y_) for y_ in np.arange(5.6, 7.4, 0.45)]
    Wd.ground_z = lambda x, y: 0.0
    Wd.asset_instances(bpy, 'fern_02', pts, (0.8, 1.4), R)
    # the camera: 35 mm at eye height, level with a little tilt down, on the trunk's axis
    cd = bpy.data.cameras.new('cam'); cd.lens = CAM['lens']; cd.sensor_width = 36.0; cd.sensor_fit = 'HORIZONTAL'
    cd.dof.use_dof = True; cd.dof.aperture_fstop = 5.6; cd.dof.focus_distance = 5.0
    cam = bpy.data.objects.new('cam', cd); sc.collection.objects.link(cam); sc.camera = cam
    cam.location = (0.0, -0.4, CAM['z']); cam.rotation_euler = (math.radians(90 + CAM['pitch']), 0, 0)
    W, H = int(1800 * a.scale), int(1200 * a.scale)
    sc.render.engine = 'CYCLES'; cy = sc.cycles; cy.device = 'CPU'; cy.samples = a.samples
    cy.use_adaptive_sampling = True; cy.adaptive_threshold = 0.015
    cy.use_denoising = True; cy.denoiser = 'OPENIMAGEDENOISE'
    cy.max_bounces = 12; cy.transmission_bounces = 12; cy.volume_bounces = 2; cy.transparent_max_bounces = 16
    cy.sample_clamp_indirect = 8.0
    sc.render.resolution_x, sc.render.resolution_y = W, H
    sc.render.film_transparent = False
    sc.render.image_settings.file_format = 'OPEN_EXR'; sc.render.image_settings.color_depth = '16'
    sc.view_settings.view_transform = 'Standard'
    return sc, cam


def plate(bpy, side):
    import assets
    w = bpy.context.scene.world or bpy.data.worlds.new('plate')
    bpy.context.scene.world = w
    w.use_nodes = True; nt = w.node_tree; nt.nodes.clear()
    out = nt.nodes.new('ShaderNodeOutputWorld'); bg = nt.nodes.new('ShaderNodeBackground')
    env = nt.nodes.new('ShaderNodeTexEnvironment')
    env.image = bpy.data.images.load(os.path.abspath(assets.hdri(side['hdri'], '4k')), check_existing=True)
    tc = nt.nodes.new('ShaderNodeTexCoord'); mp = nt.nodes.new('ShaderNodeMapping')
    mp.inputs['Rotation'].default_value = (0, 0, math.radians(side['rot']))
    nt.links.new(tc.outputs['Generated'], mp.inputs['Vector']); nt.links.new(mp.outputs['Vector'], env.inputs['Vector'])
    nt.links.new(env.outputs['Color'], bg.inputs['Color']); bg.inputs['Strength'].default_value = side['strength']
    nt.links.new(bg.outputs[0], out.inputs['Surface'])


def lay(bpy, d, feather=24, ev=(0.0, 0.0), look='AgX - Medium High Contrast'):
    """The two renders laid together on the trunk's axis (the frame's center column), feathered inside the trunk."""
    import composite as Cp
    bpy.ops.wm.read_factory_settings(use_empty=True)
    L = Cp.load_exr(bpy, os.path.join(d, 'left.exr'))[..., :3] * 2 ** ev[0]
    R = Cp.load_exr(bpy, os.path.join(d, 'right.exr'))[..., :3] * 2 ** ev[1]
    H, W = L.shape[:2]
    x = np.arange(W) + 0.5
    # the join: narrow behind the trunk, widening below its foot to a broad blend of the two grounds
    y = (np.arange(H) + 0.5) / H
    f = feather * (1 + 9 * np.clip((y - 0.62) / 0.38, 0, 1))[:, None]
    t = np.clip((x[None, :] - W / 2) / f * 0.5 + 0.5, 0, 1)[..., None]
    out = L * (1 - t) + R * t
    Cp.save(bpy, out, os.path.join(d, 'frame.png'), look)
    print('laid', W, H)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--out', required=True)
    ap.add_argument('--scale', type=float, default=1.0)
    ap.add_argument('--samples', type=int, default=64)
    ap.add_argument('--rot', type=float, nargs=2, help='the two plates turned (deg)')
    ap.add_argument('--lay', action='store_true', help='only lay the two renders together')
    ap.add_argument('--ev', type=float, nargs=2, default=(0.0, 0.0))
    a = ap.parse_args()
    import bpy
    if a.lay:
        return lay(bpy, a.out, ev=a.ev)
    os.makedirs(a.out, exist_ok=True)
    if a.rot:
        LEFT['rot'], RIGHT['rot'] = a.rot
    sc, cam = build(bpy, a)
    for name, side in (('left', LEFT), ('right', RIGHT)):
        plate(bpy, side)
        sc.render.filepath = os.path.join(os.path.abspath(a.out), f'{name}.exr')
        bpy.ops.render.render(write_still=True)
        print('rendered', name, flush=True)
    lay(bpy, a.out, ev=a.ev)


if __name__ == '__main__':
    main()
