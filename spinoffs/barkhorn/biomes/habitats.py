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
    # rotate_z: -5 mirrored a lava patch in the side panel's foot (an LED strip); -1 left the polished horn's left wall
    # mirroring the sky as a pale wedge (the gate on 8fe79529); 12 (10 deg off the camera's line) is under test
    'ember': {'product.instances.0.rotate_z': 12, 'camera.position': [2.4349, -6.0267, 0.8],
              'lights.crack_r.target': [0.0, 0.0, 0.5], 'lights.crack_r.irradiance': 2.0},
    # the coordinator's gate on Haze (2026-11-03): with the sun behind, the lining batts block the backlight and the
    # cabinet sits in its own shadow (a near-black box). The key from the side, as in Dust (sun at 118, passed)
    # (the sun lamp at 1.5 deg is lost in the grass and hills: 6 deg as Dust's; the sky's own sun disk turned with it,
    # 248.3 -> 187.8, so the sky and the lamp agree and nothing bright sits behind the speaker)
    # ruling 2 (the coordinator, 20:21): no part-links; the shot's rim lit the speaker's 99 parts alone, so it now lights
    # whatever it reaches
    # (the sky's turn: a larger rotation_deg moves the HDRI's features to smaller azimuths (Acid's proxy at 237.1 put the
    # bright sunset behind the speaker), so the sky turns by +delta where the sun turns by -delta)
    # (the coordinator's gate on 43ad3a3f: the lining near-black, 77 % of the cabinet; the same voile as Ice's, so the light:
    # the low sun behind at 148 deg, the batts block it. To three-quarter back, 120, as Dust's 118, the sky turned with it)
    # (the 9097 yellow read olive at that luminance: the camera's exposure up +0.75 EV (-0.1 -> 0.65, a global camera
    # change; the sky's p99 170 has room) and more of the low sun through a break in the rain cloud, 10 -> 18)
    'acid_b': {'product.instances.0.rotate_z': -8.0, 'lights.rim.receivers': None, 'sun.azimuth_deg': 120.0,
               'sky.rotation_deg': 292.9, 'render.exposure': 0.65, 'sun.irradiance': 35.0},   # 28 deg off mirrored a wedge (crease 26.7), 10 deg off 13.7: 4 deg, as Ice
    # the polished horn mirrors the bright sky in one wall as a pale wedge (half an X) when it's turned far from the
    # camera; turned to about 10 deg off the camera's line it reads clean, as Ice's does (front-on gives a symmetric X)
    # (at -5, 10 deg off, Haze's narrow side face, seen near grazing, mirrored the bright sky as a flat lavender sheet;
    # -10, 5 deg off, as Ice's 4: the side barely shows)
    # (the coordinator's gate on df201486: the box a dark block, the upper two thirds at sRGB 4-8. The low sun to a
    # three-quarter back position, 135, through the right wall, as Dust's, the disk still out of frame; the sky turned
    # with it, 248.3 - (160.5 - 135); framed lower, so the horn's top sits near a third of the frame, not 46 %)
    # (then the sun round to the front side, 70, the disk and sky with it: the upper box 26 -> 38 (at 135) -> 41, the
    # horn-to-box ratio 13.7 -> 4.5, horn and box one violet, 239 / 238 deg)
    'haze_b': {'product.instances.0.rotate_z': -10.0, 'sun.azimuth_deg': 70.0, 'sun.elevation_deg': 6.0,
               'sky.rotation_deg': 338.8, 'camera.shift_y': -0.13},
    # Fog (the coordinator's gate on 45a190d1): the clear polished horn refracted the fog bank's top edge into an X.
    # The camera 0.30 m lower (lens rise 0.06 -> 0.18 keeps the framing) puts the whole horn on plain sky, and it is
    # turned 5 deg toward the front (-15 -> -10, not front-on). f/4 for a softer background; the sun's colour cooled
    # (#FEEA98 -> #FFFFFF, neutral), a photographer's white balance: the cut edges read ivory (b* 22 -> 17 at #FFF1D6)
    # (rotate_z 10 left it 20 deg off the camera's line: the left side face, with the white batt behind clear acrylic, read
    # as a flat cream sheet (the gate on the real-card Fog). -5: 5 deg off, as Haze and Ice)
    'fog_b': {'product.instances.0.rotate_z': -5.0, 'sun.azimuth_deg': 110.0, 'sun.color': '#FFFFFF', 'camera.position': [-1.0072, -5.7119, 0.85], 'camera.shift_y': 0.18,
              'camera.fstop': 4.0},
    # Poison under the canopy: light through a canopy gap from the camera side and above (the opaque lining batts block
    # any light from behind: a sunfleck from the back-left left the cabinet at L 2)
    # (the gap's lamp mirrored in the polished horn's rim as a white check-mark glint and green flecks by the pod: a wider,
    # softer gap at the same irradiance, so its radiance, and so its reflection, is about a quarter; reflections at full;
    # then moved where the canopy opens, on the sun's side, front-left: the rim's check-mark was this gap mirrored;
    # then wider, softer and higher (5 x 5 m at 7, 65 deg up): at 3 m and 12 it lit the top batt to a khaki sheet and
    # drew a bright propeller in the horn's throat (my gate on the 3 m final, kept in held/))
    # (at 5 the real sun, from azimuth -100, caught the rim's lower-left lip as a white check-mark glint: 9 moves it off)
    # ruling 1: the shot's litter bounce had specular 0 (hidden in reflections); at full now
    # ruling 4 (23:47): the canopy real (every ray type), its own openings the only way light comes through; the gap lamp
    # under it (in earlier commits) is gone. The mist casts shadows (--real-set, below)
    'poison_g5': {'product.instances.0.rotate_z': 9.0, 'lights.litter.specular': 1.0},
}
# set props left out (the coordinator's gate on Dust, 2026-11-03: the tumbleweed floats, its shadow detached)
DROP = {'dust': ['tumbleweed']}
# set props changed per habitat, by fn: Haze's visible sun disk (an emitter in the set) moved with the key to the sun
# lamp's azimuth and elevation, out of frame, so the light in the picture has one source (the coordinator, 17:29)
MODIFY = {'haze_b': {'sundisk': {'azimuth': 70.0, 'elevation': 6.0}}}
# the black flag behind the camera, per habitat (m; default 8 x 6): Haze's front mirrored it as a dead black upper half
FLAG = {'haze_b': (4.0, 3.0)}
# feet bedding per habitat (m; default 0.012, the cabinet on the ground). Acid stands in a puddle: at 12 mm its bottom sat
# exactly on the water, and the water reflected a band of sky between the edge and its reflection (the gate: "hovers")
SINK = {'acid_b': 0.015,   # 3 mm under the water (at 18 mm the submerged part showed through, below the reflection's start)
        'acid_b_old': 0.03, 'ice': 0.022}   # Ice ~1 cm deeper: light showed under its left front corner in the snow
