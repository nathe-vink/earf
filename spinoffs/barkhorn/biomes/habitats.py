"""The seven habitats (Smoke has smoke_align.py) on the speaker lane's model, by one rule (r48-biomes, 2026-11-03).

    python3.11 spinoffs/barkhorn/biomes/habitats.py OUTDIR [NAME ...] [--samples 64] [--scale 0.75] [--frame portrait]

Each habitat's live shot (elements/build.py writes them to studio/shots/barkhorn/element31/) rendered through
habitat.py: horn A linked (on its own feet, settled onto the set), the speaker lane's welded volume glass, a black flag
and side cards, light off by day. The owner's notes (2026-11-03): see-through, grounded, no light thrown down, the
current horn. The shots' speaker fills (bounces, reflectors and lamps set close behind the speaker for the old model)
light the white lining from inside, and the walls then read as painted white sheets, so they are off. What the scene
itself motivates stays: lava cracks, a river's glow, ground light, a thin rim.
"""
import argparse, json, os, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
SHOTS = os.path.join(ROOT, 'studio', 'shots', 'barkhorn', 'element31')

# name -> (tint, {lamp: factor}); 0 drops a lamp
HABITATS = {
    'ember':     ('Ember',  {'through': 0, 'horn': 0, 'face': 0}),
    'dust':      ('Dust',   {'bounce': 0.35}),   # the sand's bounce, low: lifts the bottom wall, no white faces
    'acid_b':    ('Acid',   {'bounce': 0, 'throat': 0, 'low': 0, 'rim': 0.3}),
    'poison_g5': ('Poison', {'reflector': 0, 'bounce': 0, 'card': 0}),
    'ice':       ('Ice',    {'bounce': 0, 'back': 0, 'throat': 0}),
    'haze_b':    ('Haze',   {'bounce': 0}),
    'fog_b':     ('Fog',    {'bounce': 0}),
}
# shot keys set per habitat (habitat.py --set), and samples where the scene is dark (the satin horn's grain)
SETS = {
    # the coordinator's gate on Ember (2026-11-03): a three-quarter view so the side panel carries the lava through the
    # red (the right crack's lamp, on that crack, aimed at the speaker), the camera lower so the horn clears the ridge
    # rotate_z -1, not -5: at -5 the side panel's foot mirrored a lava patch as a hot streak, read as an LED strip
    'ember': {'product.instances.0.rotate_z': -1, 'camera.position': [2.4349, -6.0267, 0.8],
              'lights.crack_r.target': [0.0, 0.0, 0.5], 'lights.crack_r.irradiance': 2.0},
    # the coordinator's gate on Haze (2026-11-03): with the sun behind, the lining batts block the backlight and the
    # cabinet sits in its own shadow (a near-black box). The key from the side, as in Dust (sun at 118, passed)
    # (the sun lamp at 1.5 deg is lost in the grass and hills: 6 deg as Dust's; the sky's own sun disk turned with it,
    # 248.3 -> 187.8, so the sky and the lamp agree and nothing bright sits behind the speaker)
    'haze_b': {'sun.azimuth_deg': 100.0, 'sun.elevation_deg': 6.0, 'sky.rotation_deg': 187.8},
    'fog_b': {'sun.azimuth_deg': 110.0},
    # Poison under the canopy: light through a canopy gap from the camera side and above (the opaque lining batts block
    # any light from behind: a sunfleck from the back-left left the cabinet at L 2)
    'poison_g5': {'lights.skygap': {'type': 'area', 'size_m': [1.6, 1.6], 'target': [0.0, 0.0, 0.6], 'irradiance': 12.0,
                                    'color': '#EEF2E2', 'orbit': {'azimuth_deg': 30, 'elevation_deg': 55, 'distance_m': 3.0},
                                    'specular': 1.0}},
}
# set props left out (the coordinator's gate on Dust, 2026-11-03: the tumbleweed floats, its shadow detached)
DROP = {'dust': ['tumbleweed']}
# feet bedding per habitat (m; default 0.012, the cabinet on the ground). Acid stands in a puddle: at 12 mm its bottom sat
# exactly on the water, and the water reflected a band of sky between the edge and its reflection (the gate: "hovers")
SINK = {'acid_b': 0.03, 'ice': 0.022}   # Ice ~1 cm deeper: light showed under its left front corner in the snow
# the horn's outside: polished (the owner, 2026-11-03 15:14: "Horn: polished"; satin was 0.25)
HORN_ROUGH = 0.05
SAMPLES = {'ember': 96, 'poison_g5': 96, 'haze_b': 96, 'fog_b': 96}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('out'); ap.add_argument('names', nargs='*')
    ap.add_argument('--samples', type=int, default=64); ap.add_argument('--scale', type=float, default=0.75)
    ap.add_argument('--proxy', action='store_true', help='16 samples at half scale, whatever the habitat')
    ap.add_argument('--frame', choices=['portrait', 'landscape'], default='portrait')
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    for n in a.names or HABITATS:
        tint, lights = HABITATS[n]
        shot = os.path.join(SHOTS, f'{n}-portrait.json' if a.frame == 'portrait' else f'{n}.json')
        out = os.path.join(a.out, f'{n}-{a.frame}.png')
        if n in DROP:
            sh = json.load(open(shot))
            sh['set']['props'] = [p for p in sh['set']['props'] if p.get('fn') not in DROP[n]]
            shot = out.replace('.png', '.src.json')
            json.dump(sh, open(shot, 'w'), indent=1)
        # horn A on its own M8 feet (base A and its light left out), direct light stopped at the horn
        cmd = [sys.executable, os.path.join(HERE, 'habitat.py'), shot, tint, '--out', out,
               '--samples', '16' if a.proxy else str(max(a.samples, SAMPLES.get(n, 0))),
               '--scale', '0.5' if a.proxy else str(a.scale), '--stand', 'feet', '--sink', str(SINK.get(n, 0.012)),
               '--horn-front', '--horn-rough', str(HORN_ROUGH)] + [x for k, v in lights.items() for x in ('--light', f'{k}={v}')] \
            + [x for k, v in SETS.get(n, {}).items() for x in ('--set', f'{k}={json.dumps(v)}')]
        with open(out.replace('.png', '.log'), 'w') as log:
            r = subprocess.run(cmd, stdout=log, stderr=subprocess.STDOUT)
        print(n, 'ok' if r.returncode == 0 else f'failed ({r.returncode})', flush=True)


if __name__ == '__main__':
    main()
