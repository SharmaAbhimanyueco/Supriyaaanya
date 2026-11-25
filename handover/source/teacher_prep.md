# Teacher Prep: be ready for questions and live demos

For Supriya Mahshere and Aanya Upadhyay. Read this the night before. It tells you what to say if the teacher asks questions, and what to show if she asks you to run something.

Paths like `04_Data/rasters` are inside the `Urban_Growth_Handover` folder. Slide numbers are from the 24-slide deck in `02_Presentation/`.

**Golden rules**
- If you do not know, say: "I am not sure. Here is how we would check." Never guess a number.
- Every number comes from the slides or the cheat sheet below. Do not round differently.
- Anything marked **UNCONFIRMED** is waiting for the teacher's answer. Say "we have asked, and are using this as our working choice."

---

## 0. Numbers cheat sheet

| What | Value |
|---|---|
| Study area | 1,209,178 pixels of 30 m, about 108,800 ha (about 1,088 km²) |
| Built-up 2015 / 2020 / 2025 | 7,844 / 10,033 / 14,786 ha |
| Built-up share | 7.2% / 9.2% / 13.6% |
| Growth 2015–2025 | +6,942 ha (+88.5%, "+89%"), 694 ha a year |
| Yearly rate (SDG 11.3.1 formula) | 6.34% overall; 4.92% (2015–20); 7.76% (2020–25) |
| Cropland 2015 / 2020 / 2025 | 81,218 / 77,204 / 66,728 ha |
| Trees/vegetation | 14,255 / 17,150 / 22,299 ha |
| Bare/fallow | 5,482 / 4,439 / 4,970 ha |
| West zone built-up | 4,336 → 9,236 ha; share 6.1% → 13.0%; UEII 0.69 |
| East zone built-up | 3,507 → 5,545 ha; share 9.3% → 14.8%; UEII 0.54 |
| Cropland that became built-up | 6,916 ha (68% of 10,170 ha new built-up) |
| Built-up in 2015 but not 2025 | 3,225 ha (noise) |
| Overall accuracy (158 points) | 74.6%; built-up vs not 87.0% |
| Built-up user's / producer's | 62.0% / 51.9% |
| Error-adjusted built-up 2025 | 17,706 ± 4,648 ha (map: 14,786 ha) |
| ESA WorldCover 2020 | 92.8% agreement; it finds 12,181 ha vs our 10,033 ha |
| Model | K-means, 10 clusters, 10 starts, up to 300 iterations, trained on 3,626,753 pixels |

---

## 1. The 60-second story

Say this if she asks, "Explain your project in one minute."

> "Our project asks one question: how fast is the area around Chandigarh turning into city? We studied the Mohali, Kharar, Zirakpur and Dera Bassi belt in Punjab. We used free Landsat 8 satellite photos from March 2015, 2020 and 2025. A computer method called K-means sorted every 30-metre pixel into ten groups, and we named the groups and merged them into four land types: built-up, cropland, trees and bare land.
>
> Built-up land grew from 7,844 hectares in 2015 to 14,786 hectares in 2025. That is 6,942 hectares more, nearly double, or 6.3% a year. Growth sped up after 2020, from 4.9% to 7.8% a year. The western part, Kharar and Mohali, grew faster than the east. About two-thirds of the new built-up land was farmland in 2015.
>
> We checked the map on 158 points using detailed photos. It is right at 75% of points overall and 87% for built-up versus not built-up. But it misses about half of the real built-up land, so our hectares are conservative. Our best corrected estimate for 2025 is about 17,700 hectares. Finally, we built an open web map where anyone can switch years, search a town and see the change."

**Time check:** about 60 seconds when read at a calm pace. Practise it once with a timer.

---

## 2. Three disclosures: say them before anyone asks

Say these early, in a calm voice. Teachers respect honesty. Being caught hiding something costs far more.

### 2.1 Python, not QGIS

> "Our teacher asked for the analysis in QGIS. Because of the deadline, we ran the analysis in Python. Every output opens in QGIS: the land-cover maps, the clusters and the Landsat images all have QGIS styles. The QGIS route is written step by step in `08_Project_Notes/04_qgis_steps.md`, and we can show you the results in QGIS now."

Do **not** say or imply the analysis was done in QGIS. The tool column on slide 13 says Python. Whether a Python route is acceptable is **UNCONFIRMED** with the teacher.

### 2.2 The photo labels were AI-assisted

> "To check accuracy, we needed to know what is really on the ground at 158 random points. We looked at detailed Esri photos. The labels were AI-assisted: two independent interpreters labelled every point without seeing our map. They agreed on 144 of 160 points, and a third look settled the 16 disagreements. These labels are not field visits. We should spot-check a sample ourselves, and we are happy to do that with you."

Before the presentation, open 10 to 15 chips in `04_Data/validation/chips/` yourselves and compare them with `04_Data/validation/reference_labels.csv`. Then you can say how many you checked and what you found. Only say a number if you really did it.

### 2.3 The hectares are conservative

