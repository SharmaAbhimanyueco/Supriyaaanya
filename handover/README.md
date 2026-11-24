# Handover

This folder holds the handover documents for the project, plus the charts, screenshots and tables made for them.

| File | What it is |
|---|---|
| `Master_Document_Urban_Growth_Mohali.pdf` / `.docx` | The master document, A to Z: concepts in plain words, data, the method with the reason for each choice, results, accuracy, limitations, decisions log, where the code ran, how to re-run it, teacher Q&A, glossary, references and the file list |
| `Master_Document_source.md` | The same text as Markdown. Rebuild with `scripts/handover/build_master.py` |
| `Teacher_QA_and_Demo.pdf` / `.docx` / `.md` | Numbers cheat sheet, the 60-second story, the three disclosures, 58 likely questions with answers, demo scripts, and a day-before checklist |
| `Screenshot_Checklist.pdf` / `.docx` / `.md` | Screenshots to take yourselves, and which slide each one goes on |
| `ENVIRONMENT.md`, `HOW_TO_RUN.md` | Where the code ran, and how to run it again |
| `charts/` | Eight charts (PNG), all drawn from `results/results.json` by `scripts/handover/make_charts.py` |
| `screenshots/` | Six web map screenshots, taken offline, so without the background map |
| `tables/` | Every result as CSV, for Excel or Google Sheets |
| `source/` | The chapters the master document was assembled from |

## The full package

The documents were written for a complete handover package (a zip with folders `00_READ_ME_FIRST.md` to `08_Project_Notes/`), so their file paths use that layout. In this repository the same files live here:

| Package folder | In this repository |
|---|---|
| `01_Master_Document/`, `07_Teacher_Prep/` | `handover/` |
| `02_Presentation/` | `slides/` |
| `03_Maps_and_Charts/maps/` | `results/maps/` (plus `slides/assets/location_map.jpg`) |
| `03_Maps_and_Charts/charts/`, `screenshots/` | `handover/charts/`, `handover/screenshots/` |
| `04_Data/` | `results/`: `results.json`, `rasters/`, `images/` (the Landsat composites), `validation/`, `model_checks/`; the CSV tables are in `handover/tables/` |
| `05_Code/` | `scripts/`: `analysis/`, `demo/`, `handover/`, `slides/`, `webmap/` |
| `06_Web_Map/` | `webmap/`; live at https://sharmaabhimanyueco.github.io/Supriyaaanya/ |
| `08_Project_Notes/` | The numbered notes `01_…` to `05_…` in the repository root |

**Not in this public repository, for licence reasons:** the study-area boundary and its zone mask (GADM does not allow redistribution) and the 160 photo chips and contact sheets of the accuracy check (Esri imagery). They are only in the private package.

## Quick checks from this repository

```
pip install -r scripts/requirements-demo.txt
python scripts/demo/recompute_areas.py results/rasters
python scripts/demo/recompute_accuracy.py results
```

Both scripts reproduce `results/results.json` exactly.
