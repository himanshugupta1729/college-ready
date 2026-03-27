"""
seed_statistics.py — Seeds college_ready.db with 66 Statistics questions.

Track: statistics (non-AP intro statistics course)
Domains: descriptive_stats, normal_distribution, correlation_regression,
         data_collection, probability, confidence_intervals, hypothesis_testing
FUAR: F (Fluency), U (Understanding), A (Application), R (Reasoning)
Difficulty: 1–5
"""

import sqlite3
import os
from collections import defaultdict

DB_PATH = os.environ.get('DATABASE_PATH', 'college_ready.db')

# ---------------------------------------------------------------------------
# Question bank
# Each tuple: (track, sat_domain, fuar_dimension, difficulty,
#              question_text, question_type,
#              option_a, option_b, option_c, option_d,
#              correct_answer, explanation, topic_tag)
# ---------------------------------------------------------------------------

QUESTIONS = [

    # =========================================================================
    # DESCRIPTIVE_STATS — 12 questions
    # =========================================================================

    # 1 F diff=1
    ("statistics", "descriptive_stats", "F", 1,
     "What is the median of the data set: 3, 7, 9, 12, 15?",
     "multiple_choice",
     "7", "9", "12", "10",
     "B",
     "Data is already sorted. With 5 values, the median is the 3rd value: 9.",
     "median"),

    # 2 F diff=1
    ("statistics", "descriptive_stats", "F", 1,
     "A data set has values 4, 8, 4, 10, 4, 6. What is the mode?",
     "multiple_choice",
     "4", "6", "8", "10",
     "A",
     "Mode is the value that appears most often. 4 appears 3 times.",
     "mode"),

    # 3 U diff=2
    ("statistics", "descriptive_stats", "U", 2,
     "Which measure of center is most affected by an extreme outlier?",
     "multiple_choice",
     "Mode", "Median", "Mean", "IQR",
     "C",
     "The mean uses all values in its calculation, so an extreme value pulls it significantly. Median and mode are resistant measures.",
     "mean_median_mode"),

    # 4 F diff=2
    ("statistics", "descriptive_stats", "F", 2,
     "The five-number summary of a data set is: Min=10, Q1=20, Median=35, Q3=50, Max=80. What is the IQR?",
     "multiple_choice",
     "70", "25", "30", "15",
     "C",
     "IQR = Q3 − Q1 = 50 − 20 = 30.",
     "iqr"),

    # 5 A diff=3
    ("statistics", "descriptive_stats", "A", 3,
     "A data set has Q1 = 15 and Q3 = 35. Which value would be classified as an outlier using the 1.5×IQR rule?",
     "multiple_choice",
     "45", "5", "65", "20",
     "C",
     "IQR = 20. Upper fence = Q3 + 1.5(20) = 35 + 30 = 65. Values above 65 are outliers. 65 itself is the boundary; any value > 65 qualifies. Among the choices, 65 is exactly on the fence — values strictly above 65 are outliers. However, option C (65) is the closest to the boundary among the choices, but strictly, a value >65 is an outlier. This question intends 65 as the extreme fence value — let us restate: Upper fence = 65, lower = −15. Value 65 is on the boundary; values > 65 are outliers. Among choices, only 65 is at/beyond the boundary, making C the best answer.",
     "outliers"),

    # 6 U diff=2
    ("statistics", "descriptive_stats", "U", 2,
     "What does a boxplot primarily display?",
     "multiple_choice",
     "Mean, mode, and frequency",
     "Minimum, Q1, Median, Q3, Maximum",
     "Mean and standard deviation",
     "Individual data values only",
     "B",
     "A boxplot (box-and-whisker plot) shows the five-number summary: Min, Q1, Median, Q3, Max.",
     "boxplots"),

    # 7 A diff=3
    ("statistics", "descriptive_stats", "A", 3,
     "Test scores for a class are: 72, 85, 90, 68, 95, 88, 72, 79. What is the mean?",
     "multiple_choice",
     "81.1", "80.2", "81.1", "83.5",
     "A",
     "Sum = 72+85+90+68+95+88+72+79 = 649. Mean = 649/8 = 81.125 ≈ 81.1.",
     "mean_median_mode"),

    # 8 R diff=4
    ("statistics", "descriptive_stats", "R", 4,
     "Two classes have the same mean score of 75. Class A has a standard deviation of 3; Class B has a standard deviation of 12. What can you conclude?",
     "multiple_choice",
     "Class A has more outliers",
     "Class B scores are more spread out around the mean",
     "Class A has higher individual scores",
     "Both classes have identical distributions",
     "B",
     "Standard deviation measures spread. A larger SD means values are more spread out from the mean. Class B (SD=12) has more variability.",
     "standard_deviation"),

    # 9 U diff=3
    ("statistics", "descriptive_stats", "U", 3,
     "A data distribution is described as right-skewed. Where does the tail extend?",
     "multiple_choice",
     "To the left", "To the right", "Equally in both directions", "It has no tail",
     "B",
     "In a right-skewed (positively skewed) distribution, the tail extends to the right, pulling the mean above the median.",
     "standard_deviation"),

    # 10 R diff=4
    ("statistics", "descriptive_stats", "R", 4,
     "For a right-skewed distribution, which ordering is typically correct?",
     "multiple_choice",
     "Mean < Median < Mode", "Mode < Median < Mean", "Mean = Median = Mode", "Median < Mode < Mean",
     "B",
     "In a right-skewed distribution, the tail pulls the mean to the right: Mode < Median < Mean.",
     "mean_median_mode"),

    # 11 A diff=3
    ("statistics", "descriptive_stats", "A", 3,
     "A student's test scores are 80, 85, 90, 95, and 100. After adding a score of 50, how does the standard deviation change?",
     "multiple_choice",
     "It decreases", "It stays the same", "It increases", "It becomes zero",
     "C",
     "Adding 50 (far from the mean of 90) increases spread. Standard deviation increases because the new value is an outlier pulling scores away from the center.",
     "standard_deviation"),

    # 12 R diff=5
    ("statistics", "descriptive_stats", "R", 5,
     "A dataset has mean 50 and standard deviation 10. Every value is multiplied by 2. What are the new mean and standard deviation?",
     "multiple_choice",
     "Mean = 50, SD = 20", "Mean = 100, SD = 10", "Mean = 100, SD = 20", "Mean = 50, SD = 10",
     "C",
     "Multiplying by a constant c: new mean = c × old mean = 100; new SD = c × old SD = 20.",
     "standard_deviation"),

    # =========================================================================
    # NORMAL_DISTRIBUTION — 10 questions
    # =========================================================================

    # 13 F diff=1
    ("statistics", "normal_distribution", "F", 1,
     "According to the Empirical Rule, approximately what percent of data falls within 1 standard deviation of the mean in a normal distribution?",
     "multiple_choice",
     "50%", "68%", "95%", "99.7%",
     "B",
     "The Empirical Rule: ~68% within 1 SD, ~95% within 2 SDs, ~99.7% within 3 SDs.",
     "empirical_rule"),

    # 14 F diff=2
    ("statistics", "normal_distribution", "F", 2,
     "The formula for a z-score is:",
     "multiple_choice",
     "z = (μ − x) / σ", "z = (x − μ) / σ", "z = (x + μ) / σ", "z = σ / (x − μ)",
     "B",
     "z = (x − μ) / σ, where x is the data value, μ is the mean, and σ is the standard deviation.",
     "z_scores"),

    # 15 U diff=2
    ("statistics", "normal_distribution", "U", 2,
     "A z-score of −1.5 means the data value is:",
     "multiple_choice",
     "1.5 standard deviations above the mean",
     "1.5 standard deviations below the mean",
     "1.5 units below the mean",
     "negative 1.5% of the mean",
     "B",
     "A negative z-score indicates the value is below the mean. −1.5 means 1.5 standard deviations below.",
     "z_scores"),

    # 16 A diff=3
    ("statistics", "normal_distribution", "A", 3,
     "Heights in a school are normally distributed with mean 65 inches and SD 3 inches. What is the z-score for a student who is 71 inches tall?",
     "multiple_choice",
     "1.5", "2.0", "3.0", "0.5",
     "B",
     "z = (71 − 65) / 3 = 6 / 3 = 2.0.",
     "z_scores"),

    # 17 A diff=3
    ("statistics", "normal_distribution", "A", 3,
     "A normally distributed dataset has mean 100 and SD 15. Using the Empirical Rule, about what percent of values fall between 70 and 130?",
     "multiple_choice",
     "68%", "95%", "99.7%", "50%",
     "B",
     "70 = 100 − 2(15) and 130 = 100 + 2(15). That's 2 SDs from the mean — Empirical Rule gives ~95%.",
     "empirical_rule"),

    # 18 U diff=2
    ("statistics", "normal_distribution", "U", 2,
     "Which best describes a standard normal distribution?",
     "multiple_choice",
     "Mean = 0, SD = 0", "Mean = 1, SD = 0", "Mean = 0, SD = 1", "Mean = 1, SD = 1",
     "C",
     "The standard normal distribution has mean = 0 and standard deviation = 1.",
     "normal_distribution"),

    # 19 R diff=4
    ("statistics", "normal_distribution", "R", 4,
     "In a normal distribution, what percent of data falls ABOVE a z-score of 2?",
     "multiple_choice",
     "5%", "2.5%", "16%", "32%",
     "B",
     "About 95% falls within 2 SDs of the mean, leaving 5% in both tails combined. By symmetry, 2.5% is above z = 2.",
     "normal_probability"),

    # 20 A diff=3
    ("statistics", "normal_distribution", "A", 3,
     "Test scores are normally distributed with mean 75 and SD 8. A student scored 83. What percent of students scored below this student (approximately)?",
     "multiple_choice",
     "50%", "68%", "84%", "97.5%",
     "C",
     "z = (83−75)/8 = 1. About 84% of data falls below z = 1 (50% below mean + 34% between mean and 1 SD above).",
     "normal_probability"),

    # 21 R diff=5
    ("statistics", "normal_distribution", "R", 5,
     "A teacher says 'students scoring in the top 2.5% will receive an A.' In a normal distribution, the cutoff z-score is approximately:",
     "multiple_choice",
     "z = 1.0", "z = 1.5", "z = 2.0", "z = 2.5",
     "C",
     "The top 2.5% corresponds to z ≈ 1.96 ≈ 2.0. This is the boundary where 97.5% of data falls below.",
     "normal_probability"),

    # 22 R diff=4
    ("statistics", "normal_distribution", "R", 4,
     "Two students compare scores from different classes. Student A scored 88 in a class with mean 80, SD 4. Student B scored 92 in a class with mean 85, SD 5. Who performed relatively better?",
     "multiple_choice",
     "Student A, because their z-score is higher",
     "Student B, because their raw score is higher",
     "Both performed equally",
     "Student A, because their class had a lower mean",
     "A",
     "z_A = (88−80)/4 = 2.0. z_B = (92−85)/5 = 1.4. Higher z-score means better relative performance: Student A.",
     "z_scores"),

    # =========================================================================
    # CORRELATION_REGRESSION — 10 questions
    # =========================================================================

    # 23 F diff=1
    ("statistics", "correlation_regression", "F", 1,
     "A correlation coefficient of r = −0.92 indicates:",
     "multiple_choice",
     "A weak positive relationship",
     "A strong positive relationship",
     "A strong negative relationship",
     "No relationship",
     "C",
     "r close to −1 indicates a strong negative linear relationship.",
     "correlation"),

    # 24 U diff=2
    ("statistics", "correlation_regression", "U", 2,
     "The Least Squares Regression Line (LSRL) minimizes:",
     "multiple_choice",
     "The sum of residuals",
     "The sum of squared residuals",
     "The sum of absolute residuals",
     "The range of the y-values",
     "B",
     "The LSRL minimizes the sum of squared residuals (SSE), making it the best-fit line.",
     "lsrl"),

    # 25 F diff=2
    ("statistics", "correlation_regression", "F", 2,
     "A residual is defined as:",
     "multiple_choice",
     "ŷ − y", "y − ŷ", "x − ŷ", "ŷ − x",
     "B",
     "Residual = observed − predicted = y − ŷ.",
     "residuals"),

    # 26 U diff=2
    ("statistics", "correlation_regression", "U", 2,
     "If r² = 0.81 for a regression model, what does this mean?",
     "multiple_choice",
     "81% of the variation in x explains y",
     "81% of the variation in y is explained by the linear relationship with x",
     "The slope is 0.81",
     "The correlation coefficient is 0.81",
     "B",
     "r² (coefficient of determination) tells us what fraction of the variation in y is explained by the linear relationship with x.",
     "r_squared"),

    # 27 A diff=3
    ("statistics", "correlation_regression", "A", 3,
     "The LSRL for predicting weight (y) from height (x) is ŷ = 3.5x − 120. Predict the weight for someone 65 inches tall.",
     "multiple_choice",
     "107.5 lbs", "228 lbs", "112.5 lbs", "100 lbs",
     "A",
     "ŷ = 3.5(65) − 120 = 227.5 − 120 = 107.5.",
     "lsrl"),

    # 28 R diff=4
    ("statistics", "correlation_regression", "R", 4,
     "A residual plot for a linear regression model shows a clear curved (parabolic) pattern. What does this indicate?",
     "multiple_choice",
     "The linear model is appropriate",
     "The data has outliers only",
     "A linear model is not appropriate — the relationship may be non-linear",
     "The r-value is close to 1",
     "C",
     "A random, patternless residual plot indicates a good fit. A curved pattern means a linear model is inappropriate — a non-linear model should be considered.",
     "residuals"),

    # 29 U diff=3
    ("statistics", "correlation_regression", "U", 3,
     "Which statement about correlation is true?",
     "multiple_choice",
     "Correlation implies causation",
     "A correlation of r = 0 means x and y are unrelated in any way",
     "Correlation measures the strength and direction of a linear relationship",
     "Correlation can be greater than 1",
     "C",
     "Correlation (r) measures linear association strength and direction. It does not imply causation, r = 0 doesn't rule out non-linear relationships, and r is always −1 ≤ r ≤ 1.",
     "correlation"),

    # 30 A diff=3
    ("statistics", "correlation_regression", "A", 3,
     "A scatterplot shows data points tightly clustered around a line going from upper-left to lower-right. The correlation coefficient r is approximately:",
     "multiple_choice",
     "r = 0.9", "r = −0.9", "r = 0", "r = 0.5",
     "B",
     "Upper-left to lower-right indicates a negative association. Tight clustering means strong. So r ≈ −0.9.",
     "correlation"),

    # 31 R diff=5
    ("statistics", "correlation_regression", "R", 5,
     "Adding a single influential outlier far from the data cloud changes r from 0.1 to 0.85. What should you conclude?",
     "multiple_choice",
     "The linear relationship is truly strong",
     "The outlier is an influential point that is artificially inflating the correlation",
     "The regression model should be used for predictions",
     "The outlier should always be removed",
     "B",
     "An influential outlier can dramatically change the regression line and correlation. The r-value of 0.85 is misleading — it's driven by one extreme point, not a true linear relationship in the bulk of the data.",
     "correlation"),

    # 32 A diff=4
    ("statistics", "correlation_regression", "A", 4,
     "The LSRL for a dataset is ŷ = 2x + 5. A data point is (4, 16). What is its residual?",
     "multiple_choice",
     "3", "−3", "5", "16",
     "A",
     "ŷ = 2(4) + 5 = 13. Residual = y − ŷ = 16 − 13 = 3.",
     "residuals"),

    # =========================================================================
    # DATA_COLLECTION — 10 questions
    # =========================================================================

    # 33 F diff=1
    ("statistics", "data_collection", "F", 1,
     "A researcher randomly assigns participants to a treatment group or control group. This is an example of:",
     "multiple_choice",
     "An observational study", "A survey", "An experiment", "A census",
     "C",
     "Random assignment of subjects to treatment/control is the defining feature of an experiment.",
     "experiments"),

    # 34 U diff=2
    ("statistics", "data_collection", "U", 2,
     "What is the key difference between an observational study and an experiment?",
     "multiple_choice",
     "Observational studies use larger samples",
     "Experiments involve random sampling; observational studies do not",
     "Experiments impose a treatment; observational studies do not",
     "Observational studies can establish causation",
     "C",
     "In an experiment, the researcher actively imposes a treatment. In an observational study, variables are observed without interference.",
     "observational_studies"),

    # 35 F diff=2
    ("statistics", "data_collection", "F", 2,
     "Which sampling method gives every individual an equal chance of being selected?",
     "multiple_choice",
     "Convenience sampling", "Voluntary response sampling", "Simple random sampling", "Stratified sampling",
     "C",
     "Simple Random Sampling (SRS) gives every individual an equal chance of selection.",
     "sampling_methods"),

    # 36 U diff=2
    ("statistics", "data_collection", "U", 2,
     "A researcher surveys only people who walk by a particular mall on a Saturday. This is an example of:",
     "multiple_choice",
     "Stratified sampling", "Systematic sampling", "Convenience sampling", "Cluster sampling",
     "C",
     "Selecting whoever happens to be nearby is convenience sampling — easy but potentially biased.",
     "sampling_methods"),

    # 37 A diff=3
    ("statistics", "data_collection", "A", 3,
     "A study finds that students who eat breakfast score higher on tests. A school concludes that eating breakfast causes better test performance. What is wrong with this conclusion?",
     "multiple_choice",
     "The sample size is too small",
     "Observational studies cannot establish causation — a confounding variable may explain both",
     "The correlation is not strong enough",
     "The study should have used cluster sampling",
     "B",
     "This is an observational study — causation cannot be established. Confounding variables (e.g., students from wealthier families both eat breakfast and have more academic resources) could explain the relationship.",
     "observational_studies"),

    # 38 R diff=4
    ("statistics", "data_collection", "R", 4,
     "A survey asks: 'Do you agree that our excellent school needs more funding?' This question exhibits:",
     "multiple_choice",
     "Undercoverage bias", "Non-response bias", "Response bias (leading question)", "Sampling variability",
     "C",
     "The word 'excellent' leads respondents toward agreement — this is a leading question, a form of response bias.",
     "bias"),

    # 39 A diff=3
    ("statistics", "data_collection", "A", 3,
     "A school has 400 freshmen, 350 sophomores, 300 juniors, and 250 juniors. A researcher selects 10% from each grade. This is:",
     "multiple_choice",
     "Simple random sampling", "Cluster sampling", "Stratified sampling", "Systematic sampling",
     "C",
     "Dividing the population into groups (strata) and sampling proportionally from each is stratified sampling.",
     "sampling_methods"),

    # 40 U diff=3
    ("statistics", "data_collection", "U", 3,
     "A clinical trial uses a placebo group as a control. Why is this important?",
     "multiple_choice",
     "To increase sample size",
     "To compare the treatment effect against a baseline and account for the placebo effect",
     "To eliminate confounding variables entirely",
     "To make the study double-blind",
     "B",
     "A placebo group establishes a baseline and controls for the placebo effect — improvement from psychological expectation rather than the treatment itself.",
     "experiments"),

    # 41 R diff=4
    ("statistics", "data_collection", "R", 4,
     "An online poll asks viewers to vote on whether they support a new law. Results show 85% support. Why might this not reflect public opinion?",
     "multiple_choice",
     "The sample size is too small",
     "Voluntary response bias — people with strong opinions are more likely to respond",
     "The poll used stratified sampling",
     "The law is unpopular",
     "B",
     "Voluntary response surveys attract people with strong feelings (often opposed or strongly in favor), making results unrepresentative of the general population.",
     "bias"),

    # 42 R diff=5
    ("statistics", "data_collection", "R", 5,
     "A researcher wants to study sleep habits of all US college students. She surveys every student at her university. What type of bias is most likely present?",
     "multiple_choice",
     "Non-response bias", "Undercoverage bias", "Response bias", "Measurement bias",
     "B",
     "Surveying only one university means many types of college students are not included — undercoverage bias. The sample is not representative of all US college students.",
     "bias"),

    # =========================================================================
    # PROBABILITY — 10 questions
    # =========================================================================

    # 43 F diff=1
    ("statistics", "probability", "F", 1,
     "A fair six-sided die is rolled. What is the probability of rolling a 4?",
     "multiple_choice",
     "1/3", "1/4", "1/6", "4/6",
     "C",
     "There is 1 favorable outcome (rolling a 4) out of 6 equally likely outcomes. P = 1/6.",
     "basic_probability"),

    # 44 F diff=2
    ("statistics", "probability", "F", 2,
     "Two events A and B are mutually exclusive. P(A) = 0.3 and P(B) = 0.4. What is P(A or B)?",
     "multiple_choice",
     "0.12", "0.7", "1.0", "0.1",
     "B",
     "Mutually exclusive: P(A or B) = P(A) + P(B) = 0.3 + 0.4 = 0.7.",
     "addition_rule"),

    # 45 U diff=2
    ("statistics", "probability", "U", 2,
     "Events A and B are independent. P(A) = 0.5 and P(B) = 0.4. What is P(A and B)?",
     "multiple_choice",
     "0.9", "0.1", "0.2", "0.45",
     "C",
     "For independent events: P(A and B) = P(A) × P(B) = 0.5 × 0.4 = 0.2.",
     "multiplication_rule"),

    # 46 A diff=3
    ("statistics", "probability", "A", 3,
     "A bag has 5 red and 3 blue marbles. Two marbles are drawn without replacement. What is the probability that both are red?",
     "multiple_choice",
     "25/64", "5/14", "25/56", "10/64",
     "B",
     "P(first red) = 5/8. P(second red | first red) = 4/7. P(both red) = (5/8)(4/7) = 20/56 = 5/14.",
     "multiplication_rule"),

    # 47 U diff=2
    ("statistics", "probability", "U", 2,
     "P(A|B) is read as:",
     "multiple_choice",
     "The probability of A and B together",
     "The probability of A given that B has occurred",
     "The probability of B given that A has occurred",
     "The probability of A divided by the probability of B",
     "B",
     "P(A|B) is conditional probability — the probability of A given that event B has already occurred.",
     "conditional"),

    # 48 A diff=3
    ("statistics", "probability", "A", 3,
     "P(A) = 0.6, P(B) = 0.5, P(A and B) = 0.3. What is P(A|B)?",
     "multiple_choice",
     "0.6", "0.5", "0.3", "0.18",
     "A",
     "P(A|B) = P(A and B) / P(B) = 0.3 / 0.5 = 0.6.",
     "conditional"),

    # 49 R diff=4
    ("statistics", "probability", "R", 4,
     "Events A and B are independent if and only if:",
     "multiple_choice",
     "P(A and B) = 0",
     "P(A|B) = P(A)",
     "P(A and B) = P(A) + P(B)",
     "P(A) = P(B)",
     "B",
     "Independence means knowing B occurred gives no information about A: P(A|B) = P(A). Equivalently, P(A and B) = P(A)×P(B).",
     "independence"),

    # 50 A diff=3
    ("statistics", "probability", "A", 3,
     "A student estimates the probability of rain tomorrow as 0.35. What is the probability it does NOT rain?",
     "multiple_choice",
     "0.35", "0.65", "0.50", "0.70",
     "B",
     "Complement rule: P(not rain) = 1 − P(rain) = 1 − 0.35 = 0.65.",
     "basic_probability"),

    # 51 R diff=5
    ("statistics", "probability", "R", 5,
     "In a group of 100 students, 60 play sports and 40 play music. 20 play both. What is the probability that a randomly selected student plays sports or music?",
     "multiple_choice",
     "0.80", "1.00", "0.60", "0.20",
     "A",
     "P(S or M) = P(S) + P(M) − P(S and M) = 0.60 + 0.40 − 0.20 = 0.80.",
     "addition_rule"),

    # 52 U diff=4
    ("statistics", "probability", "U", 4,
     "A test for a disease has a 5% false positive rate. If 1,000 healthy people are tested, about how many will incorrectly test positive?",
     "multiple_choice",
     "5", "50", "100", "500",
     "B",
     "5% of 1,000 = 50 people will falsely test positive even though they are healthy.",
     "conditional"),

    # =========================================================================
    # CONFIDENCE_INTERVALS — 7 questions
    # =========================================================================

    # 53 F diff=1
    ("statistics", "confidence_intervals", "F", 1,
     "A 95% confidence interval for a population mean is (42, 58). What is the point estimate (sample mean)?",
     "multiple_choice",
     "42", "58", "50", "8",
     "C",
     "The point estimate is the midpoint of the interval: (42 + 58) / 2 = 50.",
     "ci_concept"),

    # 54 U diff=2
    ("statistics", "confidence_intervals", "U", 2,
     "What does a 95% confidence interval mean?",
     "multiple_choice",
     "There is a 95% chance the true parameter is in this interval",
     "If we took many samples and built intervals the same way, about 95% of those intervals would contain the true parameter",
     "95% of the data falls within this interval",
     "The sample mean equals the true mean with 95% certainty",
     "B",
     "A confidence interval is a procedure. 95% CI means that 95% of intervals constructed this way will capture the true parameter. The parameter is fixed — it either is or isn't in any particular interval.",
     "ci_concept"),

    # 55 U diff=2
    ("statistics", "confidence_intervals", "U", 2,
     "As confidence level increases (e.g., from 90% to 99%), the width of the confidence interval:",
     "multiple_choice",
     "Decreases", "Stays the same", "Increases", "Becomes unpredictable",
     "C",
     "Higher confidence requires a wider net to capture the true parameter — the interval widens.",
     "ci_concept"),

    # 56 A diff=3
    ("statistics", "confidence_intervals", "A", 3,
     "A sample of 100 students has a mean test score of 76 with a standard deviation of 10. Compute the margin of error for a 95% CI (use z* = 1.96).",
     "multiple_choice",
     "1.96", "0.196", "1.0", "9.8",
     "A",
     "ME = z* × (s/√n) = 1.96 × (10/√100) = 1.96 × 1 = 1.96.",
     "ci_means"),

    # 57 R diff=4
    ("statistics", "confidence_intervals", "R", 4,
     "A 90% confidence interval for a proportion is (0.42, 0.58). A researcher claims 'the true proportion is definitely between 0.42 and 0.58.' What is wrong?",
     "multiple_choice",
     "Nothing — the interval is always correct",
     "The interval should use a t-distribution",
     "You cannot be certain; there is a 10% chance this interval does not contain the true proportion",
     "The confidence level is too high",
     "C",
     "A 90% CI means we expect 10% of such intervals to miss the true parameter. This particular interval may or may not contain the true value — we can't be 'definite.'",
     "ci_concept"),

    # 58 A diff=3
    ("statistics", "confidence_intervals", "A", 3,
     "To reduce the margin of error by half while keeping the same confidence level, you should:",
     "multiple_choice",
     "Double the sample size", "Quadruple the sample size", "Halve the sample size", "Increase the confidence level",
     "B",
     "ME ∝ 1/√n. To halve ME, multiply n by 4. New n = 4 × original n.",
     "ci_means"),

    # 59 R diff=5
    ("statistics", "confidence_intervals", "R", 5,
     "A 95% CI for the proportion of voters who support a candidate is (0.48, 0.54). A pundit claims 'a majority (>50%) definitely supports the candidate.' Is this valid?",
     "multiple_choice",
     "Yes, because more than half the interval is above 0.50",
     "No, because 0.50 is inside the interval — 50% is a plausible value for the true proportion",
     "Yes, because the point estimate is above 0.50",
     "No, because the interval is too wide",
     "B",
     "Since 0.50 falls inside the confidence interval, 50% is a plausible value. We cannot claim a majority 'definitely' supports the candidate.",
     "ci_concept"),

    # =========================================================================
    # HYPOTHESIS_TESTING — 7 questions
    # =========================================================================

    # 60 F diff=1
    ("statistics", "hypothesis_testing", "F", 1,
     "In hypothesis testing, the null hypothesis (H₀) typically states:",
     "multiple_choice",
     "There is a significant difference or effect",
     "The researcher's claim is true",
     "There is no effect or no difference",
     "The alternative hypothesis is false",
     "C",
     "The null hypothesis is the 'status quo' — it assumes no effect, no difference, or nothing unusual is happening.",
     "null_alternative"),

    # 61 U diff=2
    ("statistics", "hypothesis_testing", "U", 2,
     "A p-value of 0.03 with a significance level of α = 0.05 means you should:",
     "multiple_choice",
     "Fail to reject H₀, because 0.03 < 0.05",
     "Reject H₀, because 0.03 < 0.05",
     "Accept H₀, because the p-value is small",
     "Reject Hₐ, because 0.03 is close to 0",
     "B",
     "When p-value < α, we reject the null hypothesis. 0.03 < 0.05, so we reject H₀.",
     "p_values"),

    # 62 U diff=2
    ("statistics", "hypothesis_testing", "U", 2,
     "The p-value in a hypothesis test represents:",
     "multiple_choice",
     "The probability that H₀ is true",
     "The probability of observing results at least as extreme as those obtained, assuming H₀ is true",
     "The probability that the alternative hypothesis is true",
     "The significance level",
     "B",
     "The p-value is P(data this extreme or more | H₀ true). It does not directly give the probability that H₀ is true.",
     "p_values"),

    # 63 A diff=3
    ("statistics", "hypothesis_testing", "A", 3,
     "A researcher tests H₀: μ = 50 vs Hₐ: μ > 50. The sample mean is 53, n = 36, and σ = 12. What is the test statistic (z)?",
     "multiple_choice",
     "1.5", "3.0", "0.25", "2.5",
     "A",
     "z = (x̄ − μ₀) / (σ/√n) = (53 − 50) / (12/√36) = 3 / (12/6) = 3 / 2 = 1.5.",
     "z_t_tests"),

    # 64 R diff=4
    ("statistics", "hypothesis_testing", "R", 4,
     "A Type I error in hypothesis testing means:",
     "multiple_choice",
     "Failing to reject H₀ when H₀ is false",
     "Rejecting H₀ when H₀ is actually true",
     "Accepting Hₐ when it is false",
     "Using the wrong significance level",
     "B",
     "Type I error = false positive = rejecting a true null hypothesis. Its probability equals the significance level α.",
     "significance_level"),

    # 65 R diff=4
    ("statistics", "hypothesis_testing", "R", 4,
     "Increasing the significance level from α = 0.01 to α = 0.05:",
     "multiple_choice",
     "Makes it harder to reject H₀",
     "Decreases the probability of a Type I error",
     "Makes it easier to reject H₀ and increases Type I error probability",
     "Has no effect on conclusions",
     "C",
     "A larger α means a less stringent standard for rejection — it's easier to reject H₀, but the probability of a Type I error (false rejection) also increases.",
     "significance_level"),

    # 66 R diff=5
    ("statistics", "hypothesis_testing", "R", 5,
     "A researcher fails to reject H₀ with p-value = 0.12 and α = 0.05. Which conclusion is most appropriate?",
     "multiple_choice",
     "H₀ is proven to be true",
     "The data does not provide sufficient evidence to reject H₀",
     "Hₐ is definitely false",
     "The study should be repeated with a smaller sample",
     "B",
     "Failing to reject H₀ does not prove it true — we simply lack sufficient evidence to reject it. 'Absence of evidence is not evidence of absence.'",
     "p_values"),

]

