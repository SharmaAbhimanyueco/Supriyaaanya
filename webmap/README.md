# Urban growth web map

An open-source, interactive dashboard of urban growth in the Mohali–Kharar–Zirakpur–Dera Bassi belt (S.A.S. Nagar district, Punjab), 2015–2025.

**Live site:** https://abhimanyu04.codeberg.page/mohali-urban-growth/ (Codeberg Pages, served from the `pages` branch of https://codeberg.org/Abhimanyu04/mohali-urban-growth)

## What it does
- **Guided tour:** nine steps that fly the map to each finding and explain it with the project's numbers. Ideal for presenting.
- **Compare:** drag a divider to see one year on the left and another on the right (2015 | 2025 by default).
- **Backgrounds:** grey or colour OpenStreetMap, the Landsat 8 true-colour picture of the same year (open data), Esri's high-resolution photo (free to view, not open data), or none. With the Landsat background and low opacity you see the picture each map was made from.
- **Search** towns and villages (built-in list from Wikidata; anything else through OpenStreetMap/Photon when online). The map flies there and shows built-up land within 0.5–3 km, by year.
- **Filter** by year, land type and zone (West / East), or show only land that became built-up (all, or farmland only). A play button animates 2015 → 2025.
- **1 km² hexagon grid** coloured by built-up growth, built-up share, farmland built over, or growth intensity (UEII).
- **Live figures** for whatever is on screen, a ranking of the fastest-growing places, click-anywhere profiles, an on-map legend, full screen, and **shareable links** that reopen the exact view (`…/#@lat,lng,zoom z,view`).
- **Downloads:** the land-cover maps (GeoTIFF with QGIS styles), all result tables (CSV), every number (JSON) and the grid (GeoJSON).

## Run it yourself
It is a static site: no server code, no accounts, no API keys, and Leaflet is included. From this folder run `python -m http.server 8000` and open http://localhost:8000. (Opening `index.html` directly as a file will not load the data, because browsers block local file requests.)

## Rebuild it
`python -I scripts/webmap/build_webmap.py <repo root> <W/analysis2/zones.npy>` regenerates `index.html`, `layers/`, `data/` and `downloads/` from `results/`. The page layout is `scripts/webmap/template.html`. Set `WEBMAP_REPO`, `WEBMAP_REPO_NAME` and `WEBMAP_HOST` for the source-code link and the hosting credit.

## Licence
Code: MIT. Maps, figures and data: CC BY 4.0. Leaflet: BSD-2-Clause (`LEAFLET_LICENSE.txt`). Third-party credits: see `LICENSE-DATA.md`.
