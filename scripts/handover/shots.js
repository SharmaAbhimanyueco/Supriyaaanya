// Ready-made screenshots of the web dashboard (served locally). Usage: node shots.js <out dir>
const { chromium, devices } = require('playwright');
const URL = 'http://127.0.0.1:8765/index.html';
const out = process.argv[2];
(async () => {
  const b = await chromium.launch();
  const ready = async (p) => { await p.waitForFunction(() => /Ready/.test(document.getElementById('status').textContent), null, { timeout: 60000 }); await p.waitForTimeout(1500); };
  const desk = async (hash = '') => { const p = await b.newPage({ viewport: { width: 1440, height: 900 }, deviceScaleFactor: 2, colorScheme: 'light' }); await p.goto(URL + hash); await ready(p); return p; };
  const log = {};
  let p = await desk(); await p.screenshot({ path: `${out}/webmap_01_overview_2025.png` }); log.kpis = await p.$$eval('#vKpis .kpi b', (e) => e.map((x) => x.textContent)); await p.close();
  p = await desk(); await p.click('#vchange'); await p.waitForTimeout(1200); await p.screenshot({ path: `${out}/webmap_02_change_2015_2025.png` });
  log.change = await p.$$eval('#classes li', (e) => e.map((x) => x.textContent.replace(/\s+/g, ' ').trim())); await p.close();
  p = await desk(); await p.fill('#q', 'Kharar'); await p.waitForTimeout(300); await p.keyboard.press('Enter'); await p.waitForTimeout(1800);
  log.profile = [await p.textContent('#h-profile'), await p.$$eval('#pKpis .kpi b', (e) => e.map((x) => x.textContent))];
  await p.screenshot({ path: `${out}/webmap_03_search_kharar.png` }); await p.close();
  p = await desk(); await p.check('#grid'); await p.waitForTimeout(1200); await p.screenshot({ path: `${out}/webmap_04_hex_grid.png` });
  log.ticks = await p.$$eval('#hexTicks span', (e) => e.map((x) => x.textContent));
  await p.selectOption('#zone', 'E'); await p.waitForTimeout(1200); await p.screenshot({ path: `${out}/webmap_05_east_zone_ranking.png` });
  log.rankEast = await p.$$eval('#rank button', (e) => e.slice(0, 3).map((x) => x.textContent.replace(/\s+/g, ' ').trim())); await p.close();
  const ctx = await b.newContext({ ...devices['iPhone 13'], colorScheme: 'light' });
  p = await ctx.newPage(); await p.goto(URL + '#kharar'); await ready(p); await p.screenshot({ path: `${out}/webmap_06_phone.png` }); await ctx.close();
  console.log(JSON.stringify(log, null, 1));
  await b.close();
})();
