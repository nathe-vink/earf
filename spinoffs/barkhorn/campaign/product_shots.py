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


HEMI_SCALE = float(os.environ.get('HEMI_SCALE', '1.0'))   # the owner, 16:15: Hemisphere stays its size, hung in multiples
CORE_BASE = None    # (the owner, 16:25: Core's base satin black; the lamps lane's own material since r32-lamps-final 7c359b88, so no override)
LAMPS = 'spinoffs/barkhorn/campaign/stage/stage2_props.py'


def _pbr(tex, **k):
    return {'material': 'pbr', 'texture': tex, 'tex_res': '2k', **k}


BAR_BW = 1.45                         # our bar's brick wall (y)
BAR_EV_P1, BAR_EV_P2 = -5.0, -4.5     # the lamps lane's: Core -5, Hemisphere -2 (a frame of both: between)
BAR_ROOM_P1, BAR_ROOM_P2 = 1.0, 1.0   # the declared room light's scale, set so the brick and wood read at that exposure


def _bar_set():
    """Our bar: a red brick wall close behind, a brushed concrete floor, a dark wood back bar on the brick, the round
    table and two iron stools (Poly Haven scans)."""
    BW = BAR_BW
    return [
        {'kind': 'kit', 'shape': 'box', 'size': [12.0, 10.0, 0.02], 'position': [0.0, -3.5, -0.02], **_pbr('brushed_concrete', gain=0.75)},
        {'kind': 'kit', 'shape': 'box', 'size': [12.0, 0.25, 4.5], 'position': [0.0, BW + 0.125, -0.02], **_pbr('red_brick', gain=0.95)},
        {'kind': 'kit', 'shape': 'box', 'size': [2.6, 0.42, 0.045], 'position': [0.55, BW - 0.21, 1.1], **_pbr('dark_wood')},
        _asset('round_wooden_table_02', 0.0, 0.0),
        _asset('metal_stool_01', -0.66, 0.22, 0.0, 30.0), _asset('metal_stool_01', 0.68, 0.38, 0.0, -40.0)]


def _bar_lights(k=1.0):
    """The room's declared light, both out of frame: a dusk window to the right (cool) and a doorway to the left (warm,
    the next room's light), at the lamps' exposure (about 2^7 times the first version's window)."""
    return {'dusk-window': {'type': 'area', 'size_m': [1.6, 2.0], 'position': [3.2, -0.6, 1.7], 'target': [0.0, 0.6, 1.0],
                            'irradiance': round(6.0 * k, 3), 'color': '#9FB3DA'},
            'doorway': {'type': 'area', 'size_m': [1.0, 2.1], 'position': [-3.0, -0.4, 1.05], 'target': [0.0, 0.8, 0.9],
                        'irradiance': round(3.0 * k, 3), 'color': '#FFD9B0'}}


def p1():
    """Core in Ember on the round table of our own bar (the coordinator, 16:40: "re-shoot it in THIS bar"): close, an
    85 mm lens at a seated guest's eye, f/2 on the Core, the brick and the back bar soft behind, no other lamp or bright
    shape in frame, its dock's cable out of the back (the lamp at rot 0). Exposed as the lamps lane exposes Core (AgX,
    Punchy, -5 EV, no white balance) so the ball holds Ember's red to the centre; the room brought up to it by the
    declared dusk window and doorway, both out of frame."""
    s = _empty([1800, 1200], 'Core in Ember on a table in our bar')
    T = 0.746
    s['set']['props'] = _bar_set() + [
        {'kind': 'kit', 'shape': 'ext', 'path': LAMPS, 'fn': 'lamps', 'led_k': shots.LED_K, 'core_load': shots.CORE_LOAD,
         'cores': [{'tint': 'red', 'x': 0.06, 'y': 0.02, 'floor_z': T, 'rot': 0.0}]}]
    s['sky'] = {'kind': 'gradient', 'strength': 0.0}
    s['lights'] = _bar_lights(BAR_ROOM_P1)
    s['camera'] = {'position': [0.25, -1.30, 1.06], 'target': [0.04, 0.0, T + 0.12], 'lens_mm': 85.0, 'level': True,
                   'fstop': 2.0, 'focus': [0.06, 0.02, T + 0.12]}
    s['render'].update(view='AgX', look='AgX - Punchy', exposure=BAR_EV_P1)
    s['render'].pop('white_balance_k', None)
    return s


def p2():
    """A corner of a bar of our own (the owner, 16:05: "Red brick, wood, cement textures mostly. No TVs"; 15:43: "classy
    and refined"), built from scanned materials: a red brick wall (red_brick) close behind, a brushed concrete floor
    (brushed_concrete), a dark wood back bar along the brick with Mantle on it (dark_wood), a real table
    (round_wooden_table_02) and two metal stools (metal_stool_01, black iron, leather). A cluster of five Hemispheres
    low over the table, close, at different heights (the owner, 16:15), at their own size; two Cores on it. The only
    light sources in frame are EARF's lamps; the rest is one declared dusk window out of frame to the right, cool and
    low. No HDRI. (Proof 1: too dark, the lamps hung high, the Tropos pair at the frame's edges unreadable: the wall
    nearer, the lamps lower, tighter, the pair dropped.)"""
    s = _empty([1920, 1080], 'A cluster of Hemispheres over a table in a brick bar of our own')
    T = 0.746
    s['set']['props'] = _bar_set() + [
        {'kind': 'kit', 'shape': 'ext', 'path': LAMPS, 'fn': 'lamps', 'hemi_scale': HEMI_SCALE, 'top_z': 3.6,
         'led_k': shots.LED_K, 'core_load': shots.CORE_LOAD, **({'core_base': CORE_BASE} if CORE_BASE else {}),
         # a cluster of five over the table, close, at different heights, the lowest 0.42 m over the top
         'hemispheres': [{'tint': shots.KEY[t], 'x': x, 'y': y, 'rim_z': z} for t, x, y, z in
                         (('ember', -0.26, -0.04, 1.17), ('dust', -0.05, 0.16, 1.33), ('acid', 0.15, -0.09, 1.22),
                          ('ember', 0.32, 0.12, 1.41), ('dust', 0.04, -0.22, 1.48))],
         'cores': [{'tint': shots.KEY[t], 'x': x, 'y': y, 'floor_z': T, 'rot': 0.0} for t, x, y in (('ember', -0.17, -0.1), ('acid', 0.2, 0.08))]}]
    # (16:40: Mantle out, lost in the dark: this is a lamps picture)
    s['sky'] = {'kind': 'gradient', 'strength': 0.0}
    s['lights'] = _bar_lights(BAR_ROOM_P2)
    # (proof 2: the table cut at the foot, the top lamp at the head: a little wider)
    s['camera'] = {'position': [0.28, -2.05, 1.12], 'target': [0.12, 0.4, 1.08], 'lens_mm': 36.0, 'level': True,
                   'fstop': 2.8, 'focus': [0.0, 0.0, 0.95]}
    # (16:40: exposed for the lamps, as the lamps lane does: AgX, Punchy, no white balance; the room brought up to it)
    s['render'].update(view='AgX', look='AgX - Punchy', exposure=BAR_EV_P2)
    s['render'].pop('white_balance_k', None)
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
