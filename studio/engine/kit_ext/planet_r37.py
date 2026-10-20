"""Planet EARF, round 37: the bar as a showroom (spinoffs/barkhorn/planet/r37/README.md). Round 36's room
(planet_r36.py) on round 37's plan (r37_plan.py): the room neutral and warm so any configuration works, the bar pair
in two timber-lined, felt-lined niches in the back bar either side of the decks, EARF's record players at the decks,
the sink in Smoke glowing amber.

    {"kind": "kit", "shape": "ext", "module": "planet_r37", "fn": "room", ...round 36's keys...}

Round 36's builders read their plan module as `R`; this swaps it for round 37's (which imports round 36's and changes
only what the brief changes), runs round 36's room, then adds the niches.
"""
import os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
sys.path.insert(0, os.path.join(ROOT, 'spinoffs', 'barkhorn', 'planet', 'r37'))
sys.path.insert(0, HERE)
import planet_r36 as K                                               # noqa: E402
import r37_plan as R                                                 # noqa: E402

LK = K.LK
DEFAULTS = dict(colourway='neutral', chair_leather=R.CHAIR_LEATHER, banq_col=R.BANQ_COL, sink_deep=R.SINK_DEEP,
                sink_glow_col=R.SINK_GLOW, decks='earf', disc_col='#FFD2A0')


def niches(bpy, kit, p, objs):
    """Each a box of dark oak (cheeks, head, floor board, back) lined in charcoal felt, open to the counter; a hidden
    warm strip in the head grazes down the cabinet; the felt stops 150 above the horn."""
    N = R.SPK_NICHE
    oak = K.Mesh('spk-niche-oak'); felt = K.Mesh('spk-niche-felt'); strip = K.Mesh('spk-niche-strip')
    for xc in R.SPK_NICHES:
        x0, x1, yf, yb, z0, z1 = R.niche_box(xc)
        t, f = N['wall'], N['felt']
        oak.box(x0, yf + 0.004, z0, x0 + t, yb, z1)                  # the cheeks
        oak.box(x1 - t, yf + 0.004, z0, x1, yb, z1)
        oak.box(x0 + t, yf + 0.004, z1 - t, x1 - t, yb, z1)          # the head
        oak.box(x0 + t, yf, z0, x1 - t, yb, z0 + 0.02)               # the floor board
        oak.box(x0 + t, yb - t, z0 + 0.02, x1 - t, yb, z1 - t)       # the back
        fw = 0.045                                                    # a proud face frame: two stiles and a head
        oak.box(x0 - 0.012, yf - 0.012, z0, x0 + fw, yf + 0.004, z1 + 0.012)
        oak.box(x1 - fw, yf - 0.012, z0, x1 + 0.012, yf + 0.004, z1 + 0.012)
        oak.box(x0 + fw, yf - 0.012, z1 - fw, x1 - fw, yf + 0.004, z1 + 0.012)
        # the felt: a hair inside the oak (coplanar faces render black)
        felt.box(x0 + t + 0.001, yb - t - f, z0 + 0.021, x1 - t - 0.001, yb - t - 0.001, z1 - t - 0.001)
        felt.box(x0 + t + 0.001, yf + 0.02, z0 + 0.021, x0 + t + f, yb - t - f, z1 - t - 0.001)
        felt.box(x1 - t - f, yf + 0.02, z0 + 0.021, x1 - t - 0.001, yb - t - f, z1 - t - 0.001)
        felt.box(x0 + t + f, yf + 0.02, z1 - t - f, x1 - t - f, yb - t - f, z1 - t - 0.001)
        strip.box(x0 + t + f + 0.03, yf + 0.04, z1 - t - f - 0.012, x1 - t - f - 0.03, yf + 0.06, z1 - t - f - 0.004)
    objs.append(oak.object(bpy, K.dark_oak(bpy, vertical=True, name='oak-spk-niche'), bevel=0.003))
    objs.append(felt.object(bpy, kit.material(bpy, 'felt', p.get('niche_felt', '#1C1B1A'))))
    lamp = strip.object(bpy, K.emitter(bpy, 'spk-niche-strip', '#FFC890', p.get('spk_niche_strip', 2.0)))
    lamp.visible_camera = False; lamp.visible_glossy = False; objs.append(lamp)


def room(bpy, name, p, kit):
    K.R = R                                                           # round 36's builders on round 37's plan
    p = {**DEFAULTS, **p}
    objs = K.room(bpy, name, p, kit)
    niches(bpy, kit, p, objs)
    return objs
