// The site's 3D view (round 47): a product's render model, its acrylic as physically based transmission tinted as the
// renders tint it (the engine's resin: a colour reached after a distance, which is what three.js's attenuation is), lit
// by a small studio made in code (no file to fetch), on the studio's pale ground, turned by hand within limits.
// Loaded only when a visitor asks for it; the page keeps its pictures if WebGL is missing or anything here fails.
//
//   const v = await (await import('./3d/viewer.js')).open(box, spec, tint, { reduce })
//   v.tint(tint)      repaints the acrylic in another colour, the model kept
//   v.dispose()       frees the GPU and removes the canvas
import * as THREE from './three/three.module.min.js';
import { OrbitControls } from './three/OrbitControls.js';
import { GLTFLoader } from './three/GLTFLoader.js';
import { MeshoptDecoder } from './three/meshopt_decoder.module.js';

export function supported() {
  try { const c = document.createElement('canvas'); return !!(window.WebGL2RenderingContext && c.getContext('webgl2')); }
  catch (e) { return false; }
}

// a studio: a big soft key above front left, a fill, a rim from behind and a floor bounce, as emissive panels in a pale
// room, rendered once into the environment (what RoomEnvironment does, lit as the site's studio pictures are)
function studio(renderer) {
  const scene = new THREE.Scene(), box = new THREE.BoxGeometry();
  const room = new THREE.Mesh(box, new THREE.MeshStandardMaterial({ color: 0xdedad3, side: THREE.BackSide, roughness: 1 }));
  room.scale.set(12, 8, 12); room.position.y = 3.5; scene.add(room);
  scene.add(new THREE.HemisphereLight(0xffffff, 0xd8d3ca, 1.2));
  const panel = (w, h, x, y, z, k, warm) => {
    const m = new THREE.Mesh(new THREE.PlaneGeometry(w, h), new THREE.MeshBasicMaterial({ color: new THREE.Color(warm ? 0xfff3e1 : 0xf4f7ff).multiplyScalar(k) }));
    m.position.set(x, y, z); m.lookAt(0, 0.8, 0); scene.add(m);
  };
  panel(3.0, 2.2, -3.2, 4.2, 3.4, 14, true);     // the key, a big softbox high front left
  panel(2.4, 2.4, 4.6, 2.0, 2.4, 2.6, true);    // the fill, right
  panel(1.2, 3.2, 1.0, 3.0, -4.4, 10, false);    // a rim from behind, cool
  panel(0.6, 4.0, -5.0, 2.0, -1.0, 4, false);   // a strip down the left, for a line on the edges
  const pm = new THREE.PMREMGenerator(renderer);
  const env = pm.fromScene(scene, 0.01).texture;
  pm.dispose(); scene.traverse(o => { if (o.geometry) o.geometry.dispose(); if (o.material) o.material.dispose(); });
  return env;
}

// the finishes as the engine paints them (studio/products/<name>.json), simplified to what a browser does
function finishes(spec, tint) {
  const M = {}, P = THREE.MeshPhysicalMaterial;
  for (const [name, f] of Object.entries(spec.finishes)) {
    M[name] = new P({ color: f.color || '#888', roughness: f.roughness ?? 0.5, metalness: f.metal ? 1 : 0,
      clearcoat: f.coat || 0, clearcoatRoughness: 0.3, sheen: f.sheen || 0, sheenColor: new THREE.Color(f.color || '#fff'),
      emissive: f.emit ? new THREE.Color(f.color) : 0x000000, emissiveIntensity: f.emit || 0, envMapIntensity: f.env ?? 1 });
  }
  for (const [name, a] of Object.entries(spec.acrylic)) {      // the tinted parts: clear, the colour a volume
    M[name] = new P({ color: 0xffffff, metalness: 0, roughness: a.roughness, ior: 1.49, transmission: 1, thickness: a.thickness,
      specularIntensity: 1, envMapIntensity: 1.1, side: THREE.DoubleSide });
    // a slab's colour deepens as you look across it: the path through it is its thickness over the cosine of the
    // refracted angle, so a face seen square on is pale and one seen edge-on is deep (three.js takes one thickness)
    M[name].onBeforeCompile = s => { s.fragmentShader = s.fragmentShader.replace('material.thickness = thickness;',
      `material.thickness = thickness;
       { float ci = abs( dot( normal, normalize( vViewPosition ) ) ), si2 = 1.0 - ci * ci;
         material.thickness /= sqrt( max( 1.0 - si2 / 2.22, 0.04 ) ) * mix( 1.0, ci, ${(a.grazing ?? 0.6).toFixed(2)} ); }`); };
    M[name].customProgramCacheKey = () => 'earf-slab-' + (a.grazing ?? 0.6);
  }
  paint(M, spec, tint);
  return M;
}
function paint(M, spec, tint) {
  for (const [name, a] of Object.entries(spec.acrylic)) {
    const m = M[name]; if (!m) continue;
    m.attenuationColor.set(tint[a.deep]); m.attenuationDistance = a.radius;
  }
  for (const [name, key] of Object.entries(spec.tinted || {})) if (M[name]) M[name].color.set(tint[key]);
  // what is inside is lit through the walls, so its light has crossed one wall already: its colour filtered by the tint
  for (const [name, f] of Object.entries(spec.inside || {})) if (M[name]) {
    M[name].color.set(spec.finishes[name].color).multiply(new THREE.Color(tint[f.through])).multiplyScalar(f.dim ?? 1); M[name].envMapIntensity = f.light ?? 0.7; }
}

