"""Fog: above the fog at dawn (round 31's dioramas; BRIEF.md is the direction, fog.md the notes).

Stuffed felt clouds in the icon's shape (three circles on a bar) hang on threads at several depths; cotton wool and a
low fog veil the speaker's feet; a pale dawn glows behind it all and lights the clear acrylic from behind.
"""
from common import finish, kit, point, portrait_of, shot as frame, area, tilt_shift

FELT, SEAM, COTTON = '#F5F5F3', '#DADDE0', '#FBFBFA'


def plush(x, y, z, s, rz=0.0, top=5.5, color=FELT, threads=True, fuzz=25000):
    """A stuffed felt cloud, the icon's shape, centred on (x, y, z), `s` metres an icon unit, hung on two threads."""
    out = [kit('ext', 'felt', color, module='fog', fn='plush', size=s, stitch=SEAM, position=[x, y, z], rotate=[0, 0, rz],
               fuzz=fuzz, fibre=0.005)]
    if threads:
        import math
        c, sn = math.cos(math.radians(rz)), math.sin(math.radians(rz))
        for ix, iz in ((-171, 35), (187, 67)):
            a = [x + ix * s * c, y + ix * s * sn, z + iz * s]
            out.append(kit('thread', 'paper', '#A8A39A', a=a, b=[a[0], a[1], top], radius=0.002))
    return out


def wool(puffs, fuzz=0, seed=1, tear=0.4):
    """Cotton wool pulled into a bank: lumpy, deep-scattering, fibres teased out of it."""
    return [kit('ext', 'cotton', COTTON, module='fog', fn='wool', puffs=puffs, fuzz=fuzz, fibre=0.03, tear=tear,
                squash=0.55, seed=seed)]


WALL = 2.6            # the paper sky stands this far behind the speaker, so the horn is seen against it


def mist(density=2.6, height=0.44):
    return [kit('ext', 'cotton', '#FFFFFF', module='fog', fn='mist', box=[-5.0, -1.2, 0.0, 5.0, WALL - 0.02, height + 0.12],
                height=height, density=density, billow=0.5, clump=0.85, step=3.0)]


def sun(x, z, r, emit=2.0):
    """A tissue-paper sun on the paper sky, lit from behind: the dawn."""
    return [kit('cylinder', 'tissue', '#FFE4CC', radius=r, height=0.01, position=[x, WALL - 0.05, z], rotate=[90, 0, 0],
                emit=emit, segments=96)]


