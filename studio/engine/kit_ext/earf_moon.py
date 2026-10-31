"""EARF Moon, the bar lamps (round 32, spinoffs/barkhorn/companions/moon.py), as kit pieces a set can place: the fab
kit's own models (studio/products/earf-moon-table.json and earf-moon-pendant.json, their GLBs in the companions'
out-moon-*/render), with their materials in a flavour and their light set up.

    {"kind": "kit", "shape": "ext", "module": "earf_moon", "fn": "table", "spots": [[x, y, z], ...], "flavour": "smoked"}
    {"kind": "kit", "shape": "ext", "module": "earf_moon", "fn": "pendant", "spots": [[x, y, z_rim], ...], "ceiling": 3.2}

- table: `spots` the table tops the lamps stand on (metres, the foot's underside);
- pendant: `spots` the domes' rims (their lowest point); `ceiling` (metres, absolute) moves each canopy up to it and
  lengthens the cord to suit (the model's own drop is 600 mm, the canopy's top 757 above the rim);
- a spot can be {"position": [x, y, z], "flavour": ..., "rotate_z": deg} to vary one lamp;
- `flavour`: ember, dust, acid, poison, ice, haze, fog, smoke, clear, frosted or smoked;
- `lamp_w`: the hidden lamp's power (W, a Cycles point lamp; defaults 4 for the table lamp, 14 for the pendant);
  `lamp_k` its colour temperature (2700); `shade_glow`: the frosted dome's own emission (default 3.0, as the round's
  bar frames), so the frost reads lit from inside without the lamp drawing a shape through it;
- `materials`: overrides by the product's material names (body, shade, brass, steel, ...), as a shot's would be.

Round 32d, the pick (spinoffs/barkhorn/companions/crystal.py): `fn` "dome" (the pendant whose covers swap by hand;
spots its rim, `ceiling` as above) and "orb" (the cordless crystal ball; spots the table). Their frost is set within
the tint, and it is the liner that glows (`shade_glow`, default 0.25); `lamp_w` defaults 9 and 3. For a spot or the
piece: `hide` (a pattern of part names, e.g. "hub|pins|cob|gland|cord|canopy" for a spare cover alone), `cover_drop`
(m) and `cover_turn` (deg) to show the swap, and `lamp`: false for no light. `noshadow` (a pattern of part names, e.g.
COVER) makes those parts cast no shadow, so the hidden lamp lights the room through them (Cycles passes a lamp's light
through glass only as caustics; Planet's loft, f7c99a4); unset, every part casts its shadow, as before. (Planet r38:
restored here; round 32f's kit had dropped it, and the bar went dark, 25.6 to 6.5.)

Round 35 (spinoffs/barkhorn/companions/README.md): `dome` is Hemisphere (Hemisphere North in rounds 35 to 37; its fins above the cover, the cover
clamped, the COB 81.5 above the rim), `orb` is Core (its base 48 tall with its cells; one ball frosted inside, the
cartridge gone, so `cartridge` changes nothing), and `south` is Hemisphere South (dropped 2026-10-25, kept as a record; spots: the bowl's rim; no `ceiling`
stretch: the rod is 450 to the canopy's face, so put the rim 500 below the ceiling; its light, the ceiling wash from
the lid and the bowl's glow, is the shot's own to set: `lamp: false`).

Round 41 (the owner signed round 40, 2026-10-29): round 32f's low profiles again. `dome`'s fins are gone: a black crown
and an aluminium cap, the cap's top 126 above the rim, so its cord runs from 126 and the canopy's top is 776; `orb`'s
base is 30 again (three 18650 cells round the LED), its light 100.4 above the table.

Round 32f: the hardware is black (black anodised aluminium, black polished acrylic), in the GLBs themselves. The Orb
plugs in over USB-C as standard; for a spot or the piece, `cable` (default true: its black fabric cable, dressed
straight back from a notch at the back left, 420 mm) and `cartridge`: "none" (the default: the plug-in Orb, a blanking
cap in the bay), "in" (the battery cartridge fitted: cordless) or "out" (the cartridge slid `cartridge_out` m out of
the back, default 0.045, to show it). A cordless Orb is `cable: false, cartridge: "in"`.

The lamp follows Planet's loft (commit f7c99a4): hidden from the camera and from transmission (seen through rough or
frosted acrylic it read as a blob or a square), and from glossy rays (it mirrored as a hot spot in the frost); it lights
the room and the table under the dome, and the dome glows by itself. lift_shot.py can scale `lamp_w` and `shade_glow`
as room settings (glow:lamp_w=2).
"""
import math, os, sys

