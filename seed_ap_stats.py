"""
seed_ap_stats.py — Seeds the college_ready.db with 84 AP Statistics questions.

Track: ap_stats
Units (sat_domain field):
  exploring_data      (14 Qs) — distributions, center, spread, boxplots, histograms
  two_var_data        ( 6 Qs) — scatterplots, correlation, LSRL, residuals
  collecting_data     (10 Qs) — experiments vs observational, sampling, bias, randomization
  probability         (12 Qs) — probability rules, conditional, independence, binomial, geometric
  sampling_dist       ( 8 Qs) — sampling distributions, CLT, standard error
  inference_proportions (12 Qs) — CIs for proportions, z-tests, hypothesis testing
  inference_means     (12 Qs) — t-tests, CIs for means, paired vs two-sample
  chi_square          ( 5 Qs) — goodness of fit, independence, homogeneity
  inference_slopes    ( 5 Qs) — regression inference, t-test for slope

FUAR: F (Fluency), U (Understanding), A (Application), R (Reasoning)
Difficulty: 1–5
"""

import sqlite3
from collections import defaultdict

DB_PATH = "college_ready.db"

# ---------------------------------------------------------------------------
# Question bank
# Each tuple: (track, sat_domain, fuar_dimension, difficulty,
#              question_text, question_type,
#              option_a, option_b, option_c, option_d,
#              correct_answer, explanation, topic_tag)
# ---------------------------------------------------------------------------

