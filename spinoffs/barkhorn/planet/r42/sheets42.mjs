// The round 42 sheets to PNG previews and one PDF, through the pre-installed Chromium (no install step).
//   node spinoffs/barkhorn/planet/r42/sheets42.mjs OUTDIR sheet1.svg sheet2.svg ...
// Each SVG is an ARCH D sheet (36 x 24 in) in millimetres; the PDF keeps it vector, one sheet a page.
import { createRequire } from 'module';
const { chromium } = createRequire(import.meta.url)('playwright');
import fs from 'fs';
import path from 'path';

const [out, ...svgs] = process.argv.slice(2);
const browser = await chromium.launch();
const page = await browser.newPage({ viewport: { width: 3456, height: 2304 }, deviceScaleFactor: 1 });
for (const f of svgs) {
  const svg = fs.readFileSync(f, 'utf8');
  await page.setContent(`<html><body style="margin:0;background:#fff">${svg.replace(/width="[\d.]+mm" height="[\d.]+mm"/, 'width="3456" height="2304"')}</body></html>`);
  await page.evaluate(() => document.fonts.ready);
  await page.screenshot({ path: path.join(out, path.basename(f, '.svg') + '.png'), clip: { x: 0, y: 0, width: 3456, height: 2304 } });
}
const body = svgs.map(f => `<div class="s">${fs.readFileSync(f, 'utf8')}</div>`).join('');
await page.setContent(`<html><head><style>@page{size:36in 24in;margin:0}body{margin:0}.s{width:36in;height:24in;page-break-after:always;overflow:hidden}.s svg{width:36in;height:24in;display:block}</style></head><body>${body}</body></html>`);
await page.evaluate(() => document.fonts.ready);
await page.pdf({ path: path.join(out, 'planet-earf-r42-drawings.pdf'), width: '36in', height: '24in', printBackground: true });
await browser.close();
