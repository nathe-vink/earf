"""V11-9 (the V10 check; UL 1598 6.15.1.3, Table 20.1.1 item 1.33): Hemisphere's wiring diagram with its assembly
instructions, for a lamp shipped with its cord unconnected. Writes wiring-diagram.pdf and .png into each Hemisphere
package (out-dome-pendant, -topA, -topA-nolock, -topB). Run with the CAD venv:
    .venv-fab/bin/python spinoffs/barkhorn/companions/hemi_wiring.py"""
import os
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
HERE = os.path.dirname(os.path.abspath(__file__))
fig, ax = plt.subplots(figsize=(16.5, 11.7))
ax.set_xlim(0, 330); ax.set_ylim(0, 234); ax.axis('off')
def boxp(x, y, w, h, t, fc='#ffffff', ec='#000000', fs=11):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle='round,pad=0.6', fc=fc, ec=ec, lw=1.4))
    ax.text(x + w / 2, y + h / 2, t, ha='center', va='center', fontsize=fs)
def wire(pts, c, lw=2.6, ls='-'):
    xs, ys = zip(*pts); ax.plot(xs, ys, color=c, lw=lw, ls=ls, solid_capstyle='round')
ax.text(5, 226, 'Hemisphere: wiring diagram and assembly (120 V AC, 60 Hz; Class 2 output)', fontsize=17, weight='bold')
ax.text(5, 218, 'The lamp is shipped with its cord unconnected: the installer makes the connections below (UL 1598 6.15.1.3). '
        'Turn the power off at the breaker first.', fontsize=11)
# the outlet box
boxp(10, 120, 90, 80, '', fc='#f3f3f3')
ax.text(55, 194, 'OUTLET BOX\n(4 in, for luminaire support)', ha='center', va='top', fontsize=10, weight='bold')
ax.text(14, 182, 'supply', fontsize=10)
wire([(14, 175), (40, 175)], '#111111'); ax.text(14, 177.5, 'L (black)', fontsize=9)
wire([(14, 160), (40, 160)], '#bbbbbb'); ax.text(14, 162.5, 'N (white)', fontsize=9)
wire([(14, 140), (70, 140), (70, 128)], '#1a8a1a'); ax.text(14, 142.5, 'grounding conductor (green or bare)', fontsize=9)
boxp(40, 171, 14, 8, 'C1', fc='#ffe9a8', fs=9); boxp(40, 156, 14, 8, 'C2', fc='#ffe9a8', fs=9)
ax.text(14, 131, 'C1, C2: listed splicing connectors (UL 486C)\nfor 18 AWG to the supply\'s gauge', fontsize=8, va='top')
# the plate
ax.add_patch(plt.Rectangle((10, 112), 300, 4, fc='#999999')); ax.text(312, 113, 'mounting\nplate', fontsize=9, va='center')
boxp(64, 118, 12, 6, 'green\nscrew', fc='#c9f2c9', fs=7.5)
ax.text(104, 121, 'GND: under the cupped washer of the green screw (10-32) on the plate\'s top face', fontsize=8.5)
# the driver
boxp(30, 40, 70, 50, 'DRIVER\nERP ESS010W-0180-42-XL\n(Class 2 output)\nin its steel tray', fc='#e8eef7')
wire([(54, 175), (90, 175), (90, 105), (45, 105), (45, 90)], '#111111')
wire([(54, 160), (84, 160), (84, 108), (55, 108), (55, 90)], '#bbbbbb')
ax.text(92, 100, 'input leads (black L, white N; 300 long,\n150 or more in the box), up through the\nplate\'s rolled opening', fontsize=8.5)
ax.text(33, 30, 'its dimming leads are cut at the factory', fontsize=8.5, style='italic')
# the splices
boxp(150, 60, 22, 14, 'A  (-)', fc='#ffd0b0'); boxp(150, 30, 22, 14, 'B  (+)', fc='#ffd0b0')
ax.text(150, 80, 'two WAGO 221-412 lever splices\nin the cord clamp (Class 2)', fontsize=9)
wire([(100, 70), (150, 70)], '#111111'); ax.text(104, 72.5, 'LED lead - (black)', fontsize=8.5)
wire([(100, 50), (130, 50), (130, 36), (150, 36)], '#cc0000'); ax.text(104, 52.5, 'LED lead + (red)', fontsize=8.5)
# the cord
wire([(172, 67), (215, 67), (215, 20)], '#444444'); wire([(172, 37), (205, 37), (205, 20)], '#444444', ls=(0, (6, 2)))
ax.text(176, 69.5, 'plain conductor', fontsize=8.5); ax.text(176, 39.5, 'identified conductor (ribbed or printed)', fontsize=8.5)
ax.add_patch(plt.Rectangle((200, 10), 20, 10, fc='#222222')); ax.text(223, 13, 'the cord (SVT 18/2), down to the lamp', fontsize=9)
# steps
steps = ['1. Thread the two cables and the cord through the canopy (cables through its floor holes, the cord through its grommet).',
         '2. Hang the plate on one box screw through its slot. Splice the driver\'s black lead to the supply\'s L and its white lead',
         '    to N with listed connectors (C1, C2), 150 mm or more of each lead in the box. Land the grounding conductor under the',
         '    green screw\'s cupped washer and tighten it. Fold the wires into the box and screw the plate to the box.',
         '3. Hang and level the lamp on its cables (NOTES); keep the canopy tied 10 to 15 cm below the plate.',
         '4. Mark and clamp the cord in its two straps (NOTES); cut it 40 above the upper strap; strip the jacket 4 above it and',
         '    each conductor 11. Open each splice\'s lever, insert, close: the IDENTIFIED conductor into B with the RED lead (+), the',
         '    plain conductor into A with the BLACK lead (-). Tug each wire.',
         '5. Untie the canopy, slide it up and tighten its two set screws in turn. Restore the power.']
for k, t in enumerate(steps):
    ax.text(230, 200 - 7.2 * k, t, fontsize=8.6, va='top', family='DejaVu Sans', wrap=False) if False else None
y = 205
for t in steps:
    ax.text(118, y, t, fontsize=9.2, va='top'); y -= 8.4
for d in ('out-dome-pendant', 'out-dome-pendant-topA', 'out-dome-pendant-topA-nolock', 'out-dome-pendant-topB'):
    o = os.path.join(HERE, d)
    if os.path.isdir(o):
        fig.savefig(os.path.join(o, 'wiring-diagram.pdf')); fig.savefig(os.path.join(o, 'wiring-diagram.png'), dpi=90)
        print(o)
