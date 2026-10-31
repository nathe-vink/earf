"""Round 43: does a stock-colour prototype still look like EARF? (the coordinator, 2026-10-31, from the research's R1
on r46-owner-notes: the nearest stock cell-cast colours are 2423 Red for Ember and 2064 Gray for Smoke).

Core (pass 4's studio hero) and Mantle (its own dusk shot from r32-turntable-final) in three looks each, in Ember and
in Smoke: the site's tint; the stock colour, kind case; the stock colour, harsh case. The stock colours are the chips'
hue from the photos in R1's Appendix A (2423 #D4606F, 2064 #A5A5A4) scaled to TruCast's published transmission
(2423 14.1 %, 2064 29.3 %, at 1/8"; AC Plastics, which stocks the 3/8" and 1/2" sheet, sells TruCast). How a stock
sheet deepens with thickness is not published (R1 1.2), so two cases:
- kind: each stock sheet transmits like its 1/8" chip whatever its thickness (some makers adjust the dye to hold
  the light transmission), so Core's 3/8" ball wall is one chip, and Mantle's 25 mm plinth, two 1/2" sheets laminated,
  is two chips;
- harsh: one dye loading at every thickness (Beer-Lambert from the 1/8" chip).
The 1/8" chips (about $1 each, R1 section 5) settle which is true.

    python3 spinoffs/barkhorn/companions/stock_colours.py [--render]
"""
import copy, json, os, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
sys.path.insert(0, HERE)
import lamps_pdp_r41 as P4                                          # noqa: E402

SHOTS = os.path.join(ROOT, 'studio', 'shots', 'barkhorn', 'stock-colours')
RENDERS = os.path.join(ROOT, 'renders', '2026-10-31', 'barkhorn', 'stock-colours')
MANTLE = 'spinoffs/barkhorn/companions/out-turntable-float/open/barkhorn-turntable-float-open.json'


def _lin(h):
    c = [int(h[i:i + 2], 16) / 255 for i in (1, 3, 5)]
    return [x / 12.92 if x <= 0.04045 else ((x + 0.055) / 1.055) ** 2.4 for x in c]


def _hex(c):
    o = []
    for x in c:
        x = max(0.0, min(1.0, x))
        o.append(round((12.92 * x if x <= 0.0031308 else 1.055 * x ** (1 / 2.4) - 0.055) * 255))
    return '#%02X%02X%02X' % tuple(o)


def chip(photo, lt):
    """The 1/8" (3.175 mm) chip's transmission per channel: the photo's hue at the published light transmission."""
    c = _lin(photo)
    y = 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2]
    return [min(1.0, x * lt / y) for x in c]


STOCK = {'ember': ('2423 Red', chip('#D4606F', 0.141)), 'smoke': ('2064 Gray', chip('#A5A5A4', 0.293))}


def deep(T, path_mm, case, sheet_mm):
    """The colour transmitted through `path_mm` (the material's radius) of a part cut from `sheet_mm` stock."""
    if case == 'kind':
        n = path_mm / sheet_mm                         # chips' worth of sheets along the path
    else:
        n = path_mm / 3.175                            # one dye loading: Beer-Lambert from the chip
    return _hex([t ** n for t in T])


def core(flavour, case):
    s = P4.orb(flavour)
    if case != 'site':
        name, T = STOCK[flavour]
        s['materials'].setdefault('body', {})['deep'] = deep(T, 5.0, case, 9.5)       # the ball wall from 3/8" sheet
    s['size'] = [1600, 2000]
    s['title'] = f'Core in {flavour}: {"the site tint" if case == "site" else STOCK[flavour][0] + ", " + case}'
    return s


def mantle(flavour, case):
    raw = subprocess.run(['git', 'show', f'origin/r32-turntable-final:studio/shots/barkhorn/turntable-float/dusk-{flavour}.json'],
                         cwd=ROOT, check=True, capture_output=True).stdout
    s = json.loads(raw)
    s = s[0] if isinstance(s, list) else s
    s['product']['def'] = MANTLE
    s['finish'] = {'enabled': False}          # its finishing pass needs PIL, which the render Python here lacks
    if case != 'site':
        name, T = STOCK[flavour]
        m = s.setdefault('materials', {})
        # the plinth 25 (two 1/2" laminated: its material's radius 25), the lid 6 (one 1/4" sheet: radius 7.5)
        m['acrylic'] = {'deep': deep(T, 25.0, case, 12.7)}
        m['acrylic-lid'] = {'deep': deep(T, 7.5, case, 5.6)}
    s['title'] = f'Mantle in {flavour}: {"the site tint" if case == "site" else STOCK[flavour][0] + ", " + case}'
    return s


CASES = ('site', 'kind', 'harsh')
BUILD = {f'{w}-{f}-{c}': (lambda w=w, f=f, c=c: {'core': core, 'mantle': mantle}[w](f, c))
         for w in ('core', 'mantle') for f in ('ember', 'smoke') for c in CASES}
LABEL = {'site': 'site tint', 'kind': 'stock, kind case', 'harsh': 'stock, harsh case'}


def sheet():
    tiles = []
    for w in ('core', 'mantle'):
        row = []
        for f in ('ember', 'smoke'):
            for c in CASES:
                src = os.path.join(RENDERS, f'{w}-{f}-{c}.png')
                t = os.path.join(RENDERS, f'_{w}-{f}-{c}.png')
                lab = f'{f.title()}: ' + (LABEL[c] if c == 'site' else f'{STOCK[f][0]}, {LABEL[c][7:]}')
                geo = '520x650^' if w == 'core' else '780x520^'
                subprocess.run(['convert', src, '-resize', geo, '-gravity', 'center', '-extent', geo[:-1],
                                '-gravity', 'south', '-background', '#F4F1EC', '-splice', '0x40', '-font', 'DejaVu-Sans',
                                '-pointsize', '18', '-fill', '#222222', '-annotate', '+0+10', lab, t], check=True)
                row.append(t)
        tiles.append(row)
    out = os.path.join(RENDERS, 'stock-colours-sheet.png')
    subprocess.run(['convert', '(', *tiles[0], '+append', ')', '(', *tiles[1], '+append', ')', '-gravity', 'center',
                    '-background', '#F4F1EC', '-append', '-quality', '95', out], check=True)
    for r in tiles:
        for t in r:
            os.remove(t)
    print('sheet', os.path.relpath(out, ROOT))


def main():
    os.makedirs(SHOTS, exist_ok=True)
    for n, f in BUILD.items():
        json.dump(f(), open(os.path.join(SHOTS, n + '.json'), 'w'), indent=1)
    print(len(BUILD), 'shots;', {f: (STOCK[f][0], {c: deep(STOCK[f][1], 5.0, c, 9.5) for c in ('kind', 'harsh')})
                               for f in STOCK})
    if '--render' in sys.argv:
        os.makedirs(RENDERS, exist_ok=True)
        for n in BUILD:
            if os.path.exists(os.path.join(RENDERS, n + '.png')) and '--again' not in sys.argv:
                continue
            subprocess.run(['python3', os.path.join(ROOT, 'studio', 'engine', 'render.py'), os.path.join(SHOTS, n + '.json'),
                            '--out', os.path.join(RENDERS, n + '.png'), '--scale', '0.4', '--samples', '64'], cwd=ROOT,
                           check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            print('rendered', n, flush=True)
        sheet()


if __name__ == '__main__':
    main()
