"""The horn on its four posts (2026-11-01, the engineering audit's item 2): when does it lift, and what do the posts
carry once their feet are fixed?

    python3.11 spinoffs/barkhorn/stability/horn.py      ->  horn.json beside this file, and a table

The horn assembly is the parts that lift off with it, its mass and centroid from com.py's parts. The posts stand at the
four reviewed places (CAD x 97 / 463 at y 35, x 240 / 320 at y 353; com.py's frame: x -183 / +183 at y -0.1787, x -40 /
+40 at y +0.1393), their tops (the pads) at z 0.9416 (front) and 1.0107 (rear), the cabinet's top at 0.892.

The load: the stability test's push (20 % of the speaker's weight) at the horn's top, in each direction round the
compass. With loose feet (today: the posts stand in sleeved sockets, one M6 tie rod in rear post 3), the horn starts
to lift when a post other than post 3 would go into tension, and its rotation is limited only by the sockets' depth.
With fixed feet (each post threaded into an insert, below), the posts are a rigid four-post frame: each post's axial
load is the weight's share plus the overturning moment's share (as a bolt group), and each takes a quarter of the
shear, bending as a cantilever from the top plate.
"""
import json, math, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import com                                                               # noqa: E402

G = 9.81
POSTS = [(-0.183, -0.1787), (0.183, -0.1787), (-0.040, 0.1393), (0.040, 0.1393)]   # post 1, 2 (front), 3 (tie), 4
PAD_Z = [0.9416, 0.9416, 1.0107, 1.0107]
TOP = 0.892
HORN = {'current': ('waveguide', 'horn-throat', 'horn-pod', 'waveguide-cap', 'horn-pads', 'horn-saddle', 'hf-', 'cap-o-ring', 'tie-rod', 'post-'),
        'strata': ('horn-strata', 'horn-pod', 'waveguide-cap', 'horn-pads', 'horn-saddle', 'hf-', 'cap-o-ring', 'tie-rod', 'strata-post')}
POST_D = {'current': (0.010, 0.007), 'strata': (0.016, 0.006)}            # outside and bore (the cable post's), m
E_POST = {'current': 193e9, 'strata': 100e9}


def main():
    cur, _ = com.parts('studio/products/barkhorn-cloud.json')
    st = {**com.parts('studio/products/barkhorn-cloud.json', com_hide())[0],
          **com.parts('studio/products/barkhorn-variants.json', ['horn-topo*'])[0]}
    total = {'current': sum(p['mass'] for p in cur.values()), 'strata': sum(p['mass'] for p in st.values())}
    tops = {'current': 1.2951, 'strata': 1.305}
    res = {}
    for label, P in (('current', cur), ('strata', st)):
        hp = {n: p for n, p in P.items() if n.startswith(HORN[label])}
        m = sum(p['mass'] for p in hp.values())
        c = [sum(p['mass'] * p['c'][i] for p in hp.values()) / m for i in range(3)]
        F = min(0.2 * total[label] * G, 250.0); W = m * G; h = tops[label]
        zp = sum(PAD_Z) / 4
        cx = sum(x for x, _ in POSTS) / 4; cy = sum(y for _, y in POSTS) / 4
        lift, worst = [], dict(tension=0, comp=0, bend=0)
        do, di = POST_D[label]
        I = math.pi * (do ** 4 - di ** 4) / 64; Z = I / (do / 2)
        for deg in range(0, 360, 5):
            ux, uy = math.sin(math.radians(deg)), -math.cos(math.radians(deg))   # 0 = a push toward the back (+y)... see below
            # the push's moment about the pads' plane: arm (h - zp), about the horizontal axis normal to the push
            Mx = -F * uy * (h - zp); My = F * ux * (h - zp)           # moment vector (about x, about y)
            # the weight's moment about the posts' centroid
            Mx += W * (c[1] - cy); My += -W * (c[0] - cx)
            # bolt-group axial loads: N_i = W/4 + (My*(x_i-cx) - Mx*(y_i-cy)) / ... (compression positive)
            Ixx = sum((y - cy) ** 2 for _, y in POSTS); Iyy = sum((x - cx) ** 2 for x, _ in POSTS)
            N = [W / 4 + (-My * (x - cx) / Iyy if Iyy else 0) + (Mx * (y - cy) / Ixx) for x, y in POSTS]
            # loose feet: lifts once any post but the tie post (index 2) goes tensile: find the push that does it
            def n_at(Fp):
                Mx2 = -Fp * uy * (h - zp) + W * (c[1] - cy); My2 = Fp * ux * (h - zp) - W * (c[0] - cx)
                return [W / 4 + (-My2 * (x - cx) / Iyy) + (Mx2 * (y - cy) / Ixx) for x, y in POSTS]
            lo, hi = 0.0, 2000.0
            for _ in range(60):
                mid = (lo + hi) / 2
                nn = n_at(mid)
                if min(nn[i] for i in (0, 1, 3)) < 0:
                    hi = mid
                else:
                    lo = mid
            lift.append((deg, round(lo, 1)))
            # fixed feet: worst axial and the bending at the post's root (a quarter of the shear on the longest post)
            worst['tension'] = max(worst['tension'], -min(N)); worst['comp'] = max(worst['comp'], max(N))
            Lmax = max(PAD_Z) - TOP
            worst['bend'] = max(worst['bend'], (F / 4) * Lmax / Z / 1e6)
        mn = min(lift, key=lambda t: t[1])
        res[label] = dict(horn_kg=round(m, 2), horn_com=[round(x, 4) for x in c], push_N=round(F, 1),
                          post_load_static_N=round(W / 4, 1), lift_push_min_N=mn[1], lift_direction_deg=mn[0],
                          fixed_feet=dict(max_tension_N=round(worst['tension'], 1), max_compression_N=round(worst['comp'], 1),
                                          max_bending_MPa=round(worst['bend'], 1)))
        print(label, json.dumps(res[label]))
    json.dump(res, open(HERE / 'horn.json', 'w'), indent=1)


def com_hide():
    return ['cloth-disc', 'horn-throat', 'post-*', 'post-sleeves', 'post-sockets', 'waveguide', 'woofer-ring']


if __name__ == '__main__':
    main()
