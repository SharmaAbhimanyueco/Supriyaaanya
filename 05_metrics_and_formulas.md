# Which numbers to report, and how to calculate them

This is the research-based answer to "which number shows how much the area urbanised?". The main number is the **increase in built-up area in hectares**, which is what the teacher asks for. Published studies and the UN's SDG method add a few standard measures, and each one answers a different question.

## The measures

In the Excel examples, B2 is the earlier year's built-up hectares, C2 the later year's, B8 the total hectares, D2 the zone's hectares, and the gap between the years is 5.

| Question | Measure | Formula | Excel example |
|---|---|---|---|
| How much? | Increase in built-up area | later ha − earlier ha | `=C2-B2` |
| How much per year? | Average built-up added per year | (later − earlier) ÷ years | `=(C2-B2)/5` |
| How much, relatively? | Percent change | (later − earlier) ÷ earlier × 100 | `=(C2-B2)/B2*100` |
| What part of the area? | Built-up share | built-up ha ÷ total ha × 100 | `=B2/B$8*100` |
| How fast? | Land consumption rate (SDG 11.3.1 formula) | ln(later ÷ earlier) ÷ years × 100 | `=LN(C2/B2)/5*100` |
| Where, fairly? | Urban Expansion Intensity Index (UEII) | (later − earlier) ÷ (zone ha × years) × 100 | `=(C2-B2)/(D2*5)*100` |
| What land was lost? | Cropland that became built-up | from–to table, code 21 | from the QGIS report |

Notes:
- **Hectares from QGIS:** ha = m² ÷ 10,000, which equals the pixel count × 0.09.
- **Total ha** for the share: add up all five classes from that year's unique values report, so the total matches the map exactly.
- **ln** is the natural logarithm: `LN()` in Excel, or the "ln" key on a scientific calculator. It turns "grew from A to B in 5 years" into one steady yearly rate, the way a bank works out compound interest.
- **UEII** compares zones of different sizes fairly, the same way you turn marks out of 50 and out of 100 into percentages before comparing them. Some studies label the value with speed bands: below 0.28 slow, 0.28–0.59 low, 0.59–1.05 medium, 1.05–1.92 high, above 1.92 very high. These bands are a convention, not a rule.
- **SDG 11.3.1:** the UN measures the whole urban area, parks included, while we count only built-up pixels. So write "calculated with the SDG 11.3.1 formula", not "the SDG 11.3.1 value". Check the formula on the UN metadata page before you quote it.

## Why the choice of formula matters (an example, not a result)

Suppose built-up land doubled in 5 years. The "yearly growth" would then be 20% with the simple formula, 14.9% with the compound formula (used by FAO), and 13.9% with the ln formula (used by UN-Habitat and by Puyravaud, 2003). Choose one standard formula and always say which one you used.

## Left out, and why

- **The full SDG 11.3.1 ratio** (land consumption rate ÷ population growth rate) needs population figures for 2015–2025. India's last census was in 2011, and the next one counts people in early 2027. List it under limitations and future work.
- **Sprawl indices** (Shannon's entropy, landscape metrics) measure how scattered growth is, not how much there was, and they add work. They belong in future work.

## Accuracy caution

All of these numbers come from counting pixels on maps that contain mistakes. The standard reference (Olofsson et al., 2014) says plain pixel counts are biased. It recommends estimating areas from a random sample of hand-checked points and reporting a ± range. Do this if the teacher wants accuracy figures (question 4 in the message).

## Tables to fill in

Built-up area by year:

| | 2015 | 2020 | 2025 |
|---|---|---|---|
| Built-up (ha) | | | |
| Built-up share (%) | | | |

Change in built-up area:

| Period | Increase (ha) | ha per year | % change | Land consumption rate (% per year) |
|---|---|---|---|---|
| 2015–2020 | | | | |
| 2020–2025 | | | | |
| 2015–2025 | | | | |

All classes:

| Class | 2015 ha | 2020 ha | 2025 ha | Change 2015–2025 (ha) |
|---|---|---|---|---|
| Built-up | | | | |
| Cropland | | | | |
| Trees/vegetation | | | | |
| Water | | | | |
| Bare/fallow | | | | |
| Total | | | | |

By zone:

| Zone | Zone ha | Built-up 2015 (ha) | Built-up 2025 (ha) | UEII 2015–2025 |
|---|---|---|---|---|
| West (Kharar and Mohali) | | | | |
| East (Dera Bassi, incl. Zirakpur) | | | | |
| Zirakpur area (approximate) | | | | |

## Charts to make

1. A bar chart of hectares by class, with one group of bars per year.
2. A line chart of built-up hectares for 2015, 2020 and 2025.
3. A bar chart of UEII by zone.

## Sources

- UN SDG indicator 11.3.1 metadata: https://unstats.un.org/sdgs/metadata/files/Metadata-11-03-01.pdf
- UN-Habitat 11.3.1 metadata: https://unhabitat.org/sites/default/files/2020/07/metadata_on_sdg_indicator_11.3.1.pdf
- Puyravaud, J.-P. (2003). Standardizing the calculation of the annual rate of deforestation. *Forest Ecology and Management* 177, 593–596.
- Olofsson, P., Foody, G.M., Herold, M., Stehman, S.V., Woodcock, C.E. and Wulder, M.A. (2014). Good practices for estimating area and assessing accuracy of land change. *Remote Sensing of Environment* 148, 42–57. https://doi.org/10.1016/j.rse.2014.02.015
- UEII speed bands as used in: https://www.mdpi.com/2220-9964/11/7/406

I couldn't open the full texts of these documents from my session. The formulas come from search results and from standard references. Check the SDG wording and formula on the UN pages before you quote them.
