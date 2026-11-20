"""The horn 360 on the house ground (the coordinator, 20 Nov 14:44): the turn of the 10 Nov set (370de3da,
renders/2026-11-04/barkhorn/rollout/A-polished-p2-p2b/turn-<tint>-NN: 24 frames, 15 degrees apart from 115, the
camera at [1.2, -2.5, 1.25] on the horn with a 125 mm lens) re-shot on the Tropos fronts' set: each frame is the
front's own shot file (A-polished-tallr7/site-front-off-tall-<tint>.shot.json: its sweep, key, fill, every lamp,
its sky, its render settings and finish block, unchanged) with only the turn's camera and the speaker's turn put in.

    python3 spinoffs/barkhorn/campaign/horn_turn.py OUTDIR TINT [SIZE_W SIZE_H] [FRAME ...]
"""
import copy, json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
RO = os.path.join(ROOT, 'renders', '2026-11-04', 'barkhorn', 'rollout')
FRONT = os.path.join(RO, 'A-polished-tallr7', 'site-front-off-tall-{tint}.shot.json')
TURN = os.path.join(RO, 'A-polished-p2-p2b', 'turn-{tint}-{n:02d}.shot.json')


def frame(tint, n, size=(1200, 1080)):
    s = json.load(open(FRONT.format(tint=tint)))
    t = json.load(open(TURN.format(tint=tint, n=n)))
    s = copy.deepcopy(s)
    s['camera'] = copy.deepcopy(t['camera'])          # the turn's framing and camera, unchanged
    rz = t['products'][0]['instances'][0]['rotate_z']
    for blk in s['products']:
        for i in blk['instances']:
            i['rotate_z'] = rz
    s['size'] = list(size)
    s['title'] = f'Tropos turning on the house ground, {tint}, frame {n}'
    return s


if __name__ == '__main__':
    od, tint = sys.argv[1], sys.argv[2]
    rest = sys.argv[3:]
    size = (1200, 1080)
    if len(rest) >= 2 and int(rest[0]) > 100:
        size = (int(rest[0]), int(rest[1])); rest = rest[2:]
    frames = [int(x) for x in rest] or list(range(24))
    os.makedirs(od, exist_ok=True)
    for n in frames:
        json.dump(frame(tint, n, size), open(os.path.join(od, f'turn-{tint}-{n:02d}.json'), 'w'), indent=1)
        print(f'turn-{tint}-{n:02d}', size)
