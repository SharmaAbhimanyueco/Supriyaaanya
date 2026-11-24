---
title: "Mapping Urban Growth in the Mohali–Kharar–Zirakpur–Dera Bassi Belt, Punjab, using LULC Analysis"
subtitle: "Master document: everything from A to Z, what was done, how, and why"
author: "Supriya Mahshere and Aanya Upadhyay"
date: "Handover version, 25 November 2026"
---

This document explains the whole project in one place: the geospatial ideas behind it, every step of the method and the reason for each choice, the results, how good they are, where the code ran and how to run it again, and how to answer the teacher's questions. Every number in it comes from `04_Data/results.json`, the single file that holds all final figures. Nothing here was typed in by hand from memory.

**Contents**

- Part 0 — How to use this package
- Part 1 — The project on one page
- Part 2 — Geospatial concepts in plain words
- Part 3 — The study area
- Part 4 — The data, and why it was chosen
- Part 5 — The method, step by step, with the reason for each choice
- Part 6 — Is the model suitable and properly trained?
- Part 7 — Results
- Part 8 — How accurate is the map?
- Part 9 — The web map
- Part 10 — Limitations
- Part 11 — Decisions log
- Part 12 — Where the code ran, and how to run it again
- Part 13 — Teacher prep: questions, demos and screenshots
- Part 14 — Glossary
- Part 15 — References and sources
- Part 16 — File inventory

```{=openxml}
<w:p><w:r><w:br w:type="page"/></w:r></w:p>
```

# Part 0 — How to use this package

The package holds everything the project produced: the slides, every map and chart, all the data, all the code, the web map, and preparation notes for the teacher's questions. Nothing in it needs the internet except the live web map and re-downloading the satellite images.

| Folder | What is inside | When you need it |
|----------------------|--------------------------------------------------|----------------------------|
| `00_READ_ME_FIRST.md` | One-page guide to the package | First |
| `01_Master_Document/` | This document (Word and PDF) | To understand everything |
| `02_Presentation/` | The 24-slide deck (PowerPoint and PDF), every slide as a picture, and the slide text with speaker notes | To present, or to build your own deck |
| `03_Maps_and_Charts/` | Final maps, charts, ready-made web map screenshots, and the superseded first-run maps (archive) | To paste into slides or a report |
| `04_Data/` | `results.json`, 16 CSV tables, the land-cover and cluster maps (GeoTIFF with QGIS styles), the Landsat composites, the accuracy-check data with photo chips, model checks, and the study-area boundary | To check a number, open the maps in QGIS, or answer "show me" |
| `05_Code/` | Every script, where it ran, how to run it, and two quick demo scripts | If asked to run something |
| `06_Web_Map/` | The dashboard as files, one-click launchers that work offline, and the live link | To show the web map, with or without internet |
| `07_Teacher_Prep/` | Questions and answers, demo scripts, the screenshot checklist and a numbers cheat sheet | The night before and on the day |
| `08_Project_Notes/` | The planning notes: message to the teacher, her brief, the image guide, QGIS steps and formulas | Background and the QGIS route |

**If you only have 15 minutes:** read Part 1 of this document, then sections 0–2 of `07_Teacher_Prep/Teacher_QA_and_Demo` (numbers cheat sheet, 60-second story, three disclosures). Then start the offline web map once (`06_Web_Map/run_local_windows.bat` or `run_local_mac_linux.sh`) to be sure it works on your laptop.

**Private material.** Two things in the package must not be published or uploaded to a public site: the study-area boundary (`04_Data/study_area/`, GADM licence) and the photo chips (`04_Data/validation/chips/` and `sheets/`, Esri imagery terms). Everything else is open: the code is under the MIT licence and the maps and figures under CC BY 4.0 (`LICENSE`, `LICENSE-DATA.md`).

# Part 1 — The project on one page

**Question.** How much, how fast and where did the Mohali–Kharar–Zirakpur–Dera Bassi belt urbanise between 2015 and 2025? Urbanisation is the theme. The loss of farmland is a supporting finding.

**Where.** S.A.S. Nagar (Mohali) district, Punjab, next to Chandigarh: about 108,800 ha (1,088 km²) covering Mohali, Kharar, Zirakpur and Dera Bassi.

**Data.** Landsat 8 satellite images from March 2015, 2020 and 2025, at 30 m resolution. Two clear scenes were used per year, merged into one cloud-free picture.

**Method.** The satellite pictures were sorted into 10 groups of similar pixels with K-means, an unsupervised clustering method. One model was trained on all 3,626,753 pixels of the three years together, so each group means the same thing in every year. The groups were then named and merged into four land types: Built-up, Cropland, Trees/vegetation and Bare/fallow. Areas, change, growth rates and zone comparisons were computed from the maps. The 2025 map was checked against 158 photo-checked points.

**Headline results**

