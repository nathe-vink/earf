"""Mantle as signed (Strata Float v3, the owner's pick of 2026-11-01, rebuilt at 71d3163e), by day, the light off
(the coordinator, 2026-11-10 01:06): scene.py's day studio, real out-of-frame lamps and cards only, no emitter of any kind.

    python3.11 v3_day.py OUT.png [--cards] [--hide-cards] -- SCENE.PY ARGS...

--cards (the coordinator's set, 01:06): a black card above and behind the camera (the glassy top mirrors black, so it
reads as tinted glass, not gray) and the 'top' scrim lamp off (it whitened the top). A white card low behind the plinth
cannot stand out of frame from this camera; the sweep is the white surface behind and below. --hide-cards hides the
card from the camera, for gt_audit.py to prove it out of frame (0 px).

Before the render: the two black flags (scene.py hides them from the camera) are made ordinary camera-visible cards (they
stand out of frame, so nothing changes in the picture but their status), and the run stops if any material emits.
The scene is saved beside OUT as .blend (for gt_audit.py) and the linear result as .exr.
"""
import os
import runpy
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
out = sys.argv[1]
mine = sys.argv[2:sys.argv.index('--')]
args = sys.argv[sys.argv.index('--') + 1:]
import bpy
real = bpy.ops


def cards():
    from mathutils import Vector
    sc = bpy.context.scene; cam = sc.camera
    pl = [o for o in bpy.data.objects if o.name.startswith('plinth-L1')]
    pts = [o.matrix_world @ Vector(c) for o in pl for c in o.bound_box]
    lo = Vector((min(p.x for p in pts), min(p.y for p in pts), min(p.z for p in pts)))
    hi = Vector((max(p.x for p in pts), max(p.y for p in pts), max(p.z for p in pts)))
    C = (lo + hi) / 2
    print(f'v3_day: the plinth {tuple(round(v, 3) for v in lo)} to {tuple(round(v, 3) for v in hi)}', flush=True)

    def card(name, w, h, loc, target, col, rough):
        bpy.ops.mesh.primitive_plane_add(size=1.0, location=loc)
        o = bpy.context.active_object; o.name = name; o.scale = (w, h, 1)
        o.rotation_euler = (Vector(target) - Vector(loc)).to_track_quat('Z', 'Y').to_euler()
        m = bpy.data.materials.new(name); m.use_nodes = True; b = m.node_tree.nodes['Principled BSDF']
        b.inputs['Base Color'].default_value = col + (1,); b.inputs['Roughness'].default_value = rough
        o.data.materials.append(m)
        if '--hide-cards' in mine:
            o.visible_camera = False
        return o
    # black: above and a little behind the camera, 1.6 x 1.0 m, black velvet-like (rough, 2 %)
    cl = cam.matrix_world.translation; up = cam.matrix_world.to_3x3() @ Vector((0, 1, 0)); back = cam.matrix_world.to_3x3() @ Vector((0, 0, 1))
    # (the first placement, up 0.45 and back 0.25, crossed the lens's view: gt_audit, 20 % of the frame)
    # (up 0.95 back 0.55 still 6 %): behind the camera's image plane, 0.4 back and 0.35 up in world z, so never in frame
    card('card-black-top', 1.6, 1.0, cl + back * 0.4 + Vector((0, 0, 0.35)), C, (0.02, 0.02, 0.02), 0.95)
    # no white card: from this camera the ground behind and under the plinth is in frame, so a card there is seen
    # (gt_audit: 47 % of the frame). The seamless sweep is the real white surface behind and below; the studio's lamps
    # light it
    t = bpy.data.objects.get('top')
    if t is not None:
        t.hide_render = True
        print('v3_day: the top scrim lamp off', flush=True)


def prepare():
    if '--cards' in mine:
        cards()
    for o in bpy.data.objects:
        if o.name.startswith('flag-'):
            o.visible_camera = True
            print('v3_day: card', o.name, 'camera-visible', flush=True)
    for m in bpy.data.materials:
        if not m.node_tree:
            continue
        for nd in m.node_tree.nodes:
            if nd.type == 'EMISSION' and (nd.inputs['Strength'].is_linked or nd.inputs['Strength'].default_value > 0):
                users = [o.name for o in bpy.data.objects if hasattr(o.data, 'materials') and m.name in [s.material.name for s in o.material_slots if s.material]]
                if users:
                    raise SystemExit(f'v3_day: {m.name} emits on {users}: no emitter allowed')
    bpy.ops.wm.save_as_mainfile(filepath=os.path.splitext(out)[0] + '.blend', copy=True)


class _R:
    def __getattr__(self, n):
        if n != 'render':
            return getattr(real.render, n)

        def render(*a, **k):
            prepare()
            r = real.render.render(*a, **k)
            sc = bpy.context.scene; im = sc.render.image_settings
            f, d = im.file_format, im.color_depth
            im.file_format = 'OPEN_EXR'; im.color_depth = '32'
            bpy.data.images['Render Result'].save_render(os.path.splitext(out)[0] + '.exr', scene=sc)
            im.file_format, im.color_depth = f, d
            return r
        return render


class _O:
    def __getattr__(self, n):
        return _R() if n == 'render' else getattr(real, n)


bpy.ops = _O()
sys.argv = [os.path.join(HERE, 'scene.py')] + args + ['--out', out]
os.chdir(HERE)
runpy.run_path(os.path.join(HERE, 'scene.py'), run_name='__main__')
