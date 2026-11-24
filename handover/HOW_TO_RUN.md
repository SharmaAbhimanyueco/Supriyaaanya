# How to run the code

Run every command from inside the `Urban_Growth_Handover` folder unless a step says otherwise. Sections A–C need no internet once Python is installed; D and E need internet.

## A. Quick checks on a laptop (about 10 minutes the first time)

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

## B. The web map without internet

- **Windows:** double-click `06_Web_Map/run_local_windows.bat`. **Mac/Linux:** run `sh 06_Web_Map/run_local_mac_linux.sh`. Either one starts a small local web server and opens http://localhost:8000 in the browser. Keep the window open while you use the map; close it (or press Ctrl+C) to stop.
- Offline, these all work: the land-cover layers, filters, live figures, the 1 km² grid, the rankings, and search over the built-in place list. Only the background map and the online search for other places need internet.
- Don't double-click `index.html` directly. Browsers block a page opened as a file from reading its data files, so the grid and the place list would not load.
- The live copy is at https://sharmaabhimanyueco.github.io/Supriyaaanya/ (see `06_Web_Map/LIVE_URL.txt`).

## C. Open the results in QGIS

1. Install QGIS (the current Long Term Release from qgis.org).
2. Drag `04_Data/rasters/lulc_2025.tif` into QGIS. The colours and names load by themselves from `lulc_2025.qml`, which sits next to it with the same name. The same applies to 2015, 2020 and the `clusters_*.tif` files.
3. Drag in `04_Data/landsat_composites/landsat_composite_2025.tif`. It opens in true colour (red = band 3, green = band 2, blue = band 1). For false colour, where plants show red: Layer Properties → Symbology → Style → Load Style → `style_false_colour_NIR_red_green.qml`.
4. To recount areas inside QGIS, open the Processing Toolbox and run **Raster layer unique values report** on `lulc_2025.tif`. Multiply each pixel count by 0.09 to get hectares (1 = Built-up, 2 = Cropland, 3 = Trees/vegetation, 5 = Bare/fallow).
5. For the study area outline, unzip `04_Data/study_area/Study_Area.zip` and add `study_area.shp`. Don't show its "Kharar"/"Rajpura" labels: they are wrong (see the master document, Part 3).

## D. Re-run the whole analysis (advanced; needs internet)

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

## E. Rebuild the web map

Use the GitHub repository rather than this package, because the build script expects the repository's folder layout:

```
git clone https://github.com/SharmaAbhimanyueco/Supriyaaanya
cd Supriyaaanya
git checkout claude/urban-growth-mapping-handover-xkppdn
python -I scripts/webmap/build_webmap.py . <path to 04_Data/study_area/zones_west1_east2.npy>
```

It rewrites `webmap/index.html`, `webmap/layers/` and `webmap/data/`. To publish, copy the contents of `webmap/` to the `gh-pages` branch and push. GitHub Pages serves that branch.

## F. The slides and this package's charts

- The deck is built by `05_Code/slides/build_deck.js`, which also needs a theme helper that is not included. To change the slides, edit `02_Presentation/Urban_Growth_Mohali_slides.pptx` directly in PowerPoint or Google Slides.
- The charts, CSV tables and QGIS styles in this package can be rebuilt with:

```
python 05_Code/handover_tools/make_charts.py 04_Data/results.json 03_Maps_and_Charts/charts
python 05_Code/handover_tools/make_tables.py 04_Data/results.json 06_Web_Map/site/data 04_Data/tables
python 05_Code/handover_tools/make_qgis_styles.py 04_Data
```

`make_charts.py` needs matplotlib, and `make_qgis_styles.py` needs numpy and rasterio.
