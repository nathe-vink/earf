"""The globe as a Death Star, its dish a driver (round 24b).

Round 24 cut the globe open, its layers a driver. The owner: "The speaker cross section is too big and has too much
detail. I was thinking more like a death star with a slightly bigger divot. These don't feel minimal and polished
enough." So: a sphere in Ice blue with the equator's trench in Poison green (the outside, blue and green), and in its
northern half a dish, a little bigger than the Death Star's, that is a driver seen from the front: its surround Flare
red, its cone Dust orange and its dust cap Acid yellow (the inside, yellow, orange and red, as the Earth's core). The
dish is concave, so its rings sit a little off centre, toward the sphere's middle. Flat colour, no strokes. The
one-colour versions keep the strokes, as the globe's do: the trench and the rings' edges drawn as gaps in the ground.
Purple can be a small cap at the dish's centre (a variant), and is the ring of sound the dish sends out when it kicks
(earth.py).

Round 25. The owner: "Keep exploring. And a slightly larger divot is fine. And more earth on the outside." So the dish is
a little larger (24 degrees across, from 21), and the outside is the Earth: the continents in green on the blue, their
coasts coarse and rounded, so it reads as the Earth at a glance and stays flat colour (OUTSIDE 'land'; round 24b's plain
sphere and green trench is OUTSIDE 'plain'). In one colour the coasts are gaps, as the trench and the rings' edges are.

    python3 spinoffs/barkhorn/core.py     ->  brand/earth-core-<paper|ink|cap|black|white>.svg
"""
import math, os, sys

import numpy as np
from shapely.geometry import LineString, Point, Polygon
from shapely.ops import unary_union
from shapely import affinity

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import earth as E                                        # noqa: E402

OUT = os.path.join(HERE, 'brand')
C = dict(E.CLOUDS)
DISH = dict(at=(0.32, 0.34), ang=21.0, depth=0.55)      # its centre's direction (x, y on the face); its angular radius
                                                         # (the Death Star's is about 15 degrees); how deep, of its radius.
                                                         # Round 25: tried at 24, it bit every Atlantic coast, so back to
                                                         # 21 (the critics' second and third rounds: in from (0.40, 0.36),
                                                         # and deeper, 0.42 to 0.55, so it reads as a bowl, not a target)
CUTS = dict(full=dict(ang=21.0, depth=0.55),             # the dish sized by eye for each cut: at the small sizes larger
            mid=dict(ang=21.0, depth=0.42),              # and shallower, so its rings stay a pixel or more apart
            small=dict(ang=24.0, depth=0.42))
RINGS = [(1.0, C['Flare']), (0.70, C['Dust']), (0.40, C['Acid'])]   # surround, cone and dust cap, of the dish's radius
CAP = (0.15, C['Haze'])                                  # the variant's small cap at the centre
TRENCH = dict(elev=14.0, half=0.045)                     # the equator seen from a little above; its half width, of the radius
LEAN = 8.0                                               # the whole turned a little (round 25's second critic: 18 put the
                                                         # dish at half past two and tipped the Americas over)
GAP = 0.032                                              # the one-colour versions' gaps (the globe's seam, near enough)
OUTSIDE = 'land'                                         # round 25: the continents on the blue ('plain': round 24b's sphere)
# round 25, after the brand critic's first round (critic/rounds/2026-10-15/brand-deathstar-r1.json): the Americas face, the
# dish over the open Atlantic (on land its rings read as a target on a country); no trench, which sliced the land and
# wanted a blue outside the palette (it can come back, in violet); the land kept CLEAR of the dish's rim, so the red
# surround only ever meets blue (red and green are one value: the edge would vanish in grey, and to the colour-blind), and
# CLEAR inside the limb in one colour, so the disc stays a whole circle; no piece of land under MIN_PIECE of the disc
# (Greenland's tip was a speck beside the dish); the coasts rounder
TRENCH_ON = False                                        # the equator's trench (on the plain sphere, green)
VIEW = (-65.0, 12.0)                                     # the land's longitude and latitude at the face's centre (round 25's
                                                         # first try, -75, left Africa a sliver on the limb)
