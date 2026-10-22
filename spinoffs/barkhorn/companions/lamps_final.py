"""Round 35, the lamps final: Hemisphere South's hero (the ceiling wash), North and South hung together, and Core with
its taller base (its cells under the LED), lit, with the hatch underneath. The same room and the same light units as
the brightness study (hemisphere_brightness.py: a Cycles watt of white light is 683 lm, EV100 6.0), so these frames
show the light the fittings would give, not a studio's.

How each fitting's light is carried (Cycles cannot pass a lamp's light through refracting acrylic except as caustics):
- North: the COB, a Lambertian disc at its face, P = lm / 683 x 0.85 / 0.521 (the reflector; as the brightness study).
- South: its ring board sends about 57 % of its light straight out of the mouth (the rim's edge is 49 deg off the axis
  from the LED: sin2 49 = 0.57). The frosted lid passes about 85 % of that and spreads it like a Lambertian surface, so
  the wash is a Lambertian disc the lid's size just above it, P = lm x 0.57 x 0.85 / 683, facing up. The rest falls on
  the bowl's wall; the bowl's glow is the liner's emission (`shade_glow`, set by eye) and the light that leaves through
  the wall into the room a small lamp in the bowl in the tint's colour, about a third of that share (an estimate).
- Core: its LED shines up into the ball; the ball's glow is the liner's emission and the pool round it two small lamps
  just outside its equator, as in the site frames (round 32f), scaled to its 200 lm.

    python3 spinoffs/barkhorn/companions/lamps_final.py
    python3 spinoffs/barkhorn/companions/lamps_final.py --render [names] [--scale 1.0]
"""
import copy, json, os, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
sys.path.insert(0, HERE)
import hemisphere_brightness as HB                                  # noqa: E402

SHOTS = HB.SHOTS
RENDERS = os.path.join(ROOT, 'renders', '2026-10-22', 'barkhorn', 'lamps-final')
NORTH_LM = 575.0           # round 35's recommendation (README): about 370 lux across a table, half the heat
SOUTH_LM = 2 * NORTH_LM
TINT_LIGHT = {'ember': '#FF6A40', 'poison': '#B8E070', 'haze': '#B090FF', 'smoke': '#CFC4B8', 'ice': '#80D0FF',
              'acid': '#FFD060', 'dust': '#FFA070', 'fog': '#FFF0E0'}
CEIL = 2.7


def room(props=(), keep_table=True):
    """The brightness study's room and its own light, without its pendant (and its table if asked)."""
    s = HB.shot('1100', 'ember')
    s['set']['props'] = [p for p in s['set']['props'] if p.get('module') != 'earf_moon'
                         and (keep_table or p.get('kind') != 'table' and p.get('shape') not in ('cylinder', 'lathe', 'box')
                              or p.get('material') == 'glow' or (p.get('position') or [0, 0, 0])[1] > 2.5)]
    s['set']['props'] += list(props)
    del s['lights']['cob']
    return s


def north(x, y, rim_z, flavour, lm=NORTH_LM):
    piece = {'kind': 'kit', 'shape': 'ext', 'module': 'earf_moon', 'fn': 'dome', 'spots': [[x, y, rim_z]],
             'flavour': flavour, 'ceiling': CEIL, 'lamp': False, 'shade_glow': 0.0, 'hide': 'reflector'}
    light = {'type': 'area', 'shape': 'DISK', 'size_m': [0.010, 0.010], 'position': [x, y, rim_z + HB.COB_MM / 1000],
             'target': [x, y, 0.0], 'power_w': HB.cob_w(lm), 'color': 2700, 'camera': False}
    return piece, {'north_cob': light}


