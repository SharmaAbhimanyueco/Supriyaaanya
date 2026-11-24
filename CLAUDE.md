# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is

This is a student semester project by Supriya Mahshere and Aanya Upadhyay. It maps urban growth (land use / land cover, LULC) in S.A.S. Nagar (Mohali) district, Punjab, covering Mohali, Kharar, Zirakpur and Dera Bassi. It uses Landsat 8 images from March 2015, 2020 and 2025, classified with unsupervised K-means.

- **Theme:** urbanisation. Farmland loss is a supporting finding only.
- **Deliverables:** the slide deck (`slides/`), the results (`results/`), and the web map (`webmap/`, see below). The teacher's plan was qgis2web on GitHub Pages.
- **Audience:** the students are beginners. Explain technical terms in plain words with an everyday analogy, and pace advice one step at a time.

## Sources of truth (read these instead of re-deriving)

- `results/results.json` holds **every final number**. Never hand-type figures into slides or docs; read them from this file. `results/README.md` is the human-readable version: method, naming table, tables, accuracy.
- `02_teacher_brief_and_slide_list.md` holds the teacher's procedure and slide list. It is the handover's summary, not her words.
- `01_message_to_teacher.md` holds the open questions to the teacher, all still unanswered. Anything marked **UNCONFIRMED** waits on her: satellite/years, K-means vs ISODATA, validation level, the web map tool, the deadline/format, and the missing slide 16.
- `README.md` is the start-here plan, the file map and the warnings.

## Key facts

- **Study area.** The GADM boundary comes from `Study_Area.zip`, which is not in the repo because GADM's licence forbids redistribution. Its two polygons are mislabelled: "Kharar" is Kharar + Mohali, and "Rajpura" is Dera Bassi including Zirakpur (Rajpura town is outside). They are used as the **West/East zones, not official tehsils**. The area is 1,209,178 pixels of 30 m, about 108,800 ha.
- **Grid.** EPSG:32643 (UTM 43N), 30 m pixels, 1 pixel = 0.09 ha. The working grid is 1409 × 2170.
- **Scenes.** Landsat 8 Collection 2 Level-2, path 147 row 39, from Microsoft Planetary Computer: 2015-03-07 and 03-23, 2020-03-04 and 03-20, 2025-03-02 and 03-18. QA_PIXEL bits 0–4 are masked, then a median composite is taken.
- **Codes in `lulc_*.tif`.** 1 Built-up, 2 Cropland, 3 Trees/vegetation, 5 Bare/fallow, 0 nodata. Code 4 (Water) is unused because no water cluster appeared. Colours: B03A2E, 8DB63C, 2E6B3F, (2F7FB0), D9A441.
- **Final model.** KMeans with k=10, n_init=10, max_iter=300, seed 0, fitted on all 3,626,753 pixels pooled from the three years. Clusters are renumbered by the NDVI of their centre. Naming: 1 Bare; 2 Built-up; 3 and 5 Trees; 4 and 6–10 Cropland. Each cluster takes the name of its nearest centre in `results/model_checks/naming_reference_centres.npy` (the first-run clusters, which were named by location and colour).
- **Headline.** Built-up 7,844 → 10,033 → 14,786 ha (+6,942 ha, +88.5%). Yearly rate 6.34% (4.92% → 7.76%), using the SDG 11.3.1 formula ln(B2/B1)/years. UEII: West 0.69, East 0.54. Cropland → built-up: 6,916 ha (68% of new built-up).
- **Accuracy** (2025 map, 158 photo-checked points, Olofsson area-weighted):
  - Overall 74.6%; built-up vs not 87.0%; built-up user's/producer's 62.0% / 51.9%.
  - Error-adjusted built-up for 2025 is 17,706 ± 4,648 ha, so the map **undercounts**.
  - ESA WorldCover 2020: 92.8% agreement.
- **Superseded numbers.** 6,609 → 14,529 ha (+120%) came from an earlier model trained on a 300k-pixel sample, which was unstable when retrained. Do not use these.

## Rules for this project (from the handover)

- Never invent data, figures, dates or official facts. SDG wording, administrative boundaries, GMADA/PUDA details and satellite specifications must be verified on official sources.
- Always disclose three things:
  - The analysis ran in Python, while the teacher asked for QGIS.
  - The photo labels are AI-assisted (two blind Sonnet raters, disagreements settled by a third look), so the students should spot-check them.
  - The hectares are conservative estimates.
- Don't commit GADM boundary files or Esri imagery chips, for licence reasons.

## Analysis pipeline (`scripts/analysis/`)

Python needs numpy, rasterio, scikit-learn, pystac-client, planetary-computer, pyshp, shapely, pyproj, matplotlib, pillow and requests. Run scripts with `python -I`. In the cloud container, set `REQUESTS_CA_BUNDLE=/root/.ccr/ca-bundle.crt`.

The network hosts needed are planetarycomputer.microsoft.com and landsateuwest.blob.core.windows.net (Landsat), ai4edataeuwest.blob.core.windows.net (WorldCover) and server.arcgisonline.com (Esri chips). They are allowed in the cloud environment "Supriyaaanya".

The scripts take paths as arguments and assume this layout under a work root `W`:

| Folder | Contents |
|---|---|
| `W/analysis` | composites, `inside.npy`, first-run outputs |
| `W/analysis2` | final outputs |
| `W/validation` | |
| `W/diagnostics` | |

