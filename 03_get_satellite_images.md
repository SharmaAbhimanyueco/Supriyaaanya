# Getting the satellite images

You need one Landsat 8/9 image for each study year, taken in February–March. The years are planned as 2015, 2020 and 2025 (UNCONFIRMED). The script [scripts/export_landsat_composites.js](scripts/export_landsat_composites.js) builds these images in Google Earth Engine and saves them to your Google Drive. It only downloads images. All classification happens in QGIS, as the teacher asked.

## Plain words first

- **Landsat 8 and Landsat 9** are two near-identical satellites run by NASA and the US Geological Survey (USGS). Landsat 8 has been in orbit since 2013 and Landsat 9 since 2021. Both number their bands the same way, so images from different years can be compared. Check the specifications on usgs.gov before you quote them.
- **Bands** are the separate "colours" a satellite records, including some our eyes can't see. Think of a camera with six colour channels instead of three. The script keeps six: blue, green, red, near-infrared, and two shortwave-infrared bands. Healthy plants reflect near-infrared strongly, which is why green wheat stands out from concrete.
- **A composite** is one picture made from many. The script stacks every clear February–March picture of a year and keeps the middle (median) value for each pixel, so clouds and odd days drop out. It's like making one typical photo from a stack of photos of the same street.
- **Why February–March:** wheat is green then, so farmland looks very different from buildings. Using the same months every year also removes crop-season differences between years.

## Steps

1. **Get Earth Engine access (one time only).** Go to earthengine.google.com and sign up with a Google account. You'll be asked to register a Google Cloud project for non-commercial (academic) use. Follow the steps on the screen. If your university already has an Earth Engine project, ask the teacher.
2. Open the **Code Editor** at code.earthengine.google.com and check that your project is selected (top right).
3. In the **Scripts** panel on the left, click **NEW → File** and name it `export_landsat_composites`. Paste in everything from `scripts/export_landsat_composites.js` and click **Save**.
4. Click **Run**. The **Console** on the right shows how many pictures were found for each year. On the map, open the **Layers** menu and tick `2015 true colour`, `2020 true colour` and `2025 true colour` in turn. Check each year for holes or leftover cloud.
5. Open the **Tasks** tab on the right. Click **RUN** next to each of the three tasks, keep the settings shown, and confirm. Each export often takes several minutes, sometimes longer.
6. In Google Drive, open the folder `urban_growth_mohali` and download the three files: `landsat_2015_febmar.tif`, `landsat_2020_febmar.tif` and `landsat_2025_febmar.tif`. Keep them together in one project folder on your computer.

## What's in each file

- Six bands, in this order: blue, green, red, near-infrared (NIR), SWIR1, SWIR2.
- The values are surface reflectance × 10,000. For example, 1,234 means 12.34% of the light was reflected.
- The grid is UTM zone 43N (EPSG:32643) with 30 m pixels, identical for all three years. It covers the study area plus about 5 km around it. You clip to the exact boundary in QGIS (step 2 of [04_qgis_steps.md](04_qgis_steps.md)).
- Missing pixels are stored as −32768 and marked as NoData in the file. None are expected.

## If something goes wrong

- **A year shows 0 pictures, or the image has big holes:** paste the Console output into the chat. The months can be widened.
- **"Project not registered" or a permission error:** finish the Earth Engine sign-up first (step 1).
- **Any red error message:** paste it into the chat exactly as it appears.

## Without Earth Engine

If the teacher doesn't allow Earth Engine, you can download Landsat 8/9 "Collection 2 Level-2" scenes for February–March from USGS EarthExplorer (earthexplorer.usgs.gov, free account). This route is slower: each scene is a large download, you have to stack the bands yourself, and you may need two scenes per year to cover the area. Ask in the chat and I'll write those steps.
