// node svg2png.cjs: drawings/*.svg -> drawings/*.png (fonts loaded), 1400 x 900 at 1.5x
const { chromium } = require('playwright'); const fs = require('fs'), path = require('path');
(async () => {
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1400, height: 900 }, deviceScaleFactor: 1.5 });
  for (const f of fs.readdirSync('drawings').filter(f => f.endsWith('.svg'))) {
    const svg = fs.readFileSync(path.join('drawings', f), 'utf8');
    await p.setContent(`<html><head><style>@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500&family=Instrument+Sans:wght@400..700&display=block');body{margin:0}</style></head><body>${svg}</body></html>`, { waitUntil: 'networkidle' });
    await p.evaluate(() => document.fonts.ready);
    await p.screenshot({ path: path.join('drawings', f.replace('.svg', '.png')) });
  }
  await b.close();
})();
