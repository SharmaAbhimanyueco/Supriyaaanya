// Builds slides/Urban_Growth_Mohali_slides.pptx from results/results.json and results/maps/*.png.
// Usage: node scripts/slides/build_deck.js <out.pptx>   (needs pptxgenjs, react-icons, react, react-dom, sharp;
// PPTX_SKILL_DIR must point at the pptx skill folder that contains scripts/apply_theme.js)
const path = require('path');
const pptxgen = require('pptxgenjs');
const React = require('react');
const ReactDOMServer = require('react-dom/server');
const sharp = require('sharp');
const fa = require('react-icons/fa6');

const SKILL = process.env.PPTX_SKILL_DIR || '/root/.claude/skills/synced/c9bdf813-47d6-4116-9b3e-2798304a1cc4_49c63783-d931-47c3-95c9-b4bb58cfb4f5/pptx';
const ROOT = path.resolve(__dirname, '..', '..');
const { applyTheme } = require(path.join(SKILL, 'scripts/apply_theme.js'));
const OUT = process.argv[2];
const MAP_IMG = path.join(ROOT, 'slides', 'assets', 'location_map.jpg');
const WEB_IMG = path.join(ROOT, 'slides', 'assets', 'webmap_dashboard.jpg');
const RES = path.join(ROOT, 'results', 'maps');
const F = require(path.join(ROOT, 'results', 'results.json'));

// ---------- numbers ----------
const n0 = (x) => Math.round(x).toLocaleString('en-US');
const p1 = (x) => (Math.round(x * 10) / 10).toFixed(1);
const BU = { 2015: F.area['2015']['Built-up'], 2020: F.area['2020']['Built-up'], 2025: F.area['2025']['Built-up'] };
const SH = { 2015: F.share['2015']['Built-up'], 2025: F.share['2025']['Built-up'] };
const C1525 = F.change['2015-2025'], C1520 = F.change['2015-2020'], C2025 = F.change['2020-2025'];
const ZW = F.zones['West zone (Kharar and Mohali)'], ZE = F.zones['East zone (Dera Bassi, incl. Zirakpur)'];
const totalHa = F.area['2015'].Total;
const UEII_ALL = (BU[2025] - BU[2015]) / (totalHa * 10) * 100;
const seeds = Object.values(F.bu_by_seed);
const rng = (y) => `${n0(Math.min(...seeds.map((s) => s[y])))}–${n0(Math.max(...seeds.map((s) => s[y])))}`;
const inert = Object.values(F.training.runs).map((r) => r.inertia);
const inertDiffPct = (Math.max(...inert) - Math.min(...inert)) / Math.min(...inert) * 100;
const SR = F.sample_runs.summary;
const ACC = F.acc;
const ADJ = ACC.builtup_area_2025;
const WC = F.wc;
const RAT = F.raters;
const NAMING = F.naming; // cluster -> class
const groupsOf = (cls) => Object.keys(NAMING).filter((k) => NAMING[k] === cls).map(Number).sort((a, b) => a - b);

const THEME = {
  name: 'Urban Growth Mohali', headFontFace: 'Cambria', bodyFontFace: 'Calibri',
  colors: { dk1: '1F2A2E', lt1: 'FFFFFF', dk2: '22363C', lt2: 'EDF1EE', accent1: 'B03A2E', accent2: '8DB63C', accent3: '2E6B3F', accent4: '2F7FB0', accent5: 'D9A441', accent6: '5F6F73', hlink: '2F7FB0', folHlink: '5F6F73' },
};
const pres = new pptxgen();
pres.layout = 'LAYOUT_WIDE';
pres.theme = { headFontFace: THEME.headFontFace, bodyFontFace: THEME.bodyFontFace };
pres.title = 'Mapping Urban Growth in the Mohali-Kharar-Zirakpur-Dera Bassi Belt, Punjab';
pres.subject = 'Urban growth LULC analysis, 2015-2025';
pres.author = 'Supriya Mahshere, Aanya Upadhyay';
const C = pres.SchemeColor;
const CLASS_COLOURS = { 1: C.accent1, 2: C.accent2, 3: C.accent3, 4: C.accent4, 5: C.accent5 };
const CLASS_NAMES = [[1, 'Built-up'], [2, 'Cropland'], [3, 'Trees/vegetation'], [4, 'Water'], [5, 'Bare/fallow']];
const FOOTER = 'Mapping urban growth · Mohali–Kharar–Zirakpur–Dera Bassi';

pres.defineSlideMaster({ title: 'TITLE_DARK', background: { color: C.text2 }, objects: [
  { placeholder: { options: { name: 'title', type: 'title', x: 0.7, y: 1.2, w: 6.8, h: 2.45, fontSize: 38, bold: true, color: C.background1, valign: 'top', align: 'left', margin: 0 }, text: '' } },
  { placeholder: { options: { name: 'body', type: 'body', x: 0.7, y: 3.92, w: 6.8, h: 0.85, fontSize: 18, color: C.background2, valign: 'top', align: 'left', margin: 0 }, text: '' } },
] });
pres.defineSlideMaster({ title: 'CONTENT', background: { color: C.background1 }, margin: [0.5, 0.6, 0.6, 0.6], objects: [
  { placeholder: { options: { name: 'title', type: 'title', x: 0.6, y: 0.35, w: 12.13, h: 0.85, fontSize: 36, bold: true, color: C.text1, valign: 'middle', align: 'left', margin: 0 }, text: '' } },
  { text: { text: FOOTER, options: { x: 0.6, y: 7.02, w: 8, h: 0.3, fontSize: 10, color: C.accent6, margin: 0 } } },
], slideNumber: { x: 12.23, y: 7.02, w: 0.5, h: 0.3, fontSize: 10, color: '5F6F73', align: 'right' } });
pres.defineSlideMaster({ title: 'CLOSING_DARK', background: { color: C.text2 }, margin: [0.5, 0.6, 0.6, 0.6], objects: [
  { placeholder: { options: { name: 'title', type: 'title', x: 0.6, y: 0.35, w: 12.13, h: 0.85, fontSize: 36, bold: true, color: C.background1, valign: 'middle', align: 'left', margin: 0 }, text: '' } },
  { text: { text: FOOTER, options: { x: 0.6, y: 7.02, w: 8, h: 0.3, fontSize: 10, color: C.background2, margin: 0 } } },
], slideNumber: { x: 12.23, y: 7.02, w: 0.5, h: 0.3, fontSize: 10, color: 'EDF1EE', align: 'right' } });

// ---------- helpers ----------
const iconCache = {};
async function iconData(name, hex = 'FFFFFF') {
  const key = name + hex;
  if (!iconCache[key]) {
    let svg = ReactDOMServer.renderToStaticMarkup(React.createElement(fa[name], { size: 256 }));
    svg = svg.replace(/currentColor/g, '#' + hex);
    if (!svg.includes('xmlns=')) svg = svg.replace('<svg', '<svg xmlns="http://www.w3.org/2000/svg"');
    const buf = await sharp(Buffer.from(svg)).resize(256, 256, { fit: 'contain', background: { r: 0, g: 0, b: 0, alpha: 0 } }).png().toBuffer();
    iconCache[key] = 'image/png;base64,' + buf.toString('base64');
  }
  return iconCache[key];
}
async function iconCircle(slide, name, x, y, d, fill, label) {
  slide.addShape(pres.shapes.OVAL, { x, y, w: d, h: d, fill: { color: fill }, objectName: label + ' icon background' });
  const pad = d * 0.25;
  slide.addImage({ data: await iconData(name), x: x + pad, y: y + pad, w: d - 2 * pad, h: d - 2 * pad, altText: label + ' icon', objectName: label + ' icon' });
}
const nb = (x) => x.replace(/(\d) (ha|m²|m\b|km²|km\b|%)/g, '$1\u00a0$2').replace(/(\d) × (\d)/g, '$1\u00a0×\u00a0$2');
function tb(slide, text, opts) { const t = typeof text === 'string' ? nb(text) : text.map((r) => Object.assign({}, r, { text: nb(r.text) })); slide.addText(t, Object.assign({ margin: 0, isTextBox: true, color: C.text1, valign: 'top', fontSize: 15 }, opts)); }
function kicker(slide, text) { tb(slide, text, { x: 0.6, y: 1.2, w: 12.13, h: 0.5, fontSize: 17, color: C.accent6, objectName: 'Key message' }); }
function card(slide, x, y, w, h, name, fill = C.background2) { slide.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y, w, h, fill: { color: fill }, rectRadius: 0.08, objectName: name }); }
function bulletRuns(items, { number = false, space = 8 } = {}) { return items.map((t, i) => ({ text: t, options: { bullet: number ? { type: 'number' } : true, breakLine: i < items.length - 1, paraSpaceAfter: space } })); }
function classLegend(slide, x, y, colour, widths = [1.15, 1.2, 1.75, 0.95, 1.3], items = CLASS_NAMES) {
  let cx = x;
  items.forEach(([code, name], i) => {
    slide.addShape(pres.shapes.RECTANGLE, { x: cx, y: y + 0.07, w: 0.2, h: 0.2, fill: { color: CLASS_COLOURS[code] }, objectName: 'Legend ' + name });
    tb(slide, name, { x: cx + 0.28, y, w: widths[i] - 0.3, h: 0.34, fontSize: 12, color: colour, valign: 'middle' });
    cx += widths[i];
  });
}
function pixelGrid(slide, x0, y0, rows, size, gap, name) {
  rows.forEach((row, r) => row.split('').forEach((code, c) => slide.addShape(pres.shapes.RECTANGLE, { x: x0 + c * (size + gap), y: y0 + r * (size + gap), w: size, h: size, fill: { color: CLASS_COLOURS[code] }, objectName: `${name} r${r + 1}c${c + 1}` })));
}
function arrow(slide, x, y, w, h, { colour = C.accent6, reverse = false, dashed = false, width = 2 } = {}) {
  const line = { color: colour, width };
  if (dashed) line.dashType = 'dash';
  if (reverse) line.beginArrowType = 'triangle'; else line.endArrowType = 'triangle';
  slide.addShape(pres.shapes.LINE, { x, y, w, h, line, objectName: 'Arrow' });
}
async function analogyCard(slide, text) {
  card(slide, 0.6, 5.75, 12.13, 0.95, 'Everyday comparison');
  await iconCircle(slide, 'FaLightbulb', 0.85, 5.92, 0.6, C.accent5, 'Everyday comparison');
  tb(slide, [{ text: 'In everyday terms: ', options: { bold: true } }, { text }], { x: 1.65, y: 5.8, w: 10.85, h: 0.85, fontSize: 16, valign: 'middle' });
}
function statCard(slide, x, y, w, h, value, label, name, { valueSize = 28, fill = C.background2 } = {}) {
  card(slide, x, y, w, h, name, fill);
  tb(slide, value, { x: x + 0.25, y: y + 0.1, w: w - 0.4, h: 0.7, fontSize: valueSize, bold: true, color: C.accent1, valign: 'middle' });
  tb(slide, label, { x: x + 0.25, y: y + 0.8, w: w - 0.4, h: h - 0.9, fontSize: 14 });
}
const lineChartOpts = (title) => ({
  showTitle: true, title, titleFontSize: 13, titleColor: '1F2A2E', titleFontFace: '+mn-lt', chartColors: ['B03A2E'], lineSize: 2, lineDataSymbol: 'circle', lineDataSymbolSize: 6,
  catAxisLabelColor: '5F6F73', valAxisLabelColor: '5F6F73', catAxisLabelFontSize: 11, valAxisLabelFontSize: 10, catAxisLabelFontFace: '+mn-lt', valAxisLabelFontFace: '+mn-lt',
  valGridLine: { color: 'E3E7E4', size: 0.5 }, catGridLine: { style: 'none' }, showLegend: false,
  showCatAxisTitle: true, catAxisTitle: 'Number of groups (k)', catAxisTitleFontSize: 11, catAxisTitleColor: '5F6F73',
});

