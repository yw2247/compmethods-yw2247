# Problem Set 3
**Name:** Yu (Irene) Wang<br>
**NetID:** yw2247        <br>
## Instructions to Run Code
- Python 3.x required  
- Install dependencies:  
  ```bash
  pip install pandas matplotlib sqlite3

### Exercise 1: Retrieving PubMed Data via Entrez API<br>
**1a. Retrieve PubMed IDs for Alzheimer’s and Cancer Papers**<br> 
PubMed IDs for 1000 Alzheimer’s papers and 1000 cancer papers from 2024 were retrieved. 

**1b. Retrieve Metadata for the Papers**<br> 
The results were saved in two JSON files: "alzheimers_2024_metadata.json" and "cancer_2024_metadata json".<br>
Note: 1 record from the cancer set returned no metadata, likely because the corresponding PubMed entry lacked an abstract or was not a standard article.

**1c. Analyze Overlap Between the Two Paper Sets**<br> 
PubMed ID 40162470 is present in both the Alzheimer’s and cancer paper sets.<br>

**1d. Handle Structured Abstracts**<br> 
*Identify any limitations for your approach.*
For papers that have structured abstracts (with multiple <AbstractText> sections such as Background, Methods, and Results), the code collects all parts of the abstract and joins them into one continuous string.

- Each section’s text is extracted and cleaned using XML parsing.<br>
- If a section has a label (e.g., “Background”), the label is kept and placed before the text (for example, “Background: …”).<br>
- All parts are then concatenated with spaces to form a single, complete abstract in the output JSON file.<br>

This ensures that no part of the abstract is lost, even when it’s divided into multiple sections.<br>

Limitation:<br>
Combining all sections into one string makes the abstract easier to store but removes the clear separation between sections. This means it is not possible to tell where one section ends and another begins. A better approach would store each section as a list of labeled parts instead of one combined string.<br>

### Exercise 2: SPECTER Embeddings and Principal Component Analysis<br>
*Apply principal component analysis (PCA) to identify the first three principal components.*<br>
A total of 1998 papers were analyzed (1000 on Alzheimer’s disease and 999 on cancer, with 1 overlap). Using the SPECTER model, each paper’s title and abstract were converted into a 768-dimensional embedding, and PCA was applied to reduce the data to three principal components. The first three components explained 18.4%, 6.2%, and 4.9% of the total variance, respectively.

*Plot 2D scatter plots for PC0 vs PC1, PC0 vs PC2, and PC1 vs PC2; color code these by the search query used (Alzheimers vs cancer).* 

<img src="plots/Figure_1.png" width="750"/>

<img src="plots/Figure_2.png" width="750"/>

<img src="plots/Figure_3.png" width="750"/>

*Comment on the separation or lack thereof, and any take-aways from that.*<br>
- PC0 vs PC1<br>
In this plot, there is a clear separation between Alzheimer’s and cancer papers along the PC0 axis. Most Alzheimer’s papers appear on the left, and most cancer papers on the right, with only a small overlap. This suggests that the main direction of variance (PC0) captures strong topic-level differences between the two groups.

- PC0 vs PC2<br>
A similar pattern is seen in this plot: the two groups remain mostly distinct along PC0, while PC2 adds some variation within each topic. This shows that PC0 is still the primary dimension of separation, and PC2 may represent subtopics variations within each disease area.

- PC1 vs PC2<br>
Here, the two topics overlap considerably. Without PC0, it is much harder to distinguish the two groups. This indicates that PC1 and PC2 mainly capture within-topic diversity rather than overall differences between Alzheimer’s and cancer papers.

Takeaways:<br>
- SPECTER embeddings effectively capture topic information. PCA reveals clear clustering by research area.<br>
- PC0 strongly separates the two disease topics, suggesting the embeddings encode distinct semantic patterns related to each field.<br>
- PC1 and PC2 reflect finer differences (for example, study type or research focus) within each disease group.<br>
- Overall, these findings show that SPECTER embeddings meaningfully organize research papers by topic, and PCA provides an interpretable visualization of this high-dimensional text representation.<br>

### Exercise 3: Computer math vs calculus<br>

<img src="plots/Figure_4.png" width="750"/>

As h becomes smaller, [f(3+h)−f(3)]/h initially gets closer to the true derivative value of 27, and the error decreases. However, after a certain point (around h≈10^−8), the error starts to increase again even though h continues to shrink. Hypothesis: This happens because of round-off error in computer arithmetic. When h is extremely small, f(3+h) and f(3) are almost equal, so subtracting them causes a loss of precision due to limited floating-point accuracy. Dividing this small difference by a tiny h amplifies the rounding error, making the result less accurate. Therefore, as we can see, for moderate h, the approximation improves as expected, but for very small h, floating-point precision limits cause the numerical result to deviate from the true derivative.

### Exercise 4: Health and disease<br>
*Plot the time course of the number of infected individuals until that number drops below 1.*<br>

<img src="plots/Figure_5.png" width="750"/>

*For those parameter values, when does the number of infected people peak? How many people are infected at the peak?*<br>
Peak time ≈ 11.74 days<br>
Peak infected ≈ 21070 people<br>

*Unfortunately, for new diseases, we may not know beta or gamma with much accuracy. Vary these two variables over "nearby" values, and plot on a heat map how the time of the peak of the infection depends on these two variables.*

<img src="plots/Figure_6.png" width="750"/>

*Do the same for the number of individuals infected at peak.*

<img src="plots/Figure_7.png" width="750"/>

### Exercise 5: Data Exploration for Hospital Readmissions Reduction Program Dataset<br>
*License permitting reuse*<br>
The dataset comes from the Centers for Medicare & Medicaid Services (CMS) Provider Data Catalog:https://data.cms.gov/provider-data/dataset/9n3s-kdb3<br>
According to CMS’s Terms of Use, data posted on data.cms.gov are publicly available and free for reuse with attribution.<br>

*Present a representative set of figures that gives insight into the data. Comment on the insights gained.*

Four figures were created to summarize the Hospital Readmissions Reduction Program (HRRP) dataset from the Centers for Medicare & Medicaid Services.

<img src="figs/fig1_err_hist.png" width="750"/>

Figure 1 shows the distribution of the Excess Readmission Ratio (ERR) across all hospitals. The values are centered around 1.0, which means most hospitals perform close to the national expectation. A few hospitals have ERR > 1.1, indicating slightly higher-than-expected readmissions.

<img src="figs/fig2_err_by_measure.png" width="750"/>

Figure 2 compares ERR values across the six clinical measures (AMI, HF, CABG, COPD, PN, and HIP/KNEE). The medians are close to 1.0 for all measures, but CABG and COPD show a wider spread, suggesting more variation in hospital performance for those conditions.

<img src="figs/fig3_volume_vs_err.png" width="750"/>

Figure 3 plots the number of discharges (hospital volume) against ERR. The variability in ERR is greater among hospitals with fewer discharges, which is expected because smaller hospitals tend to have more unstable rates. Larger hospitals cluster more tightly around 1.0, showing consistent performance.

<img src="figs/fig4_state_mean_err.png" width="750"/>

Figure 4 displays the average ERR by state. Most states have mean ERR values near 1.0, indicating that differences across states are modest. This suggests that CMS’s risk-adjustment methods are working to keep state-level comparisons fair.

Overall, these plots show that hospital performance is fairly consistent nationwide, with small differences by condition and hospital size.


*Identify any data cleaning needs (this includes checking for missing data) and write code to perform them. If the data does not need to be cleaned, explain how you reached this conclusion.*

Before analysis, the dataset contained text values such as "N/A" and "Too Few to Report" in numeric columns. These were converted to missing values (NaN) so that calculations could be done correctly. Numeric columns such as Number of Discharges, Excess Readmission Ratio, and Predicted/Expected Readmission Rate were then converted to numeric type. Date columns were also checked and found to be identical for all rows, so they were dropped to simplify the data.

A check for missingness showed that about 35% of rows lacked ERR and related fields, which corresponds to hospitals with too few cases to report. These rows were excluded from numeric summaries and figures. All remaining data were valid, with no duplicates or inconsistent types.

```python
import pandas as pd

na_like = ["N/A", "Too Few to Report", ""]
df = pd.read_csv("FY_2025_Hospital_Readmissions_Reduction_Program_Hospital.csv",
                 na_values=na_like)

num_cols = ["Number of Discharges", "Excess Readmission Ratio",
            "Predicted Readmission Rate", "Expected Readmission Rate",
            "Number of Readmissions"]

for c in num_cols:
    df[c] = pd.to_numeric(df[c], errors="coerce")

df = df.drop(columns=["Start Date", "End Date"])
df_clean = df[df["Excess Readmission Ratio"].notna()]
```
After cleaning, the dataset contained only valid numeric entries and was ready for exploration.
