"""Light model C for the Tropos fronts and the horn 360 (the owner, 24 Nov 04:02: "5. C"; the coordinator's 21 Nov 08:34
recommendation, critics unanimous on the S1 test, renders/2026-11-21/barkhorn/s1-test/ c): one physical light model.
  - refractive and reflective caustics on, clamp 0, filter_glossy 0;
  - the acrylics' shadow-ray shortcut cut (living_ext.no_glass_shadows, last in the set), then shadow_ray_report: both
    write their counts into the frame's .report.json (`notes`), so each frame carries its own proof;
  - the sweep's painted contact term off (contact strength and core_strength 0): every shadow is cast by the lights;
  - S4b (the coordinator, 24 Nov 09:21): no reflect-only flags. A reflect-only flag (no shadow, no diffuse, unseen by
    transmission, one-sided) becomes a real black card: every ray on, two-sided, casting shadows, out of frame; an
    overhead one (facing down) comes out instead, since as a real card it shades the backdrop and the product (the
    fronts' flags 3 and 5: renders/2026-11-24/barkhorn/light-c/s4/readings.md).
Nothing else changes: each front is A-polished-tallr7/site-front-off-tall-<tint>.shot.json, each turn frame is
horn_turn.frame(tint, n) (the front's shot with the turn's camera and the speaker's turn), each horn-back and amp plate
the FA123 batch's shot file (renders/2026-11-13/barkhorn/fa123/horn-back-<tint>, macro-amp-<tint>), all made model C.

    python3 spinoffs/barkhorn/campaign/light_c.py OUTDIR fronts                ->  OUTDIR/front-<tint>.json (8)
    python3 spinoffs/barkhorn/campaign/light_c.py OUTDIR turn TINT [N ...]     ->  OUTDIR/turn-<tint>-NN.json (24)
    python3 spinoffs/barkhorn/campaign/light_c.py OUTDIR stills [TINT ...]     ->  OUTDIR/horn-back-<tint>.json, amp-<tint>.json
Render each with  python3 studio/engine/render.py SHOT --out PNG --masks  (no LAMPS_ROOT, no Mantle: the two models)."""
import copy, json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import horn_turn                                                          # noqa: E402
FA123 = os.path.join(horn_turn.ROOT, 'renders', '2026-11-13', 'barkhorn', 'fa123', '{name}-{tint}.shot.json')
TINTS = ('acid', 'dust', 'ember', 'fog', 'haze', 'ice', 'poison', 'smoke')
EXT = 'spinoffs/barkhorn/campaign/living/living_ext.py'


def real_flags(s):
    """S4b: every reflect-only flag made a real black card, or taken out if it hangs overhead facing down. Returns
    (made real, taken out) as flag indices; a flag taken out keeps its slot (`off`), so later indices hold."""
    real, out = [], []
    for i, f in enumerate(s['set'].get('flags', [])):
        if not f or f.get('off') or not f.get('reflect_only'):
            continue
        if f.get('normal', (0, 0, 0))[2] < -0.5:
            f['off'] = True; out.append(i)
        else:
            f.pop('reflect_only'); f.update(one_sided=False, camera=True, glossy=True); real.append(i)
    return real, out


def model_c(s, title):
    s = copy.deepcopy(s)
    s['render'].update(caustics_refractive=True, caustics_reflective=True, filter_glossy=0.0, clamp=0)
    s['set'].setdefault('props', []).extend([{'kind': 'kit', 'shape': 'ext', 'path': EXT, 'fn': 'no_glass_shadows'},
                                             {'kind': 'kit', 'shape': 'ext', 'path': EXT, 'fn': 'shadow_ray_report'}])
    s['set']['contact'] = {**(s['set'].get('contact') or {}), 'strength': 0.0, 'core_strength': 0.0}
    real_flags(s)
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
    elif what == 'stills':
        for t in sys.argv[3:] or TINTS:
            for name, out, what_ in (('horn-back', 'horn-back', 'horn A from behind'), ('macro-amp', 'amp', 'the amplifier plate')):
                s = model_c(json.load(open(FA123.format(name=name, tint=t))), f'Tropos, {what_}, {t}, light model C')
                json.dump(s, open(os.path.join(od, f'{out}-{t}.json'), 'w'), indent=1)
            print('stills', t)