QUESTIONS = [

    # =========================================================================
    # EXPLORING DATA — 14 questions (F×4, U×4, A×3, R×3)
    # =========================================================================

    # ED-1 F diff=1
    ("ap_stats", "exploring_data", "F", 1,
     "Which measure of center is most resistant to extreme outliers?",
     "multiple_choice",
     "Mean", "Median", "Mode", "Range",
     "B",
     "The median is resistant to outliers because it depends only on the middle value(s), not the magnitude of extreme values. The mean is pulled toward outliers.",
     "center_spread"),

    # ED-2 F diff=1
    ("ap_stats", "exploring_data", "F", 1,
     "A distribution is described as skewed right. Which statement is most likely true?",
     "multiple_choice",
     "The mean equals the median.",
     "The mean is less than the median.",
     "The mean is greater than the median.",
     "The median is greater than the mode.",
     "C",
     "In a right-skewed distribution, the tail pulls the mean toward higher values, making the mean greater than the median. A common memory aid: the mean chases the tail.",
     "distributions"),

    # ED-3 F diff=2
    ("ap_stats", "exploring_data", "F", 2,
     "The five-number summary for a dataset is: Min = 10, Q1 = 20, Median = 30, Q3 = 45, Max = 70. What is the interquartile range (IQR)?",
     "multiple_choice",
     "15", "20", "25", "60",
     "C",
     "IQR = Q3 − Q1 = 45 − 20 = 25. The IQR measures the spread of the middle 50% of the data.",
     "center_spread"),

    # ED-4 F diff=2
    ("ap_stats", "exploring_data", "F", 2,
     "Using the 1.5 × IQR rule, a value is an outlier if it is below Q1 − 1.5(IQR) or above Q3 + 1.5(IQR). For a dataset with Q1 = 20 and Q3 = 50, what is the upper fence (the boundary above which values are outliers)?",
     "multiple_choice",
     "65", "80", "95", "110",
     "C",
     "IQR = Q3 − Q1 = 50 − 20 = 30. Upper fence = Q3 + 1.5 × IQR = 50 + 1.5(30) = 50 + 45 = 95. Any value above 95 would be flagged as a potential high outlier. Lower fence = 20 − 45 = −25.",
     "center_spread"),

    # ED-5 U diff=2
    ("ap_stats", "exploring_data", "U", 2,
     "A histogram of exam scores is unimodal and roughly symmetric with mean 74 and standard deviation 8. Approximately what percentage of scores fall between 66 and 82?",
     "multiple_choice",
     "34%", "50%", "68%", "95%",
     "C",
     "66 = 74 − 8 = mean − 1 SD; 82 = 74 + 8 = mean + 1 SD. By the Empirical Rule (68-95-99.7), approximately 68% of values fall within 1 standard deviation of the mean for a roughly normal distribution.",
     "normal_distribution"),

    # ED-6 U diff=2
    ("ap_stats", "exploring_data", "U", 2,
     "Two datasets have the same mean of 50. Dataset A has standard deviation 2; Dataset B has standard deviation 10. Which statement correctly compares them?",
     "multiple_choice",
     "Dataset A is more spread out than Dataset B.",
     "Dataset B is more spread out than Dataset A.",
     "Both datasets have the same spread.",
     "The dataset with the larger standard deviation has a higher mean.",
     "B",
     "Standard deviation measures spread around the mean. A larger standard deviation means more variability. Dataset B (SD = 10) is more spread out than Dataset A (SD = 2). The means are equal, so mean tells us nothing about spread.",
     "center_spread"),

    # ED-7 U diff=3
    ("ap_stats", "exploring_data", "U", 3,
     "A boxplot shows Q1 = 30, Median = 35, Q3 = 50, with whiskers at 15 and 65, and a dot at 85. What does the dot at 85 represent?",
     "multiple_choice",
     "The maximum value in the dataset.",
     "A value exactly 1.5 IQRs above Q3.",
     "A potential outlier identified by the 1.5 × IQR rule.",
     "The mean of the dataset.",
     "C",
     "In a standard boxplot, dots beyond the whiskers represent potential outliers identified by the 1.5 × IQR rule. The whisker extends to the most extreme non-outlier value. The dot at 85 lies beyond the upper whisker and is flagged as a potential outlier.",
     "boxplots"),

    # ED-8 U diff=3
    ("ap_stats", "exploring_data", "U", 3,
     "A student scores 78 on an exam where the class mean is 70 and the standard deviation is 4. What is the student's z-score?",
     "multiple_choice",
     "0.5", "1.5", "2.0", "3.0",
     "C",
     "z = (x − μ) / σ = (78 − 70) / 4 = 8 / 4 = 2.0. A z-score of 2 means the student scored 2 standard deviations above the mean.",
     "z_scores"),

    # ED-9 A diff=3
    ("ap_stats", "exploring_data", "A", 3,
     "A data analyst reports that the median household income in a city is $55,000 while the mean is $82,000. What does this suggest about the income distribution?",
     "multiple_choice",
     "The distribution is roughly symmetric.",
     "The distribution is skewed left with a few very low incomes pulling the mean down.",
     "The distribution is skewed right with a few very high incomes pulling the mean up.",
     "The data contains a calculation error because the mean should equal the median.",
     "C",
     "When the mean is significantly greater than the median, it suggests right skew. A few very high incomes (outliers on the high end) pull the mean upward while the median remains resistant. This is typical of income distributions.",
     "distributions"),

    # ED-10 A diff=3
    ("ap_stats", "exploring_data", "A", 3,
     "A teacher records test scores: 55, 60, 65, 70, 70, 75, 80, 85, 90, 100. If the score of 100 is changed to 200 due to a data entry error, which measures will change?",
     "multiple_choice",
     "Only the mean will change.",
     "Only the median will change.",
     "Both the mean and median will change.",
     "Neither the mean nor the median will change.",
     "A",
     "Changing the maximum value from 100 to 200 affects the mean (which uses all values in its calculation) but not the median (which depends only on the order of values). With 10 data points, the median is the average of the 5th and 6th values (70 and 75), which are unaffected.",
     "center_spread"),

    # ED-11 A diff=4
    ("ap_stats", "exploring_data", "A", 4,
     "A distribution of test scores has mean 72 and standard deviation 6. If every score is multiplied by 1.1 and then 5 points are added, what is the new standard deviation?",
     "multiple_choice",
     "6.0", "6.6", "7.1", "11.6",
     "B",
     "Adding a constant to all values shifts the distribution but does not change the spread. Multiplying by a constant scales the spread. New SD = 1.1 × 6 = 6.6. The +5 does not affect the standard deviation.",
     "transformations"),

    # ED-12 R diff=4
    ("ap_stats", "exploring_data", "R", 4,
     "A researcher compares two histograms. Histogram A is symmetric and bell-shaped. Histogram B has a long left tail. A student claims: 'The median of B is greater than its mean.' Is the student correct?",
     "multiple_choice",
     "Yes, because in left-skewed distributions the median exceeds the mean.",
     "No, because the mean is always greater than the median.",
     "No, because symmetry is required for the median to differ from the mean.",
     "Yes, because the mode is always the highest point in any distribution.",
     "A",
     "In a left-skewed (negatively skewed) distribution, the tail pulls the mean toward lower values. Therefore the mean < median. The student's claim is correct: the median exceeds the mean in a left-skewed distribution.",
     "distributions"),

    # ED-13 R diff=4
    ("ap_stats", "exploring_data", "R", 4,
     "A professor says: 'Since the standard deviation of scores increased from 8 to 12 after a difficult exam, students performed worse on average.' Is this reasoning valid?",
     "multiple_choice",
     "Yes, a higher standard deviation always means lower scores.",
     "No, standard deviation measures spread, not the level of scores. The mean must be examined separately.",
     "Yes, because more spread means more students failed.",
     "No, because standard deviation and mean always move in the same direction.",
     "B",
     "Standard deviation measures variability (spread), not the center. An increase in SD means scores were more spread out, but says nothing about whether the average score was higher or lower. The mean must be compared separately to assess average performance.",
     "center_spread"),

    # ED-14 R diff=5
    ("ap_stats", "exploring_data", "R", 5,
     "Two classes take the same exam. Class 1: mean = 80, SD = 5. Class 2: mean = 80, SD = 15. A student who scored 90 took one of the classes but doesn't remember which. In which class would a score of 90 be more unusual?",
     "multiple_choice",
     "Class 1, because the z-score is higher relative to that class's spread.",
     "Class 2, because the larger SD means more students scored 90.",
     "Neither class — a score of 90 is equally unusual in both because the means are equal.",
     "Class 1, because a smaller SD means more students scored exactly 80.",
     "A",
     "z-score for Class 1: (90−80)/5 = 2.0. z-score for Class 2: (90−80)/15 = 0.67. A z-score of 2.0 is more unusual than 0.67. A score of 90 is 2 SDs above the mean in Class 1, making it more remarkable there than in Class 2 where it is less than 1 SD above the mean.",
     "z_scores"),

    # =========================================================================
    # TWO-VARIABLE DATA — 6 questions (F×2, U×2, A×1, R×1)
    # =========================================================================

    # TV-1 F diff=1
    ("ap_stats", "two_var_data", "F", 1,
     "A correlation coefficient of r = −0.92 between hours of TV watched and GPA indicates:",
     "multiple_choice",
     "Watching TV causes lower GPA.",
     "There is a strong negative linear relationship between hours of TV watched and GPA.",
     "There is a weak negative relationship between the two variables.",
     "GPA decreases by 0.92 for each additional hour of TV watched.",
     "B",
     "r = −0.92 is close to −1, indicating a strong negative linear association. Correlation does not imply causation, so we cannot say TV watching causes lower GPA. The value of r is not a slope — it measures the strength and direction of the linear relationship.",
     "correlation"),

    # TV-2 F diff=2
    ("ap_stats", "two_var_data", "F", 2,
     "The least-squares regression line (LSRL) for predicting weight (lbs) from height (in) is: ŷ = −100 + 5x. What is the predicted weight for a person who is 65 inches tall?",
     "multiple_choice",
     "225 lbs", "235 lbs", "250 lbs", "325 lbs",
     "A",
     "ŷ = −100 + 5(65) = −100 + 325 = 225 lbs. Substitute x = 65 into the regression equation.",
     "lsrl"),

    # TV-3 U diff=2
    ("ap_stats", "two_var_data", "U", 2,
     "In a regression analysis, r² = 0.81. Which statement correctly interprets this value?",
     "multiple_choice",
     "The correlation between the variables is 0.81.",
     "81% of the variation in the response variable is explained by the linear relationship with the explanatory variable.",
     "The regression line predicts the response variable with 81% accuracy.",
     "There is a 0.81 probability that the regression line is correct.",
     "B",
     "r² (the coefficient of determination) represents the proportion of variability in the response variable that is explained by the linear regression model. r² = 0.81 means 81% of the variation in y is accounted for by the linear relationship with x. Note: r = ±0.9, not 0.81.",
     "r_squared"),

    # TV-4 U diff=3
    ("ap_stats", "two_var_data", "U", 3,
     "A residual plot for a linear regression shows a curved (U-shaped) pattern. What does this indicate?",
     "multiple_choice",
     "The linear model is a good fit for the data.",
     "The data has high variability that cannot be modeled.",
     "A linear model is not appropriate; a nonlinear model may be a better fit.",
     "The residuals are normally distributed, confirming the model is valid.",
     "C",
     "A residual plot should show random scatter around zero if the linear model is appropriate. A U-shaped or curved pattern indicates a systematic trend that the linear model is not capturing, suggesting that a nonlinear (e.g., quadratic) model may be more appropriate.",
     "residuals"),

    # TV-5 A diff=3
    ("ap_stats", "two_var_data", "A", 3,
     "A study finds a correlation of r = 0.95 between ice cream sales and drowning rates. A reporter concludes that eating ice cream causes drowning. What is the most appropriate statistical response?",
     "multiple_choice",
     "The reporter is correct because r > 0.9 confirms causation.",
     "Correlation does not imply causation; hot weather is likely a lurking variable that increases both ice cream sales and swimming (and thus drowning).",
     "The correlation should be recalculated after removing outliers to confirm the causal link.",
     "Since r is positive, ice cream protects against drowning.",
     "B",
     "This is a classic example of confounding/lurking variables. High temperature (summer) causes both increased ice cream sales and increased swimming activity (which raises drowning risk). Correlation measures association, not causation. A lurking variable (temperature) drives both variables simultaneously.",
     "correlation"),

    # TV-6 R diff=4
    ("ap_stats", "two_var_data", "R", 4,
     "The LSRL for predicting salary (in thousands) from years of experience is ŷ = 40 + 3.2x. A person with 10 years of experience earns $78,000. What is the residual?",
     "multiple_choice",
     "−$6,000", "+$6,000", "+$4,000", "+$38,000",
     "B",
     "Predicted: ŷ = 40 + 3.2(10) = 40 + 32 = 72 (thousands) = $72,000. Residual = Actual − Predicted = 78 − 72 = +6 (thousands) = +$6,000. A positive residual means the actual salary exceeded the model's prediction.",
     "residuals"),

    # =========================================================================
    # COLLECTING DATA — 10 questions (F×3, U×3, A×2, R×2)
    # =========================================================================

    # CD-1 F diff=1
    ("ap_stats", "collecting_data", "F", 1,
     "A researcher randomly assigns 50 subjects to receive a new drug and 50 subjects to receive a placebo. This is an example of:",
     "multiple_choice",
     "An observational study",
     "A survey",
     "A randomized experiment",
     "A census",
     "C",
     "A randomized experiment involves the researcher actively assigning subjects to treatment conditions (new drug vs placebo) using randomization. Observational studies only observe subjects without imposing treatments.",
     "experiments_vs_observational"),

    # CD-2 F diff=1
    ("ap_stats", "collecting_data", "F", 1,
     "Which sampling method divides a population into groups and randomly selects from each group proportionally?",
     "multiple_choice",
     "Simple random sample (SRS)",
     "Stratified random sample",
     "Cluster sample",
     "Convenience sample",
     "B",
     "Stratified random sampling divides the population into homogeneous subgroups (strata) and randomly samples from each stratum. This ensures representation from all groups and often reduces variability compared to an SRS.",
     "sampling_methods"),

    # CD-3 F diff=2
    ("ap_stats", "collecting_data", "F", 2,
     "A pollster surveys shoppers at a mall on a Tuesday afternoon. What type of bias is most likely present?",
     "multiple_choice",
     "Response bias",
     "Nonresponse bias",
     "Voluntary response bias",
     "Undercoverage bias",
     "D",
     "Mall shoppers on a Tuesday afternoon are not representative of the general population (e.g., employed people are underrepresented). This is undercoverage — certain segments of the population have little or no chance of being selected.",
     "bias"),

    # CD-4 U diff=2
    ("ap_stats", "collecting_data", "U", 2,
     "In a double-blind experiment, which of the following is true?",
     "multiple_choice",
     "Neither the subjects nor the researchers evaluating outcomes know who received which treatment.",
     "Only the subjects do not know which treatment they received.",
     "Only the researchers do not know which treatment was administered.",
     "The experiment has two control groups and one treatment group.",
     "A",
     "In a double-blind experiment, both the subjects and the evaluators (researchers) are unaware of treatment assignments. This eliminates placebo effects (subject side) and evaluator bias (researcher side), making results more reliable.",
     "experiments_vs_observational"),

    # CD-5 U diff=2
    ("ap_stats", "collecting_data", "U", 2,
     "A researcher wants to study whether a new fertilizer increases crop yield. She divides a field into plots, randomly assigns half to receive the fertilizer, and measures yield. She cannot draw a cause-and-effect conclusion because:",
     "multiple_choice",
     "She did not use blocking.",
     "She used a field instead of a greenhouse.",
     "This is an observational study, not an experiment.",
     "Actually, she CAN draw a cause-and-effect conclusion because of random assignment.",
     "D",
     "Random assignment of subjects to treatments is the key feature that allows cause-and-effect conclusions in an experiment. Because she randomly assigned plots to fertilizer vs no fertilizer, any differences in yield can be attributed to the fertilizer. She CAN make a causal conclusion.",
     "experiments_vs_observational"),

    # CD-6 U diff=3
    ("ap_stats", "collecting_data", "U", 3,
     "A study mails surveys to 500 randomly selected households. Only 120 respond. The researchers use only the 120 responses. What concern does this raise?",
     "multiple_choice",
     "Undercoverage, because not all households were contacted.",
     "Nonresponse bias, because those who respond may differ systematically from those who do not.",
     "Response bias, because people lie on surveys.",
     "Sampling variability, which is unavoidable in all surveys.",
     "B",
     "Nonresponse bias occurs when those who do not respond differ systematically from those who do. With only 24% response rate (120/500), the remaining 76% who did not respond may have different opinions or characteristics, making the results potentially unrepresentative.",
     "bias"),

    # CD-7 A diff=3
    ("ap_stats", "collecting_data", "A", 3,
     "A school wants to survey students about cafeteria food. They randomly select 3 homeroom classes and survey every student in those classes. This is a:",
     "multiple_choice",
     "Stratified random sample",
     "Simple random sample",
     "Cluster sample",
     "Systematic sample",
     "C",
     "Cluster sampling selects entire naturally occurring groups (clusters — here, homeroom classes) at random and surveys all members. Stratified sampling would randomly select some students from each homeroom; cluster sampling selects entire groups. This is a cluster sample.",
     "sampling_methods"),

    # CD-8 A diff=3
    ("ap_stats", "collecting_data", "A", 3,
     "A researcher studying the effect of sleep on test performance cannot randomly assign subjects to sleep amounts because students control their own sleep. The researcher instead compares students who naturally sleep 6 hours vs 8 hours. Which conclusion is most appropriate?",
     "multiple_choice",
     "Students who sleep 8 hours perform better because of the extra sleep.",
     "Sleep causes higher test scores since the association was observed in data.",
     "There is an association between sleep and test scores, but confounding variables prevent a causal conclusion.",
     "No conclusion can be drawn because the sample size is unknown.",
     "C",
     "Without random assignment, this is an observational study. Confounding variables (e.g., motivation, course load, stress) could explain both sleep patterns and test scores. We can identify association but cannot establish causation without an experiment.",
     "experiments_vs_observational"),

    # CD-9 R diff=4
    ("ap_stats", "collecting_data", "R", 4,
     "To study voter preferences, a researcher uses systematic sampling: she selects every 10th voter from a registration list. A critic says this could be biased if the list has a periodic pattern. The critic is:",
     "multiple_choice",
     "Wrong — systematic sampling always produces unbiased estimates.",
     "Correct — if the list repeats a pattern every 10 entries (e.g., every 10th person is from the same neighborhood), the sample could be systematically unrepresentative.",
     "Correct — systematic sampling is equivalent to convenience sampling and is always biased.",
     "Wrong — periodic patterns in lists are mathematically impossible.",
     "B",
     "Systematic sampling can introduce bias if there is a periodic structure in the list that aligns with the sampling interval. For example, if every 10th entry coincides with a particular characteristic (address pattern, alphabetical clustering), the sample may over- or under-represent certain groups. The critic's concern is statistically valid.",
     "sampling_methods"),

    # CD-10 R diff=5
    ("ap_stats", "collecting_data", "R", 5,
     "A randomized block design is used in an experiment. What is the primary purpose of blocking?",
     "multiple_choice",
     "To increase the number of treatment groups.",
     "To reduce the effect of a known source of variability, making it easier to detect treatment differences.",
     "To eliminate the need for a control group.",
     "To ensure that the experiment is double-blind.",
     "B",
     "Blocking groups experimental units that are similar with respect to a known variable (the blocking variable), then randomly assigns treatments within each block. This reduces variability within treatment groups, making it easier to detect real treatment effects. It controls for the blocking variable's influence — similar to stratified sampling but in an experimental design.",
     "randomization"),

    # =========================================================================
    # PROBABILITY — 12 questions (F×3, U×3, A×3, R×3)
    # =========================================================================

    # PR-1 F diff=1
    ("ap_stats", "probability", "F", 1,
     "A fair six-sided die is rolled. What is the probability of rolling a number greater than 4?",
     "multiple_choice",
     "1/6", "1/3", "1/2", "2/3",
     "B",
     "Numbers greater than 4 on a standard die: {5, 6} — two outcomes. P(>4) = 2/6 = 1/3.",
     "probability_rules"),

    # PR-2 F diff=2
    ("ap_stats", "probability", "F", 2,
     "Events A and B are independent with P(A) = 0.4 and P(B) = 0.5. What is P(A and B)?",
     "multiple_choice",
     "0.10", "0.20", "0.45", "0.90",
     "B",
     "For independent events, P(A ∩ B) = P(A) × P(B) = 0.4 × 0.5 = 0.20. Independence means the occurrence of one event does not affect the probability of the other.",
     "independence"),

    # PR-3 F diff=2
    ("ap_stats", "probability", "F", 2,
     "P(A) = 0.6, P(B) = 0.3, and A and B are mutually exclusive. What is P(A or B)?",
     "multiple_choice",
     "0.18", "0.30", "0.72", "0.90",
     "D",
     "Mutually exclusive events cannot occur together, so P(A ∩ B) = 0. Addition rule: P(A ∪ B) = P(A) + P(B) = 0.6 + 0.3 = 0.9.",
     "probability_rules"),

    # PR-4 U diff=2
    ("ap_stats", "probability", "U", 2,
     "A bag contains 5 red and 3 blue marbles. If two marbles are drawn without replacement, what is the probability that both are red?",
     "multiple_choice",
     "5/16", "5/14", "25/64", "10/56",
     "B",
     "P(both red) = P(1st red) × P(2nd red | 1st red) = (5/8) × (4/7) = 20/56 = 5/14. After drawing one red marble, 4 red and 3 blue remain (7 total).",
     "conditional_probability"),

    # PR-5 U diff=3
    ("ap_stats", "probability", "U", 3,
     "The probability that a student passes math is 0.7. The probability that a student passes both math and science is 0.5. Given that a student passes math, what is the probability they also pass science?",
     "multiple_choice",
     "0.35", "0.50", "0.71", "0.75",
     "C",
     "P(Science | Math) = P(Math ∩ Science) / P(Math) = 0.5 / 0.7 ≈ 0.714 ≈ 0.71. This is the conditional probability formula: P(B|A) = P(A ∩ B) / P(A).",
     "conditional_probability"),

    # PR-6 U diff=3
    ("ap_stats", "probability", "U", 3,
     "A binomial setting requires four conditions (BINS). Which of the following is NOT one of those conditions?",
     "multiple_choice",
     "Binary outcomes (success or failure)",
     "Independent trials",
     "Normal distribution of outcomes",
     "Fixed number of trials (n)",
     "C",
     "The four BINS conditions for a binomial setting are: Binary outcomes, Independent trials, fixed Number of trials (n), and same probability of Success (p) for each trial. A normal distribution of outcomes is NOT required for a binomial setting (though the sampling distribution of the count approximates normal for large n).",
     "binomial_distribution"),

    # PR-7 A diff=3
    ("ap_stats", "probability", "A", 3,
     "A basketball player makes 70% of free throws. She shoots 10 free throws in a game. Using the binomial model, what is the expected number of free throws she will make?",
     "multiple_choice",
     "5", "6", "7", "8",
     "C",
     "For a binomial distribution, the expected value (mean) = np = 10 × 0.70 = 7. She is expected to make 7 out of 10 free throws.",
     "binomial_distribution"),

    # PR-8 A diff=3
    ("ap_stats", "probability", "A", 3,
     "A geometric distribution models the number of trials until the first success. If the probability of success on any trial is 0.25, what is the expected number of trials until the first success?",
     "multiple_choice",
     "0.25", "2", "4", "25",
     "C",
     "For a geometric distribution, the expected number of trials until the first success = 1/p = 1/0.25 = 4. On average, you'd expect 4 trials before getting the first success.",
     "geometric_distribution"),

    # PR-9 A diff=4
    ("ap_stats", "probability", "A", 4,
     "A student argues: 'I've flipped heads 5 times in a row, so tails is due — it's more likely on the next flip.' This reasoning illustrates:",
     "multiple_choice",
     "The law of large numbers applied correctly.",
     "The gambler's fallacy — independent events have no memory.",
     "Conditional probability applied correctly.",
     "The central limit theorem in action.",
     "B",
     "Each flip of a fair coin is independent. The probability of tails on the next flip is always 0.5, regardless of previous outcomes. The gambler's fallacy is the mistaken belief that past independent events influence future ones. The law of large numbers applies over very many trials, not predicting individual outcomes.",
     "independence"),

    # PR-10 R diff=4
    ("ap_stats", "probability", "R", 4,
     "A test for a disease has 99% sensitivity (P(positive | disease) = 0.99) and 95% specificity (P(negative | no disease) = 0.95). The disease prevalence is 1%. A patient tests positive. Which statement is most accurate?",
     "multiple_choice",
     "There is a 99% chance the patient has the disease.",
     "There is a 95% chance the patient has the disease.",
     "The positive predictive value is much lower than 99% because the disease is rare.",
     "The test result is meaningless because no test is perfect.",
     "C",
     "With rare diseases (1% prevalence), even very accurate tests have lower positive predictive value due to false positives. Using Bayes' theorem: true positives ≈ 0.01×0.99 = 0.0099; false positives ≈ 0.99×0.05 = 0.0495. PPV = 0.0099/(0.0099+0.0495) ≈ 16.6%. Most positives are false positives. Low prevalence dramatically reduces PPV.",
     "conditional_probability"),

    # PR-11 R diff=4
    ("ap_stats", "probability", "R", 4,
     "If P(A) = 0.5, P(B) = 0.4, and P(A and B) = 0.2, are events A and B independent?",
     "multiple_choice",
     "Yes, because P(A and B) = P(A) × P(B) = 0.5 × 0.4 = 0.2.",
     "No, because P(A and B) should equal P(A) + P(B) for independent events.",
     "Yes, because A and B are not mutually exclusive.",
     "No, because the events overlap.",
     "A",
     "Two events are independent if P(A ∩ B) = P(A) × P(B). Here: P(A) × P(B) = 0.5 × 0.4 = 0.20, which equals P(A and B) = 0.20. Therefore A and B are independent. Note: independence and mutual exclusivity are different concepts — mutually exclusive events (except trivial cases) are NOT independent.",
     "independence"),

    # PR-12 R diff=5
    ("ap_stats", "probability", "R", 5,
     "The standard deviation of a binomial random variable with n = 100 and p = 0.3 is:",
     "multiple_choice",
     "√21 ≈ 4.58", "√30 ≈ 5.48", "√(100 × 0.3) = 5.48", "√(0.3 × 0.7) ≈ 0.46",
     "A",
     "SD of a binomial = √(np(1−p)) = √(100 × 0.3 × 0.7) = √21 ≈ 4.58. Note: np = 30 is the mean, not the standard deviation. √30 is a common distractor from confusing mean and variance.",
     "binomial_distribution"),

    # =========================================================================
    # SAMPLING DISTRIBUTIONS — 8 questions (F×2, U×2, A×2, R×2)
    # =========================================================================

    # SD-1 F diff=1
    ("ap_stats", "sampling_dist", "F", 1,
     "The Central Limit Theorem (CLT) states that for large sample sizes, the sampling distribution of the sample mean is:",
     "multiple_choice",
     "Identical to the population distribution.",
     "Approximately normal, regardless of the shape of the population distribution.",
     "Skewed in the same direction as the population.",
     "Always exactly normal for any sample size.",
     "B",
     "The CLT states that for sufficiently large n (generally n ≥ 30 as a rule of thumb), the sampling distribution of x̄ is approximately normal, regardless of the population's shape. This is one of the most powerful results in statistics.",
     "clt"),

    # SD-2 F diff=2
    ("ap_stats", "sampling_dist", "F", 2,
     "A population has mean μ = 50 and standard deviation σ = 10. What is the standard error of the sample mean for samples of size n = 25?",
     "multiple_choice",
     "0.4", "2", "10", "50",
     "B",
     "Standard error (SE) of the sample mean = σ/√n = 10/√25 = 10/5 = 2. The standard error measures the typical distance between the sample mean and the population mean across repeated samples.",
     "standard_error"),

    # SD-3 U diff=2
    ("ap_stats", "sampling_dist", "U", 2,
     "As sample size increases, the standard error of the sample mean:",
     "multiple_choice",
     "Increases proportionally to n.",
     "Remains constant regardless of n.",
     "Decreases — larger samples produce more precise estimates.",
     "Increases then decreases at n = 30.",
     "C",
     "SE = σ/√n. As n increases, √n increases, so SE decreases. Larger samples reduce sampling variability and produce more precise estimates of the population mean. This is why larger samples are better.",
     "standard_error"),

    # SD-4 U diff=3
    ("ap_stats", "sampling_dist", "U", 3,
     "A population has mean 80 and standard deviation 16. Samples of size n = 64 are taken. What is the probability that a sample mean exceeds 82?",
     "multiple_choice",
     "Approximately 0.16", "Approximately 0.84", "Approximately 0.025", "Approximately 0.975",
     "A",
     "SE = 16/√64 = 2. z = (82 − 80)/2 = 1.0. P(x̄ > 82) = P(z > 1) ≈ 1 − 0.8413 = 0.1587 ≈ 0.16. Using the standard normal table, about 16% of samples of size 64 will have a mean above 82.",
     "clt"),

    # SD-5 A diff=3
    ("ap_stats", "sampling_dist", "A", 3,
     "A sampling distribution of p̂ (sample proportion) is approximately normal when:",
     "multiple_choice",
     "n > 30",
     "np ≥ 10 and n(1 − p) ≥ 10",
     "p > 0.5",
     "The population size exceeds 1000",
     "B",
     "The sampling distribution of p̂ is approximately normal when both np ≥ 10 and n(1−p) ≥ 10 (the Large Counts condition). This ensures there are enough expected successes and failures. The condition n > 30 applies to sample means, not proportions.",
     "sampling_dist_proportions"),

    # SD-6 A diff=3
    ("ap_stats", "sampling_dist", "A", 3,
     "The mean of the sampling distribution of p̂ is:",
     "multiple_choice",
     "p/n", "p̂", "p", "√(p(1−p)/n)",
     "C",
     "The sampling distribution of p̂ is centered at the true population proportion p. That is, E(p̂) = p, making p̂ an unbiased estimator of p. The standard deviation of the sampling distribution is √(p(1−p)/n), not the mean.",
     "sampling_dist_proportions"),

    # SD-7 R diff=4
    ("ap_stats", "sampling_dist", "R", 4,
     "A student says: 'The Central Limit Theorem says the sample data will be normal if n is large.' What is wrong with this statement?",
     "multiple_choice",
     "Nothing — the CLT applies to individual data values for large n.",
     "The CLT applies to the sampling distribution of the sample mean, not to individual data values in the sample.",
     "The CLT only applies when the population is already normal.",
     "The CLT requires n ≥ 100, not just 'large n.'",
     "B",
     "This is a critical distinction. The CLT guarantees that the sampling distribution of the sample mean (x̄) becomes approximately normal for large n, not that the individual data values become normal. The sample data retains the shape of the population distribution regardless of sample size.",
     "clt"),

    # SD-8 R diff=5
    ("ap_stats", "sampling_dist", "R", 5,
     "Two researchers each take samples from the same population (μ = 100, σ = 20). Researcher A uses n = 25; Researcher B uses n = 100. Which statement about their sampling distributions is correct?",
     "multiple_choice",
     "Both have the same standard error of 20.",
     "Researcher A's sampling distribution has SE = 4; Researcher B's has SE = 2.",
     "Researcher B's sampling distribution has a higher mean because of the larger sample.",
     "Researcher A's estimates will be more precise because smaller samples have less bias.",
     "B",
     "SE_A = 20/√25 = 4; SE_B = 20/√100 = 2. Both sampling distributions are centered at μ = 100 (unbiased). Researcher B's estimates are more precise (lower SE). Sample size affects precision, not bias (both estimators are unbiased). Larger samples produce narrower sampling distributions.",
     "standard_error"),

    # =========================================================================
    # INFERENCE — PROPORTIONS — 12 questions (F×3, U×3, A×3, R×3)
    # =========================================================================

    # IP-1 F diff=1
    ("ap_stats", "inference_proportions", "F", 1,
     "A 95% confidence interval for a population proportion is (0.42, 0.58). What is the point estimate (p̂)?",
     "multiple_choice",
     "0.42", "0.50", "0.58", "0.95",
     "B",
     "The point estimate is the midpoint of the confidence interval: (0.42 + 0.58)/2 = 1.00/2 = 0.50. The margin of error is (0.58 − 0.42)/2 = 0.08.",
     "confidence_intervals"),

    # IP-2 F diff=2
    ("ap_stats", "inference_proportions", "F", 2,
     "A 95% confidence interval for the proportion of adults who exercise regularly is (0.38, 0.52). Which interpretation is correct?",
     "multiple_choice",
     "There is a 95% probability that the true proportion is between 0.38 and 0.52.",
     "95% of adults exercise between 38% and 52% of the time.",
     "We are 95% confident that the interval (0.38, 0.52) captures the true population proportion.",
     "If we repeated the study, 95% of the data would fall between 0.38 and 0.52.",
     "C",
     "The correct interpretation of a confidence interval refers to the method's long-run success rate: 95% of intervals constructed this way will capture the true parameter. The true proportion is fixed (not random), so it is incorrect to say 'there is a 95% probability it falls in this interval' — that's a common misconception.",
     "confidence_intervals"),

    # IP-3 F diff=2
    ("ap_stats", "inference_proportions", "F", 2,
     "Which of the following increases the width of a confidence interval for a proportion, all else equal?",
     "multiple_choice",
     "Increasing the sample size",
     "Decreasing the confidence level from 95% to 90%",
     "Increasing the confidence level from 95% to 99%",
     "Using a value of p̂ closer to 0 or 1",
     "C",
     "A higher confidence level requires a wider interval to provide greater certainty of capturing the parameter. Increasing n narrows the interval. A p̂ closer to 0 or 1 (not 0.5) actually decreases the margin of error because p̂(1−p̂) is maximized at p̂ = 0.5.",
     "confidence_intervals"),

    # IP-4 U diff=2
    ("ap_stats", "inference_proportions", "U", 2,
     "The null hypothesis in a one-proportion z-test is H₀: p = 0.5. The alternative hypothesis is Hₐ: p > 0.5. This is a:",
     "multiple_choice",
     "Two-sided test",
     "Left-tailed test",
     "Right-tailed test",
     "Chi-square test",
     "C",
     "The alternative hypothesis Hₐ: p > 0.5 specifies a direction (greater than), making this a right-tailed (one-sided) test. The p-value is the area to the right of the test statistic in the standard normal distribution.",
     "hypothesis_testing"),

    # IP-5 U diff=3
    ("ap_stats", "inference_proportions", "U", 3,
     "A p-value of 0.03 is obtained from a hypothesis test. Which statement correctly interprets this p-value?",
     "multiple_choice",
     "There is a 3% probability that the null hypothesis is true.",
     "There is a 97% probability that the alternative hypothesis is true.",
     "If the null hypothesis were true, there is a 3% probability of observing a test statistic as extreme as (or more extreme than) the one observed.",
     "The null hypothesis should be accepted because p < 0.05.",
     "C",
     "The p-value is the probability of obtaining results as extreme as (or more extreme than) those observed, assuming H₀ is true. It does NOT give the probability that H₀ is true or false. A small p-value (typically < 0.05) provides evidence against H₀ — we reject H₀ — but we never 'accept' H₀.",
     "p_values"),

    # IP-6 U diff=3
    ("ap_stats", "inference_proportions", "U", 3,
     "Conditions for a one-proportion z-interval include: the sample is random, np̂ ≥ 10, and n(1−p̂) ≥ 10. In a sample of 40 people, 6 report a side effect (p̂ = 0.15). Is the Normal condition met?",
     "multiple_choice",
     "Yes, because n = 40 > 30.",
     "Yes, because p̂ = 0.15 < 0.5.",
     "No, because n(1−p̂) = 40 × 0.85 = 34, which is ≥ 10, but np̂ = 40 × 0.15 = 6, which is < 10.",
     "No, because p̂ must be at least 0.5 for the normal approximation.",
     "C",
     "Both np̂ ≥ 10 AND n(1−p̂) ≥ 10 must be satisfied. Here np̂ = 6 < 10, so the Large Counts condition is NOT met. The normal approximation may not be appropriate. n > 30 is the condition for sample means, not proportions.",
     "conditions_inference"),

    # IP-7 A diff=3
    ("ap_stats", "inference_proportions", "A", 3,
     "A researcher tests H₀: p = 0.40 vs Hₐ: p ≠ 0.40. The test statistic is z = 2.1. The p-value is approximately 0.036. At α = 0.05, the conclusion is:",
     "multiple_choice",
     "Fail to reject H₀; there is insufficient evidence that p ≠ 0.40.",
     "Reject H₀; there is sufficient evidence that p ≠ 0.40.",
     "Accept H₀; the true proportion is 0.40.",
     "Reject Hₐ; the proportion is significantly different from 0.40.",
     "B",
     "Since p-value (0.036) < α (0.05), we reject H₀. There is sufficient evidence that the true proportion differs from 0.40. We never 'accept' H₀ — we either reject or fail to reject. We also never reject Hₐ (the alternative).",
     "hypothesis_testing"),

    # IP-8 A diff=4
    ("ap_stats", "inference_proportions", "A", 4,
     "A 99% confidence interval for a proportion yields (0.31, 0.49). A student concludes: 'Since 0.40 is in the interval, we have proven that p = 0.40.' What is wrong with this conclusion?",
     "multiple_choice",
     "Nothing — if 0.40 is in the interval, it is proven to be the true proportion.",
     "The interval proves all values between 0.31 and 0.49 are equally likely to be the true proportion.",
     "A confidence interval does not prove any specific value; it gives a plausible range. Many values are in the interval, none are 'proven.'",
     "The student should have used a hypothesis test, not a confidence interval.",
     "C",
     "A confidence interval provides a range of plausible values for the parameter, not proof of any particular value. All values from 0.31 to 0.49 are plausible — not just 0.40. Saying a specific value is 'proven' misunderstands inference. A hypothesis test of H₀: p = 0.40 would fail to reject (since 0.40 is in the CI), but that's not the same as proof.",
     "confidence_intervals"),

    # IP-9 A diff=4
    ("ap_stats", "inference_proportions", "A", 4,
     "A Type I error in hypothesis testing is:",
     "multiple_choice",
     "Failing to reject H₀ when it is false.",
     "Rejecting H₀ when it is actually true.",
     "Accepting Hₐ when the sample is too small.",
     "Computing a p-value incorrectly.",
     "B",
     "A Type I error (false positive) occurs when H₀ is rejected even though it is true. The probability of a Type I error equals the significance level α. A Type II error (false negative) occurs when H₀ is false but we fail to reject it. Power = 1 − P(Type II error).",
     "hypothesis_testing"),

    # IP-10 R diff=4
    ("ap_stats", "inference_proportions", "R", 4,
     "A researcher increases the significance level from α = 0.01 to α = 0.05. What is the effect on Type I and Type II error rates?",
     "multiple_choice",
     "Type I error rate decreases; Type II error rate increases.",
     "Type I error rate increases; Type II error rate decreases.",
     "Both Type I and Type II error rates decrease.",
     "Neither error rate changes because α only affects the critical value.",
     "B",
     "Increasing α raises the threshold for rejection, making it easier to reject H₀. This increases the Type I error rate (more false positives) but decreases the Type II error rate (fewer false negatives), because the test is more likely to detect real effects. There is an inherent tradeoff between Type I and Type II errors.",
     "hypothesis_testing"),

    # IP-11 R diff=4
    ("ap_stats", "inference_proportions", "R", 4,
     "A study finds a statistically significant result (p = 0.001). A student concludes: 'This result is practically important.' Is this conclusion justified?",
     "multiple_choice",
     "Yes — a very small p-value always indicates a large, meaningful effect.",
     "Not necessarily — statistical significance indicates the result is unlikely due to chance, but does not guarantee practical importance. Effect size matters.",
     "Yes — p < 0.05 is the definition of practical significance.",
     "No — p = 0.001 is too small to be meaningful.",
     "B",
     "Statistical significance and practical significance are different. With very large samples, even tiny, practically irrelevant differences can be statistically significant. A p-value measures evidence against H₀, not the size or importance of an effect. Effect size (like the actual difference in proportions) and context determine practical importance.",
     "p_values"),

    # IP-12 R diff=5
    ("ap_stats", "inference_proportions", "R", 5,
     "A two-proportion z-test is performed comparing p₁ and p₂. The test statistic uses a pooled proportion p̂_c. Why is the pooled proportion used?",
     "multiple_choice",
     "Because p̂₁ and p̂₂ are always unreliable individually.",
     "Because under H₀: p₁ = p₂, we assume both samples come from populations with the same proportion, so we use all data to estimate that common proportion.",
     "Because the pooled proportion has a smaller standard error than either individual estimate.",
     "Because the CLT requires pooling for two-proportion tests.",
     "B",
     "Under the null hypothesis H₀: p₁ = p₂, we assume both groups have the same true proportion. To estimate this common proportion as accurately as possible, we combine (pool) data from both samples: p̂_c = (x₁ + x₂)/(n₁ + n₂). This gives the best estimate of the assumed-equal common proportion under H₀.",
     "hypothesis_testing"),

    # =========================================================================
    # INFERENCE — MEANS — 12 questions (F×3, U×3, A×3, R×3)
    # =========================================================================

    # IM-1 F diff=1
    ("ap_stats", "inference_means", "F", 1,
     "Why is a t-distribution used instead of a z-distribution when making inferences about a population mean?",
     "multiple_choice",
     "Because the t-distribution is always more conservative.",
     "Because the population standard deviation σ is usually unknown and must be estimated by the sample standard deviation s.",
     "Because the t-distribution is used only when n < 30.",
     "Because the z-distribution requires the sample to be normally distributed.",
     "B",
     "When σ is unknown (the typical case), we estimate it with s (sample standard deviation). This introduces additional uncertainty, and the t-distribution (with heavier tails than z) accounts for this extra variability. As n increases, the t-distribution approaches the z-distribution.",
     "t_distributions"),

    # IM-2 F diff=2
    ("ap_stats", "inference_means", "F", 2,
     "A one-sample t-test has n = 20. How many degrees of freedom does the t-distribution have?",
     "multiple_choice",
     "18", "19", "20", "21",
     "B",
     "For a one-sample t-test, degrees of freedom = n − 1 = 20 − 1 = 19. Degrees of freedom measure how much information is used to estimate the standard deviation. One degree of freedom is 'used' to estimate the mean.",
     "t_distributions"),

    # IM-3 F diff=2
    ("ap_stats", "inference_means", "F", 2,
     "A 95% confidence interval for the mean is (42, 58). Which statement is the correct interpretation?",
     "multiple_choice",
     "95% of sample means fall between 42 and 58.",
     "There is a 95% chance the population mean is between 42 and 58.",
     "We are 95% confident this interval captures the true population mean.",
     "The population mean is between 42 and 58 with certainty.",
     "C",
     "The correct interpretation references the confidence in the method, not a probability about the fixed (but unknown) parameter. Once an interval is computed, it either does or does not contain the true mean — there's no probability about that. 95% confidence means 95% of such intervals constructed the same way would capture the true mean.",
     "confidence_intervals"),

    # IM-4 U diff=2
    ("ap_stats", "inference_means", "U", 2,
     "When is a paired t-test more appropriate than a two-sample t-test?",
     "multiple_choice",
     "When the two groups have equal variances.",
     "When each measurement in one group is naturally paired with a measurement in the other group (e.g., before-after, matched pairs).",
     "When the sample sizes are equal.",
     "When the data are skewed.",
     "B",
     "A paired t-test is used when data consists of matched pairs — each subject measured twice (before/after) or matched subjects in two conditions. Pairing removes individual-to-individual variability, making the test more powerful. A two-sample t-test is used for independent groups.",
     "paired_vs_two_sample"),

    # IM-5 U diff=3
    ("ap_stats", "inference_means", "U", 3,
     "A researcher tests H₀: μ = 50 vs Hₐ: μ < 50 with n = 16, x̄ = 47, s = 8. What is the t-statistic?",
     "multiple_choice",
     "−1.50", "−1.00", "1.50", "3.00",
     "A",
     "t = (x̄ − μ₀) / (s/√n) = (47 − 50) / (8/√16) = −3 / (8/4) = −3/2 = −1.50. The negative sign indicates the sample mean is below the hypothesized value.",
     "t_tests"),

    # IM-6 U diff=3
    ("ap_stats", "inference_means", "U", 3,
     "The conditions for a one-sample t-test include: random sample, and the population is normal OR n is large. What is the guideline for 'large enough' n when the population is not known to be normal?",
     "multiple_choice",
     "n ≥ 10", "n ≥ 20", "n ≥ 30", "n ≥ 50",
     "C",
     "The general guideline is n ≥ 30 for the CLT to make the sampling distribution of x̄ approximately normal, even if the population is not normal. For smaller n, we require the population to be approximately normal (check with a boxplot or normal probability plot). If n ≥ 30 and there are no extreme outliers, the t-procedures are robust.",
     "conditions_inference"),

    # IM-7 A diff=3
    ("ap_stats", "inference_means", "A", 3,
     "A paired t-test is conducted on before/after blood pressure measurements for 15 patients. The mean of the differences is d̄ = −5.2 mmHg and the standard deviation of differences is s_d = 4.0. The t-statistic is:",
     "multiple_choice",
     "−1.30", "−3.25", "−5.03", "−13.00",
     "C",
     "t = d̄ / (s_d / √n) = −5.2 / (4.0 / √15) = −5.2 / (4.0/3.873) = −5.2 / 1.033 ≈ −5.03. With df = 14, this very negative t-statistic provides strong evidence that blood pressure decreased.",
     "paired_vs_two_sample"),

    # IM-8 A diff=4
    ("ap_stats", "inference_means", "A", 4,
     "A two-sample t-test compares the mean exam scores of two classes. Class A: n=25, x̄=78, s=10. Class B: n=30, x̄=82, s=12. What do we conclude if the p-value is 0.08 and α=0.05?",
     "multiple_choice",
     "Reject H₀; there is significant evidence the means differ.",
     "Fail to reject H₀; there is insufficient evidence at α=0.05 to conclude the means differ.",
     "Accept H₀; the means are equal.",
     "The test is invalid because the sample sizes differ.",
     "B",
     "Since p-value (0.08) > α (0.05), we fail to reject H₀. There is insufficient statistical evidence at the 5% significance level to conclude the class means differ. 'Fail to reject' is not the same as 'accept H₀' — we simply don't have enough evidence to reject it. Unequal sample sizes are fine for a two-sample t-test.",
     "t_tests"),

    # IM-9 A diff=4
    ("ap_stats", "inference_means", "A", 4,
     "To construct a valid 95% t-confidence interval for a population mean with n = 12, which assumption is most critical?",
     "multiple_choice",
     "The population standard deviation is known.",
     "The sample size is at least 30.",
     "The population distribution is approximately normal (or the data show no severe skew or outliers).",
     "The confidence level must be at least 90%.",
     "C",
     "For small samples (n < 30), t-procedures require the population to be approximately normal. With n = 12, we should examine a boxplot or normal probability plot for strong skew or outliers. If the distribution appears roughly symmetric without outliers, t-procedures are appropriate. σ being unknown is why we use t (not z).",
     "conditions_inference"),

    # IM-10 R diff=4
    ("ap_stats", "inference_means", "R", 4,
     "A researcher fails to reject H₀: μ = 100 at α = 0.05. She concludes: 'The population mean is 100.' What error might she be making?",
     "multiple_choice",
     "She is making a Type I error by not rejecting H₀.",
     "She is incorrectly interpreting 'fail to reject' as 'accept' — failing to reject H₀ does not prove it is true.",
     "She should have used α = 0.01 instead of α = 0.05.",
     "No error — failing to reject H₀ always means H₀ is true.",
     "B",
     "Failing to reject H₀ means the data do not provide sufficient evidence against H₀ at the given significance level. It does NOT mean H₀ is true. The test may have low power (e.g., small sample size), failing to detect a real difference. 'Fail to reject' ≠ 'accept.'",
     "hypothesis_testing"),

    # IM-11 R diff=5
    ("ap_stats", "inference_means", "R", 5,
     "A 95% confidence interval for μ₁ − μ₂ from a two-sample t-test is (−2.1, 8.3). Which conclusion is most appropriate?",
     "multiple_choice",
     "There is significant evidence that μ₁ > μ₂ because the interval contains positive values.",
     "There is significant evidence that μ₁ < μ₂ because the interval contains negative values.",
     "There is no significant evidence of a difference because the interval contains 0, meaning 0 is a plausible difference.",
     "The interval is invalid because it crosses zero.",
     "C",
     "A confidence interval that contains 0 means 0 is a plausible value for the difference μ₁ − μ₂. This corresponds to failing to reject H₀: μ₁ = μ₂ in a two-sided test at the corresponding significance level. The interval crossing zero does not invalidate it — it simply indicates insufficient evidence to conclude a difference exists.",
     "confidence_intervals"),

    # IM-12 R diff=5
    ("ap_stats", "inference_means", "R", 5,
     "A researcher wants to compare two teaching methods using students in the same school. She considers (1) randomly assigning each student to one method or (2) measuring each student under both methods (with a washout period). Which design is preferred and why?",
     "multiple_choice",
     "Design 1, because larger sample sizes are better.",
     "Design 2, because the paired design controls for student ability differences, increasing power.",
     "Design 1, because two-sample t-tests are always more powerful than paired t-tests.",
     "Design 2, because all experiments must be within-subject designs.",
     "B",
     "The paired design (Design 2) removes student-to-student variability as a source of error, since each student serves as their own control. This increases the power of the test to detect real differences between methods. Two-sample designs are appropriate when pairing is not possible, but the paired design is preferred when feasible for this reason.",
     "paired_vs_two_sample"),

    # =========================================================================
    # CHI-SQUARE — 5 questions (F×1, U×2, A×1, R×1)
    # =========================================================================

    # CS-1 F diff=2
    ("ap_stats", "chi_square", "F", 2,
     "A chi-square goodness-of-fit test is used to determine whether:",
     "multiple_choice",
     "Two categorical variables are associated.",
     "The distribution of a single categorical variable matches a claimed distribution.",
     "Two population means are equal.",
     "A regression slope is significantly different from zero.",
     "B",
     "The chi-square goodness-of-fit test compares the observed distribution of one categorical variable to an expected (claimed) distribution. A chi-square test for independence or homogeneity is used to examine relationships between two categorical variables.",
     "chi_square_gof"),

    # CS-2 U diff=2
    ("ap_stats", "chi_square", "U", 2,
     "In a chi-square test, the expected count for a cell is calculated as:",
     "multiple_choice",
     "(Row total × Column total) / Grand total",
     "(Observed − Expected)² / Expected",
     "Row total / Grand total",
     "Observed count × sample size",
     "A",
     "For a chi-square test of independence or homogeneity, expected count = (row total × column total) / grand total. This formula creates the expected counts under the assumption of independence (no association between the variables).",
     "chi_square_independence"),

    # CS-3 U diff=3
    ("ap_stats", "chi_square", "U", 3,
     "A chi-square test yields χ² = 12.4 with 3 degrees of freedom and a p-value of 0.006. At α = 0.05, the conclusion is:",
     "multiple_choice",
     "Fail to reject H₀; the distribution fits the expected pattern.",
     "Reject H₀; there is significant evidence the observed distribution differs from expected.",
     "Accept H₀; the chi-square statistic is too large.",
     "The test is inconclusive because df = 3.",
     "B",
     "p-value (0.006) < α (0.05), so we reject H₀. There is significant evidence that the observed distribution differs from the hypothesized distribution (goodness-of-fit) or that the variables are not independent (test of independence). Larger chi-square values indicate greater discrepancy between observed and expected.",
     "chi_square_gof"),

    # CS-4 A diff=3
    ("ap_stats", "chi_square", "A", 3,
     "A researcher surveys 200 students on their preferred study environment (library, home, café) and their year in school (freshman, sophomore, junior, senior). She wants to know if study environment preference is associated with year. What test should she use?",
     "multiple_choice",
     "One-sample t-test",
     "Chi-square goodness-of-fit test",
     "Chi-square test of independence",
     "Two-proportion z-test",
     "C",
     "The chi-square test of independence examines whether two categorical variables (study environment and year in school) are associated in a single population. The goodness-of-fit test compares one variable to a specified distribution. T-tests and z-tests apply to quantitative or proportion data.",
     "chi_square_independence"),

    # CS-5 R diff=4
    ("ap_stats", "chi_square", "R", 4,
     "What is the key difference between a chi-square test of independence and a chi-square test of homogeneity?",
     "multiple_choice",
     "The test of independence uses a larger significance level.",
     "The test of homogeneity requires matched pairs; the test of independence does not.",
     "In a test of independence, one random sample is drawn and both variables are measured. In a test of homogeneity, separate random samples are drawn from different populations and one categorical variable is compared across groups.",
     "The calculations are completely different for the two tests.",
     "C",
     "Both tests use the same chi-square formula and mechanics. The key conceptual difference is the sampling design: independence tests draw one sample and categorize by two variables; homogeneity tests draw separate samples from multiple populations and compare distributions of one variable. The hypotheses and interpretation differ accordingly.",
     "chi_square_homogeneity"),

    # =========================================================================
    # INFERENCE FOR SLOPES — 5 questions (F×1, U×2, A×1, R×1)
    # =========================================================================

    # IS-1 F diff=2
    ("ap_stats", "inference_slopes", "F", 2,
     "In regression inference, the null hypothesis for the slope is typically H₀: β = 0. What does rejecting this hypothesis mean?",
     "multiple_choice",
     "The regression line has a slope of exactly 0.",
     "There is a statistically significant linear relationship between the explanatory and response variables.",
     "The y-intercept is not significantly different from 0.",
     "The coefficient of determination r² is large.",
     "B",
     "H₀: β = 0 means no linear relationship between x and y. Rejecting H₀ provides evidence that β ≠ 0 — that a statistically significant linear relationship exists. This does not necessarily mean the relationship is strong or practically important (r² may still be low).",
     "regression_inference"),

    # IS-2 U diff=3
    ("ap_stats", "inference_slopes", "U", 3,
     "A t-test for the slope of a regression line yields t = 3.8 with df = 18 and p = 0.001. The regression equation is ŷ = 2 + 0.5x. What is the correct conclusion?",
     "multiple_choice",
     "The slope is not statistically significant; we cannot use this regression.",
     "There is strong evidence of a positive linear relationship between x and y in the population.",
     "The slope equals exactly 0.5 in the population.",
     "The regression explains 3.8% of the variation in y.",
     "B",
     "t = 3.8 and p = 0.001 < 0.05 (or any common α). We reject H₀: β = 0. There is strong evidence that the population slope is not 0 — i.e., a significant positive linear relationship exists. The sample slope (0.5) is our estimate; t = 3.8 is the test statistic, not r².",
     "regression_inference"),

    # IS-3 U diff=3
    ("ap_stats", "inference_slopes", "U", 3,
     "A 95% confidence interval for the population slope β is (0.3, 0.9). What is the correct interpretation?",
     "multiple_choice",
     "95% of the data points fall within 0.3 and 0.9 of the regression line.",
     "We are 95% confident that for each one-unit increase in x, the population mean response y increases between 0.3 and 0.9 units.",
     "There is a 95% probability the true slope is between 0.3 and 0.9.",
     "The slope equals 0.6 with ±95% precision.",
     "B",
     "The confidence interval for the slope is interpreted in terms of the population linear relationship: we are 95% confident that the true population slope β is between 0.3 and 0.9. This means for each one-unit increase in x, the average y increases by between 0.3 and 0.9 units in the population.",
     "regression_inference"),

    # IS-4 A diff=4
    ("ap_stats", "inference_slopes", "A", 4,
     "A computer output for regression shows: slope = 1.24, SE of slope = 0.31, df = 23. What is the t-statistic for the test H₀: β = 0?",
     "multiple_choice",
     "0.25", "1.24", "4.00", "28.52",
     "C",
     "t = b / SE_b = 1.24 / 0.31 = 4.00. The t-statistic for testing the slope measures how many standard errors the sample slope is from 0. With df = 23, t = 4.00 would yield a very small p-value, providing strong evidence against H₀: β = 0.",
     "regression_inference"),

    # IS-5 R diff=5
    ("ap_stats", "inference_slopes", "R", 5,
     "A researcher notes that a test for H₀: β = 0 is significant (p < 0.05) but r² = 0.04. What is the most appropriate interpretation?",
     "multiple_choice",
     "The result is contradictory — a significant slope always means a strong relationship.",
     "The linear relationship is statistically significant but explains very little of the variation in y (only 4%), so it may not be practically useful.",
     "r² = 0.04 means the test was performed incorrectly.",
     "Statistical significance confirms the relationship is important for prediction.",
     "B",
     "With very large samples, even tiny, practically trivial slopes can be statistically significant. r² = 0.04 means the linear model explains only 4% of the variability in y — a very weak relationship. Statistical significance tells us the slope is probably not exactly zero, but practical utility requires examining effect size (r², the slope magnitude, and context).",
     "regression_inference"),

]

