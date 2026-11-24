# Model checks (all numbers from model_checks.json)

**Is k = 10 suitable?** Reasonable, not optimal by statistics. Silhouette is highest at k = 4 (0.386) and falls to 0.299 at k = 10; the inertia elbow (max distance to chord) is at k = 8; Davies-Bouldin is best at k = 16 and Calinski-Harabasz at k = 4. Silhouette is flat (about 0.30-0.33) from k = 5 to 16. Since clusters are merged into 4 classes afterwards, more clusters than classes is normal, so k = 10 is defensible.

**Convergence?** Yes. The refit stopped at iteration 24 of 100 (inertia 437.03). However, it did not reproduce the saved centres (max absolute difference 0.123 reflectance) and gives different built-up hectares (7,759 / 9,907 / 14,594 vs reference 6,609 / 9,224 / 14,529). Classifying with the saved centres does reproduce the reference hectares.

**Stable?** Only moderately. Built-up range over 5 re-runs: 2015 6,698-8,177 ha (CV 7.8%); 2020 9,288-10,647 ha (5.7%); 2025 14,426-15,842 ha (4.7%). Adjusted Rand index vs saved reference 0.52-0.92; 4-class agreement 86.4-98.7%. The direction and rough size of growth are consistent in every run.

**Sample size?** Little effect: 50k/100k/200k pixels per year give 2015 6,799/7,759/6,779 ha, 2020 9,441/9,907/9,394, 2025 14,756/14,594/14,656. Seed matters more than size.

**Caveats:** no ground-truth accuracy was assessed. Built-up depends on which clusters are called built-up (each run mapped one cluster to Built-up by nearest reference centre), so 2015 is the least certain year. Report built-up as a range, e.g. roughly 6,600-8,200 ha for 2015.