ROUND = 0.05                                             # how much the coasts are rounded, of the radius
CLEAR = 0.06                                             # the land's distance from the dish's rim (and, in one colour, the limb)
CLEAR_ONE = 0.10                                         # in one colour, from the rim (0.06 fused ring and land at 32 px)
MIN_PIECE = 0.015                                        # the smallest piece of land kept, of the disc's area
SMALL = 24                                               # at this many pixels across and under, the figure drops its land
MID = (48, 0.06)                                         # and up to this many, keeps only pieces this share of the disc
                                                         # (the two Americas: at 32 px the rest was specks)
# the continents, coarse (longitude, latitude), drawn by hand: enough to read as the Earth at a mark's size, no more
LAND = {
    'north america': [(-168, 66), (-160, 71), (-140, 70), (-120, 71), (-95, 72), (-80, 72), (-62, 60), (-56, 52), (-66, 45),
                      (-76, 36), (-81, 25), (-83, 29), (-90, 29), (-97, 27), (-97, 20), (-88, 21), (-87, 15), (-83, 10),
                      (-79, 8), (-92, 15), (-105, 20), (-110, 24), (-117, 32), (-124, 40), (-124, 48), (-133, 56), (-150, 60),
                      (-165, 60)],
    'south america': [(-79, 8), (-72, 12), (-62, 11), (-50, 0), (-35, -6), (-39, -14), (-48, -26), (-58, -38), (-65, -42),
                      (-68, -53), (-74, -52), (-73, -40), (-71, -30), (-70, -18), (-76, -14), (-81, -5), (-80, 0)],
    'africa': [(-17, 21), (-6, 35), (10, 37), (20, 32), (32, 31), (35, 28), (43, 12), (51, 12), (40, -10), (40, -16),
               (35, -24), (32, -29), (20, -35), (18, -30), (12, -17), (13, -5), (9, 4), (-8, 4), (-17, 14)],
    'eurasia': [(-10, 36), (-9, 43), (-2, 44), (-5, 48), (5, 52), (8, 57), (5, 62), (18, 70), (30, 71), (45, 68), (70, 73),
                (100, 78), (140, 72), (170, 70), (180, 66), (163, 60), (150, 59), (140, 53), (135, 43), (129, 35), (122, 31),
                (121, 24), (110, 20), (106, 10), (100, 13), (98, 8), (103, 1), (98, 16), (92, 21), (80, 15), (77, 8),
                (72, 20), (66, 25), (57, 25), (58, 23), (52, 17), (44, 13), (39, 21), (35, 28), (36, 36), (28, 37),
                (26, 40), (23, 38), (20, 40), (13, 45), (16, 41), (12, 44), (9, 44), (3, 43), (-1, 37), (-6, 36)],
    'australia': [(114, -22), (123, -17), (131, -12), (137, -12), (142, -11), (146, -19), (153, -26), (151, -34), (146, -39),
                  (138, -35), (130, -32), (116, -35), (114, -26)],
    'greenland': [(-73, 78), (-55, 82), (-30, 83), (-20, 75), (-22, 70), (-43, 60), (-50, 64), (-55, 70)],
}


def _basis(d):
    d = np.asarray(d, float) / np.linalg.norm(d)
    u = np.cross([0.0, 0.0, 1.0], d)
    u = u / np.linalg.norm(u) if np.linalg.norm(u) > 1e-9 else np.array([1.0, 0.0, 0.0])
    return d, u, np.cross(d, u)


def _dish_dir():
    x, y = DISH['at']
    return np.array([x, y, math.sqrt(max(0.0, 1 - x * x - y * y))])


def ring(f, n=180, dish=None):
    """The dish's ring at a share f of its radius, as the polygon it projects to: the dish a cap cut into the sphere,
    its floor a paraboloid `depth` of its radius deep, so the inner rings lie deeper and show nearer the middle."""
    dish = dish or DISH
    d, u, v = _basis(_dish_dir())
    a = math.radians(dish['ang'])
    rr = math.sin(a)
    h = dish['depth'] * rr * (1 - f * f)                 # below the rim's plane
    c = (math.cos(a) - h) * d
    t = np.linspace(0, 2 * math.pi, n, endpoint=False)
    p = c + f * rr * (np.outer(np.cos(t), u) + np.outer(np.sin(t), v))
    return Polygon(p[:, :2])


