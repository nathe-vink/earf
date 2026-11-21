"""Tropos's weight as the site shows it (the coordinator, 21 Nov: "the site needs the number").

The parts are those of the approved front (renders/2026-11-04/barkhorn/rollout/A-polished-tallr7/
site-front-off-tall-ember.shot.json): the Cloud less its hides (the cloth disc, its own posts, sleeves and sockets, the
woofer ring) and the variants' parts less theirs (the topo horns, the outer bases, the Strata horn), no options. Each
part's mass comes from com.py's rule: the parts list's (out-cloud/bom.csv) where it gives one, else its closed mesh's
volume times its material's density. The stability clauses on these numbers are in standard-2018.md (horn A on its own
feet, 3 Nov: the same 72.6 kg).

    python3.11 spinoffs/barkhorn/stability/tropos_weight.py      ->  tropos_weight.json beside this file, and a table
"""
import json, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import com                                                               # noqa: E402

SHOT = com.ROOT / 'renders/2026-11-04/barkhorn/rollout/A-polished-tallr7/site-front-off-tall-ember.shot.json'


def main():
    s = json.load(open(SHOT))
    P, by = {}, {}
    for b in s['products']:
        i = b['instances'][0]
        got, _ = com.parts(b['def'], i.get('hide', []), tuple(i.get('options') or []))
        clash = set(got) & set(P)
        assert not clash, clash
        P.update(got); by[b['def']] = round(sum(p['mass'] for p in got.values()), 2)
    M = sum(p['mass'] for p in P.values())
    C = [sum(p['mass'] * p['c'][i] for p in P.values()) / M for i in range(3)]
    h = max(p['zmax'] for p in P.values())
    src = {}
    for p in P.values():
        k = 'parts list' if p['src'] == 'bom' else ('parts list, by volume' if 'by volume' in p['src'] else 'volume x density')
        src[k] = round(src.get(k, 0) + p['mass'], 2)
    res = dict(shot=str(SHOT.relative_to(com.ROOT)), mass_kg=round(M, 1), mass_lb=round(M / 0.45359237, 1),
               by_model_kg=by, by_source_kg=src, parts=len(P), com_m=[round(x, 4) for x in C], top_m=round(h, 4),
               heaviest=[(n, round(p['mass'], 2), p['src']) for n, p in sorted(P.items(), key=lambda kv: -kv[1]['mass'])[:15]])
    json.dump(res, open(Path(__file__).with_name('tropos_weight.json'), 'w'), indent=1)
    print('TROPOS', res['mass_kg'], 'kg', res['mass_lb'], 'lb;', res['parts'], 'parts;', by, src)
    print('CoM', res['com_m'], 'top', res['top_m'])
    for n, m, s_ in res['heaviest']:
        print(f'   {n:28s} {m:6.2f}  {s_}')


if __name__ == '__main__':
    main()
    sys.stdout.flush()
    import os; os._exit(0)
