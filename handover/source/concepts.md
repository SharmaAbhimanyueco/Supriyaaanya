# Concepts handbook: every technical term in the project, in plain words

How to use this chapter. Each concept has up to four lines: what it means, an everyday picture, exactly what this project did (with the real numbers and the file where you can see them), and one sentence you can say aloud if the teacher asks. Every number comes from `results/results.json`, `results/README.md` or the scripts in `scripts/analysis/`. Where something is still waiting on the teacher it says **UNCONFIRMED**.

---

## Part A — Maps and data basics

### GIS (Geographic Information System)
**In plain words:** Software that stores, shows and calculates with information that has a place on Earth. QGIS is the free GIS the teacher asked for.
**Everyday analogy:** A phone map app where you can switch layers (roads, shops, traffic) on and off, and also ask it questions such as "how much area is covered by buildings?"
**In this project:** The calculations ran in Python (numpy, rasterio, scikit-learn), not in QGIS. Part I shows the QGIS tool for every step. The guide is `04_qgis_steps.md`.

### Geospatial data
**In plain words:** Any data that says where something is, as well as what it is.
**Everyday analogy:** A parcel with an address label. Without the address, you know what is inside but not where to deliver it.
**In this project:** The Landsat images, the study-area boundary, the land-cover maps and the 1 km² hexagon grid are all geospatial data.

### Raster vs vector
**In plain words:** A raster is a grid of pixels, each holding a number. A vector is made of points, lines and polygons drawn from coordinates.
**Everyday analogy:** A raster is a photo made of tiny coloured tiles. A vector is a drawing made of outlines you could trace with a pen.
**In this project:** Rasters: the Landsat composites and the `lulc_YEAR.tif` maps. Vectors: the study-area boundary (Shapefile) and the hexagons (`webmap/data/hex.geojson`).

### Pixel and spatial resolution
**In plain words:** A pixel is one square of a raster. Spatial resolution is how much ground one pixel covers.
**Everyday analogy:** A mosaic floor. Big tiles give a blocky picture. Small tiles show fine detail.
**In this project:** One pixel is 30 m × 30 m = 900 m² = 0.09 ha. So hectares = pixel count × 0.09. The study area holds 1,209,178 pixels, about 108,800 ha. The working grid is 1409 × 2170 pixels (`CLAUDE.md`).
**If the teacher asks:** "Each pixel is 30 m by 30 m, which is 0.09 hectare, so we count pixels and multiply by 0.09."

### Extent and nodata
**In plain words:** The extent is the rectangle a raster covers. Nodata is a special number that means "no valid value here".
**Everyday analogy:** A photo is always a rectangle, even if you only care about one house in it. The white margin you ignore is the nodata.
**In this project:** The composites are cut to a rectangle around the study area. Pixels outside the boundary, or with no clear view in any scene, are nodata: −32768 in the composites, 0 in the land-cover maps (`build_composites.py`). This is why the yearly totals differ slightly: 108,799, 108,826 and 108,783 ha.

### File formats used
**In plain words:** Each file type stores data in a different way.
**Everyday analogy:** Photos, spreadsheets and PDFs each suit different jobs.
**In this project:**
- **GeoTIFF (.tif):** a raster with its location built in. Composites, `clusters_YEAR.tif` and `lulc_YEAR.tif` (`results/rasters/`, `results/images/`).
- **Shapefile (.shp):** a vector format made of several files. The GADM boundary arrives this way in `Study_Area.zip` (not in the repo).
- **GeoJSON (.geojson):** vectors as text. `webmap/data/hex.geojson`.
- **PNG:** an ordinary picture: map figures and `webmap/layers/lulc_YEAR.png`.
- **CSV:** a plain table: `reference_labels.csv`.
- **JSON:** structured text: `results/results.json` holds every final number.
- **NumPy .npy:** a saved Python array: `inside.npy`, `zones.npy`, `naming_reference_centres.npy`.
**If the teacher asks:** "Rasters are GeoTIFF, the boundary is a Shapefile, the web grid is GeoJSON, and all final numbers are in one JSON file."

### Metadata
**In plain words:** Data about the data: who made it, when, the coordinate system, the pixel size, the nodata value.
**Everyday analogy:** The label on a jar: what is inside, when it was made, how to store it.
**In this project:** The composites carry their grid, 30 m pixel size, nodata value and band names (blue, green, red, nir, swir1, swir2). In QGIS, right-click a layer, then Properties, then Information, to check them (`04_qgis_steps.md`, step 1).

---

## Part B — Where on Earth

### Coordinates
**In plain words:** Numbers that name a place, such as latitude and longitude, or metres east and north.
**Everyday analogy:** A seat number in a cinema: row and seat.
**In this project:** Check-point locations are stored as longitude and latitude in `points.csv`. The analysis grid uses metres.

### Coordinate reference system (CRS)
**In plain words:** The rulebook that turns numbers into places on Earth. The same coordinates mean different places under different rulebooks.
**Everyday analogy:** The same number "100" means different amounts in rupees and in dollars. You must know the unit.
**In this project:** Everything analysed uses one CRS, EPSG:32643. Mixing CRSs is the classic way to get layers that do not line up.

### Geographic vs projected CRS
**In plain words:** A geographic CRS uses angles (degrees of latitude and longitude) on the globe. A projected CRS flattens part of the globe onto a plane and uses metres.
**Everyday analogy:** Measuring a room with a protractor (degrees) versus a tape measure (metres). `04_qgis_steps.md` uses this very comparison.
**In this project:** Boundary and check points arrive in degrees (WGS 84). The analysis grid is projected (UTM 43N), so a pixel is exactly 30 m.

