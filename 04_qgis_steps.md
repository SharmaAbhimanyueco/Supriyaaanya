# QGIS steps

These steps are written for QGIS 4.2, the version your boundary file was saved with. QGIS 3.44 LTR works the same way. Menu names can differ slightly between versions. If something isn't where this guide says, tell me what you see.

Plain words for the main terms:
- **Raster:** a grid of pixels, like a photo. **Vector:** shapes drawn from points and lines, like the study-area outline.
- **Processing Toolbox:** QGIS's searchable list of tools. Open it from **Processing → Toolbox**, then type a tool's name in its search box.
- **CRS (coordinate reference system):** the map grid that tells QGIS where each pixel sits. We use **EPSG:32643 (WGS 84 / UTM zone 43N)**, which works in metres, so areas come out in square metres. Measuring areas on a latitude/longitude grid is like measuring a room with a protractor.

## 0. Set up (once)

1. Install QGIS from qgis.org (4.2, or 3.44 LTR).
2. Go to **Plugins → Manage and Install Plugins**. Install the **Semi-Automatic Classification Plugin** (SCP; version 9 works with QGIS 4) and **qgis2web**. SCP may install extra Python parts the first time it runs. If it shows an error, paste it into the chat.
3. **Add satellite imagery as a background** (you'll need it to name the clusters). In the **Browser** panel, right-click **XYZ Tiles → New Connection**. Name: `Esri World Imagery`. URL: `https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}`. Click OK, then double-click it to add it to the map. Credit "Esri World Imagery" wherever you show it.
4. Go to **Project → Properties → CRS**, search `32643`, choose **WGS 84 / UTM zone 43N**, and click OK. Save the project with **Project → Save As**.
5. Install **Google Earth Pro**, a free desktop app. Its **View → Historical Imagery** slider shows what a place looked like in 2015 or 2020. You'll need it to name the older years' clusters.

## 1. Load the data and fix the location map

1. Unzip `Study_Area.zip` and drag `study_area.shp` into QGIS.
2. Right-click it → **Properties → Labels → No Labels**. This hides the wrong "Kharar"/"Rajpura" labels.
3. Make a single outline in metres: run **Dissolve** (Processing Toolbox) on `study_area`, then run **Reproject Layer** on the result with target CRS EPSG:32643. Save it as `study_area_32643.gpkg` and use it from now on.
4. Fix the location map in your print layout. Select the India inset map item and tick **Lock layers** while only the India layer and a red location marker are visible, so no labels leak into the inset. Add a text label reading `Basemap © OpenStreetMap contributors`. Then export the map again.
5. Drag in the three images (`landsat_2015_febmar.tif` and the others). Right-click one → **Properties → Information** and check that the pixel size is 30 and the CRS is EPSG:32643. For a natural-colour view, go to **Symbology** and set Red = band 3, Green = band 2, Blue = band 1.

## 2. Clip each image to the study area

Open **Clip raster by mask layer** from the Processing Toolbox (under GDAL → Raster extraction).
- Input layer: `landsat_2015_febmar`
- Mask layer: `study_area_32643`
- Tick **Match the extent of the clipped raster to the extent of the mask layer**
- Assign a specified NoData value to output bands: `-32768`
- Clipped (mask): save as `clip_2015.tif`

Repeat for 2020 and 2025. To do all three at once, use **Run as Batch Process** at the bottom of the tool window.

## 3. Cluster each year (unsupervised classification)

Use **exactly the same settings for all three years** and write them down. They go on slide 9. Ask the teacher which route she expects (question 3 in the message).

**Route A: the SCP plugin (K-means)**
1. Open **SCP → Band set**. Create band set 1 from the six bands of `clip_2015`, in order: blue, green, red, NIR, SWIR1, SWIR2. If the band set only accepts single-band files, first split the image with SCP's **Split raster bands** tool (under Preprocessing).
2. Open **SCP → Band processing → Clustering**. Choose band set 1, method **K-means**, **number of classes: 10**, maximum iterations: 10, seed signatures from band values, and minimum distance. Tick **Use NoData value** and enter `-32768`.
3. Run it and save the result as `clusters_2015.tif`.
4. Repeat for 2020 and 2025 with the same settings, using a band set for each year.

SCP 9 changed some menus. If they don't match the steps above, the "Clustering" page of the SCP manual shows the current layout: semiautomaticclassificationmanual.readthedocs.io

**Route B: GRASS tools (no plugin needed)**
1. Open **i.cluster** from the Processing Toolbox (GRASS → Imagery). Input rasters: `clip_2015` (all bands). Initial number of clusters: 10. Save the signature file as `sig_2015`.
2. Open **i.maxlik**. Input rasters: `clip_2015`. Signature file: `sig_2015`. Save the classification as `clusters_2015.tif`.
3. Repeat for 2020 and 2025.

## 4. Name the clusters

Cluster numbers mean nothing on their own, and **cluster 3 in 2015 is not the same as cluster 3 in 2020**. Name each year separately.
1. Right-click `clusters_2015` → **Properties → Symbology**. Set the render type to **Paletted/Unique values** and click **Classify**. Set the layer opacity to about 60% so the satellite background shows through.
2. Compare each colour with the Esri imagery. Use the **Identify Features** tool (the "i" cursor) to click places you recognise: dense parts of Mohali, Zirakpur and Kharar, open fields, the wooded foothills in the north, rivers and ponds.
3. For 2015 and 2020, check the same spots in Google Earth Pro's historical imagery, because today's imagery shows today's buildings.
4. Fill in a naming table for each year:

| Cluster | What it covers | Class code |
|---|---|---|
| 1 | | |
| 2 | | |
| … | | |
| 10 | | |

Use the same class codes **every year**: 1 = Built-up, 2 = Cropland, 3 = Trees/vegetation, 4 = Water, 5 = Bare/fallow.

A cluster may clearly mix two classes; bare fields mixed with built-up is the most common case. If that happens, record it as a limitation. If the teacher agrees, you can instead run the clustering again with more clusters, for example 15.

## 5. Merge the clusters into 5 classes

Open **Reclassify by table** from the Processing Toolbox.
- Raster layer: `clusters_2015`
- Reclassification table: click **…** and add one row per cluster. Minimum = the cluster number, Maximum = the same number, Value = the class code. For example, the row `4 | 4 | 1` turns cluster 4 into Built-up.
- Range boundaries: **min <= value <= max**
- Save as `lulc_2015.tif`

Repeat for 2020 and 2025, each with that year's own table. Then give every LULC map the same colours: Built-up `B03A2E` (brick red), Cropland `8DB63C` (wheat green), Trees/vegetation `2E6B3F` (dark green), Water `2F7FB0` (blue), Bare/fallow `D9A441` (ochre). The slides use the same colours. Style one map, save the style with right-click → **Styles → Save Style**, then use **Load Style** on the others.

## 6. Measure the area of each class

Run **Raster layer unique values report** (Processing Toolbox) with `lulc_2015` as the input.
The result lists each class value with its pixel **count** and its area in **m²**. Hectares = m² ÷ 10,000, which is the same as count × 0.09, because one 30 m pixel is 900 m², or 0.09 ha.
Repeat for 2020 and 2025, and copy the numbers into the tables in [05_metrics_and_formulas.md](05_metrics_and_formulas.md) or into a spreadsheet.

## 7. Change maps

Open **Raster → Raster Calculator** for each of these:
- **New built-up 2015–2025:** `("lulc_2015@1" != 1) AND ("lulc_2025@1" = 1)`. Save as `new_builtup_2015_2025.tif`. Pixels with the value 1 became built-up.
- **Cropland that became built-up:** `("lulc_2015@1" = 2) AND ("lulc_2025@1" = 1)`. Save as `crop_to_builtup_2015_2025.tif`.
- **The full from–to table:** `"lulc_2015@1" * 10 + "lulc_2025@1"`. Save as `fromto_2015_2025.tif`. Each pixel gets a two-digit code: the first digit is its 2015 class and the second its 2025 class. So 21 means cropland became built-up, and 11 means it stayed built-up. Run **Raster layer unique values report** on this layer to get every change in one table.

If you have time, do the same for 2015–2020 and 2020–2025.

## 8. Where did growth happen?

You need zones to compare. Correct tehsil outlines are best (see the warning in the [README](README.md)). Until you have them, use the two pieces of the boundary file, renamed honestly as **West zone (Kharar and Mohali)** and **East zone (Dera Bassi, including Zirakpur)**. Say in the report that these come from GADM, not from official tehsil maps. To look at Zirakpur alone, draw a polygon around the town (**Layer → Create Layer → New GeoPackage Layer**, geometry type polygon) and describe it as approximate.

Then open **Zonal histogram** (Processing Toolbox). Raster layer: `lulc_2015`. Vector layer: your zones. The output adds one column per class (HISTO_1 to HISTO_5) with the pixel count in each zone. Multiply the counts by 0.09 to get hectares. Repeat for 2025, then work out the UEII for each zone (see [05_metrics_and_formulas.md](05_metrics_and_formulas.md)).

## 9. Web map

1. **Make the layers light.** Rasters turn into heavy images on the web. For the change layer, convert to shapes: run **Polygonize (raster to vector)** on `new_builtup_2015_2025`. Keep only the new built-up areas with **Extract by attribute** (DN = 1), then run **Simplify** with a tolerance of about 15 m.
2. Go to **Web → qgis2web → Create web map**. Tick the layers to include: the study-area outline, `lulc_2015`, `lulc_2020`, `lulc_2025` and the new built-up shapes. Choose **Leaflet**. Under Export, pick a folder and click **Export**. Open the `index.html` it creates to check the map in your browser.
3. **Publish it on GitHub Pages.** Upload the exported folder to this repository, for example as a folder named `webmap`. On GitHub, go to **Settings → Pages**, choose **Deploy from a branch**, then branch `main` and folder `/ (root)`, and click **Save**. After a minute or two the page shows your site's address. The map will be at that address followed by `/webmap/`. On a free GitHub account, Pages only works for public repositories (check GitHub's documentation for your plan). If you keep the GADM outline on the map, name GADM as its source, and ask the teacher whether that's acceptable (question 5 in the message).