async function build() {
  // ===== 1. Title =====
  pres.addSection({ title: 'Introduction' });
  let s = pres.addSlide({ masterName: 'TITLE_DARK', sectionTitle: 'Introduction' });
  s.addText('Mapping Urban Growth in the Mohali–Kharar–Zirakpur–Dera Bassi Belt, Punjab', { placeholder: 'title' });
  s.addText('Land use / land cover (LULC) analysis, 2015–2025', { placeholder: 'body' });
  tb(s, 'How fast is Chandigarh’s neighbourhood turning into city?', { x: 0.7, y: 4.85, w: 6.8, h: 0.55, fontSize: 20, italic: true, color: C.accent5, objectName: 'Tagline' });
  tb(s, [{ text: 'Supriya Mahshere · Aanya Upadhyay', options: { bold: true, breakLine: true } }, { text: 'November 2026' }], { x: 0.7, y: 5.6, w: 6.8, h: 0.85, fontSize: 15, color: C.background1, objectName: 'Team and date' });
  tb(s, '2015', { x: 7.75, y: 1.6, w: 2.22, h: 0.4, fontSize: 16, bold: true, color: C.background1, align: 'center' });
  tb(s, '2025', { x: 10.57, y: 1.6, w: 2.22, h: 0.4, fontSize: 16, bold: true, color: C.background1, align: 'center' });
  pixelGrid(s, 7.75, 2.1, ['332211', '322211', '225221', '242222', '422522', '222222'], 0.32, 0.06, 'Pixel 2015');
  pixelGrid(s, 10.57, 2.1, ['332111', '321111', '221111', '242111', '422512', '222222'], 0.32, 0.06, 'Pixel 2025');
  arrow(s, 10.07, 3.21, 0.4, 0, { colour: C.background1, width: 2.5 });
  classLegend(s, 7.75, 4.55, C.background2, [1.15, 1.2, 1.9], CLASS_NAMES.slice(0, 3));
  classLegend(s, 7.75, 4.92, C.background2, [1.15, 1.5], CLASS_NAMES.slice(3));
  tb(s, 'Illustration only: each square stands for one 30 m pixel.', { x: 7.75, y: 5.4, w: 5.04, h: 0.35, fontSize: 12, color: C.background2 });
  s.addNotes('Title slide. Add the course and teacher name if required. The two coloured grids illustrate the idea (pixels turning from farmland to built-up); they are not real data.');

  // ===== 2. Problem statement =====
  s = pres.addSlide({ masterName: 'CONTENT', sectionTitle: 'Introduction' });
  s.addText('Problem statement', { placeholder: 'title' });
  kicker(s, 'The towns around Chandigarh are growing fast. Planners need a consistent measure of how much, and where.');
  tb(s, 'Why it matters', { x: 0.6, y: 1.95, w: 6.3, h: 0.45, fontSize: 20, bold: true });
  const why = [
    ['FaCity', C.accent1, 'Growth drivers: Chandigarh’s spillover, industrial parks, the international airport, and large township and Aerotropolis projects'],
    ['FaRoad', C.accent6, 'Unplanned sprawl strains water supply, roads and public services'],
    ['FaWheatAwn', C.accent2, 'New building covers productive wheat–rice farmland, which is hard to get back'],
    ['FaMapLocationDot', C.accent4, 'Planners need a consistent, repeatable measure of how much built-up land has grown, and where'],
  ];
  for (let i = 0; i < why.length; i++) { const y = 2.6 + i * 1.02; await iconCircle(s, why[i][0], 0.6, y, 0.55, why[i][1], 'Why ' + (i + 1)); tb(s, why[i][2], { x: 1.35, y: y - 0.02, w: 5.6, h: 0.92 }); }
  card(s, 7.3, 1.95, 5.43, 4.75, 'Stakeholder panel');
  tb(s, 'Who it affects', { x: 7.6, y: 2.15, w: 4.8, h: 0.45, fontSize: 20, bold: true });
  const who = [['FaLandmark', 'Planning and development authorities'], ['FaBuilding', 'Municipal councils'], ['FaScaleBalanced', 'Punjab Government and Agriculture Department'], ['FaTractor', 'Farmers and landowners'], ['FaFaucetDrip', 'Groundwater and environmental agencies'], ['FaHelmetSafety', 'Real-estate and infrastructure developers'], ['FaGraduationCap', 'Researchers']];
  for (let i = 0; i < who.length; i++) { const y = 2.75 + i * 0.56; await iconCircle(s, who[i][0], 7.6, y, 0.4, C.text2, who[i][1]); tb(s, who[i][1], { x: 8.15, y, w: 4.45, h: 0.4, fontSize: 14, valign: 'middle' }); }
  s.addNotes('Say: the belt around Chandigarh is one of Punjab’s fastest-urbanising areas. Back that claim with a source before presenting (for example Census of India town data, a GMADA master plan, or a published study). Main theme: urban growth. Farmland loss is a consequence, not the headline.');

  // ===== 3. SDG link =====
  s = pres.addSlide({ masterName: 'CONTENT', sectionTitle: 'Introduction' });
  s.addText('SDG link', { placeholder: 'title' });
  kicker(s, 'Primary link: SDG 11, Target 11.3. Supporting links: SDG 2 and SDG 15, through the farmland lost to building.');
  card(s, 0.6, 1.95, 6.6, 4.6, 'SDG 11 card');
  s.addShape(pres.shapes.OVAL, { x: 0.95, y: 2.25, w: 1.0, h: 1.0, fill: { color: C.accent1 }, objectName: 'SDG 11 badge' });
  tb(s, '11', { x: 0.95, y: 2.25, w: 1.0, h: 1.0, fontSize: 30, bold: true, color: C.background1, align: 'center', valign: 'middle' });
  tb(s, 'SDG 11: Sustainable cities and communities', { x: 2.2, y: 2.25, w: 4.75, h: 0.75, fontSize: 18, bold: true });
  tb(s, 'Target 11.3', { x: 2.2, y: 2.95, w: 4.75, h: 0.35, fontSize: 16, bold: true, color: C.accent1 });
  tb(s, '“By 2030, enhance inclusive and sustainable urbanization and capacity for participatory, integrated and sustainable human settlement planning and management in all countries”', { x: 0.95, y: 3.5, w: 5.95, h: 1.35, italic: true });
  tb(s, 'Indicator 11.3.1 compares how fast built-up land grows with how fast the population grows', { x: 0.95, y: 4.9, w: 5.95, h: 0.6, fontSize: 14 });
  tb(s, 'Our link: we measure the land side, how fast built-up land grows, using the 11.3.1 formula.', { x: 0.95, y: 5.55, w: 5.95, h: 0.95, bold: true });
  for (const [y, num, col, head, body] of [[1.95, '2', C.accent2, 'SDG 2 · Target 2.4', 'Sustainable food production systems. We report how much cropland became built-up.'], [4.35, '15', C.accent3, 'SDG 15 · Target 15.3', 'Land degradation. Land-cover change is one of the measures behind indicator 15.3.1; we report farmland turned into built-up land.']]) {
    card(s, 7.6, y, 5.13, 2.2, 'SDG ' + num + ' card');
    s.addShape(pres.shapes.OVAL, { x: 7.85, y: y + 0.25, w: 0.8, h: 0.8, fill: { color: col }, objectName: 'SDG ' + num + ' badge' });
    tb(s, num, { x: 7.85, y: y + 0.25, w: 0.8, h: 0.8, fontSize: 24, bold: true, color: C.background1, align: 'center', valign: 'middle' });
    tb(s, head, { x: 8.9, y: y + 0.25, w: 3.6, h: 0.4, fontSize: 17, bold: true });
    tb(s, body, { x: 8.9, y: y + 0.7, w: 3.6, h: 1.4, fontSize: 14 });
  }
  tb(s, 'Target wording: United Nations, sdgs.un.org', { x: 0.6, y: 6.7, w: 12.13, h: 0.25, fontSize: 10, color: C.accent6 });
  s.addNotes('Check the exact wording of Targets 11.3, 2.4 and 15.3 and of indicators 11.3.1 and 15.3.1 on sdgs.un.org before presenting. The official name of 11.3.1 is “ratio of land consumption rate to population growth rate”. We use its formula for the land side only; there is no census population for 2015–2025.');

  // ===== 4. Study area =====
  s = pres.addSlide({ masterName: 'CONTENT', sectionTitle: 'Introduction' });
  s.addText('Study area', { placeholder: 'title' });
  kicker(s, 'S.A.S. Nagar (Mohali) district, Punjab, next to Chandigarh');
  s.addImage({ path: MAP_IMG, x: 0.6, y: 1.85, w: 6.58, h: 4.65, altText: 'Location map of the study area, S.A.S. Nagar (Mohali) district, Punjab, with an inset map of India', objectName: 'Location map' });
  tb(s, 'Basemap © OpenStreetMap contributors. The “Kharar” and “Rajpura” labels come from an outdated boundary dataset (GADM); its outline covers the Mohali, Kharar and Dera Bassi tehsils.', { x: 0.6, y: 6.52, w: 6.58, h: 0.45, fontSize: 10, color: C.accent6 });
  tb(s, `${n0(totalHa)} ha`, { x: 7.6, y: 1.85, w: 5.13, h: 0.85, fontSize: 40, bold: true, color: C.accent1, objectName: 'Area stat' });
  tb(s, 'area inside the study-area boundary (about 1,088 km²)', { x: 7.6, y: 2.7, w: 5.13, h: 0.4, fontSize: 14, color: C.accent6 });
  tb(s, bulletRuns(['Tehsils: Mohali, Kharar and Dera Bassi', 'Zirakpur: a municipal council inside Dera Bassi tehsil', 'Adjoins Chandigarh and borders Panchkula (Haryana)', 'Why this boundary: one district holds all four growing towns, so results can feed district-level planning'], { space: 10 }), { x: 7.6, y: 3.35, w: 5.13, h: 3.2 });
  s.addNotes('Area = 1,209,178 pixels of 30 m inside the GADM boundary, measured in UTM zone 43N. Check it against the official district area, and confirm the tehsil list on an official source. Before submitting, ideally replace the map with a version without the “Kharar”/“Rajpura” labels.');

  // ===== 5. Objectives =====
  s = pres.addSlide({ masterName: 'CONTENT', sectionTitle: 'Introduction' });
  s.addText('Objectives', { placeholder: 'title' });
  kicker(s, 'One question: how much, how fast and where did the belt urbanise?');
  const objectives = [
    ['FaLayerGroup', C.accent2, 'Make a map of what covers the ground for each year by sorting satellite images into groups', 'Three land-cover maps: 2015, 2020, 2025'],
    ['FaRulerCombined', C.accent1, 'Measure how much the built-up area grew between years, in hectares and as a yearly rate', 'Change table: hectares, % and yearly rate'],
    ['FaMapLocationDot', C.accent4, 'Identify where urban growth is concentrated and how much farmland it replaced', 'Zone comparison and a change map'],
    ['FaChartColumn', C.accent5, 'Present the results as charts and an interactive web map', 'Charts and a live web map'],
  ];
  for (let i = 0; i < objectives.length; i++) {
    const x = 0.6 + i * 3.093;
    card(s, x, 1.95, 2.85, 4.6, 'Objective ' + (i + 1));
    await iconCircle(s, objectives[i][0], x + 0.3, 2.3, 0.8, objectives[i][1], 'Objective ' + (i + 1));
    tb(s, '0' + (i + 1), { x: x + 1.35, y: 2.35, w: 1.2, h: 0.7, fontSize: 30, bold: true, valign: 'middle' });
    tb(s, objectives[i][2], { x: x + 0.3, y: 3.4, w: 2.3, h: 1.75, fontSize: 16 });
    tb(s, 'OUTPUT', { x: x + 0.3, y: 5.25, w: 2.3, h: 0.3, fontSize: 11, bold: true, color: C.accent6, charSpacing: 1 });
    tb(s, objectives[i][3], { x: x + 0.3, y: 5.55, w: 2.3, h: 0.85 });
  }
  s.addNotes('The teacher asks for at least three objectives. These four follow the procedure: a land-cover map per year, built-up growth in hectares, where growth is concentrated (plus farmland replaced), and charts plus a web map.');

  // ===== 6. Data =====
  pres.addSection({ title: 'Data and methods' });
  s = pres.addSlide({ masterName: 'CONTENT', sectionTitle: 'Data and methods' });
  s.addText('Data', { placeholder: 'title' });
  kicker(s, 'Free, open data: satellite images for the analysis, other layers for checking and context');
  const data = [
    ['FaSatellite', C.accent1, 'Satellite images', 'Landsat 8, 30 m, two clear March images per year', 'USGS / NASA, via Microsoft Planetary Computer', 'Land-cover maps'],
    ['FaMapLocationDot', C.accent6, 'Study-area boundary', 'S.A.S. Nagar district outline', 'GADM (to be checked against an official map)', 'Clipping and total area'],
    ['FaGlobe', C.accent3, 'Independent land-cover map', 'ESA WorldCover 2020 and 2021, 10 m', 'European Space Agency, via Planetary Computer', 'Accuracy check'],
    ['FaMagnifyingGlass', C.accent4, 'Detailed satellite photos', 'Esri World Imagery at 158 check points', 'Esri', 'Accuracy check'],
    ['FaRoute', C.accent5, 'Base map', 'Roads, places and boundaries', 'OpenStreetMap contributors', 'Location map'],
  ];
  for (let i = 0; i < data.length; i++) {
    const y = 1.85 + i * 0.97;
    const [ic, col, title, detail, source, use] = data[i];
    card(s, 0.6, y, 12.13, 0.88, title + ' row');
    await iconCircle(s, ic, 0.82, y + 0.16, 0.56, col, title);
    tb(s, title, { x: 1.6, y: y + 0.08, w: 4.3, h: 0.38, fontSize: 16, bold: true });
    tb(s, detail, { x: 1.6, y: y + 0.46, w: 4.3, h: 0.38, fontSize: 14 });
    tb(s, 'SOURCE', { x: 6.1, y: y + 0.08, w: 3.3, h: 0.28, fontSize: 11, bold: true, color: C.accent6, charSpacing: 1 });
    tb(s, source, { x: 6.1, y: y + 0.36, w: 3.3, h: 0.5, fontSize: 13 });
    tb(s, 'USED FOR', { x: 9.6, y: y + 0.08, w: 2.9, h: 0.28, fontSize: 11, bold: true, color: C.accent6, charSpacing: 1 });
    tb(s, use, { x: 9.6, y: y + 0.36, w: 2.9, h: 0.5, fontSize: 14 });
  }
  s.addNotes('Scenes used (Landsat 8 Collection 2 Level-2, path 147, row 39): 7 and 23 March 2015; 4 and 20 March 2020; 2 and 18 March 2025. Satellite and years are still to be confirmed with the teacher. Record the GADM version you downloaded.');

  // ===== 7. Data preparation =====
  s = pres.addSlide({ masterName: 'CONTENT', sectionTitle: 'Data and methods' });
  s.addText('Data preparation', { placeholder: 'title' });
  kicker(s, 'One clean, comparable picture per year');
  const prep = [
    ['FaCloud', C.accent4, '1. Remove clouds', 'Hide cloudy, shadowy and hazy pixels using the image’s built-in quality flags'],
    ['FaClone', C.accent6, '2. Merge photos', 'Middle value of two clear March photos per year'],
    ['FaCalendarDays', C.accent2, '3. Keep it fair', 'Same month (March) and same satellite (Landsat 8) every year'],
    ['FaCompass', C.accent5, '4. Same grid', 'One standard map grid (UTM zone 43N), same 30 m pixels every year'],
    ['FaCrosshairs', C.accent1, '5. Cut out the area', 'Keep only the study area: 1,209,178 pixels'],
  ];
  for (let i = 0; i < prep.length; i++) {
    const x = 0.6 + i * 2.48;
    await iconCircle(s, prep[i][0], x, 2.0, 0.9, prep[i][1], prep[i][2]);
    if (i < prep.length - 1) arrow(s, x + 1.05, 2.45, 1.28, 0);
    tb(s, prep[i][2], { x, y: 3.1, w: 2.25, h: 0.45, fontSize: 17, bold: true });
    tb(s, prep[i][3], { x, y: 3.6, w: 2.2, h: 1.5, fontSize: 14 });
  }
  card(s, 0.6, 5.45, 12.13, 1.15, 'Why March');
  tb(s, [{ text: 'Why March? ', options: { bold: true } }, { text: 'Wheat is green then, so farmland and buildings look very different. Using the same month every year removes crop-season effects.' }], { x: 0.9, y: 5.55, w: 11.5, h: 0.95, fontSize: 16, valign: 'middle' });
  s.addNotes('Steps 1–5 were run in Python (pystac, rasterio). Cloud removal: pixels flagged as fill, dilated cloud, cirrus, cloud or cloud shadow in the QA_PIXEL band were removed. The Earth Engine script in the kit does steps 1–4 for anyone repeating the work, and QGIS can do step 5.');

  // ===== 8. Methodology =====
  s = pres.addSlide({ masterName: 'CONTENT', sectionTitle: 'Data and methods' });
  s.addText('Methodology', { placeholder: 'title' });
  kicker(s, 'From satellite photos to growth figures, checked for accuracy');
  const xs = [0.6, 3.12, 5.64, 8.16, 10.68];
  const row1 = [['Landsat 8 March photos: 2015, 2020, 2025', C.accent6], ['Clean picture per year (clouds removed)', C.text2], ['Cut out the study area', C.text2], ['K-means: computer sorts pixels into 10 groups', C.text2], ['Name the groups by location and colour', C.text2]];
  const row2 = [['Merge into 4 land types', C.text2], ['Land-cover maps 2015, 2020, 2025', C.text2], ['Area per land type (hectares)', C.text2], ['Change: new built-up, cropland → built-up', C.text2], ['Charts · report · web map', C.accent1]];
  const box = (x, y, text, fill, name) => { s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y, w: 2.05, h: 1.2, fill: { color: fill }, rectRadius: 0.08, objectName: name }); tb(s, text, { x: x + 0.12, y, w: 1.81, h: 1.2, fontSize: 14, bold: true, color: C.background1, align: 'center', valign: 'middle' }); };
  row1.forEach(([t, f], i) => { box(xs[i], 1.95, t, f, 'Step ' + (i + 1)); if (i < 4) arrow(s, xs[i] + 2.08, 2.55, 0.41, 0); });
  arrow(s, 11.705, 3.18, 0, 0.5);
  row2.forEach(([t, f], i) => { box(xs[4 - i], 3.7, t, f, 'Step ' + (i + 6)); if (i < 4) arrow(s, xs[3 - i] + 2.08, 4.3, 0.41, 0, { reverse: true }); });
  arrow(s, 9.185, 4.93, 0, 0.42, { dashed: true, colour: C.accent5, width: 1.5 });
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: 5.64, y: 5.35, w: 4.57, h: 0.95, fill: { color: C.background1 }, line: { color: C.accent5, width: 1.5, dashType: 'dash' }, rectRadius: 0.08, objectName: 'Validation box' });
  tb(s, [{ text: 'Accuracy check: ', options: { bold: true } }, { text: '158 points checked on detailed photos, plus ESA WorldCover' }], { x: 5.84, y: 5.35, w: 4.17, h: 0.95, fontSize: 14, valign: 'middle' });
  [['Data', C.accent6, 0.6, 0.8], ['Processing', C.text2, 1.55, 1.2], ['Output', C.accent1, 2.9, 1.0]].forEach(([t, f, x, w]) => {
    s.addShape(pres.shapes.RECTANGLE, { x, y: 5.69, w: 0.2, h: 0.2, fill: { color: f }, objectName: 'Legend ' + t });
    tb(s, t, { x: x + 0.28, y: 5.62, w: w - 0.3, h: 0.34, fontSize: 12, color: C.accent6, valign: 'middle' });
  });
  s.addNotes('Walk through the top row left to right, then the bottom row right to left. The next four slides explain each step in plain words.');

  // ===== 9–12. In plain words =====
  pres.addSection({ title: 'In plain words' });
  // 9. What the satellite sees
  s = pres.addSlide({ masterName: 'CONTENT', sectionTitle: 'In plain words' });
  s.addText('In plain words: what the satellite sees', { placeholder: 'title' });
  kicker(s, 'Landsat 8 photographs the ground in six kinds of light; we merge two March photos into one clean picture per year.');
  tb(s, bulletRuns(['Landsat 8 is a free NASA and US Geological Survey satellite.', 'Each picture is made of squares called pixels: 30 m × 30 m, about a 100 ft plot.', 'Each pixel is measured in six kinds of light (bands), two of which our eyes cannot see.', 'Two clear March photos per year are merged, keeping the middle value, into one cloud-free picture.'], { space: 12 }), { x: 0.6, y: 1.95, w: 5.7, h: 3.6, fontSize: 17 });
  const bands = [['Blue', C.accent4], ['Green', C.accent2], ['Red', C.accent1], ['Near-infrared', C.accent6], ['Shortwave infrared 1', C.accent5], ['Shortwave infrared 2', C.text2]];
  tb(s, 'Six readings for every pixel', { x: 6.9, y: 1.95, w: 3.0, h: 0.35, fontSize: 14, bold: true });
  bands.forEach(([b, col], i) => { s.addShape(pres.shapes.RECTANGLE, { x: 6.9, y: 2.4 + i * 0.42, w: 0.9, h: 0.3, fill: { color: col }, objectName: 'Band ' + b }); tb(s, b, { x: 7.9, y: 2.4 + i * 0.42, w: 2.1, h: 0.3, fontSize: 13, valign: 'middle' }); });
  tb(s, 'One pixel = 30 m × 30 m', { x: 10.25, y: 1.95, w: 2.48, h: 0.35, fontSize: 14, bold: true });
  for (let r = 0; r < 5; r++) for (let c = 0; c < 5; c++) s.addShape(pres.shapes.RECTANGLE, { x: 10.35 + c * 0.44, y: 2.4 + r * 0.44, w: 0.4, h: 0.4, fill: { color: r === 2 && c === 2 ? C.accent1 : C.background2 }, line: { color: 'D5DCD8', width: 0.5 }, objectName: `Pixel demo ${r}${c}` });
  tb(s, '1,209,178 pixels cover the study area', { x: 10.25, y: 4.65, w: 2.48, h: 0.6, fontSize: 13, color: C.accent6 });
  await analogyCard(s, 'like a mosaic floor: each tile is one pixel, and every tile is photographed through six coloured filters.');
  s.addNotes('Landsat 8 is a free NASA and US Geological Survey satellite. Its pictures are made of small squares called pixels, each 30 metres wide. For every pixel it records six kinds of light, called bands. Healthy plants reflect near-infrared light strongly, which is why green wheat stands out from concrete. We took two clear March photos for each of 2015, 2020 and 2025 and merged them into one cloud-free picture per year, called a composite.');

  // 10. How the computer sorted the land
  s = pres.addSlide({ masterName: 'CONTENT', sectionTitle: 'In plain words' });
  s.addText('In plain words: how the computer sorted the land', { placeholder: 'title' });
  kicker(s, 'K-means sorts pixels into groups that look alike, without being told what any group means.');
  tb(s, bulletRuns(['K-means groups pixels by how similar their six light readings are.', `Training: it studied all ${(F.training.training_pixels / 1e6).toFixed(1)} million pixels from the three years and found 10 typical groups.`, 'It moves each group’s centre again and again until nothing changes: then it is trained.', 'One trained model was used for every year, so a group means the same thing in 2015 and 2025.'], { space: 12 }), { x: 0.6, y: 1.95, w: 5.7, h: 3.6, fontSize: 17 });
  card(s, 6.9, 1.95, 1.75, 2.9, 'Step 1 panel');
  const dots = [[0.2, 0.3], [0.9, 0.2], [1.3, 0.6], [0.5, 0.8], [1.1, 1.1], [0.3, 1.4], [0.8, 1.6], [1.35, 1.75], [0.25, 2.0], [0.95, 2.2]];
  dots.forEach(([dx, dy], i) => s.addShape(pres.shapes.OVAL, { x: 7.0 + dx, y: 2.05 + dy, w: 0.16, h: 0.16, fill: { color: C.accent6 }, objectName: 'Sample dot ' + i }));
  tb(s, '3.6 million pixels', { x: 6.9, y: 4.95, w: 1.75, h: 0.5, fontSize: 13, bold: true, align: 'center' });
  arrow(s, 8.72, 3.4, 0.45, 0);
  card(s, 9.25, 1.95, 1.75, 2.9, 'Step 2 panel');
  const pal = [C.accent1, C.accent2, C.accent3, C.accent4, C.accent5, C.accent6, C.text2, C.accent1, C.accent2, C.accent3];
  for (let i = 0; i < 10; i++) s.addShape(pres.shapes.OVAL, { x: 9.42 + (i % 3) * 0.48, y: 2.12 + Math.floor(i / 3) * 0.48, w: 0.38, h: 0.38, fill: { color: pal[i] }, objectName: 'Group centre ' + (i + 1) });
  await iconCircle(s, 'FaArrowsRotate', 9.83, 4.15, 0.55, C.accent5, 'Repeat until stable');
  tb(s, '10 groups, adjusted until stable', { x: 9.15, y: 4.95, w: 1.95, h: 0.5, fontSize: 13, bold: true, align: 'center' });
  arrow(s, 11.07, 3.4, 0.4, 0);
  ['2015', '2020', '2025'].forEach((y, i) => { s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: 11.55, y: 2.05 + i * 0.95, w: 1.15, h: 0.75, fill: { color: C.text2 }, rectRadius: 0.06, objectName: 'Year ' + y }); tb(s, y, { x: 11.55, y: 2.05 + i * 0.95, w: 1.15, h: 0.75, fontSize: 15, bold: true, color: C.background1, align: 'center', valign: 'middle' }); });
  tb(s, 'Same model, every year', { x: 11.4, y: 4.95, w: 1.33, h: 0.6, fontSize: 13, bold: true, align: 'center' });
  await analogyCard(s, 'like sorting a mixed sack of pulses into 10 heaps by look, shuffling grains between heaps until none needs to move.');
  s.addNotes('K-means is a way of sorting without an answer key. We gave the computer every pixel from all three years, about 3.6 million. It started with 10 group centres, put each pixel in the nearest group, moved the centres to the middle of their groups, and repeated until nothing changed. That is what “training” means. We then used this one trained model on all three years, so a group means the same thing in 2015, 2020 and 2025, and the years can be compared fairly.');

  // 11. From groups to land types
  s = pres.addSlide({ masterName: 'CONTENT', sectionTitle: 'In plain words' });
  s.addText('In plain words: from groups to land types', { placeholder: 'title' });
  kicker(s, 'The computer only numbers the groups; we named each one from where it falls and how it looks.');
  tb(s, bulletRuns(['Clues: towns and roads, the forested hills in the north, fields, and true-colour pictures.', 'The ten groups were merged into four land types.', `Built-up is group ${groupsOf('Built-up').join(', ')}, which sits on the towns and main roads.`, 'No water class: ponds and streams are too small to fill a 30 m pixel.'], { space: 12 }), { x: 0.6, y: 1.95, w: 5.7, h: 3.6, fontSize: 17 });
  const types = [['Built-up', 1], ['Cropland', 2], ['Trees/vegetation', 3], ['Bare/fallow', 5]];
  types.forEach(([name, code], i) => {
    const y = 1.95 + i * 0.86;
    card(s, 6.9, y, 5.83, 0.74, name + ' row');
    s.addShape(pres.shapes.RECTANGLE, { x: 7.05, y: y + 0.17, w: 0.4, h: 0.4, fill: { color: CLASS_COLOURS[code] }, objectName: name + ' colour' });
    tb(s, name, { x: 7.6, y, w: 2.2, h: 0.74, fontSize: 16, bold: true, valign: 'middle' });
    const g = groupsOf(name);
    g.forEach((k, j) => { s.addShape(pres.shapes.OVAL, { x: 9.7 + j * 0.46, y: y + 0.16, w: 0.42, h: 0.42, fill: { color: C.background1 }, line: { color: C.accent6, width: 1 }, objectName: `Group ${k}` }); tb(s, String(k), { x: 9.7 + j * 0.46, y: y + 0.16, w: 0.42, h: 0.42, fontSize: 12, bold: true, align: 'center', valign: 'middle' }); });
  });
  tb(s, 'Groups numbered 1–10; water formed no group of its own.', { x: 6.9, y: 5.4, w: 5.83, h: 0.3, fontSize: 12, color: C.accent6 });
  await analogyCard(s, 'like ten unnamed student groups: you learn who they are from where they sit, then place them into four school houses.');
  s.addNotes('The computer only says group one, group two and so on, so we gave them meaning. We looked at where each group appears: towns and roads, the forested hills in the north, the fields. We also looked at true-colour pictures, which look like ordinary photographs. Then we merged the ten groups into four land types. Water did not form its own group, because ponds and streams are too small to fill a 30 metre pixel.');

  // 12. How growth was measured
  s = pres.addSlide({ masterName: 'CONTENT', sectionTitle: 'In plain words' });
  s.addText('In plain words: how growth was measured', { placeholder: 'title' });
  kicker(s, 'We count pixels, turn them into hectares, and compare years as a total, a percentage and a yearly rate.');
  tb(s, bulletRuns(['Count built-up pixels and multiply by 0.09 ha (one pixel = 900 m²).', `Built-up: ${n0(BU[2015])} ha (2015) → ${n0(BU[2025])} ha (2025): +${n0(C1525.increase_ha)} ha, or +${Math.round(C1525.pct_change)}%.`, `The yearly rate works like compound interest: ${p1(C1525.lcr_pct_per_year)}% a year overall, ${p1(C2025.lcr_pct_per_year)}% after 2020.`, 'UEII compares zones of different size: new built-up land per year as a % of the zone’s area.'], { space: 12 }), { x: 0.6, y: 1.95, w: 5.7, h: 3.6, fontSize: 17 });
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: 6.9, y: 1.95, w: 5.83, h: 0.6, fill: { color: C.text2 }, rectRadius: 0.06, objectName: 'Formula' });
  tb(s, 'built-up pixels × 0.09 = hectares', { x: 6.9, y: 1.95, w: 5.83, h: 0.6, fontSize: 17, bold: true, color: C.background1, align: 'center', valign: 'middle' });
  s.addChart(pres.charts.BAR, [{ name: 'Built-up area (ha)', labels: ['2015', '2020', '2025'], values: [Math.round(BU[2015]), Math.round(BU[2020]), Math.round(BU[2025])] }], {
    x: 6.9, y: 2.7, w: 5.83, h: 2.85, barDir: 'col', chartColors: ['B03A2E'], barGapWidthPct: 70, showTitle: true, title: 'Built-up area (ha)', titleFontSize: 13, titleColor: '1F2A2E', titleFontFace: '+mn-lt',
    showValue: true, dataLabelPosition: 'outEnd', dataLabelFormatCode: '#,##0', dataLabelFontSize: 12, dataLabelColor: '1F2A2E', dataLabelFontFace: '+mn-lt',
    catAxisLabelColor: '5F6F73', catAxisLabelFontSize: 12, catAxisLabelFontFace: '+mn-lt', valAxisHidden: true, valGridLine: { style: 'none' }, catGridLine: { style: 'none' }, showLegend: false, objectName: 'Built-up chart (plain words)' });
  await analogyCard(s, 'marks out of 50 and out of 100 can’t be compared until both become percentages; UEII does the same for zones of different size.');
  s.addNotes('Counting is simple: each pixel is 900 square metres, or 0.09 hectare, so we count built-up pixels and multiply. The yearly rate is like compound interest on a bank deposit: each year’s growth builds on a bigger base. It uses the official SDG 11.3.1 formula, ln(later ÷ earlier) ÷ years. UEII, the Urban Expansion Intensity Index, turns new built-up land into a percentage of each zone’s area per year, so a big zone and a small zone can be compared fairly.');

  // ===== 13. GIS and RS analysis =====
  pres.addSection({ title: 'Analysis' });
  s = pres.addSlide({ masterName: 'CONTENT', sectionTitle: 'Analysis' });
  s.addText('GIS and remote sensing analysis', { placeholder: 'title' });
  kicker(s, 'What was done and with which tool, with identical settings for all three years');
  const head = ['Step', 'What was done', 'Tool used', 'Result'].map((t) => ({ text: t, options: { bold: true, color: C.background1, fill: { color: C.text2 } } }));
  const rowsData = [
    ['Images', 'Middle value of two clear March scenes per year, clouds removed', 'Python: pystac, rasterio', 'One composite per year'],
    ['Clip', 'Cut to the study area on a standard map grid (UTM 43N)', 'Python: rasterio', '1,209,178 pixels of 30 m'],
    ['Cluster', 'K-means, 10 groups, trained on all 3.6 million pixels (best of 10 starts)', 'Python: scikit-learn', 'Group map per year'],
    ['Name', 'Groups named from their location and true colour', 'Visual check', 'Naming table'],
    ['Reclassify', '10 groups merged into 4 land types', 'Python: numpy', 'Land-cover map per year'],
    ['Measure', 'Pixel count × 0.09 ha (1 pixel = 900 m²)', 'Python: numpy', 'Hectares per land type'],
    ['Change', 'From–to comparison 2015 → 2025, and growth by zone (UEII)', 'Python: numpy, rasterio', 'Change map, zone table'],
    ['Check', '158 photo-checked points; ESA WorldCover comparison', 'Python + photo checks', 'Accuracy figures'],
  ];
  s.addTable([head].concat(rowsData.map((r, i) => r.map((t, j) => ({ text: t, options: { bold: j === 0, fill: { color: i % 2 ? C.background2 : C.background1 } } })))), { x: 0.6, y: 1.85, w: 12.13, colW: [1.5, 5.4, 2.8, 2.43], rowH: 0.5, fontSize: 14, color: C.text1, valign: 'middle', margin: [0.04, 0.1, 0.04, 0.1], border: { type: 'solid', pt: 0.75, color: 'D5DCD8' }, autoPage: false });
  s.addNotes('Because of the deadline, the analysis was run in Python. The teacher asked for QGIS, so say which tool was used; the same steps can be repeated in QGIS with the composites in results/images and the guide 04_qgis_steps.md. Final K-means settings: 10 clusters, 10 starts, up to 300 iterations, trained on all 3,626,753 pixels from the three years.');

  // ===== 14. Risks, suitability and assumptions =====
  s = pres.addSlide({ masterName: 'CONTENT', sectionTitle: 'Analysis' });
  s.addText('Risks, suitability and assumptions', { placeholder: 'title' });
  kicker(s, 'What the method relies on, why it fits, and what could go wrong');
  const rsa = [
    ['FaListCheck', C.accent6, 'Assumptions', ['March images are comparable from year to year', 'Landsat 8 measures the same way each year', '30 m pixels are fine enough for town-scale growth', 'Built-up land rarely turns back into farmland']],
    ['FaCircleCheck', C.accent3, 'Suitability', ['Free, consistent Landsat archive', 'Same trained model for every year', 'Trained on every pixel, not a sample', 'Same satellite-based approach as SDG 11.3.1']],
    ['FaTriangleExclamation', C.accent1, 'Risks', ['Bare fields confused with built-up', 'Mixed pixels: fields and houses in one pixel', 'Small villages and roads missed', 'Naming groups by eye is subjective', 'GADM boundary may be out of date']],
  ];
  for (let i = 0; i < rsa.length; i++) {
    const x = 0.6 + i * 4.125;
    card(s, x, 1.95, 3.88, 4.75, rsa[i][2] + ' card');
    await iconCircle(s, rsa[i][0], x + 0.3, 2.2, 0.6, rsa[i][1], rsa[i][2]);
    tb(s, rsa[i][2], { x: x + 1.05, y: 2.25, w: 2.6, h: 0.5, fontSize: 20, bold: true, valign: 'middle' });
    tb(s, bulletRuns(rsa[i][3]), { x: x + 0.3, y: 3.05, w: 3.3, h: 3.5 });
  }
  s.addNotes('Suitability: Landsat 8 has a free archive from 2013, so 2015–2025 can use one satellite. The risks are measured on the accuracy slide and listed under limitations.');

  // ===== 15. Results: how much =====
  pres.addSection({ title: 'Results' });
  s = pres.addSlide({ masterName: 'CONTENT', sectionTitle: 'Results' });
  s.addText('Results: how much and how fast', { placeholder: 'title' });
  kicker(s, 'Built-up land nearly doubled between 2015 and 2025, and growth sped up after 2020');
  [[`${n0(BU[2015])} ha`, `Built-up 2015 (${p1(SH[2015])}% of the area)`], [`${n0(BU[2025])} ha`, `Built-up 2025 (${p1(SH[2025])}% of the area)`], [`+${n0(C1525.increase_ha)} ha`, `Increase 2015–2025 (+${Math.round(C1525.pct_change)}%)`], [`${p1(C1525.lcr_pct_per_year)}% a year`, 'Yearly growth rate (compound, like interest)']]
    .forEach(([v, l], i) => statCard(s, 0.6 + i * 3.077, 1.9, 2.9, 1.45, v, l, 'Stat ' + (i + 1)));
  classLegend(s, 0.6, 3.5, C.text1, [1.15, 1.2, 1.75, 1.3], CLASS_NAMES.filter((c) => c[0] !== 4));
  tb(s, 'No water class: water bodies are too small to form their own group at 30 m', { x: 6.3, y: 3.5, w: 6.43, h: 0.34, fontSize: 12, color: C.accent6, valign: 'middle' });
  [2015, 2020, 2025].forEach((yr, i) => { const h = 2.85, w = h * (4.2 / 6.2); s.addImage({ path: path.join(RES, `map_lulc_${yr}.png`), x: 0.6 + i * 3.077 + (2.9 - w) / 2, y: 3.9, w, h, altText: `Land-cover map of the study area, ${yr}`, objectName: `LULC map ${yr}` }); });
  s.addChart(pres.charts.BAR, [{ name: 'Built-up area (ha)', labels: ['2015', '2020', '2025'], values: [Math.round(BU[2015]), Math.round(BU[2020]), Math.round(BU[2025])] }], {
    x: 9.83, y: 3.9, w: 2.9, h: 2.85, barDir: 'col', chartColors: ['B03A2E'], barGapWidthPct: 60, showTitle: true, title: 'Built-up area (ha)', titleFontSize: 13, titleColor: '1F2A2E', titleFontFace: '+mn-lt',
    showValue: true, dataLabelPosition: 'outEnd', dataLabelFormatCode: '#,##0', dataLabelFontSize: 11, dataLabelColor: '1F2A2E', dataLabelFontFace: '+mn-lt',
    catAxisLabelColor: '5F6F73', catAxisLabelFontSize: 11, catAxisLabelFontFace: '+mn-lt', valAxisHidden: true, valGridLine: { style: 'none' }, catGridLine: { style: 'none' }, showLegend: false, objectName: 'Built-up chart' });
  s.addNotes(`Built-up area: ${n0(BU[2015])} ha (2015), ${n0(BU[2020])} ha (2020), ${n0(BU[2025])} ha (2025). Growth: +${n0(C1520.increase_ha)} ha in 2015–2020 (${p1(C1520.lcr_pct_per_year)}% a year) and +${n0(C2025.increase_ha)} ha in 2020–2025 (${p1(C2025.lcr_pct_per_year)}% a year), using the SDG 11.3.1 formula ln(later ÷ earlier) ÷ years. The accuracy check shows the map undercounts built-up land (corrected 2025 estimate ${n0(ADJ.error_adjusted_ha)} ± ${n0(ADJ.ci95_ha)} ha), so present these as conservative estimates.`);

  // ===== 16. Results: where =====
  s = pres.addSlide({ masterName: 'CONTENT', sectionTitle: 'Results' });
  s.addText('Results: where growth happened', { placeholder: 'title' });
  kicker(s, `The West (Kharar–Mohali) grew fastest; ${Math.round(F.crop_share)}% of the new built-up land was cropland in 2015`);
  { const h = 4.85, w = h * (4.6 / 6.6); s.addImage({ path: path.join(RES, 'map_change_2015_2025.png'), x: 0.6 + (6.3 - w) / 2, y: 1.85, w, h, altText: 'Map of built-up change 2015–2025 with West and East zones', objectName: 'Change map' }); }
  const zh = ['Zone', 'Built-up 2015 (ha)', 'Built-up 2025 (ha)', 'UEII'].map((t) => ({ text: t, options: { bold: true, color: C.background1, fill: { color: C.text2 } } }));
  const zr = [['West (Kharar and Mohali)', n0(ZW.builtup_2015_ha), n0(ZW.builtup_2025_ha), ZW.ueii_2015_2025.toFixed(2)], ['East (Dera Bassi, incl. Zirakpur)', n0(ZE.builtup_2015_ha), n0(ZE.builtup_2025_ha), ZE.ueii_2015_2025.toFixed(2)], ['Whole study area', n0(BU[2015]), n0(BU[2025]), UEII_ALL.toFixed(2)]]
    .map((r, i) => r.map((t, j) => ({ text: t, options: { bold: j === 0, align: j === 0 ? 'left' : 'center', fill: { color: i % 2 ? C.background2 : C.background1 } } })));
  s.addTable([zh].concat(zr), { x: 7.2, y: 1.9, w: 5.53, colW: [2.33, 1.1, 1.1, 1.0], rowH: 0.55, fontSize: 14, color: C.text1, valign: 'middle', margin: [0.04, 0.08, 0.04, 0.08], border: { type: 'solid', pt: 0.75, color: 'D5DCD8' }, autoPage: false });
  card(s, 7.2, 4.45, 5.53, 1.3, 'Cropland stat');
  tb(s, `${n0(F.crop_to_bu)} ha`, { x: 7.45, y: 4.55, w: 2.1, h: 1.1, fontSize: 28, bold: true, color: C.accent1, valign: 'middle' });
  tb(s, `of cropland became built-up: ${Math.round(F.crop_share)}% of all new built-up land, 2015–2025`, { x: 9.6, y: 4.55, w: 2.95, h: 1.1, fontSize: 14, valign: 'middle' });
  tb(s, 'UEII = new built-up land each year as a % of the zone’s area. West scores “medium” (0.59–1.05); East scores “low” (0.28–0.59).', { x: 7.2, y: 5.95, w: 5.53, h: 0.75, fontSize: 14, italic: true, color: C.accent6 });
  s.addNotes(`Zones: West ${n0(ZW.zone_ha)} ha (built-up ${p1(ZW.share_2015_pct)}% → ${p1(ZW.share_2025_pct)}%, UEII ${ZW.ueii_2015_2025.toFixed(2)}, yearly rate ${p1(ZW.lcr_2015_2025)}%); East ${n0(ZE.zone_ha)} ha (${p1(ZE.share_2015_pct)}% → ${p1(ZE.share_2025_pct)}%, UEII ${ZE.ueii_2015_2025.toFixed(2)}, yearly rate ${p1(ZE.lcr_2015_2025)}%). The zones are the two pieces of the GADM boundary, not official tehsils. Cropland → built-up: ${n0(F.crop_to_bu)} of the ${n0(F.new_bu)} ha that became built-up. Also say that ${n0(F.lost_bu)} ha mapped as built-up in 2015 were not built-up in 2025, a sign of classification noise.`);

  // ===== 17. How we checked the model (plain words) =====
  pres.addSection({ title: 'Checking the model' });
  s = pres.addSlide({ masterName: 'CONTENT', sectionTitle: 'Checking the model' });
  s.addText('In plain words: how we checked the model', { placeholder: 'title' });
  kicker(s, 'Three tests: is it set up sensibly, does it give the same answer twice, and does it match reality?');
  const checks = [
    ['FaListOl', C.accent6, 'Is 10 groups sensible?', 'Yes', 'The “elbow” test puts the best range at 7–10 groups, and 10 groups merge neatly into 4 land types.'],
    ['FaRepeat', C.accent3, 'Same answer when retrained?', 'Yes', `Trained on all ${(F.training.training_pixels / 1e6).toFixed(1)} million pixels. Three separate runs agree within 1%: built-up 2025 = ${rng('2025')} ha.`],
    ['FaEye', C.accent1, 'Does it match reality?', 'Mostly', `${Math.round(ACC.overall_accuracy_pct)}% of ${F.acc_points} photo-checked points are right (${Math.round(ACC.builtup_binary.overall_agreement_pct)}% for built-up vs not). It misses about half of small built-up spots, so it undercounts.`],
  ];
  for (let i = 0; i < checks.length; i++) {
    const x = 0.6 + i * 4.125;
    card(s, x, 1.95, 3.88, 3.6, checks[i][2]);
    await iconCircle(s, checks[i][0], x + 0.3, 2.2, 0.6, checks[i][1], checks[i][2]);
    tb(s, checks[i][2], { x: x + 1.05, y: 2.2, w: 2.65, h: 0.65, fontSize: 17, bold: true, valign: 'middle' });
    tb(s, checks[i][3], { x: x + 0.3, y: 3.0, w: 3.3, h: 0.6, fontSize: 28, bold: true, color: checks[i][1] });
    tb(s, checks[i][4], { x: x + 0.3, y: 3.65, w: 3.3, h: 1.8, fontSize: 15 });
  }
  await analogyCard(s, 'like checking an exam: is the marking scheme sensible, does a second examiner give the same marks, and do they match the model answer?');
  s.addNotes('The computer had no answer key, so we tested it three ways. First, is ten groups a sensible number? Second, if we train it again, do we get the same answer? Third, does the map agree with reality? For the third test we checked 158 random points on detailed satellite photos and compared the map with an independent map from the European Space Agency. The details are on the next two slides.');

  // ===== 18. Model checks (technical) =====
  s = pres.addSlide({ masterName: 'CONTENT', sectionTitle: 'Checking the model' });
  s.addText('Model checks: suitable and properly trained?', { placeholder: 'title' });
  kicker(s, 'Trained on all the data, gives the same answer when retrained, and uses a sensible number of groups');
  const K = F.kcheck;
  s.addChart(pres.charts.LINE, [{ name: 'Inertia', labels: K.k.map(String), values: K.inertia.map((v) => Math.round(v)) }], Object.assign(lineChartOpts('Elbow check: spread inside groups (lower = tighter)'), { x: 0.6, y: 1.85, w: 5.95, h: 2.75, valAxisLabelFormatCode: '#,##0', objectName: 'Elbow chart' }));
  s.addChart(pres.charts.LINE, [{ name: 'Silhouette', labels: K.k.map(String), values: K.silhouette.map((v) => Math.round(v * 1000) / 1000) }], Object.assign(lineChartOpts('Separation check: silhouette (higher = clearer groups)'), { x: 6.78, y: 1.85, w: 5.95, h: 2.75, valAxisLabelFormatCode: '0.00', objectName: 'Silhouette chart' }));
  statCard(s, 0.6, 4.8, 3.9, 1.85, (F.training.training_pixels).toLocaleString('en-US'), 'pixels used to train the final model: every pixel, all three years', 'Training stat', { valueSize: 26 });
  statCard(s, 4.715, 4.8, 3.9, 1.85, `${inertDiffPct < 0.01 ? '< 0.01' : inertDiffPct.toFixed(2)}%`, 'difference in fit between 3 independent training runs (each the best of 10 starts)', 'Repeatability stat', { valueSize: 26 });
  statCard(s, 8.83, 4.8, 3.9, 1.85, `${rng('2025')} ha`, `built-up 2025 across the 3 runs (2015: ${rng('2015')} ha)`, 'Stability stat', { valueSize: 26 });
  s.addNotes(`Number of groups: the elbow of the curve is at k = ${K.elbow_k}, and k = 7–10 all score within about 10% of the best elbow value, so 10 is inside the sensible range. The silhouette score is highest at k = 4 but nearly flat (0.29–0.33) from 5 to 16 groups. Using more groups than final land types is normal for unsupervised classification, because groups are merged afterwards. Training: an earlier version trained on a 300,000-pixel sample gave different answers when retrained (2015 built-up ${n0(SR['2015'].min)}–${n0(SR['2015'].max)} ha), so the final model was trained on all ${F.training.training_pixels.toLocaleString('en-US')} pixels; three independent runs converged in ${Object.values(F.training.runs).map((r) => r.n_iter).join(', ')} iterations and agree closely.`);

  // ===== 19. Accuracy check (technical) =====
  s = pres.addSlide({ masterName: 'CONTENT', sectionTitle: 'Checking the model' });
  s.addText('Accuracy check: is the map right?', { placeholder: 'title' });
  kicker(s, `${F.acc_points} random points checked on detailed satellite photos, plus a comparison with ESA WorldCover`);
  s.addImage({ path: path.join(RES, 'validation_examples.png'), x: 0.6, y: 1.85, w: 4.95, h: 4.95 * (800 / 930), altText: 'Six example check points: detailed satellite photos with the photo label and the map label', objectName: 'Validation examples' });
  tb(s, 'Six of the check points: the yellow square is one 30 m pixel. Imagery: Esri World Imagery.', { x: 0.6, y: 1.85 + 4.95 * (800 / 930) + 0.06, w: 4.95, h: 0.45, fontSize: 11, color: C.accent6 });
  [[`${Math.round(ACC.overall_accuracy_pct)}%`, 'of points correct across the 4 land types'], [`${Math.round(ACC.builtup_binary.overall_agreement_pct)}%`, 'correct for built-up vs not built-up'], [`${Math.round(ACC['Built-up'].users_accuracy_pct)}%`, 'of points mapped built-up really are built-up'], [`${Math.round(ACC['Built-up'].producers_accuracy_pct)}%`, 'of real built-up land is found by the map']]
    .forEach(([v, l], i) => statCard(s, 5.85 + (i % 2) * 3.47, 1.85 + Math.floor(i / 2) * 1.6, 3.33, 1.45, v, l, 'Accuracy stat ' + (i + 1)));
  card(s, 5.85, 5.1, 6.88, 1.6, 'Accuracy notes');
  tb(s, bulletRuns([`Corrected built-up area 2025: ${n0(Math.round(ADJ.error_adjusted_ha / 100) * 100)} ± ${n0(Math.round(ADJ.ci95_ha / 100) * 100)} ha (map: ${n0(ADJ.map_ha)} ha), so the map undercounts.`, `ESA WorldCover 2020: ${Math.round(WC.agreement_pct)}% agreement on built-up vs not; it finds ${n0(WC.wc_builtup_ha)} ha built-up in 2020 (ours: ${n0(BU[2020])} ha).`], { space: 6 }), { x: 6.05, y: 5.2, w: 6.5, h: 1.4, fontSize: 14 });
  s.addNotes(`Design: stratified random sample of 160 points from the 2025 map (50 built-up, 50 cropland, 30 trees, 30 bare), 2 dropped for cloud, so ${F.acc_points} used. Each point was labelled from Esri World Imagery by two independent AI-assisted interpreters who could not see the map; they agreed on ${RAT.agree} of ${RAT.n} points (${Math.round(100 * RAT.bin_agree / RAT.n)}% for built-up vs not), and the ${RAT.n - RAT.agree} disagreements were settled by a third look. The students should spot-check these labels. Accuracies are area-weighted (Olofsson et al., 2014). Cropland: user’s ${Math.round(ACC.Cropland.users_accuracy_pct)}%, producer’s ${Math.round(ACC.Cropland.producers_accuracy_pct)}%; trees: ${Math.round(ACC['Trees/vegetation'].users_accuracy_pct)}% and ${Math.round(ACC['Trees/vegetation'].producers_accuracy_pct)}%; bare/fallow is weakest. Compared with WorldCover, ${Math.round(WC.mean_wc_builtup_fraction_in_our_builtup)}% of each of our built-up pixels is built-up in WorldCover on average, against ${Math.round(WC.mean_wc_builtup_fraction_elsewhere)}% for all other pixels.`);

  // ===== 20. Web map =====
  pres.addSection({ title: 'Outlook' });
  s = pres.addSlide({ masterName: 'CONTENT', sectionTitle: 'Outlook' });
  s.addText('Web map: what the dashboard shows', { placeholder: 'title' });
  kicker(s, 'The end product: an interactive map anyone can open in a browser');
  s.addImage({ path: WEB_IMG, x: 0.6, y: 1.95, w: 6.9, h: 4.31, altText: 'Screenshot of the web dashboard in compare mode: 2015 left of a drag handle and 2025 right of it, with the key findings, filters and live figures', objectName: 'Dashboard screenshot' });
  s.addShape(pres.shapes.RECTANGLE, { x: 0.6, y: 1.95, w: 6.9, h: 4.31, fill: { color: C.background1, transparency: 100 }, line: { color: C.accent6, width: 1 }, objectName: 'Screenshot frame' });
  tb(s, 'Live at abhimanyu04.codeberg.page/mohali-urban-growth (compare view)', { x: 0.6, y: 6.33, w: 6.9, h: 0.3, fontSize: 11, color: C.accent6 });
  tb(s, 'What it does', { x: 7.85, y: 1.95, w: 4.88, h: 0.45, fontSize: 18, bold: true });
  tb(s, bulletRuns(['A guided tour of the findings, step by step', 'Compare two years side by side with a drag handle', 'Search a place and read hectares within 0.5–3 km', 'Satellite background, filters and a 1 km² growth grid', 'Open source (Leaflet), hosted free on Codeberg Pages']), { x: 7.85, y: 2.45, w: 4.88, h: 2.4 });
  tb(s, 'Future work', { x: 7.85, y: 4.95, w: 4.88, h: 0.45, fontSize: 18, bold: true });
  tb(s, bulletRuns(['Hotspot analysis: finding where growth is bunched together (Getis-Ord Gi*)', 'Development Pressure Index: distance to built-up areas, roads, the airport and town centres']), { x: 7.85, y: 5.45, w: 4.88, h: 1.25 });
  s.addNotes('The web map is live at https://abhimanyu04.codeberg.page/mohali-urban-growth/, hosted free on Codeberg Pages, a non-profit, open-source service (the site files are in codeberg.org/Abhimanyu04/mohali-urban-growth). Start the demo with the Guided tour button: nine steps that move the map and explain each finding. The map uses the same land-cover maps and results.json as these slides, and every figure is computed in the browser. It was built with Leaflet, an open-source map library, not with qgis2web, the tool the teacher\u2019s plan named (UNCONFIRMED): say so if asked. You may replace the screenshot with your own of the live site. Future work is mentioned only here and in the conclusion; it is not being built now.');

  // ===== 21. Limitations =====
  s = pres.addSlide({ masterName: 'CONTENT', sectionTitle: 'Outlook' });
  s.addText('Limitations', { placeholder: 'title' });
  kicker(s, 'What the results can and cannot tell us');
  const lims = [
    ['FaMagnifyingGlass', C.accent1, 'Undercount', `The map finds about ${Math.round(ACC['Built-up'].producers_accuracy_pct)}% of real built-up land; small villages, roads and houses under trees are missed`],
    ['FaObjectGroup', C.accent5, 'Look-alike classes', 'Bare fields and bright roofs share groups; water bodies were too small to form a class'],
    ['FaTags', C.accent2, 'Mixed pixels', 'At 30 m, one pixel can hold fields and houses, so small settlements are hard to separate'],
    ['FaEye', C.accent3, 'Classification noise', `About ${n0(Math.round(F.lost_bu / 100) * 100)} ha mapped as built-up in 2015 were not built-up in 2025, so changes include some noise`],
    ['FaSatellite', C.accent4, 'Crop stage', 'Crops were at slightly different stages each March, so some cropland shows as trees or bare land'],
    ['FaScaleBalanced', C.accent6, 'Not covered', 'Permits and zoning (GMADA/PUDA) are not included, and no census exists for 2015–2025'],
  ];
  for (let i = 0; i < lims.length; i++) {
    const x = 0.6 + (i % 3) * 4.125, y = 1.95 + Math.floor(i / 3) * 2.45;
    card(s, x, y, 3.88, 2.2, lims[i][2]);
    await iconCircle(s, lims[i][0], x + 0.25, y + 0.25, 0.55, lims[i][1], lims[i][2]);
    tb(s, lims[i][2], { x: x + 0.95, y: y + 0.27, w: 2.75, h: 0.5, fontSize: 17, bold: true, valign: 'middle' });
    tb(s, lims[i][3], { x: x + 0.25, y: y + 0.95, w: 3.4, h: 1.15, fontSize: 14 });
  }
  s.addNotes('The undercount is the most important limitation: the corrected 2025 built-up area is higher than the map figure. The growth direction and the West-versus-East pattern are not affected by it. The photo labels were AI-assisted and should be spot-checked by the students.');

  // ===== 22. Conclusion =====
  s = pres.addSlide({ masterName: 'CLOSING_DARK', sectionTitle: 'Outlook' });
  s.addText('Conclusion', { placeholder: 'title' });
  [[`+${n0(C1525.increase_ha)} ha`, `built-up land added, 2015–2025: +${Math.round(C1525.pct_change)}%, or ${p1(C1525.lcr_pct_per_year)}% a year`], [`${ZW.ueii_2015_2025.toFixed(2)} vs ${ZE.ueii_2015_2025.toFixed(2)}`, 'UEII, West (Kharar–Mohali) vs East (Dera Bassi–Zirakpur): the West grew faster'], [`${n0(F.crop_to_bu)} ha`, `of cropland turned into built-up land (${Math.round(F.crop_share)}% of the new built-up)`]]
    .forEach(([v, l], i) => { const x = 0.6 + i * 4.125; card(s, x, 1.55, 3.88, 2.3, 'Finding ' + (i + 1), C.background1); tb(s, v, { x: x + 0.3, y: 1.75, w: 3.3, h: 0.8, fontSize: 30, bold: true, color: C.accent1, valign: 'middle' }); tb(s, l, { x: x + 0.3, y: 2.6, w: 3.3, h: 1.1 }); });
  tb(s, 'Why it matters', { x: 0.6, y: 4.1, w: 12.13, h: 0.4, fontSize: 18, bold: true, color: C.accent5 });
  tb(s, `Built-up land nearly doubled in ten years and grew faster after 2020 (${p1(C2025.lcr_pct_per_year)}% a year, up from ${p1(C1520.lcr_pct_per_year)}%). The map undercounts small settlements, so the true figures are likely higher. Water, roads and services need to keep pace, above all in the Kharar–Mohali corridor.`, { x: 0.6, y: 4.55, w: 12.13, h: 0.95, color: C.background1 });
  tb(s, 'Next steps', { x: 0.6, y: 5.55, w: 12.13, h: 0.4, fontSize: 18, bold: true, color: C.accent5 });
  tb(s, bulletRuns(['Spot-check the photo labels and maps; share the web map link', 'Future work: hotspot analysis (Getis-Ord Gi*) and a Development Pressure Index']), { x: 0.6, y: 6.0, w: 12.13, h: 0.8, color: C.background1 });
  s.addNotes(`Headline: built-up area grew from ${n0(BU[2015])} ha (2015) to ${n0(BU[2025])} ha (2025). The figures are conservative: the accuracy check suggests about ${n0(Math.round(ADJ.error_adjusted_ha / 100) * 100)} ha were built-up in 2025. Keep the headline on urban growth; the cropland finding supports it.`);

  // ===== 23. Glossary =====
  s = pres.addSlide({ masterName: 'CONTENT', sectionTitle: 'Outlook' });
  s.addText('Glossary: the technical words in plain English', { placeholder: 'title' });
  const gl = [
    ['Landsat', 'A NASA / US Geological Survey satellite. Its free images have 30 m pixels.'],
    ['Band', 'One kind of light the satellite measures, such as blue, red or near-infrared.'],
    ['Pixel', 'One small square of a satellite image: here 30 m × 30 m, or 0.09 hectare.'],
    ['Composite', 'One clean picture made from two clear photos, keeping the middle value of each pixel.'],
    ['LULC', 'Land use / land cover: what covers the ground, such as buildings, crops or trees.'],
    ['K-means', 'A method that sorts things into a chosen number of groups by similarity, without labels.'],
    ['Cluster (group)', 'One set of similar pixels found by K-means. It has a number until people name it.'],
    ['Training a model', 'Letting the computer study the pixels and adjust its groups until they stop changing.'],
    ['Hectare', 'A unit of land area: a square 100 m × 100 m, about 2.5 acres.'],
    ['UEII', 'Urban Expansion Intensity Index: new built-up land each year as a % of a zone’s area.'],
    ['Land consumption rate', 'How fast built-up land grows each year, as a compound percentage (SDG 11.3.1 formula).'],
    ['Accuracy check', 'Comparing the map with detailed photos or another map to see how often it is right.'],
  ];
  gl.forEach(([term, def], i) => {
    const x = 0.6 + Math.floor(i / 6) * 6.17, y = 1.45 + (i % 6) * 0.9;
    card(s, x, y, 5.96, 0.78, term);
    tb(s, term, { x: x + 0.2, y, w: 1.9, h: 0.78, fontSize: 15, bold: true, color: C.accent1, valign: 'middle' });
    tb(s, def, { x: x + 2.15, y, w: 3.65, h: 0.78, fontSize: 13, valign: 'middle' });
  });
  s.addNotes('Use this slide if anyone asks what a technical word means.');

  // ===== 24. References =====
  s = pres.addSlide({ masterName: 'CONTENT', sectionTitle: 'Outlook' });
  s.addText('References', { placeholder: 'title' });
  const refsL = [
    '1. U.S. Geological Survey. Landsat Collection 2 Level-2 Science Products. usgs.gov/landsat-missions',
    '2. Microsoft Planetary Computer. Landsat Collection 2 Level-2 and ESA WorldCover data catalogue. planetarycomputer.microsoft.com',
    '3. Zanaga, D. et al. (2021). ESA WorldCover 10 m 2020 v100. Zenodo. doi.org/10.5281/zenodo.5571936',
    '4. Pedregosa, F. et al. (2011). Scikit-learn: Machine learning in Python. Journal of Machine Learning Research, 12, 2825–2830.',
    '5. Olofsson, P., Foody, G.M., Herold, M., Stehman, S.V., Woodcock, C.E. and Wulder, M.A. (2014). Good practices for estimating area and assessing accuracy of land change. Remote Sensing of Environment, 148, 42–57.',
    '6. Puyravaud, J.-P. (2003). Standardizing the calculation of the annual rate of deforestation. Forest Ecology and Management, 177, 593–596.',
  ];
  const refsR = [
    '7. United Nations. Sustainable Development Goals: Targets 11.3, 2.4 and 15.3. sdgs.un.org/goals',
    '8. UN Statistics Division and UN-Habitat. SDG indicator metadata 11.3.1. unstats.un.org/sdgs/metadata',
    '9. GADM. Database of Global Administrative Areas. gadm.org',
    '10. Esri. World Imagery basemap.',
    '11. OpenStreetMap contributors. openstreetmap.org (ODbL licence)',
    '12. QGIS Development Team (2026). QGIS Geographic Information System. qgis.org',
  ];
  const refRuns = (arr) => arr.map((t, i) => ({ text: t, options: { breakLine: i < arr.length - 1, paraSpaceAfter: 9 } }));
  tb(s, refRuns(refsL), { x: 0.6, y: 1.45, w: 5.9, h: 5.4, fontSize: 13 });
  tb(s, refRuns(refsR), { x: 6.83, y: 1.45, w: 5.9, h: 5.4, fontSize: 13 });
  s.addNotes('The teacher wants mostly official sources. Add the Census of India and GMADA/PUDA documents if you use them, and the GADM version you downloaded. Check each entry before submitting.');

  await pres.writeFile({ fileName: OUT });
  await applyTheme(OUT, THEME);
  console.log('written', OUT);
}
build().catch((e) => { console.error(e); process.exit(1); });
