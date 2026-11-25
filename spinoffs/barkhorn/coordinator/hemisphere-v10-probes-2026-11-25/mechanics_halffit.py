"""The half-fitted shade (V10, no lock): what holds it on the flat band, what a ramp in the band's ceiling would drive,
and the detent's drag the lane's ramp study leaves out. Shade weights from my solids (out/weights.txt): B 974, today 980,
A without the lock 998 g. Pins bear at r 43; the ball (Kipp K0310.05: F = 6 + 5 x/0.9 N, x its push-in) rides the bore at
x 0.70 throughout the band (py/detent.py), so F 9.9 N, at r 41; the collar's reaction on the PEEK land opposite."""
g = 9.81
r_p, r_b, r_rim = 0.043, 0.041, 0.100
Fb = 6 + 5 * 0.70 / 0.9
print(f'ball force on the bore in the band: {Fb:.1f} N')
for name, m in (('B', 0.974), ('today', 0.980), ('A without the lock', 0.998)):
    W = m * g
    print(f'\n{name}: W {W:.2f} N')
    for lab, mp, mb, ml in (('greased', 0.15, 0.10, 0.15), ('dry, low', 0.25, 0.15, 0.25), ('dry, mid', 0.30, 0.15, 0.30), ('dry, high', 0.45, 0.25, 0.40)):
        Tp = mp * W * r_p
        Td = Fb * r_b * (mb + ml)
        T = Tp + Td
        print(f'  {lab:10s} mu pins {mp}, ball {mb}, land {ml}: pins {Tp:.3f} + detent {Td:.3f} = {T:.3f} N m -> {T / r_rim:.1f} N at the rim')
        for s in (0.4, 0.6, 1.0):
            drive = W * r_p * (s - mp) / (1 + mp * s)
            print(f'      ramp slope {s}: drive {drive:+.3f} N m, less the detent {drive - Td:+.3f} N m -> '
                  + ('self-seats' if drive - Td > 0 else 'DOES NOT self-seat'))
# the gate (my proposal): a step 0.8 down from each band's ceiling just past its entry
print('\nGate 0.8: the Ø4 pins at the stop (band floor) top at 86.5, the gate underside 86.7: 0.2 clear; the key pin (Ø6) top 87.5 '
      'under a key gate 1.0 down (87.75): 0.25 clear. A shade resting on the ceiling (pins top 87.5) must be lifted >= 0.8 '
      'to pass back over the gate: a lift of the 9.8 N shade, not a sideways wipe.')
