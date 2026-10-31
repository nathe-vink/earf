const { chromium } = require('playwright'); const path = require('path');
(async () => { const [src, pdf, png] = process.argv.slice(2);
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 480, height: 1344 }, deviceScaleFactor: 2 });
  await p.goto('file://' + path.resolve(src), { waitUntil: 'networkidle' }); await p.evaluate(() => document.fonts.ready);
  await p.pdf({ path: pdf, width: '5in', height: '7in', printBackground: true });
  if (png) await p.screenshot({ path: png, fullPage: true }); await b.close(); })();
