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

DEFS = {'table': 'studio/products/earf-moon-table.json', 'pendant': 'studio/products/earf-moon-pendant.json'}
LIGHT_MM = {'table': (0.0, 0.0, 222.0), 'pendant': (0.0, 0.0, 70.0)}   # moon.TABLE_LIGHT, moon.PENDANT_LIGHT
LAMP_W = {'table': 4.0, 'pendant': 14.0}
CORD_MM = (121.0, 707.0)            # the pendant's cord, from the cap to the canopy; the canopy's top at 757
CANOPY_TOP_MM = 757.0
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
    over = {'shade': {'glow': p.get('shade_glow', 3.0)}}
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
        if which == 'pendant' and p.get('ceiling') is not None:
            lift = p['ceiling'] - s['position'][2] - CANOPY_TOP_MM / 1000
        for pname, t in tpl.items():
            mname = next((r['material'] for r in pdef['assign'] if PR._match(pname, r['match'])), None)
            if mname is None:
                continue
            ob = bpy.data.objects.new(f'{name}-{pname}#{i}', t.data)
            bpy.context.scene.collection.objects.link(ob)
            ob.material_slots[0].link = 'OBJECT'; ob.material_slots[0].material = mats[fl][mname]
            M = Matrix.Identity(4)
            if lift and pname == 'canopy':
                M = Matrix.Translation((0, 0, lift))
            elif lift and pname == 'cord':
                z0, z1 = CORD_MM[0] / 1000, CORD_MM[1] / 1000
                k = (z1 - z0 + lift) / (z1 - z0)
                M = Matrix.Translation((0, 0, z0)) @ Matrix.Diagonal((1, 1, k, 1)) @ Matrix.Translation((0, 0, -z0))
            ob.matrix_world = T @ M
            objs.append(ob)
        pos = T @ (Vector(LIGHT_MM[which]) / 1000)
        objs.append(_lamp(bpy, f'{name}-lamp#{i}', pos, p.get('lamp_w', LAMP_W[which]), p.get('lamp_k', 2700)))
    return objs


def table(bpy, name, p, kit):
    return _place(bpy, 'table', name, p, kit)


def pendant(bpy, name, p, kit):
    return _place(bpy, 'pendant', name, p, kit)