def props():
    p = []
    p += sun(2.45, 0.42, 0.58, emit=3.0)
    # clouds: one at the speaker's depth on the left (crisp, its felt and seam legible), one behind on the right above
    # the sun, and a small one far off
    p += plush(-0.89, 0.6, 1.43, 0.00105, rz=10, fuzz=30000)
    # the joke: a balsa ladder up from the fog to that cloud, as if someone had just gone up to hang it
    p.append(kit('ext', 'card', '#D8BC94', module='fog', fn='ladder', a=[-0.6, 0.78, -0.02], b=[-0.78, 0.66, 1.24],
                 width=0.15, step=0.1, strip=0.013, across=[1, 0.3, 0]))
    p += plush(2.23, 1.26, 1.45, 0.0014, rz=-6, fuzz=0)
    p += plush(1.1, 1.65, 1.62, 0.0008, rz=4, fuzz=0)
    # cotton wool: a drift round the speaker's feet (more at the front left), a few islands, the bank on the horizon the
    # sun sinks into, and soft lumps close to the lens
    p += wool([[-0.62, -0.3, 0.08, 0.3], [-0.3, -0.48, 0.04, 0.16], [-0.98, -0.05, 0.06, 0.24], [-0.75, 0.32, 0.05, 0.2],
               [-1.2, -0.35, 0.04, 0.16], [-0.45, -0.62, 0.02, 0.1], [0.42, -0.42, 0.02, 0.1], [0.66, -0.18, 0.03, 0.14],
               [0.6, 0.35, 0.05, 0.2], [0.1, 0.48, 0.05, 0.22]], seed=1, tear=0.5)
    p += wool([[-1.9, 1.1, 0.05, 0.3], [-1.55, 1.3, 0.04, 0.22], [-2.25, 0.9, 0.04, 0.2]], seed=4, tear=0.45)
    p += wool([[1.55, 0.95, 0.05, 0.26], [1.9, 1.15, 0.04, 0.22], [1.25, 1.2, 0.04, 0.16]], seed=5, tear=0.45)
    p += wool([[3.2, 2.2, 0.06, 0.42], [2.6, 2.3, 0.06, 0.44], [2.0, 2.2, 0.05, 0.36], [1.4, 2.3, 0.05, 0.34],
               [0.7, 2.2, 0.05, 0.3], [0.0, 2.3, 0.05, 0.36], [-0.7, 2.25, 0.05, 0.32], [-1.4, 2.3, 0.05, 0.38],
               [-2.1, 2.2, 0.05, 0.34], [-2.8, 2.3, 0.05, 0.4], [-3.5, 2.2, 0.05, 0.36], [-4.2, 2.3, 0.05, 0.4]], seed=2)
    p += wool([[-1.55, -0.95, 0.06, 0.3], [-1.2, -1.15, 0.05, 0.22], [-1.85, -0.7, 0.05, 0.2], [0.75, -1.25, 0.05, 0.24],
               [1.1, -1.1, 0.06, 0.3], [1.45, -0.85, 0.05, 0.22], [1.9, -0.6, 0.06, 0.28], [2.2, -0.25, 0.05, 0.22]], seed=3)
    p += mist()
    # the floor: pale felt laid over the table, the paper sky only behind
    p.append(kit('box', 'felt', '#DCE2E8', size=[12.0, 6.4, 0.012], position=[0.0, -1.0, 0.0]))
    return p


def lights():
    return {
        # the dawn: low behind, warm, through the fog and the clear acrylic
        'dawn': {'type': 'area', 'size_m': [2.6, 1.6], 'position': [2.2, 2.2, 1.5], 'target': [0.0, 0.1, 0.7],
                 'irradiance': 3.2, 'color': '#FFD8B8', 'receivers': ['[!sz]*', 's[!w]*']},   # all but the paper sky and the fog
        # the same dawn on the fog alone, gentler, so it glows toward the sun without burning out
        'dawnfog': {'type': 'area', 'size_m': [3.0, 2.0], 'position': [2.2, 2.2, 1.6], 'target': [0.0, 0.1, 0.3],
                    'irradiance': 1.4, 'color': '#FFDCC4', 'receivers': ['zz*']},
        # the glow on the paper sky behind, low like a horizon
        # (light-linked to the paper sky alone, from well in front, so nothing on the set throws a shadow up it)
        'glow': {'type': 'area', 'size_m': [3.0, 1.0], 'position': [2.0, 0.6, 0.55], 'target': [2.2, 2.6, 0.5],
                 'power_w': 160, 'color': '#FFDCC4', 'receivers': ['sweep']},
        # a soft cool sky fill from the front, above
        'sky': area(-35, 50, 6.0, 4.2, '#F4F4F3', (5.0, 5.0), (0.0, 0.0, 0.8)),
    }


def shot():
    st = {'kind': 'sweep', 'color': '#98A8B9', 'width': 16.0, 'front': 10.0, 'depth': WALL, 'radius': 0.5, 'height': 7.0,
          'kit_scale': 12.0, 'props': props()}
    cam = tilt_shift(elevation=16, azimuth=-22, distance=8.0, lens=70, target=(0.32, 0.35, 0.74), focus=(0.0, 0.05, 0.75),
                     fstop=11, miniature=11)
    return frame('fog', st, lights(), cam, 'barkhorn, Fog, above the fog',
                 sky={'kind': 'gradient', 'zenith': '#DDE4EA', 'horizon': '#E8E8EA', 'ground': '#B9C2CA', 'strength': 0.5},
                 fin=finish(bloom=0.22, saturation=0.1, lift=0.04, lift_color='#A8B6C4', vignette=0.18), rotate_z=-6.0, exposure=0.3)


def portrait():
    return portrait_of(shot(), lens=58)
