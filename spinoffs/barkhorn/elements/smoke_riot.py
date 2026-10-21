"""Smoke, setting E9: the bridge, with smoke that moves like smoke (the owner, 2026-10-21: "I wanted bridge smoke. That
smoke looks bad").

E7's overpass at blue hour, rebuilt around one change: the smoke is simulated, not drawn. `plume_sim.py` solves the
flow of a car fire's hot gas, so the soot rolls into lobes on every scale, leans with a light wind and rises out of
frame, and the flames are the hottest part of that same flow, not a separate glowing box. The near wreck burns in the
cabin and the engine bay, its fire lighting the road and the speaker's flank; two more fires further along the bridge
and in the city send their own columns up, so the sky is smoke from edge to edge, as in a news photograph of a riot.

The speaker stands untouched on the wet deck in the foreground. An empty aftermath: no people.
"""
from common import area, camera, finish, piece, point, shot as frame, portrait_of, sky
from smoke import SHELL, SPEAKER
from smoke_bridge import DECK_HALF, deck, lamps, wreck

SKY = 'sunset_jhbcentral'                   # a city skyline at twilight from a rooftop (Poly Haven, CC0)
CACHE = 'renders/2026-10-21/barkhorn/plume/plume_a.npz'
WIND = 145.0                                # the sim's downwind +x turned left and away: the smoke leans left in frame
# the wrecks: (x, y, heading in degrees, paint left showing, burning); the burning one lies along the wind, as the
# sim's fire does
WRECKS = [(-1.2, 15.0, 145.0, 0.05, True), (3.6, 21.0, 20.0, 0.12, False), (-3.4, 29.0, 70.0, 0.08, False)]
# the far fires: (x, y, scale), down the bridge and out over the city
FAR = [(20.7, 150.0, 2.0), (-45.0, 230.0, 2.6)]          # left of the speaker, both drifting left: the sky behind its horn stays clear


def plume(x, y, scale=1.0, density=4.5, strength=320.0, seed=0, near=True):
    """Soot brown-grey enough that the dusk sky lifts its tops (p3's critics: "black cotton wool"), torn and firm at the
    edges (p4's: "mushy"), uneven inside; flames that clip yellow-white at their cores and break into hard-edged tongues
    (p4's: "a soft, creamy glow"). The far fires take fewer noise octaves: their detail is below a pixel, and each octave
    is paid at every step of every ray."""
    oct = (4.0, 2.0, 3.0) if near else (2.0, 1.0, 2.0)
    return piece('ext', module='plume', fn='plume', cache=CACHE, position=[x, y, 0.0], rotate_z=WIND, scale=scale,
                 density=density / scale, strength=strength, color='#8F857B', anisotropy=0.4, cool=1100.0, hot=2100.0,
                 flame_floor=0.25, tongues=0.9, tongue_scale=0.22 * scale, tongue_edge=[0.42, 0.62], edge=[0.02, 0.22],
                 detail=2.5 if near else 1.5, detail_scale=0.18 * scale, detail_octaves=oct[0],
                 breakup=0.45 if near else 0.3, breakup_scale=0.7 * scale, breakup_octaves=oct[1], tongue_octaves=oct[2],
                 seed=seed)


def burning_wreck(x, y, heading, paint_left, seed):
    """The burning saloon whole: its roof on (E7's sag read as a flat slab with a tube on top), seen three-quarter."""
    return piece('ext', module='wreck', fn='sedan', position=[x, y], heading=heading, paint='#2B3036',
                 paint_left=paint_left, crumple=0.2, sag=0.0, seed=seed)


def shot():
    props = deck()
    lp, lights = lamps()
    props += lp
    # the contact shadow: a shadow-only disc in the cabinet's base, blocking the sky and lamps over the road beneath it
    props.append(piece('ext', module='smoke_el', fn='occluder', position=[0.0, 0.0, 0.012], radius=0.5, sx=1.0, sy=0.85,
                       rotate_z=18.0))
    lights.update({
        'skyfill': {**area(-20, 5, 2.4, 1.6, '#AEB8C8', (4.0, 3.0), (0.0, 0.0, 0.6)), 'receivers': SPEAKER},
        'bounce': {**area(-25, 12, 2.0, 4.0, '#C9BBA8', (2.4, 2.4), (0.0, 0.0, 0.6)), 'receivers': SPEAKER},
        'kicker': {**area(-150, 22, 3.0, 30.0, '#FF9A50', (0.5, 2.4), (0.0, 0.0, 0.8)), 'receivers': SHELL},
        'kicker_r': {**area(150, 14, 3.0, 20.0, '#FFB070', (0.6, 2.4), (0.0, 0.0, 0.8)), 'receivers': SHELL},
    })
    for i, (x, y, heading, paint_left, burning) in enumerate(WRECKS):
        props.append((burning_wreck if burning else wreck)(x, y, heading, paint_left, 11 + i))
        if burning:
            props.append(plume(x, y, seed=3))
            props.append(piece('scatter', count=25, radius=[0.003, 0.008], position=[x, y, 1.6], material='glow',
                               color='#FF8A30', emit=25.0, seed=50 + i,
                               plume={'height': 7.0, 'spread': [0.3, 2.4], 'lean': [-3.0, 0.5], 'taper': 0.7}))
            # the fire's light from among the flames, just above the roof: it lights the road, the speaker's flank and
            # the lowest billows (p3: "the underside is unlit"; p4 at 26 kW and 2 m: "a smooth orange haze")
            lights[f'fire{i}'] = point([x, y, 1.6], 14000.0, '#FF7A2E', 1.0)
            lights[f'firerim{i}'] = {'type': 'area', 'size_m': [1.0, 1.0], 'position': [x * 0.4, y * 0.4, 1.3],
                                     'target': [0.0, 0.0, 0.8], 'irradiance': 120.0, 'color': '#FF8A3A', 'receivers': SHELL}
    for k, (x, y, s) in enumerate(FAR):
        props.append(plume(x, y, scale=s, seed=7 + k, near=False))
        lights[f'farfire{k}'] = point([x, y, 1.2 * s], 25000.0 * s * s, '#FF7A2E', 1.0 * s)
    cam = camera(height=0.8, distance=5.0, azimuth=-12, lens=35, target=(0.0, 0.0, 0.85), fstop=2.8, shift_y=0.14)
    cam['clip_end'] = 3000
    s = frame('smoke_riot', props, cam, sky(SKY, rotation_deg=0.0, strength=0.6),
              'barkhorn, Smoke, the bridge with simulated smoke', lights=lights, rotate_z=18.0, position=(0.0, 0.0, 0.0),
              samples=512, exposure=0.0,
              fin={**finish(contrast=0.06, clarity=0.04, bloom=0.2, bloom_px=40, threshold=0.7, vignette=0.25), 'grain': 2.5})
    s['render']['volume_bounces'] = 1
    return s


def portrait():
    sh = shot()
    return portrait_of(sh, **camera(height=0.8, distance=4.2, azimuth=-12, lens=35, target=(0.0, 0.0, 0.85), fstop=4.0,
                                    shift_y=0.16))