> "Our map undercounts built-up land. The accuracy check shows it finds about 52% of real built-up land. So treat our hectares as a floor. The corrected estimate for 2025 is about 17,700 hectares, give or take 4,600, against 14,786 on the map. The trend, the speed-up after 2020, and the West-versus-East pattern are the reliable findings."

---

## 3. Likely questions and answers

Each answer is 2 to 4 sentences. Say it in your own words. **Show** tells you where to point.

### 3.1 Study area and boundary

**Q1. Why did you choose this area?**
**Say:** It is the belt next to Chandigarh where four fast-growing towns meet: Mohali, Kharar, Zirakpur and Dera Bassi. One district holds all four, so results can feed district-level planning. Growth drivers include Chandigarh's spillover, industrial parks and the airport.
**Show:** Slide 2, slide 4; `03_Maps_and_Charts/maps/location_map.jpg`.

**Q2. Where does your boundary come from? Is it official?**
**Say:** It comes from GADM, a free world database of boundaries. It is not an official Punjab map. We say that openly on the slides, and an official boundary would be the better choice. Checking it against an official district map is still to do.
**Show:** Slide 4 footnote; slide 6.

**Q3. Are "West" and "East" real tehsils?**
**Say:** No. The GADM file has two polygons with wrong labels: "Kharar" really holds Kharar and Mohali, and "Rajpura" really holds Dera Bassi including Zirakpur. Rajpura town is outside the study area. So we call them the West zone and East zone, not official tehsils.
**Show:** Slide 16 table and notes.

**Q4. How big is the study area? Did you check it against an official figure?**
**Say:** It is 1,209,178 pixels of 30 m, about 108,800 hectares, or about 1,088 km². We have not yet compared it with an official district area. That check is still open.
**Show:** Slide 4; `04_Data/tables/`.

**Q5. Why no buffer around the district?**
**Say:** We stayed inside the boundary, so every hectare belongs to the study area. Whether a 5 km buffer is wanted is **UNCONFIRMED**: we asked the teacher. A buffer would show growth just outside the line, for example near Banur (the project notes suggest Banur may fall just outside the line).
**Show:** `08_Project_Notes/01_message_to_teacher.md`, question 5.

### 3.2 Data and satellite

**Q6. Why Landsat 8 and not Sentinel-2?**
**Say:** Landsat 8 has a free, consistent archive, so we could use one satellite for all three years. Its pixels are 30 m. Sentinel-2 has 10 m pixels and would see small villages better, but we did not use it. It is on our next-steps list. The satellite choice is **UNCONFIRMED** with the teacher.
**Show:** Slide 6, slide 14, slide 21.

**Q7. Exactly which images did you use?**
**Say:** Landsat 8 Collection 2 Level-2, path 147, row 39, from Microsoft Planetary Computer. Two clear March scenes per year: 7 and 23 March 2015, 4 and 20 March 2020, and 2 and 18 March 2025.
**Show:** Slide 6 notes; `05_Code/analysis/build_composites.py`.

**Q8. Why March?**
**Say:** In March the wheat is green, so farmland and buildings look very different. Using the same month every year removes crop-season effects, so changes are real changes. The downside is that crops are at slightly different stages each March.
**Show:** Slide 7, slide 21.

**Q9. Why only 2015, 2020 and 2025?**
**Say:** Our working plan is 2015, 2020 and 2025: ten years with a middle point. Three years give two periods, and the middle point shows that growth sped up after 2020. These years are **UNCONFIRMED** with the teacher.
**Show:** Slide 15.

**Q10. Is 30 m enough?**
**Say:** It is fine for town-scale growth. It is not fine for single houses or narrow roads. One pixel can hold fields and houses together, which is why the map undercounts small settlements.
**Show:** Slide 14, slide 21.

**Q11. Is all your data free and open?**
**Say:** Yes. Landsat is free from USGS and NASA. WorldCover is free from the European Space Agency. The boundary is free for study but cannot be redistributed, so it is not in the public repository.
**Show:** Slide 6, slide 24.

### 3.3 Pre-processing

**Q12. How did you handle clouds?**
**Say:** We used the image's built-in quality flags (QA_PIXEL) to hide fill, cloud, cirrus, cloud shadow and dilated cloud pixels. We then combined two scenes per year.
**Show:** Slide 7; `05_Code/analysis/build_composites.py`.

**Q13. What is a composite and why a median?**
**Say:** A composite is one clean picture made from two clear photos. For each pixel we keep the middle value, so a stray cloud or shadow in one photo does not spoil the result. It is like taking the median of two exam attempts.
**Show:** Slide 9; slide 23 glossary.

**Q14. What are the six bands?**
**Say:** Blue, green, red, near-infrared, shortwave infrared 1 and shortwave infrared 2. Three are invisible to our eyes: near-infrared and the two shortwave-infrared bands. Healthy plants reflect near-infrared strongly, which separates green wheat from concrete.
**Show:** Slide 9.

**Q15. Why UTM zone 43N?**
**Say:** It measures in metres, so one 30 m pixel is 900 m², or 0.09 hectare, in every year. Measuring on a latitude and longitude grid would give wrong areas. All three years share one grid.
**Show:** Slide 7; QGIS: Layer Properties, Information.

