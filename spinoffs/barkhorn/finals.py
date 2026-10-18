"""The speakers' final pictures (round 31): every view of every colour from one place, so none is left behind when the
design moves on. The owner: "we need to make sure all of the speaker renders are good to go and then replace them
wherever they appear with the finals. I noticed some of them don't have handles, some of them are using poison for the
dissection shot, etc."

The site's pictures had been rendered round by round: the front views in round 21 and the horns turning in round 23,
before the 240 grips were made standard (round 24) and the R of the mark on the back was given its hole (round 29);
the back and the plate in round 30, the plate's connectors provisional; one cutaway, Poison's, shown for every colour.
Here each view is its template shot, the one tuned in its round, rendered again with the product as it stands now
(studio/products/barkhorn-cloud.json, its model rebuilt from the CAD), for all eight colours:

- front-on, front-off: the three-quarter view from the front, cover on and off (lookbook21);
- horn-side, horn-back: the horn close, from the side and from behind (horn21);
- back, amp: the speaker from behind, and the amplifier's plate close (site30);
- inside: the cutaway, now in each colour (site30's inside, Poison's alone until now);
- turn-00 ... turn-23: the horn turning, 15 degrees a frame (turn23), made into each colour's sprite;

and the line's own: the hero (the eight on an arc) and the room (a pair of Poison, room17).

    python3 spinoffs/barkhorn/finals.py build                writes every shot to studio/shots/barkhorn/finals31/
    python3 spinoffs/barkhorn/finals.py render [--only red] [--shard 1/8] [--views front-on,back] [--samples N --scale S]
                                                             renders its share into renders/2026-10-18/barkhorn/finals31/,
                                                             skipping a picture newer than both its shot and the model
    python3 spinoffs/barkhorn/finals.py sprites              each colour's 24 turning frames as one sprite (6 x 4)
    python3 spinoffs/barkhorn/finals.py check                what is missing or stale, and any view that should show a
                                                             grip and does not, or shows another colour
    python3 spinoffs/barkhorn/finals.py sheet                every final on one sheet, for a look before it ships
"""
import argparse, copy, json, os, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
SHOTS = os.path.join(ROOT, 'studio', 'shots', 'barkhorn')
OUT_SHOTS = os.path.join(SHOTS, 'finals31')
OUT = os.path.join(ROOT, 'renders', '2026-10-18', 'barkhorn', 'finals31')
MODEL = os.path.join(HERE, 'out-cloud', 'render', 'barkhorn-cloud.glb')
FLAVOUR = {'red': 'cloud-red', 'orange': 'cloud-orange', 'amber': 'cloud-amber', 'green': 'eucalyptus-y2k-green',
           'blue': 'cloud-blue', 'violet': 'cloud-violet', 'ice': 'birch-fog-clear', 'black': 'cloud-black'}
KEYS = list(FLAVOUR)
TURN = 24
# each view: its template (a shot per colour, or one shot made each colour's), and whether it shows a side, so a grip
VIEWS = {'front-on': ('lookbook21/look-{k}-on.json', True), 'front-off': ('lookbook21/look-{k}-off.json', True),
         'horn-side': ('horn21/horn-{k}-side.json', False), 'horn-back': ('horn21/horn-{k}-back.json', False),
         'back': ('site30/back-{k}.json', True), 'amp': ('site30/detail-{k}.json', False),
         'inside': ('site30/inside.json', False)}
VIEWS.update({f'turn-{i:02d}': (f'turn23/turn-{{k}}-{i:02d}.json', False) for i in range(TURN)})
LINE = {'hero': 'site30/hero.json', 'room': 'room17/room-poison.json'}


def recolour(sh, k):
    """The shot with every copy of the speaker in colour k (the templates already are, but for the cutaway)."""
    s = copy.deepcopy(sh)
    p = s['product']
    p['flavour'] = FLAVOUR[k]
    for inst in p.get('instances', []):
        inst['flavour'] = FLAVOUR[k]
    s['title'] = s.get('title', '') + f' (finals31, {k})'
    return s


def shots():
    """[(name, shot dict)]: every final, in a stable order (by colour, then view), the line's last."""
    out = []
    for k in KEYS:
        for v, (tpl, _) in VIEWS.items():
            sh = json.load(open(os.path.join(SHOTS, tpl.format(k=k))))
            out.append((f'{v}-{k}' if not v.startswith('turn-') else f'turn/{k}-{v[5:]}', recolour(sh, k)))
    for name, tpl in LINE.items():
        out.append((name, json.load(open(os.path.join(SHOTS, tpl)))))
    return out


def build():
    for name, sh in shots():
        f = os.path.join(OUT_SHOTS, name + '.json')
        os.makedirs(os.path.dirname(f), exist_ok=True)
        json.dump(sh, open(f, 'w'), indent=1)
    print(f'{len(shots())} shots in', os.path.relpath(OUT_SHOTS, ROOT))