def trench(n=180):
    """The equator's trench: the band between two parallels just either side of it, the near half only."""
    e = math.radians(TRENCH['elev'])
    t = np.linspace(math.pi, 2 * math.pi, n)             # the near half, left limb to right
    arcs = []
    for lat in (TRENCH['half'], -TRENCH['half']):
        r, y0 = math.cos(lat), math.sin(lat)
        arcs.append(np.c_[r * np.cos(t), y0 * math.cos(e) + r * np.sin(t) * math.sin(e)])
    return Polygon(np.vstack([arcs[0], arcs[1][::-1]])).intersection(Point(0, 0).buffer(1.0, resolution=128))


def _project(lon, lat):
    """A point on the Earth as the face shows it (orthographic, from above VIEW, before the figure's LEAN): x, y on the
    face and z toward us."""
    l, p = math.radians(lon - VIEW[0]), math.radians(lat)
    p0 = math.radians(VIEW[1])
    return (math.cos(p) * math.sin(l), math.cos(p0) * math.sin(p) - math.sin(p0) * math.cos(p) * math.cos(l),
            math.sin(p0) * math.sin(p) + math.cos(p0) * math.cos(p) * math.cos(l))


def land():
    """The continents on the near side as one shape on the face (y up, before LEAN): each coast made dense, its points
    on the far side moved out to the rim (so a coast running round the back follows it), then rounded by ROUND."""
    out = []
    for pts in LAND.values():
        dense = [(a + (c - a) * f, b + (d - b) * f) for (a, b), (c, d) in zip(pts, pts[1:] + pts[:1])
                 for f in np.linspace(0, 1, 12, endpoint=False)]
        P = [_project(lo, la) for lo, la in dense]
        if sum(z > 0 for _, _, z in P) < 3:
            continue
        out.append(Polygon([(x, y) if z > 0 else (x / max(1e-9, math.hypot(x, y)), y / max(1e-9, math.hypot(x, y)))
                            for x, y, z in P]).buffer(0))
    g = unary_union(out).intersection(Point(0, 0).buffer(1.0, resolution=128))
    return g.buffer(ROUND).buffer(-ROUND * 1.6).buffer(ROUND * 0.6)


def shapes(cut='full', clear=CLEAR):
    """The figure's parts for a cut (CUTS: the dish's size and depth) (y up, the sphere's radius 1, turned by LEAN): the
    sphere, the land (`clear` of the dish's rim), the trench, the dish's rings (outermost first, with their colours), the
    cap, and the dish's centre (for the kick)."""
    dish = {**DISH, **CUTS[cut]}
    turn = lambda g: affinity.rotate(g, -LEAN, origin=(0, 0))
    sphere = Point(0, 0).buffer(1.0, resolution=128)
    rings = [(turn(ring(f, dish=dish)), col) for f, col in RINGS]
    c = turn(ring(1e-3, dish=dish)).centroid
    ground = None
    if OUTSIDE == 'land':                                # clear of the dish, and no specks
        g = turn(land()).difference(rings[0][0].buffer(clear, resolution=64))
        keep = [q for q in getattr(g, 'geoms', [g]) if q.geom_type == 'Polygon' and q.area >= MIN_PIECE * math.pi]
        ground = unary_union(keep) if keep else None
    return dict(sphere=sphere, land=ground, trench=turn(trench()) if TRENCH_ON else None, rings=rings,
                cap=turn(ring(CAP[0], dish=dish)), centre=(c.x, c.y), dish=dish)


def colours():
    """The outside's colours: the sea (the sphere), the land, and the trench (green on the plain sphere, a deeper blue
    across the land and the sea)."""
    sea = C['Ice']
    return sea, C['Poison'], (E._lighter(sea, -0.25) if OUTSIDE == 'land' else C['Poison'])


