# Where the V10 one-way marks sit (crystal.py:1173, :1180): the collar's top face (the arrow) and the crown's lowest
# tier's side at 30 deg (the line). From the meshes: the up-facing faces at the collar's top, the clamp ring's top, the
# crown's side; then the eye heights a fitter would need to see an up-facing face, for the standard hang.
import struct, numpy as np, sys, math
def tri(p):
    b = open(p, 'rb').read(); n = struct.unpack('<I', b[80:84])[0]
    a = np.frombuffer(b[84:84 + n * 50], dtype=np.dtype([('n', '<f4', 3), ('v', '<f4', (3, 3)), ('x', '<u2')]))
    return a['v'].astype(float)
B = sys.argv[1]
for b in ('out-dome-pendant-topA-nolock', 'out-dome-pendant', 'out-dome-pendant-topB'):
    col = tri(f'{B}/{b}--collar.stl'); clp = tri(f'{B}/{b}--clamp.stl'); crn = tri(f'{B}/{b}--crown.stl')
    def upfaces(t, z):
        nrm = np.cross(t[:, 1] - t[:, 0], t[:, 2] - t[:, 0]); nz = nrm[:, 2] / (np.linalg.norm(nrm, axis=1) + 1e-12)
        sel = (nz > 0.99) & (np.abs(t[:, :, 2].mean(1) - z) < 0.05)
        r = np.hypot(t[sel][:, :, 0], t[sel][:, :, 1])
        return (r.min(), r.max(), sel.sum()) if sel.sum() else None
    zc = col[:, :, 2].max(); zk = clp[:, :, 2].max()
    print(b, '| collar top z', round(zc, 2), 'up-face r', [round(x, 2) for x in upfaces(col, zc)[:2]],
          '| clamp top z', round(zk, 2), '| collar stands', round(zc - zk, 2), 'above the clamp ring',
          '| crown z', round(crn[:, :, 2].min(), 2), '..', round(crn[:, :, 2].max(), 2))
# the standard hang: canopy underside 726 above the rim, the canopy 50 tall: the rim 776 under the ceiling
for ceil in (2.44, 2.59, 2.74):
    rim = ceil - 0.776
    print(f'ceiling {ceil} m: rim {rim:.2f} m, collar top (A) {rim + 0.10333:.2f} m, crown line {rim + 0.1033:.2f}-{rim + 0.1147:.2f} m')
