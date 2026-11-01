"""The flush horn (the owner, 2026-11-01: the horn no wider than the cabinet) against the approved one, low band.

    .venv-fab/bin/python spinoffs/barkhorn/horn_sim.py solve lo --name check610              # the approved, re-solved
    .venv-fab/bin/python spinoffs/barkhorn/horn_sim.py solve lo --name flush536 --mouth-w 536
    .venv-fab/bin/python spinoffs/barkhorn/acoustics/flush_compare.py                       # -> flush_compare.json

Per frequency: the -6 dB beamwidths (horizontal, vertical), the directivity index, the on-axis level and the radiated
power at the same piston velocity (dB against the approved horn), and the throat's radiation resistance (the real part
of the face pressure over the piston's velocity, the horn's loading on the driver).
"""
import json, sys
from pathlib import Path
import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from horn_plots import coverage, load, cplx                                 # noqa: E402


def run(name):
    ang, res = load(name, ['lo'])
    cov = coverage(res, ang)
    i0 = int(np.where(ang == 0)[0][0])
    out = []
    for c, r in zip(cov, res):
        on = abs(cplx(r['1']['h'])[i0])
        out.append(dict(f=c['f'], h=c['h'], v=c['v'], di=round(c['di'], 2), on=float(on), power=float(r['1']['power']),
                        rload=float(complex(*r['1']['p_face']).real)))
    return out


def main():
    a, b = run('check610'), run('flush536')
    rows = []
    for x, y in zip(a, b):
        rows.append(dict(f=x['f'], h610=x['h'], h536=y['h'], v610=x['v'], v536=y['v'], di610=x['di'], di536=y['di'],
                         on_db=round(20 * np.log10(y['on'] / x['on']), 2), power_db=round(10 * np.log10(y['power'] / x['power']), 2),
                         rload_ratio=round(y['rload'] / x['rload'], 3)))
    stored = json.loads((HERE / 'summary.json').read_text())['horn']
    st = {s['f']: s for s in stored}
    check = [dict(f=x['f'], h=x['h'], h_stored=st.get(x['f'], {}).get('h')) for x in a]
    (HERE / 'flush_compare.json').write_text(json.dumps(dict(rows=rows, control=check), indent=1))
    fmt = lambda v: '  -  ' if v is None else f'{v:5.0f}'
    print('   f   h610  h536   v610  v536  di610 di536  on dB  pow dB  Rload')
    for r in rows:
        print(f"{r['f']:5d} {fmt(r['h610'])} {fmt(r['h536'])}  {fmt(r['v610'])} {fmt(r['v536'])}  {r['di610']:5.1f} {r['di536']:5.1f}  {r['on_db']:+5.2f}  {r['power_db']:+5.2f}  {r['rload_ratio']:.3f}")
    print('control (re-solved vs stored h):', [(c['f'], None if c['h'] is None else round(c['h']), None if c['h_stored'] is None else round(c['h_stored'])) for c in check[::4]])


if __name__ == '__main__':
    main()
