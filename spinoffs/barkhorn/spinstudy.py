"""Round 27l's study: the mark spinning as one solid object, three ways (none chosen yet, so the mark's files stay as they are).

The owner, 2026-10-17: "Also wondering if, especially for the spinning, there's a way to make it function more like a
solid object than a bunch of independent discs clipping through each other." Spinning on its own axis, the three
parallels are circles round that axis, so they never appear to move, and the meridians slide through discs that stand
still: that is what reads as clipping. Opaque discs lit by one light make each face turn in the light as a plate of one
object would; a turn about the upright moves every disc together.

    colour-lit         A: each disc an opaque slab in its colour (earth._slab), under one light from the upper left
                       (LIGHT): its face lighter as it turns toward the light, its rim in the acrylic's deeper edge tone,
                       lit too; on the globe's own axis, as the spins now turn
    black-lit          B: the seamed discs in one ink, each piece a tone of it by how its disc faces the light
    colour-turntable   C: A turned about the picture's upright instead (a turntable), so nothing slides through anything

    python3 spinoffs/barkhorn/spinstudy.py [--clips DIR] [--sheet PATH]

--clips writes each as an MP4 and a WebM, made as mark.py makes the spins (720 px, 30 fps, 45 degrees a second, a
quarter of the globe's width clear round it); A and B loop at half a turn, as the spins do, C at a whole one. --sheet
draws a strip of frames of each.
"""
import argparse, math, os, subprocess, sys, tempfile
from contextlib import contextmanager

import numpy as np
from PIL import Image, ImageDraw, ImageFont
from shapely import affinity, make_valid
from shapely.errors import GEOSException
from shapely.ops import unary_union

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import earth as E                                        # noqa: E402
import mark as K                                         # noqa: E402

LIGHT = np.array([-0.45, 0.6, 0.66]) / np.linalg.norm([-0.45, 0.6, 0.66])   # toward the light: up, left, toward us
TONE = dict(face=0.16, rim=0.12, ink=0.22, mid=0.6)      # OKLab lightness per unit of light: a face, a rim, the ink's
                                                         # pieces; `mid` the light at which a colour is its own
OPTIONS = {'colour-lit': ('colour', 'spin', 180.0), 'black-lit': ('black', 'spin', 180.0),
           'colour-turntable': ('colour', 'turn', 360.0)}   # each: how it is drawn, what turns, the loop in degrees
_basis = E.basis


@contextmanager
def _turned(t):
    """earth's globe turned t degrees about the picture's upright (a turntable), on top of its own axis's spin."""
    if t:
        c, s = math.cos(math.radians(t)), math.sin(math.radians(t))
        E.basis = lambda *a, **k: tuple(np.array([v[0] * c + v[2] * s, v[1], -v[0] * s + v[2] * c]) for v in _basis(*a, **k))
    try:
        yield
    finally:
        E.basis = _basis


def _poly(g):
    """The polygons of a geometry (an overlay can leave lines and points beside them)."""
    if g.is_empty or g.geom_type in ('Polygon', 'MultiPolygon'):
        return g
    return unary_union([q for q in getattr(g, 'geoms', []) if q.geom_type in ('Polygon', 'MultiPolygon')])


def _ov(op, a, b):
    """a's `op` ('difference' or 'intersection') with b, polygons only: snapped to earth's grid, else exact, else
    coarser (turning edge on, two slabs can meet along a line GEOS cannot place)."""
    a, b = _poly(make_valid(a)), _poly(make_valid(b))
    for gs in (E.GRID, None, 1e-5, 1e-4):
        try:
            return _poly(getattr(a, op)(b, grid_size=gs))
        except GEOSException:
            continue
    raise GEOSException(f'{op} failed at every grid')


def _shade(c, k):
    """c lighter (k > 0) or darker (k < 0) by k in OKLab lightness."""
    L, a, b = E._oklab(c)
    return E._from_oklab(np.array([L + k, a, b]))


def _lit(face):
    """How much light a slab's face and its near rim take (0 to 1): the face by its normal turned toward us, the rim by
    the direction it faces, out from the face's middle and square to it."""
    n = np.asarray(face['n'], float)
    m = n if n[2] >= 0 else -n
    r = np.array([0.0, 0.0, 1.0]) - m[2] * m
    return max(0.0, float(m @ LIGHT)), max(0.0, float(r @ LIGHT) / (np.linalg.norm(r) + 1e-9))


def _slabs(spin, turn, thick):
    """Each disc's visible part (earth.facets, as slabs `thick` thick) with its face and rim, the globe turned."""
    if abs(spin % 60 - 30) < 1e-3:                       # (as mark.spin_svg: a meridian exactly edge on drops out)
        spin += 2e-3
    with _turned(turn):
        return E.facets(spin, thick), [E._slab(g, thick) for g in E.rings(spin)]


def colour_body(spin=0.0, turn=0.0, cols=E.RING, lap=0.004):
    """A and C: the discs opaque in their colours, each face and rim toned by the light, flush as the colour discs are
    (each part a hair larger, cut to the outline, so no hairline of the ground shows between two)."""
    fs, slabs = _slabs(spin, turn, E.THICK)
    sil = unary_union([f for f in fs if not f.is_empty])
    out = []
    for i, (f, (face, rim)) in enumerate(zip(fs, slabs)):
        if f.is_empty:
            continue
        lf, lr = _lit(face)
        tones = (_shade(cols[i], TONE['face'] * (lf - TONE['mid'])),
                 _shade(E._side(cols[i], E.ACRYLIC['paper']), TONE['rim'] * (lr - TONE['mid'])))
        f, rim = _poly(f), _poly(rim)
        for region, c in zip((_ov('difference', f, rim), _ov('intersection', f, rim)), tones):
            if not region.is_empty:
                g = _ov('intersection', region.buffer(lap, join_style=2, mitre_limit=4), sil)
                out.append(f'<path d="{E._poly_d(g)}" fill="{c}" fill-rule="evenodd"/>')
    return ''.join(out)


