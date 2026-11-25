```{=openxml}
<w:p><w:r><w:br w:type="page"/></w:r></w:p>
```

# Part 14 — Glossary

Short definitions, A to Z. Part 2 explains each idea at length, with an everyday analogy.

| Term | Meaning |
|---------------------------|-------------------------------------------------------------------------|
| Adjusted Rand index (ARI) | A score from 0 to 1 for how alike two groupings of the same pixels are; 1 = identical |
| Band | One "colour" a satellite records, often invisible to the eye (for example near-infrared) |
| Basemap | The background map (streets, names) under the project's own layers |
| Built-up | Land covered by buildings, roads and other hard surfaces |
| Calinski–Harabasz score | A cluster-quality score: higher = clusters more compact and further apart |
| Cluster | A group of pixels with similar colours, found by the computer without labels |
| Collection 2 Level-2 | The Landsat product that is already corrected for the atmosphere (surface reflectance) |
| Composite | One picture made from several, here by taking the middle (median) value per pixel |
| Confusion matrix | A table of map class against true class at check points; the diagonal = agreement |
| CRS (coordinate reference system) | The rule that ties map coordinates to places on Earth |
| Davies–Bouldin score | A cluster-quality score: lower = better separated clusters |
| Elbow method | Choosing the number of clusters where adding more stops helping much |
| EPSG code | A standard number for a CRS: 4326 = latitude/longitude, 32643 = UTM 43N, 3857 = Web Mercator |
| Error-adjusted area | An area corrected with the accuracy-check results, given with a ± range |
| ESA WorldCover | A global 10 m land-cover map from the European Space Agency, used as a second opinion |
| GADM | A free worldwide boundary database; the source of the study-area outline (no redistribution) |
| GeoJSON | A text file format for map shapes, used for the web map's hexagon grid |
| GeoTIFF | An image file that also knows where on Earth it lies; all the project's rasters |
| GIS | Geographic Information System: software that stores, shows and analyses mapped data (e.g. QGIS) |
| Codeberg Pages | Free hosting of static websites from a Codeberg repository's `pages` branch, run by the non-profit Codeberg e.V.; hosts the web map |
| Hectare (ha) | 100 m × 100 m = 10,000 m²; one 30 m pixel = 0.09 ha |
| Inertia | The total squared distance from each pixel to its cluster centre; lower = tighter clusters |
| K-means | A clustering method that sorts pixels into k groups around k centres, moving the centres until stable |
| Land consumption rate | Yearly growth rate of built-up land, ln(later ÷ earlier) ÷ years; the land part of SDG 11.3.1 |
| Landsat 8 | A NASA/USGS Earth-observation satellite launched in 2013; free 30 m images |
| Leaflet | A free open-source JavaScript library for web maps |
| LULC | Land use / land cover: what covers the ground (buildings, crops, trees, bare soil, water) |
| Median | The middle value of a set; ignores extreme values such as clouds |
| NDVI | (NIR − Red) ÷ (NIR + Red): a greenness index from −1 to 1; healthy plants score high |
| Nodata | A cell value that means "no information here" (0 in the land-cover maps, −32768 in the composites) |
| Olofsson method | Good-practice accuracy and area estimation that weights each check point by its class's map area |
| Overall accuracy | Share of the area the map labels correctly |
| Pixel | One square cell of a raster; here 30 m × 30 m |
| Planetary Computer | Microsoft's free catalogue and storage of public Earth data, used to get the images |
| Producer's accuracy | Of the real land in a class, the share the map found (misses = omission errors) |
| QA_PIXEL | Landsat's quality band, flagging fill, cloud, cirrus and shadow per pixel |
| QGIS | Free, open-source desktop GIS; the tool the teacher asked for |
| Raster / vector | Raster = a grid of cells (images, land-cover maps); vector = points, lines and shapes (the boundary) |
| Reclassification | Merging clusters into named land types (10 clusters → 4 land types) |
| Reflectance | The share of sunlight a surface reflects, from 0 to 1 |
| Remote sensing | Learning about the Earth's surface from a distance, here from a satellite |
| SDG 11.3.1 | UN indicator: ratio of land consumption rate to population growth rate |
| Seed (random seed) | A number that fixes the random choices so a run can be repeated exactly |
| Silhouette score | How well each pixel fits its own cluster compared with the next nearest one (−1 to 1) |
| STAC | SpatioTemporal Asset Catalog: a standard way to search satellite images, like a library catalogue |
| Stratified random sample | Random points with a fixed number per class, so small classes are checked too |
| Supervised / unsupervised classification | Supervised learns from labelled examples; unsupervised groups pixels first, and people name the groups |
| UEII | Urban Expansion Intensity Index: new built-up ÷ (zone area × years) × 100 |
| User's accuracy | Of the map's pixels in a class, the share that are right (false alarms = commission errors) |
| UTM zone 43N | A flat metric map grid for 72°E–78°E north of the equator; used for all area measurements |
| Web Mercator | The projection of web maps (EPSG:3857); fine for display, wrong for measuring areas |
| WRS-2 path/row | Landsat's fixed grid of scene footprints; this area is path 147, row 39 |
| Zone (West/East) | The two pieces of the boundary file, used for comparison; not official tehsils |