### 3.4 Classification and K-means

**Q16. What does "unsupervised" mean?**
**Say:** The computer groups pixels that look alike without being told what any group is. We name the groups afterwards. It is like sorting a sack of mixed pulses into heaps by look.
**Show:** Slide 10.

**Q17. Why not supervised classification, such as Random Forest?**
**Say:** The earlier plan used it, and the teacher asked for clustering instead. Supervised needs training points we label ourselves, which is slower for three years. Its advantage is that classes are defined by us. It is a good next step.
**Show:** `08_Project_Notes/02_teacher_brief_and_slide_list.md`; slide 14.

**Q18. Why K-means and not ISODATA?**
**Say:** The teacher offered K-means or ISODATA. We used K-means because it is simple and standard in scikit-learn. ISODATA can split and merge clusters by itself, so the number of groups can change. Which one she prefers is **UNCONFIRMED**.
**Show:** Slide 10; `08_Project_Notes/01_message_to_teacher.md`, question 3.

**Q19. Why 10 clusters for 4 land types?**
**Say:** Each land type looks different in different places: wet field, dry field, young wheat. Ten groups capture those variations, and we then merge them into four types. Using more clusters than land types is normal in unsupervised classification.
**Show:** Slide 11, slide 18.

**Q20. How did you name the clusters?**
**Say:** The computer only gives numbers. We named each cluster from where it sits: towns and roads, the forested hills in the north, fields. We also used true-colour images. Group 2 is built-up, groups 3 and 5 are trees, group 1 is bare land and the rest are cropland.
**Show:** Slide 11; `04_Data/model_checks/final_model_training.json`.

**Q21. Why one model for all three years?**
**Say:** If we trained a new model each year, group 4 in 2015 might mean something else from group 4 in 2020. One trained model gives each group the same meaning in every year, so the years compare fairly.
**Show:** Slide 10.

**Q22. Why is there no water class?**
**Say:** No cluster picked out water. Ponds and streams are too small to fill a 30 m pixel. So code 4 (water) is unused. We say that on the slides.
**Show:** Slide 11, slide 15.

**Q23. Why did you train on every pixel?**
**Say:** An earlier version trained on a 300,000-pixel sample gave different answers when retrained. Training on all 3,626,753 pixels from the three years fixed that. Three separate runs now agree within 1%.
**Show:** Slide 18.

**Q24. Why did you use Python instead of QGIS?**
**Say:** Deadline pressure. Python let us train on all pixels and repeat checks quickly. The results open in QGIS, and the QGIS steps are documented. Whether this is acceptable is the teacher's call.
**Show:** Slide 13; section 2.1 above.

### 3.5 Model checks

**Q25. Is 10 the best number of clusters?**
**Say:** Not by statistics alone. The elbow is at k = 8, and k = 7 to 10 score within about 10% of the best elbow value. The silhouette score is highest at k = 4 (0.386) but nearly flat from 5 to 16 clusters. Ten is inside the sensible range.
**Show:** Slide 18; `03_Maps_and_Charts/charts/chart_06_k_selection.png`.

**Q26. Is the model stable? Does it give the same answer twice?**
**Say:** Yes. Three runs with different random seeds converged in 35, 31 and 29 iterations. Their fit scores differ by less than 0.01%. Built-up area in 2025 is 14,737 to 14,841 ha across runs, within 1%.
**Show:** Slide 18; `03_Maps_and_Charts/charts/chart_07_stability.png`.

**Q27. Your numbers differ from an earlier version. Why?**
**Say:** The earlier model, trained on a 300,000-pixel sample, gave 6,609 to 14,529 ha (+120%). When we retrained it on other samples, 2015 moved between 6,698 and 8,177 ha, so it was unstable. We replaced it with the full-data model. Only the new numbers are used everywhere.
**Show:** Slide 18 notes; `04_Data/model_checks/model_checks.md`.

**Q28. Did the sample size matter?**
**Say:** Little. In the earlier tests, 50,000, 100,000 and 200,000 pixels per year gave similar 2025 built-up (14,756, 14,594 and 14,656 ha). The random seed mattered more than the sample size. That is why we moved to all pixels.
**Show:** `04_Data/model_checks/model_checks.md`.

### 3.6 Results and numbers

**Q29. What is your main result?**
**Say:** Built-up land grew from 7,844 ha in 2015 to 14,786 ha in 2025: +6,942 ha, about +89%. That is 6.3% a year. The share of the study area went from 7.2% to 13.6%.
**Show:** Slide 15; `03_Maps_and_Charts/charts/chart_01_builtup_trend.png`.

**Q30. Did growth speed up?**
**Say:** Yes. Built-up grew 2,190 ha (4.9% a year) in 2015–2020 and 4,753 ha (7.8% a year) in 2020–2025. The map undercount affects both periods, so the speed-up is likely real.
**Show:** Slide 15, slide 12.

