"""Horns and waveguides as solids: a profile r(x) from throat to mouth, a wall of some thickness, a flange at the
throat for the driver and an optional rolled lip at the mouth. Round horns are revolved; rectangular ones lofted
between their sections.

Profiles (x from the throat, r the half width, mm):
  conical(r0, angle_deg, L)                 straight walls
  exponential(r0, fc, L)                    r = r0 e^(m x / 2), m = 4 pi fc / c: loads the driver down to fc
  tractrix(fc, r0)                          the mouth radius c / (2 pi fc), the length set by r0 (the classic shape)
  os(r0, angle_deg, L)                      oblate-spheroidal waveguide: r = sqrt(r0^2 + (x tan a)^2), constant
                                            directivity to its coverage angle, the throat's slope continuous

    from speaker.horn import tractrix, round_horn, rect_horn
    prof = tractrix(fc=500, r0=12.7)
    shell = round_horn(prof, wall=4, flange=dict(d=110, t=10, bolt_d=76, bolts=4, bolt_hole=6.5), lip=12)

The shell's local frame: the axis is z, the throat at z = 0, the mouth at z = L, the driver's flange behind the throat
at z = -t (place it with speaker.drivers.place). The wall is offset along its normal and the lip rolls back over the
outside, so a tractrix (square to the axis at its mouth) keeps its full wall.
Nothing here simulates: a horn's real response wants a BEM run (earmilk's fab/bem.py does that for its waveguide).
"""
import math

import numpy as np
from build123d import Axis, Polyline, Pos, loft, make_face, revolve, Wire, Sketch, Plane, Rectangle, Solid, Cylinder, Align

C_MM = 343000.0


def conical(r0, angle_deg, L, n=40):
    t = math.tan(math.radians(angle_deg / 2))
    return [(x, r0 + x * t) for x in np.linspace(0, L, n)]


def exponential(r0, fc, L, n=60):
    m = 4 * math.pi * fc / C_MM
    return [(x, r0 * math.exp(m * x / 2)) for x in np.linspace(0, L, n)]


def tractrix(fc, r0, n=80):
    """The tractrix from a throat radius r0 to its mouth radius rm = c / (2 pi fc), where the wall turns square to the
    axis. x is measured from the throat."""
    rm = C_MM / (2 * math.pi * fc)
    if r0 >= rm:
        raise ValueError(f'throat radius {r0} is not smaller than the mouth {rm:.0f} for {fc} Hz')
    def xm(r):           # distance back from the mouth plane for radius r
        s = math.sqrt(max(rm * rm - r * r, 0.0))
        return rm * math.log((rm + s) / r) - s
    L = xm(r0)
    rs = np.geomspace(r0, rm * 0.999, n)
    return [(L - xm(r), r) for r in rs]


def os(r0, angle_deg, L, n=50):
    t = math.tan(math.radians(angle_deg / 2))
    return [(x, math.sqrt(r0 * r0 + (x * t) ** 2)) for x in np.linspace(0, L, n)]


def _clean(pts):
    out = []
    for q in pts:
        if not out or abs(q[0] - out[-1][0]) > 1e-6 or abs(q[1] - out[-1][1]) > 1e-6:
            out.append(q)
    return out


def shell_profile(profile, wall=4.0, lip=0.0):
    """The horn's wall in its (x, r) half plane: the inner (air) surface along `profile` [(x, r)], throat to mouth,
    then, if `lip` > 0, rolled back over the outside on a quarter-plus arc of radius `lip` (as a trumpet's bell: from
    the mouth's slope round until it points back toward the throat), and the outer surface `wall` away along the
    surface's normal (not straight out from the axis: a tractrix's wall turns square to the axis at its mouth, where
    a radial offset would leave no wall at all). Returns (inner, outer), each [(x, r)] from the throat."""
    P = np.array(_clean([(float(x), float(r)) for x, r in profile]))
    inner = [tuple(q) for q in P]
    if lip > 0:
        assert lip > wall + 1.0, f'the lip ({lip}) must be wider than the wall ({wall}) to roll round it'
        t = P[-1] - P[-2]; t /= np.linalg.norm(t)
        a0 = math.atan2(t[1], t[0])                     # the mouth's slope, from the axis
        nl = np.array([-t[1], t[0]])                    # left of the way along: into the wall
        c = P[-1] + lip * nl
        for ph in np.linspace(a0 - math.pi / 2, math.pi / 2, 16)[1:]:
            inner.append((c[0] + lip * math.cos(ph), c[1] + lip * math.sin(ph)))
    I = np.array(inner)
    T = np.gradient(I, axis=0); T /= np.linalg.norm(T, axis=1, keepdims=True)
    N = np.c_[-T[:, 1], T[:, 0]]
    outer = [tuple(q) for q in I + wall * N]
    return inner, outer


