"""A small SVG writer for the round 42 drawings: paper millimetres, a plan or section frame mapped onto the paper, and
the few things an architectural sheet needs (poché, hatches, door swings, dimensions in feet and inches, tags).
No dependencies; drawings42.py builds the sheets with it."""
import math
from xml.sax.saxutils import escape

INK = '#1d1c1a'
GREY = '#8c8984'
LIGHT = '#c9c5bd'
PAPER = '#ffffff'
FONT = "Inter, 'Helvetica Neue', Arial, sans-serif"
ARCH_D = (914.4, 609.6)          # 36 x 24 in


def ftin(m, inch=True):
    """Metres as feet and inches, to the nearest inch: 10.668 -> 35'-0"."""
    t = round(m / 0.0254)
    f, i = divmod(t, 12)
    return f"{f}'-{i}\"" if inch else f"{f}'"


class Sheet:
    def __init__(self, size=ARCH_D):
        self.w, self.h = size
        self.el = []
        self.defs = []
        self._hatches = set()

    # --- raw ----------------------------------------------------------------------------------------------------------
    def add(self, s):
        self.el.append(s)

    @staticmethod
    def _style(fill='none', stroke=INK, sw=0.18, dash=None, opacity=None, cap='butt', join='miter'):
        s = f'fill="{fill}" stroke="{stroke}" stroke-width="{sw:.3f}"'
        if dash:
            s += f' stroke-dasharray="{dash}"'
        if opacity is not None:
            s += f' opacity="{opacity}"'
        if cap != 'butt':
            s += f' stroke-linecap="{cap}"'
        if join != 'miter':
            s += f' stroke-linejoin="{join}"'
        return s

    def rect(self, x0, y0, x1, y1, rx=0, **k):
        x, y = min(x0, x1), min(y0, y1)
        w, h = abs(x1 - x0), abs(y1 - y0)
        r = f' rx="{rx:.2f}"' if rx else ''
        self.add(f'<rect x="{x:.2f}" y="{y:.2f}" width="{w:.2f}" height="{h:.2f}"{r} {self._style(**k)}/>')

    def line(self, x0, y0, x1, y1, **k):
        self.add(f'<line x1="{x0:.2f}" y1="{y0:.2f}" x2="{x1:.2f}" y2="{y1:.2f}" {self._style(**k)}/>')

    def poly(self, pts, close=True, **k):
        p = ' '.join(f'{x:.2f},{y:.2f}' for x, y in pts)
        tag = 'polygon' if close else 'polyline'
        self.add(f'<{tag} points="{p}" {self._style(**k)}/>')

    def path(self, d, **k):
        self.add(f'<path d="{d}" {self._style(**k)}/>')

    def circle(self, x, y, r, **k):
        self.add(f'<circle cx="{x:.2f}" cy="{y:.2f}" r="{r:.2f}" {self._style(**k)}/>')

    def ellipse(self, x, y, rx, ry, **k):
        self.add(f'<ellipse cx="{x:.2f}" cy="{y:.2f}" rx="{rx:.2f}" ry="{ry:.2f}" {self._style(**k)}/>')

    def text(self, x, y, s, size=2.6, anchor='start', weight=400, fill=INK, spacing=0, rot=0, italic=False, base='auto'):
        t = f' transform="rotate({rot:.1f} {x:.2f} {y:.2f})"' if rot else ''
        ls = f' letter-spacing="{spacing:.2f}"' if spacing else ''
        st = ' font-style="italic"' if italic else ''
        db = f' dominant-baseline="{base}"' if base != 'auto' else ''
        self.add(f'<text x="{x:.2f}" y="{y:.2f}" font-family="{FONT}" font-size="{size:.2f}" font-weight="{weight}" '
                 f'fill="{fill}" text-anchor="{anchor}"{ls}{st}{db}{t}>{escape(str(s))}</text>')

    def lines_of(self, x, y, rows, size=2.6, lead=1.45, **k):
        for i, r in enumerate(rows):
            self.text(x, y + i * size * lead, r, size=size, **k)
        return y + len(rows) * size * lead

    def hatch(self, name, angle=45, gap=1.2, sw=0.12, color=INK, bg='none'):
        if name in self._hatches:
            return f'url(#{name})'
        self._hatches.add(name)
        self.defs.append(f'<pattern id="{name}" patternUnits="userSpaceOnUse" width="{gap}" height="{gap}" '
                         f'patternTransform="rotate({angle})"><rect width="{gap}" height="{gap}" fill="{bg}"/>'
                         f'<line x1="0" y1="0" x2="0" y2="{gap}" stroke="{color}" stroke-width="{sw}"/></pattern>')
        return f'url(#{name})'

    def dots(self, name, gap=1.4, r=0.16, color=INK, bg='none'):
        if name in self._hatches:
            return f'url(#{name})'
        self._hatches.add(name)
        self.defs.append(f'<pattern id="{name}" patternUnits="userSpaceOnUse" width="{gap}" height="{gap}">'
                         f'<rect width="{gap}" height="{gap}" fill="{bg}"/>'
                         f'<circle cx="{gap / 2}" cy="{gap / 2}" r="{r}" fill="{color}"/></pattern>')
        return f'url(#{name})'

    def image(self, x, y, w, h, href):
        self.add(f'<image x="{x:.2f}" y="{y:.2f}" width="{w:.2f}" height="{h:.2f}" href="{href}" '
                 f'preserveAspectRatio="xMidYMid slice"/>')

    def svg(self):
        return (f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" '
                f'width="{self.w}mm" height="{self.h}mm" viewBox="0 0 {self.w} {self.h}">'
                f'<defs>{"".join(self.defs)}</defs><rect width="{self.w}" height="{self.h}" fill="{PAPER}"/>'
                + '\n'.join(self.el) + '</svg>')

    # --- a sheet's furniture --------------------------------------------------------------------------------------------
    def frame(self, number, title, subtitle, sheet_list, notes=(), site=None):
        """The border and a title strip down the right-hand edge, US style."""
        m = 12.0
        self.rect(m, m, self.w - m, self.h - m, sw=0.5)
        tx = self.w - m - 92
        self.line(tx, m, tx, self.h - m, sw=0.35)
        x = tx + 6
        self.text(x, m + 16, 'PLANET EARF', size=7.2, weight=700, spacing=0.9)
        self.text(x, m + 23, 'A listening bar for San Francisco', size=3.0)
        self.text(x, m + 28, 'EARF  ·  earf.world', size=2.6, fill=GREY)
        y = m + 40
        self.line(tx, y - 5, self.w - m, y - 5, sw=0.2)
        self.text(x, y, 'STATUS', size=2.2, weight=600, spacing=0.4, fill=GREY)
        y = self.lines_of(x, y + 5, ['Proposal, not for construction.', 'Every dimension and choice is a working',
                                     'assumption for the owner to overturn.', 'Not reviewed by an architect, an',
                                     'engineer or the building official.'], size=2.6)
        y += 4
        self.text(x, y, 'SITE (ASSUMED)', size=2.2, weight=600, spacing=0.4, fill=GREY)
        y = self.lines_of(x, y + 5, site or ["A ground floor 35'-0\" x 80'-0\" inside the", 'walls: 2,800 sq ft. Existing shell,',
                                             "15'-9\" to the joists, one street front,", 'a rear yard with a side passage to',
                                             'the street. No site chosen.'], size=2.6)
        y += 4
        for n in notes:
            self.text(x, y, n[0], size=2.2, weight=600, spacing=0.4, fill=GREY)
            y = self.lines_of(x, y + 5, n[1], size=2.6) + 4
        # the sheet index, and this sheet's number
        yb = self.h - m - 92
        self.line(tx, yb, self.w - m, yb, sw=0.2)
        self.text(x, yb + 7, 'SHEETS', size=2.2, weight=600, spacing=0.4, fill=GREY)
        yy = yb + 13
        for n, t in sheet_list:
            w = 600 if n == number else 400
            self.text(x, yy, n, size=2.7, weight=w)
            self.text(x + 16, yy, t, size=2.7, weight=w)
            yy += 4.6
        self.text(x, self.h - m - 36, 'ISSUE', size=2.2, weight=600, spacing=0.4, fill=GREY)
        self.text(x, self.h - m - 31, 'Round 42 · 31 October 2026 · rev A', size=2.7)
        self.line(tx, self.h - m - 26, self.w - m, self.h - m - 26, sw=0.35)
        self.text(x, self.h - m - 17, title, size=4.0, weight=600)
        self.text(x, self.h - m - 11, subtitle, size=2.6, fill=GREY)
        self.text(self.w - m - 6, self.h - m - 8, number, size=9.0, weight=700, anchor='end')
        return tx

    def scale_bar(self, x, y, S, feet=(0, 4, 8, 16, 32), label="1/4\" = 1'-0\""):
        """A bar in feet at S paper mm per metre."""
        u = 0.3048 * S
        for i in range(len(feet) - 1):
            a, b = feet[i] * u, feet[i + 1] * u
            self.rect(x + a, y, x + b, y + 1.6, fill=INK if i % 2 == 0 else PAPER, sw=0.18)
        for f in feet:
            self.text(x + f * u, y + 5.2, f"{f}'", size=2.3, anchor='middle')
        self.text(x, y - 2.0, label, size=2.5, weight=600)

    def north(self, x, y, r=6.0, rot=0.0):
        a = math.radians(rot)
        def P(u, v):
            return x + u * math.cos(a) - v * math.sin(a), y + u * math.sin(a) + v * math.cos(a)
        self.circle(x, y, r, sw=0.25)
        self.poly([P(0, -r * 0.9), P(r * 0.35, r * 0.5), P(0, r * 0.2), P(-r * 0.35, r * 0.5)], fill=INK, sw=0.1)
        tx, ty = P(0, -r - 2.5)
        self.text(tx, ty, 'N', size=3.0, weight=700, anchor='middle')

    def section_mark(self, x, y, letter, sheet, direction):
        """A section cut's bubble; direction a unit vector on the paper for the arrow (where it looks)."""
        dx, dy = direction
        self.poly([(x + dx * 7.5, y + dy * 7.5), (x - dy * 3.2, y + dx * 3.2), (x + dy * 3.2, y - dx * 3.2)], fill=INK, sw=0.1)
        self.circle(x, y, 4.6, fill=PAPER, sw=0.3)
        self.line(x - 4.6, y, x + 4.6, y, sw=0.2)
        self.text(x, y - 1.0, letter, size=3.4, weight=700, anchor='middle')
        self.text(x, y + 3.4, sheet, size=2.0, anchor='middle')

    def tag(self, x, y, s, size=2.6, weight=600, spacing=0.5, fill=INK, anchor='middle'):
        self.text(x, y, s.upper(), size=size, weight=weight, spacing=spacing, anchor=anchor, fill=fill)


