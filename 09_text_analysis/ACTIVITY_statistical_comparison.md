# 📌 ACTIVITY

## Statistical Comparison of Prompt Performance

🕒 *Estimated Time: 15-20 minutes*

---

## ✅ Your Task

Learn to use t-test and ANOVA to compare quality control scores across different prompts. This activity teaches you statistical hypothesis testing skills needed for Homework 3, where you'll design your own experiment comparing prompt performance.

### 🧱 Stage 1: Load and Explore Quality Control Scores

- [x] Open [`03_statistical_comparison.R`](03_statistical_comparison.R) or [`03_statistical_comparison.py`](03_statistical_comparison.py) in your IDE
- [x] Review the script structure and comments to understand the statistical approach
- [x] Run the script to load the quality control scores from [`data/prompt_comparison_scores.csv`](data/prompt_comparison_scores.csv)
- [x] Observe the summary statistics by prompt: which prompt has the highest mean overall score?
- [x] Note the differences in means and standard deviations between prompts

### 🧱 Stage 2: Perform T-Test to Compare Two Prompts

- [x] Review how Bartlett's test checks for equal variances
- [x] Understand the t-test comparing Prompt A vs Prompt B
- [x] Run the script and view the t-test results
- [x] Interpret the p-value: is the difference between Prompt A and Prompt B statistically significant?

### 🧱 Stage 3: Perform ANOVA to Compare All Three Prompts

- [x] Review how ANOVA compares all three prompts simultaneously
- [x] Understand the difference between standard ANOVA and Welch's ANOVA (for unequal variances)
- [x] Run the script and view the ANOVA results
- [x] Interpret the F-statistic and p-value: do prompts differ significantly?

### 🧱 Stage 4: Interpret Results and Explore Quality Dimensions

- [x] Review the interpretation sections in the script output
- [x] Examine the formality and succinctness comparisons
- [x] Understand what the statistical tests tell us about prompt performance
- [x] Note how statistical significance differs from practical significance

---

## 📤 To Submit

- For credit: Submit a screenshot showing:
  1. The t-test results (comparing Prompt A vs Prompt B)
  2. The ANOVA results (comparing all three prompts)
  3. The interpretation output showing whether differences are statistically significant

---

![](../docs/prep/icons.png)

---

← 🏠 [Back to Top](#ACTIVITY)
