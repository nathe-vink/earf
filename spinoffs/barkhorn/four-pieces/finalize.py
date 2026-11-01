"""The slide's deliverables from a finished frame: anchors.json (1920 x 1080 px) with each product's box, its label zone
and the zone's tone, the header zone, and how even each zone is in the picture; plus the 1920 x 1080 copy and the
3840 x 2160 master as a high-quality JPEG.

    python3 spinoffs/barkhorn/four-pieces/finalize.py SHOT.json FRAME.png OUTDIR NAME

Tone: "light" when the zone's median luminance is 128 or more (dark ink reads), else "dark" (light ink). Evenness: the
luminance spread (p95 - p5) and the largest step across the zone in 8 px blocks; the coordinator's label builder picks
the ink from the picture underneath, so an even zone matters more than anything else.
"""
import json, os, sys

import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import layout  # noqa: E402

NAMES = {'tropos': 'Tropos', 'mantle': 'Mantle', 'core': 'Core', 'hemisphere': 'Hemisphere'}


def lum(a):
    return 0.2126 * a[..., 0] + 0.7152 * a[..., 1] + 0.0722 * a[..., 2]


def zone_stats(L, z, A=None):
    x0, y0, x1, y1 = [int(round(v)) for v in z]
    r = L[y0:y1, x0:x1]
    rgb = [round(float(np.median(A[y0:y1, x0:x1, c]))) for c in range(3)] if A is not None else None
    blocks = r[: (r.shape[0] // 8) * 8, : (r.shape[1] // 8) * 8].reshape(r.shape[0] // 8, 8, r.shape[1] // 8, 8).mean((1, 3))
    return {'median': round(float(np.median(r)), 1), 'p5': round(float(np.percentile(r, 5)), 1),
            'p95': round(float(np.percentile(r, 95)), 1), 'spread': round(float(np.percentile(r, 95) - np.percentile(r, 5)), 1),
            'block_range': round(float(blocks.max() - blocks.min()), 1),
            'median_srgb': rgb, 'median_hex': '#%02X%02X%02X' % tuple(rgb) if rgb else None}


def main(shot_path, frame, outdir, name):
    shot = json.load(open(shot_path))
    B, Z, problems = layout.solve(shot, verbose=False)
    img = Image.open(frame).convert('RGB')
    small = img.resize((1920, 1080), Image.LANCZOS)
    A = np.asarray(small).astype(np.float32)
    L = lum(A)
    os.makedirs(outdir, exist_ok=True)
    out = {'image_1920': f'{name}-1920.png', 'image_3840': f'{name}-3840.jpg', 'size': [1920, 1080],
           'note': 'pixels at 1920 x 1080, [x0, y0, x1, y1] from the top left; label zones 380 x 130, 40-80 px from '
                   'their product; tone is the ground under the zone (light: use dark ink; dark: use light ink)',
           'products': {}, 'header': None, 'layout_problems': problems}
    for k, spec in shot['labels'].items():
        if k == 'header':
            continue
        b = B[spec['of']][0]
        st = zone_stats(L, Z[k], A)
        out['products'][k] = {'name': NAMES[k], 'bbox': [round(v) for v in b],
                              'label_zone': [round(v) for v in Z[k]], 'label_side': spec['side'],
                              'tone': 'light' if st['median'] >= 128 else 'dark', 'zone_luminance': st}
        if k == 'tropos':
            out['products'][k]['note'] = 'the pair; the box and zone are the left speaker\'s'
            out['products'][k]['bbox_right'] = [round(v) for v in B['tropos1'][0]]
    st = zone_stats(L, Z['header'], A)
    out['header'] = {'zone': [round(v) for v in Z['header']], 'tone': 'light' if st['median'] >= 128 else 'dark',
                     'zone_luminance': st}
    # the coordinator's small "A render" note in the bottom-right corner
    cz = [1600, 1020, 1880, 1060]
    st = zone_stats(L, cz, A)
    out['corner_note'] = {'zone': cz, 'tone': 'light' if st['median'] >= 128 else 'dark', 'zone_luminance': st}
    json.dump(out, open(os.path.join(outdir, f'{name}.anchors.json'), 'w'), indent=1)
    small.save(os.path.join(outdir, f'{name}-1920.png'), optimize=True)
    if img.size[0] >= 3840:
        img.save(os.path.join(outdir, f'{name}-3840.jpg'), quality=92, subsampling=0)
    for k, v in out['products'].items():
        print(k, v['label_zone'], v['tone'], v['zone_luminance'])
    print('header', out['header'])
    if problems:
        print('LAYOUT PROBLEMS', problems)


if __name__ == '__main__':
    main(*sys.argv[1:5])
