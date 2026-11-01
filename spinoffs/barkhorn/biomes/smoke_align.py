"""Smoke's habitat, re-composed to sit with the other seven (r48-biomes, the owner's note of 2026-11-01).

    python3.11 spinoffs/barkhorn/biomes/smoke_align.py WORKTREE landscape|portrait --out OUT.png [--samples 128] [--scale 1]

The owner, on seeing the eight habitats side by side: "The smoke image looks like the odd one out now, in terms of
speaker positioning in its setting. Anyway to align it with the rest? Maybe the fire in front is preventing it from
looking right."

The other seven portraits put the speaker at 0.51 of the width (median), 0.41 of the height, its feet on the line at
0.79, seen at about eye level (README, "Smoke aligned"). This takes E12r p19's own shot (the meteor on the overpass at
dusk, from the r31-element-smoke-e10 worktree WORKTREE at d55e7570) and changes only the composition:
- the speaker comes up out of its crater onto the intact road 2.4 m toward the camera, upright, turned to it, its
  feet a few millimetres into the asphalt's dust;
- the crater, the fire, the plume and the trench stay where they were, behind it, so the fire rises behind and over
  its top and the trench runs in from behind;
- nothing in front: the field of slabs thrown forward and the debris spread ahead of the crater are left out;
- the camera is the other habitats': 60 mm from 6.5 m at 0.95 m (landscape), 92 mm (portrait).
The speaker is linked from the speaker lane's asset (assets/horn2/tropos.blend, r33-speaker-horn c77460f0, cover
off): the engine's own model is still built, so the shot's lamps find their parts by name, but hidden, and the linked
Tropos Smoke stands in its place in each lamp's light linking.
"""
import argparse, json, math, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ASSET = os.path.join(HERE, 'assets', 'horn2', 'tropos.blend')
BLACK_LINING = False                  # --black-lining
SPOT = (0.0, -2.4)                    # where the speaker now stands (the crater is at the origin)
TURN = -22.0                          # its front turned toward the camera's side
# the speaker's box in each frame (fractions, x0 y0 x1 y1 from the top left), measured on the proofs, with a margin
SPEAKER_BOX = {'portrait': [0.355, 0.355, 0.64, 0.80], 'landscape': [0.39, 0.225, 0.60, 0.79]}


def compose(sh, frame):
    inst = sh['product']['instances'][0]
    inst['position'] = [SPOT[0], SPOT[1], -0.006]
    inst['rotate_z'] = TURN
    inst['tilt'] = [0.0, 0.0]
    keep = []
    for p in sh['set']['props']:
        if p.get('fn') == 'slabs' and abs(p.get('y0', 0) - 0.3) < 1e-6:
            continue                                               # the slabs thrown forward of the crater
        if p.get('fn') == 'debris':
            p = dict(p, ahead=0.0, forward=0.0, count=int(p.get('count', 100) * 0.6))
        keep.append(p)
    sh['set']['props'] = keep
    az = math.radians(-12.0)
    d = 6.5
    cam = {'position': [round(SPOT[0] + d * math.sin(az), 4), round(SPOT[1] - d * math.cos(az), 4), 0.95],
           'target': [SPOT[0], SPOT[1], 0.66 if frame == 'landscape' else 0.86],
           'lens_mm': 60 if frame == 'landscape' else 92, 'level': True, 'fstop': 4.0,
           'focus': [SPOT[0], SPOT[1] - 0.21, 0.66], 'clip_end': 3000}
    sh['camera'] = cam
    sh['size'] = [2400, 1600] if frame == 'landscape' else [1200, 1500]
    sh['title'] = 'Smoke in its element, aligned with the other seven (r48)'
    # the heat shimmer (a 2D haze in the finish) keeps off the speaker where it now stands, a margin round it
    hz = (sh.get('finish') or {}).get('dream', {}).get('haze')
    if hz:
        hz['exclude'] = [SPEAKER_BOX[frame]]
    return sh


