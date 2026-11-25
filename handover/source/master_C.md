```{=openxml}
<w:p><w:r><w:br w:type="page"/></w:r></w:p>
```

# Part 9 — The web map

**What it is.** An interactive dashboard that anyone can open in a browser, free, with no login: **https://abhimanyu04.codeberg.page/mohali-urban-growth/**. The teacher called the web map the end goal of the project.

![The dashboard in compare mode: 2015 left of the handle, 2025 right of it, over the Landsat satellite picture (screenshot of the live site; the street background map did not load on the computer that took it).](03_Maps_and_Charts/screenshots/webmap_02_compare_2015_2025.png){width=6.2in}

**What it does**

- **Guided tour:** nine steps fly the map to each finding and explain it with the project's numbers. It is the easiest way to present the map.
- **Compare:** drag a round handle to see one year on the left and another on the right (2015 and 2025 by default).
- **Backgrounds:** a grey or colour street map (OpenStreetMap), the Landsat 8 true-colour picture of the same year (open data), Esri's high-resolution photo (free to view, not open data), or none. With the Landsat background and low opacity you see the picture each map was made from.
- **Search** towns and villages from a built-in list (Wikidata), or any other place through an online search when connected. The map flies there and shows the built-up land within 0.5–3 km for each year.
- **Filter** by year, by land type and by zone (West or East), or show only land that became built-up, either all of it or farmland only. A play button animates 2015 → 2025.
- **1 km² hexagon grid** coloured by built-up growth, built-up share, farmland built over, or growth intensity (UEII), with a slider to hide small values.
- **Live figures** for whatever is on screen, a ranking of the fastest-growing places, click-anywhere profiles, an on-map legend and a full-screen button.
- **Share and download:** "Copy link to this view" makes a link that reopens the exact view, and a downloads panel offers the land-cover maps (GeoTIFF with QGIS styles), all result tables (CSV), every number (JSON) and the grid (GeoJSON).

**How it was built.** The script `05_Code/webmap/build_webmap.py` turns the final land-cover maps and the Landsat composites into picture layers in Web Mercator, the projection web maps use. It builds the hexagon grid with hectares per land type for each year (computed on the 30 m UTM maps, so the areas are correct), the list of places, and the downloads. The page uses Leaflet, a free open-source map library, and a copy of Leaflet ships with the site, so it loads no outside code. All filtering and counting happens in the visitor's browser: the page decodes the picture layers back into land-type codes. There is no server code, database or API key.

**Why not qgis2web?** The teacher's plan named qgis2web (UNCONFIRMED). qgis2web exports a QGIS project as a map with layers and pop-ups. A custom Leaflet page was chosen to add the tour, compare, search, live hectare figures and rankings described above, all computed from the land-cover data in the browser. Say so openly if asked.

**Hosting.** The site is hosted free on **Codeberg Pages**. Codeberg is a non-profit service (Codeberg e.V.), and its Pages server, git-pages, is free/open-source software. The site files live on the `pages` branch of the public repository https://codeberg.org/Abhimanyu04/mohali-urban-growth, which also holds a copy of the project's code. A webhook republishes the site whenever that branch changes. It is not hosted on GitHub Pages.

**Offline.** `06_Web_Map/` holds the same site and one-click launchers (`run_local_windows.bat`, `run_local_mac_linux.sh`). Without internet everything works except the street background map and the online search.

**Licences.** Code MIT; maps and figures CC BY 4.0; Leaflet BSD-2-Clause; place names from Wikidata (CC0); street map © OpenStreetMap contributors; Landsat imagery courtesy of the U.S. Geological Survey. The GADM zone outlines are not on the page (licence); each hexagon carries only a West/East label.

# Part 10 — Limitations

Say these openly. Knowing the limits of your own work is part of doing it well.