def round_horn(profile, wall=4.0, flange=None, lip=0.0, liner=0.0):
    """A revolved horn shell: the inner surface on `profile` [(x, r)] (x from the throat), `wall` thick along its
    normal, its mouth rolled back on a lip of radius `lip` (0: a plain edge), and a throat flange behind the throat
    (dict d, t, and optionally bolt_d, bolts, bolt_hole): the driver bolts to its back face, at z = -t. Local frame:
    the axis is z, the throat at z = 0, the mouth toward +z. Each surface is a spline, so it draws and renders smooth.
    With `liner` > 0 it returns (shell, liner): a skin that thick just inside the air surface, for painting the bell's
    inside apart from its outside in a render."""
    from geom import revolve_profile
    inner, outer = shell_profile(profile, wall, lip)
    n = len(inner)
    pts = [(r, x) for x, r in inner] + [(r, x) for x, r in reversed(outer)]
    shell = revolve_profile(pts, axis='z', smooth=[(0, n - 1), (n, 2 * n - 1)])
    if flange:
        r0 = inner[0][1]
        fl = Pos(0, 0, -flange['t']) * (Cylinder(flange['d'] / 2, flange['t'], align=(Align.CENTER, Align.CENTER, Align.MIN)) -
                                        Cylinder(r0, flange['t'] + 1, align=(Align.CENTER, Align.CENTER, Align.MIN)))
        if flange.get('bolts'):
            for k in range(flange['bolts']):
                a = 2 * math.pi * (k + 0.5) / flange['bolts']
                fl = fl - Pos(flange['bolt_d'] / 2 * math.cos(a), flange['bolt_d'] / 2 * math.sin(a), -flange['t'] - 0.5) * \
                     Cylinder(flange['bolt_hole'] / 2, flange['t'] + 1, align=(Align.CENTER, Align.CENTER, Align.MIN))
        shell = shell + fl
    if liner > 0:
        I = np.array(inner)
        T = np.gradient(I, axis=0); T /= np.linalg.norm(T, axis=1, keepdims=True)
        Ni = I - liner * np.c_[-T[:, 1], T[:, 0]]       # a skin on the air side
        lp = [(r, x) for x, r in I] + [(r, x) for x, r in reversed(Ni)]
        return shell, revolve_profile(lp, axis='z', smooth=[(0, n - 1), (n, 2 * n - 1)])
    return shell


def outer_radius_at(profile, x, wall=4.0, lip=0.0):
    """The shell's outside radius at axial position x (from the throat), for a saddle or a clamp, ignoring the rolled
    lip's return (the largest r of the outer surface at that x)."""
    _, outer = shell_profile(profile, wall, lip)
    O = np.array(outer)
    best = None
    for (x0, r0), (x1, r1) in zip(O[:-1], O[1:]):
        if (x0 - x) * (x1 - x) <= 0 and abs(x1 - x0) > 1e-9:
            r = r0 + (r1 - r0) * (x - x0) / (x1 - x0)
            best = r if best is None else max(best, r)
    return best


def rect_horn(profile_w, profile_h, wall=4.0, n_sections=12, flange=None):
    """A rectangular horn: half widths from `profile_w` [(x, half width)] and half heights from `profile_h` [(x, half
    height)] (sampled at the same x), the shell lofted between rectangular sections, `wall` thick."""
    xs = np.linspace(profile_w[0][0], profile_w[-1][0], n_sections)
    hw = np.interp(xs, [p[0] for p in profile_w], [p[1] for p in profile_w])
    hh = np.interp(xs, [p[0] for p in profile_h], [p[1] for p in profile_h])
    def body(grow):
        secs = [Plane.XY.offset(x) * Rectangle(2 * (w + grow), 2 * (h + grow)) for x, w, h in zip(xs, hw, hh)]
        return loft(secs)
    shell = body(wall) - body(0.0)
    if flange:
        fl = Pos(0, 0, 0) * Cylinder(flange['d'] / 2, flange['t'], align=(Align.CENTER, Align.CENTER, Align.MIN))
        shell = shell + (fl - body(0.0))
    return shell


