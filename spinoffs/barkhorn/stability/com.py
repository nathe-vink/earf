"""Tropos's centre of mass and the tipping check of IEC 62368-1 8.6.2.2 (2026-11-01, the engineering audit's item 1).

    python3.11 spinoffs/barkhorn/stability/com.py            ->  com.json beside this file, and a table

Each part's centroid is its closed mesh's volume centroid in the render models (the Cloud, and the proposals for
Strata), in the asset's frame: metres, z up, front -y, the feet on z = 0. Its mass is the parts list's (out-cloud/bom.csv,
per piece) where it gives one, else its volume times the material's density. The lining's batts are 30 kg/m3.

The test: a static force of 20 % of the weight (at most 250 N), in any horizontal direction, at the most unfavourable
point up to 2 m: here the top of the horn. The speaker must not tip. Since the force scales with the weight, the
check is purely geometric: about each tipping edge (the line through two feet's contacts), the centre of mass must be
at least 0.2 x the force's height inside it. Margin = (restoring - overturning) / overturning.
"""
import csv, json, math, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / 'studio' / 'engine'))
import bpy, bmesh                                                       # noqa: E402
import product as Pr                                                     # noqa: E402

G = 9.81
DENS = {'lining': 30, 'post': 7900, 'strata-post': 8800, 'strata-collar': 8800, 'screw': 7900, 'insert': 8500,
        'feet': 7900, 'hf-adaptor': 2700, 'amp-box': 2700, 'tie-rod': 7900}
ACRYLIC = 1190
# bought parts drawn in pieces (name prefix: pieces that are separate parts), and the parts list's row for each
GROUPS = {'woofer': ('woofer-ring', 'woofer-screws', 'woofer-gasket'), 'hf': ('hf-adaptor',), 'amp-plate': ()}
GROUP_BOM = {'woofer': 'woofer', 'hf': 'hf', 'amp-plate': 'amp-plate'}
SKIP = ('horn-tool', 'cloth-disc')          # tooling is not the speaker; the cover is off (and light)
BOM = {}
for r in csv.DictReader(open(ROOT / 'spinoffs/barkhorn/out-cloud/bom.csv')):
    if r['mass_g']:
        for it in r['item'].split(', '):
            BOM[it.strip()] = float(r['mass_g']) / 1000


def props(ob):
    bm = bmesh.new(); bm.from_mesh(ob.data); bmesh.ops.triangulate(bm, faces=bm.faces[:])
    V = 0.0; C = [0.0, 0.0, 0.0]
    for f in bm.faces:
        a, b, c = (v.co for v in f.verts)
        v = a.dot(b.cross(c)) / 6.0
        V += v
        for i in range(3):
            C[i] += v * (a[i] + b[i] + c[i]) / 4.0
    bm.free()
    if abs(V) < 1e-12:
        return 0.0, None
    return abs(V), [x / V for x in C]


def parts(prod, hide=()):
    bpy.ops.wm.read_factory_settings(use_empty=True)
    pdef = Pr.load_def(prod, ROOT)
    t = Pr.import_model(bpy, Path(ROOT, pdef['model']), pdef['origin_mm'], pdef.get('axes', 'gltf'))
    unfitted = {n for names in pdef.get('options', {}).values() for n in names}
    out, groups = {}, {}
    for name, ob in t.items():
        if name in unfitted or any(Pr._match(name, h) for h in hide) or any(name.startswith(s) for s in SKIP):
            continue
        vol, c = props(ob)
        if c is None:
            continue
        g = next((k for k in GROUPS if name.startswith(k + '-') and name not in GROUPS[k]), None)
        if g:                                  # a bought part drawn in pieces: its listed mass spread by volume
            groups.setdefault(g, []).append((name, vol, c)); continue
        if name in BOM:
            m, src = BOM[name], 'bom'
        else:
            d = next((v for k, v in DENS.items() if name.startswith(k)), ACRYLIC)
            m, src = vol * d, f'{d} kg/m3'
        out[name] = dict(mass=m, c=c, src=src)
    for g, pieces in groups.items():
        V = sum(v for _, v, _ in pieces)
        for name, v, c in pieces:
            out[name] = dict(mass=BOM[GROUP_BOM[g]] * v / V, c=c, src=f'{GROUP_BOM[g]} by volume')
    return out, pdef


