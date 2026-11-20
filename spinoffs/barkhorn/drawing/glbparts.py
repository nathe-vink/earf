"""The render model's parts (out-cloud/render/barkhorn-cloud.glb) as triangle arrays in the Cloud's CAD frame, millimetres:
x across (0..560), y front to back (the horn's front at -0.1), z up (the feet's pads at -12)."""
import os
import numpy as np, pygltflib

GLB = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'out-cloud', 'render', 'barkhorn-cloud.glb')
_DT = {5120: np.int8, 5121: np.uint8, 5122: np.int16, 5123: np.uint16, 5125: np.uint32, 5126: np.float32}
_N = {'SCALAR': 1, 'VEC2': 2, 'VEC3': 3, 'VEC4': 4}


def _acc(g, blob, i):
    a = g.accessors[i]; bv = g.bufferViews[a.bufferView]
    dt = np.dtype(_DT[a.componentType]); n = _N[a.type]
    off = (bv.byteOffset or 0) + (a.byteOffset or 0)
    stride = bv.byteStride or dt.itemsize * n
    raw = np.frombuffer(blob, dtype=np.uint8, count=stride * (a.count - 1) + dt.itemsize * n, offset=off)
    out = np.lib.stride_tricks.as_strided(raw, shape=(a.count, dt.itemsize * n), strides=(stride, 1)).copy()
    return out.view(dt).reshape(a.count, n) if n > 1 else out.view(dt).reshape(a.count)


def parts(path=GLB):
    """{name: (V (n,3) float mm, F (m,3) int)}: each part placed by its own node, in the CAD frame (the file's Y-up root turn
    left out)."""
    g = pygltflib.GLTF2().load(path); blob = g.binary_blob()
    out = {}
    for n in g.nodes:
        if n.mesh is None:
            continue
        Vs, Fs, base = [], [], 0
        for pr in g.meshes[n.mesh].primitives:
            V = _acc(g, blob, pr.attributes.POSITION).astype(float)
            F = _acc(g, blob, pr.indices).reshape(-1, 3).astype(int) if pr.indices is not None else np.arange(len(V)).reshape(-1, 3)
            Vs.append(V); Fs.append(F + base); base += len(V)
        V = np.vstack(Vs)
        if n.matrix:
            M = np.array(n.matrix, float).reshape(4, 4).T
        else:
            M = np.eye(4)
            if n.scale: M = M @ np.diag([*n.scale, 1.0])
            if n.rotation:
                x, y, z, w = n.rotation
                R = np.array([[1 - 2 * (y * y + z * z), 2 * (x * y - z * w), 2 * (x * z + y * w)],
                              [2 * (x * y + z * w), 1 - 2 * (x * x + z * z), 2 * (y * z - x * w)],
                              [2 * (x * z - y * w), 2 * (y * z + x * w), 1 - 2 * (x * x + y * y)]])
                T = np.eye(4); T[:3, :3] = R; M = T @ M
            if n.translation:
                T = np.eye(4); T[:3, 3] = n.translation; M = T @ M
        V = (np.c_[V, np.ones(len(V))] @ M.T)[:, :3] * 1000.0          # metres to millimetres
        out[n.name] = (V, np.vstack(Fs))
    return out