def mouth_for_coverage(fc, angle_deg):
    """The mouth width (mm) a horn needs to hold its coverage `angle_deg` down to fc Hz: Keele's rule (AES preprint
    1038, 1975), W = 25e3 / (theta f) metres; a 90 degree horn holds to 1 kHz with a 278 mm mouth."""
    return 25.0e6 / (angle_deg * fc)


def _se_wire(w, h, n, z, pts=72):
    """A closed superellipse |x/w|^n + |y/h|^n = 1 at height z, as one periodic spline (one smooth face when lofted:
    no seams at the corners, as a rounded rectangle's straight-and-arc edges leave). The points start at a corner,
    where they lie close together: started at a side's middle, where a square section's points lie far apart, the
    spline's closure dented that side by up to 1.6 mm (round 5)."""
    from build123d import Edge, Wire, Vector
    P = []
    for k in range(pts):
        t = math.pi / 4 + 2 * math.pi * k / pts
        c, s_ = math.cos(t), math.sin(t)
        P.append(Vector(w * math.copysign(abs(c) ** (2 / n), c), h * math.copysign(abs(s_) ** (2 / n), s_), z))
    return Wire([Edge.make_spline(P, periodic=True)])


def _se_sections(r0, half_w, half_h, depth, n_mouth=4.5, n=12, beyond=0.0, grow=0.0, z0=0.0, before=0.0):
    """Superellipse sections of a rectangular waveguide: round at the throat (n = 2, radius r0), each half dimension
    growing as sqrt(r0^2 + (z tan a)^2), squaring off toward the mouth (n -> n_mouth). `grow` inflates every section
    (the wall's outside), `beyond` runs straight on past the mouth so a cut opens through the face."""
    ta = math.sqrt(max(half_w ** 2 - r0 ** 2, 0.0)) / depth
    tb = math.sqrt(max(half_h ** 2 - r0 ** 2, 0.0)) / depth
    out = [_se_wire(r0 + grow, r0 + grow, 2.0, z0 - before)] if before else []      # straight on behind the throat
    for i in range(n + 1):
        z = depth * (i / n) ** 1.3
        w = math.sqrt(r0 ** 2 + (z * ta) ** 2) + grow
        h = math.sqrt(r0 ** 2 + (z * tb) ** 2) + grow
        out.append(_se_wire(w, h, 2.0 + (n_mouth - 2.0) * (z / depth) ** 1.2, z0 + z))
    if beyond:
        out.append(_se_wire(half_w + grow, half_h + grow, n_mouth, z0 + depth + beyond))
    return out


def _rr_sections(r0, half_w, half_h, depth, corner, n=10, beyond=0.0, grow=0.0, z0=0.0):
    """Rounded-rectangle sections of an oblate-spheroidal-like waveguide from a round throat (radius r0, z = z0) to a
    rounded-rectangle mouth (half_w x half_h, corner radius `corner`, z = z0 + depth): each half dimension grows as
    sqrt(r0^2 + (z tan a)^2), so the walls start square to the throat and open to their mouth angle; the corners go
    from round at the throat to `corner` at the mouth. `grow` inflates every section (an offset of the wall), `beyond`
    adds a straight run past the mouth (so a cut opens through the face)."""
    from build123d import RectangleRounded, Plane
    ta = math.sqrt(max(half_w ** 2 - r0 ** 2, 0.0)) / depth
    tb = math.sqrt(max(half_h ** 2 - r0 ** 2, 0.0)) / depth
    secs = []
    zs = [depth * (i / n) ** 1.3 for i in range(n + 1)]
    for z in zs:
        w = math.sqrt(r0 ** 2 + (z * ta) ** 2) + grow
        h = math.sqrt(r0 ** 2 + (z * tb) ** 2) + grow
        s = (z / depth) ** 1.5
        rc = min(w, h) * (1 - s) + (corner + grow) * s
        rc = min(rc, min(w, h) - 0.02)
        secs.append(Plane.XY.offset(z0 + z) * RectangleRounded(2 * w, 2 * h, rc))
    if beyond:
        secs.append(Plane.XY.offset(z0 + depth + beyond) * RectangleRounded(2 * (half_w + grow), 2 * (half_h + grow), min(corner + grow, min(half_w, half_h) + grow - 0.02)))
    return secs


