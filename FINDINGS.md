# 🎓 Student Performance Analysis Report (Hashemite Technical University)
**Prepared by:** Jumana (Jumana-ML)  
**Role:** AI Engineer  
**Date:** April 2026  

---

## 1. Dataset Description & Quality Control
The analysis was performed on a dataset of **2,000 students** at Hashemite Technical University across 5 departments.

* **Data Shape:** 2,000 rows × 10 columns. (See `output/data_profile.txt`)
* **Key Issues Handled:**
    * **Commute Minutes:** Found 181 missing values (~9%). Handled via **Median Imputation** to maintain statistical robustness against extreme outliers.
    * **Scholarship Status:** 389 missing values (~19%) were identified. These were categorized as **'None'**, representing self-funded students.
    * **Study Hours:** Minimal missing data (~5%) was handled by dropping rows (MCAR) to ensure the integrity of the correlation analysis.

---

## 2. Distribution & Categorical Insights
* **GPA Distribution:** The data shows a **Left-Skewed distribution** for GPAs (*See `output/dist_gpa.png`*), meaning the majority of students are high-achievers with scores clustering in the 2.5–3.5 range.
* **Departmental Box Plots:** (*See `output/boxplot_gpa_by_department.png`*)
    * **Computer Science** and **Mathematics** show relatively stable/higher median GPAs.
    * The **Engineering** department shows a wider "Interquartile Range" (IQR), indicating a higher variance in student performance.
* **Scholarship Distribution:** The bar chart (*See `output/barchart_scholarships.png`*) confirms that the majority of students are in the 'None' category, followed by 'Merit' and 'Need-based' grants.

---

## 3. Correlation Analysis (Key Drivers)
We calculated the **Pearson Correlation Matrix** (*See `output/correlation_heatmap.png`*) to identify which factors actually drive academic success:

| Relationship | Correlation (r) | Strength |
| :--- | :--- | :--- |
| **Study Hours vs. GPA** | **0.639** | **Moderate-to-Strong Positive** |
| **Commute vs. GPA** | **0.100** | **Very Weak/Negligible** |
| **Attendance % vs. GPA** | **0.040** | **No Correlation** |

* **The "Study Factor":** With $r = 0.64$ (*See `output/scatter_top_pair_1.png`*), weekly study hours are the single most reliable predictor of a student's GPA.
* **The "Attendance Paradox":** A correlation of $0.04$ is statistically negligible. This suggests that simply "showing up" does not influence the GPA in this dataset—actual engagement (study hours) is what matters.
* **Caveat:** Correlation is not causation. While study hours and GPA move together, we cannot overlook internal factors like student aptitude or prior background.

---

## 4. Hypothesis Testing Results

### Hypothesis 1: Internship Impact (Independent T-Test)
* **Statement:** Students with internships achieve higher GPAs than those without.
* **Statistical Results:** $t$-statistic = `13.5644`, $p$-value = `3.68e-40`.
* **Interpretation:** The result is highly statistically significant ($p < 0.05$). We reject the null hypothesis. 
* **Effect Size (Cohen’s d):** `0.6898`. This represents a **medium-to-large effect size**, confirming that the GPA difference is not just mathematically significant but practically meaningful for career readiness.

### Hypothesis 2: Scholarship vs. Department (Chi-Square Test)
* **Statement:** Scholarship status is associated with specific departments.
* **Statistical Results:** Chi-square statistic = `17.1358`, $p$-value = `0.3768`, Degrees of Freedom = `16`.
* **Interpretation:** Because $p > 0.05$, we **fail to reject the null hypothesis**. Scholarships are distributed fairly and independently across all university departments.

---

## 5. Actionable Recommendations

1. **Shift Focus from Attendance to Engagement:** Since attendance has almost zero correlation with GPA ($r = 0.04$), the university should evaluate *how* lectures are delivered. Moving toward an **Active Learning** model (flipped classrooms) might turn attendance into a more meaningful predictor of success.
2. **Structured Study Groups:** Given that study hours are the primary driver ($r = 0.64$), departments should facilitate peer-to-peer study sessions. Providing "Guided Study Hours" in the library could help students reach that "Success Threshold" faster.
3. **Expansion of Internship Programs:** The T-test proved that internships significantly enhance academic performance (Cohen's d = 0.69). HTU should partner with tech sectors to secure "Micro-Internships" for the student body, as the data shows a clear academic "lift" for those with practical experience.