Run order:
1. `build_composites.py <study_area.shp> W/analysis` writes `composite_YYYY.tif` and `inside.npy`.
2. `cluster_pooled.py W/analysis`, then `results.py W/analysis <shp>`. This is the first run. It provides `pooled_centres.npy` (the naming reference) and the first-run `lulc_2025.tif`, which supplies the sampling strata and the reference grid.
3. `worldcover_check.py W/analysis W/validation` writes `wc_builtup_frac_{2020,2021}.npy`.
4. `train_full.py W/analysis W/analysis2`, then `results2.py W/analysis W/analysis2 <shp> W/validation`. This produces the final rasters, `results2.json` and `zones.npy`.
5. `make_chips.py W/analysis W/validation` draws the stratified sample (50/50/30/30 from the first-run 2025 map) and the Esri chips. Label them blind, then write `reference_labels.csv` (format in `results/validation/`).
6. `accuracy.py W/validation W/analysis/lulc_2025.tif W/analysis2/lulc_2025.tif`.
7. `model_checks/*.py` runs the k sweep 4–16 and the seed/sample stability checks on the 300k sample. Set `LULC_WORK=W` first (`common.py` reads it).
8. `finalise.py W` writes the maps, `validation_examples.png` and `final.json`. Copy these to `results/results.json` and `results/maps/`.

The CA-bundle setting for GDAL is applied only when `/root/.ccr/ca-bundle.crt` exists, so the scripts also run on a laptop. Quick checks that need only numpy, rasterio and pyproj: `scripts/demo/recompute_areas.py results/rasters` and `scripts/demo/recompute_accuracy.py results` (both reproduce `results.json` exactly; the second uses `results/rasters/first_run_sampling_strata/`). QGIS styles (`.qml`) sit next to every raster in `results/rasters/` and `results/images/`.

## Slides

`slides/Urban_Growth_Mohali_slides.pptx` and its `.pdf` are generated. Do not hand-edit numbers in them. The source is `scripts/slides/build_deck.js`, which reads `results/results.json`, `results/maps/*.png`, `slides/assets/location_map.jpg` and `slides/assets/webmap_dashboard.jpg` (slide 20 shows the real dashboard; its notes say it is Leaflet, not qgis2web).

To rebuild:
1. Run `npm install pptxgenjs react-icons react react-dom sharp`.
2. Run `PPTX_SKILL_DIR=<pptx skill folder> NODE_PATH=<node_modules> node scripts/slides/build_deck.js out.pptx`.
3. Validate and render with the pptx skill's `scripts/office/validate.py` and `soffice.py`.

The 24 slides follow the teacher's list, plus four additions:
- slides 9–12: plain-language explainers
- slides 17–19: model and accuracy checks
- slide 23: glossary
- two Results slides (15–16)

## Web map (open-source dashboard)

`webmap/` is a static site built by `python -I scripts/webmap/build_webmap.py <repo root> <W/analysis2/zones.npy>`. It regenerates `index.html`, `layers/lulc_YYYY.png` (EPSG:3857), `data/hex.geojson` (1 km² hexagons with land-cover hectares per year) and `data/places.json` (Wikidata places, CC0; raw copy in `scripts/webmap/places_wikidata_raw.json`).
- The layout lives in `scripts/webmap/template.html`. Leaflet 1.9.4 loads from cdnjs, and its CSS is inlined from `scripts/webmap/leaflet-1.9.4.css`.
- Everything is computed in the browser: it decodes the PNG layers into class arrays for filtering, radius statistics and rankings. Online search uses Photon (photon.komoot.io), which only works when the site is hosted.
- To test locally, serve the folder over HTTP (`python -m http.server`), because `file://` blocks fetch.
- The v1 files (`*_v1.*`) are the older static map, kept for reference.
- Licences: code MIT (`LICENSE`); maps and figures CC BY 4.0 (`LICENSE-DATA.md`).
- Don't add the GADM zone polygons to the page (licence). The hexagons carry only a `z` (W/E) label.

## Handover package

- `handover/` holds the master document (`Master_Document_Urban_Growth_Mohali.docx/.pdf`, source `.md`), the teacher Q&A and demo pack, the screenshot checklist, `ENVIRONMENT.md`, `HOW_TO_RUN.md`, 8 charts, 6 offline web map screenshots and 16 CSV tables. `handover/README.md` maps the package layout to the repo.
- The full private package (`00_READ_ME_FIRST.md` to `08_Project_Notes/`, about 131 MB zipped) also holds the GADM boundary, the zone mask, the 160 Esri chips and an offline web map copy with launchers. It was built in the session scratchpad and sent to the user; it is not committed.
- Builders in `scripts/handover/`: `make_charts.py`, `make_tables.py`, `make_qgis_styles.py`, `make_true_colour.py`, `build_master.py` (pandoc + python-docx + LibreOffice), `shots.js` (Playwright screenshots). Chart colours are the map colours, with trees stepped to #2A6E3A so the palette passes the colour check.

## Git

- `main` holds only the user's own README "first commit".
- `claude/urban-growth-mapping-handover-xkppdn` holds all project work. Push with `git push origin claude/urban-growth-mapping-handover-xkppdn`.
- `gh-pages` holds only the built site: the contents of `webmap/` (`index.html`, `layers/`, `data/`, README and licences) and `.nojekyll`. To refresh it after rebuilding, recreate the branch from `webmap/` (build a commit from a temporary index with `git --work-tree=webmap add index.html layers data`) and push.
- The repo is public, and GitHub Pages serves `gh-pages` at https://sharmaabhimanyueco.github.io/Supriyaaanya/. The user turns Pages on in Settings → Pages.
- Push access works since 25 Nov 2026, when the user installed the Claude GitHub App.