def stale(name):
    png, shot = os.path.join(OUT, name + '.png'), os.path.join(OUT_SHOTS, name + '.json')
    if not os.path.exists(png):
        return 'missing'
    t = os.path.getmtime(png)
    if t < os.path.getmtime(shot) or (os.path.exists(MODEL) and t < os.path.getmtime(MODEL)):
        return 'stale'
    return None


def render(a):
    names = [n for n, _ in shots()]
    if a.only:
        names = [n for n in names if any(n.endswith(f'-{k}') or n.startswith(f'turn/{k}-') for k in a.only.split(','))]
    if a.views:
        vs = a.views.split(',')
        names = [n for n in names if any(n.startswith(v + '-') or n == v or (v == 'turn' and n.startswith('turn/')) for v in vs)]
    if a.shard:
        i, n = (int(x) for x in a.shard.split('/'))
        names = names[i - 1::n]
    todo = [n for n in names if a.force or stale(n)]
    print(f'{len(todo)} of {len(names)} to render')
    for j, name in enumerate(todo):
        out = os.path.join(OUT, name + '.png')
        os.makedirs(os.path.dirname(out), exist_ok=True)
        cmd = [sys.executable, os.path.join(ROOT, 'studio', 'engine', 'render.py'), os.path.join(OUT_SHOTS, name + '.json'), '--out', out]
        if a.samples:
            cmd += ['--samples', str(a.samples)]
        if a.scale:
            cmd += ['--scale', str(a.scale)]
        print(f'[{j + 1}/{len(todo)}] {name}', flush=True)
        subprocess.run(cmd, check=True, cwd=ROOT)


def sprites():
    from PIL import Image
    for k in KEYS:
        frames = [os.path.join(OUT, 'turn', f'{k}-{i:02d}.png') for i in range(TURN)]
        if not all(os.path.exists(f) for f in frames):
            print(k, 'frames missing'); continue
        fw, fh = 480, 432
        sheet = Image.new('RGB', (fw * 6, fh * 4))
        for i, f in enumerate(frames):
            sheet.paste(Image.open(f).convert('RGB').resize((fw, fh), Image.LANCZOS), (fw * (i % 6), fh * (i // 6)))
        sheet.save(os.path.join(OUT, f'turn-{k}.jpg'), quality=86)
        print(os.path.relpath(os.path.join(OUT, f'turn-{k}.jpg'), ROOT))


def check():
    """Missing or stale pictures; a view showing a side whose report has no grip in frame; a report of another colour."""
    bad = 0
    for name, sh in shots():
        why = stale(name)
        rep = os.path.join(OUT, name + '.report.json')
        if not why and os.path.exists(rep):
            r = json.load(open(rep))
            parts = json.dumps(r.get('parts_2d', ''))
            v = name.rsplit('-', 1)[0] if not name.startswith('turn/') else 'turn'
            if VIEWS.get(v, (None, False))[1] and 'grip-' not in parts:
                why = 'no grip in frame'
            fl = sh['product'].get('flavour')
            if fl and fl not in json.dumps(r.get('shot', r)) and fl not in open(os.path.join(OUT, name + '.shot.json')).read():
                why = f'not {fl}'
        if why:
            bad += 1
            print(f'{name}: {why}')
    print('all good' if not bad else f'{bad} to do')


def sheet():
    from PIL import Image
    rows = []
    for k in KEYS:
        row = [os.path.join(OUT, f'{v}-{k}.png') for v in ('front-on', 'front-off', 'horn-side', 'horn-back', 'back', 'amp', 'inside')]
        row.append(os.path.join(OUT, 'turn', f'{k}-00.png'))
        rows.append(row)
    H = 300
    ims = [[Image.open(f).convert('RGB') if os.path.exists(f) else Image.new('RGB', (240, 300), (220, 40, 40)) for f in r] for r in rows]
    ims = [[i.resize((int(i.width * H / i.height), H), Image.LANCZOS) for i in r] for r in ims]
    W = max(sum(i.width + 8 for i in r) for r in ims)
    S = Image.new('RGB', (W, (H + 8) * len(ims)), 'white')
    for y, r in enumerate(ims):
        x = 0
        for i in r:
            S.paste(i, (x, y * (H + 8))); x += i.width + 8
    S.save(os.path.join(OUT, 'sheet.jpg'), quality=84)
    print(os.path.relpath(os.path.join(OUT, 'sheet.jpg'), ROOT))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('what', choices=['build', 'render', 'sprites', 'check', 'sheet'])
    ap.add_argument('--only'); ap.add_argument('--views'); ap.add_argument('--shard')
    ap.add_argument('--samples', type=int); ap.add_argument('--scale', type=float); ap.add_argument('--force', action='store_true')
    a = ap.parse_args()
    {'build': build, 'render': lambda: render(a), 'sprites': sprites, 'check': check, 'sheet': sheet}[a.what]()


if __name__ == '__main__':
    main()
