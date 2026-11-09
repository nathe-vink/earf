"""The Hemisphere's photometry in the night pictures' own lamp (the coordinator, 2026-11-09 18:47): the lamps lane's
FLUX check (r32-lamps-final 5c319549, lamp_site.py) on the lamp exactly as night_room.py places it.

    python3.11 spinoffs/barkhorn/night-pictures/flux_check.py LAMP_DIR [--samples 256]

Two renders, nothing else in the scene: the lamp appended as night_room does (the honest 11 mm COB at the top of the
bore, the CAD's aluminium reflector), and the bare COB alone (the same disk, no fitting, the 100 % reference). Under each,
a 3 x 3 m translucent white sensor 30 mm below the rim, seen from below by an orthographic camera in linear light;
flux (W) = mean luminance x pi x area. Reflective and refractive caustics on, no indirect clamp, as the pictures render.
Prints each flux and the fitting's share of the bare COB's (the lamps lane measured 53 % with no reflector, 78 % with
the aluminium).
"""
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))


def run(lamp_dir, samples, bare):
    import bpy
    sys.path.insert(0, HERE)
    import night_room as NR
    bpy.ops.wm.read_factory_settings(use_empty=True)
    sc = bpy.context.scene
    W = bpy.data.worlds.new('w'); sc.world = W; W.use_nodes = True
    W.node_tree.nodes['Background'].inputs['Strength'].default_value = 0.0
    got = NR._append_lamp(bpy, os.path.join(lamp_dir, 'hemi-fog-night.blend'), (0.0, 0.0, 0.0), honest_cob=0.011)
    cob = next(bpy.data.objects[n] for n in got if n.startswith('cob') and bpy.data.objects[n].type == 'LIGHT')
    rim_z = min((o.matrix_world @ v.co).z for n in got if n.startswith('rim') for o in [bpy.data.objects[n]] for v in o.data.vertices)
    if '--no-liner' in sys.argv:
        # the liner's own emission off (it stands for the reflector's spill lighting the opal; 145 lm on the scale)
        for m in bpy.data.materials:
            if m.name.startswith('opal-lit') and m.node_tree:
                for nd in m.node_tree.nodes:
                    if nd.type == 'EMISSION':
                        for l in list(nd.inputs['Strength'].links):
                            m.node_tree.links.remove(l)
                        nd.inputs['Strength'].default_value = 0.0
    if bare:
        # the COB alone: the same light where it sits, every part of the fitting removed
        for n in got:
            o = bpy.data.objects.get(n)
            if o is not None and o is not cob:
                bpy.data.objects.remove(o, do_unlink=True)
    zs = rim_z - (float(sys.argv[sys.argv.index('--floor') + 1]) if '--floor' in sys.argv else 0.03)
    half = 3.0 if '--floor' in sys.argv else 1.5     # a 6 x 6 m sensor at floor distance, 3 x 3 m under the rim
    sm = bpy.data.materials.new('sensor'); sm.use_nodes = True; nt = sm.node_tree; nt.nodes.clear()
    o_ = nt.nodes.new('ShaderNodeOutputMaterial'); tr = nt.nodes.new('ShaderNodeBsdfTranslucent')
    tr.inputs['Color'].default_value = (1, 1, 1, 1); nt.links.new(tr.outputs[0], o_.inputs['Surface'])
    NR._mesh(bpy, 'sensor', [(-half, -half, zs), (half, -half, zs), (half, half, zs), (-half, half, zs)], [(0, 1, 2, 3)], sm)
    cd = bpy.data.cameras.new('fluxcam'); cd.type = 'ORTHO'; cd.ortho_scale = 2 * half
    co = bpy.data.objects.new('fluxcam', cd); sc.collection.objects.link(co)
    co.location = (0, 0, zs - 1.0); co.rotation_euler = (math.pi, 0, 0); sc.camera = co
    sc.render.engine = 'CYCLES'; cy = sc.cycles; cy.device = 'CPU'; cy.samples = samples; cy.use_denoising = False
    cy.use_adaptive_sampling = False
    cy.caustics_reflective = True; cy.caustics_refractive = True; cy.sample_clamp_indirect = 0.0; cy.sample_clamp_direct = 0.0
    cy.max_bounces = 32; cy.glossy_bounces = 16; cy.transmission_bounces = 32
    sc.render.resolution_x = sc.render.resolution_y = 300; sc.render.resolution_percentage = 100
    sc.view_settings.view_transform = 'Standard'; sc.view_settings.look = 'None'; sc.view_settings.exposure = 0
    sc.render.image_settings.file_format = 'OPEN_EXR'
    out = os.path.join('/tmp', f'flux-{"bare" if bare else "fitting"}-{os.getpid()}.exr')
    sc.render.filepath = out
    bpy.ops.render.render(write_still=True)
    img = bpy.data.images.load(out); px = img.pixels[:]
    n = len(px) // 4
    Y = sum(0.2126 * px[4 * i] + 0.7152 * px[4 * i + 1] + 0.0722 * px[4 * i + 2] for i in range(n)) / n
    if '--floor' in sys.argv:
        # the radial profile of the irradiance on the floor, in 0.1 m rings round the point under the lamp
        import numpy as np
        a = np.array(px, dtype=np.float64).reshape(300, 300, 4)
        yl = 0.2126 * a[..., 0] + 0.7152 * a[..., 1] + 0.0722 * a[..., 2]
        c = (np.arange(300) + 0.5) / 300 * 2 * half - half
        rr = np.hypot(*np.meshgrid(c, c))
        prof = [(r0, float(yl[(rr >= r0) & (rr < r0 + 0.1)].mean())) for r0 in np.arange(0, 2.0, 0.1)]
        print('PROFILE', ' '.join(f'{r0:.1f}:{v:.4f}' for r0, v in prof), flush=True)
    return Y * math.pi * (2 * half) ** 2, cob.data.energy


def main():
    lamp_dir = sys.argv[1]
    samples = int(sys.argv[sys.argv.index('--samples') + 1]) if '--samples' in sys.argv else 256
    mode = sys.argv[sys.argv.index('--mode') + 1] if '--mode' in sys.argv else 'fitting'
    f, e = run(lamp_dir, samples, bare=(mode == 'bare'))
    print(f'FLUX {mode}: {f:.4f} W through the sensor (the COB set at {e:.2f} W)', flush=True)


if __name__ == '__main__':
    main()