def south(x, y, flavour, lm=SOUTH_LM, glow=0.22):
    rim_z = CEIL - 0.50
    piece = {'kind': 'kit', 'shape': 'ext', 'module': 'earf_moon', 'fn': 'south', 'spots': [[x, y, rim_z]],
             'flavour': flavour, 'lamp': False, 'shade_glow': glow, 'noshadow': 'lid'}
    lights = {
        'south_wash': {'type': 'area', 'shape': 'DISK', 'size_m': [0.17, 0.17], 'position': [x, y, rim_z + 0.004],
                       'target': [x, y, CEIL], 'power_w': round(lm * 0.57 * 0.85 / HB.LM_PER_W, 4), 'color': 2700,
                       'camera': False},
        'south_wall': {'type': 'point', 'position': [x, y, rim_z - 0.05],
                       'power_w': round(lm * 0.43 / 3 / HB.LM_PER_W, 4), 'radius_m': 0.05,
                       'color': TINT_LIGHT[flavour], 'camera': False, 'transmission': False, 'specular': 0.0},
    }
    return piece, lights, rim_z


def hero_light(s, fill_at, target):
    """Round 35, critic r1 (3.0 and 4.0, both critics): the wall lights outshone the lamps and the black hardware read as a
    silhouette. For the heroes (not the brightness study) the room's wall lights are dimmed to 40 lm, half a stop less
    exposure keeps the ceiling's wash off white, and a soft fill from the camera's side draws the hardware."""
    for k in ('sconce1', 'sconce2'):
        s['lights'][k]['power_w'] = round(40 / HB.LM_PER_W, 4)
    for p in s['set']['props']:
        if p.get('material') == 'glow' and p.get('radius') == 0.06:
            p['emit'] = 0.45
    s['render']['exposure'] = round(s['render']['exposure'] - 0.5, 3)
    s['lights']['fill'] = {'type': 'area', 'size_m': [0.8, 0.8], 'position': fill_at, 'target': target,
                           'irradiance': 0.06, 'color': 3000, 'camera': False}
    return s


def south_hero():
    """South in Ember over the sideboard end of the room, from the table, looking up: the bowl, its glow and the wash
    on the ceiling."""
    sp, sl, rz = south(0.55, 2.45, 'ember')
    s = room([sp], keep_table=False)
    s['lights'].update(sl)
    s['title'] = 'Hemisphere South in Ember: the ceiling wash'
    s['size'] = [1600, 2000]
    # r1: closer and nearer the bowl's height, so it fills the frame and the wash reads above it
    s['camera'] = {'position': [0.16, 1.48, 1.62], 'target': [0.55, 2.45, 2.22], 'lens_mm': 33, 'level': True,
                   'fstop': 4.0, 'focus': [0.55, 2.45, 2.1]}
    return hero_light(s, [-0.2, 1.4, 1.9], [0.55, 2.45, 2.1])


def north_south():
    """North over the table, South over the sideboard, both Ember, from the room's front corner: one set of shades,
    both ways up."""
    np_, nl = north(HB.TABLE[0], HB.TABLE[1], HB.RIM_Z, 'ember')
    sp, sl, rz = south(0.55, 2.62, 'ember')
    s = room([np_, sp])
    s['lights'].update(nl); s['lights'].update(sl)
    s['title'] = 'Hemisphere North and South, one set of shades both ways up'
    s['size'] = [1800, 1200]
    # r1: closer, both pendants larger, the cut-off glass at the bottom edge out of the frame
    s['camera'] = {'position': [-0.70, 0.30, 1.50], 'target': [0.30, 1.85, 1.86], 'lens_mm': 32, 'level': True,
                   'fstop': 5.6, 'focus': [0.25, 1.6, 1.7]}
    return hero_light(s, [-0.9, 0.4, 2.0], [0.3, 1.8, 1.8])


def core_piece(x, y, z, flavour, glow=0.3, **k):
    # Core's ball is one 9 mm tinted layer where the casts were matched through 12 (the shell and the skin): the caster
    # deepens each cast by 12/9 so it reads the same, drawn here as the tint's depth (its radius) at 0.75
    r = {'smoke': 0.012, 'smoked': 0.0055}.get(flavour, 0.005) * 0.75
    # and its frost (a bead-blasted face, drawn as a 0.4 skin of the liner's material) scatters only at its surface: a
    # short subsurface radius, or the thin skin renders mottled
    k.setdefault('materials', {'body': {'radius': round(r, 5)}, 'liner': {'radius': 0.002}})
    return {'kind': 'kit', 'shape': 'ext', 'module': 'earf_moon', 'fn': 'orb',
            'spots': [{'position': [x, y, z], 'rotate_z': k.pop('rotate_z', -40)}], 'flavour': flavour,
            'lamp_w': 200 / HB.LM_PER_W * 0.6, 'shade_glow': glow, **k}


