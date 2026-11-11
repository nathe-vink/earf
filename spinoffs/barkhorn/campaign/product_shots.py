"""Product pictures of the family (the owner, 2026-11-11 13:45: "I'd rather have better product shots. Like core on a
nice bar table. Bar images. Combo product images for monochrome, complimentary, etc."; the coordinator's brief):

    p1  core-bar-table            Core (Ember) glowing on a real bar table, close, seated eye level, shallow focus
    p2  bar-pendants              three Hemispheres over a real bar table with bar chairs, two Cores on it
    p3  combo-mono-ice            the family in Ice: a Tropos pair either side of a real cabinet, Mantle and a Core on
                                  it, a Hemisphere above; a plain studio
    p4  combo-complement-ice-dust the same, the Tropos in Ice and the lamps in Dust (Mantle in Ember: Mantle has no
                                  Dust flavour in 450064b8)

    TROPOS_BASE=A python3 spinoffs/barkhorn/campaign/product_shots.py OUTDIR      -> OUTDIR/<name>.json

Every rule of a product picture: the approved builds (shots._approved); the lamps lit only by their own LEDs at the
lamp lane's lumens (lamps_final.py); any other light a declared studio lamp outside the frame, or a real place's own
light (a Poly Haven HDRI of a real interior, named); real props are Poly Haven scans, credited.
"""
import copy, json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import shots  # noqa: E402

BAR = 'warm_bar'                    # a real bar at night (Poly Haven, CC0)
BAR_ROT = -120.0                    # its counter behind the tables (-135 puts it dead ahead: a test render, 2026-11-11)
BAR_FLOOR = 'terracotta_floor_tiles'
# the lamp lane's own settings for these lamps (lamp_site.py; the bar lane's afterhours): no clamp, caustics; denoised
LAMP_RENDER = {'samples': 96, 'adaptive': 0.01, 'denoise': True, 'clamp': 0, 'bounces': 48, 'diffuse_bounces': 16,
               'glossy_bounces': 24, 'transmission_bounces': 32, 'caustics_refractive': True, 'caustics_reflective': True,
               'view': 'Khronos PBR Neutral'}


def _asset(model, x, y, z=0.0, rz=0.0, scale=1.0):
    return {'kind': 'kit', 'shape': 'asset', 'model': model, 'res': '2k', 'position': [x, y, z], 'rotate': [0.0, 0.0, rz], 'scale': scale}


def _empty(size, title):
    return {'title': title, 'size': size, 'products': [], 'lights': {}, 'materials': {},
            'render': dict(LAMP_RENDER), 'set': {'kind': 'stage', 'props': []}}


def p1():
    """Core in Ember on a real bar table (round_wooden_table_02, its top at 0.746 m), close: an 85 mm lens at a seated
    guest's eye (1.08 m), f/2 on the Core. A second Core (Acid) on the next table along, out of focus, a bottle beside
    it. The room is warm_bar, dimmed to a bar at night (its own light, the HDRI's strength the only dial)."""
    s = _empty([1800, 1200], 'Core in Ember on a bar table (warm_bar)')
    T = 0.746
    s['set']['props'] = [
        _asset('round_wooden_table_02', 0.0, 0.0),
        _asset('round_wooden_table_02', -0.75, 1.9),
        _asset('wine_bottles_01', -0.62, 1.95, T, 70.0),
        shots._family(cores=[('ember', 0.06, 0.02, T, 200.0), ('acid', -0.85, 1.75, T, 200.0)])]
    s['sky'] = {'kind': 'hdri', 'polyhaven': BAR, 'res': '4k', 'rotation_deg': BAR_ROT, 'strength': 0.10}
    s['camera'] = {'position': [0.22, -1.32, 1.08], 'target': [0.04, 0.0, T + 0.11], 'lens_mm': 85.0, 'level': True,
                   'fstop': 2.0, 'focus': [0.06, 0.02, T + 0.12]}
    s['render'].update(exposure=1.8, white_balance_k=3400, white_balance_tint=0.0)   # (proofs: 2700 K turned the warm bar blue; at 2.6 the lamps blew to white)
    return s


