"""Recount the land-cover areas from the classified maps: a quick check anyone can run.

Usage:  python recompute_areas.py <folder that holds lulc_2015.tif, lulc_2020.tif and lulc_2025.tif>
        e.g.  python 05_Code/demo/recompute_areas.py 04_Data/rasters
Needs:  numpy and rasterio  (pip install -r 05_Code/requirements-demo.txt)

It counts the pixels of each land type in each year and multiplies by the pixel area
(30 m x 30 m = 900 m² = 0.09 ha). It then prints the built-up change with the yearly rate
(SDG 11.3.1 land-consumption formula: ln(later / earlier) / years x 100) and how much
cropland became built-up. The output should match slide 15, results.json and RESULTS_README.md.
"""
import math
import sys
from pathlib import Path

import numpy as np
import rasterio

folder = Path(sys.argv[1] if len(sys.argv) > 1 else ".")
NAMES = {1: "Built-up", 2: "Cropland", 3: "Trees/vegetation", 5: "Bare/fallow"}
YEARS = (2015, 2020, 2025)
maps, area = {}, {}
for yr in YEARS:
    with rasterio.open(folder / f"lulc_{yr}.tif") as src:
        maps[yr] = src.read(1)
        px_ha = abs(src.transform.a * src.transform.e) / 10000
        if yr == YEARS[0]:
            print(f"Map grid: {src.width} x {src.height} pixels, CRS {src.crs}, pixel {abs(src.transform.a):.0f} m = {px_ha:.2f} ha")
    area[yr] = {c: int((maps[yr] == c).sum()) * px_ha for c in NAMES}

print("\nArea by land type (hectares, and % of the mapped area)")
print(f"{'Land type':<18}" + "".join(f"{yr:>18}" for yr in YEARS))
tot = {yr: sum(area[yr].values()) for yr in YEARS}
for c, name in NAMES.items():
    print(f"{name:<18}" + "".join(f"{area[yr][c]:>10,.0f} ({100 * area[yr][c] / tot[yr]:4.1f}%)" for yr in YEARS))
print(f"{'Total':<18}" + "".join(f"{tot[yr]:>18,.0f}" for yr in YEARS))

print("\nBuilt-up change")
for a, b in ((2015, 2020), (2020, 2025), (2015, 2025)):
    b1, b2, n = area[a][1], area[b][1], b - a
    print(f"  {a}-{b}: +{b2 - b1:,.0f} ha  (+{100 * (b2 - b1) / b1:.1f}%), {(b2 - b1) / n:,.0f} ha a year, "
          f"yearly rate {100 * math.log(b2 / b1) / n:.2f}%")

l15, l25 = maps[2015], maps[2025]
new = (l25 == 1) & np.isin(l15, (2, 3, 5))
crop = (l25 == 1) & (l15 == 2)
print(f"\nNew built-up 2015 -> 2025: {new.sum() * px_ha:,.0f} ha, of which cropland in 2015: {crop.sum() * px_ha:,.0f} ha "
      f"({100 * crop.sum() / new.sum():.0f}%)")
print(f"Built-up in 2015 but not in 2025 (mostly classification noise): {((l15 == 1) & np.isin(l25, (2, 3, 5))).sum() * px_ha:,.0f} ha")