from mathutils import Matrix, Vector

HERE = os.path.dirname(os.path.abspath(__file__))
ENGINE = os.path.dirname(HERE)
ROOT = os.path.dirname(os.path.dirname(ENGINE))
if ENGINE not in sys.path:
    sys.path.insert(0, ENGINE)
import product as PR                                                 # noqa: E402

DEFS = {'table': 'studio/products/earf-moon-table.json', 'pendant': 'studio/products/earf-moon-pendant.json',
        'dome': 'studio/products/earf-dome-pendant.json', 'orb': 'studio/products/earf-orb-table.json',
        'south': 'studio/products/earf-hemisphere-south.json'}
# moon.TABLE_LIGHT, moon.PENDANT_LIGHT, crystal.DOME_LIGHT, crystal.ORB_LIGHT
LIGHT_MM = {'table': (0.0, 0.0, 222.0), 'pendant': (0.0, 0.0, 70.0), 'dome': (0.0, 0.0, 81.5), 'orb': (0.0, 0.0, 100.4),
            'south': (0.0, 0.0, -66.0)}    # round 41: Core's base 30 again (118.4 on rounds 35 to 39's 48); South's LED ring
LAMP_W = {'table': 4.0, 'pendant': 14.0, 'dome': 9.0, 'orb': 3.0, 'south': 9.0}
# the pendants' cords, from the cap to the canopy, and the canopy's top (mm above the rim)
CORD_MM = {'pendant': (121.0, 707.0), 'dome': (126.0, 726.0)}     # round 41: the low top's cap (160 over rounds 35 to 39's fins)
CANOPY_TOP_MM = {'pendant': 757.0, 'dome': 776.0}
# the material that glows by itself, and its default (Moon's white frost; round 32d's liner, set within the tint)
GLOW = {'table': ('shade', 3.0), 'pendant': ('shade', 3.0), 'dome': ('liner', 0.25), 'orb': ('liner', 0.25),
        'south': ('liner', 0.25)}
COVER = 'shell*|liner|skin|rim|collar|clamp|gaskets|grommet'   # a cover (Hemisphere's, Core's ball): what lifts off
_CACHE = {}


def _templates(bpy, which):
    key = (which, bpy.context.scene.name)
    if key not in _CACHE:
        pdef = PR.load_def(DEFS[which], ROOT)
        _CACHE[key] = (pdef, PR.import_model(bpy, os.path.join(ROOT, pdef['model']), pdef['origin_mm']))
    return _CACHE[key]


def _lamp(bpy, name, pos, watts, kelvin):
    import lights as L
    d = bpy.data.lights.new(name, 'POINT')
    d.energy = watts; d.shadow_soft_size = 0.02; d.specular_factor = 0.0
    L.set_color(d, kelvin)
    ob = bpy.data.objects.new(name, d); bpy.context.scene.collection.objects.link(ob)
    ob.location = pos
    ob.visible_camera = False
    ob.visible_transmission = False
    return ob