def p2():
    """The same room, wider: a bar-height round table (round_wooden_table_01, 1.0 m) with three real bar chairs
    (bar_chair_round_01), three Hemispheres over it in Ember, Dust and Acid hung 0.75 m above it, two Cores on it. Our
    own floor of real terracotta tiles (the HDRI's floor is at infinity), the room beyond it the HDRI's."""
    s = _empty([1920, 1080], 'Three Hemispheres over a bar table (warm_bar)')
    T = 1.005
    s['set']['props'] = [
        {'kind': 'kit', 'shape': 'box', 'size': [9.0, 9.0, 0.01], 'position': [0.0, 1.5, -0.01],
         'material': 'pbr', 'texture': BAR_FLOOR, 'tex_res': '2k', 'gain': 0.9},
        _asset('round_wooden_table_01', 0.0, 0.0),
        *[_asset('bar_chair_round_01', 0.95 * __import__('math').sin(a), 0.95 * __import__('math').cos(a) * 0.9, 0.0, -a * 57.3)
          for a in (-2.3, 2.3, 3.14)],
        shots._family(hemis=[('ember', -0.38, 0.0, T + 0.75), ('dust', 0.0, 0.2, T + 0.85), ('acid', 0.38, 0.0, T + 0.75)],
                      cores=[('ember', -0.25, -0.2, T, 200.0), ('acid', 0.3, 0.12, T, 200.0)])]
    s['sky'] = {'kind': 'hdri', 'polyhaven': BAR, 'res': '4k', 'rotation_deg': BAR_ROT, 'strength': 0.10}
    s['camera'] = {'position': [0.35, -2.9, 1.5], 'target': [0.0, 0.0, 1.2], 'lens_mm': 40.0, 'level': True,
                   'fstop': 4.0, 'focus': [0.0, 0.0, 1.2]}
    s['render'].update(exposure=1.8, white_balance_k=3400, white_balance_tint=0.0)   # (proofs: 2700 K turned the warm bar blue; at 2.6 the lamps blew to white)
    return s


def _combo(tropos_tint, lamp_tint, mantle_flavour, title):
    """A Tropos pair either side of a real cabinet (modern_wooden_cabinet, 2.44 x 0.52 x 0.68 m), Mantle and a Core
    on it, a Hemisphere hung over it; a plain studio: a seamless ground, a large soft key high left (the site fronts'
    kind of light), a soft fill and a kicker from behind so the acrylic glows. All three studio lamps out of frame."""
    s = shots._cast_base()
    k = shots.HERO_ORDER.index(tropos_tint)
    for blk in s['products']:
        i = blk['instances'][k]
        blk['instances'] = [{**copy.deepcopy(i), 'position': [-1.58, 0.0, 0.0], 'rotate_z': 12.0},
                            {**copy.deepcopy(i), 'position': [1.58, 0.0, 0.0], 'rotate_z': -12.0}]
    shots._approved(s, order=[tropos_tint, tropos_tint])
    C = 0.68
    s['products'].append(shots._mantle(0.35, 0.02, C + 0.001, -12.0, mantle_flavour))
    s['set'] = {'kind': 'sweep', 'color': '#8F8A84', 'width': 14.0, 'front': 8.0, 'depth': 2.4, 'radius': 1.2, 'height': 5.0,
                'contact': {'strength': 0.9, 'distance_m': 0.3, 'core_strength': 1.2, 'core_distance_m': 0.03},
                'props': [_asset('modern_wooden_cabinet', 0.0, 0.05),
                          shots._family(hemis=[(lamp_tint, -0.45, 0.05, 1.72)], cores=[(lamp_tint, -0.62, 0.05, C + 0.001, 200.0)])]}
    s['materials']['sweep'] = {'roughness': 0.6}
    s['lights'] = {
        'key': {'type': 'area', 'size_m': [3.0, 3.0], 'position': [-4.2, -4.6, 3.6], 'target': [0.0, 0.0, 0.8], 'irradiance': 1.6, 'color': '#FFF6EC'},
        'fill': {'type': 'area', 'size_m': [3.0, 2.0], 'position': [4.5, -5.5, 1.6], 'target': [0.0, 0.0, 0.8], 'irradiance': 0.35, 'color': '#F4F6FF'},
        'kicker': {'type': 'area', 'size_m': [2.0, 1.0], 'position': [0.0, 1.8, 3.7], 'target': [0.0, 0.0, 0.9], 'irradiance': 3.6,
                   'spread_deg': 70, 'color': '#FFFFFF'}}
    # (proof: flat and wide, the family small in a white field: closer, a mid-grey ground, the key lower, the kicker up)
    s['camera'] = {'position': [0.0, -6.2, 1.2], 'target': [0.0, 0.0, 1.1], 'lens_mm': 50.0, 'level': True}
    s['size'] = [1800, 1200]
    s['render'].update(samples=96, exposure=0.0, denoise=True, clamp=0, caustics_refractive=True, caustics_reflective=True)
    s.pop('finish', None)
    s['title'] = title
    return s


def p3():
    return _combo('ice', 'ice', 'ice-2069', 'The family in Ice: a Tropos pair, Mantle, Core and Hemisphere (studio)')


def p4():
    return _combo('ice', 'dust', 'ember-2423', 'Ice and Dust: the Tropos pair in Ice, the lamps in Dust, Mantle in Ember (studio)')


SHOTS = {'core-bar-table': p1, 'bar-pendants': p2, 'combo-mono-ice': p3, 'combo-complement-ice-dust': p4}

if __name__ == '__main__':
    od = sys.argv[1]
    os.makedirs(od, exist_ok=True)
    for n, f in SHOTS.items():
        json.dump(f(), open(os.path.join(od, n + '.json'), 'w'), indent=1)
        print(n)
