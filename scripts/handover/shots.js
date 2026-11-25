const { chromium, devices } = require('playwright');
const URL = 'https://abhimanyu04.codeberg.page/mohali-urban-growth/', out = process.argv[2];
(async () => {
  const b = await chromium.launch(); const errs = [];
  const watch = (p) => { p.on('pageerror', (e) => errs.push('pageerror: ' + e.message)); p.on('console', (m) => { if (m.type() === 'error' && !/fonts\.g|tile\.openstreetmap|arcgisonline|ERR_|photon|Failed to load resource/.test(m.text())) errs.push('console: ' + m.text()); }); };
  const open = async (hash = '') => { const p = await b.newPage({ viewport: { width: 1440, height: 900 }, deviceScaleFactor: 2 }); watch(p); await p.goto(URL + hash); await p.waitForFunction(() => !document.getElementById('tourBtn').disabled, null, { timeout: 90000 }); await p.waitForTimeout(1500); return p; };
  const base = async (p, v, op) => { await p.selectOption('#basemap', v); if (op !== undefined) await p.$eval('#opacity', (e, o) => { e.value = o; e.dispatchEvent(new Event('input')); }, op); await p.waitForTimeout(1500); };
  let p = await open(); await base(p, 'landsat', 85); await p.screenshot({ path: `${out}/webmap_01_overview_2025.png` });
  await p.click('#vcompare'); await p.waitForTimeout(1500); await p.screenshot({ path: `${out}/webmap_02_compare_2015_2025.png` }); await p.close();
  p = await open(); await base(p, 'landsat', 85); await p.fill('#q', 'Kharar'); await p.waitForTimeout(300); await p.keyboard.press('Enter'); await p.waitForTimeout(2500); await p.screenshot({ path: `${out}/webmap_03_search_kharar.png` }); await p.close();
  p = await open(); await base(p, 'landsat', 85); await p.check('#grid'); await p.waitForTimeout(1500); await p.screenshot({ path: `${out}/webmap_04_hex_grid.png` }); await p.close();
  p = await open(); await p.click('#tourBtn'); await p.waitForTimeout(1500); await p.click('#tourNext'); await p.waitForTimeout(1500); await p.click('#tourNext'); await p.waitForTimeout(2500); await p.screenshot({ path: `${out}/webmap_05_tour_change.png` });
  for (let i = 0; i < 4; i++) { await p.click('#tourNext'); await p.waitForTimeout(1800); }
  await p.waitForTimeout(1500); await p.screenshot({ path: `${out}/webmap_07_satellite_compare.png` }); await p.close();
  const ctx = await b.newContext({ ...devices['iPhone 13'] }); p = await ctx.newPage(); watch(p);
  await p.goto(URL); await p.waitForFunction(() => !document.getElementById('tourBtn').disabled, null, { timeout: 90000 }); await p.waitForTimeout(1000);
  const overflow = await p.evaluate(() => document.documentElement.scrollWidth > innerWidth);
  await p.screenshot({ path: `${out}/webmap_06_phone.png` }); await ctx.close();
  console.log('phone overflow:', overflow, '\nerrors:', errs); await b.close();
})();
