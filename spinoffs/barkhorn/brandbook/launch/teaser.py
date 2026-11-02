"""EARF's teaser for the debut: a 25-second animatic built from the existing renders, in the brand's type.

    python3 teaser.py [--aspect 16x9|4x5] [--fps 25] [--out out/earf-teaser-16x9.mp4]

Silent: the music is a placeholder, a licensed track to be chosen (STORYBOARD.md). Every beat is a slow move on a still.
Tropos is always shown whole, its cover off (owner, 2026-10-31): the horn beat is a whole speaker, not the site's turn
sprite, whose frames crop the cabinet. Core is cordless: its stills come from the Brand Book (book/img), which carries
the lamps lane's cordless set; the site's lamps-orbs.jpg still shows cords. Frames are drawn with Pillow and encoded by ffmpeg.
The fonts (Instrument Sans, IBM Plex Mono; OFL) are fetched once from Google Fonts into ~/.cache/earf-fonts.
"""
import argparse, math, os, subprocess, urllib.request
from PIL import Image, ImageDraw, ImageFont, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
B = os.path.abspath(os.path.join(HERE, '..', '..'))
IMG = os.path.join(B, 'site', 'img')
BOOK = os.path.join(HERE, '..', 'book', 'img')   # cordless Core, whole Tropos
CACHE = os.path.expanduser('~/.cache/earf-fonts')
FONTS = {'sans400': 'https://fonts.gstatic.com/s/instrumentsans/v4/pximypc9vsFDm051Uf6KVwgkfoSxQ0GsQv8ToedPibnr-yp2JGEJOH9npSTF-Qf1.ttf',
         'sans600': 'https://fonts.gstatic.com/s/instrumentsans/v4/pximypc9vsFDm051Uf6KVwgkfoSxQ0GsQv8ToedPibnr-yp2JGEJOH9npSQb_gf1.ttf',
         'mono500': 'https://fonts.gstatic.com/s/ibmplexmono/v20/-F6qfjptAgt5VM-kVkqdyU8n3twJ8lc.ttf'}
PAPER, INK, NIGHT, NIGHT_INK, MUTED = (244, 241, 236), (28, 26, 24), (14, 13, 16), (237, 231, 221), (167, 159, 147)
TINTS = [('01', 'Ember', 'red'), ('02', 'Dust', 'orange'), ('03', 'Acid', 'amber'), ('04', 'Poison', 'green'),
         ('05', 'Ice', 'blue'), ('06', 'Haze', 'violet'), ('07', 'Fog', 'ice'), ('08', 'Smoke', 'black')]


def font(name, size):
    os.makedirs(CACHE, exist_ok=True)
    p = os.path.join(CACHE, name + '.ttf')
    if not os.path.exists(p):
        urllib.request.urlretrieve(FONTS[name], p)
    return ImageFont.truetype(p, size)


def ease(x):
    x = min(1.0, max(0.0, x))
    return x * x * (3 - 2 * x)


def cover(im, W, H, zoom=1.0, fx=0.5, fy=0.5):
    """The still cropped to fill W x H, zoomed by `zoom` about the point (fx, fy) of the image."""
    s = max(W / im.width, H / im.height) * zoom
    w, h = im.width * s, im.height * s
    x = min(max(fx * w - W / 2, 0), w - W); y = min(max(fy * h - H / 2, 0), h - H)
    box = (x / s, y / s, (x + W) / s, (y + H) / s)
    return im.resize((W, H), Image.LANCZOS, box=box)


