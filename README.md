# Supriyaaanya

**Mapping Urban Growth in the Mohali–Kharar–Zirakpur–Dera Bassi Belt, Punjab, using LULC analysis**

> **Status, 25 November 2026: the analysis is done.** Start with [handover/README.md](handover/README.md) and the master document in `handover/`. Results are in [results/README.md](results/README.md), the slides in `slides/`, and the live web map at https://sharmaabhimanyueco.github.io/Supriyaaanya/. The plan below is the original starting plan, kept for the record.

This folder is the project's home and replaces the shared Drive folder from the handover. It contains everything that could be rebuilt from the handover note and the two files you had: the study-area boundary and the location map.

## Start here: the next 24 hours

1. **Send the message to your teacher today**: [01_message_to_teacher.md](01_message_to_teacher.md). Several choices are still unconfirmed. Her original instructions, the rubric and the deadline only exist with her.
2. **Get the satellite images today**: [03_get_satellite_images.md](03_get_satellite_images.md) with [scripts/export_landsat_composites.js](scripts/export_landsat_composites.js). Earth Engine needs a one-time sign-up and the exports take a while, so start early.
3. **Install QGIS and the two plugins, and fix the location map**: steps 0 and 1 of [04_qgis_steps.md](04_qgis_steps.md).
4. **When the images arrive**, clip, cluster, name, reclassify and measure: [04_qgis_steps.md](04_qgis_steps.md).
5. **Turn the areas into results**: [05_metrics_and_formulas.md](05_metrics_and_formulas.md).
6. **Fill in the results slides, then build the web map**: [slides/](slides/) and step 9 of [04_qgis_steps.md](04_qgis_steps.md).

## What the handover listed, and what you have now

| Handover item | Status | Where it is now |
|---|---|---|
| Study-area boundary | You have it (`Study_Area.zip`), but its labels are wrong | With you. See the warning below |
| Location map | You have it. It needs two fixes | Your PNG, also on slide 4 |
| Slides 1–4 (farmland version) | Lost. Rebuilt for the urbanisation theme, along with every other slide | [slides/Urban_Growth_Mohali_slides.pptx](slides/Urban_Growth_Mohali_slides.pptx) |
| Teacher's messages and slide list | Her exact words are lost. The handover's summary is saved, and the message asks her to resend | [02_teacher_brief_and_slide_list.md](02_teacher_brief_and_slide_list.md) |
| Marking rubric | Only the teacher has it | Requested in [01_message_to_teacher.md](01_message_to_teacher.md) |
| Shared Drive folder | Not found in your Google Drive | This repository replaces it |
| Old Earth Engine script | Not needed. It used the method the teacher rejected | Replaced by a script that only downloads images |
| Satellite images | None yet | [03_get_satellite_images.md](03_get_satellite_images.md) |

## Two warnings about the files you have

- **Boundary labels are wrong.** The boundary comes from GADM, a free worldwide database of boundaries. It has two pieces, labelled "Kharar" and "Rajpura". Mohali lies inside the "Kharar" piece, and Zirakpur and Dera Bassi lie inside the "Rajpura" piece. Rajpura town itself is outside the study area, in Patiala district. Don't show these labels anywhere. Get correct tehsil outlines before you report anything "by tehsil". The whole outline measures **108,829 ha (about 1,088 km²)** in UTM zone 43N. Before you quote that figure, compare it with an official district map. One place to check: Banur seems to fall just outside the line.
- **The location map needs two fixes.** Switch off the "Kharar"/"Rajpura" labels; they also show as "arar" and "ura" in the India inset. Then add the credit "© OpenStreetMap contributors", which the background map's licence requires.

GADM's licence allows academic use but not redistribution without permission (check it on gadm.org). So the boundary files are not stored in this repository, and they shouldn't be uploaded to a public one.

## Folder contents

| File | What it is |
|---|---|
| `01_message_to_teacher.md` | Ready-to-send questions for the teacher |
| `02_teacher_brief_and_slide_list.md` | The teacher's procedure and slide list, as recorded in the handover |
| `03_get_satellite_images.md` | How to download one cloud-free image per year |
| `scripts/export_landsat_composites.js` | The Earth Engine script. It only downloads images and classifies nothing |
| `04_qgis_steps.md` | QGIS steps: clip, cluster, name, reclassify, measure, change maps, web map |
| `05_metrics_and_formulas.md` | Which numbers to report, with formulas, tables to fill in, and sources |
| `slides/Urban_Growth_Mohali_slides.pptx` / `.pdf` | The 24-slide deck: results, plain-language explainer slides, model checks, accuracy check and glossary; speaker notes say what to check |
| `results/` | Final results: maps, land-cover rasters, Landsat composites for QGIS, model checks, accuracy check and all the numbers ([results/README.md](results/README.md)) |
| `scripts/analysis/` | The Python scripts that produced the results |

Anything marked **UNCONFIRMED** is waiting on the teacher's answers.
