"""The images on Planet EARF's screens (round 34): slow, mysterious pictures for the panels behind the frosted acrylic.
Each is drawn soft already; the panel's rough transmission softens it again, physically, in the render.

    python3 spinoffs/barkhorn/planet/loft/screens.py [OUT_DIR]      # default studio/assets/cache/planet_screens/

- hands: palms and fingers pressed against fogged glass from the far side, sharp and dark where they touch, the fog
  around them pale, a few runs of condensation;
- dancer: the silhouette of a woman dancing behind fog, one arm raised, her hair and skirt swung out;
- ovoid: an Arrival-like shell hanging in pale fog, dark and smooth, a little tilted;
- logogram: an ink ring on fog, broken and feathered, tendrils drifting off it.

Tasteful and suggestive, never explicit: shapes and shadows, no faces.
"""
import math, os, random, sys

from PIL import Image, ImageDraw, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(HERE))))
S = 1024


def fog(seed, lo=150, hi=215):
    """A pale fog: a soft vertical falloff and broad cloudy variation."""
    rnd = random.Random(seed)
    small = Image.new('L', (16, 16))
    for x in range(16):
        for y in range(16):
            small.putpixel((x, y), rnd.randint(lo, hi))
    im = small.resize((S, S), Image.BICUBIC).filter(ImageFilter.GaussianBlur(60))
    grad = Image.linear_gradient('L').resize((S, S)).point(lambda v: 235 - v // 6)
    return Image.blend(im, grad, 0.4)


def _blob(d, pts, w0, w1):
    """A stroke through pts tapering from w0 to w1, drawn as discs."""
    n = len(pts) - 1
    for k, ((x0, y0), (x1, y1)) in enumerate(zip(pts, pts[1:])):
        for t in range(16):
            u = (k + t / 15) / n; x, y = x0 + (x1 - x0) * t / 15, y0 + (y1 - y0) * t / 15
            w = w0 + (w1 - w0) * u
            d.ellipse([x - w, y - w, x + w, y + w], fill=255)


def hand(d, dc, cx, cy, sc, ang):
    """A hand pressed on the far side of fogged glass: the silhouette (d) and the contact pads (dc): the finger
    pads, the heel of the palm, the ball of the thumb."""
    ca, sa = math.cos(ang), math.sin(ang)
    def P(x, y):
        return (cx + sc * (x * ca - y * sa), cy + sc * (x * sa + y * ca))
    d.polygon([P(-0.38, -0.12), P(0.38, -0.12), P(0.43, 0.30), P(0.36, 0.68), P(0.16, 0.86), P(-0.18, 0.86),
               P(-0.38, 0.70), P(-0.45, 0.32)], fill=255)                      # the palm
    fingers = [(-0.30, -0.10, -0.42, -0.80, 0.085), (-0.10, -0.12, -0.13, -0.98, 0.090), (0.10, -0.12, 0.13, -0.94, 0.088),
               (0.29, -0.06, 0.42, -0.72, 0.078)]
    for x0, y0, x1, y1, w in fingers:
        _blob(d, [P(x0, y0), P((x0 + x1) / 2, (y0 + y1) / 2), P(x1, y1)], w * sc, w * sc * 0.82)
        tx, ty = P(x1 * 0.97, y1 * 0.95)
        r = w * sc * 0.75
        dc.ellipse([tx - r, ty - r * 1.2, tx + r, ty + r * 1.2], fill=255)                     # the pad
    _blob(d, [P(-0.36, 0.45), P(-0.62, 0.18), P(-0.80, -0.10)], 0.10 * sc, 0.075 * sc)        # the thumb
    tx, ty = P(-0.78, -0.08); r = 0.06 * sc; dc.ellipse([tx - r, ty - r, tx + r, ty + r], fill=255)
    for x, y, r in ((0.0, 0.62, 0.22), (-0.22, 0.30, 0.12), (0.22, 0.25, 0.10)):              # the heel, the mounts
        a, b = P(x, y); rr = r * sc
        dc.ellipse([a - rr, b - rr * 0.8, a + rr, b + rr * 0.8], fill=255)


def hands():
    base = fog(3)
    rnd = random.Random(4)
    sil = Image.new('L', (S, S), 0); ds = ImageDraw.Draw(sil)
    pad = Image.new('L', (S, S), 0); dp = ImageDraw.Draw(pad)
    hand(ds, dp, 400, 600, 260, -0.20)
    hand(ds, dp, 660, 500, 245, 0.16)
    halo = sil.filter(ImageFilter.GaussianBlur(45)).point(lambda v: v * 0.40)     # the fog wiped round them
    body = sil.filter(ImageFilter.GaussianBlur(3))                                 # pressed flat: crisp where it touches
    core = sil.filter(ImageFilter.MinFilter(9)).filter(ImageFilter.GaussianBlur(5))   # darker in the middle of the press
    out = Image.composite(Image.new('L', (S, S), 135), base, halo)
    out = Image.composite(Image.new('L', (S, S), 78), out, body)
    out = Image.composite(Image.new('L', (S, S), 50), out, core.point(lambda v: v * 0.8))
    d = ImageDraw.Draw(out)                                         # a few runs of condensation
    for _ in range(6):
        x = rnd.randint(330, 720); y = rnd.randint(810, 860); ln = rnd.randint(50, 140)
        d.line([(x, y), (x + rnd.randint(-4, 4), y + ln)], fill=rnd.randint(150, 175), width=rnd.randint(2, 4))
    return out.filter(ImageFilter.GaussianBlur(1.2))


def dancer():
    base = fog(7, 165, 225)
    sil = Image.new('L', (S, S), 0); d = ImageDraw.Draw(sil)
    cx = 500
    d.ellipse([cx - 34, 205, cx + 30, 290], fill=255)               # the head, turned and tilted
    _blob(d, [(cx - 30, 225), (cx - 110, 250), (cx - 175, 300)], 34, 10)       # the hair, swung out
    _blob(d, [(cx, 285), (cx + 4, 330)], 20, 22)                    # the neck
    _blob(d, [(cx - 5, 345), (cx + 10, 420), (cx + 5, 500)], 62, 48)           # the torso, a gentle S
    _blob(d, [(cx + 45, 350), (cx + 120, 285), (cx + 150, 190), (cx + 135, 120)], 20, 11)   # an arm raised
    _blob(d, [(cx - 45, 360), (cx - 120, 430), (cx - 215, 450), (cx - 270, 425)], 19, 10)   # the other, low
    d.polygon([(cx - 40, 490), (cx + 45, 488), (cx + 120, 600), (cx + 230, 720), (cx + 120, 760),
               (cx - 10, 780), (cx - 140, 760), (cx - 120, 650)], fill=255)  # the skirt, swinging
    _blob(d, [(cx - 30, 740), (cx - 45, 850), (cx - 70, 950)], 22, 12)          # the legs
    _blob(d, [(cx + 30, 745), (cx + 85, 840), (cx + 150, 920)], 21, 11)
    sil = sil.filter(ImageFilter.GaussianBlur(9))
    blur = sil.filter(ImageFilter.BoxBlur(0)).transform((S, S), Image.AFFINE, (1, 0, 18, 0, 1, 0))  # a trace of motion
    sil = Image.blend(sil, blur, 0.35)
    glow = sil.filter(ImageFilter.GaussianBlur(70)).point(lambda v: v * 0.5)
    out = Image.composite(Image.new('L', (S, S), 120), base, glow)
    return Image.composite(Image.new('L', (S, S), 40), out, sil.filter(ImageFilter.GaussianBlur(6)))


def ovoid():
    base = fog(11, 175, 228)
    sh = Image.new('L', (S, S), 0); d = ImageDraw.Draw(sh)
    pts = []
    for k in range(240):
        t = 2 * math.pi * k / 240
        x = 0.19 * math.cos(t) * (1 - 0.18 * math.sin(t)); y = 0.42 * math.sin(t)
        a = 0.16
        pts.append((S * 0.52 + S * (x * math.cos(a) - y * math.sin(a)), S * 0.44 + S * (x * math.sin(a) + y * math.cos(a))))
    d.polygon(pts, fill=255)
    sh = sh.filter(ImageFilter.GaussianBlur(8))
    tone = Image.linear_gradient('L').resize((S, S)).point(lambda v: 20 + v // 5)        # darker at the top
    out = Image.composite(tone, base, sh)
    fogfront = Image.linear_gradient('L').resize((S, S)).point(lambda v: max(0, v - 90) * 1.4)   # fog over its foot
    return Image.composite(Image.new('L', (S, S), 212), out, fogfront).filter(ImageFilter.GaussianBlur(2))


def logogram():
    base = fog(17, 180, 228)
    ink = Image.new('L', (S, S), 0); d = ImageDraw.Draw(ink)
    rnd = random.Random(19)
    cx, cy, r = S / 2, S / 2, 290
    for k in range(900):
        t = 2 * math.pi * k / 900
        if 0.9 < t < 1.2 or 3.95 < t < 4.05:
            continue
        w = 9 + 22 * abs(math.sin(2.5 * t + 0.7)) ** 3 + rnd.uniform(-2, 2)
        rr = r + 8 * math.sin(7 * t)
        x, y = cx + rr * math.cos(t), cy + rr * math.sin(t)
        d.ellipse([x - w, y - w, x + w, y + w], fill=255)
    for _ in range(14):                                              # tendrils and spatters, feathering out
        t = rnd.uniform(0, 2 * math.pi); x, y = cx + r * math.cos(t), cy + r * math.sin(t)
        heading = t + rnd.uniform(-0.6, 0.6)
        for s in range(rnd.randint(25, 70)):
            heading += rnd.uniform(-0.08, 0.08); x += math.cos(heading) * 3; y += math.sin(heading) * 3
            w = max(0.8, 9 - s * 0.15)
            d.ellipse([x - w, y - w, x + w, y + w], fill=255)
        for _ in range(rnd.randint(2, 6)):
            sx, sy = x + rnd.uniform(-30, 30), y + rnd.uniform(-30, 30); w = rnd.uniform(2, 6)
            d.ellipse([sx - w, sy - w, sx + w, sy + w], fill=255)
    ink = ink.filter(ImageFilter.GaussianBlur(4))
    bleed = ink.filter(ImageFilter.GaussianBlur(26)).point(lambda v: v * 0.5)
    out = Image.composite(Image.new('L', (S, S), 125), base, bleed)
    return Image.composite(Image.new('L', (S, S), 25), out, ink)


IMAGES = {'hands': hands, 'dancer': dancer, 'ovoid': ovoid, 'logogram': logogram}


def make(out=None):
    out = out or os.path.join(ROOT, 'studio', 'assets', 'cache', 'planet_screens')
    os.makedirs(out, exist_ok=True)
    paths = {}
    for k, fn in IMAGES.items():
        p = os.path.join(out, f'{k}.png')
        if not os.path.exists(p):
            fn().save(p)
        paths[k] = p
    return paths


if __name__ == '__main__':
    print(make(sys.argv[1] if len(sys.argv) > 1 else None))