# the horn's outside: polished (the owner, 2026-11-03 15:14: "Horn: polished"; satin was 0.25)
HORN_ROUGH = 0.05
# a tint's channel split from the speaker lane's shared model where it changed after the asset was built (9097, 732a8671)
SPLIT = {'acid_b': (0.085, 0.10, 1.00)}
# habitats whose sets are made real: every object seen by every ray type, casting shadows (ruling 4)
REAL_SET = {'poison_g5'}
SAMPLES = {'ember': 96, 'poison_g5': 96, 'haze_b': 96, 'fog_b': 96}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('out'); ap.add_argument('names', nargs='*')
    ap.add_argument('--samples', type=int, default=64); ap.add_argument('--scale', type=float, default=0.75)
    ap.add_argument('--glossy-flag', action='store_true', help='the earlier reflection-only flag and cards (comparison)')
    ap.add_argument('--proxy', action='store_true', help='16 samples at half scale, whatever the habitat')
    ap.add_argument('--frame', choices=['portrait', 'landscape'], default='portrait')
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    for n in a.names or HABITATS:
        tint, lights = HABITATS[n]
        shot = os.path.join(SHOTS, f'{n}-portrait.json' if a.frame == 'portrait' else f'{n}.json')
        out = os.path.join(a.out, f'{n}-{a.frame}.png')
        if n in DROP or n in MODIFY:
            sh = json.load(open(shot))
            sh['set']['props'] = [dict(p, **MODIFY.get(n, {}).get(p.get('fn'), {})) for p in sh['set']['props']
                                  if p.get('fn') not in DROP.get(n, [])]
            shot = out.replace('.png', '.src.json')
            json.dump(sh, open(shot, 'w'), indent=1)
        # horn A on its own M8 feet (base A and its light left out), direct light stopped at the horn
        cmd = [sys.executable, os.path.join(HERE, 'habitat.py'), shot, tint, '--out', out,
               '--samples', '16' if a.proxy else str(max(a.samples, SAMPLES.get(n, 0))),
               '--scale', '0.5' if a.proxy else str(a.scale), '--stand', 'feet', '--sink', str(SINK.get(n, 0.012)),
               '--horn-front', '--horn-rough', str(HORN_ROUGH)] + [x for k, v in lights.items() for x in ('--light', f'{k}={v}')] \
            + [x for k, v in SETS.get(n, {}).items() for x in ('--set', f'{k}={json.dumps(v)}')] \
            + (['--glossy-flag'] if a.glossy_flag else []) \
            + (['--flag', *map(str, FLAG[n])] if n in FLAG else []) \
            + (['--split', *map(str, SPLIT[n])] if n in SPLIT else []) \
            + (['--real-set'] if n in REAL_SET else [])
        with open(out.replace('.png', '.log'), 'w') as log:
            r = subprocess.run(cmd, stdout=log, stderr=subprocess.STDOUT)
        print(n, 'ok' if r.returncode == 0 else f'failed ({r.returncode})', flush=True)


if __name__ == '__main__':
    main()