**Q31. What happened to the other land types?**
**Say:** Cropland fell from 81,218 to 66,728 ha. Trees rose from 14,255 to 22,299 ha. Bare/fallow went 5,482, then 4,439, then 4,970 ha. The tree rise may partly be crop stage in March, so do not over-read it.
**Show:** `03_Maps_and_Charts/charts/chart_02_landcover_by_year.png`.

**Q32. How much farmland did the growth eat?**
**Say:** 10,170 ha became built-up between 2015 and 2025. Of that, 6,916 ha, or 68%, was cropland in 2015. Farmland loss is a supporting finding. The main theme is urban growth.
**Show:** Slide 16; `03_Maps_and_Charts/charts/chart_04_new_builtup_sources.png`.

**Q33. Why does some built-up land turn back into cropland?**
**Say:** Mostly it does not. 3,225 ha were mapped built-up in 2015 but not in 2025. Real built-up land rarely returns to farmland, so we treat that as classification noise, for example bare fields or bright roofs that look alike. This is why individual change pixels need care.
**Show:** Slide 16 notes, slide 21.

**Q34. Why do trees increase so much?**
**Say:** We do not know exactly. Some of it may be real: new parks, avenues and plantations. Some is crop stage: crops at a different growth stage in March can look like trees. We have not tested this separately.
**Show:** Slide 21.

**Q35. Where did growth happen?**
**Say:** The West zone, Kharar and Mohali, grew more: 4,336 to 9,236 ha. The East zone, Dera Bassi and Zirakpur, went from 3,507 to 5,545 ha. For place-level answers, the web map ranks the fastest-growing places.
**Show:** Slide 16; web map "Fastest-growing places" panel.

### 3.7 Change and urban metrics

**Q36. How do you calculate the yearly rate?**
**Say:** We use the SDG 11.3.1 formula for land consumption rate: ln(later ÷ earlier) ÷ years. It works like compound interest. For 2015–2025 it gives 6.34% a year.
**Show:** Slide 12; `08_Project_Notes/05_metrics_and_formulas.md`.

**Q37. Did you calculate SDG indicator 11.3.1?**
**Say:** Only half of it. The official indicator is the ratio of land consumption rate to population growth rate. We computed the land-consumption side. We have no census population for 2015–2025, so the full ratio is future work.
**Show:** Slide 3 notes, slide 21.

**Q38. What is UEII?**
**Say:** The Urban Expansion Intensity Index is new built-up land per year as a percentage of the zone's area. It lets a big zone and a small zone be compared fairly, like turning marks out of 50 and out of 100 into percentages. The speed bands (slow, low, medium, high) are a convention from published studies, not a rule.
**Show:** Slide 12, slide 16, slide 23.

**Q39. West has the higher UEII but a lower built-up share than East. Is that a mistake?**
**Say:** No, they answer different questions. The share is how much of the zone is built-up now: East 14.8%, West 13.0%. UEII is how fast new land was added: West 0.69, East 0.54. East started higher, in 2015 at 9.3% against 6.1%, probably because it holds older towns. West started lower and added more land per year.
**Show:** Slide 16 table.

**Q40. Why the ln formula and not simple growth?**
**Say:** UN-Habitat and published studies use the ln formula, so our rate can be compared with others. The simple formula would give a different number for the same data. We name the formula wherever we quote the rate.
**Show:** Slide 12; `08_Project_Notes/05_metrics_and_formulas.md`.

### 3.8 Accuracy

**Q41. How did you check accuracy?**
**Say:** We drew 160 random points from the 2025 map: 50 built-up, 50 cropland, 30 trees and 30 bare. For each we cut a photo about 300 m across from Esri World Imagery and labelled it without seeing the map. Two points under cloud were dropped, so 158 were used. Results are area-weighted (Olofsson method).
**Show:** Slide 19; `04_Data/validation/chips/`.

**Q42. Why should we trust AI-assisted labels?**
**Say:** You should not trust them blindly, and we do not. Two independent interpreters labelled without seeing the map and agreed on 90% of points (95% for built-up versus not). A third look settled the rest. They are still not field visits. We will spot-check a sample, and you can see every chip and sheet.
**Show:** `04_Data/validation/reference_labels.csv`, `labels_A.csv`, `labels_B.csv`; demo 4.4.

**Q43. Is 158 points enough?**
**Say:** It gives usable, not tight, answers. That is why we report a range: corrected built-up 17,706 ± 4,648 ha. More points would shrink that range. This is an honest limit.
**Show:** Slide 19.

**Q44. Explain user's and producer's accuracy.**
**Say:** User's accuracy asks: of the pixels the map calls built-up, how many really are? That is 62%. Producer's accuracy asks: of the real built-up land, how much did the map find? That is 52%. So the map is a little over half right when it says built-up, and finds about half of the real built-up land.
**Show:** Slide 19; `03_Maps_and_Charts/charts/chart_05_accuracy_by_class.png`.

**Q45. 75% overall is not high. Is the map useful?**
**Say:** It is useful for trends, with care. Built-up versus not built-up is 87% right. Cropland is the strongest class (user's 84.3%, producer's 87.1%). Bare/fallow is weakest (35.7% and 27.8%), so do not rely on it.
**Show:** Slide 19; `04_Data/validation/accuracy.json`.

