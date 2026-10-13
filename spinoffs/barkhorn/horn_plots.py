"""Charts and numbers from horn_sim.py's runs (acoustics/<name>-<band>.json), for the README of acoustics/.

    .venv-fab/bin/python spinoffs/barkhorn/horn_plots.py              # -> acoustics/*.png, acoustics/summary.json

- coverage.png: the horn alone (lo, mid, hi merged): how loud each direction is against the axis, by frequency,
  horizontally and vertically (darker is louder; the solid line -6 dB, the dashed -3 dB), its -6 dB coverage and its
  directivity index beside the woofer's on the cabinet;
- throat.png: the load the driver sees: the throat's resistance and reactance against a plane wave's (1 = rho c);
- crossover.png: the whole speaker (cab: the horn and the woofer on the cabinet) through Linkwitz-Riley crossovers
  (fourth order, each driver equalised flat on the listening axis and aligned there, as the amplifier's DSP can):
  the level 30, 45 and 60 degrees off axis horizontally against the axis, and the vertical maps, at 800 Hz (today's)
  and the proposal.
"""
import glob, json, os
from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap, BoundaryNorm

HERE = Path(__file__).resolve().parent
A = HERE / 'acoustics'
# the reference palette (dataviz): ink, a blue ramp for magnitude, categorical slots in order
INK, INK2, MUTED, GRID, SURF = '#0b0b0b', '#52514e', '#8a8984', '#e4e2dd', '#fcfcfb'
RAMP = ['#cde2fb', '#b7d3f6', '#9ec5f4', '#86b6ef', '#6da7ec', '#5598e7', '#3987e5', '#2a78d6', '#256abf', '#1c5cab',
        '#184f95', '#104281', '#0d366b']
S1, S2, S3, S4 = '#2a78d6', '#eb6834', '#1baf7a', '#eda100'
XO = 800.0
plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 10, 'axes.edgecolor': MUTED, 'axes.labelcolor': INK2,
                     'xtick.color': INK2, 'ytick.color': INK2, 'axes.titlesize': 11, 'axes.titlecolor': INK,
                     'axes.titleweight': 'bold', 'axes.titlelocation': 'left', 'figure.facecolor': SURF, 'axes.facecolor': SURF,
                     'savefig.facecolor': SURF})


def cplx(L):
    return np.array([complex(a, b) for a, b in L])


def load(name, bands):
    by_f, angles = {}, None
    for b in bands:
        p = A / f'{name}-{b}.json'
        if not p.exists():
            continue
        d = json.loads(p.read_text())
        angles = np.array(d['angles'])
        for r in d['results']:
            by_f[r['f']] = r
    return angles, [by_f[f] for f in sorted(by_f)]


def arc(r, rad, plane):
    return cplx(r[str(rad)][plane])