def waveguide_block(width, height, depth, mouth_w, mouth_h, mouth_corner, r0=12.7, wall=8.0, edge=40.0, corner_r=70.0,
                    back_edge=20.0, boss=None, solid=False, n_mouth=4.5):
    """A rectangular waveguide cast as one block: a rounded box `width` x `height` x `depth` (its depth-wise corners
    on `corner_r`, the front edges on `edge`, the back's on `back_edge`) with the waveguide (round throat r0 on the
    back face, a `mouth_w` x `mouth_h` rounded-rectangle mouth on the front) through it. Hollow unless `solid`: an outer
    skin and the waveguide's own skin, both `wall` thick, a void between (a cast or printed shell, not a solid ingot);
    `boss` (dict d, t, bolt_d, bolts, bolt_hole) on the back round the throat takes the driver. Local frame: x across,
    y up, z from the back face (z = 0, the throat) to the front (z = depth)."""
    from build123d import Box, Align, Pos, Cylinder, fillet, Axis, loft
    outer = Box(width, height, depth, align=(Align.CENTER, Align.CENTER, Align.MIN))
    outer = fillet(outer.edges().filter_by(Axis.Z), corner_r)
    outer = fillet(outer.edges().group_by(Axis.Z)[-1], edge)
    outer = fillet(outer.edges().group_by(Axis.Z)[0], back_edge)
    # the waveguide's surface: superellipse sections, round at the throat, squaring toward the mouth (n_mouth), lofted
    # through splines so it is one smooth face (`mouth_corner` is kept for the older rounded-rectangle sections)
    # the loft runs on straight through the back face and past the mouth, so it opens both (a cylinder unioned to it
    # at the throat would meet it edge to edge, a tangency OpenCascade mishandles)
    cav = Solid.make_loft(_se_sections(r0, mouth_w / 2, mouth_h / 2, depth, n_mouth, beyond=5.0, before=6.0), False)
    body = outer
    if not solid:
        t = wall
        void = Box(width - 2 * t, height - 2 * t, depth - 2 * t, align=(Align.CENTER, Align.CENTER, Align.MIN))
        void = Pos(0, 0, t) * fillet(void.edges().filter_by(Axis.Z), max(corner_r - t, 2.0))
        grown = Solid.make_loft(_se_sections(r0, mouth_w / 2, mouth_h / 2, depth, n_mouth, grow=t, beyond=5.0, before=6.0), False)
        body = body - (void - grown)
    body = body - cav
    if boss:
        b = Pos(0, 0, -boss['t']) * (Cylinder(boss['d'] / 2, boss['t'], align=(Align.CENTER, Align.CENTER, Align.MIN)) -
                                     Cylinder(r0, boss['t'] + 1, align=(Align.CENTER, Align.CENTER, Align.MIN)))
        for k in range(boss.get('bolts', 0)):
            a = 2 * math.pi * (k + 0.5) / boss['bolts']
            b = b - Pos(boss['bolt_d'] / 2 * math.cos(a), boss['bolt_d'] / 2 * math.sin(a), -boss['t'] - 0.5) * \
                Cylinder(boss['bolt_hole'] / 2, boss['t'] + 1, align=(Align.CENTER, Align.CENTER, Align.MIN))
        body = body + b
    return body


def _smax(a, b, k=8.0):
    """A smooth maximum: the larger of a and b, rounded where they cross (so a flare meets a pod without a crease)."""
    return (a ** k + b ** k) ** (1.0 / k)