class Teaser:
    def __init__(self, W, H):
        self.W, self.H = W, H
        u = H / 1080 if W >= H else W / 1080            # a unit that keeps type the same size on both crops
        self.u = u
        self.f_big = font('sans600', int(92 * u)); self.f_mid = font('sans600', int(58 * u))
        self.f_txt = font('sans400', int(30 * u)); self.f_mono = font('mono500', int(20 * u))
        load = lambda f: Image.open(os.path.join(IMG, f)).convert('RGB')
        self.studio = load('red-studio.jpg'); self.facade = load('facade.jpg'); self.hero = load('hero.jpg' if W > H else 'hero-portrait.jpg')
        book = lambda f: Image.open(os.path.join(BOOK, f)).convert('RGB')
        self.orbs = book('lamps-orbs.jpg'); self.mantle = load('tt-violet-dusk.jpg')
        self.horn = book('amber-studio-light.jpg')
        self.habitat = [load(f'{k}-habitat.jpg') for _, _, k in TINTS]
        word = Image.open(os.path.join(B, 'brand', 'mark', 'earf-wordmark-white.png')).convert('RGBA')
        self.word_w = word.resize((int(150 * u), int(150 * u * word.height / word.width)), Image.LANCZOS)
        wb = Image.open(os.path.join(B, 'brand', 'mark', 'earf-wordmark-black.png')).convert('RGBA')
        self.word_b = wb.resize(self.word_w.size, Image.LANCZOS)
        gdir = os.path.join(HERE, 'out', '_globe')
        if not os.path.isdir(gdir):
            os.makedirs(gdir)
            subprocess.run(['ffmpeg', '-v', 'error', '-i', os.path.join(IMG, 'globe-turn-night.mp4'), os.path.join(gdir, 'g%03d.png')], check=True)
        self.globe = [Image.open(os.path.join(gdir, f)).convert('RGB') for f in sorted(os.listdir(gdir))]
        # the beats: (start, end, draw); each crossfades 0.4 s into the next
        self.beats = [(0.0, 3.2, self.b_studio), (3.0, 7.7, self.b_turn), (7.5, 11.7, self.b_facade),
                      (11.5, 15.7, self.b_tints), (15.5, 18.7, self.b_lamps), (18.5, 21.7, self.b_hero), (21.5, 25.0, self.b_end)]
        self.length = 25.0

    # type
    def text(self, im, xy, s, f, fill, alpha=1.0, anchor='la'):
        if alpha <= 0:
            return
        layer = Image.new('RGBA', im.size, (0, 0, 0, 0)); d = ImageDraw.Draw(layer)
        d.text(xy, s, font=f, fill=fill + (int(255 * alpha),), anchor=anchor)
        im.paste(layer, (0, 0), layer)

    def line(self, im, s, t, t0, dark=True, big=False, y=None):
        """A line set low left, rising 12 px as it fades in from t0."""
        a = ease((t - t0) / 0.6); m = int(80 * self.u)
        f = self.f_big if big else self.f_mid
        lines = 1
        if f.getlength(s) > self.W - 2 * m and ', ' in s:      # too wide for the 4:5 crop: break at the last comma
            i = s.rindex(', ') + 1; s = s[:i] + '\n' + s[i + 1:]; lines = 2
        y = y if y is not None else self.H - m - int((92 if big else 58) * self.u) * lines
        self.text(im, (m, y + int(12 * self.u * (1 - a))), s, self.f_big if big else self.f_mid, NIGHT_INK if dark else INK, a)

    def label(self, im, s, dark=True, alpha=1.0, top=True):
        m = int(80 * self.u)
        self.text(im, (m, m if top else self.H - m), s.upper(), self.f_mono, MUTED if dark else (94, 90, 83), alpha, 'la' if top else 'ls')

    def mark(self, im, dark=True, alpha=1.0):
        w = self.word_w if dark else self.word_b
        layer = Image.new('RGBA', im.size, (0, 0, 0, 0)); m = int(80 * self.u)
        layer.paste(w, (self.W - m - w.width, m), w)
        if alpha < 1:
            layer.putalpha(layer.getchannel('A').point(lambda v: int(v * alpha)))
        im.paste(layer, (0, 0), layer)

    # the beats
    def b_studio(self, t):
        k = t / 3.2
        im = cover(self.studio, self.W, self.H, 1.0 + 0.10 * ease(k), 0.5, 0.5)
        if t < 0.9:
            im = Image.blend(Image.new('RGB', im.size, NIGHT), im, ease(t / 0.9))
        self.label(im, 'EARF · San Francisco', alpha=ease((t - 0.8) / 0.6))
        self.line(im, 'Eight colors, Ember to Smoke.', t, 1.3)   # the tagline stays once, on beat 6
        return im

    def b_turn(self, t):
        k = (t - 3.0) / 4.7
        # the whole speaker, cover off; a slow push of 4% about its center keeps it whole on both crops
        im = cover(self.horn, self.W, self.H, 1.0 + 0.04 * ease(k), 0.5, 0.5)
        self.label(im, 'Tropos · the horn, formed from its own acrylic', dark=False, alpha=ease((t - 3.4) / 0.6))
        self.line(im, 'The oldest amplifier is a shape.', t, 4.4, dark=False)
        return im

    def b_facade(self, t):
        k = (t - 7.5) / 4.2
        s = self.H / self.facade.height * 1.12
        w = int(self.facade.width * s)
        im = cover(self.facade, self.W, self.H, 1.12, 0.38 + 0.24 * ease(k), 0.55)
        self.line(im, 'Put a light under it.', t, 8.3)
        return im

    def b_tints(self, t):
        k = (t - 11.5) / 4.2
        n = min(7, int(k * 8)); kk = k * 8 - n
        im = cover(self.habitat[n], self.W, self.H, 1.04 + 0.05 * kk, 0.5, 0.55)
        no, name, _ = TINTS[n]
        m = int(80 * self.u)
        self.text(im, (m, self.H - m - int(58 * self.u)), f'{no}  {name}', self.f_mid, NIGHT_INK)
        self.label(im, 'Eight colors, each where it began')
        return im

    def b_lamps(self, t):
        k = (t - 15.5) / 3.2
        if k < 0.5:
            im = cover(self.orbs, self.W, self.H, 1.06 - 0.06 * ease(k * 2), 0.5, 0.5)
            self.label(im, 'Core · cordless', dark=False)
        else:
            im = cover(self.mantle, self.W, self.H, 1.0 + 0.06 * ease((k - 0.5) * 2), 0.5, 0.55)
            self.label(im, 'Mantle')
        self.line(im, 'Light, and a record player, in the same eight.', t, 15.9, dark=k >= 0.5)
        return im

    def b_hero(self, t):
        k = (t - 18.5) / 3.2
        im = cover(self.hero, self.W, self.H, 1.10 - 0.10 * ease(k), 0.5, 0.42)
        m = int(80 * self.u)
        a = ease((t - 19.0) / 0.7)
        tag = 'A world of sound, in color.'               # the tagline (owner, 2026-11-02); breaks only after its comma
        if self.f_mid.getlength(tag) > self.W - 2 * m:
            tag = 'A world of sound,\nin color.'
        self.text(im, (m, m + int(12 * self.u * (1 - a))), tag, self.f_mid, INK, a)
        self.label(im, 'Tropos · the eight, Ember to Smoke', dark=False, alpha=a, top=False)
        return im

    def b_end(self, t):
        k = (t - 21.5) / 3.5
        im = Image.new('RGB', (self.W, self.H), self.globe[0].getpixel((2, 2)))   # the globe film's own night
        g = self.globe[int((t - 21.5) * 30) % len(self.globe)]
        gs = int(self.H * 0.36); g = g.resize((gs, gs), Image.LANCZOS)
        im.paste(g, ((self.W - gs) // 2, int(self.H * 0.14)))
        cx = self.W // 2; a = ease((t - 21.9) / 0.6)
        w = self.word_w; layer = Image.new('RGBA', im.size, (0, 0, 0, 0))
        layer.paste(w, (cx - w.width // 2, int(self.H * 0.55)), w)
        layer.putalpha(layer.getchannel('A').point(lambda v: int(v * a))); im.paste(layer, (0, 0), layer)
        self.text(im, (cx, int(self.H * 0.66)), 'Tuesday 19 January 2027', self.f_mid, NIGHT_INK, ease((t - 22.3) / 0.6), 'ma')
        self.text(im, (cx, int(self.H * 0.66) + int(78 * self.u)), '[VENUE], SAN FRANCISCO  ·  EARF.WORLD', self.f_mono, MUTED, ease((t - 22.6) / 0.6), 'ma')
        self.text(im, (cx, self.H - int(60 * self.u)), 'EVERY PICTURE IS A RENDER  ·  ON THE NIGHT, THE REAL THING', self.f_mono, (110, 103, 94), ease((t - 23.0) / 0.6), 'ma')
        if t > 24.4:
            im = Image.blend(im, Image.new('RGB', im.size, (0, 0, 0)), ease((t - 24.4) / 0.6))
        return im

    def frame(self, t):
        live = [(s, e, f) for s, e, f in self.beats if s <= t < e]
        if len(live) == 1:
            return live[0][2](t)
        (s0, e0, f0), (s1, e1, f1) = live[0], live[-1]
        return Image.blend(f0(t), f1(t), ease((t - s1) / (e0 - s1)))


def main():
    a = argparse.ArgumentParser()
    a.add_argument('--aspect', default='16x9'); a.add_argument('--fps', type=int, default=25); a.add_argument('--out')
    a.add_argument('--stills', action='store_true', help='write one still per beat instead of the film')
    args = a.parse_args()
    W, H = {'16x9': (1920, 1080), '4x5': (1080, 1350)}[args.aspect]
    tz = Teaser(W, H)
    os.makedirs(os.path.join(HERE, 'out'), exist_ok=True)
    if args.stills:
        for i, t in enumerate([2.4, 5.6, 10.0, 12.2, 17.6, 20.8, 23.6]):
            tz.frame(t).save(os.path.join(HERE, 'out', f'teaser-{args.aspect}-beat{i + 1}.jpg'), quality=88)
        return
    out = args.out or os.path.join(HERE, 'out', f'earf-teaser-{args.aspect}.mp4')
    n = int(tz.length * args.fps)
    p = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(args.fps),
                          '-i', '-', '-c:v', 'libx264', '-preset', 'slow', '-crf', '23', '-pix_fmt', 'yuv420p', '-movflags', '+faststart', out],
                         stdin=subprocess.PIPE)
    for i in range(n):
        p.stdin.write(tz.frame(i / args.fps).tobytes())
    p.stdin.close(); p.wait()
    print('wrote', out, os.path.getsize(out) // 1024, 'KB')


if __name__ == '__main__':
    main()
