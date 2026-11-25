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