class Frame:
    """A drawing's world-to-paper map: metres (a, b) in its own frame to paper (x, y), b up the page."""
    def __init__(self, ox, oy, S):
        self.ox, self.oy, self.S = ox, oy, S

    def __call__(self, a, b):
        return self.ox + a * self.S, self.oy - b * self.S

    def r(self, sh, a0, b0, a1, b1, **k):
        x0, y0 = self(a0, b0); x1, y1 = self(a1, b1)
        sh.rect(x0, y0, x1, y1, **k)

    def l(self, sh, a0, b0, a1, b1, **k):
        x0, y0 = self(a0, b0); x1, y1 = self(a1, b1)
        sh.line(x0, y0, x1, y1, **k)

    def c(self, sh, a, b, r, **k):
        x, y = self(a, b)
        sh.circle(x, y, r * self.S, **k)

    def p(self, sh, pts, **k):
        sh.poly([self(a, b) for a, b in pts], **k)

    def t(self, sh, a, b, s, **k):
        x, y = self(a, b)
        sh.text(x, y, s, **k)

    def tag(self, sh, a, b, s, **k):
        x, y = self(a, b)
        sh.tag(x, y, s, **k)

    def door(self, sh, hinge, leaf, opens, w, sw=0.18):
        """A door in plan: hinge point, the closed leaf's direction (unit, along the wall) and the side it opens to
        (unit, normal to the wall): draws the open leaf and its swing."""
        hx, hy = hinge; lx, ly = leaf; ox, oy = opens
        a0 = self(hx + lx * w, hy + ly * w)
        a1 = self(hx + ox * w, hy + oy * w)
        h = self(hx, hy)
        sh.line(h[0], h[1], a1[0], a1[1], sw=0.3)
        r = w * self.S
        # sweep: from the closed leaf to the open one; the sign from the cross product on the paper
        cr = (a0[0] - h[0]) * (a1[1] - h[1]) - (a0[1] - h[1]) * (a1[0] - h[0])
        sh.path(f'M{a0[0]:.2f},{a0[1]:.2f} A{r:.2f},{r:.2f} 0 0 {1 if cr > 0 else 0} {a1[0]:.2f},{a1[1]:.2f}',
                sw=0.13, dash='1.2 0.8')

    def dim(self, sh, a0, b0, a1, b1, off, text=None, size=2.5):
        """A dimension between two world points, its line `off` paper mm to the left of the direction a->b."""
        p, q = self(a0, b0), self(a1, b1)
        dx, dy = q[0] - p[0], q[1] - p[1]
        Ln = math.hypot(dx, dy)
        if Ln < 1e-6:
            return
        ux, uy = dx / Ln, dy / Ln
        nx, ny = uy, -ux                                 # left of the direction on the paper (y down)
        P2 = (p[0] + nx * off, p[1] + ny * off); Q2 = (q[0] + nx * off, q[1] + ny * off)
        s = 1 if off > 0 else -1
        for A, B in ((p, P2), (q, Q2)):
            sh.line(A[0] + nx * s * 1.0, A[1] + ny * s * 1.0, B[0] + nx * s * 1.4, B[1] + ny * s * 1.4, sw=0.12)
        sh.line(P2[0], P2[1], Q2[0], Q2[1], sw=0.13)
        for A in (P2, Q2):                               # architectural ticks
            sh.line(A[0] - 1.1 * (ux + nx) * 0.7, A[1] - 1.1 * (uy + ny) * 0.7, A[0] + 1.1 * (ux + nx) * 0.7,
                    A[1] + 1.1 * (uy + ny) * 0.7, sw=0.3)
        m = ((P2[0] + Q2[0]) / 2 + nx * 1.4 * s, (P2[1] + Q2[1]) / 2 + ny * 1.4 * s)
        ang = math.degrees(math.atan2(uy, ux))
        if ang > 90.1 or ang < -89.9:
            ang += 180
        txt = text if text is not None else ftin(math.hypot(a1 - a0, b1 - b0))
        if s < 0:
            m = (m[0] - nx * 1.6, m[1] - ny * 1.6)
        sh.text(m[0], m[1], txt, size=size, anchor='middle', rot=ang, base='middle' if False else 'auto')