**Q46. You said the map undercounts, but WorldCover agrees 93%. How?**
**Say:** Most pixels are not built-up, so agreement is high even when built-up is missed. For built-up alone, 70.9% of our built-up pixels are built-up in WorldCover, and we find 59.1% of its built-up land. WorldCover finds 12,181 ha in 2020 against our 10,033 ha, which is the same undercount.
**Show:** Slide 19; `04_Data/validation/worldcover_check.json`.

**Q47. What does "17,706 ± 4,648 ha" mean?**
**Say:** It is the area estimate after correcting the map using our checked points. The true 2025 built-up area is probably somewhere between 13,058 and 22,354 ha (95% range). Our map value of 14,786 ha sits inside the range, at the low end.
**Show:** Slide 19; `04_Data/validation/accuracy.json`.

### 3.9 Web map

**Q48. What can the web map do?**
**Say:** A guided tour steps through the findings. You can switch between 2015, 2020, 2025 and a change view, or compare two years side by side with a drag handle, and a play button animates the years. The background can be the Landsat picture of the same year, so you see what each map was made from. You can filter land types and zones, show only land that became built-up, and colour a 1 km² hexagon grid by growth, share, farmland built over or UEII. You can search a town, see figures within 0.5 to 3 km, click any 30 m square for its history, rank the fastest-growing places, copy a link to the exact view, and download the data.
**Show:** Live site; demo 4.1; `03_Maps_and_Charts/screenshots/`.

**Q49. Is it made with qgis2web, as planned?**
**Say:** No. It is a static site we built with Python and the open-source Leaflet library. The plan was qgis2web on GitHub Pages. We chose a custom page so users can compare, filter, search and rank, and we host it free on Codeberg Pages, a non-profit, open-source service. Whether she accepts this is **UNCONFIRMED**.
**Show:** `05_Code/webmap/`; `06_Web_Map/site/`. Slide 20 shows a screenshot of the real dashboard; its speaker notes say it was built with Leaflet, not qgis2web.

**Q50. Does it work offline? Is it safe to publish?**
**Say:** Yes, offline with limits. The land-cover layers, the Landsat satellite background, the tour and the statistics work. The street background map and online search need internet. The site publishes only our results, not the GADM polygons, because of licence. Code is MIT and maps and figures are CC BY 4.0.
**Show:** Demo 4.1b; `06_Web_Map/LIVE_URL.txt`.

**Q51. How are the hexagon numbers made?**
**Say:** Each hexagon is about 1 km². We count built-up pixels inside it for each year and turn them into hectares. The page decodes the map layers in your browser, so the same counting happens on screen. Hexagons carry only a West/East label, not the GADM polygons.
**Show:** Live site, tick "1 km² grid"; `03_Maps_and_Charts/screenshots/webmap_04_hex_grid.png`.

### 3.10 Tools, code and reproducibility

**Q52. Can someone else reproduce your results?**
**Say:** Yes. The scripts, the settings and the seed are in the code. Anyone can run the full pipeline with `05_Code/HOW_TO_RUN.md`. For a quick test, our two demo scripts recompute the areas and the accuracy from the saved maps in under a minute.
**Show:** `05_Code/HOW_TO_RUN.md`; demo 4.3.

**Q53. Can your results open in QGIS?**
**Say:** Yes. Each raster has a same-name .qml style, so QGIS colours it automatically. The Landsat composites have a true-colour style. We can show that now.
**Show:** Demo 4.2; `04_Data/rasters/`.

**Q54. Where is the code and is it public?**
**Say:** It is on GitHub in a public repository, with an MIT licence for code and CC BY 4.0 for maps. The GADM boundary and Esri chips are not published, for licence reasons.
**Show:** https://github.com/SharmaAbhimanyueco/Supriyaaanya; screenshot 9.

**Q55. Why aren't the boundary files in the public repository?**
**Say:** GADM's licence allows academic use but not redistribution. So `Study_Area.zip` is only in the private package copy. Please do not publish it.
**Show:** `04_Data/study_area/`.

### 3.11 Limitations and next steps

**Q56. What is the biggest weakness?**
**Say:** The undercount. The map finds only about half of real built-up land, mostly small villages, roads and houses under trees. Hectares are therefore conservative. The trend and the West-versus-East pattern are less affected.
**Show:** Slide 21.

**Q57. Would you trust the hectare numbers?**
**Say:** Trust the direction and the speed-up, treat the hectares as a floor. For 2025 the corrected estimate of 17,700 ha is the better central number. 2015 is the least certain year, because the earlier sample-based tests moved it by about 1,500 ha.
**Show:** Slide 19, slide 21.

**Q58. What would you do with more time?**
**Say:** Check more points, including field visits. Use Sentinel-2 at 10 m. Train a supervised classifier with our own samples. Use official tehsil boundaries. Add population data for the full SDG 11.3.1 ratio.
**Show:** Slide 22; section 7 below.

---

## 4. Demo scripts

Practise each demo once on your own laptop. Keep it short. If something fails, say so, and move on to a screenshot.

