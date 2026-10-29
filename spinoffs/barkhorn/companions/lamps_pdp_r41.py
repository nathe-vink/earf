"""Round 41, pass 4 of the site's lamp pictures (the coordinator, 2026-10-29: "Re-render all 19 of pass 3's pictures in
the new design ... Use pass 3's shots exactly: same cameras, lights, exposure and samples, so a picture changes only
where a lamp changed."). The owner signed round 40: Hemisphere's low top and Core on the 30 base are now the main
builds (studio/products/earf-dome-pendant.json, earf-orb-table.json) and the kit piece (earf_moon.py) follows them.

Each picture is pass 3's (lamps_pdp_r35: dome_p3, orb_p3, p3_row) with only what belongs to the lamp moved with it:
- Hemisphere: the cap's glint 34 lower with the cap (126 over the rim, was 160); the fin strips stay and draw the
  crown's edge.
- Core: its light, its glints and the pools it throws on the table 18 lower with the ball (the base 48 -> 30).
- The rows: the kit piece carries the new heights; the Cores row's pools drop 18 with the balls.

    python3 spinoffs/barkhorn/companions/lamps_pdp_r41.py                         # the shots
    python3 spinoffs/barkhorn/companions/lamps_pdp_r41.py --render NAME [NAME ...]  # render these (128 samples)
"""
import json, os, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
sys.path.insert(0, HERE)
import lamps_pdp_r35 as P                                          # noqa: E402

SHOTS = os.path.join(ROOT, 'studio', 'shots', 'barkhorn', 'lamps-pdp-r41')
RENDERS = os.path.join(ROOT, 'renders', '2026-10-29', 'barkhorn', 'lamps-pdp-r41')
CAP_DROP = -0.034             # Hemisphere's cap: 126 over the rim, was 160
BALL_DROP = -0.018            # Core's ball: the base 30, was 48


def drop_pools(s, dz):
    for k, L in s['lights'].items():
        if k.startswith('pool'):
            L['position'] = P.lift(L['position'], dz)


def dome(flavour):
    s = P.dome_p3(flavour)
    s['glints']['cap']['at'] = P.lift(s['glints']['cap']['at'], CAP_DROP)
    s['title'] = s['title'].replace('(round 39, pass 3)', '(round 41, pass 4)')
    return s


def orb(flavour):
    s = P.orb_p3(flavour)
    s['lights']['ball']['position'] = P.lift(s['lights']['ball']['position'], BALL_DROP)
    for g in s['glints'].values():
        g['at'] = P.lift(g['at'], BALL_DROP)
    drop_pools(s, BALL_DROP)
    s['title'] = s['title'].replace('(round 39, pass 3)', '(round 41, pass 4)')
    return s


def row(n):
    s = P.p3_row(n)
    if n == 'lamps-orbs':
        drop_pools(s, BALL_DROP)
    s['title'] = s['title'].replace('(round 39, pass 3)', '(round 41, pass 4)')
    return s


BUILD = {f'p4-lamp-{lamp}-{f}': (lambda lamp=lamp, f=f: {'dome': dome, 'orb': orb}[lamp](f))
         for f in P.FLAVOURS for lamp in ('dome', 'orb')}
BUILD.update({f'p4-{n}': (lambda n=n: row(n)) for n in P.ROWS})


def main():
    os.makedirs(SHOTS, exist_ok=True)
    for n, f in BUILD.items():
        s = f()
        s['render']['samples'] = 128
        json.dump(s, open(os.path.join(SHOTS, n + '.json'), 'w'), indent=1)
    print(len(BUILD), 'shots in', os.path.relpath(SHOTS, ROOT), flush=True)
    if '--render' in sys.argv:
        want = [x for x in sys.argv[sys.argv.index('--render') + 1:] if x in BUILD]
        os.makedirs(RENDERS, exist_ok=True)
        for n in want:
            subprocess.run(['python3', os.path.join(ROOT, 'studio', 'engine', 'render.py'), os.path.join(SHOTS, n + '.json'),
                            '--out', os.path.join(RENDERS, n + '.png'), '--samples', '128'], cwd=ROOT, check=True,
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            print('rendered', n, flush=True)


if __name__ == '__main__':
    main()
