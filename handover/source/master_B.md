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
