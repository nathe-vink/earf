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


def black_posts():
    # the owner, 2026-11-10: the posts black, the lamps' satin black (companions/common.py: #18181A, roughness 0.5,
    # specular 0.3); in the parts list: 303 stainless, hot black oxide for stainless, satin, oiled
    m = bpy.data.materials.new('post-satin-black'); m.use_nodes = True; b = m.node_tree.nodes['Principled BSDF']
    c = [int('18181A'[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    b.inputs['Base Color'].default_value = tuple(x / 12.92 if x <= 0.04045 else ((x + 0.055) / 1.055) ** 2.4 for x in c) + (1,)
    b.inputs['Roughness'].default_value = 0.5; b.inputs['Specular IOR Level'].default_value = 0.3
    for o in bpy.data.objects:
        if o.name.startswith('post-') and o.type == 'MESH':
            o.data.materials.clear(); o.data.materials.append(m)
            print('v3_day: satin black', o.name, flush=True)


def side_fix():
    # the coordinator, 2026-11-10: the side strip's highlight turned the posts' lit half pale (about 205). Narrowed to
    # 0.03 m and raised to the deck's middle it still reached them (its 50 deg spread: post luma p95 231 in a crop); off,
    # the posts read black (median 14, p95 26). So the side strip is OFF for the set
    o = bpy.data.objects.get('side')
    if o is not None:
        o.hide_render = True
        print('v3_day: side strip off (it lit the posts)', flush=True)


def black_bearing():
    # VARIANT for the owner: the bearing's visible brass (housing, nut, washer) satin black; the parts list stays brass
    m = bpy.data.materials.get('post-satin-black')
    if m is None:
        black_posts(); m = bpy.data.materials['post-satin-black']
    for n in ('bearing-housing', 'bearing-nut', 'bearing-washer'):
        o = bpy.data.objects.get(n)
        if o is not None:
            o.data.materials.clear(); o.data.materials.append(m); print('v3_day: satin black', n, flush=True)


def strip_watts(w):
    # the light on: the LED strip (the drawing's light) emits w watts in all, both faces of its mesh (Cycles' mesh
    # emission is two-sided): radiance = w / (2 pi A)
    obs = [o for o in bpy.data.objects if o.name.startswith('led-strip') and o.type == 'MESH']
    A = sum(p.area for o in obs for p in o.data.polygons) * (obs[0].matrix_world.to_3x3().determinant() ** (2 / 3) if obs else 1)
    for o in obs:
        for sl in o.material_slots:
            for nd in sl.material.node_tree.nodes:
                if nd.type == 'EMISSION':
                    nd.inputs['Strength'].default_value = w / (2 * 3.14159265 * A)
    print(f'v3_day: led-strip {w} W over {A * 1e4:.1f} cm2: radiance {w / (2 * 3.14159265 * max(A, 1e-9)):.1f}', flush=True)


def lamps_off(names):
    for n in names.split(','):
        o = bpy.data.objects.get(n)
        if o is not None and o.type == 'LIGHT':
            o.hide_render = True; print('v3_day: lamp off', n, flush=True)


def prepare():
    if '--lamps-off' in mine:
        lamps_off(mine[mine.index('--lamps-off') + 1])
    if '--cards' in mine:
        cards()
    if '--black-posts' in mine:
        black_posts()
    if '--side-fix' in mine:
        side_fix()
    if '--black-bearing' in mine:
        black_bearing()
    if '--strip-watts' in mine:
        strip_watts(float(mine[mine.index('--strip-watts') + 1]))
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
                if users and not all(u.startswith('led-strip') for u in users):
                    raise SystemExit(f'v3_day: {m.name} emits on {users}: no emitter allowed (the LED strip alone may)')
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
