// The press kit as one PDF, printed from the press page itself (its print styles in web.py), so it never disagrees
// with the page: site/press/earf-press-kit.pdf. Run after web.py.
//
//   node presskit.mjs [chromium path]
import { chromium } from 'playwright-core';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
const SITE = path.join(path.dirname(path.dirname(fileURLToPath(import.meta.url))), 'site');
const b = await chromium.launch({ executablePath: process.argv[2] || '/opt/pw-browsers/chromium' });
const pg = await b.newPage({ viewport: { width: 1200, height: 900 }, reducedMotion: 'reduce' });
await pg.goto('file://' + path.join(SITE, 'index.html') + '#press');
await pg.evaluate(async () => { document.querySelectorAll('#press img').forEach(i => { i.loading = 'eager'; });
  await Promise.all([...document.querySelectorAll('#press img')].map(i => i.decode().catch(() => {}))); await document.fonts.ready; });
await pg.pdf({ path: path.join(SITE, 'press', 'earf-press-kit.pdf'), format: 'A4', printBackground: true, preferCSSPageSize: true,
  displayHeaderFooter: true, headerTemplate: '<span></span>',
  footerTemplate: '<div style="font:7pt monospace;width:100%;text-align:center;color:#777">EARF · press kit · in development, not yet for sale · every picture a render · <span class="pageNumber"></span>/<span class="totalPages"></span></div>' });
await b.close();
console.log('site/press/earf-press-kit.pdf');
