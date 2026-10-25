"""Round 35: the thermal estimate for Hemisphere (and the dropped South, kept for the record; round 38), a small resistance network in steady state, so the
review's B2 can be checked by number. Every input is written here with where it came from; all are estimates until
the thermocouple test (README, round 35, "the test plan").

    python3 spinoffs/barkhorn/companions/hemisphere_thermal.py

The nodes: the LED's junction and case, the hub (the core and its fins, one node: aluminium, short paths), the collar
(with the clamp ring and the crown's acrylic next to it), the room. The hub loses heat to the room through its fins
(convection and radiation) and leaks some to the collar through the PEEK ring, its pins and the air gap; the collar
loses it to the room directly and through the acrylic it holds.
"""
import math

SIGMA = 5.67e-8
K_AIR, K_PEEK, K_SIL, K_PMMA = 0.026, 0.25, 0.2, 0.19
EPS_ANOD = 0.85                   # black anodised aluminium, a typical emissivity
LER = 310.0                       # lm per optical watt for a 2700 K, CRI 90 white LED (a typical figure)


def elenbaas_h(s, L, dT, Ta=300.0):
    """Natural convection between vertical plates s apart and L tall (Elenbaas), W/m2 K."""
    nu, alpha, g = 1.6e-5, 2.25e-5, 9.81
    ra = g / Ta * dT * s ** 4 / (nu * alpha * L)
    nu_s = ra / 24 * (1 - math.exp(-35 / ra)) ** 0.75
    return nu_s * K_AIR / s


def h_rad(T1, T2):
    return EPS_ANOD * SIGMA * (T1 ** 2 + T2 ** 2) * (T1 + T2)


def sink_G(od, height, fins, t, core_d, dT, Ta=300.0):
    """A radial fin sink's conductance to the room, W/K: the fins' faces by Elenbaas at their mid radius, at a fin
    efficiency of 0.95 (aluminium, 25 to 30 long, 1.8 thick), and the envelope's radiation (fins see each other, so
    only the outer envelope radiates out)."""
    r_mid = (od / 2 + core_d / 2) / 2 / 1000
    s = 2 * math.pi * r_mid / fins - t / 1000
    L = height / 1000
    area = fins * 2 * (od - core_d) / 2 / 1000 * L
    conv = elenbaas_h(s, L, dT, Ta) * area * 0.95
    env = math.pi * od / 1000 * L + 2 * math.pi * (od / 2000) ** 2
    rad = h_rad(Ta + dT, Ta) * env
    return conv + rad, s


def solve(P_in, lm, eta_out, sink, Ta, R_jc=0.9, R_tim=0.3, R_core=0.2, coupling=None):
    """Heat into the hub: the electrical power less the light, plus the light the fitting absorbs. Returns the
    temperatures (C) of the junction, the hub, the collar (and the acrylic next to it)."""
    P_opt = lm / LER
    Q = P_in - P_opt + P_opt * (1 - eta_out)
    c = coupling or {}
    R_hc = c.get('R_hub_collar', 9.2)        # the PEEK ring and pins || the air gap || radiation, K/W
    R_ca = c.get('R_collar_room', 6.9)       # the collar and clamp to the room || through the acrylic crown, K/W
    T = Ta + 20.0
    for _ in range(50):                       # the sink's conductance depends on its temperature: iterate
        G, s = sink_G(*sink, dT=max(T - Ta, 1.0), Ta=Ta + 273.15)
        R_s = 1 / G
        # hub node: Q = (Th - Ta)/R_s + (Th - Ta)/(R_hc + R_ca)
        Th = Ta + Q / (1 / R_s + 1 / (R_hc + R_ca))
        T = Th
    Tcol = Ta + (Th - Ta) * R_ca / (R_hc + R_ca)
    Tc = Th + Q * (R_tim + R_core)
    Tj = Tc + (P_in - P_opt) * R_jc
    return dict(Q=Q, Tj=Tj, Tc=Tc, Th=Th, Tcol=Tcol, R_sink=R_s, spacing=s)


# Hemisphere: the Vero SE 10 (DS120: 350 mA, 26.0 V, 9.1 W, about 1,130 lm at Tc 25 C, 1,020 at 85 C; the half
# level about 175 mA, 24.5 V, 4.3 W, 575 lm, scaled) behind the reflector (85 % out); fins 80 across, 36 tall, 16 x 1.8
NORTH = {'1,100 lm (350 mA)': (9.1, 1100.0), '575 lm (175 mA)': (4.3, 575.0)}
NORTH_SINK = (80.0, 36.0, 16, 1.8, 30.0)
# Hemisphere South (dropped 2026-10-25, kept for the record): twice the pendant's light, from a ring board of mid-power LEDs (about 150 lm/W at 2700 K CRI 90 at a
# moderate current: an estimate for LM301H-class parts). Round 36 (nothing below the bowl): the hub sits in the collar,
# its heat goes up an 8 copper heat pipe in the rod (about 0.4 K/W at 220 long, gravity-assisted) to fins 90 across, 40
# tall, 18 x 1.8, on the rod above the lid; the hub, the pipe and two joints about 0.85 K/W between the LED and the fins.
# The fins' warm air rises to the ceiling, away from the acrylic: no plume over the crown now. The owner's level is
# North's 575 lm, so South's 1,150; 2,200 stays in the table for the record
SOUTH = {'1,150 lm (twice the pendant at 575)': (7.7, 1150.0), '2,200 lm (twice the pendant at 1,100)': (14.7, 2200.0)}
SOUTH_SINK = (90.0, 40.0, 18, 1.8, 30.0)
NORTH = {'575 lm (175 mA; the owner, round 36)': NORTH.pop('575 lm (175 mA)'), **NORTH}


def table():
    print('| | room | heat in the hub, W | sink, K/W | hub (COB case about +2) | LED junction | collar, the acrylic next to it |')
    print('|---|---|---|---|---|---|---|')
    for title, items, sink, eta in (('North', NORTH, NORTH_SINK, 0.85), ('South', SOUTH, SOUTH_SINK, 0.97)):
        for k, (P, lm) in items.items():
            for Ta in (25.0, 35.0):
                r = solve(P, lm, eta, sink, Ta, R_core=0.2 if title == 'North' else 0.85)
                if title == 'South':          # the hub sits above the fins' temperature by its heat over the pipe
                    r['Th'] += r['Q'] * 0.6
                    # round 37: the collar is shut in between the skin and the opal, so it loses heat only through
                    # about 16 mm of acrylic and the bowl's air: about 15 K/W to the room (6.9 open)
                    r['Tcol'] = Ta + (r['Th'] - Ta) * 15.0 / (9.2 + 15.0)
                name = 'Hemisphere' if title == 'North' else 'South (dropped)'
                print(f"| {name}, {k} | {Ta:.0f} C | {r['Q']:.1f} | {r['R_sink']:.1f} | {r['Th']:.0f} C | "
                      f"{r['Tj']:.0f} C | {r['Tcol']:.0f} C |")
    # the black bore, for the record (the hub as it was, at 9.1 W, with fins)
    r = solve(9.1, 1100, 0.52, NORTH_SINK, 25.0)
    print(f"\n(Hemisphere with the old black bore, 1,100 lm, 25 C room: {r['Q']:.1f} W in the hub, hub {r['Th']:.0f} C)")
    print('South (dropped; round 36): its fins are above the lid, so their warm air rises to the ceiling; no plume reaches the '
          'acrylic.')


if __name__ == '__main__':
    table()
