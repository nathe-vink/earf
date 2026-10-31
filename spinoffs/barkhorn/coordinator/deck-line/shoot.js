// usage: node shoot.js preview.html out.png [scale]
const { chromium } = require('/opt/node-tools/node_modules/playwright');
const path = require('path');
(async () => {
  const [src, out, scale] = process.argv.slice(2);
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1920, height: 1080 }, deviceScaleFactor: Number(scale || 1) });
  await page.goto('file://' + path.resolve(src));
  await page.evaluate(() => document.fonts.ready);
  await page.waitForTimeout(150);
  const fams = await page.evaluate(() => [...document.fonts].filter(f => f.status === 'loaded').map(f => f.family + ' ' + f.weight));
  await page.screenshot({ path: out });
  console.log('fonts loaded:', fams.join(', '));
  await browser.close();
})();