def core_hero():
    """Core in Ember on the dining table at night, lit (its 200 lm), with the room's own light: the taller base."""
    tx, ty = HB.TABLE
    s = room([core_piece(tx - 0.15, ty - 0.05, HB.TABLE_Z, 'ember')])
    s['title'] = 'Core in Ember, lit, on the table'
    s['size'] = [1600, 2000]
    for i, dx in enumerate((-0.095, 0.095)):
        s['lights'][f'corepool{i}'] = {'type': 'point', 'position': [tx - 0.15 + dx, ty - 0.07, HB.TABLE_Z + 0.06],
                                       'power_w': round(200 * 0.25 / HB.LM_PER_W, 4), 'radius_m': 0.03, 'color': '#FF8A60',
                                       'camera': False, 'transmission': False, 'specular': 0.0}
    s['lights']['tablewash'] = {'type': 'area', 'size_m': [0.6, 0.4], 'position': [tx, ty, 1.8],
                                'target': [tx, ty, HB.TABLE_Z], 'power_w': round(300 / HB.LM_PER_W, 4), 'color': 2700,
                                'camera': False, 'specular': 0.2}
    s['camera'] = {'position': [tx - 0.62, ty - 0.80, 1.02], 'target': [tx - 0.15, ty - 0.05, 0.85], 'lens_mm': 55,
                   'level': True, 'fstop': 4.0, 'focus': [tx - 0.15, ty - 0.05, 0.85]}
    return hero_light(s, [tx - 0.9, ty - 0.6, 1.3], [tx - 0.15, ty - 0.05, 0.85])


def core_under():
    """Core, off, on a glass side table, seen from below through the glass: the hatch over its cells, its four screws,
    the foot ring and the cable's notch."""
    gx, gy, gz = -1.2, 1.6, 0.45
    legs = [{'kind': 'kit', 'shape': 'cylinder', 'material': 'gloss', 'color': '#141414', 'radius': 0.008,
             'height': gz - 0.012, 'position': [gx + dx, gy + dy, 0.0]} for dx in (-0.22, 0.22) for dy in (-0.22, 0.22)]
    glass = {'kind': 'kit', 'shape': 'box', 'material': 'glass', 'color': '#F2F4F2', 'size': [0.5, 0.5, 0.012],
             'position': [gx, gy, gz - 0.012]}
    s = room(legs + [glass, core_piece(gx, gy, gz, 'smoke', glow=0.0, lamp=False, cable=False, rotate_z=200)])
    s['title'] = 'Core from below: the hatch over its cells'
    s['size'] = [1600, 1200]
    s['lights']['under'] = {'type': 'area', 'size_m': [0.6, 0.6], 'position': [gx + 0.5, gy - 0.5, 0.05],
                            'target': [gx, gy, gz], 'power_w': round(1500 / HB.LM_PER_W, 4), 'color': 3000,
                            'camera': False}
    s['camera'] = {'position': [gx + 0.30, gy - 0.42, 0.12], 'target': [gx, gy, gz], 'lens_mm': 50, 'level': False,
                   'fstop': 8.0, 'focus': [gx, gy, gz]}
    return s


# core_under is kept but not rendered: in a test the black hatch on the black base did not read (the drawings show it)
FRAMES = {'lamp-south-hero': south_hero, 'lamps-north-south': north_south, 'lamp-core-hero': core_hero}


def build():
    os.makedirs(SHOTS, exist_ok=True)
    for n, f in FRAMES.items():
        json.dump(f(), open(os.path.join(SHOTS, n + '.json'), 'w'), indent=1)
        print(n)


if __name__ == '__main__':
    a = sys.argv[1:]
    if '--render' in a:
        scale = float(a[a.index('--scale') + 1]) if '--scale' in a else 1.0
        out = a[a.index('--out') + 1] if '--out' in a else RENDERS
        HB.render([x for x in a if x in FRAMES] or list(FRAMES), scale, out)
    else:
        build()