### EPSG codes
**In plain words:** A short number that names a CRS in the public EPSG registry.
**Everyday analogy:** A PIN code that stands for a whole postal area.
**In this project:** Three codes appear: 4326, 32643 and 3857 (next three entries).

### WGS 84 (EPSG:4326)
**In plain words:** The standard model of Earth's shape used by GPS, with positions in degrees.
**Everyday analogy:** The common language every GPS device speaks.
**In this project:** The GADM boundary and the check-point coordinates are in WGS 84. `make_chips.py` converts to it to fetch Esri photos. Not used for areas.

### UTM zone 43N (EPSG:32643)
**In plain words:** UTM cuts the world into 6-degree-wide strips. Zone 43N covers 72°E to 78°E in the northern hemisphere, with its central line at 75°E. Inside it, distortion is small and coordinates are in metres.
**Everyday analogy:** A tailor's tape laid flat across one panel of a globe-shaped cloth: it measures well on that panel.
**In this project:** All 30 m grids, pixel counts and hectares use EPSG:32643 (WGS 84 / UTM zone 43N). One pixel is 900 m² in it.
**If the teacher asks:** "Mohali lies in UTM zone 43N, so hectares come out right in EPSG:32643."

### Why area must be measured in a projected CRS in metres
**In plain words:** Degrees do not have a fixed length on the ground. A degree of longitude shrinks as you go north. So a pixel "one hundredth of a degree wide" has different areas in different places.
**Everyday analogy:** Measuring a room with a protractor.
**In this project:** Pixel counts were made on the UTM grid, where every pixel is 900 m². That is why "pixels × 0.09" is valid.

### Web Mercator (EPSG:3857)
**In plain words:** The projection used by web map tiles such as OpenStreetMap. It keeps shapes right locally but stretches areas, more so away from the equator.
**Everyday analogy:** A map that enlarges northern places so they look bigger than they are.
**In this project:** Only used to display. `scripts/webmap/build_webmap.py` reprojects the class maps to 3857 for `webmap/layers/lulc_YEAR.png`. All areas and the hexagon statistics come from the 30 m UTM rasters, never from 3857.
**If the teacher asks:** "3857 is for drawing on the web; we measured area in UTM."

### Reprojection and resampling
**In plain words:** Reprojection moves a raster into another CRS or grid. Resampling decides what value each new pixel gets. Nearest neighbour copies the closest old pixel, so no new numbers appear.
**Everyday analogy:** Re-tiling a floor with a different tile layout. Nearest neighbour means each new tile copies the colour of the old tile underneath it. Averaging colours would make impossible shades.
**In this project:** The Landsat scenes were read onto one common 30 m grid with nearest neighbour (`build_composites.py`). The class maps were reprojected to 3857 for the web with nearest neighbour too (`build_webmap.py`).

---

## Part C — Satellites and images

### Remote sensing
**In plain words:** Learning about the ground from a distance, here by measuring the light it reflects.
**Everyday analogy:** Judging a fruit's ripeness from its colour without touching it.
**In this project:** Landsat 8 images from 2015, 2020 and 2025 are our only source for the land-cover maps.

### Electromagnetic spectrum and bands
**In plain words:** Light is a range of wavelengths. Our eyes see only a slice. A band is one narrow slice a satellite records.
**Everyday analogy:** A camera with extra colour filters, some for light we cannot see.
**In this project:** Six bands per pixel: blue, green, red, near-infrared (NIR), shortwave infrared 1 and 2 (SWIR1, SWIR2). Nominal ranges from NASA: blue 0.45–0.51 µm, green 0.53–0.59, red 0.64–0.67, NIR 0.85–0.88, SWIR1 1.57–1.65, SWIR2 2.11–2.29. Healthy plants reflect NIR strongly, which separates green wheat from concrete (`03_get_satellite_images.md`).
**If the teacher asks:** "We use six bands, including near-infrared, which plants reflect strongly."

### Reflectance
**In plain words:** The share of incoming sunlight that a surface bounces back, from 0 to 1.
**Everyday analogy:** White paper reflects most light, black cloth little.
**In this project:** A stored value of 1,234 means 12.34% reflected (`03_get_satellite_images.md`). K-means works on these 0–1 values (the stored integers ÷ 10,000).

### Landsat 8 and OLI
**In plain words:** Landsat 8 is a NASA and USGS Earth-observing satellite launched on 11 February 2013. Its Operational Land Imager (OLI) records the bands above at 30 m. It sees each place every 16 days.
**Everyday analogy:** A reliable photographer who returns to the same street on a fixed schedule.
**In this project:** We used Landsat 8 for all three years, so the sensor is the same each time.

### Collection 2 Level-2 surface reflectance (scale and offset)
**In plain words:** "Level-2 surface reflectance" is Landsat imagery corrected for the atmosphere, so it estimates what the ground itself reflects. It is stored as whole numbers, which must be rescaled.
**Everyday analogy:** A photo stored as a compressed file: you need the right "unzip" formula to get the true colours back.
**In this project:** USGS gives the rule: reflectance = DN × 0.0000275 − 0.2. The code does exactly this (`build_composites.py`). The result is then multiplied by 10,000 and stored as a 16-bit integer.
**If the teacher asks:** "We applied USGS's scale factor 0.0000275 and offset −0.2 to get real reflectance."

