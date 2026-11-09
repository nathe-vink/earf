"""Ground truth for scene_audit.py's in-frame test (the coordinator, 2026-11-09 23:11): Blender's own scene camera at the
scene's real resolution (and border crop, if set) renders the hidden objects themselves.

    python3.11 spinoffs/barkhorn/night-pictures/gt_audit.py SCENE.blend [--res W H]

--res: the delivered frame's size, when the scene was saved smaller for the audit (the same aspect is checked).
A control pass gives every camera-visible object one id with the targets hidden: its pixels prove the camera and the
counting see the scene (a zero from a blind setup would read as clean).

Targets: every object hidden from camera rays (meshes, curves, text, volumes' hulls) and every area lamp (hidden or not),
each made camera-visible in a flat ID emission; everything else holdout. 1 sample, no denoise, a 0.01 px filter, Raw view.
Two passes: 'seen' (the rest of the scene a holdout, so it occludes: what a photo would show) and 'footprint' (the rest
hidden: the share of the frame the object covers, occlusion ignored, as scene_audit.py measures). Every target shares the passes, its
id in the red channel; an area lamp stands in as a two-sided panel of its shape and size (it emits on one side only).
The saved scenes may carry the engine's later passes (a view-layer material override, lamps hidden for the masks): the
override is cleared; the lamps are hidden, their panels standing in.
"""
import os
import sys
import tempfile


