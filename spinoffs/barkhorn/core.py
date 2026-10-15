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
DISH = dict(at=(0.40, 0.36), ang=21.0, depth=0.42)      # its centre's direction (x, y on the face); its angular radius
                                                         # (the Death Star's is about 15 degrees); how deep, of its radius
RINGS = [(1.0, C['Flare']), (0.70, C['Dust']), (0.40, C['Acid'])]   # surround, cone and dust cap, of the dish's radius
CAP = (0.15, C['Haze'])                                  # the variant's small cap at the centre
TRENCH = dict(elev=14.0, half=0.045)                     # the equator seen from a little above; its half width, of the radius
LEAN = 18.0                                              # the whole turned a little, as the globe leans
GAP = 0.032                                              # the one-colour versions' gaps (the globe's seam, near enough)


def _basis(d):
    d = np.asarray(d, float) / np.linalg.norm(d)
    u = np.cross([0.0, 0.0, 1.0], d)
    u = u / np.linalg.norm(u) if np.linalg.norm(u) > 1e-9 else np.array([1.0, 0.0, 0.0])
    return d, u, np.cross(d, u)


def _dish_dir():
    x, y = DISH['at']
    return np.array([x, y, math.sqrt(max(0.0, 1 - x * x - y * y))])


def ring(f, n=180):
    """The dish's ring at a share f of its radius, as the polygon it projects to: the dish a cap cut into the sphere,
    its floor a paraboloid `depth` of its radius deep, so the inner rings lie deeper and show nearer the middle."""
    d, u, v = _basis(_dish_dir())
    a = math.radians(DISH['ang'])
    rr = math.sin(a)
    h = DISH['depth'] * rr * (1 - f * f)                 # below the rim's plane
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


def shapes():
    """The figure's parts (y up, the sphere's radius 1, turned by LEAN): the sphere, the trench, the dish's rings
    (outermost first, with their colours), the cap, and the dish's centre (for the kick)."""
    turn = lambda g: affinity.rotate(g, -LEAN, origin=(0, 0))
    sphere = Point(0, 0).buffer(1.0, resolution=128)
    rings = [(turn(ring(f)), col) for f, col in RINGS]
    c = turn(ring(1e-3)).centroid
    return dict(sphere=sphere, trench=turn(trench()), rings=rings, cap=turn(ring(CAP[0])), centre=(c.x, c.y))


def _path(g):
    return E._poly_d(g)


def core_svg(ground='paper', one=None, cap=False, size=None, label='EARF, the globe as a Death Star'):
    """The sphere, its trench and its dish; `one` a single colour, the trench and the rings' edges then gaps in the
    ground; `cap` the violet cap at the dish's centre."""
    bg = E.NIGHT if ground == 'night' else E.PAPER
    S = shapes()
    out = []
    if one:
        edges = unary_union([LineString(np.asarray(g.exterior.coords)) for g, _ in S['rings']]).buffer(GAP / 2)
        body = S['sphere'].difference(S['trench'].buffer(GAP * 0.15)).difference(edges)
        out.append(f'<path d="{_path(body)}" fill="{one}" fill-rule="evenodd"/>')
    else:
        out.append(f'<path d="{_path(S["sphere"])}" fill="{C["Ice"]}"/>')
        out.append(f'<path d="{_path(S["trench"])}" fill="{C["Poison"]}"/>')
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
    return dict(sphere=_path(S['sphere']), trench=_path(S['trench']), rings=[(_path(g), c) for g, c in S['rings']],
                cap=_path(S['cap']), capCol=CAP[1], centre=[round(cx, 4), round(-cy, 4)])


def main():
    os.makedirs(OUT, exist_ok=True)
    for tag, ground, one, cap in (('paper', 'paper', None, False), ('ink', 'night', None, False), ('cap', 'paper', None, True),
                                  ('black', 'paper', E.INK, False), ('white', 'night', E.WHITE, False)):
        open(os.path.join(OUT, f'earth-core-{tag}.svg'), 'w').write(core_svg(ground, one, cap))
    print('brand/earth-core-<paper|ink|cap|black|white>.svg')


if __name__ == '__main__':
    main()