### 4.1 The live web map, and the offline copy (3 to 4 minutes)

**Live site** (needs internet): https://abhimanyu04.codeberg.page/mohali-urban-growth/

1. Open the site. Say: "This is open source and free to use. The strip at the top gives the four key findings."
2. Click **▶ Guided tour** and press **Next** through the nine steps. Each step moves the map and explains one finding with our numbers. Close it with ×.
3. Click **Compare** and drag the round handle. Say: "Left is 2015, right is 2025."
4. Set **Background** to "Satellite, same year (Landsat 8)" and lower **Opacity**. Say: "This is the satellite picture each map was made from."
5. Click **Change**, then set **Show** to "Only farmland that became built-up". Say: "This is the 6,916 ha of cropland that became built-up."
6. In **Search a place**, type **Kharar** and pick it. Say: "The map flies there and shows built-up land within 1 km, by year." Change **Figures within** to 2 km.
7. Tick **1 km² grid coloured by** and pick "built-up growth (ha)". Set **Zone** to East. Say: "The ranking now shows the fastest-growing places in the East zone."
8. Click any point on the map. Say: "Each 30 m square has its own history: 2015, 2020 and 2025."
9. Click **Copy link to this view**, then scroll to **How reliable is it?** and **Download the data**. Say: "The page states the undercount openly, and anyone can download the maps."

**Offline copy** (no internet needed):
- Windows: double-click `06_Web_Map/run_local_windows.bat`.
- Mac or Linux: run `sh 06_Web_Map/run_local_mac_linux.sh`.
- It starts a local server and opens http://localhost:8000.
- Without internet, the land-cover layers, the Landsat background, the tour and the statistics still work. The street background map and online search do not. Say that before she asks. Use the built-in place list, for example Kharar, which still works.
- Do not open `index.html` by double-clicking. The grid and place data will not load.
- Close the black window when done.

### 4.2 Opening the results in QGIS (5 to 6 minutes)

Install QGIS first: the current Long Term Release (LTR) from qgis.org.

**A. The 2025 land-cover map**
1. Drag `04_Data/rasters/lulc_2025.tif` into QGIS. The same-name `lulc_2025.qml` loads automatically, so you should see four colours. If not: Layer Properties, Symbology, Style, Load Style, pick the .qml.
2. Say: "Codes are 1 Built-up, 2 Cropland, 3 Trees, 5 Bare. Code 4, water, is unused."
3. Check the legend in the Layers panel.

**B. The Landsat composite in true colour**
1. Drag `04_Data/landsat_composites/landsat_composite_2025.tif` in. The true-colour style loads.
2. If it does not, open Layer Properties, Symbology, and choose **Multiband color**. Set Red = band 3, Green = band 2, Blue = band 1. The band order is blue, green, red, NIR, SWIR1, SWIR2 (bands 1 to 6, from `05_Code/analysis/build_composites.py`).
3. Values are reflectance × 10,000, and NoData is −32768. If the picture is too dark or too bright, adjust the min and max under Symbology.
4. Say: "This is what the computer saw before classifying: what our eyes would see from space."
5. Turn `lulc_2025` on and off over it, and set opacity to about 60%.

**C. Identify tool**
1. Click **Identify Features** (the "i" cursor). Pick the `lulc_2025` layer. Click a built-up pixel in Mohali.
2. Say: "The pixel value is 1, so built-up. One pixel is 30 m by 30 m, or 0.09 hectare."

**D. Recount areas with a QGIS tool**
1. Open **Processing, Toolbox**, search **Raster layer unique values report**.
2. Input layer: `lulc_2025`. Run it.
3. In the results, find class value 1. The area is given in m². Divide by 10,000: you should get about 14,786 ha, as on slide 15 (small rounding differences are normal).
4. Repeat for `lulc_2015` and check about 7,844 ha.
5. Say: "This is the same count, done in QGIS. It matches our Python result."

**E. Side by side**: see screenshot 4 in section 5.

### 4.3 Re-running a calculation on a laptop (3 to 4 minutes)

**Setup (do this the day before):** Python 3.10 or newer. Then `pip install -r 05_Code/requirements-demo.txt` (numpy and rasterio).

**Script 1: areas**
- Run: `python 05_Code/demo/recompute_areas.py 04_Data/rasters`
- It reads `lulc_2015.tif`, `lulc_2020.tif` and `lulc_2025.tif`, and prints hectares per class per year and the built-up change.
- Check the output against slide 15: 7,844, 10,033 and 14,786 ha for built-up, and +6,942 ha.
- Say: "Each pixel is 0.09 ha. The script counts the pixels of each class and multiplies."

**Script 2: accuracy**
- Run: `python 05_Code/demo/recompute_accuracy.py 04_Data`
- It reads the validation labels and the 2025 maps, and prints the confusion matrix and the overall, user's and producer's accuracy. These are area-weighted (Olofsson method).
- Compare with slide 19: overall 74.6%, built-up user's 62.0% and producer's 51.9%.
- Say: "Rows are what the map said. Columns are what the photo showed. Numbers on the diagonal are the matches."