def refinish(raw, out, shot_json, frame):
    """The finish again on a raw render, with the shimmer kept off the speaker (no new render)."""
    sh = json.load(open(shot_json))
    fin = sh['finish']
    fin['dream']['haze']['exclude'] = [SPEAKER_BOX[frame]]
    import finish as Fn
    Fn.post(raw, out, fin)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('worktree'); ap.add_argument('frame', choices=['landscape', 'portrait'])
    ap.add_argument('--out', required=True); ap.add_argument('--samples', type=int, default=128)
    ap.add_argument('--scale', type=float, default=1.0)
    ap.add_argument('--refinish', help='a raw render (.raw.png) to finish again, no render')
    ap.add_argument('--black-lining', action='store_true')
    a = ap.parse_args()
    global BLACK_LINING
    BLACK_LINING = a.black_lining
    W = os.path.abspath(a.worktree)
    if a.refinish:
        sys.path.insert(0, os.path.join(W, 'studio', 'engine'))
        return refinish(a.refinish, a.out, os.path.splitext(a.refinish)[0].replace('.raw', '') + '.shot.json', a.frame)
    src = os.path.join(W, 'renders/2026-10-18/barkhorn/element31',
                       'smoke_e12r_p19.shot.json' if a.frame == 'landscape' else 'smoke_e12r_p19-portrait.shot.json')
    sh = compose(json.load(open(src)), a.frame)
    shot = os.path.splitext(os.path.abspath(a.out))[0] + '.in.json'
    json.dump(sh, open(shot, 'w'), indent=1)
    os.chdir(W)
    sys.path.insert(0, os.path.join(W, 'studio', 'engine'))
    import bpy, render, product as Pr, lights as Lt
    linked = []
    place0 = Pr.place

    def place(bpy_, pdef, templates, shot_, root):
        objs, part_of = place0(bpy_, pdef, templates, shot_, root)
        for o in objs:
            o.hide_render = True
        with bpy_.data.libraries.load(ASSET, link=not BLACK_LINING) as (s_, d_):
            d_.collections = ['Tropos Smoke']
        col = d_.collections[0]
        if BLACK_LINING:
            # black lining sleeves (the coordinator's recommendation, 2026-11-01, awaiting the owner): the asset is
            # appended, not linked, so its lining's material can change; everything else is the asset's own
            black = bpy_.data.materials.new('lining-black'); black.use_nodes = True
            b = black.node_tree.nodes['Principled BSDF']
            b.inputs['Base Color'].default_value = (0.012, 0.012, 0.012, 1); b.inputs['Roughness'].default_value = 0.95
            # and the acrylic at the site's Smoke look: the engine's own cloud-black cabinet and horn materials (the
            # model the site's pictures were made with), built for the hidden copy, put on the asset's parts
            site = {}
            for o in objs:
                for sl in o.material_slots:
                    if sl.material:
                        site[sl.material.name] = sl.material
            for o in col.all_objects:
                for sl in o.material_slots:
                    if not sl.material:
                        continue
                    base = sl.material.name.split('.')[0]
                    if base.startswith('lining@'):
                        sl.material = black
                    elif base.startswith('bark@') and 'bark@cloud-black' in site:
                        sl.material = site['bark@cloud-black']
                    elif base.startswith('horn-lot@') and 'horn@cloud-black' in site:
                        sl.material = site['horn@cloud-black']
            print('site look:', sorted(k for k in site if k.startswith(('bark', 'horn'))))
        for inst in shot_['product']['instances']:
            e = bpy_.data.objects.new('Tropos Smoke', None)
            e.instance_type = 'COLLECTION'; e.instance_collection = col
            e.location = inst['position']; e.rotation_euler = (0, 0, math.radians(inst['rotate_z']))
            bpy_.context.scene.collection.objects.link(e)
            linked.append(e)
        return objs, part_of
    Pr.place = place
    link0 = Lt.link_receivers

    def link_receivers(bpy_, light_ob, objects):
        link0(bpy_, light_ob, objects)
        col = light_ob.light_linking.receiver_collection
        for e in linked:
            if e.name not in col.objects:
                col.objects.link(e)
    Lt.link_receivers = link_receivers
    sys.argv = ['render.py', shot, '--out', os.path.abspath(a.out), '--samples', str(a.samples), '--scale', str(a.scale)]
    render.main()


if __name__ == '__main__':
    main()
