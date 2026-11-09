"""Apply the owner's rule on light to an existing shot file (the coordinator's rulings, 2026-11-03): shots.honest_lights
(no part-links, no specular multipliers, no light held off glass) and shots.cards_out_of_frame (a reflect-only card
only where it covers none of the frame, by ray-cast). Prints what changed and each card's coverage.

    python3 spinoffs/barkhorn/campaign/honest_shot.py IN.shot.json OUT.json [--back-off]

--back-off: the tall rig's `back` lamp off, as on the site frames (unlinked, it lit the floor and the backdrop behind
the speaker: the horn close-up's backdrop went from 6 % to 51 % clipped).
"""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import shots  # noqa: E402


def main():
    a = sys.argv[1:]
    src, dst = a[0], a[1]
    s = json.load(open(src))
    log = []
    shots.honest_lights(s, log)
    if '--back-off' in a and 'back' in s.get('lights', {}):
        s['lights']['back']['irradiance'] = 0.0
        s['lights']['back'].pop('power_w', None)
        log.append('back: off')
    shots.cards_out_of_frame(s, log)
    s['title'] = s.get('title', '') + ' (honest: the owner rule on light)'
    json.dump(s, open(dst, 'w'), indent=1)
    for line in log:
        print(line)
    for fl in s.get('set', {}).get('flags', []):
        if fl.get('reflect_only'):
            print(f"card {fl['center_m']} {fl['size_m']}: {shots.card_coverage(s, fl) * 100:.1f} % of the frame")


if __name__ == '__main__':
    main()