def black_body(spin=0.0, turn=0.0, ink=E.INK):
    """B: the seamed discs (as the spin's, each a slab its seam thicker, no piece dropped), each face and rim a tone
    of the ink by its light, scaled back by the seam as the spin's are."""
    seam = E.SEAM
    fs, slabs = _slabs(spin, turn, E.THICK + seam)
    s_ = 1 / (1 - seam / 2)
    out = []
    for f, (face, rim) in zip(fs, slabs):
        if f.is_empty:
            continue
        lf, lr = _lit(face)
        f, rim = _poly(f), _poly(rim)
        for region, k in ((_ov('difference', f, rim), lf), (_ov('intersection', f, rim), lr)):
            g = region.buffer(-seam / 2, join_style=2, mitre_limit=4) if not region.is_empty else region
            if not g.is_empty:
                g = affinity.scale(g, s_, s_, origin=(0, 0))
                out.append(f'<path d="{E._poly_d(g)}" fill="{_shade(ink, TONE["ink"] * k)}" fill-rule="evenodd"/>')
    return ''.join(out)


def study_svg(tag, a):
    """One frame of an option, turned `a` degrees, framed as mark.py frames the spins."""
    style, kind, _ = OPTIONS[tag]
    body = (colour_body if style == 'colour' else black_body)(spin=a if kind == 'spin' else 0.0, turn=a if kind == 'turn' else 0.0)
    e = 1 + 2 * K.SPIN['clear']
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{-e:.4f} {-e:.4f} {2 * e:.4f} {2 * e:.4f}">'
            f'<rect x="{-e:.4f}" y="{-e:.4f}" width="{2 * e:.4f}" height="{2 * e:.4f}" fill="{E.PAPER}"/>{body}</svg>')


def _frame(job):
    path, tag, a = job
    open(path[:-4] + '.svg', 'w').write(study_svg(tag, a))
    subprocess.run(['rsvg-convert', '-w', str(K.SPIN['px']), '-h', str(K.SPIN['px']), path[:-4] + '.svg', '-o', path], check=True)
    os.unlink(path[:-4] + '.svg')


def clips(out):
    """Each option as a seamless loop, <out>/<tag>.mp4 and .webm, encoded as mark.spin encodes the spins."""
    from multiprocessing import Pool
    os.makedirs(out, exist_ok=True)
    files = []
    for tag, (_, _, turn) in OPTIONS.items():
        n = round(turn / K.SPIN['rate'] * K.SPIN['fps'])
        with tempfile.TemporaryDirectory() as tmp:
            with Pool() as pool:
                pool.map(_frame, [(os.path.join(tmp, f'f{i:04d}.png'), tag, turn * i / n) for i in range(n)])
            src = ['ffmpeg', '-v', 'error', '-y', '-framerate', str(K.SPIN['fps']), '-i', os.path.join(tmp, 'f%04d.png')]
            f = os.path.join(out, tag)
            subprocess.run(src + ['-c:v', 'libx264', '-preset', 'slow', '-crf', '18', '-tune', 'animation', '-pix_fmt', 'yuv420p',
                                  '-movflags', '+faststart', f + '.mp4'], check=True)
            subprocess.run(src + ['-c:v', 'libvpx-vp9', '-b:v', '0', '-crf', '30', '-row-mt', '1', '-pix_fmt', 'yuv420p',
                                  '-fflags', '+bitexact', '-flags:v', '+bitexact', f + '.webm'], check=True)
            files += [f + '.mp4', f + '.webm']
    return files


def sheet(path, frames=20):
    """The options on one sheet, `frames` frames across each loop."""
    font, small = ImageFont.truetype('DejaVuSans.ttf', 15), ImageFont.truetype('DejaVuSans.ttf', 12)
    px, lw = 160, 170
    names = {'colour-lit': 'A  colour, lit', 'black-lit': 'B  black, lit', 'colour-turntable': 'C  turntable'}
    im = Image.new('RGB', (lw + frames * (px + 6), 10 + len(OPTIONS) * (px + 28)), '#DEDCD7')
    d = ImageDraw.Draw(im)
    for r, (tag, (_, kind, turn)) in enumerate(OPTIONS.items()):
        y = 10 + r * (px + 28)
        d.text((12, y + px // 2 - 8), names[tag], fill='#1C1A18', font=font)
        for i in range(frames):
            a = turn * i / frames
            im.paste(K._png(study_svg(tag, a), px, E.PAPER), (lw + i * (px + 6), y))
            d.text((lw + i * (px + 6), y + px + 4), f'{kind} {a:.0f}°', fill='#57534C', font=small)
    im.save(path)


if __name__ == '__main__':
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    ap.add_argument('--clips', help='write each option as an MP4 and a WebM in this directory')
    ap.add_argument('--sheet', help='a strip of frames of each option, to this path')
    a = ap.parse_args()
    if a.clips:
        for f in clips(a.clips):
            print(f)
    if a.sheet:
        sheet(a.sheet)
        print(a.sheet)