export async function open(box, spec, tint, { reduce = false, onProgress } = {}) {
  const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: false, powerPreference: 'high-performance' });
  renderer.setPixelRatio(Math.min(devicePixelRatio || 1, 2));
  renderer.toneMapping = THREE.NeutralToneMapping; renderer.toneMappingExposure = spec.exposure ?? 1.0;
    const scene = new THREE.Scene();
  scene.background = new THREE.Color(spec.ground || '#F4F1EC');
  scene.environment = studio(renderer);
  const key = new THREE.DirectionalLight(0xfff3e1, 1.2);       // a little direct light, for the drivers' metal
  key.position.set(-1.6, 3.2, 2.0); scene.add(key);
  const loader = new GLTFLoader().setMeshoptDecoder(MeshoptDecoder);
  const gltf = await loader.loadAsync(spec.src, e => onProgress && e.total && onProgress(e.loaded / e.total));
  const M = finishes(spec, tint), model = gltf.scene;
  model.traverse(o => {
    if (!o.isMesh) return;
    const n = o.material && o.material.name;
    if (spec.hide && spec.hide.includes(n)) { o.visible = false; return; }
    if (M[n]) { o.material.dispose(); o.material = M[n]; }
    o.castShadow = false; o.receiveShadow = false;
  });
  const bb = new THREE.Box3().setFromObject(model), c = bb.getCenter(new THREE.Vector3()), size = bb.getSize(new THREE.Vector3());
  model.position.set(-c.x, -bb.min.y, -c.z); scene.add(model);
  const H = size.y, R = 0.5 * size.length();
  // on the floor: a soft contact shadow under the footprint, and the light the acrylic throws, in its colour (the
  // renders' floors show both; a browser has no caustics, so they are painted, as a photographer's floor would be lit)
  const blob = (inner, outer, stops) => { const c = document.createElement('canvas'); c.width = c.height = 256;
    const g = c.getContext('2d'), r = g.createRadialGradient(128, 128, inner, 128, 128, outer);
    stops.forEach(([at, col]) => r.addColorStop(at, col)); g.fillStyle = r; g.fillRect(0, 0, 256, 256);
    const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace; return t; };
  const shade = new THREE.Mesh(new THREE.PlaneGeometry(size.x * 1.5, size.z * 1.6), new THREE.MeshBasicMaterial({
    map: blob(10, 128, [[0, 'rgba(40,36,32,0.55)'], [0.55, 'rgba(40,36,32,0.22)'], [1, 'rgba(40,36,32,0)']]), transparent: true, depthWrite: false, toneMapped: false }));
  shade.rotation.x = -Math.PI / 2; shade.position.y = 0.0006; scene.add(shade);
  // the pool: the tint's colour, faded out from under the speaker toward the light's far side, alpha-blended (not tone-mapped)
  const pool = new THREE.Mesh(new THREE.PlaneGeometry(size.x * 3, size.x * 3), new THREE.MeshBasicMaterial({
    map: blob(0, 128, [[0, 'rgba(255,255,255,0.5)'], [0.4, 'rgba(255,255,255,0.2)'], [1, 'rgba(255,255,255,0)']]), transparent: true,
    depthWrite: false, toneMapped: false }));
  pool.rotation.x = -Math.PI / 2; pool.position.set(size.x * 0.2, 0.0003, size.z * 0.7); pool.renderOrder = -1; scene.add(pool);
  const glow = t => { const c = new THREE.Color(t[spec.pool || 'horn']); pool.material.color.copy(c);
    pool.material.opacity = spec.poolStrength ?? 0.8; pool.visible = c.getHSL({}).s > 0.15 && c.getHSL({}).l > 0.2; };
  glow(tint);

  const camera = new THREE.PerspectiveCamera(spec.fov || 26, 1, 0.05, 50);
  const target = new THREE.Vector3(0, H * (spec.aim ?? 0.5), 0);
  const fit = () => R / Math.sin(THREE.MathUtils.degToRad(camera.fov) / 2) * (spec.zoom ?? 1.05) / Math.min(1, camera.aspect);
  const az = THREE.MathUtils.degToRad(spec.azimuth ?? -28), el = THREE.MathUtils.degToRad(spec.elevation ?? 8);
  const place = () => { const d = fit(); camera.position.set(target.x + d * Math.cos(el) * Math.sin(az), target.y + d * Math.sin(el), target.z + d * Math.cos(el) * Math.cos(az)); };

  const canvas = renderer.domElement;
  canvas.setAttribute('aria-hidden', 'true'); canvas.tabIndex = -1;
  box.appendChild(canvas);
  const controls = new OrbitControls(camera, canvas);
  controls.target.copy(target); controls.enableDamping = !reduce; controls.dampingFactor = 0.08; controls.enablePan = false;
  controls.minPolarAngle = THREE.MathUtils.degToRad(spec.minPolar ?? 55); controls.maxPolarAngle = THREE.MathUtils.degToRad(spec.maxPolar ?? 96);
  controls.rotateSpeed = 0.6; controls.zoomSpeed = 0.6;
  controls.touches = { ONE: THREE.TOUCH.ROTATE, TWO: THREE.TOUCH.DOLLY_ROTATE };
  let need = true;
  const size_ = () => {
    const w = box.clientWidth, h = box.clientHeight; if (!w || !h) return;
    renderer.setSize(w, h, false); camera.aspect = w / h; camera.updateProjectionMatrix();
    const d = fit(); controls.minDistance = d * 0.55; controls.maxDistance = d * 1.35;
    if (!placed) { place(); placed = true; } need = true;
  };
  let placed = false; size_();
  const ro = new ResizeObserver(size_); ro.observe(box);
  controls.addEventListener('change', () => { need = true; });
  // a slow quarter turn to show it can be turned, then still; never under reduced motion
  let spin = reduce ? 0 : 1, t0 = performance.now(), raf = 0, alive = true;
  controls.addEventListener('start', () => { spin = 0; });
  const tick = now => {
    if (!alive) return;
    raf = requestAnimationFrame(tick);
    if (spin) { const p = Math.min(1, (now - t0) / 2600), e = p < 1 ? 1 - Math.pow(1 - p, 3) : 1;
      controls.setAzimuthalAngle(az + e * THREE.MathUtils.degToRad(spec.intro ?? 40)); if (p >= 1) spin = 0; need = true; }
    if (controls.update() || need) { renderer.render(scene, camera); need = false; }
  };
  raf = requestAnimationFrame(tick);
  // keys: the arrows turn it, + and - bring it nearer (the box is the focusable element, not the canvas)
  const keys = e => {
    const a = THREE.MathUtils.degToRad(12);
    if (e.key === 'ArrowLeft' || e.key === 'ArrowRight') { e.preventDefault(); spin = 0; controls.setAzimuthalAngle(controls.getAzimuthalAngle() + (e.key === 'ArrowLeft' ? a : -a)); }
    else if (e.key === 'ArrowUp' || e.key === 'ArrowDown') { e.preventDefault(); spin = 0;
      const p = THREE.MathUtils.clamp(controls.getPolarAngle() + (e.key === 'ArrowUp' ? -a / 2 : a / 2), controls.minPolarAngle, controls.maxPolarAngle);
      const s = new THREE.Spherical().setFromVector3(camera.position.clone().sub(controls.target)); s.phi = p;
      camera.position.copy(controls.target).add(new THREE.Vector3().setFromSpherical(s)); }
    else if (e.key === '+' || e.key === '=' || e.key === '-') { e.preventDefault(); spin = 0;
      const v = camera.position.clone().sub(controls.target), d = THREE.MathUtils.clamp(v.length() * (e.key === '-' ? 1.12 : 0.89), controls.minDistance, controls.maxDistance);
      camera.position.copy(controls.target).add(v.setLength(d)); }
    else return;
    controls.update(); need = true;
  };
  box.addEventListener('keydown', keys);
  return {
    tint(t) { paint(M, spec, t); glow(t); need = true; },
    reset() { place(); controls.target.copy(target); controls.update(); need = true; },
    dispose() {
      alive = false; cancelAnimationFrame(raf); ro.disconnect(); box.removeEventListener('keydown', keys); controls.dispose();
      scene.traverse(o => { if (o.geometry) o.geometry.dispose(); });
      Object.values(M).forEach(m => m.dispose()); scene.environment.dispose();
      renderer.dispose(); renderer.forceContextLoss(); canvas.remove();
    },
  };
}
