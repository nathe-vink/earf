"""Fog: under felt clouds (a first sketch, round 31; the Fog set's own session takes it from here, per BRIEF.md).

A pale paper sky, felt clouds of the Fog icon's three circles hung on threads at three depths, felt hills behind and
cotton-wool fog banks round the speaker's feet, seen from above through a tilt-shift lens.
"""
from common import bank, cloud, finish, kit, mound, portrait_of, shot as frame, soft, tilt_shift


def shot():
    props = [mound(-2.1, 1.7, -0.25, 1.7, 0.9, 0.8, '#CBD3D8'), mound(1.9, 2.0, -0.3, 2.0, 1.0, 0.9, '#D3D9DD'),
             mound(0.1, 2.45, -0.45, 2.6, 0.7, 1.0, '#C3CCD2')]
    props += cloud(-1.15, 0.55, 2.2, 0.0014) + cloud(1.0, 1.15, 2.65, 0.0017) + cloud(-0.15, 1.9, 3.15, 0.0012, color='#ECEEEF') \
        + cloud(1.85, 0.2, 1.85, 0.00095)
    props += bank(-1.7, -0.32, -0.38, 0.0, 0.07, 0.17, 1) + bank(0.3, 1.9, 0.5, 0.0, 0.08, 0.2, 2) \
        + bank(0.45, 1.25, -0.7, 0.0, 0.05, 0.11, 3) + bank(-2.4, -0.9, 1.0, 0.0, 0.09, 0.22, 4)
    st = {'kind': 'sweep', 'color': '#C5CFD7', 'width': 14.0, 'front': 9.0, 'depth': 2.7, 'radius': 1.2, 'height': 6.0,
          'kit_scale': 11.0, 'props': props}
    return frame('fog', st, soft(), tilt_shift(elevation=22, azimuth=-18, distance=7.2, lens=60, target=(0.1, 0.4, 0.75),
                                               focus=(0.0, -0.2, 0.7)),
                 'barkhorn, Fog, under felt clouds', sky={'kind': 'gradient', 'zenith': '#DDE4EA', 'horizon': '#E4E8EC',
                                                         'ground': '#9AA3AA', 'strength': 0.6},
                 fin=finish(bloom=0.15, saturation=0.08, lift=0.03, lift_color='#9FB0C0', vignette=0.12))


def portrait():
    return portrait_of(shot(), lens=50)
