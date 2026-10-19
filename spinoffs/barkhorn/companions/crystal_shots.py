"""Round 32d's frames: the Orb on the table and the Dome over it, placed by Planet's kit piece (earf_moon.py, fns "orb"
and "dome"), in Moon's bar frame (moon_shots.py) in smoked and in Ember; the swap (a Dome lowered off its fixture, spare
covers in three tints on the counter); and the catch, close.

    python3 spinoffs/barkhorn/companions/crystal_shots.py
    PY=python3.11 python3 spinoffs/barkhorn/companions/crystal_shots.py --render [names] [--scale 1.0]
"""
import json, os, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
sys.path.insert(0, HERE)
import moon_shots as MS                                             # noqa: E402

SHOTS = os.path.join(ROOT, 'studio', 'shots', 'barkhorn', 'crystal')
RENDERS = os.path.join(ROOT, 'renders', '2026-10-19', 'barkhorn', 'crystal')
FIXTURE = 'hub|pins|cob|gland|cord|canopy'


def piece(fn, spots, flavour, **k):
    return {'kind': 'kit', 'shape': 'ext', 'module': 'earf_moon', 'fn': fn, 'spots': spots, 'flavour': flavour, **k}


PZ = 1.20               # the Dome's rim in the bar frames, 440 over the counter (a booth's height)


def bar(colour):
    s = MS.shot('bar', colour)
    tx, ty, px, py = -0.12, 0.0, 0.26, 0.18
    s['title'] = f'Orb and Dome in {colour}, in a bar'
    s['set']['props'] = [p for p in s['set']['props'] if p.get('module') != 'earf_moon'] + [
        piece('orb', [[tx, ty, MS.TABLE_Z]], colour),
        piece('dome', [[px, py, PZ]], colour)]
    # the Orb is squat (180 tall to Moon's 277): the strip behind Moon's column would light the counter's edge
    s['lights'].pop('strip', None)
    s['lights']['kick']['position'] = [px, 0.50, PZ + 0.08]
    s['lights']['kick']['target'] = [px, py, PZ + 0.06]
    # closer and lower than Moon's (the Orb is squat): the pendant hung lower over it
    s['camera'].update(position=[-0.30, -0.98, 0.97], target=[-0.01, 0.05, 0.99], lens_mm=50,
                       focus=[tx, ty, MS.TABLE_Z + 0.10])
    return s


def swap():
    s = MS.shot('bar', 'ember')
    s['title'] = 'Dome: the covers swap by hand'
    covers = [(-0.36, 'acid'), (-0.13, 'ice'), (0.10, 'haze')]
    s['set']['props'] = [p for p in s['set']['props'] if p.get('module') != 'earf_moon'] + [
        piece('dome', [{'position': [x, 0.02, MS.TABLE_Z], 'flavour': f, 'rotate_z': 20 * i}
                       for i, (x, f) in enumerate(covers)], 'acid', hide=FIXTURE, lamp=False, shade_glow=0.0),
        piece('dome', [[0.20, 0.08, 1.12]], 'ember', cover_drop=0.075, cover_turn=30)]
    s['lights'].pop('strip', None); s['lights'].pop('kick', None)
    s['lights']['fill']['irradiance'] = 0.16
    s['lights']['top'] = {'type': 'area', 'size_m': [0.8, 0.3], 'position': [-0.12, -0.2, 1.7], 'target': [-0.12, 0.02, 0.8],
                          'irradiance': 0.35, 'color': 2700, 'camera': False}
    s['camera'] = {'position': [-0.10, -1.15, 1.08], 'target': [-0.04, 0.05, 1.0], 'lens_mm': 42, 'level': True,
                   'fstop': 5.6, 'focus': [-0.05, 0.05, 0.95]}
    return s


def catch():
    """The bayonet, close: the cover lowered 50 mm and turned 30 deg, on a pale seamless."""
    s = MS.shot('seamless', 'acid')
    s['title'] = 'Dome: the catch'
    s['set']['props'] = [p for p in s['set']['props'] if p.get('module') != 'earf_moon' and p.get('shape') != 'box'] + [
        piece('dome', [[0.0, 0.0, 1.18]], 'acid', cover_drop=0.07, cover_turn=30, lamp=False, shade_glow=0.0)]
    s['camera'] = {'position': [0.10, -0.50, 1.18], 'target': [0.0, 0.0, 1.24], 'lens_mm': 70, 'level': False,
                   'fstop': 8.0, 'focus': [0.0, -0.04, 1.25]}
    return s


FRAMES = {'bar-smoked': lambda: bar('smoked'), 'bar-ember': lambda: bar('ember'), 'swap': swap, 'catch': catch}


def build():
    os.makedirs(SHOTS, exist_ok=True)
    for n, f in FRAMES.items():
        json.dump(f(), open(os.path.join(SHOTS, n + '.json'), 'w'), indent=1)
        print(n)


def render(names, scale):
    py = os.environ.get('PY', 'python3')
    os.makedirs(RENDERS, exist_ok=True)
    for n in names:
        subprocess.run([py, os.path.join(ROOT, 'studio', 'engine', 'render.py'), os.path.join(SHOTS, n + '.json'),
                        '--out', os.path.join(RENDERS, n + '.png'), '--scale', str(scale)], check=True,
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print(n, flush=True)


def sheet():
    tiles = ' '.join(f"-label '{t}' {os.path.join(RENDERS, n + '.png')}" for n, t in
                     (('bar-smoked', 'Orb and Dome, smoked'), ('bar-ember', 'Orb and Dome, Ember'),
                      ('swap', 'The covers swap by hand'), ('catch', 'The catch: a quarter-turn bayonet')))
    out = os.path.join(RENDERS, 'sheet.png')
    subprocess.run(f"montage {tiles} -tile 4x1 -geometry 450x500+4+4 -pointsize 16 -background '#F2F0EC' -depth 8 {out}",
                   shell=True, check=True)
    print(out)


if __name__ == '__main__':
    a = sys.argv[1:]
    if '--render' in a:
        scale = float(a[a.index('--scale') + 1]) if '--scale' in a else 1.0
        render([x for x in a if x in FRAMES] or list(FRAMES), scale)
    elif '--sheet' in a:
        sheet()
    else:
        build()