def feet(P):
    return [(x, y) for x in (P['x0'], P['x1']) for y in (P['y0'], P['y1'])]


def tipping(M, C, contact, h):
    """Margins about the four edges of the feet's rectangle (front, back, left, right) for a push at height h."""
    x0, x1, y0, y1 = contact
    d = {'forward': C[1] - y0, 'back': y1 - C[1], 'left': C[0] - x0, 'right': x1 - C[0]}
    need = 0.2 * h
    return {k: dict(arm_mm=round(v * 1000), need_mm=round(need * 1000), margin_pct=round(100 * (v - need) / need))
            for k, v in d.items()}


def main():
    STRATA_HIDE = ['cloth-disc', 'horn-throat', 'post-*', 'post-sleeves', 'post-sockets', 'waveguide', 'woofer-ring']
    cur, _ = parts('studio/products/barkhorn-cloud.json')
    st = {**parts('studio/products/barkhorn-cloud.json', STRATA_HIDE)[0],
          **parts('studio/products/barkhorn-variants.json', ['horn-topo*'])[0]}
    # the feet's contact points: the feet parts' lowest points
    res = {}
    for label, P in (('current', cur), ('strata', st)):
        M = sum(p['mass'] for p in P.values())
        C = [sum(p['mass'] * p['c'][i] for p in P.values()) / M for i in range(3)]
        res[label] = dict(mass_kg=round(M, 1), com_m=[round(x, 4) for x in C],
                          top=[(n, round(p['mass'], 2)) for n, p in sorted(P.items(), key=lambda kv: -kv[1]['mass'])[:12]])
    # the force's height: the top of the horn (the most unfavourable point under 2 m)
    tops = {'current': 1.2951, 'strata': 1.305}
    # tipping edges: the feet's centres (a swivel base pivots on its ball: the conservative edge) and their pads' outer
    # edges; then the footprint each option needs for a 15 % margin. x: -left +right; y: -front +back
    configs = {'feet now (centres)': (-0.23, 0.23, -0.1887, 0.1813),
               'feet now (pad edges)': (-0.25, 0.25, -0.2087, 0.2013)}
    for label, P in (('current', cur), ('strata', st)):
        C = res[label]['com_m']; h = tops[label]
        res[label]['push_height_m'] = h
        res[label]['push_N'] = round(min(0.2 * res[label]['mass_kg'] * G, 250), 1)
        res[label]['need_arm_mm'] = round(200 * h)
        res[label]['need_arm_mm_for_15pct'] = round(200 * h * 1.15)
        res[label]['tipping'] = {k: tipping(None, C, v, h) for k, v in configs.items()}
        a = 0.2 * h * 1.15                 # the feet's centres for a 15 % margin, about this centre of mass
        res[label]['feet_for_15pct_m'] = dict(x=[round(C[0] - a, 3), round(C[0] + a, 3)],
                                              y=[round(C[1] - a, 3), round(C[1] + a, 3)])
    json.dump(res, open(Path(__file__).with_name('com.json'), 'w'), indent=1)
    for label in res:
        r = res[label]
        print(label, r['mass_kg'], 'kg, CoM', r['com_m'], 'push', r['push_N'], 'N at', r['push_height_m'], 'm; need', r['need_arm_mm'], 'mm (15 %:', r['need_arm_mm_for_15pct'], ')')
        for k, v in r['tipping'].items():
            print('   ', k, {d: (x['arm_mm'], f"{x['margin_pct']:+d} %") for d, x in v.items()})
        print('    feet for +15 %:', r['feet_for_15pct_m'])


if __name__ == '__main__':
    main()
