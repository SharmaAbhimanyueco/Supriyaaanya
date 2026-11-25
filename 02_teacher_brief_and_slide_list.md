# Teacher's brief and slide list

This is the handover's summary of what the teacher asked for. It is **not her exact wording**, because her original messages were not passed on. Items marked UNCONFIRMED are in [01_message_to_teacher.md](01_message_to_teacher.md).

## What she asked for

1. In QGIS, cluster each year's image into classes. This is unsupervised classification: the computer groups similar pixels by itself, and we name the groups afterwards. It gives one LULC (land use / land cover) map per year.
2. Get the area of each class for each year.
3. Make charts and graphs from those areas.
4. Write the report: the interpretation, and the difference in hectares between years.
5. End goal: a web map.

## What she said was wrong with the earlier plan

- The plan was built around farmland loss. The theme must be **urbanisation**, with farmland loss only a supporting finding.
- It used supervised classification: training points plus a Random Forest classifier in Google Earth Engine. The course wants **clustering in QGIS**.
- It treated the web map as optional, but the web map is **the end goal**.

Kept from the earlier work: the study area, the location map, the idea of comparing several years, the class names, and slides 1–4 after rewording. The slides file itself was lost, so it has been rebuilt.

## Detailed plan (from the handover)

| Step | Plan | Status |
|---|---|---|
| Images | One per year, February–March, Landsat 8/9 at 30 m | UNCONFIRMED |
| Years | 2015, 2020, 2025 | UNCONFIRMED |
| Clip | Clip each image to the study area in QGIS, in EPSG:32643 | Planned |
| Cluster | K-means or ISODATA, 8–10 clusters, identical settings every year | UNCONFIRMED |
| Name and merge | Name the clusters over high-resolution imagery, then merge them into 4–5 classes with Reclassify by table, using the same class codes every year | Planned |
| Area | Raster layer unique values report, converted to hectares | Planned |
| Charts | Hectares per class per year, a bar chart, a line chart of built-up area, a change table | Planned |
| Results | Built-up hectares per year, share, change, annual rate, where growth happened; cropland that became built-up | Planned |
| Web map | qgis2web, hosted on GitHub Pages | UNCONFIRMED |
| Validation | Visual check, plus check points if she wants accuracy figures | UNCONFIRMED |

## Slide list (as given)

1. Title, team, tagline
2. Problem statement (who it affects, why it matters)
3. SDG link (specific target)
4. Study area (location map, why this boundary)
5. Objectives (minimum 3)
6. Data (kind of data, sources)
7. Data preparation (optional)
8. Methodology (workflow flowchart)
9. GIS and remote sensing analysis (clipping, clustering, reclassification, area calculation, etc.)
10. Risks, suitability and assumptions
11. Results
12. Validation
13. Idea of what a dashboard could show (the web map is now the end goal)
14. Limitations
15. Conclusion
17. References (mostly official sources: USGS/NASA for Landsat, the UN SDG site, Census of India, Punjab/GMADA/PUDA, OSM)

The list skips 16, and the message to the teacher asks about it. In the rebuilt deck, Results takes two slides, so References ends up as slide 17.

## Future work (mention only on the web-map slide and in the conclusion)

- Hotspot analysis (Getis-Ord Gi*).
- A Development Pressure Index (distance to built-up areas, major roads, the airport, and urban or industrial centres), to predict where growth will go next.
