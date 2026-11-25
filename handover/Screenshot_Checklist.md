# Screenshot checklist

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
| `screenshots/webmap_02_compare_2015_2025.png` | 20, or 15 (how much and how fast) |
| `screenshots/webmap_03_search_kharar.png` | 20 |
| `screenshots/webmap_04_hex_grid.png` | 16 (where growth happened) |
| `screenshots/webmap_05_tour_change.png` | 20 (the guided tour) |
| `screenshots/webmap_06_phone.png` | 20 (works on a phone) |
| `screenshots/webmap_07_satellite_compare.png` | 9 (what the satellite sees) |

---