### WRS-2 path/row 147/39
**In plain words:** Landsat uses a fixed grid of footprints, numbered by path and row. The grid is called the Worldwide Reference System-2 (WRS-2).
**Everyday analogy:** Postal sorting areas: every address falls in one.
**In this project:** Every scene is path 147, row 39. One scene covers the whole study area.

### Revisit time
**In plain words:** How often a satellite passes over the same place. Landsat 8 repeats every 16 days.
**Everyday analogy:** A bus that arrives every 16 days.
**In this project:** The chosen dates are exactly 16 days apart in each year: 7 and 23 March 2015, 4 and 20 March 2020, 2 and 18 March 2025.

### Scene
**In plain words:** One image from one pass of the satellite.
**Everyday analogy:** One photo from a photo shoot.
**In this project:** Six scenes were used, such as `LC08_L2SP_147039_20150307_02_T1`. See `build_composites.py`.

### Clouds and the QA_PIXEL mask
**In plain words:** Clouds and their shadows hide the ground. Each Landsat scene includes a quality band, QA_PIXEL, that flags bad pixels bit by bit.
**Everyday analogy:** An exam sheet with a tick-box for each answer marked "unreadable".
**In this project:** The code keeps a pixel only if its lowest five bits (0–4) are all zero. Those bits flag fill, dilated cloud, cirrus, cloud and cloud shadow (`build_composites.py`; slide 7 notes). The bit layout is listed in the QA_PIXEL table of the USGS Landsat 8-9 Collection 2 Level-2 Science Product Guide.
**If the teacher asks:** "We removed pixels flagged as fill, cloud, cirrus or shadow using the built-in quality band."

### Compositing and the median
**In plain words:** A composite combines several images into one. The median is the middle value when numbers are sorted. It ignores extreme values, such as a leftover cloud edge.
**Everyday analogy:** Asking two friends for the temperature and taking the middle value of several readings. One odd reading does not drag the result.
**In this project:** For each pixel and band, the median of the clear values from the two March scenes. Where both were cloudy the pixel became nodata. Result: `composite_2015.tif`, `composite_2020.tif`, `composite_2025.tif`.

### Why March
**In plain words:** The repo gives these reasons: wheat is green in March, so farmland looks very different from buildings, and using the same month every year removes crop-season differences between years.
**Everyday analogy:** Comparing school photos taken on the same day each year, not in different seasons.
**In this project:** All six scenes are from March. Seasonal side effects are in Part J.

### True colour vs false colour
**In plain words:** True colour shows red, green and blue as your eye would. False colour puts other bands (such as near-infrared) into the screen's colours.
**Everyday analogy:** An ordinary photo versus a heat-camera picture.
**In this project:** True colour was used to recognise places when naming clusters. For the QGIS guide, set Red = band 3, Green = band 2, Blue = band 1 for a natural-colour view of the downloaded images (`04_qgis_steps.md`).

### Microsoft Planetary Computer and STAC
**In plain words:** The Planetary Computer is a free online library of satellite data. STAC (SpatioTemporal Asset Catalog) is the standard "catalogue card" format that describes each scene and lets you search by place and date.
**Everyday analogy:** A library's catalogue: search by topic and date, then fetch the book from the shelf.
**In this project:** `build_composites.py` searches the `landsat-c2-l2` collection by scene id with `pystac-client`, signs the links, and reads only the window we need. WorldCover comes from the same library.

### Google Earth Engine (the alternative)
**In plain words:** Google's free platform for processing satellite images online.
**Everyday analogy:** Using a rented kitchen instead of your own.
**In this project:** Not used for the results. `03_get_satellite_images.md` and `scripts/export_landsat_composites.js` describe an Earth Engine route that builds February–March composites and exports them to Google Drive. It is meant for anyone repeating the work, and it matches the QGIS route in Part I.

---

## Part D — From image to land-cover map

### Study-area boundary and clipping
**In plain words:** Clipping cuts a raster to the shape of a boundary so only the study area is analysed.
**Everyday analogy:** Cutting a shape out of a photo with scissors.
**In this project:** The GADM outline is clipped on the grid, leaving 1,209,178 pixels (`inside.npy`).

### GADM, its licence and the mislabelled polygons
**In plain words:** GADM is a free database of administrative boundaries. Its licence forbids redistribution, so the file is not in the repo.
**Everyday analogy:** A map you may borrow but not photocopy and hand out.
**In this project:** The file has two polygons. The one labelled "Kharar" is really Kharar plus Mohali. The one labelled "Rajpura" is really Dera Bassi including Zirakpur (Rajpura town is outside). They are used only as a **West zone** and an **East zone**, not as official tehsils.
**If the teacher asks:** "The labels in the source file are wrong, so we call the two parts West and East zones, not tehsils."

### LULC and the four classes
**In plain words:** LULC means land use / land cover: what covers the ground. A class is one named category.
**Everyday analogy:** Sorting a toy box into four bins.
**In this project:** Codes in `lulc_YEAR.tif`: 1 Built-up (B03A2E), 2 Cropland (8DB63C), 3 Trees/vegetation (2E6B3F), 5 Bare/fallow (D9A441), 0 nodata. Code 4 (Water, 2F7FB0) is unused.
**If the teacher asks:** "Four classes: built-up, cropland, trees, and bare or fallow."

### Why water is missing
**In plain words:** No K-means cluster picked out water.
**Everyday analogy:** A single drop in a bucket of paint. It cannot change the colour.
**In this project:** Water bodies are too small at 30 m to fill a pixel, so no water cluster appeared (`results/README.md`). The water class stays defined but empty.

