"""V10-1 (the v9 check, 2026-11-25): the canopy's wiring, today's v9 drawing against the two options for the owner, each
drawn from crystal.py's solids (HEMI_WIRING unset, O1, O2; today's top, whose cables lie on x). Per row: the canopy from
the side as it is seen (outside, true scale), cut across the cables' line through the cord (y = 0), cut along the
enclosure through the driver (x = -11; v9's driver is centred), and from below. Writes wiring-options.png here.
Run with the CAD venv:  .venv-fab/bin/python renders/2026-11-25/barkhorn/lamp-site/v10/wiring_options.py"""
import importlib, math, os, sys, tempfile
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.join(HERE, *(['..'] * 5))
sys.path.insert(0, os.path.join(ROOT, 'spinoffs', 'barkhorn', 'companions')); sys.path.insert(0, os.path.join(ROOT, 'studio', 'fabkit'))
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
from matplotlib.collections import PolyCollection
from build123d import Box, Pos, export_stl
import numpy as np

NAME = {'canopy': 'canopy', 'strap': 'mounting plate', 'enclosure': 'enclosure', 'enclosure-cover': 'enclosure cover',
        'driver': 'driver (+ its leads in O1/O2)', 'cord': 'cord (+ its conductors in O1/O2)', 'bushings': 'snap bushing + strain relief',
        'canopy-bushing': 'floor grommet', 'splice': 'lever splice', 'plate-standoffs': 'standoffs', 'enclosure-screws': 'screws',
        'cover-screws': 'cover screws', 'box-screws': 'box screws', 'grippers': 'grippers', 'gripper-brackets': 'gripper brackets',
        'suspension': 'cables', 'ground-screw': 'green screw'}
COL = dict(zip(NAME, plt.cm.tab20.colors))
ROWS = [('', 'TODAY (v9 as drawn)', 'canopy 150 x 50, the cord centred. Not wireable: the driver (84 x 40 x 25) covers the axis and is not fixed;\n'
         'screwed flat under the enclosure\'s top it leaves 11.8 under it, and the cord\'s strain relief (8.5 inside), its jacket (6) and its\n'
         'conductors\' turn need about 21 there. The supply splices are in the enclosure (7.0 in3 needed, 8.5 free).'),
        ('O1', 'OPTION 1: the cord 20 off centre, the canopy kept', 'canopy 150 x 50 as today. The cord leaves the floor 20 off the centre, on the cables\' line, and rises straight\n'
         'beside the driver through a strain relief in the cover. The driver screwed flat by its tabs under the top against one wall;\n'
         'the enclosure 64 x 100 x 36; 10 under the driver (the 8.2 splice). Mains splices in the outlet box (the input leads, 300).'),
        ('O2', 'OPTION 2: the cord centred, the canopy 62 tall (+12)', 'canopy 150 x 62. The cord centred, up through a strain relief in the cover into 22 under the driver: 8.5 of\n'
         'strain relief, 6 of jacket, the conductors turned to the splice. The driver as in O1; the enclosure 64 x 100 x 48.\n'
         'Mains splices in the outlet box, as O1.')]
