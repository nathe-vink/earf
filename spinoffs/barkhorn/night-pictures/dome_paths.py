"""The Hemisphere's dome, light path by light path (the coordinator's photometry critics, 2026-11-10 00:13).

    python3.11 spinoffs/barkhorn/night-pictures/dome_paths.py SCENE.blend VARIANT OUT.exr [--samples N]

SCENE.blend: night_room.py --save-blend (saved before the beauty pass, the scene as it renders). Renders a crop of the
frame round the pendant (x 0.57-0.66, y 0.22-0.36 from the top, at 1920 x 1080), no denoising, no clamp, caustics on,
as the pictures render, to a linear EXR. (Blender 5 here writes the Combined pass alone, so the light paths are split by
variants of the scene, not by render passes.) VARIANT:
  as-is            the scene unchanged
  opal-black       the opal liner's diffuse and translucent colours 0 (its glossy coat kept): what is left is not light
                   the liner scatters
  glass-physical   the shells' glass (clear, clear-in, tint, tint-in, the kit's materials) without their shadow-ray
                   shortcut: the kit sends shadow rays straight through the glass as a Transparent BSDF; here every
                   ray meets the glass
  no-cob           the COB off (what the room and the window put on the dome)
  console-white    the console a white Lambertian (albedo 1, no gloss): pi x its radiance is the irradiance on it
--crop X0 Y0 X1 Y1 (frame fractions from the top left) renders another region (the walnut: 0.60 0.45 0.75 0.53).
Prints each pass's mean over the dome's face and checks the emission pass.
"""
import sys


def main():
    a = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else sys.argv[1:]
    path, variant, out = a[0], a[1], a[2]
    samples = int(a[a.index('--samples') + 1]) if '--samples' in a else 1024
    import bpy
    bpy.ops.wm.open_mainfile(filepath=path)
    sc = bpy.context.scene
    if variant == 'opal-black':
        for m in bpy.data.materials:
            if m.name.startswith('opal') and m.node_tree:
                for nd in m.node_tree.nodes:
                    if nd.type in ('BSDF_DIFFUSE', 'BSDF_TRANSLUCENT'):
                        nd.inputs['Color'].default_value = (0, 0, 0, 1)
    elif variant == 'glass-physical':
        for m in bpy.data.materials:
            base = m.name.split('.')[0]
            if base in ('clear', 'clear-in', 'tint', 'tint-in') and m.node_tree:
                nt = m.node_tree
                g = next(n for n in nt.nodes if n.type == 'BSDF_GLASS')
                o = next(n for n in nt.nodes if n.type == 'OUTPUT_MATERIAL')
                nt.links.new(g.outputs[0], o.inputs['Surface'])
                print('dome_paths: shadow-ray shortcut removed in', m.name, flush=True)
    elif variant == 'opal-black-glass-physical':
        for m in bpy.data.materials:
            if m.name.startswith('opal') and m.node_tree:
                for nd in m.node_tree.nodes:
                    if nd.type in ('BSDF_DIFFUSE', 'BSDF_TRANSLUCENT'):
                        nd.inputs['Color'].default_value = (0, 0, 0, 1)
            base = m.name.split('.')[0]
            if base in ('clear', 'clear-in', 'tint', 'tint-in') and m.node_tree:
                nt = m.node_tree
                nt.links.new(next(n for n in nt.nodes if n.type == 'BSDF_GLASS').outputs[0],
                             next(n for n in nt.nodes if n.type == 'OUTPUT_MATERIAL').inputs['Surface'])
    elif variant == 'console-white':
        wm = bpy.data.materials.new('white-card'); wm.use_nodes = True; nt = wm.node_tree; nt.nodes.clear()
        d = nt.nodes.new('ShaderNodeBsdfDiffuse'); d.inputs['Color'].default_value = (1, 1, 1, 1)
        o_ = nt.nodes.new('ShaderNodeOutputMaterial'); nt.links.new(d.outputs[0], o_.inputs['Surface'])
        for o in bpy.data.objects:
            if o.name.startswith('modern_wooden_cabinet'):
                for sl in o.material_slots:
                    sl.link = 'OBJECT'; sl.material = wm
    elif variant == 'no-cob':
        bpy.data.objects['cob'].hide_render = True
    elif variant != 'as-is':
        raise SystemExit('unknown variant ' + variant)
    r = sc.render
    r.resolution_x, r.resolution_y, r.resolution_percentage = 3840, 2160, 50
    r.use_border = True; r.use_crop_to_border = True
    x0, y0, x1, y1 = (float(v) for v in a[a.index('--crop') + 1:a.index('--crop') + 5]) if '--crop' in a else (0.57, 0.22, 0.66, 0.36)
    r.border_min_x, r.border_max_x = x0, x1
    r.border_min_y, r.border_max_y = 1 - y1, 1 - y0
    cy = sc.cycles; cy.samples = samples; cy.use_denoising = False; cy.use_adaptive_sampling = False
    r.image_settings.file_format = 'OPEN_EXR'
    r.image_settings.color_depth = '32'
    r.use_compositing = False                   # else only the composite (Combined) is written
    r.filepath = out
    vs = sc.view_settings; vs.view_transform = 'Standard'; vs.look = 'None'; vs.exposure = 0.0
    try:
        vs.use_white_balance = False
    except Exception:
        pass
    bpy.ops.render.render()
    bpy.data.images['Render Result'].save_render(out, scene=sc)    # linear (an EXR takes no view transform)
    print('dome_paths: wrote', out, flush=True)


if __name__ == '__main__':
    main()