def _path(g):
    return E._poly_d(g)


def core_svg(ground='paper', one=None, cap=False, size=None, small=False, mid=False, label='EARF, the globe as a Death Star'):
    """The sphere, its land and its dish; `one` a single colour, drawn by knock-outs (round 25): the disc solid, the
    land knocked out to the ground (CLEAR inside the limb, so the disc stays a whole circle), the dish's surround knocked
    out, its cone solid and its dust cap knocked out; `cap` the violet cap at the dish's centre; `small` the cut for
    SMALL pixels and under, without the land; `mid` the cut up to MID's pixels, only the largest land."""
    S = shapes('small' if small else 'mid' if mid else 'full', CLEAR_ONE if one else CLEAR)
    if small:
        S['land'] = None
    elif mid and S['land'] is not None:
        keep = [q for q in getattr(S['land'], 'geoms', [S['land']]) if q.area >= MID[1] * math.pi]
        S['land'] = unary_union(keep) if keep else None
    sea, green, deep = colours()
    out = []
    if one:
        (rim, _), (cone, _), (dust, _) = S['rings']
        body = S['sphere'].difference(rim.difference(cone)).difference(dust)
        if S['land'] is not None:
            body = body.difference(S['land'].intersection(S['sphere'].buffer(-CLEAR, resolution=128)))
        if S['trench'] is not None:
            body = body.difference(S['trench'].difference(rim.buffer(CLEAR)))
        out.append(f'<path d="{_path(body)}" fill="{one}" fill-rule="evenodd"/>')
    else:
        out.append(f'<path d="{_path(S["sphere"])}" fill="{sea}"/>')
        if S['land'] is not None:
            out.append(f'<path d="{_path(S["land"])}" fill="{green}" fill-rule="evenodd"/>')
        if S['trench'] is not None:
            out.append(f'<path d="{_path(S["trench"])}" fill="{deep}"/>')
        for g, col in S['rings']:
            out.append(f'<path d="{_path(g)}" fill="{col}"/>')
        if cap:
            out.append(f'<path d="{_path(S["cap"])}" fill="{CAP[1]}"/>')
    e = 1.02
    wh = f' width="{size}" height="{size}"' if size else ''
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{-e:.3f} {-e:.3f} {2 * e:.3f} {2 * e:.3f}"{wh} role="img" aria-label="{label}">'
            f'<title>{label}</title>{"".join(out)}</svg>')


def core_paths():
    """The figure as SVG path data (y down, the sphere's radius 1), for the page to draw and move."""
    S = shapes()
    cx, cy = S['centre']
    sea, green, deep = colours()
    return dict(sphere=_path(S['sphere']), land=_path(S['land']) if S['land'] is not None else '',
                trench=_path(S['trench']) if S['trench'] is not None else '', rings=[(_path(g), c) for g, c in S['rings']],
                cap=_path(S['cap']), capCol=CAP[1], centre=[round(cx, 4), round(-cy, 4)], sea=sea, landCol=green, trenchCol=deep,
                dish=dict(S['dish']), lean=LEAN, fr=[f for f, _ in RINGS])   # the dish's own numbers, so the page can move it


def main():
    os.makedirs(OUT, exist_ok=True)
    for tag, ground, one, cap, cut in (('paper', 'paper', None, False, ''), ('ink', 'night', None, False, ''),
                                       ('cap', 'paper', None, True, ''), ('black', 'paper', E.INK, False, ''),
                                       ('white', 'night', E.WHITE, False, ''), ('mid', 'paper', None, False, 'mid'),
                                       ('mid-black', 'paper', E.INK, False, 'mid'), ('small', 'paper', None, False, 'small'),
                                       ('small-black', 'paper', E.INK, False, 'small')):
        open(os.path.join(OUT, f'earth-core-{tag}.svg'), 'w').write(core_svg(ground, one, cap, small=cut == 'small', mid=cut == 'mid'))
    print('brand/earth-core-<paper|ink|cap|black|white|mid|mid-black|small|small-black>.svg')


if __name__ == '__main__':
    main()
