"""The colour globe matched to the speakers by measurement (2026-11-10, the owner on A2: "you need to assess each color
against the richer speaker colors").

Targets are the globe's colours AS RENDERED: each the OKLab midpoint of that speaker's horn and its cabinet's richest area
in the approved tallr6 fronts (the coordinator's measure). A colour is measured as the coordinator measured it: the pixels
in its OKLCH hue band with OKLab chroma over 0.05, and of those the top 40 % by chroma, their median linear RGB.

The loop renders small (globe_real.py, A2's look: translucent, the paper, the key at -90/30 and the fill, both at 1.0 in
every ray type, no emission), measures, moves each disc's input hue by the miss in OKLab, and repeats until every colour is
within TOL of its target or ROUNDS have run. An input that would leave sRGB keeps its hue and lightness at the gamut's
edge, and the disc's face is made denser instead (its depth, globe_real's face exponent). Then the final render.
No grading after the render.

    python3 spinoffs/barkhorn/globe_match.py OUT.png [--px 1024] [--samples 128]
    python3 spinoffs/barkhorn/globe_match.py --measure IMAGE.png
"""
import argparse, json, os, subprocess, sys

import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
TARGET = {'ember': '#B50404', 'dust': '#D35D17', 'acid': '#C5BC1E', 'poison': '#027614', 'ice': '#1169C1', 'haze': '#500CB4'}
BAND = {'ember': (15, 40), 'dust': (41, 78), 'acid': (92, 122), 'poison': (128, 158), 'ice': (225, 268), 'haze': (275, 322)}
START = {'ember': '#CF0913', 'dust': '#F78B34', 'acid': '#E4DE3C', 'poison': '#12AA24', 'ice': '#3C91EB',
         'haze': '#9F61E4'}                                  # A2's inputs (globe_real.TROPOS_LOGO)
TOL, ROUNDS, DEPTH0, DEPTH_STEP, DEPTH_MAX = 0.03, 8, 0.65, 0.2, 1.6
M1 = np.array([[0.4122214708, 0.5363325363, 0.0514459929], [0.2119034982, 0.6806995451, 0.1073969566],
               [0.0883024619, 0.2817188376, 0.6299787005]])
M2 = np.array([[0.2104542553, 0.7936177850, -0.0040720468], [1.9779984951, -2.4285922050, 0.4505937099],
               [0.0259040371, 0.7827717662, -0.8086757660]])


def lin(srgb):
    return np.where(srgb <= 0.04045, srgb / 12.92, ((srgb + 0.055) / 1.055) ** 2.4)


def enc(v):
    v = np.clip(v, 0, 1)
    return np.where(v <= 0.0031308, 12.92 * v, 1.055 * v ** (1 / 2.4) - 0.055)


def lab_of_lin(v):
    return (M2 @ (np.cbrt(M1 @ v.T))).T


def lin_of_lab(lab):
    lms = np.linalg.solve(M2, np.asarray(lab, float).T) ** 3
    return np.linalg.solve(M1, lms).T


def hexlin(h):
    return lin(np.array([int(h[i:i + 2], 16) for i in (1, 3, 5)]) / 255)


def hexof(v):
    return '#%02X%02X%02X' % tuple(int(round(255 * x)) for x in enc(v))


def measure(path):
    """Each colour's measured hex, as the coordinator measures it."""
    px = lin(np.asarray(Image.open(path).convert('RGB'), float).reshape(-1, 3) / 255)
    lab = lab_of_lin(px)
    c = np.hypot(lab[:, 1], lab[:, 2]); h = np.degrees(np.arctan2(lab[:, 2], lab[:, 1])) % 360
    out = {}
    for k, (lo, hi) in BAND.items():
        sel = (h >= lo) & (h <= hi) & (c > 0.05)
        if sel.sum() < 20:
            out[k] = None; continue
        cs = c[sel]; top = cs >= np.quantile(cs, 0.6)
        out[k] = hexof(np.median(px[sel][top], axis=0))
    return out


def dist(a, b):
    return float(np.linalg.norm(lab_of_lin(hexlin(a)[None])[0] - lab_of_lin(hexlin(b)[None])[0]))


def to_gamut(lab):
    """`lab` brought into sRGB at its hue and lightness (chroma eased back); returns (lab, chroma lost)."""
    L, a, b = lab; c0 = np.hypot(a, b)
    for k in np.linspace(1.0, 0.0, 201):
        v = lin_of_lab([L, a * k, b * k])
        if v.min() >= -1e-6 and v.max() <= 1 + 1e-6:
            return np.array([L, a * k, b * k]), c0 * (1 - k)
    return np.array([L, 0, 0]), c0


def render(hues, out, px, samples):
    hf = os.path.splitext(out)[0] + '.hues.json'
    json.dump(hues, open(hf, 'w'), indent=1)
    subprocess.run(['python3.11', os.path.join(HERE, 'globe_real.py'), '--still', out, '--px', str(px), '--samples',
                    str(samples), '--hues-file', hf, '--shine', '1', '1', '--neon', '0', '0', '--key-at', '-90', '30'],
                   check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def main():
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    ap.add_argument('out', nargs='?'); ap.add_argument('--px', type=int, default=1024); ap.add_argument('--samples', type=int, default=128)
    ap.add_argument('--measure'); ap.add_argument('--work', default='/tmp/globe-match')
    a = ap.parse_args()
    if a.measure:
        m = measure(a.measure)
        for k in TARGET:
            print(f'{k:7s} target {TARGET[k]}  measured {m[k]}  distance {dist(TARGET[k], m[k]):.3f}' if m[k] else f'{k} none')
        return
    os.makedirs(a.work, exist_ok=True)
    hues = {k: [v, DEPTH0] for k, v in START.items()}
    best = {k: (9.0, list(v)) for k, v in hues.items()}  # each colour's closest round: the denser faces can overshoot
    for r in range(ROUNDS):
        f = os.path.join(a.work, f'r{r}.png'); render(hues, f, 256, 24); m = measure(f)
        d = {k: dist(TARGET[k], m[k]) if m[k] else 1.0 for k in TARGET}
        print(f'round {r}: ' + '  '.join(f'{k} {m[k]} {d[k]:.3f}' for k in TARGET), flush=True)
        best = {k: (d[k], list(hues[k])) if d[k] < best[k][0] else best[k] for k in TARGET}
        if max(d.values()) <= TOL:
            break
        for k in TARGET:
            if d[k] <= TOL or not m[k]:
                continue
            inp = lab_of_lin(hexlin(hues[k][0])[None])[0]
            want = inp + (lab_of_lin(hexlin(TARGET[k])[None])[0] - lab_of_lin(hexlin(m[k])[None])[0])
            got, lost = to_gamut(want)
            hues[k][0] = hexof(lin_of_lab(got))
            if lost > 0.01:                                  # out of gamut: a denser face instead
                hues[k][1] = min(DEPTH_MAX, round(hues[k][1] + DEPTH_STEP, 3))
    hues = {k: best[k][1] for k in TARGET}
    print('inputs: ' + json.dumps(hues), flush=True)
    render(hues, a.out, a.px, a.samples)
    m = measure(a.out)
    for k in TARGET:
        print(f'{k:7s} target {TARGET[k]}  measured {m[k]}  distance {dist(TARGET[k], m[k]):.3f}', flush=True)


if __name__ == '__main__':
    main()
