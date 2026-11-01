// usage: node shoot_pair.js preview.html outA.png outB.png  (B = text transparent, shadows kept)
const { chromium } = require('/opt/node-tools/node_modules/playwright');
const path = require('path');
(async () => {
  const [src, a, b] = process.argv.slice(2);
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1920, height: 1080 } });
  await page.goto('file://' + path.resolve(src));
  await page.evaluate(() => document.fonts.ready); await page.waitForTimeout(200);
  await page.screenshot({ path: a });
  await page.addStyleTag({ content: 'section *{color:transparent !important}' });
  await page.waitForTimeout(100);
  await page.screenshot({ path: b });
  await browser.close();
})();