# Part 15 — References and sources

**Data**

- U.S. Geological Survey. Landsat 8 Collection 2 Level-2 Science Products (surface reflectance). https://www.usgs.gov/landsat-missions/landsat-collection-2-level-2-science-products. Landsat data courtesy of the U.S. Geological Survey.
- Microsoft Planetary Computer. Landsat Collection 2 Level-2 dataset and STAC API. https://planetarycomputer.microsoft.com/dataset/landsat-c2-l2
- Zanaga, D. et al. (2021). ESA WorldCover 10 m 2020 v100. https://doi.org/10.5281/zenodo.5571936
- Esri World Imagery (basemap used for the photo check; chips not redistributed). https://www.arcgis.com/home/item.html?id=10df2279f9684e4a9f6a7f08febac2a9
- GADM, database of global administrative areas (study-area outline; no redistribution). https://gadm.org
- Wikidata (place names and positions, CC0). https://www.wikidata.org
- OpenStreetMap contributors (basemap of the location map and the web map, ODbL). https://www.openstreetmap.org/copyright
- Codeberg Pages (hosting of the web map). https://docs.codeberg.org/codeberg-pages/

**Methods**

- Olofsson, P., Foody, G.M., Herold, M., Stehman, S.V., Woodcock, C.E. and Wulder, M.A. (2014). Good practices for estimating area and assessing accuracy of land change. *Remote Sensing of Environment* 148, 42–57. https://doi.org/10.1016/j.rse.2014.02.015
- United Nations Statistics Division. SDG indicator metadata, indicator 11.3.1. https://unstats.un.org/sdgs/metadata/files/Metadata-11-03-01.pdf
- UN-Habitat. Metadata on SDG indicator 11.3.1. https://unhabitat.org/sites/default/files/2020/07/metadata_on_sdg_indicator_11.3.1.pdf
- UEII speed bands, as used in: https://www.mdpi.com/2220-9964/11/7/406
- Pedregosa, F. et al. (2011). Scikit-learn: Machine learning in Python. *Journal of Machine Learning Research* 12, 2825–2830 (K-means and the cluster-quality scores).

**Software**

Python with numpy, rasterio and GDAL, scikit-learn, pyproj, shapely, pyshp, pystac-client, planetary-computer, matplotlib and Pillow; Leaflet 1.9.4 (web map); pptxgenjs (slides); QGIS (for opening the results; https://qgis.org).

**A note on checking.** The SDG metadata and the Olofsson paper are cited from their official pages, but their full texts could not be opened from the project's computer (see `08_Project_Notes/05_metrics_and_formulas.md`). Before quoting the SDG wording, read it on the UN page. The general facts in Part 2 list their own sources at the end of that part.

```{=openxml}
<w:p><w:r><w:br w:type="page"/></w:r></w:p>
```

# Part 16 — File inventory