### Spectral signature
**In plain words:** The pattern of reflectance across the bands for one kind of surface.
**Everyday analogy:** A fingerprint: each surface leaves its own.
**In this project:** The centre of each cluster is a six-number signature (saved in `results/model_checks/naming_reference_centres.npy` and in `final_model_training.json`).

### NDVI
**In plain words:** The Normalised Difference Vegetation Index. The formula is (NIR − Red) ÷ (NIR + Red). Values run from −1 to 1. Greener, denser plants give higher values. Bare ground and buildings give low values.
**Everyday analogy:** A "greenness meter".
**In this project:** NDVI is not an input to K-means; the clustering used the six raw bands. It is used only to number the clusters. After training, clusters are sorted by the NDVI of their centre, so cluster 1 has the lowest NDVI and cluster 10 the highest (`train_full.py`, `results2.py`). Numbering this way makes runs comparable, since K-means' own numbers are arbitrary.
**If the teacher asks:** "We used NDVI only to put the clusters in a fixed order; the clustering itself used six bands."

### Unsupervised vs supervised classification
**In plain words:** Supervised: you give examples of each class and the computer learns the rules. Unsupervised: the computer finds groups by itself and you name them afterwards.
**Everyday analogy:** Supervised is teaching with labelled flashcards. Unsupervised is handing over a pile of mixed seeds and saying "sort by look".
**In this project:** Unsupervised K-means, as the teacher's brief says. The team named the groups afterwards.

