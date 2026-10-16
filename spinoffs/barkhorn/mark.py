"""EARF's mark: the acrylic globe in colour, and the seamed discs in black, in white and in each speaker's colour (round 27).

The owner, 2026-10-16: "Let's go with the acrylic globe and have a color version, a black version, and a white version,
and a version for each speaker", and then: "I like discs for monochrome and acrylic for multicolor". This writes that
set, the files a printer, a maker or a web page takes (earth.py draws them: the colour is round 25's acrylic, the rest
round 24b's discs in one colour, seamed):

    brand/mark/earf-globe-colour.svg      the acrylic, the six speakers' tints together
    brand/mark/earf-globe-black.svg       the discs in one ink, for paper, print, an etch or an emboss
    brand/mark/earf-globe-white.svg       the discs in one ink, out of dark grounds and photographs
    brand/mark/earf-globe-01-flare.svg    to 08-smoke: the discs in each speaker's colour, flat, each shown on the ground
                                          where it holds 3:1 (Flare, Poison, Haze, Smoke on light; Dust, Acid, Ice, Fog on dark)
    brand/mark/earf-lockup-<colour|colour-ink|black|white>.svg   the globe beside EARF
    and a PNG of each, transparent: the globes 1024 px square, the lockups 2048 px wide

After the brand critic's round (critic/rounds/2026-10-16/brand-mark-r1.json), small sizes have their own files:

    brand/mark/small/earf-globe-<black|white>-<64|32|16>.svg   the one-ink small cuts (the seams wider), each for marks
                                                               up to that many px across (17, 8.5 and 4.2 mm in print)
    brand/mark/small/earf-lockup-<black|white>-<64|32>.svg      the lockups whose globe is that small
    each with a PNG at its size (the lockups' globe at that size)

and two rules: the discs (black, white and the speakers', the small cut drawn in their colour) above 64 px the
master, at 64 px and under the small cut for that size; the colour never below 24 px (6.4 mm), where the small black
(on light grounds) or white (on dark) stands in.

    python3 spinoffs/barkhorn/mark.py [--sheet PATH] [--sizes PATH]   also a sheet of the set, each on its ground, and
                                                                      a sheet of sizes (300, 64, 32 and 16 px)
"""
import argparse, os, subprocess, sys, tempfile

import numpy as np
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import earth as E                                        # noqa: E402
import marks as M                                        # noqa: E402

OUT = os.path.join(HERE, 'brand', 'mark')
SPEAKERS = [(num, name, colour) for key, line, num, name, colour in M.SPEAKERS if line == 'Cloud']


def _contrast(a, b):
    """WCAG's contrast ratio of two colours."""
    la, lb = sorted((float(np.dot([0.2126, 0.7152, 0.0722], E._lin(c))) for c in (a, b)), reverse=True)
    return (la + 0.05) / (lb + 0.05)


def ground(colour):
    """A flat colour's ground: paper where it holds 3:1 there (WCAG's least for graphics), else ink."""
    return E.PAPER if _contrast(colour, E.PAPER) >= 3 else E.NIGHT


# each version: its style, its colours and the ground it shows on (the files themselves have none). Round 27, the owner:
# "I like discs for monochrome and acrylic for multicolor"
GLOBES = [('colour', 'Colour', 'acrylic', E.RING, E.PAPER), ('black', 'Black', 'discs', E.INK, E.PAPER),
          ('white', 'White', 'discs', E.WHITE, E.NIGHT)] + \
         [(f'{num}-{name.lower()}', f'{num} {name}', 'discs', colour, ground(colour)) for num, name, colour in SPEAKERS]
LOCKUPS = [('colour', 'acrylic', E.RING, E.INK, 'paper'), ('colour-ink', 'acrylic', E.RING, E.WHITE, 'night'),
           ('black', 'discs', E.INK, E.INK, 'paper'), ('white', 'discs', E.WHITE, E.WHITE, 'night')]
INKS = [('black', E.INK, 'paper'), ('white', E.WHITE, 'night')]
MIN_PX = 24                                               # the colour and the speakers': never smaller (the critic's rule)
LOCK_W = (450 + 110 + M.WORDMARK_W) / 450                 # a lockup's width over its globe's