def _place(bpy, which, name, p, kit):
    pdef, tpl = _templates(bpy, which)
    gm, g0 = GLOW[which]
    over = {gm: {'glow': p.get('shade_glow', g0)}}
    for k, v in p.get('materials', {}).items():
        over[k] = {**over.get(k, {}), **v}
    mats = {}
    objs = []
    for i, spot in enumerate(p.get('spots', [p.get('position', [0, 0, 0])])):
        s = spot if isinstance(spot, dict) else {'position': spot}
        fl = s.get('flavour', p.get('flavour', 'smoked'))
        if fl not in mats:
            mats[fl] = PR.build_materials(bpy, pdef, fl, over, f'moon-{which}-{fl}')
        T = Matrix.Translation(Vector(s['position'])) @ Matrix.Rotation(math.radians(s.get('rotate_z', 0)), 4, 'Z')
        lift = 0.0
        if which in CANOPY_TOP_MM and p.get('ceiling') is not None:
            lift = p['ceiling'] - s['position'][2] - CANOPY_TOP_MM[which] / 1000
        hide = s.get('hide', p.get('hide', ''))
        # round 43: an option's parts (Hemisphere's suspension cable) stay out unless the piece asks for the option
        shown = set(s.get('options', p.get('options', [])))
        unfitted = [n for o, names in pdef.get('options', {}).items() if o not in shown for n in names]
        if unfitted:
            hide = '|'.join([h for h in [hide] + unfitted if h])
        noshadow = p.get('noshadow', '')
        cart_off = 0.0
        if which == 'orb':
            # round 32f: plug-in, the cartridge an option (none, in, out), the cable shown or not
            cart = s.get('cartridge', p.get('cartridge', 'none'))
            extra = ['cartridge*'] if cart == 'none' else ['blank']
            if not s.get('cable', p.get('cable', True)):
                extra.append('cable')
            hide = '|'.join([h for h in [hide] + extra if h])
            if cart == 'out':
                cart_off = s.get('cartridge_out', p.get('cartridge_out', 0.045))
        # the swap, shown: the cover lowered (m) and turned (deg) off its fixture
        drop, turn = s.get('cover_drop', p.get('cover_drop', 0.0)), s.get('cover_turn', p.get('cover_turn', 0.0))
        for pname, t in tpl.items():
            mname = next((r['material'] for r in pdef['assign'] if PR._match(pname, r['match'])), None)
            if mname is None or (hide and PR._match(pname, hide)):
                continue
            ob = bpy.data.objects.new(f'{name}-{pname}#{i}', t.data)
            bpy.context.scene.collection.objects.link(ob)
            ob.material_slots[0].link = 'OBJECT'; ob.material_slots[0].material = mats[fl][mname]
            M = Matrix.Identity(4)
            if (drop or turn) and PR._match(pname, COVER):
                M = Matrix.Translation((0, 0, -drop)) @ Matrix.Rotation(math.radians(-turn), 4, 'Z')
            if cart_off and PR._match(pname, 'cartridge*'):
                M = Matrix.Translation((0, cart_off, 0))
            if lift and pname == 'canopy':
                M = Matrix.Translation((0, 0, lift))
            elif lift and pname == 'cord':
                z0, z1 = CORD_MM[which][0] / 1000, CORD_MM[which][1] / 1000
                k = (z1 - z0 + lift) / (z1 - z0)
                M = Matrix.Translation((0, 0, z0)) @ Matrix.Diagonal((1, 1, k, 1)) @ Matrix.Translation((0, 0, -z0))
            ob.matrix_world = T @ M
            if noshadow and PR._match(pname, noshadow):
                ob.visible_shadow = False
            objs.append(ob)
        if s.get('lamp', p.get('lamp', True)) is False:
            continue
        pos = T @ (Vector(LIGHT_MM[which]) / 1000)
        objs.append(_lamp(bpy, f'{name}-lamp#{i}', pos, p.get('lamp_w', LAMP_W[which]), p.get('lamp_k', 2700)))
    return objs


def table(bpy, name, p, kit):
    return _place(bpy, 'table', name, p, kit)


def pendant(bpy, name, p, kit):
    return _place(bpy, 'pendant', name, p, kit)


def dome(bpy, name, p, kit):
    return _place(bpy, 'dome', name, p, kit)


def orb(bpy, name, p, kit):
    return _place(bpy, 'orb', name, p, kit)


def south(bpy, name, p, kit):
    return _place(bpy, 'south', name, p, kit)
