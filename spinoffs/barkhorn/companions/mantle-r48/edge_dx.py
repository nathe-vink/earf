"""Mantle by day, the plinth's edge and top, diagnosed (the coordinator, 2026-11-10 00:46: "black and red wood instead
of acrylic"). Runs scene.py exactly as render_lantern.sh does, then changes one thing before the render.

    python3.11 edge_dx.py VARIANT OUT.png -- SCENE.PY ARGS...

VARIANT:
  as-is           unchanged
  edge-reflect    the polished edge faces (the plinth's slot 1) an opaque black dielectric of the same IOR and
                  roughness: only what the edges reflect is left
  edge-transmit   the edge faces' specular reflection off (Specular IOR Level 0): only what is seen through them
  backdrop-flat   every backdrop surface's emission and lamps left as they are, but the seamless paper a flat mid grey
                  at roughness 1 (its gradient is the lamps'; this removes nothing, it only makes the paper matte)
The render's linear result is also written as OUT.exr.
"""
import os
import runpy
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
variant, out = sys.argv[1], sys.argv[2]
args = sys.argv[sys.argv.index('--') + 1:]
import bpy
real = bpy.ops


def modify():
    if variant == 'edge-reflect':
        for m in bpy.data.materials:
            if m.name == 'plinth-1' and m.node_tree:
                b = next(n for n in m.node_tree.nodes if n.type == 'BSDF_PRINCIPLED')
                b.inputs['Transmission Weight'].default_value = 0.0
                b.inputs['Base Color'].default_value = (0, 0, 0, 1)
                print('edge_dx: plinth-1 an opaque black dielectric', flush=True)
    elif variant == 'edge-transmit':
        for m in bpy.data.materials:
            if m.name == 'plinth-1' and m.node_tree:
                b = next(n for n in m.node_tree.nodes if n.type == 'BSDF_PRINCIPLED')
                b.inputs['Specular IOR Level'].default_value = 0.0
                print('edge_dx: plinth-1 specular off', flush=True)
    elif variant != 'as-is':
        raise SystemExit('unknown variant')


class _R:
    def __getattr__(self, n):
        if n != 'render':
            return getattr(real.render, n)

        def render(*a, **k):
            modify()
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