If the script gives a slightly different number than the slide, do not hide it. Say: "The slide uses `results.json`. Let us look at the difference." Then tell the person who built the package.

### 4.4 Showing the validation evidence (3 minutes)

1. Open `03_Maps_and_Charts/maps/validation_examples.png`. Say: "Six of the 158 points. The yellow square is one 30 m pixel."
2. Open `04_Data/validation/chips/` and pick any chip. Say: "This is the photo each interpreter saw. They could not see our map."
3. Open `04_Data/validation/sheets/` and show a labelling sheet.
4. Open `04_Data/validation/reference_labels.csv`. Show that each point has an agreed label. Then open `labels_A.csv` and `labels_B.csv` and show a disagreement.
5. Offer: "Pick any point and we will compare the chip with the map together."

---

## 5. Screenshot checklist: take these yourselves

Take these on your own laptop. They prove hands-on work and you can paste them into your own slides. Save PNGs in a new folder, for example `07_Teacher_Prep/my_screenshots/`. Windows: `Win+Shift+S`. Mac: `Cmd+Shift+4`.

**1. QGIS: study area on the 2025 true-colour composite**
- **Open:** QGIS, `04_Data/landsat_composites/landsat_composite_2025.tif`, then `04_Data/study_area/Study_Area.zip` (unzip first, drag the .shp in).
- **Steps:** Style the composite true colour. Set the outline to "no fill" with a thick red outline. Turn off the polygon labels (Properties, Labels, No Labels).
- **Visible:** satellite picture, outline, the Layers panel, QGIS title bar.
- **Save as:** `qgis_01_study_area_composite_2025.png`.
- **Slide:** 4, Study area (or slide 7, Data preparation).
- **Why:** proves you opened the data and shows the area clearly. Do not publish the picture with the GADM outline online.

**2. QGIS: lulc_2025 styled with a legend**
- **Open:** `04_Data/rasters/lulc_2025.tif`.
- **Steps:** The .qml loads. Make the Layers panel show the four classes with colours.
- **Visible:** map, class names and colours in the Layers panel.
- **Save as:** `qgis_02_lulc_2025_legend.png`.
- **Slide:** 15, Results: how much and how fast.
- **Why:** shows the result in the teacher's own tool.

**3. QGIS: area report**
- **Open:** Processing Toolbox, **Raster layer unique values report**, input `lulc_2025`.
- **Steps:** Run it. Show the parameters and the results table.
- **Visible:** tool name, input layer, the count and area for each value.
- **Save as:** `qgis_03_area_report_2025.png`.
- **Slide:** 13, GIS and remote sensing analysis (or new slide "Re-counted in QGIS").
- **Why:** shows the numbers can be reproduced in QGIS.

**4. QGIS: 2015 versus 2025 side by side**
- **Open:** `lulc_2015.tif` and `lulc_2025.tif` in two map canvases. Use **View, New Map View** and drag a layer into each. Lock the extent with **Synchronize** (in the Map View panel).
- **Visible:** both maps with the same area, a clear change of red.
- **Save as:** `qgis_04_2015_vs_2025.png`.
- **Slide:** 15 or 16.
- **Why:** shows hands-on change detection.

**5. Web map overview, 2025**
- **Open:** the live site. **Click:** 2025. Make the window wide.
- **Visible:** the map, the year buttons, the legend.
- **Save as:** `mywebmap_01_overview_2025.png`.
- **Slide:** 20, Web map. Its current screenshot was taken offline, without the background map; replace it with yours.
- **Why:** your own screenshot shows the background map and proves you opened the live site.

**6. Web map change view**
- **Steps:** Click **Change**. Set **Show** to "Only farmland that became built-up".
- **Visible:** the Change button highlighted, the filter on.
- **Save as:** `mywebmap_02_change.png`.
- **Slide:** 16, Results: where growth happened.
- **Why:** links to the 6,916 ha finding.

**7. Web map search result**
- **Steps:** Search **Kharar**. Pick it. Wait for the profile card.
- **Visible:** the search text, the map zoomed to Kharar, the figures card.
- **Save as:** `mywebmap_03_search_kharar.png`.
- **Slide:** 20.
- **Why:** shows a place-level answer.

**8. Web map hexagon grid**
- **Steps:** Tick **1 km² grid coloured by**, pick built-up growth. Set Zone to All.
- **Visible:** coloured hexagons, legend, slider.
- **Save as:** `mywebmap_04_hex_grid.png`.
- **Slide:** 16.
- **Why:** shows where growth is concentrated.

**9. GitHub repository page**
- **Open:** https://github.com/SharmaAbhimanyueco/Supriyaaanya
- **Visible:** the file list, the licence label, the repository name.
- **Save as:** `github_01_repository.png`.
- **Slide:** 24 (References) or a new slide "Open source and reproducible".
- **Why:** shows the code is public and licensed.

