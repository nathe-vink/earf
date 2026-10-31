"""The laminated horn's 22 layers as flat cut files (2026-10-31), for the request to a shop that bonds and 5-axis
machines (rfq/tropos/e-laminated-horn/). Each layer is a flat part cut from 1/2 in sheet before bonding:

- OUTER: its outline, the air path's section at the layer's front face pushed out by the wall (the stepped horn's
  terrace; for the smooth horn the same outline, the taper machined after bonding);
- INNER: a rough bore, the air path's section at the layer's back face (its narrowest) less a 3 mm allowance all
  round, so the 5-axis pass that cuts the air path through the bonded stack finds stock everywhere;
- the layer's number and thickness in the drawing.

Layer 01 is at the mouth, layer 22 at the throat; the boss (ø pod) is the 23rd part, cut from the same sheet.

Also two surfaces as STEP, the shapes the 5-axis passes cut once the stack is bonded (the whole horn's STEP is 62 MB;
these are what a machinist needs): `air-path.step`, the air path as a solid (the horn's inside, the same surface as the
formed horn's plug, from the throat at z = 0 out through the mouth's rolled lip), and `outside-smooth.step`, the smooth
option's outside as a solid (the air path's sections pushed out by the wall), in the horn's own frame (z along the
axis, from the throat; mm).

    .venv-fab/bin/python spinoffs/barkhorn/rfq/tropos/layers_dxf.py      ->  e-laminated-horn/dxf/layer-NN.dxf, layers.csv,
                                                                            e-laminated-horn/step/*.step
"""
import csv, math, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
BH = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, BH)
import ezdxf                                                          # noqa: E402
import horn_options                                                   # noqa: E402
import product                                                        # noqa: E402

ALLOW = 3.0
OUT = os.path.join(HERE, 'e-laminated-horn', 'dxf')


def ring(w, h, n):
    return [product._se_point(w, h, n, math.pi / 4 + 2 * math.pi * k / 144) for k in range(144)]


def main():
    os.makedirs(OUT, exist_ok=True)
    c = horn_options.P['horn']['cast']; F = c['formed']; L = F['laminated']
    d = c['d']; wl = L['wall']
    hw, hh, _ = product.flare_section(c, d)
    nl = max(1, round(d / L['layer'])); t = d / nl
    rows = []
    for i in range(nl):
        zz = d - i * t; za = d - (i + 1) * t
        w, h, n = product.flare_section(c, zz)
        if i == 0:
            w, h = hw, hh
        wb, hb, nb = product.flare_section(c, za)
        doc = ezdxf.new('R2010', setup=True); doc.units = ezdxf.units.MM
        for name, col in (('OUTER', 1), ('INNER', 3), ('TEXT', 7)):
            doc.layers.add(name, color=col)
        msp = doc.modelspace()
        msp.add_lwpolyline(ring(w + wl, h + wl, max(n, 2.0)), close=True, dxfattribs={'layer': 'OUTER'})
        msp.add_lwpolyline(ring(max(wb - ALLOW, 5.0), max(hb - ALLOW, 5.0), max(nb, 2.0)), close=True, dxfattribs={'layer': 'INNER'})
        msp.add_text(f'TROPOS HORN LAYER {i + 1:02d} OF {nl}  t = {t:.2f} LESS THE BOND LINE  (1/2 IN SHEET)',
                     dxfattribs={'layer': 'TEXT', 'height': 6.0}).set_placement((-(w + wl), h + wl + 12))
        f = os.path.join(OUT, f'layer-{i + 1:02d}.dxf'); doc.saveas(f)
        rows.append(dict(layer=f'{i + 1:02d}', z_front_mm=f'{zz:.1f}', z_back_mm=f'{za:.1f}', outer_mm=f'{2 * (w + wl):.1f} x {2 * (h + wl):.1f}',
                         rough_bore_mm=f'{2 * max(wb - ALLOW, 5):.1f} x {2 * max(hb - ALLOW, 5):.1f}', thickness_mm=f'{t:.2f} less the bond line'))
    with open(os.path.join(os.path.dirname(OUT), 'layers.csv'), 'w', newline='') as fh:
        wr = csv.DictWriter(fh, fieldnames=list(rows[0])); wr.writeheader(); [wr.writerow(r) for r in rows]
    from build123d import export_step
    sd = os.path.join(os.path.dirname(OUT), 'step'); os.makedirs(sd, exist_ok=True)
    air = product._loft([product._se_pts(c['r0'], c['r0'], 2.0, -c['boss']['t'] - 2.0)] + product.air_sections(c, 0.0, d))
    export_step(air, os.path.join(sd, 'air-path.step'))
    zs = [d - i * t for i in range(nl + 1)]
    secs = [product._se_pts(*(lambda w, h, n: (w + wl, h + wl, max(n, 2.0)))(*product.flare_section(c, z)), z) for z in reversed(zs)]
    export_step(product._loft(secs), os.path.join(sd, 'outside-smooth.step'))
    print(f'{nl} layers, pitch {t:.2f}: {OUT}; air path {air.volume / 1000:.0f} cm3')


if __name__ == '__main__':
    main()
