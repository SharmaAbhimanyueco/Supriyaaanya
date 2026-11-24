# Results (final model, 25 November 2026)

**Short version:** built-up land grew from **7,844 ha (2015) to 14,786 ha (2025)**, an increase of **+6,942 ha (+89%)**, or **6.3% a year**. Growth sped up after 2020: 4.9% a year in 2015–2020, then 7.8% a year in 2020–2025. The West zone (Kharar–Mohali) grew faster than the East zone (Dera Bassi–Zirakpur). Two-thirds of the new built-up land (6,916 ha, 68%) was cropland in 2015.

**Read these together with the accuracy check below.** The map undercounts built-up land: it finds about half of the real built-up area. The corrected 2025 estimate is about **17,700 ± 4,600 ha**. The trend, the speed-up after 2020 and the West-versus-East pattern are the reliable findings. Treat the exact hectares as conservative estimates.

Two more points to say openly in the presentation:
- The analysis was run in **Python, not QGIS**. If the teacher wants QGIS, the composite images in `images/` can be clustered there by following [04_qgis_steps.md](../04_qgis_steps.md).
- The photo labels used in the accuracy check came from **AI-assisted interpretation** (two independent Claude Sonnet agents). The students should spot-check a sample of them.

## How the results were made

- **Images:** Landsat 8 Collection 2 Level-2 surface reflectance, path 147 row 39, downloaded from Microsoft Planetary Computer. Two clear March scenes per year: 7 and 23 March 2015, 4 and 20 March 2020, 2 and 18 March 2025.
- **Composite:** clouds, shadows and fill were masked using QA_PIXEL, and the two scenes were combined with a median. The result is one six-band image per year.
- **Clip:** each image was cut to the study-area boundary in UTM zone 43N (EPSG:32643). That leaves 1,209,178 pixels of 30 m, about 108,800 ha.
- **Model:** K-means with 10 clusters (scikit-learn), **trained on all 3,626,753 valid pixels from the three years**. It used the best of 10 starts and up to 300 iterations. The same trained model was then applied to every year, so each cluster means the same thing in every year.
- **Naming:** clusters were named from where they fall (towns, roads, the northern hills, fields) and from true-colour images. Each final cluster was matched to the nearest cluster of the first version, which had been named that way.
- **Area:** pixel count × 0.09 ha.

### Naming table

| Cluster | Land type |
|---|---|
| 1 | Bare/fallow |
| 2 | **Built-up** |
| 3, 5 | Trees/vegetation |
| 4, 6, 7, 8, 9, 10 | Cropland |

No cluster picked out water, because the water bodies are too small at 30 m.

## Model checks: is it suitable and properly trained?

- **Training converged.** Three independent training runs on all the pixels (seeds 0, 1 and 2, each the best of 10 starts) converged in 35, 31 and 29 iterations. Their final fits (inertia) were 5243.40, 5243.77 and 5243.46, which differ by less than 0.01%. Their groupings were very similar too (adjusted Rand index 0.95–0.97).
- **The answer is stable.** Built-up area across the three runs was 7,844–7,920 ha in 2015, 10,033–10,104 ha in 2020 and 14,737–14,841 ha in 2025, all within 1%.
- **Why the model was retrained.** The first version was trained on a 300,000-pixel sample. Retraining it with other samples moved 2015 built-up between 6,698 and 8,177 ha, so it was replaced by the full-data model. See `model_checks/`.
- **Number of clusters.** The elbow of the inertia curve is at k = 8, and k = 7–10 all score within about 10% of the best elbow value. The silhouette score is highest at k = 4 but nearly flat (0.29–0.33) from 5 to 16 clusters. Using more clusters than final land types is normal for unsupervised classification, because clusters are merged into land types afterwards. k = 10 is within the sensible range.

## Area by land type (hectares)

| Land type | 2015 | 2020 | 2025 |
|---|---|---|---|
| Built-up | 7,844 | 10,033 | 14,786 |
| Cropland | 81,218 | 77,204 | 66,728 |
| Trees/vegetation | 14,255 | 17,150 | 22,299 |
| Bare/fallow | 5,482 | 4,439 | 4,970 |
| Total | 108,799 | 108,826 | 108,783 |
| Built-up share | 7.2% | 9.2% | 13.6% |

## Built-up change