### K-means step by step
**In plain words:** You choose k (the number of groups). K-means then (1) picks k starting centres, (2) assigns every pixel to its nearest centre, (3) moves each centre to the average of its pixels, and repeats steps 2 and 3 until nothing moves.
**Everyday analogy:** Sorting a mixed sack of pulses into 10 heaps by look, shuffling grains until none needs to move (the deck's slide 10 analogy).
**In this project:** The settings are in `train_full.py` and `results2.py`:
- **k = 10** groups.
- **Centres** are six numbers each (the six bands).
- **Iterations:** at most 300. The three runs stopped after 35, 31 and 29 (`results.json`, `training`).
- **Inertia:** the total squared distance from pixels to their centres. Lower is tighter. The final fits were 5243.40, 5243.77 and 5243.46.
- **n_init = 10:** the whole procedure is run from 10 different starting points and the best (lowest inertia) is kept. This guards against a bad start.
- **Random seed:** a number that fixes the "random" starting points so results can be repeated. Seeds 0, 1 and 2 were run. Seed 0 had the lowest inertia and is the final model.
**If the teacher asks:** "K-means with 10 clusters, 10 starts, up to 300 iterations; it converged in about 30 iterations."

### ISODATA
**In plain words:** Another unsupervised method taught in remote sensing. In general, it can split or merge clusters during the run, so you give a range of cluster numbers rather than one fixed number. ISODATA stands for Iterative Self-Organizing Data Analysis Technique.
**Everyday analogy:** K-means is "sort into exactly 10 heaps". ISODATA is "start with about 10 and let heaps split or merge as needed".
**In this project:** The teacher's brief says "K-means or ISODATA, 8–10 clusters, identical settings every year". Which she wants is **UNCONFIRMED** (`01_message_to_teacher.md`, question 3). We used K-means. `04_qgis_steps.md` offers GRASS `i.cluster` + `i.maxlik` as a no-plugin QGIS route.
**If the teacher asks:** "We used K-means; if you prefer ISODATA, the steps and the naming stay the same, and only the clustering tool changes."

### Clusters vs classes (naming and merging)
**In plain words:** A cluster is just a numbered group. A class is a meaningful land type. Naming links a cluster to a class. Merging several clusters into one class is called reclassification.
**Everyday analogy:** Ten unnamed student groups placed into four school houses (slide 11).
**In this project:** Ten clusters become four classes (`results/README.md`): 1 Bare/fallow; 2 Built-up; 3 and 5 Trees/vegetation; 4, 6, 7, 8, 9 and 10 Cropland. Only cluster 2 is built-up.

### The pooled model trained on all 3,626,753 pixels
**In plain words:** "Pooled" means pixels from all three years are mixed into one training set. One model is then used for every year.
**Everyday analogy:** One marking scheme for all three years' exam papers. If each year had its own scheme, the grades would not be comparable.
**In this project:** The training set is 3,626,753 valid pixels. It is a bit under 3 × 1,209,178 because pixels without a clear view are left out. Because the same trained model is used for 2015, 2020 and 2025, cluster 2 means the same thing every year.
**If the teacher asks:** "One model trained on every pixel from all three years, so changes are real and not caused by different cluster definitions."

### Naming by nearest reference centre
**In plain words:** Each new cluster takes the name of the closest cluster from the first run, as measured in the six-band space.
**Everyday analogy:** A new student is put in the same house as the older student they most resemble.
**In this project:** The first-run clusters were named by hand from location and true-colour images. The final model's clusters were matched to them by nearest centre (`naming_reference_centres.npy`, `results2.py`). This keeps names consistent without re-naming by hand.
**If the teacher asks:** "We named the first run by hand and let each final cluster inherit the name of its nearest first-run cluster."

---

## Part E — Is the model good?

### Elbow method
**In plain words:** Run K-means for several values of k and plot inertia. It always falls as k rises. The "elbow" is where it stops falling steeply.
**Everyday analogy:** Adding spoons of sugar to tea: the first few change the taste a lot, later ones hardly matter.
**In this project:** k from 4 to 16 was tested on a sample. The elbow is at k = 8, and k = 7–10 all lie within about 10% of the best elbow value (`results/model_checks/model_checks.md`; chart `k_selection.png`). The inertia values in that sweep (for example 437.05 at k = 10) come from a 300,000-pixel sample, so they differ from the final model's 5243.

### Silhouette score
**In plain words:** For each pixel: how much closer is it to its own group than to the next-nearest group? Ranges from −1 to 1. Higher is clearer separation.
**Everyday analogy:** Do people in a party stand in clear clumps, or is it one blurry crowd?
**In this project:** Highest at k = 4 (0.386), then nearly flat (about 0.29–0.33) from k = 5 to 16. At k = 10 it is 0.299. Computed on a 20,000-pixel subsample.

### Davies–Bouldin index
**In plain words:** Compares how spread out each group is with how far apart groups are. Lower is better.
**Everyday analogy:** Neighbouring villages: small and far apart is good, big and overlapping is bad.
**In this project:** Best at k = 16 (0.932). Across k = 4–16 it only moves between about 0.93 and 1.00. k = 10: 0.937.

### Calinski–Harabasz index
**In plain words:** The ratio of between-group spread to within-group spread. Higher is better. It is unbounded, so compare only across k on the same data.
**Everyday analogy:** How much the heaps differ from each other compared with how much grains differ within a heap.
**In this project:** Highest at k = 4 (42,148) and falling gently to 32,147 at k = 16. At k = 10 it is 35,404.

### Seed stability and adjusted Rand index (ARI)
**In plain words:** Seed stability asks whether a different random start gives the same result. ARI scores how similar two groupings are: 1.0 means identical (up to renumbering), about 0 means random.
**Everyday analogy:** Two examiners marking the same papers: do they sort them into the same piles?
**In this project:** Three runs on all pixels had ARI 0.95–0.97 between them (0.9491, 0.9656, 0.9549). Built-up area across them was 7,844–7,920 ha (2015), 10,033–10,104 ha (2020) and 14,737–14,841 ha (2025), all within 1%.
**If the teacher asks:** "Retraining three times gave the same map within 1% for built-up area."

### Why the 300k-sample model was replaced
**In plain words:** The first model was trained on 100,000 random pixels per year (300,000 total). That sample was too small to give a stable answer.
**Everyday analogy:** Judging a city by 300 people you happened to stop on one street.
**In this project:** Re-training on other samples moved 2015 built-up between 6,698 and 8,177 ha (CV 7.8%) and ARI against the first model fell to 0.52–0.92 (`results/model_checks/model_checks.md`). The final model uses all pixels. The old numbers (6,609 → 14,529 ha, +120%) are superseded: do not quote them.
**If the teacher asks:** "The first model was unstable, so we retrained on every pixel and checked three seeds."

---

## Part F — Measuring change

### Area from pixel counts
**In plain words:** Count pixels of a class and multiply by the area of one pixel.
**Everyday analogy:** Counting floor tiles to get the floor area.
**In this project:** Hectares = pixel count × 0.09 (`results2.py`). Built-up: 7,844 ha (2015), 10,033 ha (2020), 14,786 ha (2025). In QGIS, use "Raster layer unique values report" (ha = m² ÷ 10,000).

### Post-classification change detection
**In plain words:** Classify each year separately, then compare the finished maps.
**Everyday analogy:** Comparing two finished jigsaws instead of comparing the loose pieces.
**In this project:** The three `lulc_YEAR.tif` maps, made by the same model, are compared pixel by pixel. A weakness: any map error becomes a "change" (see classification noise below).

### From–to (transition) matrix
**In plain words:** A table with last year's class down the side and this year's class across the top. Each cell is the area that moved from one to the other.
**Everyday analogy:** Where each student sat last term versus this term.
**In this project:** In 2015→2025, 10,170 ha became built-up. Of this, 6,916 ha (68%) was cropland in 2015, 1,960 ha was bare/fallow and 1,294 ha was trees (`results.json`, `from_to`). In QGIS, the Raster Calculator code `2015 × 10 + 2025` gives two-digit codes (21 = cropland → built-up).
**If the teacher asks:** "Cropland supplied 6,916 ha, or 68%, of the new built-up land."

### "Built-up to cropland" as classification noise
**In plain words:** Built-up land almost never turns back into farmland. If the map says so, it is probably a mapping error.
**Everyday analogy:** A house reappearing as a wheat field overnight: you would suspect the photo, not the field.
**In this project:** 3,225 ha were built-up in 2015 but not in 2025 (1,310 ha to cropland, 1,576 ha to trees, 339 ha to bare).
**If the teacher asks:** "About 3,200 ha went the 'wrong' way, which shows our maps have noise."

### Built-up share
**In plain words:** Built-up area as a percentage of the whole study area.
**Everyday analogy:** The slice of the pizza covered by one topping.
**In this project:** 7.2% (2015), 9.2% (2020), 13.6% (2025) (`results/README.md`).

### Yearly growth rate (SDG 11.3.1 land-consumption-rate formula)
**In plain words:** One steady yearly percentage that takes you from the first area to the second: ln(B2 ÷ B1) ÷ years × 100, where ln is the natural logarithm. It works like compound interest.
**Everyday analogy:** The yearly interest rate that grows a bank deposit from A to B.
**In this project:** 4.92% a year (2015–2020), 7.76% (2020–2025), 6.34% (2015–2025). **Precision on SDG 11.3.1:** the official indicator is the *ratio of land consumption rate to population growth rate*. This project computes only the land-consumption part, using the same formula. There is no census for 2015–2025 to supply the population part. So say "calculated with the SDG 11.3.1 formula", not "the SDG 11.3.1 value". Also, the UN measures all urban land, while we count only built-up pixels (`05_metrics_and_formulas.md`).
**If the teacher asks:** "We computed the land-consumption half of SDG 11.3.1; the population half needs census data we do not have."

### UEII and its intensity bands
**In plain words:** The Urban Expansion Intensity Index: new built-up land per year as a percentage of the zone's total area: (later − earlier) ÷ (zone ha × years) × 100. It lets big and small zones be compared fairly.
**Everyday analogy:** Converting marks out of 50 and out of 100 into percentages before comparing.
**In this project:** West 0.69 ("medium"), East 0.54 ("low"), whole area 0.64. The bands used (below 0.28 slow, 0.28–0.59 low, 0.59–1.05 medium, 1.05–1.92 high, above 1.92 very high) are a convention from published studies, not a rule (`05_metrics_and_formulas.md`).
**If the teacher asks:** "UEII shows the West grew faster relative to its size than the East, and the speed bands are a convention."

---

## Part G — Checking accuracy

### Reference data
**In plain words:** Trusted information about what is really on the ground, used to test the map.
**Everyday analogy:** The answer key.
**In this project:** The reference is detailed Esri World Imagery photos at 158 check points. **Disclosure:** the photo labels were AI-assisted: two independent raters labelled each point without seeing the map, they agreed on 144 of 160 points, and a third look settled the 16 disagreements. The students should spot-check a sample of them. Files: `results/validation/`.

### Stratified random sampling (50/50/30/30)
**In plain words:** Divide the map into its classes (strata), then pick random points inside each class. This ensures rare classes get enough points.
**Everyday analogy:** Polling equal numbers from small and big villages so small ones are not ignored, then weighting the answers back.
**In this project:** 50 built-up, 50 cropland, 30 trees and 30 bare/fallow points, 160 in all, drawn from the first-run 2025 map (`make_chips.py`). Two points under cloud were dropped, leaving 158.
**If the teacher asks:** "160 random points, 50/50/30/30 by class; two were cloudy, so we used 158."

### Blind interpretation
**In plain words:** Labelling the photos without knowing what the map says, so the map cannot bias the answer.
**Everyday analogy:** Marking an exam with the student's name covered.
**In this project:** The point order was shuffled and the map class was hidden (`.map_key_do_not_open.csv`). Each photo is about 300 m across with the 30 m pixel outlined.

### Confusion matrix
**In plain words:** A table of map class (rows) against true class (columns). The diagonal is correct points.
**Everyday analogy:** A seating chart showing who sat where against who should have.
**In this project:** Rows = map, columns = photo (`results/README.md`): built-up row 30, 8, 5, 5; cropland row 4, 47, 6, 3; trees row 8, 8, 20, 0; bare row 7, 2, 0, 5.

### Overall accuracy
**In plain words:** The share of points where map and truth agree.
**Everyday analogy:** The exam percentage.
**In this project:** 74.6% (area-weighted) for four classes, and 87.0% for built-up versus not. Counting the matrix diagonal without weights gives 102 of 158 (about 65%). The reported 74.6% differs because points are weighted by class area (next-but-two entry).

### User's and producer's accuracy (commission and omission)
**In plain words:** User's accuracy: of the pixels the map calls X, how many truly are X (errors of commission). Producer's accuracy: of the truly X places, how many did the map find (errors of omission).
**Everyday analogy:** A fishing net for trout. User's accuracy: of the fish in the net, how many are trout. Producer's accuracy: of all trout in the lake, how many did the net catch.
**In this project:** Built-up: user's 62.0%, producer's 51.9%. Cropland 84.3% / 87.1%. Trees 61.8% / 68.7%. Bare/fallow 35.7% / 27.8%.
**If the teacher asks:** "Built-up: 62% of what we map is real, and we find 52% of what is real."

### Area-weighted accuracy and error-adjusted area (Olofsson et al. 2014)
**In plain words:** Olofsson et al. (2014) is the standard guide. Because classes were sampled unequally, each point must be weighted by how much of the map its class covers. The reference labels are then used to correct area estimates, with a 95% confidence interval.
**Everyday analogy:** Counting votes by district population, not by how many pollsters visited each.
**In this project:** `accuracy.py` implements this. Corrected built-up for 2025: **17,706 ± 4,648 ha**, against 14,786 ha on the map. The range is 13,058 to 22,354 ha, which still contains the map figure, so be honest that the interval is wide. The best estimate is higher than the map.
**If the teacher asks:** "The corrected estimate is 17,706 ha plus or minus 4,648; the interval is wide because we had only 158 points."

### Why the map undercounts built-up
**In plain words:** Producer's accuracy (51.9%) is lower than user's accuracy (62.0%): the map misses more real built-up than it wrongly adds.
**Everyday analogy:** A net with big holes: what it catches is mostly right, but many fish escape.
**In this project:** Small villages, roads and houses under trees fall below the 30 m scale or look like other classes. ESA WorldCover finds more built-up too. So hectares are conservative. The trend, the speed-up after 2020 and the West-versus-East pattern are the reliable findings.
**If the teacher asks:** "The true built-up area is probably larger than ours, so our growth figures are conservative."

### Independent comparison with ESA WorldCover 2020
**In plain words:** ESA WorldCover is a free, independent 10 m land-cover map made with Sentinel satellite data (CC BY 4.0). Comparing against it gives a second opinion with no human labelling.
**Everyday analogy:** Asking a second surveyor.
**In this project:** Each 30 m pixel covers nine WorldCover 10 m pixels; it counts as built-up in WorldCover if at least half are (class 50). Result for 2020: 92.8% agreement on built-up versus not. 70.9% of our built-up pixels are built-up in WorldCover; we find 59.1% of WorldCover's. WorldCover finds 12,181 ha built-up, against our 10,033 ha (`worldcover_check.py`).
**If the teacher asks:** "WorldCover agrees on 93% of pixels and shows the same undercount."

---

## Part H — Sharing the map

### Basemap
**In plain words:** The background map under your own layers.
**Everyday analogy:** Tracing paper laid on a printed street map.
**In this project:** OpenStreetMap by default, with an optional Esri satellite background (free to view, not open data). Credit "© OpenStreetMap contributors".

### Map tiles
**In plain words:** The web map is cut into small square pictures at many zoom levels, and the browser loads only the ones in view.
**Everyday analogy:** An atlas where you pull out only the pages you need.
**In this project:** The basemaps are tile services. Our own layers are single PNGs per year (`webmap/layers/lulc_YEAR.png`).

### Leaflet
**In plain words:** A free JavaScript library that draws interactive maps in a web page.
**Everyday analogy:** A map frame you hang on your wall and put your own pictures in.
**In this project:** Leaflet 1.9.4 (BSD-2-Clause). qgis2web also exports Leaflet; the dashboard here is custom-built (`scripts/webmap/template.html`).

### GeoJSON
**In plain words:** A text format for vector shapes and their attributes.
**Everyday analogy:** A shopping list written so every shop has an address.
**In this project:** `webmap/data/hex.geojson` stores each hexagon with its land-cover hectares for every year, plus a W/E zone label. The zone polygons themselves are not published, because of the GADM licence.

### The 1 km² hexagon grid
**In plain words:** The area is covered with hexagons, each exactly 1 km², and statistics are totalled per hexagon.
**Everyday analogy:** A honeycomb: fair, equal cells, no skinny corners.
**In this project:** Built by `build_webmap.py` from the 30 m UTM rasters. It powers the colouring by growth, share, farmland built over and UEII.

### Static website and GitHub Pages
**In plain words:** A static site is just files with no server code. GitHub Pages serves such files free from a repository branch.
**Everyday analogy:** A printed poster on a public notice board, rather than a staffed counter.
**In this project:** The `gh-pages` branch holds `index.html`, `layers/*.png` and `.nojekyll`. Site: https://sharmaabhimanyueco.github.io/Supriyaaanya/. The user turns Pages on in Settings → Pages. Locally, use `python -m http.server`, since browsers block `file://` fetches.

### Search: Wikidata places and Photon
**In plain words:** Search finds a town and flies the map there.
**Everyday analogy:** A built-in phone book, plus a call to directory enquiries if the name is not in it.
**In this project:** A built-in list of places from Wikidata (CC0), and Photon (photon.komoot.io, using OpenStreetMap data) for anything else when online. Photon works only on the hosted site.

### Open licences and data terms
**In plain words:** A licence says what others may do with data, and what credit they owe.
**Everyday analogy:** The rules on a photocopier sticker.
**In this project:** (`LICENSE-DATA.md`)
- **Our code:** MIT. **Our maps, rasters, figures and slides:** CC BY 4.0. Credit the authors.
- **Landsat:** US public domain; USGS asks only for a credit line.
- **ESA WorldCover:** CC BY 4.0. Used for the accuracy check only.
- **Wikidata places:** CC0.
- **OpenStreetMap (basemap and Photon):** ODbL. Credit "© OpenStreetMap contributors".
- **Esri World Imagery:** free to view, not open data. Chips are not redistributed.
- **GADM boundary:** no redistribution. Not in the repo, and the zone polygons are not on the web page.
**If the teacher asks:** "Our outputs are CC BY 4.0, and we left out GADM and Esri files because their terms forbid sharing."

---

## Part I — QGIS equivalents

The teacher asked for QGIS. The results came from Python. This table maps each step to the tool named in `04_qgis_steps.md`.

| Python step | QGIS tool or plugin | Notes |
|---|---|---|
| Get scenes, mask clouds, median composite (`build_composites.py`) | Earth Engine script from `03_get_satellite_images.md`, or USGS EarthExplorer | The QGIS guide starts from finished composites. |
| Boundary to one outline in metres | Dissolve, then Reproject Layer to EPSG:32643 | Save as `study_area_32643.gpkg`. |
| Clip to study area (`inside.npy`) | Clip raster by mask layer (GDAL), nodata −32768 | Run as a batch for all years. |
| K-means (`train_full.py`) | SCP, Band processing, Clustering, K-means, 10 classes; or GRASS i.cluster + i.maxlik | Guide clusters each year separately; the Python run used one pooled model. |
| Name clusters | Identify Features, Esri World Imagery XYZ tiles, Google Earth Pro historical imagery | Name each year separately. |
| Merge to classes (`results2.py`) | Reclassify by table | Same class codes every year. |
| Area (pixels × 0.09) | Raster layer unique values report | ha = m² ÷ 10,000. |
| New built-up, cropland to built-up, from–to | Raster Calculator | Code `2015 × 10 + 2025`. |
| Growth by zone, UEII | Zonal histogram | Zones are West/East, not tehsils. |
| Web map (`build_webmap.py`) | Polygonize, Extract by attribute, Simplify (about 15 m), then qgis2web (Leaflet) | Publish with GitHub Pages. |
| Colours | Save Style / Load Style | Same colours as the slides. |

The QGIS guide uses five classes including water (empty in our run), so QGIS results will not match the Python numbers exactly.
**If the teacher asks:** "Every step has a QGIS equivalent, and the guide in the repo walks through it."

---

## Part J — Limits to say out loud

### Mixed pixels at 30 m
**In plain words:** One pixel can hold fields, houses and trees together, and gets a single average signature.
**Everyday analogy:** Blending a fruit salad: you cannot tell what was in it.
**In this project:** Small settlements are hard to separate, one reason for the undercount.

### Bare/fallow vs built-up confusion
**In plain words:** Dry bare soil and bright roofs reflect light similarly.
**Everyday analogy:** A sandy floor and a concrete floor look alike from far away.
**In this project:** Bare/fallow is the weakest class (user's 35.7%, producer's 27.8%), and 7 of 14 mapped bare points were really built-up.

### Trees vs crops
**In plain words:** Green crops and trees can look alike, depending on crop stage.
**Everyday analogy:** Two shades of green paint under poor light.
**In this project:** Trees: user's 61.8%, producer's 68.7%. Of the 36 points mapped as trees, 8 were cropland in the photos.

### Seasonal effects
**In plain words:** The ground changes through the year, and also between years.
**Everyday analogy:** A school photo of a garden in spring and in autumn.
**In this project:** Same month every year helps, but crops were at slightly different stages in each March, so some cropland shows as trees or bare land.

### Boundary issues
**In plain words:** The study area is only as good as its boundary file.
**Everyday analogy:** Measuring a field from an old, mislabelled plot map.
**In this project:** The GADM boundary may be out of date and its labels are wrong. West and East are not tehsils. The area (108,799 ha from pixel counts; slide notes recommend checking against an official figure) is not yet confirmed.

### AI-assisted labels
**In plain words:** The photo labels for the accuracy check were made by AI-assisted interpretation, not by field survey or the students.
**Everyday analogy:** An answer key written by assistants, not by the examiner.
**In this project:** Two independent blind raters, with the 16 disagreements settled by a third look. The students should spot-check a sample, and say this openly.
**If the teacher asks:** "The labels were AI-assisted; we spot-checked a sample and we say so openly."

### Hectares are conservative
**In plain words:** Map totals are probably too low.
**Everyday analogy:** A tally that misses some items is a minimum, not an exact count.
**In this project:** Built-up in 2025: map 14,786 ha, corrected estimate 17,706 ± 4,648 ha. Not covered: zoning permits (GMADA/PUDA) and census population for 2015–2025.
**If the teacher asks:** "Our hectares are conservative; the trend is the reliable finding."

---

## Sources

Project files: `CLAUDE.md`, `results/README.md`, `results/results.json`, `05_metrics_and_formulas.md`, `04_qgis_steps.md`, `03_get_satellite_images.md`, `01_message_to_teacher.md`, `02_teacher_brief_and_slide_list.md`, `results/model_checks/model_checks.md`, `webmap/README.md`, `LICENSE-DATA.md`, and the scripts in `scripts/analysis/` and `scripts/webmap/`.

External pages relied on (via search results; direct page fetches were blocked, so wording was not read in full):
- USGS, scale factor FAQ (0.0000275, −0.2): https://www.usgs.gov/faqs/how-do-i-use-scale-factor-landsat-level-2-science-products
- USGS, Collection 2 quality assessment bands: https://www.usgs.gov/landsat-missions/landsat-collection-2-quality-assessment-bands
- USGS, Landsat 8 (launch 11 Feb 2013, 16-day repeat, 185 km swath, 30 m): https://www.usgs.gov/landsat-missions/landsat-8
- NASA Landsat 8: https://landsat.gsfc.nasa.gov/satellites/landsat-8/ and band list https://landsat.gsfc.nasa.gov/satellites/landsat-9/landsat-9-instruments/landsat-9-spectral-specifications
- USGS, restrictions on Landsat data: https://www.usgs.gov/faqs/are-there-any-restrictions-use-or-redistribution-landsat-data
- USGS, NDVI: https://www.usgs.gov/landsat-missions/landsat-normalized-difference-vegetation-index
- EPSG:32643: https://spatialreference.org/ref/epsg/32643/ ; EPSG:3857: https://epsg.io/3857
- Esri, Mercator and area distortion: https://pro.arcgis.com/en/pro-app/latest/help/mapping/properties/mercator.htm
- UN SDG 11.3.1 metadata: https://unstats.un.org/sdgs/metadata/files/Metadata-11-03-01.pdf ; UN-Habitat: https://unhabitat.org/sites/default/files/2020/07/metadata_on_sdg_indicator_11.3.1.pdf
- ESA WorldCover v100 (class 50, CC BY 4.0): https://developers.google.com/earth-engine/datasets/catalog/ESA_WorldCover_v100 ; DOI 10.5281/zenodo.5571936
- scikit-learn KMeans: https://scikit-learn.org/stable/modules/generated/sklearn.cluster.KMeans.html
- scikit-learn clustering evaluation: https://scikit-learn.org/stable/modules/clustering.html#clustering-performance-evaluation
- Olofsson et al. (2014), https://doi.org/10.1016/j.rse.2014.02.015
- STAC and Planetary Computer: https://learn.microsoft.com/en-us/azure/planetary-computer/stac-overview and https://planetarycomputer.microsoft.com/api/stac/v1/collections/landsat-c2-l2
- GitHub Pages: https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site
