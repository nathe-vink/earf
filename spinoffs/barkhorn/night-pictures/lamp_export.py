"""The night pictures (the coordinator, 2026-11-03 23:04): EARF's own lamps as the room's practicals.

Builds one lamp exactly as the lamps lane's picture rig builds it (r32-lamps-final, lamp_pictures.build: the same CAD
meshes, acrylic, opal liner, LED and wattage) and saves the scene to a .blend in place of rendering it. night_room.py
then appends only the lamp's own objects (its parts and its own lights) into the speaker's room; the lamps lane's room,
fill, kicker, curtain, bowl and camera are left behind.

    python3.11 spinoffs/barkhorn/night-pictures/lamp_export.py LAMPS_ROOT FRAME OUT.blend
        LAMPS_ROOT: a checkout of r32-lamps-final (its companions/out-*/stl built with fabkit)
        FRAME: lamp_pictures's frame name, e.g. hemi-fog-night or core-fog-night (today's lamps: no -nested suffix,
        the opal liner at its default, the cool-white grade)

Runs on python3.11 (bpy 5.0).
"""
import os
import sys


def main():
    root, frame, out = sys.argv[1], sys.argv[2], os.path.abspath(sys.argv[3])
    comp = os.path.join(root, 'spinoffs', 'barkhorn', 'companions')
    sys.path.insert(0, comp)
    import bpy
    real_ops = bpy.ops

    def save(*a, **k):
        # in place of the render: the scene as built, every object listed for night_room.py
        for o in sorted(bpy.data.objects, key=lambda o: o.name):
            print('OBJ', o.name, o.type, tuple(round(v, 4) for v in o.location), flush=True)
        bpy.ops.wm.save_as_mainfile(filepath=out)
        return {'FINISHED'}

    class _Render:
        def __getattr__(self, n):
            return save if n == 'render' else getattr(real_ops.render, n)

    class _Ops:
        # bpy.ops hands out a fresh submodule on each access, so the render call is swapped at this level
        def __getattr__(self, n):
            return _Render() if n == 'render' else getattr(real_ops, n)

    bpy.ops = _Ops()
    import lamp_pictures as LP
    LP.build(frame, 64, 0.25)


if __name__ == '__main__':
    main()
