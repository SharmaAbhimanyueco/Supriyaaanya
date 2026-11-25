# Where the code was run

All the analysis, the slides and the web map were produced on **24 November 2026** in one place: a **cloud Linux computer** rented for the session, not a student laptop. It was a Claude Code on the web session (Anthropic's AI coding assistant), which wrote and ran the scripts at the project team's request. The data was streamed over the internet from public sources. Nothing was installed on a personal computer.

## The machine

| Item | Value |
|---|---|
| Operating system | Ubuntu 24.04.5 LTS (Linux, x86_64) |
| Processor and memory | 4 CPU cores, 15 GB RAM |
| Python | 3.13.18, in a virtual environment |
| Python packages | numpy 2.5.5, rasterio 1.5.2 (with GDAL 3.12.2), scikit-learn 1.9.1, scipy 1.18.1, pystac-client 0.9.1, planetary-computer 1.0.0, pyshp 3.1.9, shapely 2.2.0, pyproj 3.8.0, matplotlib 3.11.2, pillow 13.0.0, requests 2.34.2 |
| Node.js (slides, screenshots) | v22.23.5 with pptxgenjs 4.0.1, react 19.3.1, react-dom 19.3.1, react-icons 5.7.0, sharp 0.35.5; Playwright 1.63.0 with Chromium |
| Office tools | LibreOffice 24.2.7.2 (PowerPoint to PDF), pandoc 3.1.3 (master document) |

## The data sources it reached over the internet

| Source | What came from it | Used by |
|---|---|---|
| Microsoft Planetary Computer (planetarycomputer.microsoft.com, landsateuwest.blob.core.windows.net) | Landsat 8 Collection 2 Level-2 scenes, path 147 row 39 | `analysis/build_composites.py`, `helpers/search_scenes.py` |
| ESA WorldCover on Planetary Computer storage (ai4edataeuwest.blob.core.windows.net) | WorldCover 2020 and 2021 built-up maps (10 m) | `analysis/worldcover_check.py` |
| Esri World Imagery (server.arcgisonline.com) | Photo chips for the accuracy check (kept private, not published) | `analysis/make_chips.py` |
| Wikidata Query Service (query.wikidata.org) | Names and positions of towns and villages for the web map search (CC0) | `webmap/fetch_places_wikidata.py` |
| GitHub (github.com) | Code repository | git |
| Codeberg (codeberg.org, Codeberg Pages) | A copy of the code, and free hosting of the web map | git, Codeberg API |

## What was not used

- **QGIS** was not used for the analysis. The teacher asked for QGIS; say this openly. Every output opens in QGIS, and `08_Project_Notes/04_qgis_steps.md` describes the QGIS route.
- **Google Earth Engine** was not used. `gee/export_landsat_composites.js` is an alternative way to download the images and was never run.

## Which step ran where

Every script listed in `README.md` ran on the machine above, in the order given in `HOW_TO_RUN.md`. The model checks in `analysis/model_checks/` ran there too, through helper agents of the same session. The photo labels for the accuracy check (`04_Data/validation/labels_A.csv` and `labels_B.csv`) came from two independent AI raters (Claude Sonnet) that could not see the map. Disagreements were settled by a third look. The students should spot-check these labels.

## Can it run on a laptop?

Yes. The two demo scripts in `demo/` run on any laptop in seconds. They need Python 3.10 or newer and the three libraries in `requirements-demo.txt`. The full pipeline also runs on a laptop with internet access. The final model trains on 3.6 million pixels, three times over, so that step takes much longer than the rest. See `HOW_TO_RUN.md`.