def half_angle(levels, ang, sign):
    """The -6 dB half angle from the axis toward +sign (levels in dB against the axis, angles from -180 by 5)."""
    i0 = int(np.where(ang == 0)[0][0]); n = len(ang)
    for j in range(1, n // 2 + 1):
        a, b = levels[(i0 + sign * (j - 1)) % n], levels[(i0 + sign * j) % n]
        if b <= -6:
            return 5 * (j - 1) + 5 * (-6 - a) / (b - a)
    return None


def coverage(res, ang, rad=1):
    """Per frequency: full -6 dB angles (h, v: the mean of the two sides, doubled) and the directivity index."""
    i0 = int(np.where(ang == 0)[0][0])
    out = []
    for r in res:
        h, v = arc(r, rad, 'h'), arc(r, rad, 'v')
        on = abs(h[i0])
        hl, vl = 20 * np.log10(np.abs(h) / on), 20 * np.log10(np.abs(v) / on)
        hw = [half_angle(hl, ang, s) for s in (1, -1)]
        vw = [half_angle(vl, ang, s) for s in (1, -1)]
        di = 10 * np.log10(on ** 2 / r[str(rad)]['power'])
        out.append(dict(f=r['f'], h=None if None in hw else sum(hw), v=None if None in vw else sum(vw),
                        up=vw[0], down=vw[1], di=float(di), hl=hl, vl=vl))
    return out


def lr4(f, fc):
    s = 1j * f / fc
    bw_lp = 1 / (1 + np.sqrt(2) * s + s * s)
    bw_hp = s * s * bw_lp
    return bw_lp ** 2, bw_hp ** 2


def system(res, ang, fc):
    """The two drivers (1 the horn, 2 the woofer) summed through LR4 at fc, each equalised flat and aligned on the
    axis: the summed arcs (complex, against the axis), per frequency."""
    i0 = int(np.where(ang == 0)[0][0])
    out = []
    for r in res:
        lp, hp = lr4(r['f'], fc)
        H = {pl: arc(r, 1, pl) for pl in ('h', 'v')}
        W = {pl: arc(r, 2, pl) for pl in ('h', 'v')}
        S = {pl: hp * H[pl] / H['h'][i0] + lp * W[pl] / W['h'][i0] for pl in ('h', 'v')}
        # power, the two drivers' added as if incoherent (their cross term over the sphere left out; they stand 0.62 m
        # apart, more than half a wavelength above about 280 Hz)
        pw = abs(hp) ** 2 * r['1']['power'] / abs(H['h'][i0]) ** 2 + abs(lp) ** 2 * r['2']['power'] / abs(W['h'][i0]) ** 2
        out.append(dict(f=r['f'], h=S['h'], v=S['v'], di=float(10 * np.log10(abs(S['h'][i0]) ** 2 / pw))))
    return out


def polar_map(ax, freqs, ang, levels_by_f, title, ylabel, lim=90, xo=XO, xo_label=True):
    sel = np.abs(ang) <= lim
    Z = np.array([l[sel] for l in levels_by_f]).T
    Z = np.clip(Z, -30, 3)
    bounds = [-30, -27, -24, -21, -18, -15, -12, -9, -6, -3, 0, 3]
    cmap = ListedColormap(RAMP[1:12])
    norm = BoundaryNorm(bounds, cmap.N)
    F, Aa = np.meshgrid(freqs, ang[sel])
    cs = ax.contourf(F, Aa, Z, levels=bounds, cmap=cmap, norm=norm, extend='neither')
    ax.contour(F, Aa, Z, levels=[-6], colors=INK, linewidths=1.6, linestyles='solid')
    ax.contour(F, Aa, Z, levels=[-3], colors=INK, linewidths=0.9, linestyles='dashed')
    ax.set_xscale('log'); ax.set_xlim(freqs[0], freqs[-1]); ax.set_ylim(-lim, lim)
    ax.set_yticks(np.arange(-lim, lim + 1, 30))
    ax.set_xticks([250, 500, 1000, 2000, 4000, 8000]); ax.set_xticklabels(['250', '500', '1k', '2k', '4k', '8k'])
    ax.minorticks_off()
    if xo:
        ax.axvline(xo, color=INK, lw=0.8, ls=':')
        if xo_label:
            ax.text(xo * 1.03, lim - 8, f'crossover {xo / 1000:g} kHz', color=INK, fontsize=9, va='top')
    ax.set_title(title); ax.set_ylabel(ylabel); ax.set_xlabel('frequency (Hz)')
    return cs


def end_label(ax, x, y, txt, color):
    """A direct label at a line's last point (text in ink, a dot of the series' colour carries the identity)."""
    pts = [(a, b) for a, b in zip(x, y) if b is not None and not np.isnan(b)]
    if not pts:
        return
    a, b = pts[-1]
    ax.annotate(txt, (a, b), xytext=(6, 0), textcoords='offset points', va='center', fontsize=9, color=INK2)


def style(ax):
    for s in ('top', 'right'):
        ax.spines[s].set_visible(False)
    ax.grid(True, color=GRID, lw=0.7); ax.set_axisbelow(True)


def main():
    ang, res = load('horn', ['lo', 'mid', 'hi'])
    angc, cab = load('horn', ['cab'])
    cov = coverage(res, ang)
    freqs = np.array([c['f'] for c in cov])
    summary = dict(horn=[{k: c[k] for k in ('f', 'h', 'v', 'up', 'down', 'di')} for c in cov])
    woof = coverage(cab, angc, rad=2) if cab else []
    horn_cab = coverage(cab, angc, rad=1) if cab else []
    summary['woofer_on_cabinet'] = [{k: c[k] for k in ('f', 'h', 'v', 'di')} for c in woof]
    summary['horn_on_cabinet'] = [{k: c[k] for k in ('f', 'h', 'v', 'up', 'down', 'di')} for c in horn_cab]

    # --- coverage.png ----------------------------------------------------------------------------------------------
    fig = plt.figure(figsize=(13, 9.4))
    gs = fig.add_gridspec(2, 2, height_ratios=[1.05, 1], hspace=0.42, wspace=0.22)
    ax1, ax2 = fig.add_subplot(gs[0, 0]), fig.add_subplot(gs[0, 1])
    cs = polar_map(ax1, freqs, ang, [c['hl'] for c in cov], 'Horizontal: each direction against the axis', 'degrees off axis (+ right)')
    polar_map(ax2, freqs, ang, [c['vl'] for c in cov], 'Vertical: each direction against the axis', 'degrees off axis (+ up)')
    cb = fig.colorbar(cs, ax=[ax1, ax2], fraction=0.025, pad=0.02, ticks=[-30, -24, -18, -12, -6, 0])
    cb.set_label('dB against the axis', color=INK2); cb.outline.set_edgecolor(MUTED)
    ax3 = fig.add_subplot(gs[1, 0])
    style(ax3)
    hh = [c['h'] for c in cov]; vv = [c['v'] for c in cov]
    ax3.plot(freqs, [np.nan if x is None else x for x in hh], color=S1, lw=2, marker='o', ms=4, label='horn, horizontal')
    ax3.plot(freqs, [np.nan if x is None else x for x in vv], color=S2, lw=2, marker='o', ms=4, label='horn, vertical')
    if woof:
        fw = [c['f'] for c in woof]
        ax3.plot(fw, [np.nan if c['h'] is None else c['h'] for c in woof], color=S3, lw=2, marker='o', ms=4,
                 label='15 in woofer on the cabinet, horizontal')
    end_label(ax3, freqs, [np.nan if x is None else x for x in hh], 'H', S1)
    end_label(ax3, freqs, [np.nan if x is None else x for x in vv], 'V', S2)
    ax3.axhline(95, color=S1, lw=0.8, ls=(0, (4, 3)), alpha=0.8); ax3.text(freqs[-1], 97, 'the walls: 95', color=INK2, ha='right', fontsize=9)
    ax3.axhline(63, color=S2, lw=0.8, ls=(0, (4, 3)), alpha=0.8); ax3.text(freqs[-1], 65, '63', color=INK2, ha='right', fontsize=9)
    ax3.axvline(XO, color=INK, lw=0.8, ls=':')
    ax3.set_xscale('log'); ax3.set_xlim(freqs[0], freqs[-1]); ax3.set_ylim(0, 200)
    ax3.set_xticks([250, 500, 1000, 2000, 4000, 8000]); ax3.set_xticklabels(['250', '500', '1k', '2k', '4k', '8k']); ax3.minorticks_off()
    ax3.set_title('Coverage: the full angle between the -6 dB points'); ax3.set_ylabel('degrees'); ax3.set_xlabel('frequency (Hz)')
    ax3.legend(frameon=False, fontsize=9, loc='upper right')
    ax4 = fig.add_subplot(gs[1, 1])
    style(ax4)
    ax4.plot(freqs, [c['di'] for c in cov], color=S1, lw=2, marker='o', ms=4, label='horn')
    if woof:
        ax4.plot([c['f'] for c in woof], [c['di'] for c in woof], color=S3, lw=2, marker='o', ms=4, label='15 in woofer on the cabinet')
    ax4.axvline(XO, color=INK, lw=0.8, ls=':')
    ax4.set_xscale('log'); ax4.set_xlim(freqs[0], freqs[-1]); ax4.set_ylim(0, 20)
    ax4.set_xticks([250, 500, 1000, 2000, 4000, 8000]); ax4.set_xticklabels(['250', '500', '1k', '2k', '4k', '8k']); ax4.minorticks_off()
    ax4.set_title('Directivity index: on axis against the average'); ax4.set_ylabel('dB'); ax4.set_xlabel('frequency (Hz)')
    ax4.legend(frameon=False, fontsize=9, loc='upper left')
    fig.suptitle('The cast horn, by boundary elements: the horn alone in free air (the woofer: on its cabinet)', x=0.06, ha='left',
                 fontsize=13, color=INK, fontweight='bold')
    fig.savefig(A / 'coverage.png', dpi=130, bbox_inches='tight'); plt.close(fig)

    # --- throat.png ------------------------------------------------------------------------------------------------
    fig, ax = plt.subplots(figsize=(9, 4.2))
    style(ax)
    z = np.array([1j * r['k'] * complex(*r['1']['p_face']) for r in res])
    ax.plot(freqs, z.real, color=S1, lw=2, marker='o', ms=4, label='resistance (what the driver can work against)')
    ax.plot(freqs, -z.imag, color=S2, lw=2, marker='o', ms=4, label='reactance (air that only moves to and fro)')
    ax.axhline(1, color=INK2, lw=0.8, ls='--'); ax.text(freqs[0] * 1.04, 1.04, 'a plane wave: 1', color=INK2, ha='left', fontsize=9)
    ax.axvline(XO, color=INK, lw=0.8, ls=':')
    ax.set_xscale('log'); ax.set_xlim(freqs[0], freqs[-1])
    ax.set_xticks([250, 500, 1000, 2000, 4000, 8000]); ax.set_xticklabels(['250', '500', '1k', '2k', '4k', '8k']); ax.minorticks_off()
    ax.set_title('The load at the throat, against a plane wave\'s (rho c)'); ax.set_xlabel('frequency (Hz)')
    ax.legend(frameon=False, fontsize=9, loc='upper right')
    fig.savefig(A / 'throat.png', dpi=130, bbox_inches='tight'); plt.close(fig)
    summary['throat'] = [dict(f=r['f'], r=float(zz.real), x=float(-zz.imag)) for r, zz in zip(res, z)]

    # --- crossover.png ---------------------------------------------------------------------------------------------
    if cab:
        fcs = [800.0, 1000.0, 1200.0]
        sysd = {fc: system(cab, angc, fc) for fc in fcs}
        fq = np.array([r['f'] for r in cab])
        i0 = int(np.where(angc == 0)[0][0])
        fig = plt.figure(figsize=(13, 9.4))
        gs = fig.add_gridspec(2, 3, height_ratios=[1, 1.05], hspace=0.45, wspace=0.25)
        cols = {800.0: S1, 1000.0: S2, 1200.0: S3}
        for k, a_ in enumerate((30, 45, 60)):
            ax = fig.add_subplot(gs[0, k]); style(ax)
            j = int(np.where(angc == a_)[0][0]); jm = int(np.where(angc == -a_)[0][0])
            for fc in fcs:
                lev = [10 * np.log10((abs(s['h'][j]) ** 2 + abs(s['h'][jm]) ** 2) / 2 / abs(s['h'][i0]) ** 2) for s in sysd[fc]]
                ax.plot(fq, lev, color=cols[fc], lw=2, marker='o', ms=3.5, label=f'crossed at {fc / 1000:g} kHz')
            ax.set_xscale('log'); ax.set_xlim(fq[0], fq[-1]); ax.set_ylim(-18, 3)
            ax.set_xticks([250, 500, 1000, 2000]); ax.set_xticklabels(['250', '500', '1k', '2k']); ax.minorticks_off()
            ax.set_title(f'{a_} degrees off axis, horizontally'); ax.set_xlabel('frequency (Hz)')
            if k == 0:
                ax.set_ylabel('dB against the axis')
                ax.legend(frameon=False, fontsize=9, loc='lower left')
        for k, fc in enumerate(fcs):
            ax = fig.add_subplot(gs[1, k])
            vl = [20 * np.log10(np.abs(s['v']) / abs(s['h'][i0])) for s in sysd[fc]]
            cs = polar_map(ax, fq, angc, vl, f'Vertical, crossed at {fc / 1000:g} kHz', 'degrees (+ up)' if k == 0 else '', xo=fc,
                           xo_label=False)
            ax.set_xticks([250, 500, 1000, 2000]); ax.set_xticklabels(['250', '500', '1k', '2k'])
        fig.suptitle('The whole speaker through the crossover (fourth-order Linkwitz-Riley, each driver equalised and aligned on the axis)',
                     x=0.06, ha='left', fontsize=13, color=INK, fontweight='bold')
        fig.savefig(A / 'crossover.png', dpi=130, bbox_inches='tight'); plt.close(fig)
        summary['system'] = {str(int(fc)): [dict(f=s['f'], di=s['di'],
                                                  h30=float(20 * np.log10(abs(s['h'][int(np.where(angc == 30)[0][0])]) / abs(s['h'][i0]))),
                                                  h45=float(20 * np.log10(abs(s['h'][int(np.where(angc == 45)[0][0])]) / abs(s['h'][i0]))),
                                                  h60=float(20 * np.log10(abs(s['h'][int(np.where(angc == 60)[0][0])]) / abs(s['h'][i0]))))
                                             for s in sysd[fc]] for fc in fcs}
    # --- bell.png: the proposal (a bell-flared lip) against the horn as built ---------------------------------------
    angb, bell = load('bell40', ['lo', 'mid'])
    if bell:
        covb = coverage(bell, angb)
        fb = np.array([c['f'] for c in covb])
        top = fb[-1]
        sel = freqs <= top
        fig, axs = plt.subplots(1, 3, figsize=(15, 4.6))
        for ax, key, ttl in ((axs[0], 'h', 'Coverage across (-6 dB, full angle)'), (axs[1], 'v', 'Coverage up and down (-6 dB, full angle)')):
            style(ax)
            ax.plot(freqs[sel], [np.nan if c[key] is None else c[key] for c, s_ in zip(cov, sel) if s_], color=S1, lw=2, marker='o', ms=4,
                    label='as built: a thin rim')
            ax.plot(fb, [np.nan if c[key] is None else c[key] for c in covb], color=S2, lw=2, marker='o', ms=4, label='proposal: a bell lip')
            ax.axvline(XO, color=INK, lw=0.8, ls=':')
            ax.set_xscale('log'); ax.set_ylim(0, 160)
            tk = [t for t in (500, 1000, 2000, 4000) if t <= top]
            ax.set_xticks(tk); ax.set_xticklabels([f'{t // 1000}k' if t >= 1000 else str(t) for t in tk]); ax.minorticks_off()
            ax.set_xlim(400, top * 1.05)
            ax.set_title(ttl); ax.set_xlabel('frequency (Hz)'); ax.set_ylabel('degrees')
        axs[0].legend(frameon=False, fontsize=9, loc='upper right')
        ax = axs[2]; style(ax)
        zb = np.array([1j * r['k'] * complex(*r['1']['p_face']) for r in bell])
        ax.plot(freqs[sel], z.real[sel], color=S1, lw=2, marker='o', ms=4, label='as built')
        ax.plot(fb, zb.real, color=S2, lw=2, marker='o', ms=4, label='bell lip')
        ax.axhline(1, color=INK2, lw=0.8, ls='--')
        ax.axvline(XO, color=INK, lw=0.8, ls=':')
        ax.set_xscale('log')
        tk = [t for t in (250, 500, 1000, 2000, 4000) if t <= top]
        ax.set_xticks(tk); ax.set_xticklabels([f'{t // 1000}k' if t >= 1000 else str(t) for t in tk]); ax.minorticks_off()
        ax.set_xlim(250, top * 1.05)
        ax.set_title('Throat resistance (1 = a plane wave)'); ax.set_xlabel('frequency (Hz)')
        ax.legend(frameon=False, fontsize=9, loc='upper right')
        fig.suptitle('A bell-flared lip (proposal, not built) against the thin rim as built', x=0.06, ha='left', fontsize=13, color=INK,
                     fontweight='bold')
        fig.savefig(A / 'bell.png', dpi=130, bbox_inches='tight'); plt.close(fig)
        summary['bell40'] = [{k: c[k] for k in ('f', 'h', 'v', 'up', 'down', 'di')} for c in covb]
        summary['bell40_throat'] = [dict(f=r['f'], r=float(zz.real), x=float(-zz.imag)) for r, zz in zip(bell, zb)]
    (A / 'summary.json').write_text(json.dumps(summary, indent=1))
    for c in cov:
        f_ = lambda x: '  - ' if x is None else f'{x:4.0f}'
        print(f"{c['f']:6.0f}  H {f_(c['h'])}  V {f_(c['v'])} (up {f_(c['up'])}, down {f_(c['down'])})  DI {c['di']:4.1f}")


if __name__ == '__main__':
    main()
