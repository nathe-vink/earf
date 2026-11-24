"""Light model C for the Tropos fronts and the horn 360 (the owner, 24 Nov 04:02: "5. C"; the coordinator's 21 Nov 08:34
recommendation, critics unanimous on the S1 test, renders/2026-11-21/barkhorn/s1-test/ c): one physical light model.
  - refractive and reflective caustics on, clamp 0, filter_glossy 0;
  - the acrylics' shadow-ray shortcut cut (living_ext.no_glass_shadows, last in the set);
  - the sweep's painted contact term off (contact strength and core_strength 0): every shadow is cast by the lights.
Nothing else changes: each front is A-polished-tallr7/site-front-off-tall-<tint>.shot.json, each turn frame is
horn_turn.frame(tint, n) (the front's shot with the turn's camera and the speaker's turn), both then made model C.

    python3 spinoffs/barkhorn/campaign/light_c.py OUTDIR fronts                ->  OUTDIR/front-<tint>.json (8)
    python3 spinoffs/barkhorn/campaign/light_c.py OUTDIR turn TINT [N ...]     ->  OUTDIR/turn-<tint>-NN.json (24)
Render each with  python3 studio/engine/render.py SHOT --out PNG --masks  (no LAMPS_ROOT, no Mantle: the two models)."""
import copy, json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import horn_turn                                                          # noqa: E402
TINTS = ('acid', 'dust', 'ember', 'fog', 'haze', 'ice', 'poison', 'smoke')
EXT = 'spinoffs/barkhorn/campaign/living/living_ext.py'


def model_c(s, title):
    s = copy.deepcopy(s)
    s['render'].update(caustics_refractive=True, caustics_reflective=True, filter_glossy=0.0, clamp=0)
    s['set'].setdefault('props', []).append({'kind': 'kit', 'shape': 'ext', 'path': EXT, 'fn': 'no_glass_shadows'})
    s['set']['contact'] = {**s['set']['contact'], 'strength': 0.0, 'core_strength': 0.0}
    s['title'] = title
    return s


if __name__ == '__main__':
    od, what = sys.argv[1], sys.argv[2]
    os.makedirs(od, exist_ok=True)
    if what == 'fronts':
        for t in TINTS:
            s = json.load(open(horn_turn.FRONT.format(tint=t)))
            json.dump(model_c(s, f'Tropos front, {t}, light model C'), open(os.path.join(od, f'front-{t}.json'), 'w'), indent=1)
            print('front', t)
    elif what == 'turn':
        t = sys.argv[3]; frames = [int(x) for x in sys.argv[4:]] or list(range(24))
        for n in frames:
            s = model_c(horn_turn.frame(t, n), f'Tropos turning on the house ground, {t}, frame {n}, light model C')
            json.dump(s, open(os.path.join(od, f'turn-{t}-{n:02d}.json'), 'w'), indent=1)
        print('turn', t, len(frames), 'frames')