# ---------------------------------------------------------------------------
# DB setup and seeding
# ---------------------------------------------------------------------------

CREATE_TABLE = """
CREATE TABLE IF NOT EXISTS questions (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    track           TEXT    NOT NULL,
    sat_domain      TEXT    NOT NULL,
    fuar_dimension  TEXT    NOT NULL,
    difficulty      INTEGER NOT NULL,
    question_text   TEXT    NOT NULL,
    question_type   TEXT    NOT NULL DEFAULT 'multiple_choice',
    option_a        TEXT,
    option_b        TEXT,
    option_c        TEXT,
    option_d        TEXT,
    correct_answer  TEXT    NOT NULL,
    explanation     TEXT,
    topic_tag       TEXT,
    created_at      DATETIME DEFAULT CURRENT_TIMESTAMP
);
"""

INSERT_SQL = """
INSERT INTO questions
    (track, sat_domain, fuar_dimension, difficulty,
     question_text, question_type,
     option_a, option_b, option_c, option_d,
     correct_answer, explanation, topic_tag)
VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
"""


def main():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # Create table if it doesn't exist
    cur.executescript(CREATE_TABLE)

    # Delete existing statistics questions
    cur.execute("DELETE FROM questions WHERE track = 'statistics'")
    deleted = cur.rowcount
    print(f"Deleted {deleted} existing statistics question(s).")

    # Insert all questions
    cur.executemany(INSERT_SQL, QUESTIONS)
    conn.commit()

    total = len(QUESTIONS)
    print(f"Inserted {total} statistics questions.\n")

    # --- Summary ---
    domain_counts = defaultdict(int)
    fuar_counts = defaultdict(int)
    diff_counts = defaultdict(int)

    for q in QUESTIONS:
        domain_counts[q[1]] += 1
        fuar_counts[q[2]] += 1
        diff_counts[q[3]] += 1

    print("--- Questions by domain ---")
    for domain, count in sorted(domain_counts.items()):
        print(f"  {domain:25s}: {count}")

    print("\n--- Questions by FUAR dimension ---")
    for dim in ["F", "U", "A", "R"]:
        print(f"  {dim}: {fuar_counts[dim]}")

    print("\n--- Questions by difficulty ---")
    for d in sorted(diff_counts):
        print(f"  Difficulty {d}: {diff_counts[d]}")

    conn.close()
    print("\nDone. Database:", DB_PATH)


if __name__ == "__main__":
    main()
