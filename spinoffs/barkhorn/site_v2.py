"""Round 48: the site audit's no-regret fixes (the coordinator, 2026-11-03; spinoffs/barkhorn/coordinator/
site-audit-2026-11-03 on r46-owner-notes 3480947a), applied to the built page while web.V2 is on. Off, web.py never
calls this and the page is byte for byte as before. Each change is an asserted replacement on the page web.py builds
(so a change in web.py that moves its target fails the build instead of passing silently), plus the CSS and script below.
HOME_V2 (also off) reorders the home as the audit's recommended "launch film"."""


class Page:
    def __init__(self, head, rest):
        self.head, self.rest = head, rest

    def sub(self, old, new, n=1, where='rest'):
        s = getattr(self, where)
        assert s.count(old) == n, ('site_v2: expected', n, 'got', s.count(old), old[:80])
        setattr(self, where, s.replace(old, new))

    def css(self, text):
        i = self.head.rindex('</style>')
        self.head = self.head[:i] + text + self.head[i:]


def pairings(p):
    """The owner's rule: on a product page, recommend only the other lines, never a speaker for a speaker (nor a lamp
    for a lamp). Monochromatic first (the same color in the other lines), then the complement, then the neighbors.
    The color pages keep the whole range."""
    p.sub("function picks(cols, pid, k, max = 4) {\n  const order = [...PRODUCTS.filter(x => x.id === pid), ...PRODUCTS.filter(x => x.id !== pid)], out = [];",
          "function picks(cols, pid, k, max = 4, others = false) {\n"
          "  const line = (PRODUCTS.find(x => x.id === pid) || {}).line;\n"
          "  const order = others ? PRODUCTS.filter(x => x.line !== line) : [...PRODUCTS.filter(x => x.id === pid), ...PRODUCTS.filter(x => x.id !== pid)], out = [];")
    p.sub("""      : `${names(r.comp)}, opposite on the color wheel. ${pair}`, picks(r.comp, pid, k)),""",
          """      : `${names(r.comp)}, opposite on the color wheel. ${pair}`, picks(r.comp, pid, k, 4, mono)),""")
    p.sub("""      : `${names(r.ana)}, either side of it on the wheel.`, picks(r.ana, pid, k))];
  if (mono) out.push(block(`${box.id}-mono`, 'Monochromatic', `${c.name} in the other lines.`, picks([k], pid, k)));""",
          """      : `${names(r.ana)}, either side of it on the wheel.`, picks(r.ana, pid, k, 4, mono))];
  if (mono) out.unshift(block(`${box.id}-mono`, 'Monochromatic', `${c.name} in the other lines.`, picks([k], pid, k, 4, true)));""")


def apply(web, head, rest):
    p = Page(head, rest)
    pairings(p)
    return p.head, p.rest
