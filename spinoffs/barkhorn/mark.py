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

Round 27e (the owner: "Maybe if we add a spinning animation like a top it will help") adds the mark in motion and a
study of its angle:

    brand/mark/earf-globe-<black|colour>-spin.<mp4|webm>   the globe spinning on its axis, 4-second loops (round 27f:
                                                          the steady spin, chosen over the top's wobble)
    python3 spinoffs/barkhorn/mark.py --spin [TAG ...] [--spin-sheet PATH] [--angles PATH]

Round 27i adds each globe in line, beside the fills (the owner: "Can we also do stroke versions of these"):

    brand/mark/earf-globe-<tag>-stroke.svg                   the colour as its six rims, the rest as the discs' edges
    brand/mark/small/earf-globe-<black|white>-stroke-64.svg  the heavier cut for 64 px (under it, the fills' small cuts)
    python3 spinoffs/barkhorn/mark.py --stroke-sheet PATH
"""
import argparse, os, subprocess, sys, tempfile

import numpy as np
from PIL import Image, ImageDraw, ImageFont
from shapely.geometry import Point, Polygon
from shapely.ops import unary_union

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
# Round 27i (the owner: "Can we also do stroke versions of these in addition to fill, or will that not work?"): each
# version again in line (earth.mark_svg's strokes), beside the fills: the colour as its six rims, the rest as the
# discs' visible edges in their one colour. Above 64 px the master, at 64 px the heavier small cut, and under 64 px the
# fill's own small cuts stand in.
STROKES = [(f'{tag}-stroke', f'{title}, in line', 'strokes', cols, bg) for tag, title, style, cols, bg in GLOBES]
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
    for tag, title, style, cols, bg in STROKES:
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
        for px in sorted(E.STROKE['small'], reverse=True):
            f = os.path.join(OUT, 'small', f'earf-globe-{tag}-stroke-{px}.svg')
            open(f, 'w').write(E.mark_svg('strokes', ink, label=f'EARF globe, {tag}, in line, up to {px} px', ground=g, px=px))
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


def sheet(path, rows=GLOBES):
    """The set on one sheet, each globe on its ground (storyboard.py's svgs); rows=STROKES for the set in line."""
    args = [f'{title}={os.path.join(OUT, f"earf-globe-{tag}.svg")}@{bg}' for tag, title, style, cols, bg in rows]
    subprocess.run([sys.executable, os.path.join(HERE, 'storyboard.py'), 'svgs', *args, '--cols', '6', '--out', path], check=True)


# Round 27e. The owner, of the one-colour discs untrimmed: "I kind of like it untrimmed because it's true to the shape
# of the combined discs. Maybe the angle Is wrong. Maybe if we add a spinning animation like a top it will help." So the
# mark spins on its axis as a top does: the meridians turn about the pole, the Earth's way (west to east, the front
# going right), while the parallels, round it, stay. `rate` degrees a second (a turn in 8 s); each loop `turn` degrees,
# the least that brings every disc of the colour back to its own place (one colour repeats every 60). The top's own
# version wobbles: its axis runs once a loop round a circle `wobble` degrees across that starts and ends at rest, so
# the loop still begins on the mark as it stands. In motion no part is dropped (earth.disc_shapes' `keep`). Each frame
# keeps the mark's clear space, `clear` of the globe's width on every side (the rule on the mark's page). Round 27f:
# the owner chose the steady spin, so the top's (its lean moving off the Earth's) is no longer made; `wobble` stays,
# should it come back (a SPINS entry with it as its last value).
SPIN = dict(rate=45.0, turn=180.0, fps=30, px=720, wobble=5.0, clear=0.25)
SPINS = [('black', 'discs', E.INK, E.PAPER, 0.0), ('colour', 'acrylic', E.RING, E.PAPER, 0.0)]


def _wobble(beta, f):
    """The axis's lean off its rest at `f` of the loop: round a circle `beta` degrees across through rest, the way it
    spins. As earth.WOBBLE: degrees, and the direction (radians) the axis turns about."""
    p = 2 * np.pi * f
    d1, d2 = beta / 2 * (1 - np.cos(p)), -beta / 2 * np.sin(p)      # toward e1 (us) and e2 (across), from rest
    return [float(np.hypot(d1, d2)), float(np.arctan2(d2, d1) + np.pi / 2)]


def spin_svg(style, cols, bg, spin, wobble=(0.0, 0.0), keep=0, clear=None):
    """One frame: the mark turned `spin` degrees on its axis, its axis leaning as `wobble` (earth.WOBBLE); with `clear`,
    framed with that share of the globe's width clear on every side, else as mark_svg frames it."""
    if abs(spin % 60 - 30) < 1e-3:                       # a meridian exactly edge on drops out of facets (it hides nothing,
        spin += 2e-3                                     # but its seam is lost for a frame); a hair past, it is the line
    E.WOBBLE[:] = wobble
    try:
        body = (E.acrylic_body(cols, 'night' if bg == E.NIGHT else 'paper', spin=spin) if style == 'acrylic' else
                E.discs_body([cols] * 6, spin=spin, flush=False, keep=keep))
    finally:
        E.WOBBLE[:] = [0.0, 0.0]
    e = 1 + 2 * clear if clear else 1 + E.W_LINE / 2
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{-e:.4f} {-e:.4f} {2 * e:.4f} {2 * e:.4f}">'
            f'<rect x="{-e:.4f}" y="{-e:.4f}" width="{2 * e:.4f}" height="{2 * e:.4f}" fill="{bg}"/>{body}</svg>')


def _spin_frame(job):
    path, style, cols, bg, turned, wobble = job
    open(path[:-4] + '.svg', 'w').write(spin_svg(style, cols, bg, turned, wobble, clear=SPIN['clear']))
    subprocess.run(['rsvg-convert', '-w', str(SPIN['px']), '-h', str(SPIN['px']), path[:-4] + '.svg', '-o', path], check=True)
    os.unlink(path[:-4] + '.svg')


def spin(out=OUT, only=()):
    """The spins, each a seamless loop: brand/mark/earf-globe-<tag>-spin.mp4 (H.264, for Safari and every player) and
    .webm (VP9, half the size, for the browsers built without H.264)."""
    from multiprocessing import Pool
    n = round(SPIN['turn'] / SPIN['rate'] * SPIN['fps'])
    files = []
    for tag, style, cols, bg, beta in SPINS:
        if only and tag not in only:
            continue
        with tempfile.TemporaryDirectory() as tmp:
            jobs = [(os.path.join(tmp, f'f{i:04d}.png'), style, cols, bg, SPIN['turn'] * i / n, _wobble(beta, i / n))
                    for i in range(n)]
            with Pool() as pool:
                pool.map(_spin_frame, jobs)
            src = ['ffmpeg', '-v', 'error', '-y', '-framerate', str(SPIN['fps']), '-i', os.path.join(tmp, 'f%04d.png')]
            f = os.path.join(out, f'earf-globe-{tag}-spin')
            subprocess.run(src + ['-c:v', 'libx264', '-preset', 'slow', '-crf', '18', '-tune', 'animation', '-pix_fmt', 'yuv420p',
                                  '-movflags', '+faststart', f + '.mp4'], check=True)
            subprocess.run(src + ['-c:v', 'libvpx-vp9', '-b:v', '0', '-crf', '30', '-row-mt', '1', '-pix_fmt', 'yuv420p',
                                  '-fflags', '+bitexact', '-flags:v', '+bitexact', f + '.webm'], check=True)   # (no random ids)
            files += [f + '.mp4', f + '.webm']
    return files


def spin_sheet(path, every=0.4):
    """The spins on one sheet, a frame `every` seconds across each loop, drawn as the videos are."""
    font, small = ImageFont.truetype('DejaVuSans.ttf', 15), ImageFont.truetype('DejaVuSans.ttf', 12)
    secs = SPIN['turn'] / SPIN['rate']
    ts = [k * every for k in range(round(secs / every))]
    px, lw = 160, 130
    sheet = Image.new('RGB', (lw + len(ts) * (px + 6), 10 + len(SPINS) * (px + 28)), '#DEDCD7')
    d = ImageDraw.Draw(sheet)
    for r, (tag, style, cols, bg, beta) in enumerate(SPINS):
        y = 10 + r * (px + 28)
        d.text((12, y + px // 2 - 8), tag.replace('-top', ', as a top'), fill='#1C1A18', font=font)
        for i, t in enumerate(ts):
            f = t / secs
            svg = spin_svg(style, cols, bg, SPIN['turn'] * f, _wobble(beta, f), clear=SPIN['clear'])
            sheet.paste(_png(svg, px, bg), (lw + i * (px + 6), y))
            d.text((lw + i * (px + 6), y + px + 4), f'{t:.1f} s', fill='#57534C', font=small)
    sheet.save(path)


def tips(spin=0.0):
    """How far the tips reach, of the radius: the discs' edges past the largest disc, where they meet the globe's
    outline."""
    discs = [Polygon(g['pts'][:, :2]).buffer(0) for g in E.rings(spin)]
    big = max(discs, key=lambda d: d.area)
    out = unary_union(discs).difference(big)
    return max((big.exterior.distance(Point(c)) for p in getattr(out, 'geoms', [out]) if p.area > 2e-4
                for c in p.exterior.coords), default=0.0)


def angles(path):
    """Round 27e's angle study: the one-colour discs turned on their axis through 60 degrees (all there is before they
    repeat), then the tip toward us from 10 to 28 degrees in one colour and in colour (the lean only turns the picture,
    so it is not here); under each, how far the tips reach past the largest disc. (Round 27f's tip, 16, among them.)"""
    font, small = ImageFont.truetype('DejaVuSans.ttf', 15), ImageFont.truetype('DejaVuSans.ttf', 12)
    px, cw, lw = 230, 250, 200
    rows = [('Turned on its axis', [(s, E.ELEV, 'discs') for s in (0, 10, 20, 30, 40, 50)]),
            ('Tipped toward us', [(0, t, 'discs') for t in (10, 13, 16, 19, 22, 28)]),
            ('Tipped, in colour', [(0, t, 'acrylic') for t in (10, 13, 16, 19, 22, 28)])]
    sheet = Image.new('RGB', (lw + 6 * cw, 20 + len(rows) * (px + 64)), '#DEDCD7')
    d = ImageDraw.Draw(sheet)
    for r, (title, cells) in enumerate(rows):
        y = 20 + r * (px + 64)
        d.text((16, y + px // 2 - 8), title, fill='#1C1A18', font=font)
        for i, (s, t, style) in enumerate(cells):
            tilt = [t - E.ELEV, np.pi / 2]                # another tip: the whole globe turned about e2, across the picture
            svg = spin_svg(style, E.RING if style == 'acrylic' else E.INK, E.PAPER, s, tilt, keep=1.5)   # as it stands
            E.WOBBLE[:] = tilt
            reach = tips(s)
            E.WOBBLE[:] = [0.0, 0.0]
            x = lw + i * cw
            sheet.paste(_png(svg, px, E.PAPER), (x, y))
            now = s == 0 and t == E.ELEV
            d.text((x, y + px + 6), (f'turned {s}°' if r == 0 else f'tip {t}°') + (' (now)' if now else ''),
                   fill='#1C1A18', font=font)
            d.text((x, y + px + 26), f'tips reach {reach:.2f} of the radius', fill='#57534C', font=small)
    sheet.save(path)



# Round 27g's study. The owner: "What would it look like if the lateral discs intersected like the longitudinal discs
# do? Did you try a version where the three stacked discs are instead the same layout as the three equal sized
# intersecting discs?" (Not before: round 21's orbits were eight meridians, round 23's gyroscope two rings on two axes.)
# The lateral discs become great circles through the globe's side axis (earth.LATERAL), as the meridians go through the
# pole. Turned on its side, the meridians' layout keeps its disc facing you, and that disc is the green one, so the two
# layouts share it and only two discs are new (five in all); any three lateral discs 60 degrees apart must have one
# nearly facing you, so a second set of its own competes with the green.
LATERALS = [('Now: three parallels, stacked', None),
            ("The meridians' layout on its side: shares the green, five discs", (30, None, -30)),
            ('On its side, the blue equator kept: six discs', (30, 0, -30)),
            ('A second set of three, 60 degrees apart: six discs', (60, 0, -60))]
# Round 27h (the owner asked again): in those the side axis lies across the picture, so the lateral discs cross on the
# outline itself, where the meridians cross inside it. Turned TURN degrees on the axis (round 27f's 16 degree tip, seen
# from the side), the side axis's end comes toward you as far as the pole does, so the lateral discs cross inside the
# outline too, upper left, as the meridians do upper right (the green then faces you turned that much). Each row: its
# title, the lateral tilts and the turn.
TURN = round(np.degrees(np.arcsin(np.sin(np.radians(E.ELEV)) / np.cos(np.radians(E.ELEV)))), 1)
LATERALS_TURNED = [('Now: three parallels, stacked', None, 0.0),
                   ('Crossing as the meridians do: five discs, the green shared', (30, None, -30), TURN),
                   ('The same with the blue equator kept: six discs', (30, 0, -30), TURN)]


def lateral(path, rows=LATERALS):
    """Round 27g's study (and 27h's, rows=LATERALS_TURNED): each layout in black and in colour, large and at 64 px,
    with its disc count and how far its tips reach."""
    font, small = ImageFont.truetype('DejaVuSans.ttf', 16), ImageFont.truetype('DejaVuSans.ttf', 12)
    px, sm, gap = 300, 64, 18
    w = gap + 2 * (px + gap) + 2 * (sm + gap) + gap
    sheet = Image.new('RGB', (w, len(rows) * (px + 52) + gap), '#DEDCD7')
    d = ImageDraw.Draw(sheet)
    for r, (title, lat, *turn) in enumerate(rows):
        turn = turn[0] if turn else 0.0
        y = gap + r * (px + 52)
        E.LATERAL = lat
        try:
            if turn:                                     # (spin_svg draws it turned; the small cut's seam by hand)
                small_disc = spin_svg('discs', E.INK, E.PAPER, turn, keep=1.5).replace(
                    E.discs_body([E.INK] * 6, spin=turn, flush=False), E.discs_body([E.INK] * 6, spin=turn, flush=False,
                                                                                   seam=E.SMALL_SEAM[64]))
                ims = [_png(spin_svg('discs', E.INK, E.PAPER, turn, keep=1.5), px, E.PAPER),
                       _png(spin_svg('acrylic', E.RING, E.PAPER, turn), px, E.PAPER),
                       _png(small_disc, sm, E.PAPER), _png(spin_svg('acrylic', E.RING, E.PAPER, turn), sm, E.PAPER)]
            else:
                ims = [_png(E.mark_svg('discs', E.INK), px, E.PAPER), _png(E.mark_svg('acrylic', E.RING), px, E.PAPER),
                       _png(E.mark_svg('discs', E.INK, px=sm), sm, E.PAPER), _png(E.mark_svg('acrylic', E.RING), sm, E.PAPER)]
            n = 6 if lat is None else sum(t is not None for t in lat) + 3
            reach = tips(turn)
        finally:
            E.LATERAL = None
        x = gap
        for i, im in enumerate(ims):
            sheet.paste(im, (x, y + (px - im.height) // 2 if i >= 2 else y))
            x += im.width + gap
        d.text((gap, y + px + 8), title, fill='#1C1A18', font=font)
        d.text((gap, y + px + 30), f'{n} discs; the tips reach {reach:.2f} of the radius', fill='#57534C', font=small)
    sheet.save(path)

if __name__ == '__main__':
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    ap.add_argument('--sheet', help='also a sheet of the set, each on its ground, to this path')
    ap.add_argument('--sizes', help='also a sheet of the sizes, to this path')
    ap.add_argument('--stroke-sheet', help="also a sheet of round 27i's set in line, to this path")
    ap.add_argument('--angles', help="also round 27e's angle study, to this path")
    ap.add_argument('--spin', nargs='*', help='also the spins (MP4 and WebM in brand/mark), or only those whose tags are named')
    ap.add_argument('--spin-sheet', help='also a sheet of the spins, a frame every 0.4 s, to this path')
    ap.add_argument('--lateral', help="also round 27g's study of the lateral discs as a second set, to this path")
    ap.add_argument('--lateral-turned', help="also round 27h's: the same crossing inside the outline, to this path")
    a = ap.parse_args()
    fs = write()
    print(f'{len(fs)} SVGs and PNGs in', os.path.relpath(OUT, HERE))
    if a.sheet:
        sheet(a.sheet)
        print(a.sheet)
    if a.sizes:
        sizes(a.sizes)
        print(a.sizes)
    if a.stroke_sheet:
        sheet(a.stroke_sheet, STROKES)
        print(a.stroke_sheet)
    if a.angles:
        angles(a.angles)
        print(a.angles)
    if a.spin is not None:
        for f in spin(only=a.spin):
            print(os.path.relpath(f, HERE))
    if a.spin_sheet:
        spin_sheet(a.spin_sheet)
        print(a.spin_sheet)
    if a.lateral:
        lateral(a.lateral)
        print(a.lateral)
    if a.lateral_turned:
        lateral(a.lateral_turned, LATERALS_TURNED)
        print(a.lateral_turned)
