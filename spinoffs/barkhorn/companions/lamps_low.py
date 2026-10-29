"""Round 40: the low profiles beside the current design, for the owner (2026-10-29: "Damn I kind of liked the old light
design though, with the lower base for core and the lower profile top for hemisphere. Did we change that for technical
reasons? I feel like the new designs detract from the acrylic piece.").

One sheet, Ember, lit: round 32f as it was, the current design (round 35 to 39), and the round 40 proposal
(dome_pendant_low.py, orb_table_low.py), Hemisphere above and Core below. Each frame is pass 3's Ember hero
(lamps_pdp_r35.dome_p3 / orb_p3: the same studio, camera, lights and exposure) with the product swapped, so the heights
compare directly: only the lamp's own light and its glints follow the part they sit on.

Round 32f's models are its fab kit's GLBs as they were at 88db7379 (the branch's start), copied to out-32f/ (git
stores the same blob once), with their engine files as studio/products/earf-*-32f.json.

Round 41: the owner signed the proposal, so it is now the main build (earf-dome-pendant, earf-orb-table) and the
'low' shots point there. The 'now' column (rounds 35 to 39: the fins, the 48 base) rebuilds only from git at 950a7eaf;
its shots here are a record of round 40 and render round 41's design if run today.

    python3 spinoffs/barkhorn/companions/lamps_low.py                  # the shots and round 32f's engine files
    python3 spinoffs/barkhorn/companions/lamps_low.py --render [--samples 128]
"""
import copy, json, os, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
sys.path.insert(0, HERE)
import lamps_pdp_r35 as P                                          # noqa: E402

SHOTS = os.path.join(ROOT, 'studio', 'shots', 'barkhorn', 'lamps-low')
RENDERS = os.path.join(ROOT, 'renders', '2026-10-29', 'barkhorn', 'lamps-low')
REV32F = '88db7379'
REC = os.path.join(HERE, 'out-32f')
DROP = -0.018                 # round 32f's and the proposal's Core: the ball 18 lower (the base 48 -> 30)
DEFS = {
    ('dome', '32f'): 'studio/products/earf-dome-pendant-32f.json',
    ('dome', 'now'): 'studio/products/earf-dome-pendant.json',
    ('dome', 'low'): 'studio/products/earf-dome-pendant.json',     # round 41: the proposal is the main build
    ('orb', '32f'): 'studio/products/earf-orb-table-32f.json',
    ('orb', 'now'): 'studio/products/earf-orb-table.json',
    ('orb', 'low'): 'studio/products/earf-orb-table.json',
}
LABELS = {'32f': 'Round 32f (as it was)', 'now': 'Current (rounds 35 to 39)', 'low': 'Proposal (round 40)'}


def record_32f():
    """Round 32f's GLBs and engine files from git, renamed so they sit beside the current ones."""
    os.makedirs(REC, exist_ok=True)
    for kind, name in (('dome', 'earf-dome-pendant'), ('orb', 'earf-orb-table')):
        src = f'spinoffs/barkhorn/companions/out-{name[5:]}/render/{name}'
        glb = os.path.join(REC, name + '-32f.glb')
        if not os.path.exists(glb):
            open(glb, 'wb').write(subprocess.run(['git', 'show', f'{REV32F}:{src}.glb'], cwd=ROOT, check=True,
                                                 capture_output=True).stdout)
        d = json.loads(subprocess.run(['git', 'show', f'{REV32F}:studio/products/{name}.json'], cwd=ROOT, check=True,
                                      capture_output=True).stdout)
        d['model'] = os.path.relpath(glb, ROOT)
        d['_note'] = f'Round 32f\'s {d.get("_note", name)} As at {REV32F}, kept for round 40\'s comparison (lamps_low.py).'
        json.dump(d, open(os.path.join(ROOT, DEFS[(kind, '32f')]), 'w'), indent=1)


def dome(v):
    s = P.dome_p3('ember')
    z = s['product']['instances'][0]['position'][2]
    s['product']['def'] = DEFS[('dome', v)]
    if v != 'now':                    # the cap 34 lower (126 over the rim, was 160)
        s['glints']['cap']['at'][2] = round(z + 0.119, 4)
    s['title'] = f'Hemisphere, {LABELS[v]}: Ember (round 40)'
    return s


def orb(v):
    s = P.orb_p3('ember')
    s['product']['def'] = DEFS[('orb', v)]
    if v != 'now':
        s['lights']['ball']['position'] = P.lift(s['lights']['ball']['position'], DROP)
        for g in s['glints'].values():
            g['at'] = P.lift(g['at'], DROP)
    if v == '32f':                    # its three layers were matched lit as they are: no single-layer depth
        s['materials'] = {'liner': s['materials']['liner']}
        s['product']['hide'] = ['cartridge', 'cartridge-pads']
    s['title'] = f'Core, {LABELS[v]}: Ember (round 40)'
    return s


BUILD = {f'{lamp}-{v}': (lambda lamp=lamp, v=v: {'dome': dome, 'orb': orb}[lamp](v))
         for lamp in ('dome', 'orb') for v in ('32f', 'now', 'low')}


def sheet(out):
    """The six frames in a 3 x 2 grid, each labelled, under 5 MB."""
    tiles = []
    for lamp in ('dome', 'orb'):
        for v in ('32f', 'now', 'low'):
            name = {'dome': 'Hemisphere', 'orb': 'Core'}[lamp]
            t = os.path.join(RENDERS, f'_{lamp}-{v}-label.png')
            subprocess.run(['convert', os.path.join(RENDERS, f'{lamp}-{v}.png'), '-gravity', 'south', '-background',
                            '#F4F1EC', '-splice', '0x56', '-font', 'DejaVu-Sans', '-pointsize', '24', '-fill', '#222222',
                            '-annotate', '+0+14', f'{name}: {LABELS[v]}', t], check=True)
            tiles.append(t)
    subprocess.run(['convert', '(', *tiles[:3], '+append', ')', '(', *tiles[3:], '+append', ')', '-append',
                    '-quality', '95', out], check=True)
    for t in tiles:
        os.remove(t)


def main():
    record_32f()
    os.makedirs(SHOTS, exist_ok=True)
    for n, f in BUILD.items():
        s = f()
        s['render']['samples'] = 128
        json.dump(s, open(os.path.join(SHOTS, n + '.json'), 'w'), indent=1)
    print(len(BUILD), 'shots in', os.path.relpath(SHOTS, ROOT))
    if '--render' in sys.argv:
        a = sys.argv[sys.argv.index('--render') + 1:]
        spp = a[a.index('--samples') + 1] if '--samples' in a else '128'
        os.makedirs(RENDERS, exist_ok=True)
        for n in BUILD:
            subprocess.run(['python3', os.path.join(ROOT, 'studio', 'engine', 'render.py'), os.path.join(SHOTS, n + '.json'),
                            '--out', os.path.join(RENDERS, n + '.png'), '--samples', spp, '--scale', '0.5'], cwd=ROOT,
                           check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            print('rendered', n, flush=True)
        sheet(os.path.join(RENDERS, 'lamps-low-sheet.png'))
        print('sheet', os.path.relpath(os.path.join(RENDERS, 'lamps-low-sheet.png'), ROOT))


if __name__ == '__main__':
    main()
