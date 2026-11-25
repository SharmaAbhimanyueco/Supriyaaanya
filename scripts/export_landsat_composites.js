/*
 * Urban growth in the Mohali–Kharar–Zirakpur–Dera Bassi belt, Punjab
 * Step 1: download one cloud-free Landsat 8/9 image per year (February–March).
 *
 * This script does NOT classify anything. All classification is done in QGIS,
 * as the teacher asked. How to run it: see 03_get_satellite_images.md
 *
 * What it does, in plain words:
 *   1. Finds every Landsat 8 and Landsat 9 picture of the area taken in
 *      February–March of each year.
 *   2. Hides clouds and cloud shadows in each picture.
 *   3. Stacks the pictures and keeps, for every pixel, the middle (median)
 *      value: a "typical clear day" picture for that year.
 *   4. Saves one GeoTIFF file per year to your Google Drive.
 */

// ---------- Settings (change only if the teacher asks) ----------
var YEARS = [2015, 2020, 2025];      // UNCONFIRMED: ask the teacher
var FIRST_DAY = '-02-01';            // 1 February
var DAY_AFTER_LAST = '-04-01';       // so the last day used is 31 March
var DRIVE_FOLDER = 'urban_growth_mohali';

// Study area plus about 5 km around it, as a rectangle in UTM zone 43N
// (EPSG:32643, metres). Worked out from the study-area boundary file and
// snapped to the 30 m pixel grid, so all three years line up exactly.
var XMIN = 638850, YMIN = 3354990, XMAX = 690570, YMAX = 3429510;
var REGION = ee.Geometry.Rectangle([XMIN, YMIN, XMAX, YMAX], 'EPSG:32643', false);
var GRID = [30, 0, XMIN, 0, -30, YMAX];   // 30 m pixels, same origin every year
var NODATA = -32768;

// ---------- Cloud masking and scaling (Landsat Collection 2, Level 2) ----------
function prepare(image) {
  var qa = image.select('QA_PIXEL');
  // Bits 0-4 flag fill, dilated cloud, cirrus, cloud and cloud shadow.
  var clear = qa.bitwiseAnd(parseInt('11111', 2)).eq(0);
  var notSaturated = image.select('QA_RADSAT').eq(0);
  var reflectance = image
    .select(['SR_B2', 'SR_B3', 'SR_B4', 'SR_B5', 'SR_B6', 'SR_B7'],
            ['blue', 'green', 'red', 'nir', 'swir1', 'swir2'])
    .multiply(0.0000275).add(-0.2);   // USGS scale factors: surface reflectance
  return reflectance.updateMask(clear).updateMask(notSaturated);
}

// Landsat 8 (from 2013) and Landsat 9 (from late 2021) use the same band numbers.
var landsat = ee.ImageCollection('LANDSAT/LC08/C02/T1_L2')
  .merge(ee.ImageCollection('LANDSAT/LC09/C02/T1_L2'))
  .filterBounds(REGION);

Map.centerObject(REGION, 10);
var trueColour = {bands: ['red', 'green', 'blue'], min: 0, max: 0.3};
var falseColour = {bands: ['nir', 'red', 'green'], min: 0, max: 0.4};

YEARS.forEach(function (year) {
  var start = ee.Date(year + FIRST_DAY);
  var end = ee.Date(year + DAY_AFTER_LAST);
  var scenes = landsat.filterDate(start, end);
  print('Year ' + year + ': Landsat pictures found (Feb–Mar)', scenes.size());

  // Median of all clear pixels in February–March.
  var composite = scenes.map(prepare).median();

  // If a pixel had no clear view in February–March, fill it from January–March.
  var backup = landsat.filterDate(ee.Date(year + '-01-01'), end).map(prepare).median();
  composite = composite.unmask(backup);

  var showByDefault = (year === YEARS[YEARS.length - 1]);
  Map.addLayer(composite.clip(REGION), trueColour, year + ' true colour', showByDefault);
  Map.addLayer(composite.clip(REGION), falseColour, year + ' false colour (plants show red)', false);

  // Reflectance x 10000 as whole numbers keeps the files small.
  var out = composite.multiply(10000).round().toInt16().unmask(NODATA, false);

  Export.image.toDrive({
    image: out,
    description: 'landsat_' + year + '_febmar',
    folder: DRIVE_FOLDER,
    fileNamePrefix: 'landsat_' + year + '_febmar',
    region: REGION,
    crs: 'EPSG:32643',
    crsTransform: GRID,
    maxPixels: 1e10,
    fileFormat: 'GeoTIFF',
    formatOptions: {noData: NODATA}
  });
});

Map.addLayer(
  ee.FeatureCollection([ee.Feature(REGION)]).style({color: 'yellow', fillColor: '00000000', width: 2}),
  {}, 'Export area');