def main():
    path = sys.argv[sys.argv.index('--') + 1] if '--' in sys.argv else sys.argv[1]
    import bpy
    import numpy as np
    bpy.ops.wm.open_mainfile(filepath=path)
    sc = bpy.context.scene
    for vl in sc.view_layers:
        vl.material_override = None
    if '--res' in sys.argv:
        i = sys.argv.index('--res'); rw, rh = int(sys.argv[i + 1]), int(sys.argv[i + 2])
        sw, sh = sc.render.resolution_x, sc.render.resolution_y
        print(f'GT: saved at {sw} x {sh} (aspect {sw / sh:.4f}); rendered at the frame\'s {rw} x {rh} (aspect {rw / rh:.4f})'
              + ('' if abs(sw / sh - rw / rh) < 1e-3 else '  <- ASPECT DIFFERS'), flush=True)
        sc.render.resolution_x, sc.render.resolution_y, sc.render.resolution_percentage = rw, rh, 100
    W = int(sc.render.resolution_x * sc.render.resolution_percentage / 100)
    H = int(sc.render.resolution_y * sc.render.resolution_percentage / 100)
    border = sc.render.use_border and sc.render.use_crop_to_border
    print(f'GT {os.path.basename(path)}: camera {sc.camera.name}, {W} x {H}'
          + (f', border x {sc.render.border_min_x:.3f}-{sc.render.border_max_x:.3f} y {sc.render.border_min_y:.3f}-{sc.render.border_max_y:.3f} (cropped)' if border else ''), flush=True)
    sc.render.engine = 'CYCLES'; cy = sc.cycles
    cy.samples = 1; cy.use_denoising = False; cy.use_adaptive_sampling = False; cy.filter_width = 0.01
    cy.max_bounces = 0
    sc.render.film_transparent = True; sc.render.dither_intensity = 0.0
    sc.camera.data.dof.use_dof = False
    vs = sc.view_settings; vs.view_transform = 'Raw'; vs.look = 'None'; vs.exposure = 0.0
    try:
        vs.use_white_balance = False
    except Exception:
        pass
    sc.render.image_settings.file_format = 'PNG'; sc.render.image_settings.color_mode = 'RGBA'
    sc.render.image_settings.color_depth = '8'
    if sc.world:
        sc.world = None
    if '--selftest' in sys.argv:
        # a known positive: a 0.2 m card and a 0.2 m area lamp, both hidden from the camera, 2 m down its axis
        from mathutils import Vector
        M = sc.camera.matrix_world; fwd = (M.to_3x3() @ Vector((0, 0, -1))).normalized()
        right = (M.to_3x3() @ Vector((1, 0, 0))).normalized()
        bpy.ops.mesh.primitive_plane_add(size=0.2, location=M.translation + fwd * 2 - right * 0.2)
        card = bpy.context.active_object; card.name = 'SELFTEST-card'; card.rotation_euler = M.to_euler()
        card.visible_camera = False
        ld = bpy.data.lights.new('SELFTEST-lamp', 'AREA'); ld.size = 0.2; ld.energy = 10
        lo = bpy.data.objects.new('SELFTEST-lamp', ld); sc.collection.objects.link(lo)
        lo.location = M.translation + fwd * 2 + right * 0.2; lo.rotation_euler = M.to_euler(); lo.visible_camera = False
        bpy.context.view_layer.update()
        print('GT selftest: a 0.2 m card and a 0.2 m area lamp hidden from the camera, 2 m in front of it', flush=True)
    geo = ('MESH', 'CURVE', 'SURFACE', 'META', 'FONT', 'CURVES', 'POINTCLOUD', 'VOLUME')
    objs = [o for o in sc.objects if o.type in geo and not o.hide_render]
    targets = [o for o in objs if not o.visible_camera]
    lamps = [o for o in sc.objects if o.type == 'LIGHT' and o.data.type == 'AREA']
    # each area lamp stands in as a two-sided panel of its own shape and size where it hangs (a lamp's surface emits
    # on one side only, so it cannot show its footprint itself; as a card, either side blocks)
    import math
    for L in lamps:
        d = L.data
        sx = d.size; sy = d.size_y if d.shape in ('RECTANGLE', 'ELLIPSE') else d.size
        if d.shape in ('DISK', 'ELLIPSE'):
            bpy.ops.mesh.primitive_circle_add(vertices=64, radius=0.5, fill_type='NGON')
        else:
            bpy.ops.mesh.primitive_plane_add(size=1.0)
        pnl = bpy.context.active_object
        pnl.name = f'lamp {L.name} ({"camera-visible" if L.visible_camera else "hidden from camera"}, {d.shape} {sx:.3f} x {sy:.3f} m)'
        pnl.matrix_world = L.matrix_world.copy()
        pnl.scale = (pnl.scale[0] * sx, pnl.scale[1] * sy, pnl.scale[2])
        pnl.visible_camera = False
        objs.append(pnl); targets.append(pnl)
    for o in sc.objects:
        if o.type == 'LIGHT':
            o.hide_render = True          # the lamps themselves play no part: their panels stand in
    hold = bpy.data.materials.new('gt-holdout'); hold.use_nodes = True; nt = hold.node_tree; nt.nodes.clear()
    h = nt.nodes.new('ShaderNodeHoldout'); ou = nt.nodes.new('ShaderNodeOutputMaterial'); nt.links.new(h.outputs[0], ou.inputs['Surface'])

    def idmat(i):
        m = bpy.data.materials.new(f'gt-id-{i}'); m.use_nodes = True; t = m.node_tree; t.nodes.clear()
        e = t.nodes.new('ShaderNodeEmission'); e.inputs['Color'].default_value = (i / 255.0, 0, 0, 1)
        e.inputs['Strength'].default_value = 1.0
        o_ = t.nodes.new('ShaderNodeOutputMaterial'); t.links.new(e.outputs[0], o_.inputs['Surface'])
        return m

    def setmat(o, m):
        d = getattr(o, 'data', None)
        if d is None or not hasattr(d, 'materials'):
            return
        if len(o.material_slots) == 0:
            d.materials.append(m)
        for s in o.material_slots:
            s.link = 'OBJECT'; s.material = m

    def render(tag):
        f = os.path.join(tempfile.gettempdir(), f'gt-{os.getpid()}-{tag}.png')
        sc.render.filepath = f
        bpy.ops.render.render(write_still=True)
        from PIL import Image
        a = np.asarray(Image.open(f).convert('RGBA')).astype(int)
        os.remove(f)
        return a

    # meshes: one id each
    ids = {}
    for i, o in enumerate(targets):
        ids[i + 1] = o.name
        setmat(o, idmat(i + 1)); o.visible_camera = True
    others = [o for o in objs if o not in targets]
    for o in sc.objects:
        if o.type == 'LIGHT':
            o.visible_camera = False
    res = {}
    if targets:
        for o in others:
            setmat(o, hold)
        a = render('seen')
        for o in others:
            o.hide_render = True
        b = render('footprint')
        for o in others:
            o.hide_render = False
        n = a.shape[0] * a.shape[1]
        for i, name in ids.items():
            s = int(((a[..., 3] > 127) & (a[..., 0] == i)).sum()); fp = int(((b[..., 3] > 127) & (b[..., 0] == i)).sum())
            res[name] = (s, fp, n)
        for o in targets:
            o.visible_camera = False
    else:
        for o in others:
            setmat(o, hold)
    # the control: every camera-visible object id 255, the targets hidden
    ctl = idmat(255)
    for o in others:
        setmat(o, ctl)
    for o in targets:
        o.hide_render = True
    c = render('control')
    for o in targets:
        o.hide_render = False
    for o in others:
        setmat(o, hold)
    print(f'GT control: the camera-visible scene covers {int(((c[..., 3] > 127) & (c[..., 0] == 255)).sum())} of {c.shape[0] * c.shape[1]} px '
          f'({c.shape[1]} x {c.shape[0]})', flush=True)
    if not res:
        print('GT: no hidden object and no area lamp in the scene')
    for name, (s, fp, n) in sorted(res.items()):
        flag = '  <- IN FRAME' if fp else ''
        print(f'GT {name}: seen {s} px, footprint {fp} px ({100.0 * fp / n:.2f} % of {n}){flag}', flush=True)


if __name__ == '__main__':
    main()