def waveguide_shell(mouth_w, mouth_h, depth, r0=12.7, wall=6.0, rim=10.0, n_mouth=4.5, pod_r=74.0, pod_back=70.0,
                    dome=45.0, cable_d=10.0, boss=None, n=14, round_rim=0.0, pads=(), cap_hole=True, tub=None,
                    solid_neck=False):
    """A rectangular waveguide as a thin cast shell that follows its own flare: the inner (air) surface a superellipse
    waveguide (round at the throat r0, squaring toward the `mouth_w` x `mouth_h` mouth, n_mouth), the outside `wall`
    away, thickening to a `rim` at the mouth, and behind the throat a round pod (`pod_r`, `pod_back` long) that hides
    the compression driver, the flare running into it smoothly. The pod is open at the back; `dome` is a separate cap
    that closes it, with a hole for the cable. Local frame: x across, y up, z from the throat (0) to the mouth (depth);
    the pod behind, z < 0. Returns (shell, cap).

    `round_rim` rounds the rim over a crest halfway through its thickness, the air surface and the outside each curving
    to it over about that radius (so the rim reads as a rolled edge, not a flat face).
    `pads`: bosses under the shell that take its mounting posts, each {'x', 'z' (where, local), 'd' (across), 'h' (how far
    its flat foot stands below the lowest point of the shell over it), 'bore' and 'bore_depth' (the hole for the
    post's thread or insert, up from the foot), 'cable' (a hole of that diameter on up through the shell, for a cable
    run down inside the post)}. The flare and the pod's void trim each boss, so none pokes into the air path.
    `cap_hole` False leaves the cap without the cable's hole (the cable leaves through a pad instead).
    `solid_neck`: the neck between the flare and the pod cast solid, not hollow (the pod's void stops behind the boss):
    in translucent resin a hollow there shows through as a squarish shadow round the throat, solid resin as a round,
    deeper halo, as the photograph's.
    `tub` {'back' (how far behind the throat the back wall's outside stands), 'taper' (how much smaller the back than the
    rim), 'round' (the share of the depth the back's edges round over in), 'end' (the back wall's size against the rim),
    'lid' (how deep the removable back is), 'seam'}: instead of following the flare, the outside runs straight back from
    the rim as a tub, rounding over into a flat back wall that hides the driver; the flare is its own skin inside, the
    space between them hollow. The cap is then the tub's back (`lid` deep, a `seam` gap), screwed on."""
    from build123d import Pos, Cylinder, Align
    hw, hh = mouth_w / 2, mouth_h / 2
    ta = math.sqrt(max(hw ** 2 - r0 ** 2, 0.0)) / depth
    tb = math.sqrt(max(hh ** 2 - r0 ** 2, 0.0)) / depth

    if tub:
        zb, L = -tub['back'], depth + tub['back']

        def outer(z, inset=0.0):
            t = min(max((depth - z) / L, 0.0), 1.0)
            r_ = tub['round']
            u = max(0.0, (t - (1 - r_)) / r_)          # 0 until the rounding begins, 1 at the back
            e = tub['end'] + (1 - tub['end']) * math.sqrt(max(1 - u * u, 0.0))
            k = (1 - tub['taper'] * t) * e
            return (hw + rim) * k - inset, (hh + rim) * k - inset, n_mouth - (n_mouth - 4.0) * t
    else:
        def outer(z, inset=0.0):
            if z >= 0:
                zz = min(z, depth)
                w = math.sqrt(r0 ** 2 + (zz * ta) ** 2); h = math.sqrt(r0 ** 2 + (zz * tb) ** 2)
                nn = 2.0 + (n_mouth - 2.0) * (zz / depth) ** 1.2
                grow = wall + (rim - wall) * max(0.0, (zz - (depth - 25.0)) / 25.0) ** 2
                W, H = _smax(w + grow, pod_r), _smax(h + grow, pod_r)
                pod = (pod_r / max(W, H)) ** 4                   # how much the pod rules here: round where it does
                return W - inset, H - inset, nn * (1 - pod) + 2.0 * pod
            return pod_r - inset, pod_r - inset, 2.0

    def flare(z):                                # the air surface's section at z
        return math.sqrt(r0 ** 2 + (z * ta) ** 2), math.sqrt(r0 ** 2 + (z * tb) ** 2), 2.0 + (n_mouth - 2.0) * (z / depth) ** 1.2

    def rounding(f, za, wc, hc):
        """Sections from z = za, where they leave surface f along its own slope, curving toward (wc, hc) at the mouth's
        plane: a quadratic Bezier in each half dimension, sampled at evenly spaced z (sections bunched where it turns
        flat make the loft overshoot), so the rim's crest is a narrow flat between two rounded shoulders."""
        (w0, h0, n0), (w1, h1, _) = f(za), f(za - 0.5)
        qw, qh = w0 + (w0 - w1) / 0.5 * (depth - za), h0 + (h0 - h1) / 0.5 * (depth - za)
        out = []
        for k in range(5):
            u = 1.0 - math.sqrt(1.0 - k / 4) if k < 4 else 0.82      # z = za + k (depth - za) / 4; the last eased off flat
            a, b, c = (1 - u) ** 2, 2 * u * (1 - u), u * u
            out.append((a * w0 + b * qw + c * wc, a * h0 + b * qh + c * hc, n0, za + (depth - za) * k / 4))
        return out

    if tub:                                      # dense where the back's edges round over
        zs = [zb + L * f for f in (0.003, 0.012, 0.03, 0.055, 0.09, 0.135, 0.19, 0.26, 0.36, 0.48, 0.6, 0.72, 0.83, 0.92, 1.0)]
    else:
        zs = sorted(set([-pod_back, -pod_back * 0.6, -pod_back * 0.25, 0.0] + [depth * (i / n) ** 1.25 for i in range(1, n + 1)]))
    back_run = (boss['t'] + 2.0) if boss else 6.0    # the air path runs straight on behind the throat, through any boss
    if round_rim > 0:                            # the rim rounded over a crest halfway through its thickness
        ra = round_rim
        crest = (hw + rim / 2, hh + rim / 2)
        osecs = [(*outer(z)[:2], outer(z)[2], z) for z in zs if z < depth - ra - 4.0] + rounding(outer, depth - ra, *crest)
        csecs = [(*flare(z)[:2], flare(z)[2], z) for z in [depth * (i / 12) ** 1.3 for i in range(0, 13)] if z < depth - ra - 4.0]
        csecs = [(r0, r0, 2.0, -back_run)] + csecs + rounding(flare, depth - ra, *crest) + [(crest[0] + 4.0, crest[1] + 4.0, n_mouth, depth + 3.0)]
        outer_solid = Solid.make_loft([_se_wire(W, H, nn, z) for W, H, nn, z in osecs], False)
        cav = Solid.make_loft([_se_wire(W, H, nn, z) for W, H, nn, z in csecs], False)
    else:
        outer_solid = Solid.make_loft([_se_wire(*outer(z)[:2], outer(z)[2], z) for z in zs], False)
        cav = Solid.make_loft(_se_sections(r0, hw, hh, depth, n_mouth, beyond=5.0, before=back_run), False)
    zv = (zb + wall) if tub else (-pod_back - 1.0)
    zt = -(boss['t'] if boss else wall) if (solid_neck and not tub) else depth - wall
    vz = [zv] + [z for z in zs if zv < z < zt] + [zt]
    void = Solid.make_loft([_se_wire(*outer(z, wall)[:2], outer(z, wall)[2], z) for z in vz], False)
    grown = Solid.make_loft(_se_sections(r0, hw, hh, depth, n_mouth, grow=wall, beyond=5.0, before=6.0), False)
    body = outer_solid
    feet = []
    for pd in pads:                             # bosses under the shell for its posts, fused before the voids are cut
        W, H, nn = outer(pd['z'])
        r = pd['d'] / 2
        def under(x):                           # the shell's underside (outer surface, y < 0) at x, section z
            u = min(abs(x) / W, 0.999999)
            return -H * (1 - u ** nn) ** (1 / nn)
        zs_ = [pd['z'] - r, pd['z'], pd['z'] + r]
        low = min(-outer(z_)[1] * (1 - min(abs(pd['x'] + dx) / outer(z_)[0], 0.999999) ** outer(z_)[2]) ** (1 / outer(z_)[2])
                  for z_ in zs_ for dx in (-r, 0.0, r))
        foot = low - pd['h']
        top = under(pd['x']) + 2 * wall + r     # well into the wall; the voids trim what rises past it
        boss_ = Pos(pd['x'], foot, pd['z']) * Cylinder(r, top - foot, rotation=(-90, 0, 0), align=(Align.CENTER, Align.CENTER, Align.MIN))
        body = body + boss_
        feet.append((pd, foot))
    shell = body - (void - grown)
    if boss:                                    # the driver's mounting boss, fused before the air path is cut through it
        b = Pos(0, 0, -boss['t']) * Cylinder(boss['d'] / 2, boss['t'], align=(Align.CENTER, Align.CENTER, Align.MIN))
        for k in range(boss.get('bolts', 0)):
            a = 2 * math.pi * (k + 0.5) / boss['bolts']
            b = b - Pos(boss['bolt_d'] / 2 * math.cos(a), boss['bolt_d'] / 2 * math.sin(a), -boss['t'] - 0.5) * \
                Cylinder(boss['bolt_hole'] / 2, boss['t'] + 1, align=(Align.CENTER, Align.CENTER, Align.MIN))
        shell = shell + b
    shell = shell - cav
    for pd, foot in feet:                       # the posts' holes, up from each foot; a cable's on through the shell
        shell = shell - Pos(pd['x'], foot - 1.0, pd['z']) * Cylinder(pd['bore'] / 2, pd['bore_depth'] + 1.0, rotation=(-90, 0, 0),
                                                                    align=(Align.CENTER, Align.CENTER, Align.MIN))
        if pd.get('cable'):                     # on up through the shell's wall into the pod, no farther
            W, H, nn = outer(pd['z'])
            u = min(abs(pd['x']) / W, 0.999999)
            reach = -H * (1 - u ** nn) ** (1 / nn) + 2 * wall
            shell = shell - Pos(pd['x'], foot - 1.0, pd['z']) * Cylinder(pd['cable'] / 2, reach - foot + 1.0, rotation=(-90, 0, 0),
                                                                        align=(Align.CENTER, Align.CENTER, Align.MIN))
    if tub:                                      # the back, split off as a lid a seam's width clear of the rest
        from build123d import Box
        zl = zb + tub['lid']
        big = 4 * (hw + hh + rim)
        lid = shell & (Pos(0, 0, zl - tub['seam'] / 2) * Box(big, big, big, align=(Align.CENTER, Align.CENTER, Align.MAX)))
        shell = shell & (Pos(0, 0, zl + tub['seam'] / 2) * Box(big, big, big, align=(Align.CENTER, Align.CENTER, Align.MIN)))
        return shell, lid
    # the cap: an ellipsoidal dome on the pod's back, a spigot inside the pod (0.3 clear) to locate it, the cable's hole
    z0 = -pod_back
    rings = [(z0 - dome * u, max(pod_r * math.sqrt(max(1 - u * u, 0.0)), cable_d / 2 + wall + 2)) for u in (0.0, 0.3, 0.55, 0.75, 0.9, 1.0)]
    cap_out = Solid.make_loft([_se_wire(r, r, 2.0, z) for z, r in rings], False)
    if cap_hole:
        inner_rings = [(z, max(r - wall, cable_d / 2 + 1.0)) for z, r in rings[:-1]] + [(rings[-1][0] - 1.0, cable_d / 2 + 1.0)]
    else:                                       # closed: the inside stops a wall short of the dome's crown
        inner_rings = [(z + wall * u, max(r - wall, 2.0)) for (z, r), u in zip(rings[:-1], (0.0, 0.3, 0.55, 0.75, 0.9))]
    cap_in = Solid.make_loft([_se_wire(pod_r - wall + 0.0, pod_r - wall, 2.0, z0 + 1.0)] + [_se_wire(r, r, 2.0, z) for z, r in inner_rings], False)
    cap = cap_out - cap_in
    spigot = Pos(0, 0, z0) * (Cylinder(pod_r - wall - 0.3, 10.0, align=(Align.CENTER, Align.CENTER, Align.MIN)) -
                              Cylinder(pod_r - 2 * wall, 11.0, align=(Align.CENTER, Align.CENTER, Align.MIN)))
    cap = cap + spigot
    return shell, cap


