"""Geometry hash of a GLB: what its shapes are, not how its bytes fall (2026-11-25: the cloud build writes different
bytes for the same sources, 14 hashes over 24-25 Nov). Per mesh (by name): every triangle as its three vertex positions
in world space (node transforms applied), rounded to 0.01 mm, the corners sorted, the triangles sorted; then the meshes
sorted by name. Equal hashes mean the same shapes in the same places.

    python3 studio/glbgeo.py FILE.glb [...]        prints: geometry-hash  triangles  meshes  file"""
import hashlib, json, struct, sys
import numpy as np

COMP = {5120: np.int8, 5121: np.uint8, 5122: np.int16, 5123: np.uint16, 5125: np.uint32, 5126: np.float32}
NCOMP = {'SCALAR': 1, 'VEC2': 2, 'VEC3': 3, 'VEC4': 4, 'MAT4': 16}


def _read(path):
    b = open(path, 'rb').read()
    assert b[:4] == b'glTF'
    off, js, bin_ = 12, None, None
    while off < len(b):
        ln, kind = struct.unpack_from('<II', b, off); chunk = b[off + 8:off + 8 + ln]
        if kind == 0x4E4F534A:
            js = json.loads(chunk)
        elif kind == 0x004E4942:
            bin_ = chunk
        off += 8 + ln
    return js, bin_


def _acc(js, bin_, i):
    a = js['accessors'][i]; v = js['bufferViews'][a['bufferView']]
    dt = np.dtype(COMP[a['componentType']]); n = NCOMP[a['type']]
    start = v.get('byteOffset', 0) + a.get('byteOffset', 0); stride = v.get('byteStride', 0) or dt.itemsize * n
    raw = np.frombuffer(bin_, dtype=np.uint8, count=stride * (a['count'] - 1) + dt.itemsize * n, offset=start)
    out = np.lib.stride_tricks.as_strided(raw, shape=(a['count'], dt.itemsize * n), strides=(stride, 1)).copy()
    return out.view(dt).reshape(a['count'], n)


def _mat(node):
    if 'matrix' in node:
        return np.array(node['matrix'], float).reshape(4, 4).T
    t = node.get('translation', [0, 0, 0]); r = node.get('rotation', [0, 0, 0, 1]); s = node.get('scale', [1, 1, 1])
    x, y, z, w = r
    R = np.array([[1 - 2 * (y * y + z * z), 2 * (x * y - z * w), 2 * (x * z + y * w)],
                  [2 * (x * y + z * w), 1 - 2 * (x * x + z * z), 2 * (y * z - x * w)],
                  [2 * (x * z - y * w), 2 * (y * z + x * w), 1 - 2 * (x * x + y * y)]])
    M = np.eye(4); M[:3, :3] = R * np.array(s); M[:3, 3] = t
    return M


def geo_hash(path):
    js, bin_ = _read(path)
    per = {}
    def walk(i, M):
        nd = js['nodes'][i]; M = M @ _mat(nd)
        if 'mesh' in nd:
            me = js['meshes'][nd['mesh']]
            for pr in me['primitives']:
                P = _acc(js, bin_, pr['attributes']['POSITION']).astype(float)
                P = (np.c_[P, np.ones(len(P))] @ M.T)[:, :3]
                I = _acc(js, bin_, pr['indices']).ravel() if 'indices' in pr else np.arange(len(P))
                T = np.round(P[I.reshape(-1, 3)] * 1e5).astype(np.int64)          # 0.01 mm
                T = np.sort(T.view([('', np.int64)] * 3).reshape(-1, 3), axis=1).view(np.int64).reshape(-1, 9)
                per.setdefault(nd.get('name') or me.get('name', ''), []).append(T)
        for c in nd.get('children', []):
            walk(c, M)
    for s in js.get('scenes', [{'nodes': range(len(js['nodes']))}]):
        for i in s['nodes']:
            walk(i, np.eye(4))
    h = hashlib.sha256(); tris = 0
    for name in sorted(per):
        T = np.concatenate(per[name]); T = T[np.lexsort(T.T[::-1])]; tris += len(T)
        h.update(name.encode()); h.update(T.tobytes())
    return h.hexdigest()[:16], tris, len(per)


if __name__ == '__main__':
    for f in sys.argv[1:]:
        g, t, m = geo_hash(f)
        print(f'{g}  {t} triangles  {m} meshes  {f}')
