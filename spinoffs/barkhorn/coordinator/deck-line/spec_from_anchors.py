#!/usr/bin/env python3
"""Make a line_build spec from the four-pieces lane's anchors.json (label zones, no leaders)."""
import json, sys
anchors, ground, out = sys.argv[1], sys.argv[2], sys.argv[3]
version = sys.argv[4] if len(sys.argv) > 4 else 'day'
a = json.load(open(anchors))
COPY = {
  'tropos': ('Tropos', 'Speaker', 'A powered horn loudspeaker.'),
  'hemisphere': ('Hemisphere', 'Pendant', 'A shade that swaps in a quarter turn.'),
  'core': ('Core', 'Table lamp', 'Cordless, about five hours a charge.'),
  'mantle': ('Mantle', 'Record player', 'Floats on its own light.'),
}
callouts = []
for key in ['hemisphere', 'core', 'mantle', 'tropos']:
    p = a['products'][key]
    x0, y0, x1, y1 = p['label_zone']
    side = p.get('label_side', 'above')
    align = 'right' if side == 'left' else ('left' if side == 'right' else 'center')
    name, kind, line = COPY[key]
    # text block ~ 112 px tall; sit it at the bottom of an "above" zone, centred vertically otherwise
    h = 112
    ty = y1 - h if side == 'above' else y0 + (y1 - y0 - h) // 2
    callouts.append({'id': key, 'name': name, 'kind': kind, 'line': line,
                     'label': {'x': x0, 'y': ty, 'w': x1 - x0, 'h': h, 'lines': 1, 'align': align}})
hx0, hy0, hx1, hy1 = a['header']['zone']
spec = {
  'ground': ground, 'src': '/_blob/PENDING',
  'alt': ('A living room ' + ('at dusk with the lamps lit' if version == 'dusk' else 'in late-afternoon sun') +
          ': a pair of Tropos speakers in Poison, a transparent green acrylic, with their covers off, either side of a low oak '
          'credenza with a Mantle record player on it; a Core lamp on a side table at the left; a Hemisphere pendant over a '
          'cognac leather chair at the right; a plain plaster wall behind'),
  'notes': ('Each piece takes its name from the Earth. Tropos is Greek for a turn; the troposphere, the layer of air where '
            'sound travels, is named for it. Core, Mantle and Hemisphere are the planet’s own parts. Here all four share one '
            'room, in Poison, one of the eight colors. It is a render, not a photograph: Tropos with its cover off, Core cordless.'),
  'header': {'eyebrow': 'The line', 'title': 'Four pieces, named for the Earth.', 'x': hx0, 'y': hy0 + 6, 'w': hx1 - hx0, 'h': hy1 - hy0, 'px': 60},
  'callouts': callouts,
  'foot': {'text': 'A render. Shown in Poison, one of eight colors.', 'x': 1280, 'y': 1036, 'w': 600, 'align': 'right'},
}
json.dump(spec, open(out, 'w'), indent=1, ensure_ascii=False)
