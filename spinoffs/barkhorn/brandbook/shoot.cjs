// Screenshot every scene in scenes/ (or those named) to out/<name>.png, its size from <body data-w data-h [data-scale]>.
//   node shoot.cjs [name ...]
const { chromium } = require('playwright');
const fs = require('fs'), path = require('path'), url = require('url');
const here = __dirname;
(async () => {
  const names = process.argv.slice(2).length ? process.argv.slice(2)
    : fs.readdirSync(path.join(here, 'scenes')).filter(f => f.endsWith('.html')).map(f => f.slice(0, -5));
  const browser = await chromium.launch();
  for (const n of names) {
    const file = path.join(here, 'scenes', n + '.html');
    const html = fs.readFileSync(file, 'utf8');
    const num = (k, d) => +((html.match(new RegExp(`data-${k}="([\\d.]+)"`)) || [0, d])[1]);
    const page = await browser.newPage({ viewport: { width: num('w', 1600), height: num('h', 1000) }, deviceScaleFactor: num('scale', 2) });
    await page.goto(url.pathToFileURL(file).href, { waitUntil: 'networkidle' });
    await page.evaluate(() => document.fonts.ready);
    await page.waitForTimeout(300);
    await page.screenshot({ path: path.join(here, 'out', n + '.png'), omitBackground: /data-transparent/.test(html) });
    console.log('shot', n);
    await page.close();
  }
  await browser.close();
})();
