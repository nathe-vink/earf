// The 3D view's files (viewer/dist/; web.py copies them to site/3d only while VIEW3D is on): three.js at the pinned version, its three add-ons with their imports made
// relative (no import map, no bundler), the viewer, and each product's model compressed from its fabkit build where the
// build is to hand (a model whose build is not is kept as it is).
//
//   cd spinoffs/barkhorn/viewer && npm install && node build.mjs
import fs from 'node:fs';
import path from 'node:path';
import { execFileSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';

const HERE = path.dirname(fileURLToPath(import.meta.url)), BARK = path.dirname(HERE);
const OUT = path.join(HERE, 'dist'), T = path.join(OUT, 'three'), NM = path.join(HERE, 'node_modules', 'three');
fs.mkdirSync(T, { recursive: true });
const version = JSON.parse(fs.readFileSync(path.join(NM, 'package.json'), 'utf8')).version;
fs.copyFileSync(path.join(NM, 'build', 'three.module.min.js'), path.join(T, 'three.module.min.js'));
for (const [src, out] of [['controls/OrbitControls.js', 'OrbitControls.js'], ['loaders/GLTFLoader.js', 'GLTFLoader.js'],
                          ['utils/BufferGeometryUtils.js', 'BufferGeometryUtils.js'], ['libs/meshopt_decoder.module.js', 'meshopt_decoder.module.js']]) {
  const js = fs.readFileSync(path.join(NM, 'examples', 'jsm', src), 'utf8')
    .replace(/from 'three'/g, "from './three.module.min.js'").replace(/from '\.\.\/utils\/BufferGeometryUtils\.js'/g, "from './BufferGeometryUtils.js'");
  fs.writeFileSync(path.join(T, out), js);
}
fs.writeFileSync(path.join(T, 'VERSION'), `three.js ${version} (MIT), from npm; see spinoffs/barkhorn/viewer/README.md\n`);
fs.copyFileSync(path.join(NM, 'LICENSE'), path.join(T, 'LICENSE'));
fs.copyFileSync(path.join(HERE, 'viewer.js'), path.join(OUT, 'viewer.js'));
// the models: site name, the fabkit build's render folder, and what else to leave out
const MODELS = [['tropos', 'out-cloud/render/barkhorn-cloud']];
for (const [name, base] of MODELS) {
  const glb = path.join(BARK, base + '.glb');
  if (!fs.existsSync(glb)) { console.log(`${name}: no build to hand (${base}.glb), kept as it is`); continue; }
  execFileSync('node', [path.join(HERE, 'compress.mjs'), glb, path.join(BARK, base + '.json'), path.join(OUT, `${name}.glb`)], { stdio: 'inherit' });
}
console.log(`three.js ${version} into ${path.relative(BARK, OUT)}`);