**10. One validation chip next to the map**
- **Open:** one image from `04_Data/validation/chips/` and `lulc_2025.tif` zoomed to the same place (use the point's coordinates in `sample_points.csv`).
- **Visible:** photo on the left, map on the right, the same location.
- **Save as:** `validation_01_chip_vs_map.png`.
- **Slide:** 19, Accuracy check.
- **Why:** shows what an accuracy check looks like on one point.

### Ready-made screenshots and charts

| File in `03_Maps_and_Charts/` | Best slide |
|---|---|
| `maps/location_map.jpg` | 4 Study area |
| `maps/map_lulc_2015.png`, `map_lulc_2020.png`, `map_lulc_2025.png` | 15 Results: how much and how fast |
| `maps/map_change_2015_2025.png` | 16 Results: where growth happened |
| `maps/validation_examples.png` | 19 Accuracy check |
| `charts/chart_01_builtup_trend.png` | 12 and 15 |
| `charts/chart_02_landcover_by_year.png` | 15, or backup for Q31 |
| `charts/chart_03_zones.png` | 16 |
| `charts/chart_04_new_builtup_sources.png` | 16 |
| `charts/chart_05_accuracy_by_class.png` | 19 |
| `charts/chart_06_k_selection.png` | 18 Model checks |
| `charts/chart_07_stability.png` | 18 Model checks |
| `screenshots/webmap_01_overview_2025.png` | 20 Web map |
| `screenshots/webmap_02_compare_2015_2025.png` | 20, or 15 (how much and how fast) |
| `screenshots/webmap_03_search_kharar.png` | 20 |
| `screenshots/webmap_04_hex_grid.png` | 16 (where growth happened) |
| `screenshots/webmap_05_tour_change.png` | 20 (the guided tour) |
| `screenshots/webmap_06_phone.png` | 20 (works on a phone) |
| `screenshots/webmap_07_satellite_compare.png` | 9 (what the satellite sees) |

---

## 6. Day-before checklist

**Laptop and files**
- [ ] Laptop charged, charger packed. Packed an adapter for the projector (HDMI or USB-C).
- [ ] The whole `Urban_Growth_Handover` folder is copied to the laptop, and a second copy is on a USB drive.
- [ ] A PDF backup of the slides: `02_Presentation/Urban_Growth_Mohali_slides.pdf`, also on your phone.
- [ ] `02_Presentation/slide_images/` ready, in case PowerPoint fails.

**Offline web map**
- [ ] Run `06_Web_Map/run_local_windows.bat` (or `sh 06_Web_Map/run_local_mac_linux.sh`) once with Wi-Fi **off**.
- [ ] Confirm the layers load, 2015 and 2025 switch, and the grid appears.
- [ ] Try the live site on your phone's hotspot too.

**QGIS and Python**
- [ ] QGIS installed. Open `lulc_2025.tif` once. Run the unique values report once.
- [ ] Python 3.10 or newer installed. `pip install -r 05_Code/requirements-demo.txt` done. Both demo scripts run once.
- [ ] Your 10 screenshots from section 5 are taken and in a folder.

**Content**
- [ ] Spot-check 10 to 15 validation chips against `reference_labels.csv`. Write down how many you checked and any you disagree with.
- [ ] Add your own screenshots to the slides. Replace the slide 20 screenshot with your own of the live site.
- [ ] Read the sentences about **UNCONFIRMED** items (satellite, years, K-means or ISODATA, validation level, web map tool, deadline, missing slide 16). If the teacher has answered, update the slides.
- [ ] Check wording of the SDG targets on sdgs.un.org (slide 3 notes). Check the references on slide 24.

**Rehearsal**
- [ ] Run the full presentation twice with a timer. Agree who speaks on which slide.
- [ ] Practise the 60-second story and the three disclosures, out loud.
- [ ] Each of you answers five random questions from section 3 without reading.
- [ ] Sleep. Arrive early. Open the live site and the offline site before she comes in.

---

## 7. What we would do next

Say these as honest next steps, not as failures.

1. **More photo and field checks.** 158 points gives a wide range (± 4,648 ha). More points, with a few field visits, would narrow it and replace the AI-assisted labels with checked ones.
2. **Sentinel-2 at 10 m.** Smaller pixels would catch small villages, roads and houses under trees, and reduce the undercount.
3. **Supervised classification with our own training samples.** We would define the classes ourselves, and could add a water class and separate bare land from built-up.
4. **Official tehsil boundaries.** This would replace the West and East zones with real administrative units and let us report by tehsil, and also check the study-area total of about 108,800 ha.
5. **Population data for the full SDG 11.3.1 ratio.** Dividing the land consumption rate by the population growth rate needs a population figure for each year. India's last census was in 2011 (check the dates of the next one), so we need other sources.
6. **Also named in the deck:** hotspot analysis (Getis-Ord Gi*) and a Development Pressure Index (distance to built-up areas, roads, the airport and town centres).
7. **Re-do the analysis in QGIS** if the teacher requires it, following `08_Project_Notes/04_qgis_steps.md`.

**Open items waiting for the teacher (UNCONFIRMED):** satellite and years; K-means or ISODATA; validation level; web map tool (qgis2web or our custom page); 5 km buffer; deadline and format; the missing slide 16 in her list.
