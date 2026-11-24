"""True-colour previews of the Landsat composites (PNG), one per year, plus 2015 vs 2025 side by side.

Usage: python make_true_colour.py <landsat_composites folder> <output folder>
One stretch (reflectance x 10,000 from 150 to 1,700, gamma 1/1.5) is used for red, green and blue in every year,
so colours are natural and the years can be compared. Outside the study area is white; pixels with no
cloud-free view in that year (303 in 2015, 478 in 2025) are grey.
"""
import sys
from pathlib import Path

import numpy as np
import rasterio
from PIL import Image

src_dir, out = Path(sys.argv[1]), Path(sys.argv[2])
LO, HI, G = 150, 1700, 1 / 1.5
ims = {}
for y in (2015, 2020, 2025):
    with rasterio.open(src_dir / f"landsat_composite_{y}.tif") as s:
        bands = [s.read(b) for b in (3, 2, 1)]
        nod = s.nodata
    rgb = np.dstack([np.clip((b.astype("float32") - LO) / (HI - LO), 0, 1) for b in bands])
    im = (np.power(rgb, G) * 255).astype("uint8")
    # outside the study area every band is nodata; inside, a missing pixel is grey
    outside = np.all([b == nod for b in bands], axis=0)
    im[outside] = 255
    ims[y] = im
with rasterio.open(src_dir / "landsat_composite_2020.tif") as s:  # 2020 has a clear view of every study-area pixel
    inside_any = s.read(1) != s.nodata
for y, im in ims.items():
    with rasterio.open(src_dir / f"landsat_composite_{y}.tif") as s:
        missing = inside_any & (s.read(1) == s.nodata)
    im[missing] = (190, 190, 190)
    Image.fromarray(im).save(out / f"landsat_true_colour_{y}.png", optimize=True)

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
fig, ax = plt.subplots(1, 2, figsize=(10, 7.6), dpi=200)
for a, y in zip(ax, (2015, 2025)):
    a.imshow(ims[y]); a.set_axis_off(); a.set_title(f"March {y}", fontsize=15, fontweight="bold")
fig.suptitle("What the satellite saw: Landsat 8 true colour, 2015 and 2025", fontsize=16, fontweight="bold", y=0.98)
fig.text(0.5, 0.02, "Green = crops and trees; light brown and grey = buildings, roads and bare ground. Landsat data courtesy of the US Geological Survey.",
         ha="center", fontsize=10, color="#52514e")
fig.subplots_adjust(left=0.01, right=0.99, top=0.91, bottom=0.05, wspace=0.02)
fig.savefig(out / "landsat_true_colour_2015_vs_2025.png", facecolor="white")
print("written to", out)
