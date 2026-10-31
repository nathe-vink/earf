// A product's render model for the web: the fabkit build's GLB (render/<name>.glb, every part one named mesh, no
// materials) made small enough to send to a phone. Each part takes a material named by its finish (from the build's
// sidecar, render/<name>.json), so the viewer can paint by finish; what a visitor cannot see at arm's length (the plates'
// printed words, the ink, the labels) goes; the parts are merged by finish, welded, simplified within a tenth of a
// millimetre, quantized and meshopt-compressed.
//
//   node compress.mjs <in.glb> <sidecar.json> <out.glb> [--drop name,name] [--error 0.0001]
import { NodeIO } from '@gltf-transform/core';
import { EXTMeshoptCompression, KHRMeshQuantization } from '@gltf-transform/extensions';
import { dedup, flatten, join, weld, simplify, prune, quantize, meshopt } from '@gltf-transform/functions';
import { MeshoptEncoder, MeshoptSimplifier } from 'meshoptimizer';
import fs from 'node:fs';

const [inp, side, out, ...rest] = process.argv.slice(2);
const opt = (k, d) => { const i = rest.indexOf(k); return i >= 0 ? rest[i + 1] : d; };
const DROP = new Set(['amp-plate-print', 'rating-plate-print', 'amp-plate-ink', 'amp-plate-labels', 'amp-plate-sticker',
  ...opt('--drop', '').split(',').filter(Boolean)]);
const ERROR = +opt('--error', '0.0001');
const finishes = JSON.parse(fs.readFileSync(side, 'utf8')).finishes;

await MeshoptEncoder.ready; await MeshoptSimplifier.ready;
const io = new NodeIO().registerExtensions([EXTMeshoptCompression, KHRMeshQuantization]).registerDependencies({ 'meshopt.encoder': MeshoptEncoder });
const doc = await io.read(inp);
const root = doc.getRoot(), mats = {};
for (const node of root.listNodes()) {
  const mesh = node.getMesh(); if (!mesh) continue;
  const name = mesh.getName() || node.getName();
  if (DROP.has(name)) { node.setMesh(null); continue; }
  const f = finishes[name] || 'other';
  mats[f] ||= doc.createMaterial(f);
  for (const p of mesh.listPrimitives()) { p.setMaterial(mats[f]); p.setAttribute('TEXCOORD_0', null); }
}
await doc.transform(prune(), dedup({ keepUniqueNames: true }), flatten(), join({ keepNamed: false }), weld(),
  simplify({ simplifier: MeshoptSimplifier, ratio: 0, error: ERROR }), prune(),
  quantize({ quantizePosition: 14, quantizeNormal: 10 }), meshopt({ encoder: MeshoptEncoder, level: 'high' }));
await io.write(out, doc);
const tris = root.listMeshes().reduce((n, m) => n + m.listPrimitives().reduce((a, p) => a + (p.getIndices()?.getCount() || 0) / 3, 0), 0);
console.log(`${out}: ${(fs.statSync(out).size / 1048576).toFixed(2)} MB, ${root.listMeshes().length} meshes, ${Math.round(tris).toLocaleString()} triangles, finishes: ${Object.keys(mats).join(' ')}`);