def _lens_outer(hw, hh, depth, rim, back, back_r, taper, edge, n_mouth):
    """The lens waveguide's outside, section by section [(W, H, n, z)]: from the front face (the mouth's plane, its
    edge rounded on `edge`) back to a round back `back_r` across at z = -back, each half dimension falling as
    (1 - t/T)^taper with the depth t behind the front: steep at once, so the edge is thin, and flat at the back,
    where the driver sits."""
    T = depth + back
    Wf, Hf = hw + rim, hh + rim
    prof = lambda t: (1.0 - min(t, T) / T) ** taper

    def sec(t, inset=0.0):
        g = prof(t)
        return (back_r + (Wf - back_r) * g - inset, back_r + (Hf - back_r) * g - inset,
                2.0 + (n_mouth - 2.0) * g ** 2, depth - t)
    out = [sec(edge * (1 - math.cos(th)), edge * (1 - math.sin(th))) for th in np.linspace(0, math.pi / 2, 6)]
    out += [sec(t) for t in [edge + (T - edge) * u for u in (0.08, 0.18, 0.3, 0.44, 0.58, 0.7, 0.8, 0.88, 0.94, 0.98, 1.0)]]
    return out


def waveguide_lens(mouth_w, mouth_h, depth, r0=12.7, rim=14.0, n_mouth=4.5, back=70.0, back_r=84.0, taper=0.55,
                   edge=5.0, pod_r=68.0, pod_wall=8.0, boss=None):
    """A rectangular waveguide cast as a lens: the flare (waveguide_shell's: round at the throat r0, squaring toward
    the `mouth_w` x `mouth_h` mouth) opens in a front face `rim` wide all round, and the body curves back from that
    face (thin at its edge) to a round back `back_r` across, deepest in the middle, where a pod `pod_r` across holds
    the compression driver behind the throat, `pod_wall` inside the back. Cast hollow in production (a 7 mm skin and
    the flare's own); drawn solid for the study. Local frame as waveguide_shell: x across, y up, z from the throat (0)
    to the mouth (depth); the back at z = -back."""
    from build123d import Pos, Cylinder, Align
    hw, hh = mouth_w / 2, mouth_h / 2
    secs = _lens_outer(hw, hh, depth, rim, back, back_r, taper, edge, n_mouth)
    body = Solid.make_loft([_se_wire(W, H, n, z) for W, H, n, z in reversed(secs)], False)
    cav = Solid.make_loft(_se_sections(r0, hw, hh, depth, n_mouth, beyond=5.0, before=6.0), False)
    bt = boss['t'] if boss else 12.0             # the driver's face sits this far behind the throat
    pod = Pos(0, 0, -back + pod_wall) * Cylinder(pod_r, back - pod_wall - bt, align=(Align.CENTER, Align.CENTER, Align.MIN))
    bore = Pos(0, 0, -bt - 1.0) * Cylinder(r0, bt + 2.0, align=(Align.CENTER, Align.CENTER, Align.MIN))   # throat to driver
    return body - cav - pod - bore


