"""The artist's rendering's helper passes from the same scene and camera as the beauty frame (the coordinator,
2026-11-11 13:10): depth (normalised, near white), an object-id flat-colour pass (a colour per object), and the lines
(the scene's contours as dark lines on white, for a pencil underdrawing: edges found in depth, normals and object id).

    python3.11 spinoffs/barkhorn/planet/afterhours/passes.py SHOT --out DIR/NAME.png --scale S --probe x

Run through render.py (it builds the scene exactly as for the beauty frame), then, instead of the probe, renders the
passes with flat emission overrides (no light involved), writes NAME-depth.png, NAME-id.png, NAME-normal.png and
NAME-lines.png, and stops before any beauty render. The haze box is hidden for these passes (it is a volume).
"""
import math, os, runpy, sys

ENG = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', '..', 'studio', 'engine')
ENG = os.path.abspath(ENG); sys.path.insert(0, ENG)
import bpy                                                            # noqa: E402
import numpy as np                                                    # noqa: E402
import probe as Pb                                                    # noqa: E402

NEAR, FAR = 0.5, 16.0


def _mat(name, build):
    m = bpy.data.materials.new(name); m.use_nodes = True; nt = m.node_tree; nt.nodes.clear()
    out = nt.nodes.new('ShaderNodeOutputMaterial'); em = nt.nodes.new('ShaderNodeEmission')
    nt.links.new(em.outputs[0], out.inputs['Surface'])
    build(nt, em)
    return m


def _depth(nt, em):
    lp = nt.nodes.new('ShaderNodeLightPath'); mr = nt.nodes.new('ShaderNodeMapRange')
    mr.inputs['From Min'].default_value = NEAR; mr.inputs['From Max'].default_value = FAR
    mr.inputs['To Min'].default_value = 1.0; mr.inputs['To Max'].default_value = 0.0
    nt.links.new(lp.outputs['Ray Length'], mr.inputs['Value']); nt.links.new(mr.outputs['Result'], em.inputs['Color'])


def _normal(nt, em):
    g = nt.nodes.new('ShaderNodeNewGeometry'); vm = nt.nodes.new('ShaderNodeVectorMath'); vm.operation = 'MULTIPLY_ADD'
    vm.inputs[1].default_value = (0.5, 0.5, 0.5); vm.inputs[2].default_value = (0.5, 0.5, 0.5)
    nt.links.new(g.outputs['Normal'], vm.inputs[0]); nt.links.new(vm.outputs[0], em.inputs['Color'])


def _ident(nt, em):
    oi = nt.nodes.new('ShaderNodeObjectInfo'); cc = nt.nodes.new('ShaderNodeCombineColor'); cc.mode = 'HSV'
    cc.inputs[1].default_value = 0.65; cc.inputs[2].default_value = 0.9
    nt.links.new(oi.outputs['Random'], cc.inputs[0]); nt.links.new(cc.outputs[0], em.inputs['Color'])


def passes(bpy_, scene, cam, objs, part_of, pattern, match, step=1):
    out = os.environ['PASSES_OUT']; base = os.path.splitext(out)[0]
    for o in scene.objects:
        if 'haze' in o.name.lower():
            o.hide_render = True
    vl = scene.view_layers[0]
    cy = scene.cycles; cy.samples = 16; cy.use_denoising = False; cy.use_adaptive_sampling = False
    cy.max_bounces = 0; cy.caustics_reflective = cy.caustics_refractive = False
    vs = scene.view_settings; vs.view_transform = 'Standard'; vs.look = 'None'; vs.exposure = 0.0; vs.use_white_balance = False
    scene.render.filter_size = 0.8
    if scene.world:
        for n in scene.world.node_tree.nodes:
            if n.type == 'BACKGROUND':
                n.inputs['Strength'].default_value = 0.0
    if scene.camera.data.dof:
        scene.camera.data.dof.use_dof = False
    arr = {}
    for nm, b in (('depth', _depth), ('normal', _normal), ('id', _ident)):
        vl.material_override = _mat('pass-' + nm, b)
        fmt = scene.render.image_settings; fmt.file_format = 'OPEN_EXR'; fmt.color_depth = '32'
        scene.render.filepath = f'{base}-{nm}.exr'
        bpy.ops.render.render(write_still=True)
        im = bpy.data.images.load(scene.render.filepath, check_existing=False)
        W, H = im.size; a = np.array(im.pixels[:], dtype=np.float32).reshape(H, W, 4)[::-1, :, :3]
        arr[nm] = a; bpy.data.images.remove(im); os.remove(scene.render.filepath)
    from PIL import Image
    d = arr['depth'][..., 0]
    Image.fromarray((np.clip(d, 0, 1) * 255 + 0.5).astype(np.uint8)).save(f'{base}-depth.png')
    Image.fromarray((np.clip(arr['id'], 0, 1) * 255 + 0.5).astype(np.uint8)).save(f'{base}-id.png')
    Image.fromarray((np.clip(arr['normal'], 0, 1) * 255 + 0.5).astype(np.uint8)).save(f'{base}-normal.png')
    # the lines: a jump in distance (relative), a fold in the surface (normals more than 35 deg apart), a change of object
    dist = NEAR + (1.0 - np.clip(d, 0, 1)) * (FAR - NEAR)
    n = arr['normal'] * 2.0 - 1.0
    nrm = n / np.maximum(np.linalg.norm(n, axis=2, keepdims=True), 1e-6)
    idc = arr['id']
    e = np.zeros(d.shape, bool)
    for dy, dx in ((0, 1), (1, 0), (1, 1), (1, -1)):
        sh = lambda x: np.roll(np.roll(x, -dy, axis=0), -dx, axis=1)     # the neighbour (wraps at the border)
        dist2, n2, id2 = sh(dist), sh(nrm), sh(idc)
        jump = np.abs(dist - dist2) / np.minimum(dist, dist2) > 0.04
        fold = (nrm * n2).sum(2) < math.cos(math.radians(35))
        obj = np.abs(idc - id2).sum(2) > 0.05
        e |= jump | fold | obj
    e[-1, :] = e[:, -1] = e[0, :] = e[:, 0] = False
    Image.fromarray(np.where(e, 0, 255).astype(np.uint8)).save(f'{base}-lines.png')
    print('PASSES', base, d.shape, 'line px %.2f%%' % (100 * e.mean()))
    raise SystemExit(0)


Pb.reflections = passes
runpy.run_path(os.path.join(ENG, 'render.py'), run_name='__main__')
