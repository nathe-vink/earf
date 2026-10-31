// node topdf.cjs page.html out.pdf [out.png]: a page to a Letter PDF (and a PNG proof at 150 dpi)
const { chromium } = require('playwright'); const path = require('path');
(async () => {
  const [src, pdf, png] = process.argv.slice(2);
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 816, height: 1056 }, deviceScaleFactor: 2 });
  await p.goto('file://' + path.resolve(src), { waitUntil: 'networkidle' }); await p.evaluate(() => document.fonts.ready);
  await p.pdf({ path: pdf, format: 'Letter', printBackground: true });
  if (png) await p.screenshot({ path: png, clip: { x: 0, y: 0, width: 816, height: 1056 } });
  await b.close();
})();