| Period | Increase (ha) | ha per year | % change | Yearly rate (SDG 11.3.1 formula) |
|---|---|---|---|---|
| 2015–2020 | +2,190 | 438 | +27.9% | 4.92% |
| 2020–2025 | +4,753 | 951 | +47.4% | 7.76% |
| 2015–2025 | +6,942 | 694 | +88.5% | 6.34% |

## By zone

The zones are the two pieces of the GADM boundary file. They are not official tehsil outlines.

| Zone | Area (ha) | Built-up 2015 | 2020 | 2025 | Share 2015 → 2025 | UEII 2015–2025 | Yearly rate |
|---|---|---|---|---|---|---|---|
| West (Kharar and Mohali) | 71,195 | 4,336 | 6,151 | 9,236 | 6.1% → 13.0% | 0.69 (medium) | 7.6% |
| East (Dera Bassi, incl. Zirakpur) | 37,604 | 3,507 | 3,879 | 5,545 | 9.3% → 14.8% | 0.54 (low) | 4.6% |
| Whole study area | 108,799 | 7,844 | 10,033 | 14,786 | 7.2% → 13.6% | 0.64 | 6.3% |

## Cropland and change noise (2015 → 2025)

- 10,170 ha became built-up. Of this, **6,916 ha (68%) was cropland in 2015**.
- 3,225 ha were mapped as built-up in 2015 but not in 2025. Built-up land rarely turns back into farmland, so this is mostly classification noise.

## Accuracy check

**Photo check (2025 map).** 160 random points were drawn, stratified by map class: 50 built-up, 50 cropland, 30 trees and 30 bare. Each was cut from Esri World Imagery as a photo about 300 m across, with the 30 m pixel marked. Two independent AI-assisted interpreters labelled every point without seeing the map. They agreed on 144 of 160 points (90%), and on 152 of 160 (95%) for built-up versus not. The 16 disagreements were settled by a third look. Two points under cloud were dropped, leaving 158. Accuracies are area-weighted (Olofsson et al., 2014).

| | Result |
|---|---|
| Overall accuracy (4 land types) | **74.6%** |
| Built-up vs not built-up | **87.0%** |
| Built-up: of map built-up, % really built-up (user's accuracy) | 62.0% |
| Built-up: of real built-up, % found by the map (producer's accuracy) | 51.9% |
| Cropland (user's / producer's) | 84.3% / 87.1% |
| Trees/vegetation (user's / producer's) | 61.8% / 68.7% |
| Bare/fallow (user's / producer's) | 35.7% / 27.8% |
| Corrected built-up area 2025 (95% range) | **17,706 ± 4,648 ha** (map: 14,786 ha) |

Point counts (rows = map, columns = photo):

| Map \ Photo | Built-up | Cropland | Trees | Bare |
|---|---|---|---|---|
| Built-up | 30 | 8 | 5 | 5 |
| Cropland | 4 | 47 | 6 | 3 |
| Trees/vegetation | 8 | 8 | 20 | 0 |
| Bare/fallow | 7 | 2 | 0 | 5 |

**Independent map (ESA WorldCover 2020, 10 m), compared with our 2020 map:**
- 92.8% agreement on built-up versus not.
- 70.9% of our built-up pixels are built-up in WorldCover, and we find 59.1% of WorldCover's built-up land.
- Our built-up pixels are on average 69% built-up in WorldCover, against 5% for all other pixels.
- WorldCover finds 12,181 ha built-up in 2020, against our 10,033 ha. That is the same undercount the photo check shows.

## Files

| Folder | Contents |
|---|---|
| `maps/` | Land-cover maps for 2015, 2020 and 2025, the built-up change map, and the validation examples (PNG) |
| `rasters/` | `lulc_YEAR.tif` (1 Built-up, 2 Cropland, 3 Trees/vegetation, 5 Bare/fallow) and `clusters_YEAR.tif` (clusters 1–10) |
| `images/` | Landsat composites for each year: 6 bands, reflectance × 10,000, NoData −32768. Ready for QGIS |
| `model_checks/` | The number-of-clusters and stability checks, and the final model's training record |
| `validation/` | Sample points, both interpreters' labels, the agreed reference labels, and the accuracy and WorldCover results |
| `results.json` | Every number above |
| `../scripts/analysis/` | The Python scripts. The final results come from `train_full.py`, `results2.py`, `accuracy.py` and `finalise.py`; the earlier first-run scripts are kept for the record |
