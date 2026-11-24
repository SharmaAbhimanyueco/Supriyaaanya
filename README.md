# Urban growth web map

An open-source, interactive dashboard of urban growth in the Mohali–Kharar–Zirakpur–Dera Bassi belt (S.A.S. Nagar district, Punjab), 2015–2025.

**Live site:** https://sharmaabhimanyueco.github.io/Supriyaaanya/ (GitHub Pages, served from the `gh-pages` branch)

## What it does
- **Search** towns and villages (built-in list from Wikidata; anything else through OpenStreetMap/Photon when online). The map flies there and shows built-up land within 0.5–3 km, by year. Shareable links: `…/#kharar`.
- **Filter** by year (2015, 2020, 2025), by land type, by zone (West / East), and show only land that became built-up (all, or farmland only). A play button animates 2015 → 2025.
- **1 km² grid** coloured by built-up growth, built-up share, farmland built over, or growth intensity (UEII), with a threshold slider.
- **Live figures** for whatever is on screen, a ranking of the fastest-growing places, and click-anywhere profiles (what each 30 m square was in each year).

## Run it yourself
It is a static site: no server code, no accounts, no API keys. From this folder run `python -m http.server 8000` and open http://localhost:8000.
(Opening `index.html` directly as a file will not load the grid and place data, because browsers block local file requests.)

## Rebuild it
`python -I scripts/webmap/build_webmap.py <repo root> <W/analysis2/zones.npy>` regenerates `index.html`, `layers/` and `data/` from
`results/results.json` and `results/rasters/`. The page layout is `scripts/webmap/template.html`.

## Licence
Code: MIT. Maps and figures: CC BY 4.0. Third-party credits: see `../LICENSE-DATA.md`.
