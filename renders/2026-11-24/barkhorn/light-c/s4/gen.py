"""S4 test (the coordinator, 24 Nov 07:33): the fronts' five reflect-only flags (set.flags 0, 1, 2, 3, 5) made real
black cards: every ray on, two-sided, casting shadows, out of frame. Everything else as the light-C front.
    python3 gen.py TINT...        -> front-<tint>-s4.json here
    python3 gen.py --s4b TINT...  -> front-<tint>-s4b.json: flags 0, 1, 2 real, the two overhead flags (3, 5) taken out
                                     (as real cards they shade the backdrop and the product: -7 and -10 grey levels each)
    python3 gen.py --conv          -> conv-dust-96.json and conv-dust-768.json (Dust's right side and base, a crop)"""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); SRC = os.path.dirname(HERE)
FLAGS = [0, 1, 2, 3, 5]


def s4(tint):
    s = json.load(open(os.path.join(SRC, f'front-{tint}.json')))
    for i in FLAGS:
        f = s['set']['flags'][i]
        f.pop('reflect_only', None)
        f.update(one_sided=False, camera=True, glossy=True)
    s['title'] = s.get('title', '') + ' (S4: flags 0-3, 5 real cards)'
    return s


if __name__ == '__main__':
    if sys.argv[1:2] == ['--s4b']:
        for t in sys.argv[2:]:
            s = json.load(open(os.path.join(SRC, f'front-{t}.json')))
            for i in (0, 1, 2):
                f = s['set']['flags'][i]; f.pop('reflect_only', None); f.update(one_sided=False, camera=True, glossy=True)
            for i in (3, 5):
                s['set']['flags'][i]['off'] = True
            s['title'] = s.get('title', '') + ' (S4b: flags 0-2 real cards, 3 and 5 out)'
            json.dump(s, open(os.path.join(HERE, f'front-{t}-s4b.json'), 'w'), indent=1)
    elif sys.argv[1:] == ['--conv']:
        for n in (96, 768):
            s = json.load(open(os.path.join(SRC, 'front-dust.json')))
            s['render'].update(samples=n, adaptive=0.01 if n == 96 else 0.001)
            s['title'] = s.get('title', '') + f' (convergence crop, {n} spp)'
            json.dump(s, open(os.path.join(HERE, f'conv-dust-{n}.json'), 'w'), indent=1)
    else:
        for t in sys.argv[1:]:
            json.dump(s4(t), open(os.path.join(HERE, f'front-{t}-s4.json'), 'w'), indent=1)
            print(t)
