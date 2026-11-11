"""The lamps as the lamp lane finished them (r32-lamps-final), placed in an engine scene: Hemisphere (the pendant, its
up-facing ring of 24 LEDs, about 1,000 lm, the 24 LED faces its only emitters) and Core (the cordless table lamp, its
Ø26 LED disc, 200 lm at the LED; the white opal ball inside the tinted one). Built by the lane's own code,
spinoffs/barkhorn/companions/lamp_site.py, so the lamps are exactly those of its pictures, on its photometric scale
(0.0065 W of Blender power a lumen).

A set prop: {"kind": "kit", "shape": "ext", "path": "spinoffs/barkhorn/planet/afterhours/lamps_final.py", "fn": "place",
 "hemispheres": [{"tint": "red", "x": .., "y": .., "rim_z": ..}], "cores": [{"tint": .., "x": .., "y": .., "floor_z": .., "rot": 0}],
 "led_k": {"red": 2200, ...}, "core_load": {"orange": 1.5, ...}}
Tints by the site's keys: red Ember, orange Dust, amber Acid, green Poison, blue Ice, violet Haze, ice Fog, black Smoke.

The lane's code is read from LAMPS_ROOT (a checkout of r32-lamps-final, default ../lamps-wt beside the repo; the commit
is printed and kept in the scene) and run up to the point where its own frame would begin: no paper, no studio light, no
world of its own. Nothing else is changed.
"""
import os, subprocess, sys, types


def _lane(root):
    src_path = os.path.join(root, 'spinoffs', 'barkhorn', 'companions', 'lamp_site.py')
    src = open(src_path).read()
    a = "    bpy.ops.wm.read_factory_settings(use_empty=True)\n"
    b = "    # --- the set: a pale paper sweep"
    assert a in src and b in src, 'lamp_site.py has changed: the embed hooks no longer match'
    src = src.replace(a, "    pass   # (embedded: the engine's scene is kept)\n", 1)
    src = src.replace(b, "    if frame == 'dome-embed':\n        return {'hemisphere': hemisphere, 'core': core}\n" + b, 1)
    mod = types.ModuleType('lamp_site_embedded'); mod.__file__ = src_path
    exec(compile(src, src_path, 'exec'), mod.__dict__)
    return mod


def place(bpy, name, p, kit):
    root = os.environ.get('LAMPS_ROOT') or p.get('lamps_root')
    if not root:
        raise SystemExit('lamps_final: set LAMPS_ROOT to a checkout of r32-lamps-final')
    try:
        sha = subprocess.run(['git', 'rev-parse', 'HEAD'], cwd=root, capture_output=True, text=True).stdout.strip()
    except Exception:
        sha = '?'
    print('LAMPS lamp_site from', root, sha)
    L = _lane(root)
    L.LED_CCT.update(p.get('led_k', {}))
    before = set(bpy.context.scene.objects)
    world = bpy.context.scene.world
    f = L.build('dome-embed', 64, 1.0)
    for h in p.get('hemispheres', []):
        f['hemisphere'](h['tint'], h['x'], h['rim_z'], y=h['y'])
    load0 = os.environ.get('CORE_LOAD')
    for c in p.get('cores', []):
        os.environ['CORE_LOAD'] = str(p.get('core_load', {}).get(c['tint'], 0.5))
        f['core'](c['tint'], c['x'], c['floor_z'], y=c['y'], rot=c.get('rot', 0.0))
    if load0 is None:
        os.environ.pop('CORE_LOAD', None)
    else:
        os.environ['CORE_LOAD'] = load0
    bpy.context.scene.world = world
    new = [o for o in bpy.context.scene.objects if o not in before]
    for o in new:
        o['lamps_commit'] = sha
    lights = [o for o in new if o.type == 'LIGHT']
    print('LAMPS placed', len(p.get('hemispheres', [])), 'Hemisphere,', len(p.get('cores', [])), 'Core;',
          len(lights), 'lamps,', round(sum(o.data.energy * L.lum(tuple(o.data.color)) for o in lights) / L.WLM), 'lm at the emitters')
    return [o for o in new if o.type != 'LIGHT']
