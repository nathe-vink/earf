"""Acid B's grade after the render: the raw frame's sky read olive (median sRGB 166/163/132), which pushed the cabinet
toward mustard, so the finals take a linear white-balance shift (green x 0.95, blue x 1.06) before the usual finish.
A blind duel preferred it to the frame as rendered, 6.2 to 5.9 (acid_b.md). The horn's hue stays on Acid's #E9B320.

    python3.11 spinoffs/barkhorn/elements/acid_b_grade.py renders/.../acid_b.raw.png renders/.../acid_b.png SHOT.json
"""
import json, os, subprocess, sys, tempfile

import numpy as np
from PIL import Image

GAINS = (1.0, 0.95, 1.06)
HERE = os.path.dirname(os.path.abspath(__file__))
FINISH = os.path.join(HERE, '..', '..', '..', 'studio', 'engine', 'finish.py')


def s2l(c):
    return np.where(c <= 0.04045, c / 12.92, ((c + 0.055) / 1.055) ** 2.4)


def l2s(c):
    c = np.clip(c, 0, 1)
    return np.where(c <= 0.0031308, c * 12.92, 1.055 * c ** (1 / 2.4) - 0.055)


def main():
    raw, out, shot = sys.argv[1:4]
    a = np.asarray(Image.open(raw).convert('RGB')).astype(float) / 255
    with tempfile.TemporaryDirectory() as d:
        shifted = os.path.join(d, 'shifted.raw.png')
        Image.fromarray((l2s(s2l(a) * np.array(GAINS)) * 255 + 0.5).astype('uint8')).save(shifted)
        spec = json.load(open(shot))['finish']
        subprocess.run([sys.executable, FINISH, 'apply', shifted, out, '--spec', json.dumps(spec)], check=True)


if __name__ == '__main__':
    main()
