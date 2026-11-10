"""Ground truth for scene_audit.py's in-frame test (the coordinator, 2026-11-09 23:11): Blender's own scene camera at the
scene's real resolution (and border crop, if set) renders the hidden objects themselves.

    python3.11 spinoffs/barkhorn/night-pictures/gt_audit.py SCENE.blend [--res W H]

--res: the delivered frame's size, when the scene was saved smaller for the audit (the same aspect is checked).
A control pass gives every camera-visible object one id with the targets hidden: its pixels prove the camera and the
counting see the scene (a zero from a blind setup would read as clean). It renders at a quarter of the frame (memory, the
biomes lane's heavy sets) after the targets' counts are printed.
--null: the null test (the biomes lane, 23:48): every target moved 50 m behind the camera; every count must be 0.

Fixes from the biomes lane (2026-11-09 23:48, their copy on r48-biomes):
- ids start at 101: id 1 collided with near-black pixels;
- instanced geometry (a collection instance's objects are not in scene.objects) was neither held out nor hidden, so
  glass in an instance stayed in the footprint pass and a lamp seen through it read as 'in frame'. Every instancer
  (an object with instance_type COLLECTION, VERTS or FACES) is now hidden in the footprint pass, and the objects its
  collection instances are held out in the seen pass;
- 'in frame' is also checked by projection: each target's vertices through world_to_camera_view (the camera's own frame).
  A footprint with no projected point in frame is flagged as seen through something, not in frame.

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
        # and a collection instance of a 0.6 m camera-visible plane 1 m down the axis, in front of the card: the card
        # must read seen 0 (held out by the instance) with its footprint unchanged (the instancer hidden)
        bpy.ops.mesh.primitive_plane_add(size=0.6, location=(0, 0, 0))
        src = bpy.context.active_object; src.name = 'SELFTEST-instanced-plane'; src.rotation_euler = M.to_euler()
        col = bpy.data.collections.new('SELFTEST-col'); col.objects.link(src); sc.collection.objects.unlink(src)
        inst = bpy.data.objects.new('SELFTEST-instancer', None); inst.instance_type = 'COLLECTION'; inst.instance_collection = col
        sc.collection.objects.link(inst); inst.location = M.translation + fwd * 1.0 - right * 0.1
        bpy.context.view_layer.update()
        print('GT selftest: a 0.2 m card and a 0.2 m area lamp hidden from the camera, 2 m in front of it; a 0.6 m plane '
              'instanced 1 m in front, over the card', flush=True)
    from bpy_extras.object_utils import world_to_camera_view

    def projected(o):
        # the share of the object's vertices that project inside the frame (z > 0)
        dg = bpy.context.evaluated_depsgraph_get(); ev = o.evaluated_get(dg)
        try:
            me = ev.to_mesh()
        except RuntimeError:
            return 0, 0
        pts = [ev.matrix_world @ v.co for v in me.vertices]; ev.to_mesh_clear()
        n = 0
        for q in pts:
            c = world_to_camera_view(sc, sc.camera, q)
            if c.z > 0 and 0.0 <= c.x <= 1.0 and 0.0 <= c.y <= 1.0:
                n += 1
        return n, len(pts)
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
    instancers = [o for o in sc.objects if o.instance_type in ('COLLECTION', 'VERTS', 'FACES') and not o.hide_render
                  and (o.instance_type != 'COLLECTION' or o.instance_collection)]
    inst_src = set()
    for o in instancers:
        if o.instance_type == 'COLLECTION':
            inst_src.update(x for x in o.instance_collection.all_objects if x.type in geo)
        else:
            inst_src.update(x for x in o.children if x.type in geo)
    inst_src = [x for x in inst_src if x not in objs]
    if instancers:
        print(f'GT: {len(instancers)} instancer(s), {len(inst_src)} instanced object(s): held out in the seen pass, hidden '
              f'in the footprint pass', flush=True)
    if '--null' in sys.argv:
        from mathutils import Vector
        back = (sc.camera.matrix_world.to_3x3() @ Vector((0, 0, 1))).normalized() * 50.0
        for o in targets:
            M = o.matrix_world.copy(); M.translation += back; o.matrix_world = M
        bpy.context.view_layer.update()
        print('GT null test: every target moved 50 m behind the camera; every count must be 0', flush=True)
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
        ids[i + 101] = o.name        # from 101: id 1 collided with near-black pixels (the biomes lane)
        setmat(o, idmat(i + 101)); o.visible_camera = True
    others = [o for o in objs if o not in targets]
    for o in sc.objects:
        if o.type == 'LIGHT':
            o.visible_camera = False
    res = {}
    if targets:
        for o in others + inst_src:
            setmat(o, hold)
        a = render('seen')
        for o in others + instancers:
            o.hide_render = True
        b = render('footprint')
        for o in others + instancers:
            o.hide_render = False
        n = a.shape[0] * a.shape[1]
        byname = {o.name: o for o in targets}
        for i, name in ids.items():
            s = int(((a[..., 3] > 127) & (a[..., 0] == i)).sum()); fp = int(((b[..., 3] > 127) & (b[..., 0] == i)).sum())
            res[name] = (s, fp, n) + projected(byname[name])
        for o in targets:
            o.visible_camera = False
    else:
        for o in others:
            setmat(o, hold)
    for name, (sn, fp, n, pin, pn) in sorted(res.items()):
        if fp and pin:
            flag = '  <- IN FRAME'
        elif fp:
            flag = '  <- footprint with no vertex in frame: seen through something, check'
        elif pin:
            flag = '  <- vertices in frame but no pixel (smaller than a pixel?)'
        else:
            flag = ''
        print(f'GT {name}: seen {sn} px, footprint {fp} px ({100.0 * fp / n:.2f} % of {n}), projected {pin} of {pn} vertices in frame{flag}', flush=True)
    if not res:
        print('GT: no hidden object and no area lamp in the scene', flush=True)
    # the control: every camera-visible object id 255, the targets hidden (a quarter of the frame: memory)
    sc.render.resolution_percentage = max(1, sc.render.resolution_percentage // 4)
    ctl = idmat(255)
    for o in others + inst_src:
        setmat(o, ctl)
    for o in targets:
        o.hide_render = True
    c = render('control')
    print(f'GT control: the camera-visible scene covers {int(((c[..., 3] > 127) & (c[..., 0] == 255)).sum())} of {c.shape[0] * c.shape[1]} px '
          f'({c.shape[1]} x {c.shape[0]})', flush=True)


if __name__ == '__main__':
    main()
