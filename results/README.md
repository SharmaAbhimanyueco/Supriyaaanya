# Results: first run (24 November 2026)

These results are **estimates**. The clusters were named from where they fall and from true-colour images, but they have **not yet been checked against high-resolution imagery**. The analysis was run in **Python, not QGIS**. If the teacher wants QGIS, the composite images in `images/` can be clustered again by following [04_qgis_steps.md](../04_qgis_steps.md).

## How the results were made

- **Images:** Landsat 8 Collection 2 Level-2 surface reflectance, path 147, row 39, downloaded from Microsoft Planetary Computer. Two clear March scenes per year: 7 and 23 March 2015, 4 and 20 March 2020, 2 and 18 March 2025.
- **Composite:** clouds, cloud shadows and fill pixels were masked using the QA_PIXEL band. The two scenes were then combined with a median, giving one image per year with six bands (blue, green, red, NIR, SWIR1, SWIR2).
- **Clip:** each image was cut to the study-area boundary in UTM zone 43N (EPSG:32643). That leaves 1,209,178 pixels of 30 m.
- **Clustering:** K-means with 10 clusters (scikit-learn; 5 starts, up to 100 iterations, random seed 42). It was fitted on 100,000 sampled pixels from each year and applied to all three years, so each cluster number means the same thing in every year. Clustering each year separately had made 2020 look more built-up than 2025, which is not realistic.
- **Area:** pixel count × 0.09 ha.

## Naming table

| Cluster | What it looks like | Class |
|---|---|---|
| 1 | Bright bare surfaces, scattered | Bare/fallow |
| 2 | Towns (Kurali, Kharar, Mohali, Zirakpur, Dera Bassi, Lalru) and road corridors | **Built-up** |
| 3 | Scattered low-vegetation fields and town edges | Bare/fallow |
| 4 | Dark vegetation in the northern hills | Trees/vegetation |
| 5 | Thin or young crops | Cropland |
| 6 | Scrub in the hills, plus some crops | Trees/vegetation |
| 7–10 | Green wheat | Cropland |

No cluster picked out water: the water bodies are too small at 30 m.

## Area by class (hectares)

| Class | 2015 | 2020 | 2025 |
|---|---|---|---|
| Built-up | 6,609 | 9,224 | 14,529 |
| Cropland | 76,708 | 72,630 | 62,014 |
| Trees/vegetation | 15,495 | 17,661 | 21,598 |
| Bare/fallow | 9,987 | 9,311 | 10,642 |
| Total | 108,799 | 108,826 | 108,783 |
| Built-up share | 6.1% | 8.5% | 13.4% |

The totals differ by a few hectares because a handful of pixels had no clear view in that year.

## Built-up change

| Period | Increase (ha) | ha per year | % change | Land consumption rate (% per year) |
|---|---|---|---|---|
| 2015–2020 | +2,615 | 523 | +39.6% | 6.67 |
| 2020–2025 | +5,305 | 1,061 | +57.5% | 9.09 |
| 2015–2025 | +7,920 | 792 | +119.8% | 7.88 |

The land consumption rate uses the SDG 11.3.1 formula: ln(later ÷ earlier) ÷ years × 100.

## By zone

The two zones are the two pieces of the GADM boundary file. They are not official tehsil outlines.

| Zone | Zone area (ha) | Built-up 2015 (ha) | Built-up 2020 (ha) | Built-up 2025 (ha) | Share 2015 → 2025 | UEII 2015–2025 |
|---|---|---|---|---|---|---|
| West (Kharar and Mohali) | 71,195 | 3,742 | 5,572 | 9,030 | 5.3% → 12.7% | 0.74 |
| East (Dera Bassi, incl. Zirakpur) | 37,604 | 2,867 | 3,649 | 5,496 | 7.6% → 14.6% | 0.70 |

Both zones fall in the "medium" UEII band (0.59–1.05).

## Cropland and change noise (2015 → 2025)

- 10,388 ha became built-up. Of this, **5,409 ha (52%) was cropland in 2015**.
- 2,464 ha were mapped as built-up in 2015 but not in 2025. Built-up land rarely turns back into farmland, so this points to classification noise. The net increase is 7,920 ha.
- Some cropland shows up as trees or bare land in other years because the crops were at different stages each March.

## Files

| Folder | Contents |
|---|---|
| `maps/` | LULC maps for 2015, 2020 and 2025, and the built-up change map (PNG) |
| `rasters/` | `lulc_YEAR.tif` (1 Built-up, 2 Cropland, 3 Trees/vegetation, 5 Bare/fallow) and `clusters_YEAR.tif` (clusters 1–10) |
| `images/` | Landsat composites for each year: 6 bands, reflectance × 10,000, NoData −32768. Ready for QGIS |
| `results.json` | Every number above, including the full from–to table |
| `../scripts/analysis/` | The Python scripts that produced these results |