| Limitation | What it means | Effect on the results |
|------------------|----------------------------------------------|------------------------------------|
| **Undercount of built-up** | The map finds about half of the real built-up land (producer's accuracy 51.9%). Small villages, roads and houses under trees are missed at 30 m | The hectares are conservative; the 2025 corrected estimate is 17,706 ± 4,648 ha |
| **Look-alike classes** | Bare fields and bright roofs fall in the same clusters; bare/fallow is the weakest class (user's 35.7%, producer's 27.8%) | Some bare land is counted as built-up and some built-up as bare |
| **Mixed pixels** | One 30 m pixel can hold a field and a house | Small settlements are hard to separate |
| **Classification noise** | 3,225 ha mapped as built-up in 2015 are not built-up in 2025 | The change figures include some noise |
| **Crop stage** | Crops were at slightly different stages each March | Some cropland shows as trees or bare land. Part of the rise in trees/vegetation (14,255 → 22,299 ha) may be greener crops rather than new trees; this was not checked separately |
| **Boundary** | The GADM outline is old and its labels are wrong; the zones are not official tehsils | Zone figures are approximate; official tehsil outlines are needed for figures "by tehsil" |
| **Accuracy check** | Photo labels are AI-assisted; the Esri photos are of mixed dates; 158 points | Spot-check the labels; small-class figures are uncertain |
| **Not covered** | Building permits and zoning (GMADA/PUDA) are not included. No census exists for 2015–2025 | The full SDG 11.3.1 ratio (land against population growth) cannot be computed |
| **Tool** | The analysis ran in Python, not QGIS | Same method and outputs; the QGIS route is documented |

**What would improve it next:** more photo or field checks; Sentinel-2 images at 10 m for the later years (its March images start in 2016); supervised classification with training samples, if the teacher allows it; official tehsil boundaries; population data for the full SDG 11.3.1 ratio. The teacher's future-work ideas, a hotspot analysis (Getis-Ord Gi*) and a Development Pressure Index, are mentioned on slides 20 and 22 only.

# Part 11 — Decisions log

Every important choice, the options, what was chosen and why. "UNCONFIRMED" means waiting on the teacher.

| # | Decision | Options | Chosen | Why |
|----|--------------|----------------------|--------------------------|----------------------------------|
| 1 | Theme | Farmland loss; urbanisation | Urbanisation; farmland loss supporting | The teacher's instruction |
| 2 | Satellite | Landsat 8; Sentinel-2; others | Landsat 8 (UNCONFIRMED) | Same free sensor for all of 2015–2025; Sentinel-2 has no March 2015 images |
| 3 | Years | Any | 2015, 2020, 2025 (UNCONFIRMED) | Equal five-year steps; the latest March is 2025 |
| 4 | Season | Any month | March, both scenes per year | Wheat is green, so farmland and buildings differ most; the same month every year removes season effects |
| 5 | Images per year | One; several | Two clear scenes, median composite | Fills cloud gaps and removes leftover haze |
| 6 | Image source | Planetary Computer; Earth Engine; EarthExplorer | Planetary Computer | Free, no sign-up, scriptable, reads only the needed area |
| 7 | Software | QGIS; Python | Python, with every output styled for QGIS | Repeatable scripts that process 3.6 million pixels the same way every run; the QGIS route is documented. Disclosed openly |
| 8 | Classification type | Supervised; unsupervised | Unsupervised | The teacher's instruction (supervised was rejected) |
| 9 | Algorithm | K-means; ISODATA | K-means (UNCONFIRMED) | Standard, reproducible with a fixed seed, available in scikit-learn |
| 10 | Number of clusters | 4–16 tested | 10 | In the teacher's 8–10 range and the elbow region; extra clusters split mixed shades before merging |
| 11 | One model or one per year | Per year; pooled | Pooled across the three years | Per-year clusters meant different things (2020 > 2025 built-up); pooled clusters mean the same every year |
| 12 | Training data | 300,000-pixel sample; all pixels | All 3,626,753 pixels, best of 10 starts, 3 seeds | The sample model was unstable (2015 built-up 6,698–8,177 ha); full data agrees within 1% |
| 13 | Naming clusters | By eye each time; by reference | NDVI order, then the nearest first-run cluster (named by location and true colour) | The same rule for every cluster, written down and repeatable |
| 14 | Classes | 4–5 planned | 4 (water dropped) | No cluster picked out water; ponds are smaller than 30 m pixels |
| 15 | Zones | Tehsils; GADM pieces | GADM pieces as West/East zones | No verified tehsil outlines; the pieces' labels are wrong, so they are not called tehsils |
| 16 | Growth rate | % change; yearly rate | Both; the yearly rate uses the SDG 11.3.1 land formula | A recognised formula that compares periods of different length fairly; population part not available |
| 17 | Comparing zones | Hectares; share; UEII | All three, UEII for speed | UEII corrects for zone size |
| 18 | Accuracy check | None; visual; sample-based | Stratified random sample (50/50/30/30), blind photo labels, Olofsson area weighting (validation level UNCONFIRMED) | The recognised good practice; gives accuracy and a corrected area with a ± range |
| 19 | Who labelled the photos | Students; AI-assisted | AI-assisted, two blind raters plus a third look | Needed overnight; disclosed, and students should spot-check |
| 20 | Second opinion | None; ESA WorldCover | WorldCover 2020 comparison | An independent 10 m map from a space agency |
| 21 | Web map tool and host | qgis2web on GitHub Pages; custom Leaflet page on an open-source host | Custom Leaflet page on Codeberg Pages (tool UNCONFIRMED) | Tour, compare, search, filters and rankings; free hosting on a non-profit, open-source service |
| 22 | Licences | — | Code MIT; maps and figures CC BY 4.0; GADM and Esri photos kept private | Open where allowed; respects third-party terms |

# Part 12 — Where the code ran, and how to run it again