def write():
    os.makedirs(OUT, exist_ok=True)
    files = []
    for tag, title, style, cols, bg in GLOBES:
        f = os.path.join(OUT, f'earf-globe-{tag}.svg')
        open(f, 'w').write(E.mark_svg(style, cols, label=f'EARF globe, {title.lower()}',
                                      ground='night' if bg == E.NIGHT else 'paper'))
        files.append((f, ['-w', '1024', '-h', '1024']))
    for tag, style, cols, word, g in LOCKUPS:
        f = os.path.join(OUT, f'earf-lockup-{tag}.svg')
        open(f, 'w').write(E.lockup_svg(style, cols, word, ground=g))
        files.append((f, ['-w', '2048']))
    os.makedirs(os.path.join(OUT, 'small'), exist_ok=True)
    for tag, ink, g in INKS:
        for px in sorted(E.SMALL_SEAM, reverse=True):
            f = os.path.join(OUT, 'small', f'earf-globe-{tag}-{px}.svg')
            open(f, 'w').write(E.mark_svg('discs', ink, label=f'EARF globe, {tag}, up to {px} px', ground=g, px=px))
            files.append((f, ['-w', str(px), '-h', str(px)]))
        for px in (64, 32):
            f = os.path.join(OUT, 'small', f'earf-lockup-{tag}-{px}.svg')
            open(f, 'w').write(E.lockup_svg('discs', ink, ink, ground=g, px=px))
            files.append((f, ['-w', str(round(px * LOCK_W))]))
    for f, size in files:
        subprocess.run(['rsvg-convert', *size, f, '-o', f[:-4] + '.png'], check=True)
    return [f for f, _ in files]


def _png(svg, px, bg):
    """An SVG (a path, or the markup itself) at px square on bg."""
    tmp = None
    if svg.lstrip().startswith('<'):
        with tempfile.NamedTemporaryFile('w', suffix='.svg', delete=False) as f:
            f.write(svg); tmp = svg = f.name
    with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as t:
        subprocess.run(['rsvg-convert', '-w', str(px), '-h', str(px), '-b', bg, svg, '-o', t.name], check=True)
        im = Image.open(t.name).convert('RGB')
    os.unlink(t.name)
    if tmp:
        os.unlink(tmp)
    return im


def sizes(path):
    """Each version at 300, 64, 32 and 16 px, as it is meant to be used: the discs (black, white and the speakers') in
    their small cuts at 64 px and under, in their own colour; the colour down to 24 px, and below it the small black or
    white."""
    font = ImageFont.truetype('DejaVuSans.ttf', 15)
    small_font = ImageFont.truetype('DejaVuSans.ttf', 11)
    rows, cols = GLOBES, (300, 64, 32, 16)
    cw, rh, lw, pad = [330, 110, 90, 80], 330, 130, 15
    sheet = Image.new('RGB', (lw + sum(cw) + pad, len(rows) * rh + 40), '#DEDCD7')
    d = ImageDraw.Draw(sheet)
    for i, px in enumerate(cols):
        d.text((lw + sum(cw[:i]) + 10, 12), f'{px} px', fill='#57534C', font=font)
    for r, (tag, title, style, cols_, bg) in enumerate(rows):
        y = 40 + r * rh
        d.rectangle([pad, y, lw + sum(cw) - 5, y + rh - 10], fill=bg)
        d.text((pad + 10, y + 12), title, fill='#ECE8E1' if bg == E.NIGHT else '#1C1A18', font=font)
        ink = next((t for t, c, g in INKS if (c == E.WHITE) == (bg == E.NIGHT)), 'black')
        for i, px in enumerate(cols):
            note = ''
            if style == 'discs' and px <= 64:
                svg = E.mark_svg('discs', cols_, px=px)
            elif px < MIN_PX:
                svg, note = os.path.join(OUT, 'small', f'earf-globe-{ink}-{px}.svg'), f'{ink}: min {MIN_PX} px'
            else:
                svg = os.path.join(OUT, f'earf-globe-{tag}.svg')
            im = _png(svg, px, bg)
            x = lw + sum(cw[:i]) + (cw[i] - px) // 2
            sheet.paste(im, (x, y + (rh - 10 - px) // 2))
            for k, line in enumerate(note.split(': ') if note else []):    # under the cell, centred: the ink, then the rule
                tx = lw + sum(cw[:i]) + (cw[i] - d.textlength(line, font=small_font)) / 2
                d.text((tx, y + rh / 2 + 22 + 14 * k), line, fill='#A39E95' if bg == E.NIGHT else '#57534C', font=small_font)
    sheet.save(path)


def sheet(path):
    """The set on one sheet, each globe on its ground (storyboard.py's svgs)."""
    args = [f'{title}={os.path.join(OUT, f"earf-globe-{tag}.svg")}@{bg}' for tag, title, style, cols, bg in GLOBES]
    subprocess.run([sys.executable, os.path.join(HERE, 'storyboard.py'), 'svgs', *args, '--cols', '6', '--out', path], check=True)


if __name__ == '__main__':
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    ap.add_argument('--sheet', help='also a sheet of the set, each on its ground, to this path')
    ap.add_argument('--sizes', help='also a sheet of the sizes, to this path')
    a = ap.parse_args()
    fs = write()
    print(f'{len(fs)} SVGs and PNGs in', os.path.relpath(OUT, HERE))
    if a.sheet:
        sheet(a.sheet)
        print(a.sheet)
    if a.sizes:
        sizes(a.sizes)
        print(a.sizes)