fig, axs = plt.subplots(3, 4, figsize=(34, 25), gridspec_kw=dict(width_ratios=[1.05, 1.05, 1.05, 0.9]))
seen = {}
for r, (w, title, text) in enumerate(ROWS):
    os.environ['HEMI_WIRING'] = w
    import crystal as C
    C = importlib.reload(C)
    ps = {q.name: q.solid for q in C.north_parts(dict(C.V3)) if q.solid is not None}
    cb = ps['canopy'].bounding_box(); zc, zt = cb.min.Z, cb.max.Z
    # 1: outside, as seen (projected onto x-z)
    ax = axs[r][0]
    for n in ('suspension', 'canopy', 'canopy-screws', 'cord'):
        tmp = os.path.join(tempfile.gettempdir(), f'wo-{os.getpid()}-{n}.stl')
        export_stl(ps[n], tmp, tolerance=0.1, angular_tolerance=0.2)
        raw = np.fromfile(tmp, dtype=np.uint8)[84:]
        tr = np.frombuffer(raw.tobytes(), dtype=np.dtype([('n', '<f4', 3), ('v', '<f4', (3, 3)), ('a', '<u2')]))['v']
        os.remove(tmp)
        polys = tr[:, :, [0, 2]]
        ax.add_collection(PolyCollection(polys, facecolor='#1a1a1a' if n != 'suspension' else '#8e9093', edgecolor='none'))
    ax.set_xlim(-100, 100); ax.set_ylim(zc - 90, zt + 15); ax.set_aspect('equal'); ax.grid(alpha=.2)
    ax.set_title(f'{title}\nthe canopy from the side (outside)', fontsize=13, loc='left')
    ax.annotate('', (80, zc), (80, zt), arrowprops=dict(arrowstyle='<->')); ax.text(83, (zc + zt) / 2, f'{zt - zc:.0f}', fontsize=12)
    cx = C.WIRE_OPT['cord'][0] if C.WIRE_OPT else 0.0
    if cx:
        ax.annotate('', (0, zc - 8), (cx, zc - 8), arrowprops=dict(arrowstyle='<->')); ax.text(cx / 2 - 6, zc - 18, f'{cx:.0f}', fontsize=12)
        ax.axvline(0, color='#999', lw=0.7, ls='--')
    ax.set_ylabel('z above the rim, mm')
    # 2, 3: the sections
    for k, (cut, at, rng, sub) in enumerate((('y', 0.0, (-80, 80), 'cut across the cables\' line through the cord (y = 0)'),
                                             ('x', -11.0, (-80, 80), 'cut along the enclosure through the driver (x = -11)'))):
        ax = axs[r][1 + k]
        slab = Pos(0, at, (zc + zt) / 2) * Box(400, 0.2, 200) if cut == 'y' else Pos(at, 0, (zc + zt) / 2) * Box(0.2, 400, 200)
        for n in NAME:
            if n not in ps:
                continue
            try:
                sec = ps[n] & slab
            except Exception:                      # noqa: BLE001
                continue
            if sec is None:
                continue
            for e in sec.edges():
                pts = [e.position_at(i / 12) for i in range(13)]
                ln, = ax.plot([p.X if cut == 'y' else p.Y for p in pts], [p.Z for p in pts], color=COL[n], lw=1.3)
                seen[NAME[n]] = ln
        ax.set_xlim(*rng); ax.set_ylim(zc - 6, zt + 10); ax.set_aspect('equal'); ax.grid(alpha=.2)
        ax.set_title(sub, fontsize=12); ax.set_xlabel(('x' if cut == 'y' else 'y') + ', mm')
    # sizes on the sections
    db = ps['driver'].bounding_box(); cvb = ps['enclosure-cover'].bounding_box()
    ax = axs[r][1]
    if C.WIRE_OPT:
        dz0 = ps['enclosure'].bounding_box().max.Z - 1.0 - 25.0     # the driver's underside (its body 25 under the 1.0 top)
        ax.annotate('', (-25, cvb.max.Z), (-25, dz0), arrowprops=dict(arrowstyle='<->', color='#c00000'))
        ax.text(-24, (cvb.max.Z + dz0) / 2, f'{dz0 - cvb.max.Z:.1f} under\nthe driver', fontsize=11, color='#c00000')
        ax.annotate('cord: jacket ends 6 past\nthe strain relief', (cx, cvb.max.Z + 14.5), (cx + 8 if cx else 12, zt - 4),
                    arrowprops=dict(arrowstyle='->'), fontsize=10)
    else:
        ax.annotate('', (-25, cvb.max.Z), (-25, cvb.max.Z + 11.8), arrowprops=dict(arrowstyle='<->', color='#c00000'))
        ax.text(-24, cvb.max.Z + 2, '11.8 if the driver\nis screwed under the top', fontsize=11, color='#c00000')
        ax.annotate('the cord ends 1.0\nunder the driver', (0, cvb.max.Z + 1), (12, zc - 2), arrowprops=dict(arrowstyle='->'), fontsize=10)
    # 4: from below
    ax = axs[r][3]
    for n in ('canopy', 'enclosure', 'driver', 'cord', 'gripper-brackets', 'canopy-bushing', 'bushings', 'splice'):
        if n not in ps:
            continue
        try:
            sec = ps[n] & (Pos(0, 0, ((zc + 2.0) if n in ('canopy', 'canopy-bushing') else (zc + zt) / 2)) * Box(400, 400, 0.2 if n in ('canopy', 'canopy-bushing') else 200))
        except Exception:                          # noqa: BLE001
            continue
        if sec is None:
            continue
        for e in sec.edges():
            pts = [e.position_at(i / 12) for i in range(13)]
            if n in ('canopy', 'canopy-bushing') or abs(pts[0].Z - pts[-1].Z) < 0.01 and n in ('enclosure', 'driver', 'gripper-brackets', 'splice', 'bushings', 'cord'):
                ax.plot([p.X for p in pts], [-p.Y for p in pts], color=COL[n], lw=1.0)
    ax.set_xlim(-80, 80); ax.set_ylim(-80, 80); ax.set_aspect('equal'); ax.grid(alpha=.2)
    ax.set_title('from below (edges of the parts in plan)', fontsize=12); ax.set_xlabel('x (the cables\' line), mm')
    axs[r][0].text(0.0, -0.16, text, transform=axs[r][0].transAxes, fontsize=13, va='top')
fig.legend(list(seen.values()), list(seen.keys()), loc='lower center', ncol=9, fontsize=12, frameon=False)
plt.subplots_adjust(hspace=0.55, bottom=0.07, top=0.97)
out = os.path.join(HERE, 'wiring-options.png'); plt.savefig(out, dpi=60, bbox_inches='tight'); print(out, os.path.getsize(out))
