"""Write QGIS style files (.qml) next to the handover rasters, so QGIS colours them automatically.

Usage: python make_qgis_styles.py <04_Data folder>
A .qml with the same name as a .tif is loaded by QGIS when the .tif is added to a project.
The true-colour stretch is the 2nd-98th percentile of each band over the three years together,
so the three years are shown with the same stretch and can be compared by eye.
"""
import sys
from pathlib import Path

import numpy as np
import rasterio

D = Path(sys.argv[1])
HEAD = ("<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>\n"
        "<qgis version=\"3.34.0-Prizren\" styleCategories=\"AllStyleCategories\" hasScaleBasedVisibilityFlag=\"0\" minScale=\"1e+08\" maxScale=\"0\">\n"
        " <pipe>\n  <provider>\n   <resampling enabled=\"false\" zoomedInResamplingMethod=\"nearestNeighbour\" zoomedOutResamplingMethod=\"nearestNeighbour\" maxOversampling=\"2\"/>\n  </provider>\n")
MINMAX = ("   <rasterTransparency/>\n   <minMaxOrigin>\n    <limits>None</limits>\n    <extent>WholeRaster</extent>\n    <statAccuracy>Estimated</statAccuracy>\n"
          "    <cumulativeCutLower>0.02</cumulativeCutLower>\n    <cumulativeCutUpper>0.98</cumulativeCutUpper>\n    <stdDevFactor>2</stdDevFactor>\n   </minMaxOrigin>\n")
TAIL = ("  <brightnesscontrast brightness=\"0\" contrast=\"0\" gamma=\"1\"/>\n"
        "  <huesaturation saturation=\"0\" grayscaleMode=\"0\" colorizeOn=\"0\" colorizeRed=\"255\" colorizeGreen=\"128\" colorizeBlue=\"128\" colorizeStrength=\"100\" invertColors=\"0\"/>\n"
        "  <rasterresampler maxOversampling=\"2\"/>\n  <resamplingStage>resamplingFilter</resamplingStage>\n </pipe>\n <blendMode>0</blendMode>\n</qgis>\n")


def paletted(entries):
    rows = "".join(f"    <paletteEntry value=\"{v}\" color=\"{c}\" alpha=\"255\" label=\"{lab}\"/>\n" for v, c, lab in entries)
    return (HEAD + "  <rasterrenderer type=\"paletted\" band=\"1\" opacity=\"1\" alphaBand=\"-1\" nodataColor=\"\">\n" + MINMAX +
            "   <colorPalette>\n" + rows + "   </colorPalette>\n   <colorramp type=\"randomcolors\" name=\"[source]\"><Option/></colorramp>\n  </rasterrenderer>\n" + TAIL)


def rgb(bands, lims):
    enh = ""
    for colour, (lo, hi) in zip(("red", "green", "blue"), lims):
        enh += (f"   <{colour}ContrastEnhancement>\n    <minValue>{lo:.0f}</minValue>\n    <maxValue>{hi:.0f}</maxValue>\n"
                f"    <algorithm>StretchToMinimumMaximum</algorithm>\n   </{colour}ContrastEnhancement>\n")
    r, g, b = bands
    return (HEAD + f"  <rasterrenderer type=\"multibandcolor\" redBand=\"{r}\" greenBand=\"{g}\" blueBand=\"{b}\" opacity=\"1\" alphaBand=\"-1\" nodataColor=\"\">\n"
            + MINMAX + enh + "  </rasterrenderer>\n" + TAIL)


LULC = [(1, "#b03a2e", "Built-up"), (2, "#8db63c", "Cropland"), (3, "#2e6b3f", "Trees/vegetation"), (5, "#d9a441", "Bare/fallow")]
CLUST = [(1, "#d9a441", "1 · Bare/fallow"), (2, "#b03a2e", "2 · Built-up"), (3, "#2e6b3f", "3 · Trees/vegetation"),
         (4, "#6f9a2c", "4 · Cropland"), (5, "#4f8a5c", "5 · Trees/vegetation"), (6, "#80aa35", "6 · Cropland"),
         (7, "#8db63c", "7 · Cropland"), (8, "#a2c55a", "8 · Cropland"), (9, "#b6d27a", "9 · Cropland"), (10, "#c9df9c", "10 · Cropland")]
for tif in sorted((D / "rasters").glob("lulc_*.tif")) + sorted((D / "rasters").rglob("lulc_*_first_run.tif")):
    tif.with_suffix(".qml").write_text(paletted(LULC))
for tif in sorted((D / "rasters").glob("clusters_*.tif")):
    tif.with_suffix(".qml").write_text(paletted(CLUST))

comps = sorted((D / "landsat_composites").glob("landsat_composite_*.tif"))
vals = {b: [] for b in (1, 2, 3, 4)}
for tif in comps:
    with rasterio.open(tif) as src:
        for b in vals:
            a = src.read(b)
            vals[b].append(a[a != src.nodata][::7])
pct = {b: np.percentile(np.concatenate(v), [2, 98]) for b, v in vals.items()}
for tif in comps:  # one stretch (150-1700) for red, green and blue keeps natural colours; the percentiles drive the false-colour style
    tif.with_suffix(".qml").write_text(rgb((3, 2, 1), [(150, 1700)] * 3))
(D / "landsat_composites" / "style_false_colour_NIR_red_green.qml").write_text(rgb((4, 3, 2), [pct[4], pct[3], pct[2]]))
print("stretch (reflectance x 10,000):", {b: [round(x) for x in p] for b, p in pct.items()})
