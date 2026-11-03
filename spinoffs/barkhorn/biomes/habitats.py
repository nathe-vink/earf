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
    'dust':      ('Dust',   {'bounce': 0}),
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
    'ember': {'product.instances.0.rotate_z': -5, 'camera.position': [2.4349, -6.0267, 0.8],
              'lights.crack_r.target': [0.0, 0.0, 0.5], 'lights.crack_r.irradiance': 2.0},
}
SAMPLES = {'ember': 96, 'poison_g5': 96, 'haze_b': 96, 'fog_b': 96}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('out'); ap.add_argument('names', nargs='*')
    ap.add_argument('--samples', type=int, default=64); ap.add_argument('--scale', type=float, default=0.75)
    ap.add_argument('--frame', choices=['portrait', 'landscape'], default='portrait')
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    for n in a.names or HABITATS:
        tint, lights = HABITATS[n]
        shot = os.path.join(SHOTS, f'{n}-portrait.json' if a.frame == 'portrait' else f'{n}.json')
        out = os.path.join(a.out, f'{n}-{a.frame}.png')
        # horn A on its own M8 feet (base A and its light left out), direct light stopped at the horn
        cmd = [sys.executable, os.path.join(HERE, 'habitat.py'), shot, tint, '--out', out,
               '--samples', str(max(a.samples, SAMPLES.get(n, 0))), '--scale', str(a.scale), '--stand', 'feet',
               '--horn-front'] + [x for k, v in lights.items() for x in ('--light', f'{k}={v}')] \
            + [x for k, v in SETS.get(n, {}).items() for x in ('--set', f'{k}={json.dumps(v)}')]
        with open(out.replace('.png', '.log'), 'w') as log:
            r = subprocess.run(cmd, stdout=log, stderr=subprocess.STDOUT)
        print(n, 'ok' if r.returncode == 0 else f'failed ({r.returncode})', flush=True)


if __name__ == '__main__':
    main()
