"""Audits a saved Blender scene against the coordinator's rulings (2026-11-03), on the scene itself, not its shot file.

    python3.11 spinoffs/barkhorn/night-pictures/scene_audit.py SCENE.blend [--step-div 240]

- Cards (the coordinator's card audit, 23:43: tools/cardcast.py's method on the real camera and the real geometry):
  every mesh hidden from camera rays is a candidate reflect-only card. Rays are cast through the frame every
  max(W, H) / 240 px from the scene's own camera (its lens, sensor and shift); a mesh counts as out of frame only if no
  ray hits it (0.0 %). Occlusion is ignored, as in cardcast.py: the share is what a real card there would block.
- Lamps: every light with its type, power and ray visibility; any light or shadow linking (rulings 1-2);
  transmission off (ruling 3). Light objects have no specular factor in Blender 5 beyond `specular_factor`, listed.
- Ruling 4: any object that casts no shadow.
Prints one line per finding, then IN FRAME / out per hidden mesh.
"""
import math
import sys


def main():
    path = sys.argv[sys.argv.index('--') + 1] if '--' in sys.argv else sys.argv[1]
    div = 240
    if '--step-div' in sys.argv:
        div = int(sys.argv[sys.argv.index('--step-div') + 1])
    import bpy
    from mathutils import Vector
    bpy.ops.wm.open_mainfile(filepath=path)
    sc = bpy.context.scene
    cam = sc.camera
    W = int(sc.render.resolution_x * sc.render.resolution_percentage / 100)
    H = int(sc.render.resolution_y * sc.render.resolution_percentage / 100)
    # the camera's own frame (lens, sensor fit, shift) at unit depth, in world space
    fr = [cam.matrix_world @ v for v in cam.data.view_frame(scene=sc)]   # top-right, bottom-right, bottom-left, top-left
    o = cam.matrix_world.translation
    tr, br, bl, tl = fr
    print(f'scene {path}: {W} x {H} (as saved), camera {cam.name} at {tuple(round(c, 3) for c in o)}')

    # lamps and rulings 1-4
    for ob in sorted(bpy.data.objects, key=lambda x: x.name):
        if ob.type == 'LIGHT':
            d = ob.data
            vis = dict(cam=ob.visible_camera, diff=ob.visible_diffuse, gloss=ob.visible_glossy, trans=ob.visible_transmission,
                       vol=ob.visible_volume_scatter)
            link = bool(ob.light_linking.receiver_collection) or bool(ob.light_linking.blocker_collection)
            flags = []
            if not vis['trans']:
                flags.append('RULING 3: transmission off')
            if link:
                flags.append('RULING 1-2: light/shadow linked')
            if getattr(d, 'specular_factor', 1.0) < 1.0:
                flags.append(f'RULING 1: specular {d.specular_factor}')
            if not vis['gloss'] or not vis['diff']:
                flags.append('a share hidden (glossy/diffuse)')
            print(f'lamp {ob.name}: {d.type} {d.energy:.4g} W, visible {vis}{"  <- " + "; ".join(flags) if flags else ""}')
        elif ob.type == 'MESH':
            if not ob.visible_shadow:
                print(f'mesh {ob.name}: casts no shadow (visible_shadow off)')
            if not ob.visible_transmission:
                print(f'mesh {ob.name}: hidden from transmission rays')
    # cards: every mesh hidden from the camera
    hidden = [ob for ob in bpy.data.objects if ob.type == 'MESH' and not ob.visible_camera and not ob.hide_render]
    # cardcast.py's grid: `div` rays across the frame's longer side, whatever the saved resolution
    nx, ny = (div, max(1, round(div * H / W))) if W >= H else (max(1, round(div * W / H)), div)
    dg = bpy.context.evaluated_depsgraph_get()
    for ob in hidden:
        ev = ob.evaluated_get(dg)
        inv = ev.matrix_world.inverted()
        hit = tot = 0
        xs, ys = [], []
        for py in range(ny):
            v = (py + 0.5) / ny
            for px in range(nx):
                u = (px + 0.5) / nx
                top = tl.lerp(tr, u); bot = bl.lerp(br, u)
                p = top.lerp(bot, v)
                d = (p - o).normalized()
                tot += 1
                lo = inv @ o; ld = (inv.to_3x3() @ d).normalized()
                ok, *_ = ev.ray_cast(lo, ld)
                if ok:
                    hit += 1; xs.append(px); ys.append(py)
        pct = 100.0 * hit / tot
        ext = (f'x {min(xs) / nx:.2f}-{max(xs) / nx:.2f} y {min(ys) / ny:.2f}-{max(ys) / ny:.2f} of the frame' if xs else '')
        print(('IN FRAME ' if hit else 'out      ') + f'{pct:5.1f} %  {ob.name} (hidden from camera) {ext}')
    if not hidden:
        print('no mesh is hidden from the camera')
    # the coordinator, 23:47: every object hidden from the camera but seen in reflections. A camera-hidden area lamp is
    # one: its rectangle (or disk) is cast as a card. Point and spot lamps have no surface a ray can meet, so are listed
    for ob in sorted(bpy.data.objects, key=lambda x: x.name):
        if ob.type != 'LIGHT' or ob.visible_camera or not (ob.visible_glossy or ob.visible_transmission):
            continue
        d = ob.data
        if d.type != 'AREA':
            print(f'lamp {ob.name}: {d.type}, hidden from the camera; no surface (a point source), not a card')
            continue
        M = ob.matrix_world
        n = (M.to_3x3() @ Vector((0, 0, 1))).normalized()
        ax = (M.to_3x3() @ Vector((1, 0, 0))); ay = (M.to_3x3() @ Vector((0, 1, 0)))
        sx = d.size * ax.length; sy = (d.size_y if d.shape in ('RECTANGLE', 'ELLIPSE') else d.size) * ay.length
        ax = ax.normalized(); ay = ay.normalized(); C = M.translation
        disk = d.shape in ('DISK', 'ELLIPSE')
        hit = tot = 0; xs, ys = [], []
        for py in range(ny):
            v = (py + 0.5) / ny
            for px in range(nx):
                u = (px + 0.5) / nx
                p = tl.lerp(tr, u).lerp(bl.lerp(br, u), v)
                dv = (p - o).normalized(); tot += 1
                den = dv.dot(n)
                if abs(den) < 1e-9:
                    continue
                t = (C - o).dot(n) / den
                if t <= 0:
                    continue
                q = o + dv * t - C
                qa, qb = q.dot(ax) / (sx / 2), q.dot(ay) / (sy / 2)
                if (qa * qa + qb * qb <= 1.0) if disk else (abs(qa) <= 1 and abs(qb) <= 1):
                    hit += 1; xs.append(px); ys.append(py)
        pct = 100.0 * hit / tot
        ext = (f'x {min(xs) / nx:.2f}-{max(xs) / nx:.2f} y {min(ys) / ny:.2f}-{max(ys) / ny:.2f} of the frame' if xs else '')
        # the coordinator, 01:47 (point 6): would a real photo from this camera see the bare emitter? Points over the
        # lamp's surface, each ray-cast from the camera against the scene; any that reaches the emitter unblocked is seen
        seen = n_pts = 0
        for i in range(-6, 7):
            for j in range(-6, 7):
                qa, qb = i / 6.0, j / 6.0
                if disk and qa * qa + qb * qb > 1.0:
                    continue
                pt = C + ax * (qa * sx / 2 * 0.98) + ay * (qb * sy / 2 * 0.98)
                # only points inside the camera's frame count (a lamp out of frame is not seen, however open)
                from bpy_extras.object_utils import world_to_camera_view
                fc = world_to_camera_view(sc, cam, pt)
                if not (0.0 <= fc.x <= 1.0 and 0.0 <= fc.y <= 1.0 and fc.z > 0):
                    continue
                dv = pt - o; dist = dv.length; dv.normalize(); n_pts += 1
                ok, loc, *_ = sc.ray_cast(dg, o, dv, distance=dist - 1e-4)
                if not ok:
                    seen += 1
        print(f'lamp {ob.name}: its emitting surface seen directly by the camera at {seen} of {n_pts} points in frame'
              + ('' if seen == 0 else '  <- a real photo would show the bare emitter'))
        print(('IN FRAME ' if hit else 'out      ') + f'{pct:5.1f} %  lamp {ob.name} ({d.shape} {sx:.2f} x {sy:.2f} m, hidden from camera, seen in reflections) {ext}')


if __name__ == '__main__':
    main()