# ---------------------------------------------------------------------------
# Schema
# ---------------------------------------------------------------------------

CREATE_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS questions (
    id               INTEGER PRIMARY KEY AUTOINCREMENT,
    track            TEXT    NOT NULL,
    sat_domain       TEXT    NOT NULL,
    fuar_dimension   TEXT    NOT NULL,
    difficulty       INTEGER NOT NULL,
    question_text    TEXT    NOT NULL,
    question_type    TEXT    NOT NULL DEFAULT 'multiple_choice',
    option_a         TEXT,
    option_b         TEXT,
    option_c         TEXT,
    option_d         TEXT,
    correct_answer   TEXT    NOT NULL,
    explanation      TEXT,
    topic_tag        TEXT,
    created_at       DATETIME DEFAULT CURRENT_TIMESTAMP
);
"""

# ---------------------------------------------------------------------------
# Seeding
# ---------------------------------------------------------------------------

def seed():
    import os
    db_path = os.path.join(os.path.dirname(__file__), DB_PATH)
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    # Ensure table exists
    cur.executescript(CREATE_TABLE_SQL)

    # Remove existing ap_stats questions
    cur.execute("DELETE FROM questions WHERE track = 'ap_stats'")
    deleted = cur.rowcount
    print(f"Deleted {deleted} existing ap_stats question(s).")

    # Insert new questions
    insert_sql = """
        INSERT INTO questions (
            track, sat_domain, fuar_dimension, difficulty,
            question_text, question_type,
            option_a, option_b, option_c, option_d,
            correct_answer, explanation, topic_tag
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """
    cur.executemany(insert_sql, QUESTIONS)
    conn.commit()

    inserted = cur.rowcount
    print(f"Inserted {len(QUESTIONS)} ap_stats question(s).")

    # Summary by unit
    print("\n--- Summary by unit (sat_domain) ---")
    cur.execute("""
        SELECT sat_domain, fuar_dimension, COUNT(*) as cnt
        FROM questions
        WHERE track = 'ap_stats'
        GROUP BY sat_domain, fuar_dimension
        ORDER BY sat_domain, fuar_dimension
    """)
    rows = cur.fetchall()
    unit_totals = {}
    for domain, fuar, cnt in rows:
        unit_totals[domain] = unit_totals.get(domain, 0) + cnt
        print(f"  {domain:<30} {fuar}  {cnt}")

    print("\n--- Totals by unit ---")
    for domain, total in sorted(unit_totals.items()):
        print(f"  {domain:<30} {total}")

    print(f"\nTotal ap_stats questions in DB: {sum(unit_totals.values())}")

    # Summary by difficulty
    print("\n--- Difficulty distribution ---")
    cur.execute("""
        SELECT difficulty, COUNT(*) as cnt
        FROM questions
        WHERE track = 'ap_stats'
        GROUP BY difficulty
        ORDER BY difficulty
    """)
    for diff, cnt in cur.fetchall():
        print(f"  Difficulty {diff}: {cnt} questions")

    conn.close()
    print("\nDone.")


if __name__ == "__main__":
    seed()
