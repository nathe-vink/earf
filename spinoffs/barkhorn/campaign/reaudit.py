"""Re-audit (2026-11-09, after the cast fix): for each rendered shot file, every hidden object (hiddencast) and every
piece of studio equipment (set flags and bounce cards, camera-visible or not) that crosses the frame, by the corrected
cast (shots._frame_rays, which now projects as Blender does). The cast ignores occlusion, so it can only overcount;
render.py's mask pass (--masks) is the pixel ground truth.

    python3 spinoffs/barkhorn/campaign/reaudit.py SHOT.json ...   (or  --git REV:PATH ...)
"""
import json, subprocess, sys

sys.path.insert(0, __file__.rsplit('/', 1)[0])
import shots, hiddencast as H  # noqa: E402


def audit(s):
    hid = [(k, n, round(c * 100, 3)) for k, n, _, c in H.hidden(s) if c > 0 and '(off)' not in k]
    eq = []
    st = s.get('set', {}) or {}
    for key in ('flags', 'bounces'):
        for c in st.get(key, []) or []:
            if c.get('camera'):
                v = shots.card_coverage(s, c)
                if v > 0:
                    eq.append((key[:-1], c.get('name', str(c['center_m'])), round(v * 100, 3)))
    return hid, eq


if __name__ == '__main__':
    args = sys.argv[1:]
    for a in args:
        if ':' in a:
            s = json.loads(subprocess.run(['git', 'show', a], capture_output=True, text=True, check=True).stdout)
            name = a.split(':', 1)[1]
        else:
            s = json.load(open(a)); name = a
        hid, eq = audit(s)
        print(f"{name.split('rollout/')[-1]}\thidden {len(hid)} {hid}\tequipment {len(eq)} {eq}")
