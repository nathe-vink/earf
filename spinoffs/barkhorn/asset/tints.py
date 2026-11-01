"""Tropos's eight tints in stock TruCast sheet, for the assets' `--tints trucast` (2026-10-31): reconciled with the
r48-biomes session's spinoffs/barkhorn/biomes/tints.json (commit b970bb3f), which uses this branch's
make/stock_tints.py method (the 'held' case). See TINTS.md.

    python3 spinoffs/barkhorn/asset/tints.py      ->  tints-trucast.json beside this file, and a table

- **Codes, TT and channel splits:** biomes' (the TruCast code for each tint is its PROPOSAL; Ember 2423 and Smoke 2064
  are this branch's stock pair). TT is A&C Plastics' TruCast chart.
- **Cabinet:** held at 20 mm, as biomes (this branch's stock flavours hold 2064 at the 3/4 in sheet's 19.05 mm; the
  difference is about one point of TT).
- **Horn, current design:** the formed horn in its deep lot keeps the site's colour (the deep lot is a custom cast, not
  a stock code). biomes instead makes the horn pass what the cabinet's wall passes; see TINTS.md.
- **Horn, Strata:** stock 1/2 in sheet of the same code, held at 12.7 mm, except Smoke, whose laminated horn is 2074
  Dark Gray (make/stock-pair.md).
"""
import json, math, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(HERE), 'make'))
from stock_tints import LUM, SURFACE, hexs, sigma_for       # noqa: E402

IOR = 1.49
# tint: flavour, code, name, TT (%), split (r48-biomes' tints.py, b970bb3f)
TINTS = {
    'Ember':  ('cloud-red',            '2423', 'Red',                14.1, (0.08, 1.00, 0.85)),
    'Dust':   ('cloud-orange',         '2422', 'Orange (amber)',     59.1, (0.02, 0.40, 1.00)),
    'Acid':   ('cloud-amber',          '9097', 'Fluorescent Yellow', 77.6, (0.00, 0.10, 1.00)),
    'Poison': ('eucalyptus-y2k-green', '2092', 'Green',              18.6, (1.00, 0.18, 0.80)),
    'Ice':    ('cloud-blue',           '2069', 'Tinted Blue',        57.6, (1.00, 0.40, 0.06)),
    'Haze':   ('cloud-violet',         '2287', 'Violet',             13.5, (0.50, 1.00, 0.12)),
    'Fog':    ('birch-fog-clear',      '0000', 'Clear',              93.0, (1.00, 1.00, 1.00)),
    'Smoke':  ('cloud-black',          '2074', 'Dark Gray',          11.7, (1.03, 1.00, 0.97)),   # 2064 until 2026-11-01
}
STRATA_HORN = {}                     # every horn in its cabinet's code (Smoke's was 2074 under a 2064 cabinet until 2026-11-01)
WALL, LAYER = 20.0, 12.7


def sig(split, tt, mm):
    return [0.0, 0.0, 0.0] if tt / 100 >= SURFACE else sigma_for(split, tt / 100, mm)


def main():
    out = {}
    print('| tint | cabinet | TT at 20 mm | Strata horn | TT at 12.7 mm |\n|---|---|---|---|---|')
    for t, (fl, code, name, tt, split) in TINTS.items():
        hc, hn, htt, hs = STRATA_HORN.get(t, (code, name, tt, split))
        sc, sh = sig(split, tt, WALL), sig(hs, htt, LAYER)
        out[t] = {'flavour': fl, 'cabinet': f'TruCast {code} {name}', 'cabinet_tt_20mm': tt,
                  'cabinet_deep': hexs([math.exp(-s * 25.0) for s in sc]), 'cabinet_radius_m': 0.025,
                  'strata_horn': f'TruCast {hc} {hn}, 1/2 in', 'strata_horn_tt_12_7mm': htt,
                  'strata_horn_deep': hexs([math.exp(-s * 10.0) for s in sh]), 'horn_radius_m': 0.010, 'ior': IOR}
        print(f"| {t} | {code} {name} | {tt} % | {hc} {hn} | {htt} % |")
    json.dump(out, open(os.path.join(HERE, 'tints-trucast.json'), 'w'), indent=1)


if __name__ == '__main__':
    main()
