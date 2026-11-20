// SVG to PNG in the container's Chromium (ImageMagick here has no SVG delegate): node svg2png.mjs IN.svg OUT.png [scale]
import { createRequire } from 'module';
const require = createRequire(import.meta.url);
let pw; try { pw = require('playwright'); } catch { pw = require('playwright-core'); }
import fs from 'fs';
const [inp, out, sc] = process.argv.slice(2);
const svg = fs.readFileSync(inp, 'utf8');
const W = +svg.match(/width="(\d+)"/)[1], H = +svg.match(/height="(\d+)"/)[1];
const b = await pw.chromium.launch({ executablePath: '/opt/pw-browsers/chromium', args: ['--no-sandbox'] }).catch(() => pw.chromium.launch());
const p = await b.newPage({ viewport: { width: W, height: H }, deviceScaleFactor: +(sc || 2) });
await p.setContent(`<html><body style="margin:0">${svg}</body></html>`);
await p.screenshot({ path: out, clip: { x: 0, y: 0, width: W, height: H } });
await b.close();