| Measure | Value |
|----------------------------|------------------------------------------------------------------------|
| Built-up land | 7,844 ha (2015) → 10,033 ha (2020) → 14,786 ha (2025) |
| Growth 2015–2025 | +6,942 ha (+88.5%), 694 ha a year |
| Yearly growth rate (SDG 11.3.1 formula) | 6.34% a year overall; 4.92% in 2015–2020, rising to 7.76% in 2020–2025 |
| Built-up share of the area | 7.2% → 9.2% → 13.6% |
| Where | West zone (Kharar–Mohali) grew faster: UEII 0.69 (medium) against 0.54 (low) for the East zone (Dera Bassi–Zirakpur) |
| Farmland | 6,916 ha of 2015 cropland became built-up: 68% of the 10,170 ha of new built-up land |
| Accuracy (2025 map) | 74.6% overall (four land types); 87.0% for built-up versus not built-up |
| Undercount | The map finds about half of the real built-up land (producer's accuracy 51.9%). The corrected 2025 estimate is 17,706 ± 4,648 ha, against 14,786 ha on the map |
| Independent check | 92.8% agreement with ESA WorldCover 2020 on built-up versus not |

**The reliable findings** are the direction and size of the trend: built-up land almost doubled, growth sped up after 2020, and the West zone grew faster than the East. The exact hectares are conservative estimates, because the map misses many small villages, roads and houses under trees.

**Three things to say openly, before anyone asks**

1. **The analysis ran in Python, not QGIS.** The teacher asked for QGIS. Every output opens in QGIS with ready-made styles, and the QGIS route is written out in `08_Project_Notes/04_qgis_steps.md`.
2. **The photo labels in the accuracy check were AI-assisted.** Two independent AI raters labelled each photo without seeing the map, and a third look settled their disagreements. You should spot-check a sample of them yourselves.
3. **The hectares are conservative.** The accuracy check shows the map undercounts built-up land.

**Still waiting for the teacher (UNCONFIRMED).** Her answers to the questions in `08_Project_Notes/01_message_to_teacher.md` have not arrived. Those questions cover the satellite and years, K-means or ISODATA, how much validation she wants, the web map tool, the deadline and format, and the missing slide 16 in her list. The work uses sensible working choices for each, explained in Part 11.

```{=openxml}
<w:p><w:r><w:br w:type="page"/></w:r></w:p>
```


# Part 2 — Geospatial concepts in plain words


How to use this chapter. Each concept has up to four lines: what it means, an everyday picture, exactly what this project did (with the real numbers and the file where you can see them), and one sentence you can say aloud if the teacher asks. Every number comes from `results/results.json`, `results/README.md` or the scripts in `scripts/analysis/`. Where something is still waiting on the teacher it says **UNCONFIRMED**.

---

## A — Maps and data basics

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

## B — Where on Earth

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

## C — Satellites and images

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

## D — From image to land-cover map

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

## E — Is the model good?

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

## F — Measuring change

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

## G — Checking accuracy

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

## H — Sharing the map

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

## I — QGIS equivalents

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

## J — Limits to say out loud

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


```{=openxml}
<w:p><w:r><w:br w:type="page"/></w:r></w:p>
```

# Part 3 — The study area

**What it is.** The study area is S.A.S. Nagar (Mohali) district in Punjab, next to Chandigarh. It contains the four growing towns in the project title: Mohali, Kharar, Zirakpur and Dera Bassi. One district holds all four towns, so the results can feed district-level planning.

![Location map of the study area (from the project's own files; basemap © OpenStreetMap contributors). The "Kharar" and "Rajpura" labels on it are wrong; see below.](03_Maps_and_Charts/maps/location_map.jpg){width=5.6in}

**Where the boundary comes from.** The outline is the file `Study_Area.zip` (in `04_Data/study_area/`). It comes from GADM, a free worldwide database of administrative boundaries. It has two polygons, and their labels are wrong:

| Label in the file | What it really covers | Used in this project as | Area |
|------------------|---------------------------------------------|----------------------|---------------|
| "Kharar" | Kharar and Mohali | **West zone** | 71,195 ha |
| "Rajpura" | Dera Bassi, including Zirakpur. Rajpura town itself is outside the study area, in Patiala district | **East zone** | 37,604 ha |

Because of this, the project never calls the pieces "tehsils". They are the **West and East zones**. The labels must not be shown on any map. Before quoting areas "by tehsil", correct tehsil outlines from an official source would be needed. One place to check against an official map: Banur seems to fall just outside the line.

**How big it is.** Three slightly different area figures exist. All are correct for what they measure:

| Figure | What it measures |
|------------------------------|----------------------------------------------------------------------|
| 108,829 ha | The area of the polygon itself, measured in UTM zone 43N |
| 108,826 ha | The 1,209,178 pixels of 30 m whose centres fall inside the polygon (× 0.09 ha) |
| 108,799 ha (2015), 108,826 ha (2020), 108,783 ha (2025) | The pixels that were actually mapped in each year. A few pixels had no cloud-free view in a year and were left out: 303 in 2015, 478 in 2025, none in 2020 |

**Licence.** GADM allows academic use but not redistribution without permission. The boundary is therefore kept out of the public code repository and out of the public web map. It is in this package only for the project team's own use.

# Part 4 — The data, and why it was chosen

## The satellite: Landsat 8

| Choice | What was used | Why |
|--------------|----------------------------------|----------------------------------------------------|
| Satellite | **Landsat 8** (NASA and the US Geological Survey), OLI sensor | Free, and the **same sensor for the whole period**, 2015–2025, so a pixel's values mean the same thing in every year. Sentinel-2 (10 m) has no images for March 2015, because its first satellite was launched in June 2015 |
| Product | **Collection 2 Level-2 surface reflectance** | Already corrected for the atmosphere, so images from different dates can be compared directly |
| Pixel size | 30 m × 30 m = 900 m² = **0.09 ha** | Fine enough to see towns and large fields; a common resolution for land-cover change studies over many years |
| Scene | WRS-2 **path 147, row 39** | One scene footprint covers the whole study area |
| Bands | Six: blue, green, red, near-infrared (NIR), shortwave-infrared 1 and 2 (SWIR1, SWIR2) | These separate plants, soil, water and buildings. The thermal bands were not needed |
| Season | **March** | Wheat is green then, so farmland and buildings look very different. Using the same month every year removes crop-season effects |
| Years | **2015, 2020, 2025** (UNCONFIRMED with the teacher) | Equal five-year steps across the Landsat 8 era, ending with the latest March |

## The scenes used

| Year | Scene 1 | Scene 2 |
|----------|---------------------------------------------|---------------------------------------------|
| 2015 | 7 March (LC08_L2SP_147039_20150307_02_T1) | 23 March (LC08_L2SP_147039_20150323_02_T1) |
| 2020 | 4 March (LC08_L2SP_147039_20200304_02_T1) | 20 March (LC08_L2SP_147039_20200320_02_T1) |
| 2025 | 2 March (LC08_L2SP_147039_20250302_02_T1) | 18 March (LC08_L2SP_147039_20250318_02_T1) |

The scene names can be read as: LC08 = Landsat 8, L2SP = Level-2 product, 147039 = path 147 row 39, then the date, collection 02, and T1 = Tier 1, the best-quality tier.

## Where the images came from: Microsoft Planetary Computer

The images were streamed from **Microsoft Planetary Computer**, which keeps a free public copy of the Landsat archive with a searchable catalogue (STAC). The script asks the catalogue for the six scenes by name and reads only the part of each image that covers the study area. Nothing had to be downloaded by hand.

**Why not the alternatives?** Google Earth Engine needs a sign-up, and the earlier version of this project, which the teacher rejected, was built on supervised classification in Earth Engine. A download-only Earth Engine script is still provided in `05_Code/gee/` as a backup route; it was not used. USGS EarthExplorer works too, but each scene is a large manual download.

## From two scenes to one clean picture per year

1. **Clouds out.** Each scene has a quality band, QA_PIXEL, which flags every pixel's problems bit by bit. A pixel was kept only if bits 0–4 are all zero: no fill, dilated cloud, cirrus, cloud or cloud shadow.
2. **Numbers to reflectance.** The stored numbers were converted to surface reflectance with the official scale and offset: reflectance = stored value × 0.0000275 − 0.2. Reflectance is the share of sunlight a surface sends back (0 = none, 1 = all).
3. **Median composite.** For every pixel and band, the middle value of the two scenes was kept. With two clear values, the median is simply their average; if one scene was cloudy at that pixel, the other one's value is used. This gives one six-band, cloud-free picture per year.
4. **Saved.** Each composite was saved as a GeoTIFF in reflectance × 10,000 (whole numbers), with −32768 marking "no data". These are `04_Data/landsat_composites/landsat_composite_YYYY.tif`, ready for QGIS.

![What the satellite saw: the March 2025 composite in true colour (red, green and blue bands), clipped to the study area. Landsat data courtesy of the US Geological Survey.](03_Maps_and_Charts/maps/landsat_true_colour_2025.png){width=4.2in}

# Part 5 — The method, step by step, with the reason for each choice

The teacher's procedure was: cluster each year's image into classes (unsupervised classification), name the classes, measure the area of each, make charts, interpret the change in hectares, and present it all on a web map. The project follows that procedure. The table gives the steps; the notes below it explain the choices.

| Step | What was done | Tool (script) | Output |
|--------------|--------------------------------------------|----------------------|--------------------|
| 1. Grid | Read the images on their own 30 m UTM zone 43N grid, in a window around the study area with a 300 m margin (1,409 × 2,170 pixels) | `build_composites.py` | Grid and study-area mask (`inside.npy`) |
| 2. Clean | Mask clouds, convert to reflectance, take the median of the two March scenes | `build_composites.py` | One composite per year |
| 3. Clip | Keep only pixels whose centre lies inside the study area (1,209,178 pixels) | `build_composites.py` | Mask applied to every map |
| 4. First run | K-means with 10 clusters on a 300,000-pixel sample; clusters named by location and colour | `cluster_pooled.py`, `results.py` | The naming reference and the first-run maps |
| 5. Final model | K-means with 10 clusters trained on **all** 3,626,753 pixels from the three years, best of 10 starts, three seeds | `train_full.py`, `results2.py` | The final model |
| 6. Name and merge | Clusters ordered by greenness (NDVI), each named after the nearest first-run cluster, then merged into four land types | `results2.py` | `clusters_YYYY.tif`, `lulc_YYYY.tif` |
| 7. Measure | Count pixels per land type × 0.09 ha | `results2.py` | Area table |
| 8. Change | Compare 2015 and 2025 pixel by pixel (from–to) | `results2.py`, `finalise.py` | Change map, from–to table |
| 9. Metrics | Built-up share, yearly growth rate, UEII per zone | `results2.py` | Zone table |
| 10. Check | Model checks; photo check of 160 random points; comparison with ESA WorldCover | `model_checks/`, `make_chips.py`, `accuracy.py`, `worldcover_check.py` | Parts 6 and 8 |
| 11. Share | Maps, charts, slides and the web map | `finalise.py`, `build_deck.js`, `build_webmap.py` | Everything in this package |

## Why each choice was made

**Why measure in UTM zone 43N (EPSG:32643)?** Area must be measured on a flat map in metres. In latitude and longitude, a "degree" is a different size on the ground in different directions, so pixel areas would be wrong. UTM zone 43N is the standard metric grid for this part of India, and it is the grid the Landsat scenes already use. So no resampling was needed, and every pixel is exactly 30 × 30 m.

**Why unsupervised classification (clustering)?** The teacher asked for it. The computer groups pixels with similar colours (similar reflectance in the six bands) without being told what anything is; people then name the groups. The earlier plan used supervised classification (training points and a Random Forest), and the teacher rejected it.

**Why K-means and not ISODATA?** Both are clustering methods. K-means is the most widely used, is well documented, and gives the same answer every time when its random seed is fixed. ISODATA can also split and merge clusters during the run, but it is not available in the Python library used (scikit-learn). Which one the teacher wants is UNCONFIRMED.

**Why 10 clusters for 4 land types?** Land types are not single colours. Cropland, for example, looks different at different crop stages and on different soils. Asking for more clusters than final classes lets the method split these shades apart; they are merged afterwards. The teacher's plan said 8–10 clusters. The model checks in Part 6 show that 10 sits in the sensible range.

**Why one model for all three years ("pooled")?** If each year is clustered separately, cluster 3 in 2015 and cluster 3 in 2025 can mean different things, and the comparison breaks. The first attempt did exactly that, and 2020 came out with more built-up land than 2025. Training one model on the pixels of all three years and applying it to each year means every cluster has the same meaning in every year.

**Why train on all pixels rather than a sample?** The first pooled model was trained on a 300,000-pixel sample. When it was retrained with other samples, the 2015 built-up area moved between 6,698 and 8,177 ha: too unstable. The final model uses all 3,626,753 pixels. Three training runs with different seeds then agree within 1% (Part 6).

**How were the clusters named?**

1. The 10 clusters were numbered from least green to most green by the NDVI of their centre, NDVI = (NIR − Red) ÷ (NIR + Red).
2. The first-run clusters had been named by people looking at where each cluster falls: town centres and roads (built-up), the northern hills (trees), fields (cropland), and bare or fallow ground. Their true colour was checked too.
3. Each final cluster took the name of the nearest first-run cluster, measured by distance between their centres in the six bands.

| Cluster | Land type |
|----------------------------------------|------------------------------------------------------------|
| 1 | Bare/fallow |
| 2 | **Built-up** |
| 3 and 5 | Trees/vegetation |
| 4, 6, 7, 8, 9 and 10 | Cropland |

**Why no water class?** No cluster picked out water. The water bodies in the area are too small to fill whole 30 m pixels, so they mix with their surroundings. Code 4 (Water) stays unused in the maps.

**Why these change measures?**

- **Area** = number of pixels × 0.09 ha.
- **Yearly growth rate** = ln(built-up later ÷ built-up earlier) ÷ years × 100. This is the land-consumption-rate formula used for SDG indicator 11.3.1. The official indicator is the ratio of this rate to the population growth rate. Population figures for 2015–2025 were not available, so only the land part is computed. The slides therefore say "calculated with the SDG 11.3.1 formula", not "the SDG 11.3.1 value".
- **UEII** (Urban Expansion Intensity Index) = new built-up ÷ (zone area × years) × 100. It makes zones of different sizes comparable, the way marks out of 50 and out of 100 are turned into percentages before comparing. Some studies label it slow (below 0.28), low (0.28–0.59), medium (0.59–1.05), high (1.05–1.92) or very high (above 1.92). These bands are a convention, not a rule.
- **From–to change** compares the 2015 and 2025 maps pixel by pixel, to see what new built-up land was before.

# Part 6 — Is the model suitable and properly trained?

**Training converged.** The three training runs on all pixels (seeds 0, 1 and 2, each the best of 10 starts) converged in 35, 31 and 29 iterations. Their final fit (inertia, the total squared distance of pixels to their cluster centre) was 5243.40, 5243.77 and 5243.46, which differ by less than 0.01%. Their groupings were very similar too: the adjusted Rand index between runs was 0.95–0.97, where 1 means identical.

**The answer is stable.** Built-up area across the three runs was 7,844–7,920 ha in 2015, 10,033–10,104 ha in 2020 and 14,737–14,841 ha in 2025, all within 1%. The run with the best fit, seed 0, was used for every map and number.

![Model stability: built-up area from repeated training runs.](03_Maps_and_Charts/charts/chart_07_stability.png){width=6.2in}

**The number of clusters is sensible.** Models with 4 to 16 clusters were compared on four standard scores:

- **Elbow of the inertia curve**: at k = 8, and k = 7–10 all score within about 10% of the best elbow value.
- **Silhouette** (how well each pixel fits its own cluster compared with the next one): highest at k = 4 (0.386), but nearly flat, 0.29–0.33, from 5 to 16 clusters.
- **Davies–Bouldin**: best at k = 16. **Calinski–Harabasz**: best at k = 4.

The scores do not agree on one best k, which is normal for land-cover data. Because clusters are merged into four land types afterwards, using more clusters than final types is standard practice, and k = 10 is within the sensible range.

![Choosing the number of clusters: the four scores for k = 4 to 16.](03_Maps_and_Charts/charts/chart_06_k_selection.png){width=6.2in}

**Why the earlier numbers changed.** An earlier version, trained on a 300,000-pixel sample, gave 6,609 → 14,529 ha (+120%). Retraining it with other samples moved the 2015 figure between 6,698 and 8,177 ha, so it was replaced by the full-data model. Do not use the earlier numbers. The sample-size test showed that sample size itself mattered little: 50,000, 100,000 and 200,000 pixels per year gave 14,756, 14,594 and 14,656 ha for 2025. The random seed mattered more, which is why the final model trains on everything.

# Part 7 — Results

## Area by land type

| Land type | 2015 (ha) | 2020 (ha) | 2025 (ha) |
|---|---|---|---|
| Built-up | 7,844 | 10,033 | 14,786 |
| Cropland | 81,218 | 77,204 | 66,728 |
| Trees/vegetation | 14,255 | 17,150 | 22,299 |
| Bare/fallow | 5,482 | 4,439 | 4,970 |
| Total mapped | 108,799 | 108,826 | 108,783 |
| Built-up share | 7.2% | 9.2% | 13.6% |

![Share of the study area in each land type.](03_Maps_and_Charts/charts/chart_02_landcover_by_year.png){width=6.2in}

## Built-up growth

| Period | Increase | Per year | % change | Yearly rate (SDG 11.3.1 formula) |
|---|---|---|---|---|
| 2015–2020 | +2,190 ha | 438 ha | +27.9% | 4.92% |
| 2020–2025 | +4,753 ha | 951 ha | +47.4% | 7.76% |
| 2015–2025 | +6,942 ha | 694 ha | +88.5% | 6.34% |

Growth more than doubled in speed after 2020: 438 ha a year in the first five years, 951 ha a year in the next five.

![Built-up land, 2015–2025.](03_Maps_and_Charts/charts/chart_01_builtup_trend.png){width=6.2in}

## The maps

![Land cover, March 2015.](03_Maps_and_Charts/maps/map_lulc_2015.png){width=3.3in}

![Land cover, March 2020.](03_Maps_and_Charts/maps/map_lulc_2020.png){width=3.3in}

![Land cover, March 2025.](03_Maps_and_Charts/maps/map_lulc_2025.png){width=3.3in}

![Built-up change, 2015 to 2025.](03_Maps_and_Charts/maps/map_change_2015_2025.png){width=3.3in}

## Where: the two zones

| Zone | Area (ha) | Built-up 2015 | 2020 | 2025 | Share 2015 → 2025 | UEII 2015–2025 | Yearly rate |
|---|---|---|---|---|---|---|---|
| West (Kharar and Mohali) | 71,195 | 4,336 | 6,151 | 9,236 | 6.1% → 13.0% | 0.69 (medium) | 7.6% |
| East (Dera Bassi, incl. Zirakpur) | 37,604 | 3,507 | 3,879 | 5,545 | 9.3% → 14.8% | 0.54 (low) | 4.6% |
| Whole study area | 108,799 | 7,844 | 10,033 | 14,786 | 7.2% → 13.6% | 0.64 | 6.3% |

The East zone was already more built-up in 2015, but the West zone added built-up land faster for its size. The zones are the two pieces of the boundary file, not official tehsils.

![West and East zones compared.](03_Maps_and_Charts/charts/chart_03_zones.png){width=6.2in}

## What the new built-up land used to be

Between 2015 and 2025, **10,170 ha** became built-up. Of this, **6,916 ha (68%) was cropland in 2015**, 1,960 ha (19%) was bare or fallow land, and 1,294 ha (13%) was trees or other vegetation.

![Where the new built-up land came from.](03_Maps_and_Charts/charts/chart_04_new_builtup_sources.png){width=6.2in}

In the other direction, 3,225 ha mapped as built-up in 2015 are not built-up in 2025. Built-up land rarely turns back into farmland, so this is mostly classification noise: pixels misread in one of the two years. It is a reminder that the maps contain errors (Part 8).

**Full from–to table, 2015 (rows) to 2025 (columns), hectares**

| 2015 \\ 2025 | Built-up | Cropland | Trees/vegetation | Bare/fallow |
|---|---|---|---|---|
| Built-up | 4,612 | 1,310 | 1,576 | 339 |
| Cropland | 6,916 | 61,669 | 9,219 | 3,388 |
| Trees/vegetation | 1,294 | 1,867 | 10,870 | 218 |
| Bare/fallow | 1,960 | 1,869 | 629 | 1,021 |

# Part 8 — How accurate is the map?

## How the check was done

1. **Random points.** 160 points were drawn at random from the 2025 map, stratified by map class: 50 built-up, 50 cropland, 30 trees and 30 bare. "Stratified" means a fixed number per class, so that small classes still get enough points. The strata came from the first-run 2025 map, and the random seed (2025) is fixed, so the same points can be drawn again.
2. **Photos.** For each point, a photo about 300 m across was cut from Esri World Imagery (high-resolution aerial and satellite photos), with the 30 m pixel marked in the middle.
3. **Blind labelling.** Two independent AI raters labelled every photo as Built-up, Cropland, Trees/vegetation, Bare or Unclear, **without seeing the map**. They agreed on 144 of 160 points (90%), and on 152 of 160 (95%) for built-up versus not. The 16 disagreements were settled by a third look. Two points were under cloud and were dropped, leaving 158.
4. **Area weighting.** The map's classes cover very different areas, and the sample took more points from small classes. So each point was weighted by the share of the map its class covers, following the standard good-practice method of Olofsson et al. (2014). The same method gives an **error-adjusted area** with a 95% range.

![Examples of the photo check: each chip shows one sample point with its 30 m pixel marked.](03_Maps_and_Charts/maps/validation_examples.png){width=6.2in}

## Results

| Measure | Result |
|----------------------------------------------------------------------|------------------------------|
| Overall accuracy (4 land types) | **74.6%** |
| Built-up versus not built-up | **87.0%** |
| Built-up: of map built-up, % really built-up (user's accuracy) | 62.0% |
| Built-up: of real built-up, % the map found (producer's accuracy) | 51.9% |
| Cropland (user's / producer's) | 84.3% / 87.1% |
| Trees/vegetation (user's / producer's) | 61.8% / 68.7% |
| Bare/fallow (user's / producer's) | 35.7% / 27.8% |
| Error-adjusted built-up area, 2025 (95% range) | **17,706 ± 4,648 ha** (map: 14,786 ha) |

![User's and producer's accuracy by land type.](03_Maps_and_Charts/charts/chart_05_accuracy_by_class.png){width=6.2in}

**Point counts** (rows = what the map says, columns = what the photo shows):

| Map \\ Photo | Built-up | Cropland | Trees | Bare |
|---|---|---|---|---|
| Built-up | 30 | 8 | 5 | 5 |
| Cropland | 4 | 47 | 6 | 3 |
| Trees/vegetation | 8 | 8 | 20 | 0 |
| Bare/fallow | 7 | 2 | 0 | 5 |

Counting the diagonal without weights gives 102 of 158 points (64.6%). The reported 74.6% is higher because cropland, which the map gets right most often, covers most of the area.

## What the numbers mean

- **The map undercounts built-up land.** It finds only about half of the real built-up land (producer's accuracy 51.9%). The missed built-up land is mostly small villages, roads, and houses under trees: at 30 m they mix with fields and trees around them. The corrected estimate for 2025 is 17,706 ha, with a 95% range of 13,058 to 22,354 ha. The range is wide and still contains the map figure, but the best estimate is clearly higher.
- **The trend is reliable.** The same method was applied to all three years, so the same kind of undercount affects every year. The growth direction, the speed-up after 2020 and the West–East pattern hold up. Treat the exact hectares as conservative estimates.
- **Bare/fallow is the weakest class.** Bare fields and bright roofs look alike to the satellite, so these two classes get mixed up.

![The 2025 map count against the corrected estimate.](03_Maps_and_Charts/charts/chart_08_builtup_error_adjusted.png){width=6.2in}

## An independent second opinion: ESA WorldCover

ESA WorldCover is a global land-cover map at 10 m made by the European Space Agency. Its 2020 map was compared with the project's 2020 map, built-up versus not:

- They agree on **92.8%** of the area.
- 70.9% of the project's built-up pixels are built-up in WorldCover, and the project finds 59.1% of WorldCover's built-up land.
- The project's built-up pixels are on average 69% built-up in WorldCover, against 5% for all other pixels.
- WorldCover finds **12,181 ha** built-up in 2020, against the project's **10,033 ha**: the same undercount the photo check shows.

## Honest caveats about the check itself

- The photo labels are AI-assisted. The two raters worked independently and blind, and their agreement was high, but you should spot-check a sample (for example 10–15 chips in `04_Data/validation/chips/` against `reference_labels.csv`).
- Esri World Imagery is a mosaic of photos taken on different dates. A change between a photo's date and March 2025 would count as a map error.
- 158 points give an overall picture, not exact figures for small classes. That is why the bare/fallow figures are uncertain.


```{=openxml}
<w:p><w:r><w:br w:type="page"/></w:r></w:p>
```

# Part 9 — The web map

**What it is.** An interactive dashboard that anyone can open in a browser, free, with no login: **https://sharmaabhimanyueco.github.io/Supriyaaanya/**. The teacher called the web map the end goal of the project.

![The dashboard, 2025 view (screenshot taken offline, so the background map is missing; online it shows streets and place names underneath).](03_Maps_and_Charts/screenshots/webmap_01_overview_2025.png){width=6.2in}

**What it does**

- **Search** towns and villages from a built-in list (Wikidata), or any other place through an online search when connected. The map flies there and shows the built-up land within 0.5–3 km for each year. Links can be shared, for example `…/#kharar`.
- **Filter** by year (2015, 2020, 2025), by land type and by zone (West or East). It can also show only land that became built-up, either all of it or farmland only. A play button animates 2015 → 2025.
- **1 km² hexagon grid** coloured by built-up growth, built-up share, farmland built over, or growth intensity (UEII), with a slider to hide small values.
- **Live figures** for whatever is on screen, a ranking of the fastest-growing places, and click-anywhere profiles showing what each 30 m square was in each year.

**How it was built.** The script `05_Code/webmap/build_webmap.py` turns the final land-cover maps into three PNG picture layers in Web Mercator, the projection web maps use. It builds the hexagon grid with hectares per land type for each year (computed on the 30 m UTM maps, so the areas are correct), and the list of places. The page uses Leaflet, a free open-source map library. All filtering and counting happens in the visitor's browser: the page decodes the picture layers back into land-type codes. There is no server code, database or API key.

**Why not qgis2web?** The teacher's plan named qgis2web (UNCONFIRMED). qgis2web exports a QGIS project as a simple map with layers and pop-ups. A custom Leaflet page was chosen to add the search, filters, live hectare figures and rankings described above, all computed from the land-cover data in the browser. Say so openly if asked.

**Hosting.** GitHub Pages serves the site for free from the `gh-pages` branch of the public repository https://github.com/SharmaAbhimanyueco/Supriyaaanya. If the link ever shows "404", switch Pages on: repository → Settings → Pages → Deploy from a branch → `gh-pages`, folder `/ (root)`.

**Offline.** `06_Web_Map/` holds the same site plus a local copy of Leaflet, and one-click launchers (`run_local_windows.bat`, `run_local_mac_linux.sh`). Without internet everything works except the background map and the online search.

**Licences.** Code MIT; maps and figures CC BY 4.0; place names from Wikidata (CC0); background map © OpenStreetMap contributors. The GADM zone outlines are not on the page (licence); each hexagon carries only a West/East label.

# Part 10 — Limitations

Say these openly. Knowing the limits of your own work is part of doing it well.

| Limitation | What it means | Effect on the results |
|------------------|----------------------------------------------|------------------------------------|
| **Undercount of built-up** | The map finds about half of the real built-up land (producer's accuracy 51.9%). Small villages, roads and houses under trees are missed at 30 m | The hectares are conservative; the 2025 corrected estimate is 17,706 ± 4,648 ha |
| **Look-alike classes** | Bare fields and bright roofs fall in the same clusters; bare/fallow is the weakest class (user's 35.7%, producer's 27.8%) | Some bare land is counted as built-up and some built-up as bare |
| **Mixed pixels** | One 30 m pixel can hold a field and a house | Small settlements are hard to separate |
| **Classification noise** | 3,225 ha mapped as built-up in 2015 are not built-up in 2025 | The change figures include some noise |
| **Crop stage** | Crops were at slightly different stages each March | Some cropland shows as trees or bare land. Part of the rise in trees/vegetation (14,255 → 22,299 ha) may be greener crops rather than new trees; this was not checked separately |
| **Boundary** | The GADM outline is old and its labels are wrong; the zones are not official tehsils | Zone figures are approximate; official tehsil outlines are needed for figures "by tehsil" |
| **Accuracy check** | Photo labels are AI-assisted; the Esri photos are of mixed dates; 158 points | Spot-check the labels; small-class figures are uncertain |
| **Not covered** | Building permits and zoning (GMADA/PUDA) are not included. No census exists for 2015–2025 | The full SDG 11.3.1 ratio (land against population growth) cannot be computed |
| **Tool** | The analysis ran in Python, not QGIS | Same method and outputs; the QGIS route is documented |

**What would improve it next:** more photo or field checks; Sentinel-2 images at 10 m for the later years (its March images start in 2016); supervised classification with training samples, if the teacher allows it; official tehsil boundaries; population data for the full SDG 11.3.1 ratio. The teacher's future-work ideas, a hotspot analysis (Getis-Ord Gi*) and a Development Pressure Index, are mentioned on slides 20 and 22 only.

# Part 11 — Decisions log

Every important choice, the options, what was chosen and why. "UNCONFIRMED" means waiting on the teacher.

| # | Decision | Options | Chosen | Why |
|----|--------------|----------------------|--------------------------|----------------------------------|
| 1 | Theme | Farmland loss; urbanisation | Urbanisation; farmland loss supporting | The teacher's instruction |
| 2 | Satellite | Landsat 8; Sentinel-2; others | Landsat 8 (UNCONFIRMED) | Same free sensor for all of 2015–2025; Sentinel-2 has no March 2015 images |
| 3 | Years | Any | 2015, 2020, 2025 (UNCONFIRMED) | Equal five-year steps; the latest March is 2025 |
| 4 | Season | Any month | March, both scenes per year | Wheat is green, so farmland and buildings differ most; the same month every year removes season effects |
| 5 | Images per year | One; several | Two clear scenes, median composite | Fills cloud gaps and removes leftover haze |
| 6 | Image source | Planetary Computer; Earth Engine; EarthExplorer | Planetary Computer | Free, no sign-up, scriptable, reads only the needed area |
| 7 | Software | QGIS; Python | Python, with every output styled for QGIS | Repeatable scripts that process 3.6 million pixels the same way every run; the QGIS route is documented. Disclosed openly |
| 8 | Classification type | Supervised; unsupervised | Unsupervised | The teacher's instruction (supervised was rejected) |
| 9 | Algorithm | K-means; ISODATA | K-means (UNCONFIRMED) | Standard, reproducible with a fixed seed, available in scikit-learn |
| 10 | Number of clusters | 4–16 tested | 10 | In the teacher's 8–10 range and the elbow region; extra clusters split mixed shades before merging |
| 11 | One model or one per year | Per year; pooled | Pooled across the three years | Per-year clusters meant different things (2020 > 2025 built-up); pooled clusters mean the same every year |
| 12 | Training data | 300,000-pixel sample; all pixels | All 3,626,753 pixels, best of 10 starts, 3 seeds | The sample model was unstable (2015 built-up 6,698–8,177 ha); full data agrees within 1% |
| 13 | Naming clusters | By eye each time; by reference | NDVI order, then the nearest first-run cluster (named by location and true colour) | The same rule for every cluster, written down and repeatable |
| 14 | Classes | 4–5 planned | 4 (water dropped) | No cluster picked out water; ponds are smaller than 30 m pixels |
| 15 | Zones | Tehsils; GADM pieces | GADM pieces as West/East zones | No verified tehsil outlines; the pieces' labels are wrong, so they are not called tehsils |
| 16 | Growth rate | % change; yearly rate | Both; the yearly rate uses the SDG 11.3.1 land formula | A recognised formula that compares periods of different length fairly; population part not available |
| 17 | Comparing zones | Hectares; share; UEII | All three, UEII for speed | UEII corrects for zone size |
| 18 | Accuracy check | None; visual; sample-based | Stratified random sample (50/50/30/30), blind photo labels, Olofsson area weighting (validation level UNCONFIRMED) | The recognised good practice; gives accuracy and a corrected area with a ± range |
| 19 | Who labelled the photos | Students; AI-assisted | AI-assisted, two blind raters plus a third look | Needed overnight; disclosed, and students should spot-check |
| 20 | Second opinion | None; ESA WorldCover | WorldCover 2020 comparison | An independent 10 m map from a space agency |
| 21 | Web map tool | qgis2web; custom Leaflet | Custom Leaflet page on GitHub Pages (UNCONFIRMED) | Search, filters, measurement and ranking; free open hosting |
| 22 | Licences | — | Code MIT; maps and figures CC BY 4.0; GADM and Esri photos kept private | Open where allowed; respects third-party terms |

# Part 12 — Where the code ran, and how to run it again

## Where the code was run

All the analysis, the slides and the web map were produced on **24 November 2026** in one place: a **cloud Linux computer** rented for the session, not a student laptop. It was a Claude Code on the web session (Anthropic's AI coding assistant), which wrote and ran the scripts at the project team's request. The data was streamed over the internet from public sources. Nothing was installed on a personal computer.

### The machine

| Item | Value |
|---|---|
| Operating system | Ubuntu 24.04.5 LTS (Linux, x86_64) |
| Processor and memory | 4 CPU cores, 15 GB RAM |
| Python | 3.13.18, in a virtual environment |
| Python packages | numpy 2.5.5, rasterio 1.5.2 (with GDAL 3.12.2), scikit-learn 1.9.1, scipy 1.18.1, pystac-client 0.9.1, planetary-computer 1.0.0, pyshp 3.1.9, shapely 2.2.0, pyproj 3.8.0, matplotlib 3.11.2, pillow 13.0.0, requests 2.34.2 |
| Node.js (slides, screenshots) | v22.23.5 with pptxgenjs 4.0.1, react 19.3.1, react-dom 19.3.1, react-icons 5.7.0, sharp 0.35.5; Playwright 1.63.0 with Chromium |
| Office tools | LibreOffice 24.2.7.2 (PowerPoint to PDF), pandoc 3.1.3 (master document) |

### The data sources it reached over the internet

| Source | What came from it | Used by |
|---|---|---|
| Microsoft Planetary Computer (planetarycomputer.microsoft.com, landsateuwest.blob.core.windows.net) | Landsat 8 Collection 2 Level-2 scenes, path 147 row 39 | `analysis/build_composites.py`, `helpers/search_scenes.py` |
| ESA WorldCover on Planetary Computer storage (ai4edataeuwest.blob.core.windows.net) | WorldCover 2020 and 2021 built-up maps (10 m) | `analysis/worldcover_check.py` |
| Esri World Imagery (server.arcgisonline.com) | Photo chips for the accuracy check (kept private, not published) | `analysis/make_chips.py` |
| Wikidata Query Service (query.wikidata.org) | Names and positions of towns and villages for the web map search (CC0) | `webmap/fetch_places_wikidata.py` |
| GitHub (github.com, GitHub Pages) | Code repository and free hosting of the web map | git |

### What was not used

- **QGIS** was not used for the analysis. The teacher asked for QGIS; say this openly. Every output opens in QGIS, and `08_Project_Notes/04_qgis_steps.md` describes the QGIS route.
- **Google Earth Engine** was not used. `gee/export_landsat_composites.js` is an alternative way to download the images and was never run.

### Which step ran where

Every script listed in `README.md` ran on the machine above, in the order given in `HOW_TO_RUN.md`. The model checks in `analysis/model_checks/` ran there too, through helper agents of the same session. The photo labels for the accuracy check (`04_Data/validation/labels_A.csv` and `labels_B.csv`) came from two independent AI raters (Claude Sonnet) that could not see the map. Disagreements were settled by a third look. The students should spot-check these labels.

### Can it run on a laptop?

Yes. The two demo scripts in `demo/` run on any laptop in seconds. They need Python 3.10 or newer and the three libraries in `requirements-demo.txt`. The full pipeline also runs on a laptop with internet access. The final model trains on 3.6 million pixels, three times over, so that step takes much longer than the rest. See `HOW_TO_RUN.md`.

## How to run the code

Run every command from inside the `Urban_Growth_Handover` folder unless a step says otherwise. Sections A–C need no internet once Python is installed; D and E need internet.

### A. Quick checks on a laptop (about 10 minutes the first time)

1. Install **Python 3.10 or newer** from python.org. On Windows, tick **"Add python.exe to PATH"** in the installer.
2. Open a terminal in the `Urban_Growth_Handover` folder.
   - Windows: open the folder in File Explorer, click the address bar, type `cmd`, press Enter.
   - Mac: right-click the folder in Finder, then Services → New Terminal at Folder.
3. Optional, but it keeps things tidy: make a virtual environment.
   - Windows: `py -m venv .venv`, then `.venv\Scripts\activate`
   - Mac/Linux: `python3 -m venv .venv`, then `source .venv/bin/activate`
4. Install the three libraries: `pip install -r 05_Code/requirements-demo.txt`
5. Recount the areas: `python 05_Code/demo/recompute_areas.py 04_Data/rasters`
6. Recompute the accuracy: `python 05_Code/demo/recompute_accuracy.py 04_Data`

If `rasterio` will not install, try a newer Python, or Anaconda: `conda install -c conda-forge rasterio pyproj`.

**What you should see.** These are the exact outputs from the project run:

```
Map grid: 1409 x 2170 pixels, CRS EPSG:32643, pixel 30 m = 0.09 ha

Area by land type (hectares, and % of the mapped area)
Land type                       2015              2020              2025
Built-up               7,844 ( 7.2%)    10,033 ( 9.2%)    14,786 (13.6%)
Cropland              81,218 (74.6%)    77,204 (70.9%)    66,728 (61.3%)
Trees/vegetation      14,255 (13.1%)    17,150 (15.8%)    22,299 (20.5%)
Bare/fallow            5,482 ( 5.0%)     4,439 ( 4.1%)     4,970 ( 4.6%)
Total                        108,799           108,826           108,783

Built-up change
  2015-2020: +2,190 ha  (+27.9%), 438 ha a year, yearly rate 4.92%
  2020-2025: +4,753 ha  (+47.4%), 951 ha a year, yearly rate 7.76%
  2015-2025: +6,942 ha  (+88.5%), 694 ha a year, yearly rate 6.34%

New built-up 2015 -> 2025: 10,170 ha, of which cropland in 2015: 6,916 ha (68%)
Built-up in 2015 but not in 2025 (mostly classification noise): 3,225 ha
```

```
Points used: 158 (unclear, dropped: 2)

Point counts (rows = map 2025, columns = photo)
                        Built-up      Cropland  Trees/vegeta   Bare/fallow
Built-up                      30             8             5             5
Cropland                       4            47             6             3
Trees/vegetation               8             8            20             0
Bare/fallow                    7             2             0             5

Overall accuracy (area-weighted): 74.6%
(simple, unweighted: 102 of 158 points = 64.6%)

Land type             user's  producer's
Built-up               62.0%       51.9%
Cropland               84.3%       87.1%
Trees/vegetation       61.8%       68.7%
Bare/fallow            35.7%       27.8%

Built-up vs not built-up: agreement 87.0%
Built-up 2025: map 14,786 ha; error-adjusted 17,706 ± 4,648 ha (95% range)
```

The totals differ slightly between years (108,783–108,826 ha) because a few pixels had no cloud-free view in that year: 303 pixels in 2015 and 478 in 2025, none in 2020. Those pixels are left out of that year's map.

### B. The web map without internet

- **Windows:** double-click `06_Web_Map/run_local_windows.bat`. **Mac/Linux:** run `sh 06_Web_Map/run_local_mac_linux.sh`. Either one starts a small local web server and opens http://localhost:8000 in the browser. Keep the window open while you use the map; close it (or press Ctrl+C) to stop.
- Offline, these all work: the land-cover layers, filters, live figures, the 1 km² grid, the rankings, and search over the built-in place list. Only the background map and the online search for other places need internet.
- Don't double-click `index.html` directly. Browsers block a page opened as a file from reading its data files, so the grid and the place list would not load.
- The live copy is at https://sharmaabhimanyueco.github.io/Supriyaaanya/ (see `06_Web_Map/LIVE_URL.txt`).

### C. Open the results in QGIS

1. Install QGIS (the current Long Term Release from qgis.org).
2. Drag `04_Data/rasters/lulc_2025.tif` into QGIS. The colours and names load by themselves from `lulc_2025.qml`, which sits next to it with the same name. The same applies to 2015, 2020 and the `clusters_*.tif` files.
3. Drag in `04_Data/landsat_composites/landsat_composite_2025.tif`. It opens in true colour (red = band 3, green = band 2, blue = band 1). For false colour, where plants show red: Layer Properties → Symbology → Style → Load Style → `style_false_colour_NIR_red_green.qml`.
4. To recount areas inside QGIS, open the Processing Toolbox and run **Raster layer unique values report** on `lulc_2025.tif`. Multiply each pixel count by 0.09 to get hectares (1 = Built-up, 2 = Cropland, 3 = Trees/vegetation, 5 = Bare/fallow).
5. For the study area outline, unzip `04_Data/study_area/Study_Area.zip` and add `study_area.shp`. Don't show its "Kharar"/"Rajpura" labels: they are wrong (see the master document, Part 3).

### D. Re-run the whole analysis (advanced; needs internet)

1. `pip install -r 05_Code/requirements.txt`
2. Make a work folder, here called `W`, with four empty sub-folders: `analysis`, `analysis2`, `validation`, `diagnostics`.
3. Unzip `04_Data/study_area/Study_Area.zip`. Below, `SHP` means the path to `study_area.shp`.
4. Run, from the `05_Code` folder:

```
python analysis/build_composites.py SHP W/analysis
python analysis/cluster_pooled.py W/analysis
python analysis/results.py W/analysis SHP
python analysis/worldcover_check.py W/analysis W/validation
python analysis/train_full.py W/analysis W/analysis2
python analysis/results2.py W/analysis W/analysis2 SHP W/validation
python analysis/make_chips.py W/analysis W/validation
```

5. **Label the photo chips blind.** `make_chips.py` hides each point's map class in `W/validation/.map_key_do_not_open.csv` so that whoever labels the chips cannot see it. Look at every chip in `W/validation/chips/` (the 30 m square is marked) and write `W/validation/reference_labels.csv` with the same columns as `04_Data/validation/reference_labels.csv`. Use "Unclear" when cloud hides the ground.
6. Then:

```
python analysis/accuracy.py W/validation W/analysis/lulc_2025.tif W/analysis2/lulc_2025.tif
python analysis/finalise.py W
```

7. Optional and slow, the model checks. Set the work folder first: on Mac/Linux, `LULC_WORK=W python analysis/model_checks/run1.py`, then `run2.py` and `plots.py` the same way. On Windows, run `set LULC_WORK=W` first.

The random choices are fixed (K-means seeds 0, 1 and 2, sample seed 2025), so a re-run should give the same numbers. Different library versions can change the last digit; the versions used are in `requirements.txt`.

### E. Rebuild the web map

Use the GitHub repository rather than this package, because the build script expects the repository's folder layout:

```
git clone https://github.com/SharmaAbhimanyueco/Supriyaaanya
cd Supriyaaanya
git checkout claude/urban-growth-mapping-handover-xkppdn
python -I scripts/webmap/build_webmap.py . <path to 04_Data/study_area/zones_west1_east2.npy>
```

It rewrites `webmap/index.html`, `webmap/layers/` and `webmap/data/`. To publish, copy the contents of `webmap/` to the `gh-pages` branch and push. GitHub Pages serves that branch.

### F. The slides and this package's charts

- The deck is built by `05_Code/slides/build_deck.js`, which also needs a theme helper that is not included. To change the slides, edit `02_Presentation/Urban_Growth_Mohali_slides.pptx` directly in PowerPoint or Google Slides.
- The charts, CSV tables and QGIS styles in this package can be rebuilt with:

```
python 05_Code/handover_tools/make_charts.py 04_Data/results.json 03_Maps_and_Charts/charts
python 05_Code/handover_tools/make_tables.py 04_Data/results.json 06_Web_Map/site/data 04_Data/tables
python 05_Code/handover_tools/make_qgis_styles.py 04_Data
```

`make_charts.py` needs matplotlib, and `make_qgis_styles.py` needs numpy and rasterio.



```{=openxml}
<w:p><w:r><w:br w:type="page"/></w:r></w:p>
```

# Part 13 — Teacher prep: questions, demos and screenshots


For Supriya Mahshere and Aanya Upadhyay. Read this the night before. It tells you what to say if the teacher asks questions, and what to show if she asks you to run something.

Paths like `04_Data/rasters` are inside the `Urban_Growth_Handover` folder. Slide numbers are from the 24-slide deck in `02_Presentation/`.

**Golden rules**

- If you do not know, say: "I am not sure. Here is how we would check." Never guess a number.
- Every number comes from the slides or the cheat sheet below. Do not round differently.
- Anything marked **UNCONFIRMED** is waiting for the teacher's answer. Say "we have asked, and are using this as our working choice."

---

## 0. Numbers cheat sheet

| What | Value |
|---|---|
| Study area | 1,209,178 pixels of 30 m, about 108,800 ha (about 1,088 km²) |
| Built-up 2015 / 2020 / 2025 | 7,844 / 10,033 / 14,786 ha |
| Built-up share | 7.2% / 9.2% / 13.6% |
| Growth 2015–2025 | +6,942 ha (+88.5%, "+89%"), 694 ha a year |
| Yearly rate (SDG 11.3.1 formula) | 6.34% overall; 4.92% (2015–20); 7.76% (2020–25) |
| Cropland 2015 / 2020 / 2025 | 81,218 / 77,204 / 66,728 ha |
| Trees/vegetation | 14,255 / 17,150 / 22,299 ha |
| Bare/fallow | 5,482 / 4,439 / 4,970 ha |
| West zone built-up | 4,336 → 9,236 ha; share 6.1% → 13.0%; UEII 0.69 |
| East zone built-up | 3,507 → 5,545 ha; share 9.3% → 14.8%; UEII 0.54 |
| Cropland that became built-up | 6,916 ha (68% of 10,170 ha new built-up) |
| Built-up in 2015 but not 2025 | 3,225 ha (noise) |
| Overall accuracy (158 points) | 74.6%; built-up vs not 87.0% |
| Built-up user's / producer's | 62.0% / 51.9% |
| Error-adjusted built-up 2025 | 17,706 ± 4,648 ha (map: 14,786 ha) |
| ESA WorldCover 2020 | 92.8% agreement; it finds 12,181 ha vs our 10,033 ha |
| Model | K-means, 10 clusters, 10 starts, up to 300 iterations, trained on 3,626,753 pixels |

---

## 1. The 60-second story

Say this if she asks, "Explain your project in one minute."

> "Our project asks one question: how fast is the area around Chandigarh turning into city? We studied the Mohali, Kharar, Zirakpur and Dera Bassi belt in Punjab. We used free Landsat 8 satellite photos from March 2015, 2020 and 2025. A computer method called K-means sorted every 30-metre pixel into ten groups, and we named the groups and merged them into four land types: built-up, cropland, trees and bare land.
>
> Built-up land grew from 7,844 hectares in 2015 to 14,786 hectares in 2025. That is 6,942 hectares more, nearly double, or 6.3% a year. Growth sped up after 2020, from 4.9% to 7.8% a year. The western part, Kharar and Mohali, grew faster than the east. About two-thirds of the new built-up land was farmland in 2015.
>
> We checked the map on 158 points using detailed photos. It is right at 75% of points overall and 87% for built-up versus not built-up. But it misses about half of the real built-up land, so our hectares are conservative. Our best corrected estimate for 2025 is about 17,700 hectares. Finally, we built an open web map where anyone can switch years, search a town and see the change."

**Time check:** about 60 seconds when read at a calm pace. Practise it once with a timer.

---

## 2. Three disclosures: say them before anyone asks

Say these early, in a calm voice. Teachers respect honesty. Being caught hiding something costs far more.

### 2.1 Python, not QGIS

> "Our teacher asked for the analysis in QGIS. Because of the deadline, we ran the analysis in Python. Every output opens in QGIS: the land-cover maps, the clusters and the Landsat images all have QGIS styles. The QGIS route is written step by step in `08_Project_Notes/04_qgis_steps.md`, and we can show you the results in QGIS now."

Do **not** say or imply the analysis was done in QGIS. The tool column on slide 13 says Python. Whether a Python route is acceptable is **UNCONFIRMED** with the teacher.

### 2.2 The photo labels were AI-assisted

> "To check accuracy, we needed to know what is really on the ground at 158 random points. We looked at detailed Esri photos. The labels were AI-assisted: two independent interpreters labelled every point without seeing our map. They agreed on 144 of 160 points, and a third look settled the 16 disagreements. These labels are not field visits. We should spot-check a sample ourselves, and we are happy to do that with you."

Before the presentation, open 10 to 15 chips in `04_Data/validation/chips/` yourselves and compare them with `04_Data/validation/reference_labels.csv`. Then you can say how many you checked and what you found. Only say a number if you really did it.

### 2.3 The hectares are conservative

> "Our map undercounts built-up land. The accuracy check shows it finds about 52% of real built-up land. So treat our hectares as a floor. The corrected estimate for 2025 is about 17,700 hectares, give or take 4,600, against 14,786 on the map. The trend, the speed-up after 2020, and the West-versus-East pattern are the reliable findings."

---

## 3. Likely questions and answers

Each answer is 2 to 4 sentences. Say it in your own words. **Show** tells you where to point.

### 3.1 Study area and boundary

**Q1. Why did you choose this area?**

**Say:** It is the belt next to Chandigarh where four fast-growing towns meet: Mohali, Kharar, Zirakpur and Dera Bassi. One district holds all four, so results can feed district-level planning. Growth drivers include Chandigarh's spillover, industrial parks and the airport.

**Show:** Slide 2, slide 4; `03_Maps_and_Charts/maps/location_map.jpg`.

**Q2. Where does your boundary come from? Is it official?**

**Say:** It comes from GADM, a free world database of boundaries. It is not an official Punjab map. We say that openly on the slides, and an official boundary would be the better choice. Checking it against an official district map is still to do.

**Show:** Slide 4 footnote; slide 6.

**Q3. Are "West" and "East" real tehsils?**

**Say:** No. The GADM file has two polygons with wrong labels: "Kharar" really holds Kharar and Mohali, and "Rajpura" really holds Dera Bassi including Zirakpur. Rajpura town is outside the study area. So we call them the West zone and East zone, not official tehsils.

**Show:** Slide 16 table and notes.

**Q4. How big is the study area? Did you check it against an official figure?**

**Say:** It is 1,209,178 pixels of 30 m, about 108,800 hectares, or about 1,088 km². We have not yet compared it with an official district area. That check is still open.

**Show:** Slide 4; `04_Data/tables/`.

**Q5. Why no buffer around the district?**

**Say:** We stayed inside the boundary, so every hectare belongs to the study area. Whether a 5 km buffer is wanted is **UNCONFIRMED**: we asked the teacher. A buffer would show growth just outside the line, for example near Banur (the project notes suggest Banur may fall just outside the line).

**Show:** `08_Project_Notes/01_message_to_teacher.md`, question 5.

### 3.2 Data and satellite

**Q6. Why Landsat 8 and not Sentinel-2?**

**Say:** Landsat 8 has a free, consistent archive, so we could use one satellite for all three years. Its pixels are 30 m. Sentinel-2 has 10 m pixels and would see small villages better, but we did not use it. It is on our next-steps list. The satellite choice is **UNCONFIRMED** with the teacher.

**Show:** Slide 6, slide 14, slide 21.

**Q7. Exactly which images did you use?**

**Say:** Landsat 8 Collection 2 Level-2, path 147, row 39, from Microsoft Planetary Computer. Two clear March scenes per year: 7 and 23 March 2015, 4 and 20 March 2020, and 2 and 18 March 2025.

**Show:** Slide 6 notes; `05_Code/analysis/build_composites.py`.

**Q8. Why March?**

**Say:** In March the wheat is green, so farmland and buildings look very different. Using the same month every year removes crop-season effects, so changes are real changes. The downside is that crops are at slightly different stages each March.

**Show:** Slide 7, slide 21.

**Q9. Why only 2015, 2020 and 2025?**

**Say:** Our working plan is 2015, 2020 and 2025: ten years with a middle point. Three years give two periods, and the middle point shows that growth sped up after 2020. These years are **UNCONFIRMED** with the teacher.

**Show:** Slide 15.

**Q10. Is 30 m enough?**

**Say:** It is fine for town-scale growth. It is not fine for single houses or narrow roads. One pixel can hold fields and houses together, which is why the map undercounts small settlements.

**Show:** Slide 14, slide 21.

**Q11. Is all your data free and open?**

**Say:** Yes. Landsat is free from USGS and NASA. WorldCover is free from the European Space Agency. The boundary is free for study but cannot be redistributed, so it is not in the public repository.

**Show:** Slide 6, slide 24.

### 3.3 Pre-processing

**Q12. How did you handle clouds?**

**Say:** We used the image's built-in quality flags (QA_PIXEL) to hide fill, cloud, cirrus, cloud shadow and dilated cloud pixels. We then combined two scenes per year.

**Show:** Slide 7; `05_Code/analysis/build_composites.py`.

**Q13. What is a composite and why a median?**

**Say:** A composite is one clean picture made from two clear photos. For each pixel we keep the middle value, so a stray cloud or shadow in one photo does not spoil the result. It is like taking the median of two exam attempts.

**Show:** Slide 9; slide 23 glossary.

**Q14. What are the six bands?**

**Say:** Blue, green, red, near-infrared, shortwave infrared 1 and shortwave infrared 2. Two are invisible to our eyes. Healthy plants reflect near-infrared strongly, which separates green wheat from concrete.

**Show:** Slide 9.

**Q15. Why UTM zone 43N?**

**Say:** It measures in metres, so one 30 m pixel is 900 m², or 0.09 hectare, in every year. Measuring on a latitude and longitude grid would give wrong areas. All three years share one grid.

**Show:** Slide 7; QGIS: Layer Properties, Information.

### 3.4 Classification and K-means

**Q16. What does "unsupervised" mean?**

**Say:** The computer groups pixels that look alike without being told what any group is. We name the groups afterwards. It is like sorting a sack of mixed pulses into heaps by look.

**Show:** Slide 10.

**Q17. Why not supervised classification, such as Random Forest?**

**Say:** The earlier plan used it, and the teacher asked for clustering instead. Supervised needs training points we label ourselves, which is slower for three years. Its advantage is that classes are defined by us. It is a good next step.

**Show:** `08_Project_Notes/02_teacher_brief_and_slide_list.md`; slide 14.

**Q18. Why K-means and not ISODATA?**

**Say:** The teacher offered K-means or ISODATA. We used K-means because it is simple and standard in scikit-learn. ISODATA can split and merge clusters by itself, so the number of groups can change. Which one she prefers is **UNCONFIRMED**.

**Show:** Slide 10; `08_Project_Notes/01_message_to_teacher.md`, question 3.

**Q19. Why 10 clusters for 4 land types?**

**Say:** Each land type looks different in different places: wet field, dry field, young wheat. Ten groups capture those variations, and we then merge them into four types. Using more clusters than land types is normal in unsupervised classification.

**Show:** Slide 11, slide 18.

**Q20. How did you name the clusters?**

**Say:** The computer only gives numbers. We named each cluster from where it sits: towns and roads, the forested hills in the north, fields. We also used true-colour images. Group 2 is built-up, groups 3 and 5 are trees, group 1 is bare land and the rest are cropland.

**Show:** Slide 11; `04_Data/model_checks/final_model_training.json`.

**Q21. Why one model for all three years?**

**Say:** If we trained a new model each year, group 4 in 2015 might mean something else from group 4 in 2020. One trained model gives each group the same meaning in every year, so the years compare fairly.

**Show:** Slide 10.

**Q22. Why is there no water class?**

**Say:** No cluster picked out water. Ponds and streams are too small to fill a 30 m pixel. So code 4 (water) is unused. We say that on the slides.

**Show:** Slide 11, slide 15.

**Q23. Why did you train on every pixel?**

**Say:** An earlier version trained on a 300,000-pixel sample gave different answers when retrained. Training on all 3,626,753 pixels from the three years fixed that. Three separate runs now agree within 1%.

**Show:** Slide 18.

**Q24. Why did you use Python instead of QGIS?**

**Say:** Deadline pressure. Python let us train on all pixels and repeat checks quickly. The results open in QGIS, and the QGIS steps are documented. Whether this is acceptable is the teacher's call.

**Show:** Slide 13; section 2.1 above.

### 3.5 Model checks

**Q25. Is 10 the best number of clusters?**

**Say:** Not by statistics alone. The elbow is at k = 8, and k = 7 to 10 score within about 10% of the best elbow value. The silhouette score is highest at k = 4 (0.386) but nearly flat from 5 to 16 clusters. Ten is inside the sensible range.

**Show:** Slide 18; `03_Maps_and_Charts/charts/chart_06_k_selection.png`.

**Q26. Is the model stable? Does it give the same answer twice?**

**Say:** Yes. Three runs with different random seeds converged in 35, 31 and 29 iterations. Their fit scores differ by less than 0.01%. Built-up area in 2025 is 14,737 to 14,841 ha across runs, within 1%.

**Show:** Slide 18; `03_Maps_and_Charts/charts/chart_07_stability.png`.

**Q27. Your numbers differ from an earlier version. Why?**

**Say:** The earlier model, trained on a 300,000-pixel sample, gave 6,609 to 14,529 ha (+120%). When we retrained it on other samples, 2015 moved between 6,698 and 8,177 ha, so it was unstable. We replaced it with the full-data model. Only the new numbers are used everywhere.

**Show:** Slide 18 notes; `04_Data/model_checks/model_checks.md`.

**Q28. Did the sample size matter?**

**Say:** Little. In the earlier tests, 50,000, 100,000 and 200,000 pixels per year gave similar 2025 built-up (14,756, 14,594 and 14,656 ha). The random seed mattered more than the sample size. That is why we moved to all pixels.

**Show:** `04_Data/model_checks/model_checks.md`.

### 3.6 Results and numbers

**Q29. What is your main result?**

**Say:** Built-up land grew from 7,844 ha in 2015 to 14,786 ha in 2025: +6,942 ha, about +89%. That is 6.3% a year. The share of the study area went from 7.2% to 13.6%.

**Show:** Slide 15; `03_Maps_and_Charts/charts/chart_01_builtup_trend.png`.

**Q30. Did growth speed up?**

**Say:** Yes. Built-up grew 2,190 ha (4.9% a year) in 2015–2020 and 4,753 ha (7.8% a year) in 2020–2025. The map undercount affects both periods, so the speed-up is likely real.

**Show:** Slide 15, slide 12.

**Q31. What happened to the other land types?**

**Say:** Cropland fell from 81,218 to 66,728 ha. Trees rose from 14,255 to 22,299 ha. Bare/fallow went 5,482, then 4,439, then 4,970 ha. The tree rise may partly be crop stage in March, so do not over-read it.

**Show:** `03_Maps_and_Charts/charts/chart_02_landcover_by_year.png`.

**Q32. How much farmland did the growth eat?**

**Say:** 10,170 ha became built-up between 2015 and 2025. Of that, 6,916 ha, or 68%, was cropland in 2015. Farmland loss is a supporting finding. The main theme is urban growth.

**Show:** Slide 16; `03_Maps_and_Charts/charts/chart_04_new_builtup_sources.png`.

**Q33. Why does some built-up land turn back into cropland?**

**Say:** Mostly it does not. 3,225 ha were mapped built-up in 2015 but not in 2025. Real built-up land rarely returns to farmland, so we treat that as classification noise, for example bare fields or bright roofs that look alike. This is why individual change pixels need care.

**Show:** Slide 16 notes, slide 21.

**Q34. Why do trees increase so much?**

**Say:** We do not know exactly. Some of it may be real: new parks, avenues and plantations. Some is crop stage: crops at a different growth stage in March can look like trees. We have not tested this separately.

**Show:** Slide 21.

**Q35. Where did growth happen?**

**Say:** The West zone, Kharar and Mohali, grew more: 4,336 to 9,236 ha. The East zone, Dera Bassi and Zirakpur, went from 3,507 to 5,545 ha. For place-level answers, the web map ranks the fastest-growing places.

**Show:** Slide 16; web map "Fastest-growing places" panel.

### 3.7 Change and urban metrics

**Q36. How do you calculate the yearly rate?**

**Say:** We use the SDG 11.3.1 formula for land consumption rate: ln(later ÷ earlier) ÷ years. It works like compound interest. For 2015–2025 it gives 6.34% a year.

**Show:** Slide 12; `08_Project_Notes/05_metrics_and_formulas.md`.

**Q37. Did you calculate SDG indicator 11.3.1?**

**Say:** Only half of it. The official indicator is the ratio of land consumption rate to population growth rate. We computed the land-consumption side. We have no census population for 2015–2025, so the full ratio is future work.

**Show:** Slide 3 notes, slide 21.

**Q38. What is UEII?**

**Say:** The Urban Expansion Intensity Index is new built-up land per year as a percentage of the zone's area. It lets a big zone and a small zone be compared fairly, like turning marks out of 50 and out of 100 into percentages. The speed bands (slow, low, medium, high) are a convention from published studies, not a rule.

**Show:** Slide 12, slide 16, slide 23.

**Q39. West has the higher UEII but a lower built-up share than East. Is that a mistake?**

**Say:** No, they answer different questions. The share is how much of the zone is built-up now: East 14.8%, West 13.0%. UEII is how fast new land was added: West 0.69, East 0.54. East started higher, in 2015 at 9.3% against 6.1%, probably because it holds older towns. West started lower and added more land per year.

**Show:** Slide 16 table.

**Q40. Why the ln formula and not simple growth?**

**Say:** UN-Habitat and published studies use the ln formula, so our rate can be compared with others. The simple formula would give a different number for the same data. We name the formula wherever we quote the rate.

**Show:** Slide 12; `08_Project_Notes/05_metrics_and_formulas.md`.

### 3.8 Accuracy

**Q41. How did you check accuracy?**

**Say:** We drew 160 random points from the 2025 map: 50 built-up, 50 cropland, 30 trees and 30 bare. For each we cut a photo about 300 m across from Esri World Imagery and labelled it without seeing the map. Two points under cloud were dropped, so 158 were used. Results are area-weighted (Olofsson method).

**Show:** Slide 19; `04_Data/validation/chips/`.

**Q42. Why should we trust AI-assisted labels?**

**Say:** You should not trust them blindly, and we do not. Two independent interpreters labelled without seeing the map and agreed on 90% of points (95% for built-up versus not). A third look settled the rest. They are still not field visits. We will spot-check a sample, and you can see every chip and sheet.

**Show:** `04_Data/validation/reference_labels.csv`, `labels_A.csv`, `labels_B.csv`; demo 4.4.

**Q43. Is 158 points enough?**

**Say:** It gives usable, not tight, answers. That is why we report a range: corrected built-up 17,706 ± 4,648 ha. More points would shrink that range. This is an honest limit.

**Show:** Slide 19.

**Q44. Explain user's and producer's accuracy.**

**Say:** User's accuracy asks: of the pixels the map calls built-up, how many really are? That is 62%. Producer's accuracy asks: of the real built-up land, how much did the map find? That is 52%. So the map is a little over half right when it says built-up, and finds about half of the real built-up land.

**Show:** Slide 19; `03_Maps_and_Charts/charts/chart_05_accuracy_by_class.png`.

**Q45. 75% overall is not high. Is the map useful?**

**Say:** It is useful for trends, with care. Built-up versus not built-up is 87% right. Cropland is the strongest class (user's 84.3%, producer's 87.1%). Bare/fallow is weakest (35.7% and 27.8%), so do not rely on it.

**Show:** Slide 19; `04_Data/validation/accuracy.json`.

**Q46. You said the map undercounts, but WorldCover agrees 93%. How?**

**Say:** Most pixels are not built-up, so agreement is high even when built-up is missed. For built-up alone, 70.9% of our built-up pixels are built-up in WorldCover, and we find 59.1% of its built-up land. WorldCover finds 12,181 ha in 2020 against our 10,033 ha, which is the same undercount.

**Show:** Slide 19; `04_Data/validation/worldcover_check.json`.

**Q47. What does "17,706 ± 4,648 ha" mean?**

**Say:** It is the area estimate after correcting the map using our checked points. The true 2025 built-up area is probably somewhere between 13,058 and 22,354 ha (95% range). Our map value of 14,786 ha sits inside the range, at the low end.

**Show:** Slide 19; `04_Data/validation/accuracy.json`.

### 3.9 Web map

**Q48. What can the web map do?**

**Say:** It switches between 2015, 2020, 2025 and a change view, with a play button. You can filter land types and zones, show only land that became built-up, and colour a 1 km² hexagon grid by growth, share, farmland built over or UEII. You can search a town, see a figure within 0.5 to 3 km, click any 30 m square for its history, and see a ranking of the fastest-growing places.

**Show:** Live site; demo 4.1; `03_Maps_and_Charts/screenshots/`.

**Q49. Is it made with qgis2web, as planned?**

**Say:** No. It is a static site we built with Python and the open-source Leaflet library. The plan was qgis2web on GitHub Pages. We chose a custom page so users can filter, search and rank. Whether she accepts this is **UNCONFIRMED**.

**Show:** `05_Code/webmap/`; `06_Web_Map/site/`. Slide 20 shows a screenshot of the real dashboard; its speaker notes say it was built with Leaflet, not qgis2web.

**Q50. Does it work offline? Is it safe to publish?**

**Say:** Yes, offline with limits. The land-cover layers and statistics work. Background map tiles and online search need internet. The site publishes only our results, not the GADM polygons, because of licence. Code is MIT and maps and figures are CC BY 4.0.

**Show:** Demo 4.1b; `06_Web_Map/LIVE_URL.txt`.

**Q51. How are the hexagon numbers made?**

**Say:** Each hexagon is about 1 km². We count built-up pixels inside it for each year and turn them into hectares. The page decodes the map layers in your browser, so the same counting happens on screen. Hexagons carry only a West/East label, not the GADM polygons.

**Show:** Live site, tick "1 km² grid"; `03_Maps_and_Charts/screenshots/webmap_04_hex_grid.png`.

### 3.10 Tools, code and reproducibility

**Q52. Can someone else reproduce your results?**

**Say:** Yes. The scripts, the settings and the seed are in the code. Anyone can run the full pipeline with `05_Code/HOW_TO_RUN.md`. For a quick test, our two demo scripts recompute the areas and the accuracy from the saved maps in under a minute.

**Show:** `05_Code/HOW_TO_RUN.md`; demo 4.3.

**Q53. Can your results open in QGIS?**

**Say:** Yes. Each raster has a same-name .qml style, so QGIS colours it automatically. The Landsat composites have a true-colour style. We can show that now.

**Show:** Demo 4.2; `04_Data/rasters/`.

**Q54. Where is the code and is it public?**

**Say:** It is on GitHub in a public repository, with an MIT licence for code and CC BY 4.0 for maps. The GADM boundary and Esri chips are not published, for licence reasons.

**Show:** https://github.com/SharmaAbhimanyueco/Supriyaaanya; screenshot 9.

**Q55. Why aren't the boundary files in the public repository?**

**Say:** GADM's licence allows academic use but not redistribution. So `Study_Area.zip` is only in the private package copy. Please do not publish it.

**Show:** `04_Data/study_area/`.

### 3.11 Limitations and next steps

**Q56. What is the biggest weakness?**

**Say:** The undercount. The map finds only about half of real built-up land, mostly small villages, roads and houses under trees. Hectares are therefore conservative. The trend and the West-versus-East pattern are less affected.

**Show:** Slide 21.

**Q57. Would you trust the hectare numbers?**

**Say:** Trust the direction and the speed-up, treat the hectares as a floor. For 2025 the corrected estimate of 17,700 ha is the better central number. 2015 is the least certain year, because the earlier sample-based tests moved it by about 1,500 ha.

**Show:** Slide 19, slide 21.

**Q58. What would you do with more time?**

**Say:** Check more points, including field visits. Use Sentinel-2 at 10 m. Train a supervised classifier with our own samples. Use official tehsil boundaries. Add population data for the full SDG 11.3.1 ratio.

**Show:** Slide 22; section 7 below.

---

## 4. Demo scripts

Practise each demo once on your own laptop. Keep it short. If something fails, say so, and move on to a screenshot.

### 4.1 The live web map, and the offline copy (3 to 4 minutes)

**Live site** (needs internet): https://sharmaabhimanyueco.github.io/Supriyaaanya/

1. Open the site. Say: "This is open source and free to use. It shows the 2025 land cover."
2. Click **2015**, then **2025**, then **Change**. Say: "Red is built-up land. In Change, we see the land that became built-up between 2015 and 2025."
3. In **Map filters**, set **Show** to "Only farmland that became built-up". Say: "This is the 6,916 ha of cropland that became built-up."
4. Press **Play 2015 → 2025**. Say: "Watch the red spread."
5. In **Search a place**, type **Kharar** and pick it. Say: "The map flies there and shows built-up land within 1 km, by year." Change **Figures within** to 2 km.
6. Tick **1 km² grid coloured by** and pick "built-up growth (ha)". Move **Hide cells below** up to show only the strongest cells.
7. Set **Zone** to East. Say: "The ranking now shows the fastest-growing places in the East zone."
8. Click any point on the map. Say: "Each 30 m square has its own profile, what it was in 2015, 2020 and 2025."
9. Scroll to **How reliable is it?** Say: "The page states the undercount openly."

**Offline copy** (no internet needed):

- Windows: double-click `06_Web_Map/run_local_windows.bat`.
- Mac or Linux: run `sh 06_Web_Map/run_local_mac_linux.sh`.
- It starts a local server and opens http://localhost:8000.
- Without internet, land-cover layers and statistics still work. Background tiles and online search do not. Say that before she asks. Use the built-in place list, for example Kharar, which still works.
- Do not open `index.html` by double-clicking. The grid and place data will not load.
- Close the black window when done.

### 4.2 Opening the results in QGIS (5 to 6 minutes)

Install QGIS first: the current Long Term Release (LTR) from qgis.org.

**A. The 2025 land-cover map**

1. Drag `04_Data/rasters/lulc_2025.tif` into QGIS. The same-name `lulc_2025.qml` loads automatically, so you should see four colours. If not: Layer Properties, Symbology, Style, Load Style, pick the .qml.
2. Say: "Codes are 1 Built-up, 2 Cropland, 3 Trees, 5 Bare. Code 4, water, is unused."
3. Check the legend in the Layers panel.

**B. The Landsat composite in true colour**

1. Drag `04_Data/landsat_composites/landsat_composite_2025.tif` in. The true-colour style loads.
2. If it does not, open Layer Properties, Symbology, and choose **Multiband color**. Set Red = band 3, Green = band 2, Blue = band 1. The band order is blue, green, red, NIR, SWIR1, SWIR2 (bands 1 to 6, from `05_Code/analysis/build_composites.py`).
3. Values are reflectance × 10,000, and NoData is −32768. If the picture is too dark or too bright, adjust the min and max under Symbology.
4. Say: "This is what the computer saw before classifying: what our eyes would see from space."
5. Turn `lulc_2025` on and off over it, and set opacity to about 60%.

**C. Identify tool**

1. Click **Identify Features** (the "i" cursor). Pick the `lulc_2025` layer. Click a built-up pixel in Mohali.
2. Say: "The pixel value is 1, so built-up. One pixel is 30 m by 30 m, or 0.09 hectare."

**D. Recount areas with a QGIS tool**

1. Open **Processing, Toolbox**, search **Raster layer unique values report**.
2. Input layer: `lulc_2025`. Run it.
3. In the results, find class value 1. The area is given in m². Divide by 10,000: you should get about 14,786 ha, as on slide 15 (small rounding differences are normal).
4. Repeat for `lulc_2015` and check about 7,844 ha.
5. Say: "This is the same count, done in QGIS. It matches our Python result."

**E. Side by side**: see screenshot 4 in section 5.

### 4.3 Re-running a calculation on a laptop (3 to 4 minutes)

**Setup (do this the day before):** Python 3.10 or newer. Then `pip install -r 05_Code/requirements-demo.txt` (numpy and rasterio).

**Script 1: areas**

- Run: `python 05_Code/demo/recompute_areas.py 04_Data/rasters`
- It reads `lulc_2015.tif`, `lulc_2020.tif` and `lulc_2025.tif`, and prints hectares per class per year and the built-up change.
- Check the output against slide 15: 7,844, 10,033 and 14,786 ha for built-up, and +6,942 ha.
- Say: "Each pixel is 0.09 ha. The script counts the pixels of each class and multiplies."

**Script 2: accuracy**

- Run: `python 05_Code/demo/recompute_accuracy.py 04_Data`
- It reads the validation labels and the 2025 maps, and prints the confusion matrix and the overall, user's and producer's accuracy. These are area-weighted (Olofsson method).
- Compare with slide 19: overall 74.6%, built-up user's 62.0% and producer's 51.9%.
- Say: "Rows are what the map said. Columns are what the photo showed. Numbers on the diagonal are the matches."

If the script gives a slightly different number than the slide, do not hide it. Say: "The slide uses `results.json`. Let us look at the difference." Then tell the person who built the package.

### 4.4 Showing the validation evidence (3 minutes)

1. Open `03_Maps_and_Charts/maps/validation_examples.png`. Say: "Six of the 158 points. The yellow square is one 30 m pixel."
2. Open `04_Data/validation/chips/` and pick any chip. Say: "This is the photo each interpreter saw. They could not see our map."
3. Open `04_Data/validation/sheets/` and show a labelling sheet.
4. Open `04_Data/validation/reference_labels.csv`. Show that each point has an agreed label. Then open `labels_A.csv` and `labels_B.csv` and show a disagreement.
5. Offer: "Pick any point and we will compare the chip with the map together."

---

## 5. Screenshot checklist: take these yourselves

Take these on your own laptop. They prove hands-on work and you can paste them into your own slides. Save PNGs in a new folder, for example `07_Teacher_Prep/my_screenshots/`. Windows: `Win+Shift+S`. Mac: `Cmd+Shift+4`.

**1. QGIS: study area on the 2025 true-colour composite**

- **Open:** QGIS, `04_Data/landsat_composites/landsat_composite_2025.tif`, then `04_Data/study_area/Study_Area.zip` (unzip first, drag the .shp in).
- **Steps:** Style the composite true colour. Set the outline to "no fill" with a thick red outline. Turn off the polygon labels (Properties, Labels, No Labels).
- **Visible:** satellite picture, outline, the Layers panel, QGIS title bar.
- **Save as:** `qgis_01_study_area_composite_2025.png`.
- **Slide:** 4, Study area (or slide 7, Data preparation).
- **Why:** proves you opened the data and shows the area clearly. Do not publish the picture with the GADM outline online.

**2. QGIS: lulc_2025 styled with a legend**

- **Open:** `04_Data/rasters/lulc_2025.tif`.
- **Steps:** The .qml loads. Make the Layers panel show the four classes with colours.
- **Visible:** map, class names and colours in the Layers panel.
- **Save as:** `qgis_02_lulc_2025_legend.png`.
- **Slide:** 15, Results: how much and how fast.
- **Why:** shows the result in the teacher's own tool.

**3. QGIS: area report**

- **Open:** Processing Toolbox, **Raster layer unique values report**, input `lulc_2025`.
- **Steps:** Run it. Show the parameters and the results table.
- **Visible:** tool name, input layer, the count and area for each value.
- **Save as:** `qgis_03_area_report_2025.png`.
- **Slide:** 13, GIS and remote sensing analysis (or new slide "Re-counted in QGIS").
- **Why:** shows the numbers can be reproduced in QGIS.

**4. QGIS: 2015 versus 2025 side by side**

- **Open:** `lulc_2015.tif` and `lulc_2025.tif` in two map canvases. Use **View, New Map View** and drag a layer into each. Lock the extent with **Synchronize** (in the Map View panel).
- **Visible:** both maps with the same area, a clear change of red.
- **Save as:** `qgis_04_2015_vs_2025.png`.
- **Slide:** 15 or 16.
- **Why:** shows hands-on change detection.

**5. Web map overview, 2025**

- **Open:** the live site. **Click:** 2025. Make the window wide.
- **Visible:** the map, the year buttons, the legend.
- **Save as:** `mywebmap_01_overview_2025.png`.
- **Slide:** 20, Web map. Its current screenshot was taken offline, without the background map; replace it with yours.
- **Why:** your own screenshot shows the background map and proves you opened the live site.

**6. Web map change view**

- **Steps:** Click **Change**. Set **Show** to "Only farmland that became built-up".
- **Visible:** the Change button highlighted, the filter on.
- **Save as:** `mywebmap_02_change.png`.
- **Slide:** 16, Results: where growth happened.
- **Why:** links to the 6,916 ha finding.

**7. Web map search result**

- **Steps:** Search **Kharar**. Pick it. Wait for the profile card.
- **Visible:** the search text, the map zoomed to Kharar, the figures card.
- **Save as:** `mywebmap_03_search_kharar.png`.
- **Slide:** 20.
- **Why:** shows a place-level answer.

**8. Web map hexagon grid**

- **Steps:** Tick **1 km² grid coloured by**, pick built-up growth. Set Zone to All.
- **Visible:** coloured hexagons, legend, slider.
- **Save as:** `mywebmap_04_hex_grid.png`.
- **Slide:** 16.
- **Why:** shows where growth is concentrated.

**9. GitHub repository page**

- **Open:** https://github.com/SharmaAbhimanyueco/Supriyaaanya
- **Visible:** the file list, the licence label, the repository name.
- **Save as:** `github_01_repository.png`.
- **Slide:** 24 (References) or a new slide "Open source and reproducible".
- **Why:** shows the code is public and licensed.

**10. One validation chip next to the map**

- **Open:** one image from `04_Data/validation/chips/` and `lulc_2025.tif` zoomed to the same place (use the point's coordinates in `sample_points.csv`).
- **Visible:** photo on the left, map on the right, the same location.
- **Save as:** `validation_01_chip_vs_map.png`.
- **Slide:** 19, Accuracy check.
- **Why:** shows what an accuracy check looks like on one point.

### Ready-made screenshots and charts

| File in `03_Maps_and_Charts/` | Best slide |
|---|---|
| `maps/location_map.jpg` | 4 Study area |
| `maps/map_lulc_2015.png`, `map_lulc_2020.png`, `map_lulc_2025.png` | 15 Results: how much and how fast |
| `maps/map_change_2015_2025.png` | 16 Results: where growth happened |
| `maps/validation_examples.png` | 19 Accuracy check |
| `charts/chart_01_builtup_trend.png` | 12 and 15 |
| `charts/chart_02_landcover_by_year.png` | 15, or backup for Q31 |
| `charts/chart_03_zones.png` | 16 |
| `charts/chart_04_new_builtup_sources.png` | 16 |
| `charts/chart_05_accuracy_by_class.png` | 19 |
| `charts/chart_06_k_selection.png` | 18 Model checks |
| `charts/chart_07_stability.png` | 18 Model checks |
| `screenshots/webmap_01_overview_2025.png` | 20 Web map |
| `screenshots/webmap_02_change_2015_2025.png` | 20 or 16 |
| `screenshots/webmap_03_search_kharar.png` | 20 |
| `screenshots/webmap_04_hex_grid.png` | 20 or 16 |
| `screenshots/webmap_05_east_zone_ranking.png` | 16 (zone comparison) |
| `screenshots/webmap_06_phone.png` | 20 (works on a phone) |

---

## 6. Day-before checklist

**Laptop and files**

- [ ] Laptop charged, charger packed. Packed an adapter for the projector (HDMI or USB-C).
- [ ] The whole `Urban_Growth_Handover` folder is copied to the laptop, and a second copy is on a USB drive.
- [ ] A PDF backup of the slides: `02_Presentation/Urban_Growth_Mohali_slides.pdf`, also on your phone.
- [ ] `02_Presentation/slide_images/` ready, in case PowerPoint fails.

**Offline web map**

- [ ] Run `06_Web_Map/run_local_windows.bat` (or `sh 06_Web_Map/run_local_mac_linux.sh`) once with Wi-Fi **off**.
- [ ] Confirm the layers load, 2015 and 2025 switch, and the grid appears.
- [ ] Try the live site on your phone's hotspot too.

**QGIS and Python**

- [ ] QGIS installed. Open `lulc_2025.tif` once. Run the unique values report once.
- [ ] Python 3.10 or newer installed. `pip install -r 05_Code/requirements-demo.txt` done. Both demo scripts run once.
- [ ] Your 10 screenshots from section 5 are taken and in a folder.

**Content**

- [ ] Spot-check 10 to 15 validation chips against `reference_labels.csv`. Write down how many you checked and any you disagree with.
- [ ] Add your own screenshots to the slides. Replace the slide 20 screenshot with your own of the live site.
- [ ] Read the sentences about **UNCONFIRMED** items (satellite, years, K-means or ISODATA, validation level, web map tool, deadline, missing slide 16). If the teacher has answered, update the slides.
- [ ] Check wording of the SDG targets on sdgs.un.org (slide 3 notes). Check the references on slide 24.

**Rehearsal**

- [ ] Run the full presentation twice with a timer. Agree who speaks on which slide.
- [ ] Practise the 60-second story and the three disclosures, out loud.
- [ ] Each of you answers five random questions from section 3 without reading.
- [ ] Sleep. Arrive early. Open the live site and the offline site before she comes in.

---

## 7. What we would do next

Say these as honest next steps, not as failures.

1. **More photo and field checks.** 158 points gives a wide range (± 4,648 ha). More points, with a few field visits, would narrow it and replace the AI-assisted labels with checked ones.
2. **Sentinel-2 at 10 m.** Smaller pixels would catch small villages, roads and houses under trees, and reduce the undercount.
3. **Supervised classification with our own training samples.** We would define the classes ourselves, and could add a water class and separate bare land from built-up.
4. **Official tehsil boundaries.** This would replace the West and East zones with real administrative units and let us report by tehsil, and also check the study-area total of about 108,800 ha.
5. **Population data for the full SDG 11.3.1 ratio.** Dividing the land consumption rate by the population growth rate needs a population figure for each year. India's last census was in 2011 (check the dates of the next one), so we need other sources.
6. **Also named in the deck:** hotspot analysis (Getis-Ord Gi*) and a Development Pressure Index (distance to built-up areas, roads, the airport and town centres).
7. **Re-do the analysis in QGIS** if the teacher requires it, following `08_Project_Notes/04_qgis_steps.md`.

**Open items waiting for the teacher (UNCONFIRMED):** satellite and years; K-means or ISODATA; validation level; web map tool (qgis2web or our custom page); 5 km buffer; deadline and format; the missing slide 16 in her list.


```{=openxml}
<w:p><w:r><w:br w:type="page"/></w:r></w:p>
```

# Part 14 — Glossary

Short definitions, A to Z. Part 2 explains each idea at length, with an everyday analogy.

| Term | Meaning |
|---------------------------|-------------------------------------------------------------------------|
| Adjusted Rand index (ARI) | A score from 0 to 1 for how alike two groupings of the same pixels are; 1 = identical |
| Band | One "colour" a satellite records, often invisible to the eye (for example near-infrared) |
| Basemap | The background map (streets, names) under the project's own layers |
| Built-up | Land covered by buildings, roads and other hard surfaces |
| Calinski–Harabasz score | A cluster-quality score: higher = clusters more compact and further apart |
| Cluster | A group of pixels with similar colours, found by the computer without labels |
| Collection 2 Level-2 | The Landsat product that is already corrected for the atmosphere (surface reflectance) |
| Composite | One picture made from several, here by taking the middle (median) value per pixel |
| Confusion matrix | A table of map class against true class at check points; the diagonal = agreement |
| CRS (coordinate reference system) | The rule that ties map coordinates to places on Earth |
| Davies–Bouldin score | A cluster-quality score: lower = better separated clusters |
| Elbow method | Choosing the number of clusters where adding more stops helping much |
| EPSG code | A standard number for a CRS: 4326 = latitude/longitude, 32643 = UTM 43N, 3857 = Web Mercator |
| Error-adjusted area | An area corrected with the accuracy-check results, given with a ± range |
| ESA WorldCover | A global 10 m land-cover map from the European Space Agency, used as a second opinion |
| GADM | A free worldwide boundary database; the source of the study-area outline (no redistribution) |
| GeoJSON | A text file format for map shapes, used for the web map's hexagon grid |
| GeoTIFF | An image file that also knows where on Earth it lies; all the project's rasters |
| GIS | Geographic Information System: software that stores, shows and analyses mapped data (e.g. QGIS) |
| GitHub Pages | Free website hosting from a GitHub repository; hosts the web map |
| Hectare (ha) | 100 m × 100 m = 10,000 m²; one 30 m pixel = 0.09 ha |
| Inertia | The total squared distance from each pixel to its cluster centre; lower = tighter clusters |
| K-means | A clustering method that sorts pixels into k groups around k centres, moving the centres until stable |
| Land consumption rate | Yearly growth rate of built-up land, ln(later ÷ earlier) ÷ years; the land part of SDG 11.3.1 |
| Landsat 8 | A NASA/USGS Earth-observation satellite launched in 2013; free 30 m images |
| Leaflet | A free open-source JavaScript library for web maps |
| LULC | Land use / land cover: what covers the ground (buildings, crops, trees, bare soil, water) |
| Median | The middle value of a set; ignores extreme values such as clouds |
| NDVI | (NIR − Red) ÷ (NIR + Red): a greenness index from −1 to 1; healthy plants score high |
| Nodata | A cell value that means "no information here" (0 in the land-cover maps, −32768 in the composites) |
| Olofsson method | Good-practice accuracy and area estimation that weights each check point by its class's map area |
| Overall accuracy | Share of the area the map labels correctly |
| Pixel | One square cell of a raster; here 30 m × 30 m |
| Planetary Computer | Microsoft's free catalogue and storage of public Earth data, used to get the images |
| Producer's accuracy | Of the real land in a class, the share the map found (misses = omission errors) |
| QA_PIXEL | Landsat's quality band, flagging fill, cloud, cirrus and shadow per pixel |
| QGIS | Free, open-source desktop GIS; the tool the teacher asked for |
| Raster / vector | Raster = a grid of cells (images, land-cover maps); vector = points, lines and shapes (the boundary) |
| Reclassification | Merging clusters into named land types (10 clusters → 4 land types) |
| Reflectance | The share of sunlight a surface reflects, from 0 to 1 |
| Remote sensing | Learning about the Earth's surface from a distance, here from a satellite |
| SDG 11.3.1 | UN indicator: ratio of land consumption rate to population growth rate |
| Seed (random seed) | A number that fixes the random choices so a run can be repeated exactly |
| Silhouette score | How well each pixel fits its own cluster compared with the next nearest one (−1 to 1) |
| STAC | SpatioTemporal Asset Catalog: a standard way to search satellite images, like a library catalogue |
| Stratified random sample | Random points with a fixed number per class, so small classes are checked too |
| Supervised / unsupervised classification | Supervised learns from labelled examples; unsupervised groups pixels first, and people name the groups |
| UEII | Urban Expansion Intensity Index: new built-up ÷ (zone area × years) × 100 |
| User's accuracy | Of the map's pixels in a class, the share that are right (false alarms = commission errors) |
| UTM zone 43N | A flat metric map grid for 72°E–78°E north of the equator; used for all area measurements |
| Web Mercator | The projection of web maps (EPSG:3857); fine for display, wrong for measuring areas |
| WRS-2 path/row | Landsat's fixed grid of scene footprints; this area is path 147, row 39 |
| Zone (West/East) | The two pieces of the boundary file, used for comparison; not official tehsils |

# Part 15 — References and sources

**Data**

- U.S. Geological Survey. Landsat 8 Collection 2 Level-2 Science Products (surface reflectance). https://www.usgs.gov/landsat-missions/landsat-collection-2-level-2-science-products. Landsat data courtesy of the U.S. Geological Survey.
- Microsoft Planetary Computer. Landsat Collection 2 Level-2 dataset and STAC API. https://planetarycomputer.microsoft.com/dataset/landsat-c2-l2
- Zanaga, D. et al. (2021). ESA WorldCover 10 m 2020 v100. https://doi.org/10.5281/zenodo.5571936
- Esri World Imagery (basemap used for the photo check; chips not redistributed). https://www.arcgis.com/home/item.html?id=10df2279f9684e4a9f6a7f08febac2a9
- GADM, database of global administrative areas (study-area outline; no redistribution). https://gadm.org
- Wikidata (place names and positions, CC0). https://www.wikidata.org
- OpenStreetMap contributors (basemap of the location map and the web map, ODbL). https://www.openstreetmap.org/copyright

**Methods**

- Olofsson, P., Foody, G.M., Herold, M., Stehman, S.V., Woodcock, C.E. and Wulder, M.A. (2014). Good practices for estimating area and assessing accuracy of land change. *Remote Sensing of Environment* 148, 42–57. https://doi.org/10.1016/j.rse.2014.02.015
- United Nations Statistics Division. SDG indicator metadata, indicator 11.3.1. https://unstats.un.org/sdgs/metadata/files/Metadata-11-03-01.pdf
- UN-Habitat. Metadata on SDG indicator 11.3.1. https://unhabitat.org/sites/default/files/2020/07/metadata_on_sdg_indicator_11.3.1.pdf
- UEII speed bands, as used in: https://www.mdpi.com/2220-9964/11/7/406
- Pedregosa, F. et al. (2011). Scikit-learn: Machine learning in Python. *Journal of Machine Learning Research* 12, 2825–2830 (K-means and the cluster-quality scores).

**Software**

Python with numpy, rasterio and GDAL, scikit-learn, pyproj, shapely, pyshp, pystac-client, planetary-computer, matplotlib and Pillow; Leaflet 1.9.4 (web map); pptxgenjs (slides); QGIS (for opening the results; https://qgis.org).

**A note on checking.** The SDG metadata and the Olofsson paper are cited from their official pages, but their full texts could not be opened from the project's computer (see `08_Project_Notes/05_metrics_and_formulas.md`). Before quoting the SDG wording, read it on the UN page. The general facts in Part 2 list their own sources at the end of that part.

```{=openxml}
<w:p><w:r><w:br w:type="page"/></w:r></w:p>
```

# Part 16 — File inventory

Every file in the package, with its size. Folders of many similar files are summarised in one row.

| File | Size | What it is |
|----------------------------------------------------------|---------|---------------------------------|
| 00_READ_ME_FIRST.md | 3 KB | One-page guide to the package |
| 01_Master_Document/​Master_Document_Urban_Growth_Mohali.docx | 6.9 MB | This document |
| 01_Master_Document/​Master_Document_Urban_Growth_Mohali.pdf | 4.0 MB | This document |
| 01_Master_Document/​Master_Document_source.md | 161 KB | This document |
| 02_Presentation/​Urban_Growth_Mohali_slides.pdf | 1.9 MB | The 24-slide deck |
| 02_Presentation/​Urban_Growth_Mohali_slides.pptx | 2.8 MB | The 24-slide deck |
| 02_Presentation/​slide_images/​ (24 files) | 6.9 MB | Every slide as a PNG picture (24) |
| 02_Presentation/​slide_text_and_notes.md | 29 KB | Every slide's text and speaker notes |
| 03_Maps_and_Charts/​archive_superseded/​README.md | under 1 KB | Superseded first-run or per-year figure (do not use the numbers) |
| 03_Maps_and_Charts/​archive_superseded/​first_run_map_change_2015_2025.png | 157 KB | Superseded first-run or per-year figure (do not use the numbers) |
| 03_Maps_and_Charts/​archive_superseded/​first_run_map_lulc_2015.png | 150 KB | Superseded first-run or per-year figure (do not use the numbers) |
| 03_Maps_and_Charts/​archive_superseded/​first_run_map_lulc_2020.png | 153 KB | Superseded first-run or per-year figure (do not use the numbers) |
| 03_Maps_and_Charts/​archive_superseded/​first_run_map_lulc_2025.png | 181 KB | Superseded first-run or per-year figure (do not use the numbers) |
| 03_Maps_and_Charts/​archive_superseded/​first_run_maps_check.jpg | 357 KB | Superseded first-run or per-year figure (do not use the numbers) |
| 03_Maps_and_Charts/​archive_superseded/​naming_aid_highlight_per_year.png | 131 KB | Superseded first-run or per-year figure (do not use the numbers) |
| 03_Maps_and_Charts/​archive_superseded/​naming_aid_highlight_pooled.png | 97 KB | Superseded first-run or per-year figure (do not use the numbers) |
| 03_Maps_and_Charts/​archive_superseded/​per_year_kmeans_clusters_2015.png | 802 KB | Superseded first-run or per-year figure (do not use the numbers) |
| 03_Maps_and_Charts/​archive_superseded/​per_year_kmeans_clusters_2020.png | 794 KB | Superseded first-run or per-year figure (do not use the numbers) |
| 03_Maps_and_Charts/​archive_superseded/​per_year_kmeans_clusters_2025.png | 801 KB | Superseded first-run or per-year figure (do not use the numbers) |
| 03_Maps_and_Charts/​charts/​chart_01_builtup_trend.png | 193 KB | Chart (PNG) |
| 03_Maps_and_Charts/​charts/​chart_02_landcover_by_year.png | 174 KB | Chart (PNG) |
| 03_Maps_and_Charts/​charts/​chart_03_zones.png | 224 KB | Chart (PNG) |
| 03_Maps_and_Charts/​charts/​chart_04_new_builtup_sources.png | 169 KB | Chart (PNG) |
| 03_Maps_and_Charts/​charts/​chart_05_accuracy_by_class.png | 228 KB | Chart (PNG) |
| 03_Maps_and_Charts/​charts/​chart_06_k_selection.png | 111 KB | Chart (PNG) |
| 03_Maps_and_Charts/​charts/​chart_07_stability.png | 52 KB | Chart (PNG) |
| 03_Maps_and_Charts/​charts/​chart_08_builtup_error_adjusted.png | 180 KB | Chart (PNG) |
| 03_Maps_and_Charts/​maps/​landsat_true_colour_2015.png | 2.8 MB | Map (PNG/JPG) |
| 03_Maps_and_Charts/​maps/​landsat_true_colour_2015_vs_2025.png | 2.5 MB | Map (PNG/JPG) |
| 03_Maps_and_Charts/​maps/​landsat_true_colour_2020.png | 2.7 MB | Map (PNG/JPG) |
| 03_Maps_and_Charts/​maps/​landsat_true_colour_2025.png | 2.8 MB | Map (PNG/JPG) |
| 03_Maps_and_Charts/​maps/​location_map.jpg | 642 KB | Map (PNG/JPG) |
| 03_Maps_and_Charts/​maps/​map_change_2015_2025.png | 169 KB | Map (PNG/JPG) |
| 03_Maps_and_Charts/​maps/​map_lulc_2015.png | 137 KB | Map (PNG/JPG) |
| 03_Maps_and_Charts/​maps/​map_lulc_2020.png | 137 KB | Map (PNG/JPG) |
| 03_Maps_and_Charts/​maps/​map_lulc_2025.png | 164 KB | Map (PNG/JPG) |
| 03_Maps_and_Charts/​maps/​validation_examples.png | 1.0 MB | Map (PNG/JPG) |
| 03_Maps_and_Charts/​screenshots/​README.md | 1 KB | Web map screenshot (taken offline, no background map) |
| 03_Maps_and_Charts/​screenshots/​webmap_01_overview_2025.png | 630 KB | Web map screenshot (taken offline, no background map) |
| 03_Maps_and_Charts/​screenshots/​webmap_02_change_2015_2025.png | 519 KB | Web map screenshot (taken offline, no background map) |
| 03_Maps_and_Charts/​screenshots/​webmap_03_search_kharar.png | 417 KB | Web map screenshot (taken offline, no background map) |
| 03_Maps_and_Charts/​screenshots/​webmap_04_hex_grid.png | 913 KB | Web map screenshot (taken offline, no background map) |
| 03_Maps_and_Charts/​screenshots/​webmap_05_east_zone_ranking.png | 726 KB | Web map screenshot (taken offline, no background map) |
| 03_Maps_and_Charts/​screenshots/​webmap_06_phone.png | 260 KB | Web map screenshot (taken offline, no background map) |
| 04_Data/​RESULTS_README.md | 8 KB | The results write-up |
| 04_Data/​landsat_composites/​landsat_composite_2015.qml | 2 KB | Landsat 8 March composite, 6 bands, reflectance × 10,000 (GeoTIFF + style) |
| 04_Data/​landsat_composites/​landsat_composite_2015.tif | 12.0 MB | Landsat 8 March composite, 6 bands, reflectance × 10,000 (GeoTIFF + style) |
| 04_Data/​landsat_composites/​landsat_composite_2020.qml | 2 KB | Landsat 8 March composite, 6 bands, reflectance × 10,000 (GeoTIFF + style) |
| 04_Data/​landsat_composites/​landsat_composite_2020.tif | 12.0 MB | Landsat 8 March composite, 6 bands, reflectance × 10,000 (GeoTIFF + style) |
| 04_Data/​landsat_composites/​landsat_composite_2025.qml | 2 KB | Landsat 8 March composite, 6 bands, reflectance × 10,000 (GeoTIFF + style) |
| 04_Data/​landsat_composites/​landsat_composite_2025.tif | 12.0 MB | Landsat 8 March composite, 6 bands, reflectance × 10,000 (GeoTIFF + style) |
| 04_Data/​landsat_composites/​scene_search_results.json | 3 KB | Landsat 8 March composite, 6 bands, reflectance × 10,000 (GeoTIFF + style) |
| 04_Data/​landsat_composites/​style_false_colour_NIR_red_green.qml | 2 KB | Landsat 8 March composite, 6 bands, reflectance × 10,000 (GeoTIFF + style) |
| 04_Data/​model_checks/​final_model_centres.npy | under 1 KB | Model checks and the final model's record |
| 04_Data/​model_checks/​final_model_training.json | under 1 KB | Model checks and the final model's record |
| 04_Data/​model_checks/​final_model_training_runs.json | under 1 KB | Model checks and the final model's record |
| 04_Data/​model_checks/​k_selection.png | 111 KB | Model checks and the final model's record |
| 04_Data/​model_checks/​model_checks.json | 6 KB | Model checks and the final model's record |
| 04_Data/​model_checks/​model_checks.md | 2 KB | Model checks and the final model's record |
| 04_Data/​model_checks/​naming_reference_centres.npy | under 1 KB | Model checks and the final model's record |
| 04_Data/​model_checks/​stability.png | 52 KB | Model checks and the final model's record |
| 04_Data/​rasters/​README.md | under 1 KB |  |
| 04_Data/​rasters/​clusters_2015.qml | 2 KB | The 10 K-means clusters (GeoTIFF + QGIS style) |
| 04_Data/​rasters/​clusters_2015.tif | 398 KB | The 10 K-means clusters (GeoTIFF + QGIS style) |
| 04_Data/​rasters/​clusters_2020.qml | 2 KB | The 10 K-means clusters (GeoTIFF + QGIS style) |
| 04_Data/​rasters/​clusters_2020.tif | 379 KB | The 10 K-means clusters (GeoTIFF + QGIS style) |
| 04_Data/​rasters/​clusters_2025.qml | 2 KB | The 10 K-means clusters (GeoTIFF + QGIS style) |
| 04_Data/​rasters/​clusters_2025.tif | 389 KB | The 10 K-means clusters (GeoTIFF + QGIS style) |
| 04_Data/​rasters/​first_run_sampling_strata/​lulc_2025_first_run.qml | 2 KB | First-run 2025 map: the sampling strata of the accuracy check |
| 04_Data/​rasters/​first_run_sampling_strata/​lulc_2025_first_run.tif | 209 KB | First-run 2025 map: the sampling strata of the accuracy check |
| 04_Data/​rasters/​lulc_2015.qml | 2 KB | Land-cover map (1 Built-up, 2 Cropland, 3 Trees, 5 Bare; GeoTIFF + QGIS style) |
| 04_Data/​rasters/​lulc_2015.tif | 158 KB | Land-cover map (1 Built-up, 2 Cropland, 3 Trees, 5 Bare; GeoTIFF + QGIS style) |
| 04_Data/​rasters/​lulc_2020.qml | 2 KB | Land-cover map (1 Built-up, 2 Cropland, 3 Trees, 5 Bare; GeoTIFF + QGIS style) |
| 04_Data/​rasters/​lulc_2020.tif | 157 KB | Land-cover map (1 Built-up, 2 Cropland, 3 Trees, 5 Bare; GeoTIFF + QGIS style) |
| 04_Data/​rasters/​lulc_2025.qml | 2 KB | Land-cover map (1 Built-up, 2 Cropland, 3 Trees, 5 Bare; GeoTIFF + QGIS style) |
| 04_Data/​rasters/​lulc_2025.tif | 191 KB | Land-cover map (1 Built-up, 2 Cropland, 3 Trees, 5 Bare; GeoTIFF + QGIS style) |
| 04_Data/​results.json | 9 KB | Every final number |
| 04_Data/​study_area/​README.md | under 1 KB | PRIVATE: GADM boundary and zone mask (do not publish) |
| 04_Data/​study_area/​Study_Area.zip | 7 KB | PRIVATE: GADM boundary and zone mask (do not publish) |
| 04_Data/​study_area/​zones_west1_east2.npy | 3.1 MB | PRIVATE: GADM boundary and zone mask (do not publish) |
| 04_Data/​tables/​01_area_by_class_ha.csv | under 1 KB | CSV table |
| 04_Data/​tables/​02_builtup_change.csv | under 1 KB | CSV table |
| 04_Data/​tables/​03_zones.csv | under 1 KB | CSV table |
| 04_Data/​tables/​04_from_to_2015_to_2025_ha.csv | under 1 KB | CSV table |
| 04_Data/​tables/​05_new_builtup_sources.csv | under 1 KB | CSV table |
| 04_Data/​tables/​06_accuracy_by_class.csv | under 1 KB | CSV table |
| 04_Data/​tables/​07_confusion_matrix_points.csv | under 1 KB | CSV table |
| 04_Data/​tables/​08_accuracy_summary.csv | under 1 KB | CSV table |
| 04_Data/​tables/​09_worldcover_comparison_2020.csv | under 1 KB | CSV table |
| 04_Data/​tables/​10_model_k_selection.csv | 1 KB | CSV table |
| 04_Data/​tables/​11_final_model_training_runs.csv | under 1 KB | CSV table |
| 04_Data/​tables/​12_superseded_300k_sample_runs.csv | under 1 KB | CSV table |
| 04_Data/​tables/​13_cluster_naming.csv | under 1 KB | CSV table |
| 04_Data/​tables/​14_landsat_scenes.csv | under 1 KB | CSV table |
| 04_Data/​tables/​15_hexagons_1km2_landcover_ha.csv | 109 KB | CSV table |
| 04_Data/​tables/​16_places_wikidata.csv | 2 KB | CSV table |
| 04_Data/​validation/​README.md | 1 KB | Accuracy-check data |
| 04_Data/​validation/​accuracy.json | 2 KB | Accuracy-check data |
| 04_Data/​validation/​chips/​ (160 files) | 23.7 MB | 160 photo chips, one per sample point (PRIVATE: Esri imagery) |
| 04_Data/​validation/​disagreements.txt | under 1 KB | Accuracy-check data |
| 04_Data/​validation/​disagreements_sheet.png | 2.5 MB | Accuracy-check data |
| 04_Data/​validation/​labels_A.csv | 6 KB | Accuracy-check data |
| 04_Data/​validation/​labels_B.csv | 4 KB | Accuracy-check data |
| 04_Data/​validation/​reference_labels.csv | 9 KB | Accuracy-check data |
| 04_Data/​validation/​sample_points.csv | 6 KB | Accuracy-check data |
| 04_Data/​validation/​sheets/​ (10 files) | 24.3 MB | 10 contact sheets of 16 chips (PRIVATE: Esri imagery) |
| 04_Data/​validation/​worldcover_check.json | 2 KB | Accuracy-check data |
| 05_Code/​ENVIRONMENT.md | 3 KB | Code |
| 05_Code/​HOW_TO_RUN.md | 8 KB | Code |
| 05_Code/​README.md | 5 KB | Code |
| 05_Code/​analysis/​accuracy.py | 3 KB | Code |
| 05_Code/​analysis/​build_composites.py | 4 KB | Code |
| 05_Code/​analysis/​cluster_pooled.py | 1 KB | Code |
| 05_Code/​analysis/​finalise.py | 5 KB | Code |
| 05_Code/​analysis/​make_chips.py | 4 KB | Code |
| 05_Code/​analysis/​model_checks/​common.py | 1 KB | Code |
| 05_Code/​analysis/​model_checks/​dbg.py | under 1 KB | Code |
| 05_Code/​analysis/​model_checks/​plots.py | 2 KB | Code |
| 05_Code/​analysis/​model_checks/​run1.py | 4 KB | Code |
| 05_Code/​analysis/​model_checks/​run2.py | 2 KB | Code |
| 05_Code/​analysis/​results.py | 6 KB | Code |
| 05_Code/​analysis/​results2.py | 6 KB | Code |
| 05_Code/​analysis/​train_full.py | 2 KB | Code |
| 05_Code/​analysis/​worldcover_check.py | 3 KB | Code |
| 05_Code/​demo/​recompute_accuracy.py | 4 KB | Code |
| 05_Code/​demo/​recompute_areas.py | 2 KB | Code |
| 05_Code/​gee/​export_landsat_composites.js | 4 KB | Code |
| 05_Code/​handover_tools/​build_master.py | 12 KB | Code |
| 05_Code/​handover_tools/​make_charts.py | 16 KB | Code |
| 05_Code/​handover_tools/​make_qgis_styles.py | 4 KB | Code |
| 05_Code/​handover_tools/​make_tables.py | 6 KB | Code |
| 05_Code/​handover_tools/​make_true_colour.py | 2 KB | Code |
| 05_Code/​handover_tools/​shots.js | 2 KB | Code |
| 05_Code/​helpers/​export_box.py | under 1 KB | Code |
| 05_Code/​helpers/​fetch_places.py | under 1 KB | Code |
| 05_Code/​helpers/​fetch_wikidata.py | under 1 KB | Code |
| 05_Code/​helpers/​highlight.py | 1 KB | Code |
| 05_Code/​helpers/​inspect_boundary.py | 2 KB | Code |
| 05_Code/​helpers/​phighlight.py | 1 KB | Code |
| 05_Code/​helpers/​search_scenes.py | 2 KB | Code |
| 05_Code/​helpers/​towns_check.py | under 1 KB | Code |
| 05_Code/​helpers/​union_check.py | 1 KB | Code |
| 05_Code/​requirements-demo.txt | under 1 KB | Code |
| 05_Code/​requirements.txt | under 1 KB | Code |
| 05_Code/​slides/​build_deck.js | 63 KB | Code |
| 05_Code/​superseded/​cluster_per_year.py | 3 KB | Code |
| 05_Code/​webmap/​build_webmap.py | 9 KB | Code |
| 05_Code/​webmap/​build_webmap_v1.py | 5 KB | Code |
| 05_Code/​webmap/​fetch_places_wikidata.py | under 1 KB | Code |
| 05_Code/​webmap/​leaflet-1.9.4.css | 15 KB | Code |
| 05_Code/​webmap/​places_wikidata_raw.json | 45 KB | Code |
| 05_Code/​webmap/​template.html | 37 KB | Code |
| 05_Code/​webmap/​template_v1.html | 17 KB | Code |
| 06_Web_Map/​LIVE_URL.txt | under 1 KB | Web map (offline copy and launchers) |
| 06_Web_Map/​run_local_mac_linux.sh | under 1 KB | Web map (offline copy and launchers) |
| 06_Web_Map/​run_local_windows.bat | under 1 KB | Web map (offline copy and launchers) |
| 06_Web_Map/​site/​LEAFLET_LICENSE.txt | 1 KB | Web map (offline copy and launchers) |
| 06_Web_Map/​site/​data/​hex.geojson | 509 KB | Web map (offline copy and launchers) |
| 06_Web_Map/​site/​data/​places.json | 3 KB | Web map (offline copy and launchers) |
| 06_Web_Map/​site/​index.html | 53 KB | Web map (offline copy and launchers) |
| 06_Web_Map/​site/​layers/​lulc_2015.png | 157 KB | Web map (offline copy and launchers) |
| 06_Web_Map/​site/​layers/​lulc_2020.png | 155 KB | Web map (offline copy and launchers) |
| 06_Web_Map/​site/​layers/​lulc_2025.png | 192 KB | Web map (offline copy and launchers) |
| 06_Web_Map/​site/​leaflet.js | 148 KB | Web map (offline copy and launchers) |
| 07_Teacher_Prep/​Screenshot_Checklist.docx | 14 KB | Teacher prep |
| 07_Teacher_Prep/​Screenshot_Checklist.md | 5 KB | Teacher prep |
| 07_Teacher_Prep/​Screenshot_Checklist.pdf | 91 KB | Teacher prep |
| 07_Teacher_Prep/​Teacher_QA_and_Demo.docx | 31 KB | Teacher prep |
| 07_Teacher_Prep/​Teacher_QA_and_Demo.md | 39 KB | Teacher prep |
| 07_Teacher_Prep/​Teacher_QA_and_Demo.pdf | 236 KB | Teacher prep |
| 08_Project_Notes/​01_message_to_teacher.md | 2 KB | Planning notes |
| 08_Project_Notes/​02_teacher_brief_and_slide_list.md | 3 KB | Planning notes |
| 08_Project_Notes/​03_get_satellite_images.md | 4 KB | Planning notes |
| 08_Project_Notes/​04_qgis_steps.md | 10 KB | Planning notes |
| 08_Project_Notes/​05_metrics_and_formulas.md | 5 KB | Planning notes |
| 08_Project_Notes/​repository_README.md | 5 KB | Planning notes |
| LICENSE | 1 KB | MIT licence for the code |
| LICENSE-DATA.md | 2 KB | CC BY 4.0 for maps and figures; third-party credits |
