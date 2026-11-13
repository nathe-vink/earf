"""15PR400-8 in Tropos's vented box (135.6 L net, fb 38 Hz, QL 7), the preset's LR4 high-pass: cone excursion and level
per volt, then against the FA122 (one channel, 75 W into 8 ohm) and the FA123 bridged (250 W into 8 ohm)."""
import numpy as np
rho, c = 1.204, 343.0
Re, Le, Bl, Mms, Fs, Qms, Vas, Sd = 5.1, 0.72e-3, 16.7, 0.0852, 35.0, 6.0, 0.2489, 0.0857
Xmax, Xdam, Pe = 5.75e-3, 15.5e-3, 400.0
Vb, fb, QL = 0.1356, 38.0, 7.0
Cms = Vas / (rho * c**2 * Sd**2); Rms = 2*np.pi*Fs*Mms/Qms
Cab = Vb / (rho*c**2); Map = 1/((2*np.pi*fb)**2*Cab); Ral = QL/(2*np.pi*fb*Cab)

def resp(f, hp=28.0):
    s = 2j*np.pi*f
    Za = 1/(s*Cab + 1/Ral + 1/(s*Map))               # box acoustic impedance
    Ze = Re + s*Le
    Zm = s*Mms + Rms + 1/(s*Cms) + Bl**2/Ze + Sd**2*Za
    u = (Bl/Ze)/Zm                                   # cone velocity per volt
    i = (1 - Bl*u)/Ze                                # current per volt
    p_box = -Za*Sd*u
    Up = p_box/(s*Map)                               # the port's outward volume velocity: the box pressure drives it out
    U = Sd*u + Up
    pf = rho*s*U/(2*np.pi*1.0)                       # half space, 1 m
    # LR4 high-pass: a 2nd-order Butterworth squared
    w = f/hp; h2 = (1j*w)**2/((1j*w)**2 + np.sqrt(2)*1j*w + 1); H = h2*h2 if hp else 1.0
    return np.abs(u/s*H), np.abs(pf*H), np.abs(1/i)  # x per Vrms (rms), p per Vrms, |Z|

f = np.array([20, 25, 28, 31.5, 35, 40, 45, 50, 56, 63, 71, 80, 100, 125])
x, p, Z = resp(f)
amps = {'FA122 (one ch, 75 W / 8)': np.sqrt(75*8), 'FA123 bridged (250 W / 8)': np.sqrt(250*8)}
print('Zmin 20-200 Hz', round(min(resp(np.linspace(20, 200, 400))[2]), 2), 'ohm')
for name, V in amps.items():
    print(f'\n{name}: {V:.1f} Vrms')
    print(' f    x_peak mm   SPL dB(1m, half)   V for Xmax  SPL at the limit (Xmax or amp)')
    for k, fk in enumerate(f):
        xp = x[k]*V*np.sqrt(2)*1e3
        Vx = Xmax/(x[k]*np.sqrt(2))
        Vl = min(V, Vx)
        spl = 20*np.log10(p[k]*V/20e-6); spll = 20*np.log10(p[k]*Vl/20e-6)
        print(f'{fk:5.1f} {xp:7.2f} {"!" if xp > Xdam*1e3 else ("*" if xp > Xmax*1e3 else " ")}   {spl:6.1f}           {Vx:6.1f}     {spll:6.1f} ({"Xmax" if Vx < V else "amp"})')
# a high-pass that keeps the full bridged swing inside Xmax from 20 Hz, and one for Xdamage
for hp in (28, 32, 35, 38, 40):
    xs, ps, _ = resp(np.linspace(15, 200, 600), hp)
    V = np.sqrt(250*8)
    print(f'HP LR4 {hp} Hz: peak x at 44.7 V {xs.max()*V*np.sqrt(2)*1e3:.1f} mm; Vmax for Xmax {Xmax/(xs.max()*np.sqrt(2)):.1f} V')