def waveguide_slab(mouth_w, mouth_h, depth, r0=12.7, rim=16.0, n_mouth=4.5, slab_t=64.0, wall=6.0, pod_r=74.0,
                   pod_back=70.0, boss=None):
    """A rectangular waveguide as a slim slab, after the photograph's: a flat superellipse slab `slab_t` thick, its edges
    rounded right round (a bar of soap's), the flare's mouth opening in its face; behind the slab the rest of the flare
    in a tail that follows it (`wall` thick) and runs into a round pod (`pod_r`, `pod_back` long) round the driver.
    Local frame as waveguide_shell."""
    from build123d import Pos, Cylinder, Align
    hw, hh = mouth_w / 2, mouth_h / 2
    Wf, Hf = hw + rim, hh + rim
    rr = slab_t / 2
    z0 = depth - slab_t
    slab = Solid.make_loft([_se_wire(Wf - rr * (1 - math.sin(th)), Hf - rr * (1 - math.sin(th)), n_mouth,
                                     z0 + rr - rr * math.cos(th)) for th in np.linspace(0.02, math.pi - 0.02, 13)], False)
    ta = math.sqrt(max(hw ** 2 - r0 ** 2, 0.0)) / depth
    tb = math.sqrt(max(hh ** 2 - r0 ** 2, 0.0)) / depth

    def tail(z):
        w = math.sqrt(r0 ** 2 + (z * ta) ** 2) + wall; h = math.sqrt(r0 ** 2 + (z * tb) ** 2) + wall
        W, H = _smax(w, pod_r), _smax(h, pod_r)
        pod = (pod_r / max(W, H)) ** 4
        return W, H, (2.0 + (n_mouth - 2.0) * (z / depth) ** 1.2) * (1 - pod) + 2.0 * pod
    # sections spaced as waveguide_shell's (a smooth loft through unevenly spaced ones overshoots), ending inside the slab
    zt = [-pod_back, -pod_back * 0.6, -pod_back * 0.25, 0.0] + [z for z in (depth * (i / 14) ** 1.25 for i in range(1, 15))
                                                                if z < z0 + rr - 4.0] + [z0 + rr]
    tailbody = Solid.make_loft([_se_wire(*tail(max(z, 0.0))[:2], tail(max(z, 0.0))[2], z) for z in zt], False)
    cav = Solid.make_loft(_se_sections(r0, hw, hh, depth, n_mouth, beyond=5.0, before=6.0), False)
    bt = boss['t'] if boss else 12.0
    pod = Pos(0, 0, -pod_back + wall) * Cylinder(pod_r - wall, pod_back - wall - bt, align=(Align.CENTER, Align.CENTER, Align.MIN))
    bore = Pos(0, 0, -bt - 1.0) * Cylinder(r0, bt + 2.0, align=(Align.CENTER, Align.CENTER, Align.MIN))   # throat to driver
    return (slab + tailbody) - cav - pod - bore
