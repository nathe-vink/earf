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
    'dust':      ('Dust',   {'bounce': 0}),   # the shot's 8 x 3 m 'bounce' panel stood hidden between the camera and the speaker
                                                 # (the audit, 2026-11-09: 100 % of the frame); off: the sand bounces for real (-0.1 stop)
    'acid_b':    ('Acid',   {'bounce': 0, 'throat': 0, 'low': 0, 'rim': 0}),   # rim off: the audit (2026-11-09) found the
                                                                             # hidden 1.5 m lamp in 5.4 % of the frame
    'poison_g5': ('Poison', {'reflector': 0, 'bounce': 0, 'card': 0, 'litter': 0}),   # litter: a fill lamp (2026-11-09: none)
    'ice':       ('Ice',    {'bounce': 0, 'back': 0, 'throat': 0}),
    'haze_b':    ('Haze',   {'bounce': 0}),
    'fog_b':     ('Fog',    {'bounce': 0}),
    # the home-page hero (2026-11-10): the eight in the passed Fog and Ice scenes, 3:2, the scenes' own lights only
    'hero_fog':  ('Fog',    {'bounce': 0}),
    # new designs (2026-11-11, proxies): Ember on a cooled lava field at dusk, no lava light; Smoke on a hillside under overcast
    'ember_c':   ('Ember',  {'bounce': 0, 'throat': 0, 'low': 0, 'rim': 0}),
    'smoke_c':   ('Smoke',  {'bounce': 0}),
    'hero_ice':  ('Ice',    {'bounce': 0, 'back': 0, 'throat': 0}),
}
# shot keys set per habitat (habitat.py --set), and samples where the scene is dark (the satin horn's grain)
SETS = {
    # the hero on Fog's hillside: Fog's look (5400 K, its sun's colour), the sky turned 40 deg so its own sun stands three-
    # quarter behind the group (az 150, el 5.8) and the horns glow against the fog bank; no white board (in a wide frame)
    'hero_fog': {'render.white_balance_k': 5400, 'sun.azimuth_deg': 150.0, 'sky.rotation_deg': 264.2, 'sun.color': '#FEEA98'},
    # Dust r3 (the coordinator, 2026-11-10 00:05, note 1): the sun 118 -> 124 deg, the sky turned with it (296 -> 290, its own
    # sun stays on the lamp): at 118 the sun through the horn's front wall (the horn under the rule) lit a three-ray fan of
    # glints on the inner flare's creases left of the pod (845 px over the horn-front crop); 121: 102 px, 124: 25 px (max 36)
    'dust': {'sun.azimuth_deg': 124.0, 'sky.rotation_deg': 290.0},
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
    'acid_b': {'product.instances.0.rotate_z': -8.0, 'sun.azimuth_deg': 120.0,   # (no rim: its receivers key re-made it)
               'sky.rotation_deg': 292.9, 'render.exposure': 1.0, 'sun.irradiance': 35.0,   # 0.65 -> 1.0 (the coordinator, 20:46: +0.5-0.7 if still dark; at +0.5 the sky washed out)
               # the gate on cc380fab (18:42): the storm neutral, the speaker the only yellow (a grey storm sun, no tint)
               # the lamp in the sky's own sun colour (hdri_sun: #FECC8B; a grey lamp under a warm-sunned sky is two suns' worth
               # of inconsistency, the coordinator 19:45); the white balance tint at 0 stays
               'sun.color': '#FECC8B', 'render.white_balance_tint': 0.0,
               # the near-white water in the bottom-right corner (L 205): the two dips nearest the camera 0.4 m left and
               # 0.2 m smaller, so that corner is wet rock and the channel under the speaker's reflection stays water
               'set.props.0.dips': [[0.0, 0.0, 1.1, 0.16], [-0.2, -1.2, 1.2, 0.2], [-0.95, -2.7, 1.3, 0.22],
                                    [-1.25, -4.1, 1.4, 0.22], [-1.1, -5.4, 1.4, 0.2], [2.6, 2.4, 1.6, 0.18]]},   # 28 deg off mirrored a wedge (crease 26.7), 10 deg off 13.7: 4 deg, as Ice
    # the polished horn mirrors the bright sky in one wall as a pale wedge (half an X) when it's turned far from the
    # camera; turned to about 10 deg off the camera's line it reads clean, as Ice's does (front-on gives a symmetric X)
    # (at -5, 10 deg off, Haze's narrow side face, seen near grazing, mirrored the bright sky as a flat lavender sheet;
    # -10, 5 deg off, as Ice's 4: the side barely shows)
    # (the coordinator's gate on df201486: the box a dark block, the upper two thirds at sRGB 4-8. The low sun to a
    # three-quarter back position, 135, through the right wall, as Dust's, the disk still out of frame; the sky turned
    # with it, 248.3 - (160.5 - 135); framed lower, so the horn's top sits near a third of the frame, not 46 %)
    # (then the sun round to the front side, 70, the disk and sky with it: the upper box 26 -> 38 (at 135) -> 41, the
    # horn-to-box ratio 13.7 -> 4.5, horn and box one violet, 239 / 238 deg)
    # (the engine's azimuth: 0 toward -y, the camera's side; so 70 was front-right but grazing the front face, which sat
    # in shade (the gate on 620c4bba: a near-black indigo block). 30: on the camera's side, 45 deg off its line, out of
    # frame behind the photographer, the front face lit so light enters the box; the sky and the disk turned with it)
    'haze_b': {'product.instances.0.rotate_z': -10.0, 'sun.azimuth_deg': 30.0, 'sun.elevation_deg': 6.0,
               'sky.rotation_deg': 18.8, 'camera.shift_y': -0.13,
               'render.exposure': -0.67},   # +1/3 stop on the shot's -1.0, whole frame (the critics on 1921b6fa: the box at the floor of 20-30)
    # Fog (the coordinator's gate on 45a190d1): the clear polished horn refracted the fog bank's top edge into an X.
    # The camera 0.30 m lower (lens rise 0.06 -> 0.18 keeps the framing) puts the whole horn on plain sky, and it is
    # turned 5 deg toward the front (-15 -> -10, not front-on). f/4 for a softer background; the sun's colour cooled
    # (#FEEA98 -> #FFFFFF, neutral), a photographer's white balance: the cut edges read ivory (b* 22 -> 17 at #FFF1D6)
    # (rotate_z 10 left it 20 deg off the camera's line: the left side face, with the white batt behind clear acrylic, read
    # as a flat cream sheet (the gate on the real-card Fog). -5: 5 deg off, as Haze and Ice)
    # (and a modest neutral fill from camera-left, a real panel out of frame, specular 1, unlinked: the warm dawn and the
    # golden grass were the only light on the white batts, so the clear cabinet read champagne)
    # (fill_l, the 2 x 2 m fill lamp at az -55 el 15, 3.5 m, is gone: the only emitters in a habitat are the sun and the
    # sky (the coordinator, 2026-11-09 23:42/23:48); in its place, at most, a white reflector board: REFLECT below)
    'fog_b': {
              # (and the camera's white balance at 5400 K, the coordinator's (c): the smallest that brings the cut edges'
              # medians to +5 b* or below; 5800 left them at +6)
              'render.white_balance_k': 5400,
              'product.instances.0.rotate_z': -5.0, 'sun.azimuth_deg': 110.0,
              # one sun (the audit, 2026-11-09): the sky turned so its own sun sits at the lamp's 110 deg (hdri_sun at 304.2:
              # az 110.0, el 5.8), the lamp in that sun's colour; before, the sky's sun shone from -150 and a white lamp from 110
              'sky.rotation_deg': 304.2, 'sun.color': '#FEEA98', 'camera.position': [-1.0072, -5.7119, 0.85], 'camera.shift_y': 0.18,
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
    # (and option (a), the coordinator 01:16: the canopy a quarter open, its gaps real holes in the geometry (habitat.py
    # --canopy-open), the sunfleck through one of the shot's own holes; the camera +1.5 EV for a forest floor)
    'poison_g5': {'product.instances.0.rotate_z': 9.0, 'sky.rotation_deg': 124.1,   # the sky's bright patch over the lamp (hdri_sun: -100.0, 43.3)
                  'render.exposure': 0.75,
                  # (the litter fill lamp is gone, 2026-11-09: the sun and the sky the only emitters; see HABITATS)
                  # the moss patch in the foreground sun fleck read as a hole (the gate, 18:58; the sun probe: moss_01 at 0.5, -2.5)
                  'set.props.4.avoid': [[0.0, 0.0, 0.3], [0.55, -2.5, 0.45]]},
}
# set props left out (the coordinator's gate on Dust, 2026-11-03: the tumbleweed floats, its shadow detached)
DROP = {'dust': ['tumbleweed'],
        # Poison (the coordinator's gate, 18:58): the skull and ribs in the litter before the base read as a pun on the name
        'poison_g5': ['bones']}
# set props changed per habitat, by fn: Haze's visible sun disk (an emitter in the set) moved with the key to the sun
# lamp's azimuth and elevation, out of frame, so the light in the picture has one source (the coordinator, 17:29)
MODIFY = {'haze_b': {'sundisk': {'azimuth': 30.0, 'elevation': 6.0}},
          # Fog (the coordinator's gate on 5c0f8509: the clear cabinet read champagne): the brown boulder right behind it,
          # seen through the clear walls, moved aside, so the bright fog bank sits behind the box
          'fog_b': {'boulder_01': {'position': [2.6, 3.6, -0.12]}},
          'hero_fog': {'boulder_01': {'position': [2.6, 3.6, -0.12]}},
          'smoke_c': {'boulder_01': {'position': [2.6, 3.6, -0.12]}},
          # Acid: the outline mask (no rain inside the speaker's outline, the gate on cc380fab) kept only in front of the
          # speaker (the coordinator, 20:46: the rain behind shows through the clear horn, as it would; without the mask a
          # near-focus streak 5-9 m out crossed the woofer again, proxy a2). The 2.5-5 m layer, soft, is not masked
          'acid_b': {'rain': {'outline': [0.022, 0.0, 0.27, 0.0, 1.25, 0.01], 'outline_front_only': True,
                              'outline_from': 5.1}},
          # Poison (d): the canopy's first explicit hole, whose sunfleck lit the top batt (the sun's line from the box's
          # top passes inside it), moved 1.0 m along the canopy's x, so its fleck falls on the floor 1 m to the right
          'poison_g5': {'canopy': {'holes': [[-15.362, -1.196, 0.36], [-11.625, 4.314, 0.7], [-8.031, 8.121, 0.8], [-5.531, 12.121, 0.7], [-14.125, 5.431, 0.6], [-16.615, 0.204, 0.4], [-16.306, 3.793, 0.1], [-17.438, -2.458, 0.16], [-16.55, -1.614, 0.18]]}}}
# the black flag behind the camera, per habitat (m; default 8 x 6): Haze's front mirrored it as a dead black upper half
FLAG = {'haze_b': (4.0, 3.0)}
# feet bedding per habitat (m; default 0.012, the cabinet on the ground). Acid stands in a puddle: at 12 mm its bottom sat
# exactly on the water, and the water reflected a band of sky between the edge and its reflection (the gate: "hovers")
SINK = {'acid_b': 0.05,    # 2026-11-09: 0.025 left the bottom panel's 20 mm front edge above the water, mirrored as a
                          # grey band 25-30 px under the cabinet (the trace); at 0.05 the reflection meets the walls
        # (earlier: at 0.015 a sky-bright strip (8-9 px) showed between the edge and its reflection (the gate on
                          # cc380fab: "hovers"); the puddle's displacement sits above the ray-cast surface. 0.025 closes it
                          # (strip peak 82 -> 56 against water 50); at 0.03 the submerged part showed through)
        'acid_b_old': 0.03, 'ice': 0.022, 'hero_ice': 0.022,
        # Dust (the gate on the 2026-11-09 re-render, grounded FAIL, and the passed file the same): a 6-8 px strip of lit
        # sand between the bottom edge and its shadow; the ripples are displaced at render time above the ray-cast sand.
        # 0.012 -> 0.028 beds the base into the ripples (crops at 0.02 and 0.028)
        'dust': 0.028}   # Ice ~1 cm deeper: light showed under its left front corner in the snow
# the horn's outside: polished (the owner, 2026-11-03 15:14: "Horn: polished"; satin was 0.25)
HORN_ROUGH = 0.05
# a tint's channel split from the speaker lane's shared model where it changed after the asset was built (9097, 732a8671)
SPLIT = {'acid_b': (0.085, 0.10, 1.00)}
# habitats whose sets are made real: every object seen by every ray type, casting shadows (ruling 4)
REAL_SET = {'poison_g5'}
# plants whose Poly Haven glTF has no alpha: none needed since the engine's _alpha_maps wires the published map (2026-11-09)
PLANT_ALPHA = {}
# set props added per habitat, after the shot's own (so no prop's index moves). Poison: two redwoods deep in the mist
# where the camera saw out of the set to the sky (the trace of the bluish patch under je_gray_02, 2026-11-09)
_RW = {"kind": "kit", "shape": "ext", "module": "poison_el", "fn": "redwood", "radius": 1.4, "height": 40.0, "tint": "#8A4126",
       "tint_mix": 0.3, "tex_scale": 1.4, "bump": 1.6}
ADD = {'poison_g5': [dict(_RW, position=[-5.0, 28.2, -0.1], seed=41, turn=40), dict(_RW, position=[-7.0, 32.9, -0.1], seed=42, turn=200),
                      dict(_RW, position=[-3.6, 31.5, -0.1], seed=43, turn=310)],
       # Acid (the coordinator, 20:46): splash crowns in the puddle at the speaker's foot, lightly breaking its reflection
       'acid_b': [{'kind': 'kit', 'shape': 'ext', 'module': 'acid_rain_el', 'fn': 'splashes', 'area': [-0.7, -1.6, 0.7, -0.22],
                   'z': -0.11, 'count': 28, 'radius': [0.006, 0.016], 'avoid': [[0.0, 0.0, 0.34]], 'opacity': 0.85, 'seed': 17}]}
# "Poison garden" g3 (the critics on g2, wf_621c52e9, via the coordinator 01:28): fly agaric the hero, true scarlet (sRGB
# 195, 25, 15 at its base tone), bold raised warts, every age, in clumps at varied heights with a troop in the near
# foreground; its host tree in frame (a Douglas-fir: the redwood builder with a furrowed pine bark, no buttress); red
# baneberry (Actaea rubra, glossy red berries), a true redwood-forest poison; no foxglove, nothing purple, no nightshade;
# the death caps and the arum (not Californian) out. habitats.py --garden (with GARDEN_SETS: a darker, damper mood)
_FLY = {'kind': 'kit', 'shape': 'ext', 'module': 'poison_b_el', 'fn': 'amanita', 'species': 'muscaria',
        'cap_ramp': [[0.15, '#6E0905'], [0.5, '#A3140A'], [0.9, '#C3190F'], [1.2, '#D4421A']], 'wart_size': 1.1, 'wart_rise': 0.6,
        'rough': 0.5, 'coat': 0.0}   # g4: g3's bold warts (1.45) covered the red and the viscid coat mirrored the haze: caps read pink
_WARTS = {'button': 80, 'young': 55, 'convex': 45, 'plane': 35, 'old': 25}
_BANE = {'kind': 'kit', 'shape': 'ext', 'module': 'poison_p_el', 'fn': 'baneberry'}
_FIR = {'kind': 'kit', 'shape': 'ext', 'module': 'poison_el', 'fn': 'redwood', 'bark': 'pine_bark', 'tint': '#3B2A1E',
        'tint_mix': 0.55, 'tex_scale': 0.9, 'bump': 2.2, 'res': '2k', 'flare': 0.18, 'foot': 0.8, 'lobes': 3, 'height': 35.0}
def _clump(cx, cy, specs, seed):
    """A clump: (dx, dy, cap, age, extra) offsets in metres round (cx, cy)."""
    return [dict(_FLY, position=[cx + dx, cy + dy, -0.02], cap=cap, age=age, seed=seed + k, warts=_WARTS[age], **ex)
            for k, (dx, dy, cap, age, ex) in enumerate(specs)]
GARDEN = (_clump(0.30, -2.45, [(0.0, 0.0, 0.09, 'old', {'torn': 0.4, 'lean': [0.02, 0.0]}), (0.13, 0.05, 0.07, 'plane', {}),
                               (-0.10, 0.08, 0.055, 'convex', {}), (0.06, -0.10, 0.035, 'young', {}),
                               (-0.05, -0.06, 0.025, 'button', {}), (0.20, -0.06, 0.045, 'convex', {'lean': [0.02, -0.01]})], 500)
          + _clump(-0.45, -1.45, [(0.0, 0.0, 0.075, 'plane', {}), (0.12, 0.04, 0.05, 'convex', {}),
                                  (-0.08, 0.06, 0.03, 'young', {}), (0.05, -0.08, 0.022, 'button', {})], 520)
          + _clump(0.42, -0.45, [(0.0, 0.0, 0.06, 'convex', {}), (0.08, 0.06, 0.04, 'young', {}),
                                 (-0.06, 0.05, 0.075, 'old', {'torn': 0.3})], 540)
          + [dict(_FLY, position=[-0.40, -0.30, -0.02], cap=0.05, age='plane', seed=560, warts=35),
             dict(_FLY, position=[1.05, -1.6, -0.02], cap=0.045, age='convex', seed=561, warts=45),
             dict(_FIR, position=[0.35, 2.9, -0.1], radius=0.42, seed=70, turn=40),
             dict(_BANE, position=[0.95, -1.05, -0.01], height=0.55, stems=3, berries=20, seed=601, lean=[-0.02, -0.03]),
             dict(_BANE, position=[-0.85, -0.75, -0.01], height=0.62, stems=2, berries=22, seed=602, lean=[0.03, -0.02]),
             dict(_BANE, position=[1.25, -0.15, -0.01], height=0.7, stems=2, berries=18, seed=603)])
GARDEN_DROP = ['amanita', 'arum']
GARDEN_SETS = {'render.exposure': 0.3, 'set.props.8.density': 0.03}   # g4: 0.5 left the frame as bright as P8 (the thinner mist)   # deeper shade, a little less golden haze

CANOPY_OPEN = {'poison_g5': 0.25}
# rain on the speaker (the coordinator, 20:46): beads on the front and the horn's lip, runnels; a meniscus at the waterline
# round 3 (the coordinator, 22:21): bigger drops, 3-6 mm, more of them low on the front, longer runnels (r2: 150 at 1.2-4.7 mm,
# 2 runnels 0.12-0.3 m, barely read at full size)
# round 4 (the coordinator, 22:45): the drops as spherical caps at water's ~70 deg contact angle on PMMA (h ~ 0.7 r), not
# the 0.38-flat domes of r2-r3, which barely read
WET = {'acid_b': (260, 60, 3, 1, 3.0, 6.0, 0.3, 0.55, 2.2, 70.0)}
MENISCUS = {'acid_b': 0.002}
REFLECT = {   # habitat -> [reflector specs] (W H AZ EL DIST TX TY TZ), white boards where fill lamps stood
    # Fog (b), 2026-11-10: a 2 x 2 m white board where fill_l stood (proxies: no fill left 15 % of the face under 10, the
    # board 5 %; the passed file 4 %). Poison takes none: a board where litter stood shades the floor on the sun's line
    'fog_b': [(2.0, 2.0, -55.0, 15.0, 3.5, 0.0, 0.0, 0.8)]}
BERM = {   # habitat -> [berm specs] (LX LY RX RY H, the speaker's frame, m)
    # Dust r3 (the coordinator's 00:05 note 2): sand banked 22 mm against the outside of the left face, its full depth: the
    # face's lower edge showed open-sand-bright (its 21 % Fresnel mirror of the sunlit sand behind at 73 deg, and the sand
    # through the bottom panel's edge; blocking the glass's direct light left it unchanged); 2.5 cm took it to 0.33-0.55
    # (removed for r4, the coordinator 11-10: zoomed in it read as a placed lump: (-0.30, -0.02, 0.05, 0.26, 0.022))
}
SAMPLES = {'ember': 96, 'poison_g5': 96, 'haze_b': 96, 'fog_b': 96}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('out'); ap.add_argument('names', nargs='*')
    ap.add_argument('--samples', type=int, default=64); ap.add_argument('--scale', type=float, default=0.75)
    ap.add_argument('--glossy-flag', action='store_true', help='the earlier reflection-only flag and cards (comparison)')
    ap.add_argument('--proxy', action='store_true', help='16 samples at half scale, whatever the habitat')
    ap.add_argument('--frame', choices=['portrait', 'landscape'], default='portrait')
    ap.add_argument('--set', action='append', default=[], help='an extra key=value passed to habitat.py after the habitat\'s own (diagnostics)')
    ap.add_argument('--tag', default='', help='suffix on the output name')
    ap.add_argument('--sink', type=float, help="the feet's bedding, m, in place of the habitat's (tests)")
    ap.add_argument('--scrim', type=float, nargs=4, help='a silk on the sun line: T W H D (tests)')
    ap.add_argument('--meniscus', type=float)
    ap.add_argument('--horn-as-cabinet', action='store_true', help="the horn's absorption per mm = the cabinet's")
    ap.add_argument('--manifest', help="the approved build's per-tint manifest, asserted")
    ap.add_argument('--asset', help='the speaker asset .blend, in place of assets/hornA3 (e.g. a rebuilt one)')
    ap.add_argument('--garden', action='store_true', help='Poison garden: fly agaric, foxglove, nightshade (GARDEN)')
    ap.add_argument('--berm', type=float, nargs=5, action='append', default=[], help='sand banked against the base: LX LY RX RY H')
    ap.add_argument('--reflector', type=float, nargs=8, action='append', default=[], help='a white board: W H AZ EL DIST TX TY TZ')
    ap.add_argument('--opaque-shadows', action='store_true', help='diagnostics: the glass blocks direct light')
    ap.add_argument('--crop', type=float, nargs=4, help='a region only, fractions X0 Y0 X1 Y1 (tests)')
    # the horn under the shadow rule as the cabinet, the standard for every habitat (the coordinator, 2026-11-09 22:15):
    # --horn-front was Ember's workaround (2026-11-03) for the asset's untinted shadow pass through the horn, from before
    # the per-face rule; kept only to compare with the files made with it
    ap.add_argument('--horn-front', action='store_true', help='direct light stops at the horn, as the files before 2026-11-09')
    ap.add_argument('--horn-shadows', action='store_true', help='(the default now; accepted for old queue lines)')
    # each glass face passes a shadow ray's 1 - F(theta) (Schlick, n 1.49), the default from 2026-11-09 22:29 (the coordinator;
    # the slab test: within 1.7 % of exact Fresnel at 0-75 deg, the flat sqrt(0.92) 64 % over at 75 deg)
    ap.add_argument('--flat-fresnel', action='store_true', help='the flat sqrt(0.92) a face, as the files before 2026-11-09 22:29')
    ap.add_argument('--wet', type=float, nargs='+', help='rain on the speaker: front beads, lip beads, runnels, seed')
    ap.add_argument('--card', nargs=5, action='append', default=[], help='a real card: KIND W H Z SIDE (tests)')
    ap.add_argument('--dot', nargs=5, action='append', default=[], help="a grip's dot: D SIZE TX TY TZ (tests)")
    ap.add_argument('--clearing-at', type=float, nargs=2, help="the gap's centre, world X Y (tests)")
    ap.add_argument('--clearing', type=float, help='a treefall gap this many m across in the canopy over the speaker (tests)')
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    for n in a.names or HABITATS:
        tint, lights = HABITATS[n]
        shot = os.path.join(SHOTS, f'{n}-portrait.json' if a.frame == 'portrait' else f'{n}.json')
        out = os.path.join(a.out, f'{n}-{a.frame}{a.tag}.png')
        if n in DROP or n in MODIFY or n in ADD or a.garden:
            sh = json.load(open(shot))
            drop = DROP.get(n, []) + (GARDEN_DROP if a.garden else [])
            sh['set']['props'] = [dict(p, **MODIFY.get(n, {}).get(p.get('fn') or p.get('model'), {})) for p in sh['set']['props']
                                  if p.get('fn') not in drop] + ADD.get(n, []) + (GARDEN if a.garden else [])
            shot = out.replace('.png', '.src.json')
            json.dump(sh, open(shot, 'w'), indent=1)
        # horn A on its own M8 feet (base A and its light left out), direct light stopped at the horn
        cmd = [sys.executable, os.path.join(HERE, 'habitat.py'), shot, tint, '--out', out,
               '--samples', '16' if a.proxy else str(max(a.samples, SAMPLES.get(n, 0))),
               '--scale', '0.5' if a.proxy else str(a.scale), '--stand', 'own' if a.manifest else 'feet', '--sink', str(a.sink if a.sink is not None else SINK.get(n, 0.012)),
               *(['--horn-front'] if a.horn_front else []), *([] if a.flat_fresnel else ['--fresnel-angle']),
               '--horn-rough', str(HORN_ROUGH)] + [x for k, v in lights.items() for x in ('--light', f'{k}={v}')] \
            + [x for k, v in SETS.get(n, {}).items() for x in ('--set', f'{k}={json.dumps(v)}')] \
            + [x for k, v in (GARDEN_SETS.items() if a.garden else []) for x in ('--set', f'{k}={json.dumps(v)}')] \
            + [x for kv in a.set for x in ('--set', kv)] \
            + (['--glossy-flag'] if a.glossy_flag else []) \
            + (['--flag', *map(str, FLAG[n])] if n in FLAG else []) \
            + (['--split', *map(str, SPLIT[n])] if n in SPLIT else []) \
            + (['--real-set'] if n in REAL_SET else []) \
            + (['--canopy-open', str(CANOPY_OPEN[n])] if n in CANOPY_OPEN else []) \
            + (['--canopy-clearing', str(a.clearing)] if a.clearing else []) \
            + (['--canopy-clearing-at', *map(str, a.clearing_at)] if a.clearing_at else []) \
            + (['--plant-alpha', *PLANT_ALPHA[n]] if n in PLANT_ALPHA else []) \
            + (['--scrim', *map(str, a.scrim)] if a.scrim else []) \
            + (['--wet', *map(str, a.wet or WET[n])] if (a.wet or n in WET) else []) \
            + (['--crop', *map(str, a.crop)] if a.crop else []) \
            + (['--opaque-shadows'] if a.opaque_shadows else []) \
            + (['--horn-as-cabinet'] if a.horn_as_cabinet else []) \
            + (['--asset', a.asset] if a.asset else []) \
            + (['--manifest', a.manifest] if a.manifest else []) \
            + [x for r in (a.reflector or REFLECT.get(n, [])) for x in ('--reflector', *map(str, r))] \
            + [x for b in (a.berm or BERM.get(n, [])) for x in ('--berm', *map(str, b))] \
            + (['--meniscus', str(a.meniscus or MENISCUS[n])] if (a.meniscus or n in MENISCUS) else []) \
            + [x for c in a.card for x in ('--card', *c)] \
            + [x for d in a.dot for x in ('--dot', *d)]
        with open(out.replace('.png', '.log'), 'w') as log:
            r = subprocess.run(cmd, stdout=log, stderr=subprocess.STDOUT)
        print(n, 'ok' if r.returncode == 0 else f'failed ({r.returncode})', flush=True)


if __name__ == '__main__':
    main()
