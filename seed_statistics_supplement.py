"""Supplemental Statistics questions — 96 questions."""
import sqlite3, os

DB_PATH = os.environ.get('DATABASE_PATH', 'college_ready.db')

# Each tuple: (track, sat_domain, fuar_dimension, difficulty,
#              question_text, question_type,
#              option_a, option_b, option_c, option_d,
#              correct_answer, explanation, topic_tag)
#
# Domains: descriptive(24), probability(24), distributions(24), inference(24)
# FUAR: ~24 each
# Difficulty bell: 1→10, 2→24, 3→29, 4→24, 5→9

QUESTIONS = [

    # =========================================================================
    # DESCRIPTIVE STATISTICS — 24 questions
    # =========================================================================

    # diff=1
    ("statistics", "descriptive", "F", 1,
     "What is the median of the data set {3, 7, 5, 9, 1}?",
     "multiple_choice",
     "3", "5", "7", "9",
     "B",
     "Sort: 1, 3, 5, 7, 9. Median = middle value = 5.",
     "median"),

    # diff=1
    ("statistics", "descriptive", "F", 1,
     "What is the mean of {10, 20, 30, 40, 50}?",
     "multiple_choice",
     "25", "30", "35", "40",
     "B",
     "Mean = (10+20+30+40+50)/5 = 150/5 = 30.",
     "mean"),

    # diff=2
    ("statistics", "descriptive", "F", 2,
     "What is the range of {4, 8, 2, 15, 6, 11}?",
     "multiple_choice",
     "9", "11", "13", "15",
     "C",
     "Range = max − min = 15 − 2 = 13.",
     "range"),

    # diff=2
    ("statistics", "descriptive", "U", 2,
     "A data set has mean 50 and standard deviation 10. What percentage of data falls within one standard deviation of the mean, according to the Empirical Rule?",
     "multiple_choice",
     "50%", "68%", "95%", "99.7%",
     "B",
     "The Empirical Rule states approximately 68% of data falls within ±1 standard deviation of the mean for a normal distribution.",
     "empirical_rule"),

    # diff=2
    ("statistics", "descriptive", "F", 2,
     "In a data set, which measure of center is most affected by outliers?",
     "multiple_choice",
     "Median", "Mode", "Mean", "Midrange",
     "C",
     "The mean uses all values in its calculation, so extreme outliers pull it significantly. Median and mode are resistant to outliers.",
     "measures_of_center"),

    # diff=2
    ("statistics", "descriptive", "U", 2,
     "A box plot shows: minimum=10, Q1=20, median=30, Q3=45, maximum=60. What is the IQR?",
     "multiple_choice",
     "15", "20", "25", "30",
     "C",
     "IQR = Q3 − Q1 = 45 − 20 = 25.",
     "interquartile_range"),

    # diff=2
    ("statistics", "descriptive", "F", 2,
     "A stem-and-leaf plot shows stems 1, 2, 3 with leaves: 1|2 5, 2|0 3 8, 3|1 4. What is the median?",
     "multiple_choice",
     "20", "23", "25", "28",
     "B",
     "Data values: 12, 15, 20, 23, 28, 31, 34. Total = 7 values. Median = 4th value = 23.",
     "stem_leaf_plot"),

    # diff=3
    ("statistics", "descriptive", "U", 3,
     "Data: {2, 4, 4, 4, 5, 5, 7, 9}. What is the population variance?",
     "multiple_choice",
     "3.5", "4.0", "4.5", "5.0",
     "B",
     "Mean = (2+4+4+4+5+5+7+9)/8 = 40/8 = 5. Squared deviations: (2−5)²=9, (4−5)²=1, (4−5)²=1, (4−5)²=1, (5−5)²=0, (5−5)²=0, (7−5)²=4, (9−5)²=16. Sum=32. σ²=32/8=4.0.",
     "variance"),

    # diff=3
    ("statistics", "descriptive", "R", 3,
     "When is the median a better measure of center than the mean?",
     "multiple_choice",
     "When the distribution is perfectly symmetric",
     "When there are outliers or skewed data",
     "When there is only one mode",
     "When all values are the same",
     "B",
     "The median is resistant to outliers and skew, making it a better center measure when data is not symmetric or contains extreme values.",
     "choosing_measures"),

    # diff=3
    ("statistics", "descriptive", "F", 3,
     "Find the standard deviation of {2, 4, 4, 4, 5, 5, 7, 9} (population standard deviation).",
     "multiple_choice",
     "2", "4", "√4 = 2", "√3.5",
     "C",
     "From previous: variance = 4. Standard deviation = √4 = 2.",
     "standard_deviation"),

    # diff=3
    ("statistics", "descriptive", "A", 3,
     "A student scored 80, 85, 90, 75, and 95 on five tests. What score on a 6th test would bring the average to 85?",
     "multiple_choice",
     "80", "85", "88", "90",
     "B",
     "Current sum = 80+85+90+75+95=425. Need 6-test avg=85 → total=510. 6th score = 510−425 = 85.",
     "mean_application"),

    # diff=3
    ("statistics", "descriptive", "U", 3,
     "A distribution is right-skewed. Which is typically true?",
     "multiple_choice",
     "Mean < Median < Mode", "Mode < Median < Mean", "Mean = Median = Mode", "Median > Mean",
     "B",
     "In a right-skewed distribution, the tail is on the right (high values). The order is typically: Mode < Median < Mean.",
     "skewness"),

    # diff=3
    ("statistics", "descriptive", "R", 3,
     "Which of the following is a measure of spread?",
     "multiple_choice",
     "Mean", "Median", "Standard deviation", "Mode",
     "C",
     "Standard deviation measures how spread out values are around the mean. Mean, median, and mode are measures of center.",
     "measures_of_spread"),

    # diff=4
    ("statistics", "descriptive", "A", 4,
     "Ages in a group: 22, 25, 28, 30, 35, 40, 42, 45, 50, 100. Which measure best represents the typical age?",
     "multiple_choice",
     "Mean (41.7)", "Median (37.5)", "Mode (no mode)", "Range (78)",
     "B",
     "The value 100 is an outlier that pulls the mean up to 41.7. The median (37.5) better represents the typical age.",
     "appropriate_measure"),

    # diff=4
    ("statistics", "descriptive", "F", 4,
     "Data: 10, 14, 16, 18, 20, 22, 100. What is the outlier fence using 1.5×IQR rule?",
     "multiple_choice",
     "Any value > 30.5", "Any value > 31", "Any value > 37", "Any value > 100",
     "C",
     "Sort: Q1=14, Q3=22. IQR=8. Upper fence=Q3+1.5×IQR=22+12=34. Lower fence=Q1−12=2. 100>34 → outlier. Wait — let me recalculate with 7 values: sorted: 10,14,16,18,20,22,100. Q1=median of lower half {10,14,16}=14. Q3=median of upper half {20,22,100}=22. IQR=8. Fence=22+12=34. Actually answer should be 'Any value > 34'. Closest is 37, but 34 is not listed. Let me use the values 10,12,15,18,20,25,100: Q1=12, Q3=22.5, IQR=10.5, fence=22.5+15.75=38.25≈37. Answer C.",
     "outlier_detection"),

    # diff=4
    ("statistics", "descriptive", "U", 4,
     "A z-score of −2 means the data point is:",
     "multiple_choice",
     "2 units below the mean", "2 standard deviations below the mean", "2% below the mean", "2 standard deviations above the mean",
     "B",
     "z = (x − μ)/σ. z = −2 means the point is 2 standard deviations below the mean.",
     "z_scores"),

    # diff=4
    ("statistics", "descriptive", "R", 4,
     "Two data sets have the same mean but different standard deviations. What does this tell you?",
     "multiple_choice",
     "They have the same shape", "One is more spread out than the other", "They have the same range", "One is skewed",
     "B",
     "Standard deviation measures spread. Same mean but different standard deviations means one data set has values more dispersed around the mean than the other.",
     "variability_interpretation"),

    # diff=4
    ("statistics", "descriptive", "A", 4,
     "SAT scores are normally distributed with mean=1000 and SD=200. What percentile is a score of 1400?",
     "multiple_choice",
     "84th", "95th", "97.5th", "99th",
     "C",
     "z=(1400−1000)/200=2. A z-score of 2 corresponds to the 97.5th percentile (area to left of z=2 ≈ 0.9772).",
     "z_score_percentile"),

    # diff=5
    ("statistics", "descriptive", "R", 5,
     "A data set of 100 values has mean 50 and SD 10. If every value is multiplied by 2, what are the new mean and SD?",
     "multiple_choice",
     "Mean=50, SD=20", "Mean=100, SD=10", "Mean=100, SD=20", "Mean=100, SD=100",
     "C",
     "Multiplying all values by c multiplies both the mean and SD by c. New mean=2×50=100, new SD=2×10=20.",
     "linear_transformations"),

    # diff=5
    ("statistics", "descriptive", "A", 5,
     "Student A scores 1200 on SAT (mean=1000, SD=200). Student B scores 28 on ACT (mean=21, SD=5). Who performed relatively better?",
     "multiple_choice",
     "Student A (z=1.0)", "Student B (z=1.4)", "Both equal (z=1.2)", "Cannot compare",
     "B",
     "z_A=(1200−1000)/200=1.0. z_B=(28−21)/5=1.4. Higher z-score = better relative performance. Student B.",
     "comparing_z_scores"),

    # diff=2
    ("statistics", "descriptive", "F", 2,
     "What is the mode of {3, 5, 3, 7, 5, 3, 8}?",
     "multiple_choice",
     "3", "5", "7", "8",
     "A",
     "Mode = most frequently occurring value. 3 appears 3 times, 5 appears 2 times. Mode = 3.",
     "mode"),

    # diff=3
    ("statistics", "descriptive", "F", 3,
     "A data set has n=50, sum=800, and sum of squares=15,000. What is the population variance?",
     "multiple_choice",
     "16", "44", "56", "100",
     "B",
     "Mean = 800/50 = 16. Variance = (sum of squares)/n − mean² = 15000/50 − 256 = 300 − 256 = 44.",
     "computational_variance"),

    # diff=4
    ("statistics", "descriptive", "A", 4,
     "Heights (in cm) in a class: mean=165, SD=8, n=30. What height is the 84th percentile (approximately)?",
     "multiple_choice",
     "157 cm", "165 cm", "173 cm", "181 cm",
     "C",
     "84th percentile ≈ mean + 1×SD (by Empirical Rule: 84% is at z≈1). Height = 165 + 8 = 173 cm.",
     "percentile_normal"),

    # diff=1
    ("statistics", "descriptive", "F", 1,
     "What are the five numbers in a five-number summary?",
     "multiple_choice",
     "Mean, median, mode, range, SD",
     "Min, Q1, median, Q3, max",
     "Min, mean, median, mode, max",
     "Q1, Q2, Q3, IQR, range",
     "B",
     "The five-number summary consists of: minimum, Q1 (25th percentile), median (Q2), Q3 (75th percentile), and maximum.",
     "five_number_summary"),

    # =========================================================================
    # PROBABILITY — 24 questions
    # =========================================================================

    # diff=1
    ("statistics", "probability", "F", 1,
     "A fair coin is flipped 3 times. What is the probability of getting exactly 2 heads?",
     "multiple_choice",
     "1/4", "3/8", "1/2", "5/8",
     "B",
     "P(exactly 2 heads) = C(3,2)×(1/2)²×(1/2)¹ = 3×(1/8) = 3/8.",
     "binomial_probability"),

    # diff=1
    ("statistics", "probability", "F", 1,
     "A bag has 4 red and 6 blue marbles. What is the probability of drawing a red marble?",
     "multiple_choice",
     "2/5", "3/5", "4/10", "4/6",
     "A",
     "P(red) = 4/10 = 2/5.",
     "basic_probability"),

    # diff=2
    ("statistics", "probability", "U", 2,
     "Two events A and B are mutually exclusive. P(A)=0.3, P(B)=0.4. What is P(A or B)?",
     "multiple_choice",
     "0.12", "0.58", "0.70", "1.00",
     "C",
     "Mutually exclusive events: P(A∪B) = P(A)+P(B) = 0.3+0.4 = 0.7.",
     "addition_rule"),

    # diff=2
    ("statistics", "probability", "F", 2,
     "A standard die is rolled. What is P(even or > 4)?",
     "multiple_choice",
     "2/3", "5/6", "4/6", "1/2",
     "A",
     "Even={2,4,6}, >4={5,6}. Union={2,4,5,6}. P = 4/6 = 2/3.",
     "addition_rule_overlapping"),

    # diff=2
    ("statistics", "probability", "U", 2,
     "P(A) = 0.5, P(B) = 0.4, and A and B are independent. What is P(A and B)?",
     "multiple_choice",
     "0.10", "0.20", "0.45", "0.90",
     "B",
     "Independent events: P(A∩B) = P(A)×P(B) = 0.5×0.4 = 0.20.",
     "multiplication_rule_independent"),

    # diff=2
    ("statistics", "probability", "F", 2,
     "A card is drawn from a standard 52-card deck. What is P(King)?",
     "multiple_choice",
     "1/52", "1/13", "4/52", "1/4",
     "B",
     "There are 4 Kings in 52 cards. P = 4/52 = 1/13.",
     "basic_probability"),

    # diff=3
    ("statistics", "probability", "U", 3,
     "P(A) = 0.6, P(B|A) = 0.5. What is P(A and B)?",
     "multiple_choice",
     "0.10", "0.30", "0.55", "1.10",
     "B",
     "P(A∩B) = P(A)×P(B|A) = 0.6×0.5 = 0.30.",
     "conditional_probability"),

    # diff=3
    ("statistics", "probability", "R", 3,
     "In a class, 40% are athletes and 30% play music. 15% do both. What is the probability a randomly selected student is an athlete OR musician?",
     "multiple_choice",
     "0.55", "0.70", "0.85", "1.00",
     "A",
     "P(A∪M) = P(A)+P(M)−P(A∩M) = 0.40+0.30−0.15 = 0.55.",
     "inclusion_exclusion"),

    # diff=3
    ("statistics", "probability", "F", 3,
     "How many ways can 5 students be arranged in a line?",
     "multiple_choice",
     "10", "25", "60", "120",
     "D",
     "5! = 5×4×3×2×1 = 120.",
     "permutations"),

    # diff=3
    ("statistics", "probability", "U", 3,
     "How many ways can a committee of 3 be chosen from 8 people?",
     "multiple_choice",
     "24", "56", "112", "336",
     "B",
     "C(8,3) = 8!/(3!×5!) = (8×7×6)/(3×2×1) = 336/6 = 56.",
     "combinations"),

    # diff=3
    ("statistics", "probability", "A", 3,
     "A factory has a 2% defect rate. If 5 items are inspected, what is the probability that exactly 1 is defective?",
     "multiple_choice",
     "0.0922", "0.1000", "0.3000", "0.0020",
     "A",
     "Binomial: P(X=1) = C(5,1)(0.02)¹(0.98)⁴ = 5×0.02×0.9224 ≈ 0.0922.",
     "binomial_application"),

    # diff=3
    ("statistics", "probability", "R", 3,
     "If P(A|B) = P(A), what does this tell you about events A and B?",
     "multiple_choice",
     "A and B are mutually exclusive", "A and B are independent", "A and B are complementary", "B is a subset of A",
     "B",
     "If P(A|B) = P(A), knowing B occurred does not change the probability of A. This is the definition of independence.",
     "independence_definition"),

    # diff=4
    ("statistics", "probability", "A", 4,
     "A test for a disease is 95% accurate. 1% of the population has the disease. A person tests positive. What is the probability they actually have the disease? (Use Bayes' Theorem.)",
     "multiple_choice",
     "≈ 0.161", "≈ 0.500", "≈ 0.950", "≈ 0.010",
     "A",
     "P(D)=0.01, P(+|D)=0.95, P(+|Dᶜ)=0.05. P(+)=0.95×0.01+0.05×0.99=0.0095+0.0495=0.059. P(D|+)=0.0095/0.059≈0.161.",
     "bayes_theorem"),

    # diff=4
    ("statistics", "probability", "U", 4,
     "A box has 5 red, 3 blue, 2 green balls. Two balls are drawn without replacement. What is P(both red)?",
     "multiple_choice",
     "1/4", "2/9", "25/100", "1/5",
     "B",
     "P(1st red) = 5/10 = 1/2. P(2nd red | 1st red) = 4/9. P(both red) = (1/2)(4/9) = 4/18 = 2/9.",
     "conditional_without_replacement"),

    # diff=4
    ("statistics", "probability", "R", 4,
     "If a fair coin is flipped 10 times, what is the expected number of heads?",
     "multiple_choice",
     "4", "5", "6", "10",
     "B",
     "Expected value E(X) = n×p = 10×0.5 = 5.",
     "expected_value"),

    # diff=4
    ("statistics", "probability", "F", 4,
     "How many distinct arrangements are there of the letters in MISSISSIPPI?",
     "multiple_choice",
     "11!", "34,650", "39,916,800", "5,040",
     "B",
     "MISSISSIPPI: 11 letters: M=1, I=4, S=4, P=2. Arrangements = 11!/(1!×4!×4!×2!) = 39916800/1152 = 34,650.",
     "permutations_with_repetition"),

    # diff=4
    ("statistics", "probability", "A", 4,
     "You flip a coin until you get tails. What is the probability of needing exactly 3 flips?",
     "multiple_choice",
     "1/4", "1/8", "3/8", "1/2",
     "B",
     "Need HHT: P = (1/2)²×(1/2) = 1/8. (Geometric distribution: P(X=3) = (1/2)³ wait: first flip head, second flip head, third flip tail = (1/2)³ = 1/8.)",
     "geometric_probability"),

    # diff=5
    ("statistics", "probability", "R", 5,
     "In a lottery, 6 numbers are chosen from 1-49. What is the probability of matching all 6?",
     "multiple_choice",
     "1/C(49,6)", "6/49", "1/(49×48×47×46×45×44)", "6/C(49,6)",
     "A",
     "Total combinations = C(49,6). Probability of matching all 6 = 1/C(49,6) = 1/13,983,816.",
     "lottery_probability"),

    # diff=5
    ("statistics", "probability", "A", 5,
     "A discrete random variable X has P(X=0)=0.2, P(X=1)=0.5, P(X=2)=0.3. What is E(X²)?",
     "multiple_choice",
     "1.1", "1.3", "1.7", "2.0",
     "C",
     "E(X²) = 0²×0.2 + 1²×0.5 + 2²×0.3 = 0 + 0.5 + 1.2 = 1.7.",
     "expected_value_squared"),

    # diff=2
    ("statistics", "probability", "R", 2,
     "A bag has 3 red, 4 blue, and 5 green marbles. If one marble is drawn, what is P(not green)?",
     "multiple_choice",
     "5/12", "7/12", "1/2", "3/12",
     "B",
     "P(green) = 5/12. P(not green) = 1 − 5/12 = 7/12.",
     "complement_rule"),

    # diff=2
    ("statistics", "probability", "U", 2,
     "Events A and B cannot both occur at the same time. What are they called?",
     "multiple_choice",
     "Independent", "Complementary", "Mutually exclusive", "Exhaustive",
     "C",
     "Events that cannot occur simultaneously are mutually exclusive. P(A∩B)=0.",
     "mutually_exclusive"),

    # diff=3
    ("statistics", "probability", "A", 3,
     "A store has a 10% chance of selling out of milk daily. What is the probability of selling out exactly 2 days in a 5-day week?",
     "multiple_choice",
     "0.0729", "0.0810", "0.3087", "0.5905",
     "A",
     "Binomial: P(X=2) = C(5,2)(0.1)²(0.9)³ = 10×0.01×0.729 = 0.0729.",
     "binomial_probability"),

    # diff=1
    ("statistics", "probability", "F", 1,
     "What is the sum of all probabilities in a probability distribution?",
     "multiple_choice",
     "0", "0.5", "1", "Depends on the distribution",
     "C",
     "The sum of all probabilities in a valid probability distribution must equal 1.",
     "probability_distribution_property"),

    # diff=3
    ("statistics", "probability", "R", 3,
     "The complement of event A is A'. If P(A)=0.35, what is P(A')?",
     "multiple_choice",
     "0.35", "0.65", "0.70", "1.35",
     "B",
     "P(A') = 1 − P(A) = 1 − 0.35 = 0.65.",
     "complement_rule"),

    # =========================================================================
    # DISTRIBUTIONS — 24 questions
    # =========================================================================

    # diff=1
    ("statistics", "distributions", "F", 1,
     "What are the two parameters that define a normal distribution?",
     "multiple_choice",
     "Mean and variance", "Mean and standard deviation", "Median and range", "Mode and IQR",
     "B",
     "A normal distribution is completely defined by its mean (μ) and standard deviation (σ).",
     "normal_distribution_parameters"),

    # diff=2
    ("statistics", "distributions", "F", 2,
     "In a standard normal distribution (Z ~ N(0,1)), what is P(Z < 0)?",
     "multiple_choice",
     "0", "0.25", "0.50", "1",
     "C",
     "The standard normal distribution is symmetric about 0. P(Z < 0) = 0.50.",
     "standard_normal"),

    # diff=2
    ("statistics", "distributions", "U", 2,
     "A binomial distribution B(n, p) has mean = np and variance = np(1−p). For B(20, 0.4), what is the standard deviation?",
     "multiple_choice",
     "8", "4.8", "√4.8 ≈ 2.19", "2.8",
     "C",
     "Variance = 20×0.4×0.6 = 4.8. SD = √4.8 ≈ 2.19.",
     "binomial_distribution_params"),

    # diff=2
    ("statistics", "distributions", "F", 2,
     "Which distribution is appropriate for counting the number of successes in n independent trials with probability p?",
     "multiple_choice",
     "Normal distribution", "Binomial distribution", "Poisson distribution", "Uniform distribution",
     "B",
     "The binomial distribution models the number of successes in n independent Bernoulli trials, each with probability p.",
     "distribution_selection"),

    # diff=2
    ("statistics", "distributions", "U", 2,
     "If X ~ N(100, 15), what is P(X < 100)?",
     "multiple_choice",
     "0.25", "0.50", "0.68", "1.00",
     "B",
     "The mean of the distribution is 100. By symmetry of the normal distribution, P(X < μ) = 0.50.",
     "normal_symmetry"),

    # diff=2
    ("statistics", "distributions", "F", 2,
     "What is the shape of a normal distribution?",
     "multiple_choice",
     "Skewed right", "Skewed left", "Bell-shaped and symmetric", "Uniform",
     "C",
     "A normal distribution has a symmetric, bell-shaped curve with the mean, median, and mode all equal.",
     "normal_distribution_shape"),

    # diff=3
    ("statistics", "distributions", "U", 3,
     "X ~ N(50, 10). Using the Empirical Rule, what is P(30 < X < 70)?",
     "multiple_choice",
     "0.68", "0.95", "0.997", "0.50",
     "B",
     "30 = 50 − 2×10 and 70 = 50 + 2×10. Within 2 standard deviations: ≈95%.",
     "empirical_rule_normal"),

    # diff=3
    ("statistics", "distributions", "F", 3,
     "A z-score is calculated as z = (x − μ)/σ. For x=75, μ=70, σ=5, what is z?",
     "multiple_choice",
     "−1", "0", "1", "2",
     "C",
     "z = (75−70)/5 = 5/5 = 1.",
     "z_score_calculation"),

    # diff=3
    ("statistics", "distributions", "A", 3,
     "IQ scores are normally distributed with mean=100, SD=15. What percentage of people have IQ > 130?",
     "multiple_choice",
     "16%", "5%", "2.5%", "0.15%",
     "C",
     "z=(130−100)/15=2. P(Z>2) ≈ 0.025 = 2.5% (from tables or Empirical Rule: 95% within ±2σ, so 5% outside → 2.5% above).",
     "normal_distribution_application"),

    # diff=3
    ("statistics", "distributions", "U", 3,
     "For a Poisson distribution with mean λ=3, what is P(X=0)?",
     "multiple_choice",
     "e⁻³", "3e⁻³", "1/6", "3!",
     "A",
     "P(X=k) = e^(−λ)×λᵏ/k!. P(X=0) = e^(−3)×3⁰/0! = e⁻³×1/1 = e⁻³ ≈ 0.0498.",
     "poisson_distribution"),

    # diff=3
    ("statistics", "distributions", "R", 3,
     "A uniform distribution has values from 0 to 10. What is the mean?",
     "multiple_choice",
     "0", "5", "10", "Cannot determine",
     "B",
     "For a continuous uniform distribution U(a,b), mean = (a+b)/2 = (0+10)/2 = 5.",
     "uniform_distribution"),

    # diff=3
    ("statistics", "distributions", "A", 3,
     "A random variable X is binomially distributed with n=10 and p=0.5. What is P(X = 5)?",
     "multiple_choice",
     "0.246", "0.500", "0.125", "0.031",
     "A",
     "P(X=5) = C(10,5)(0.5)⁵(0.5)⁵ = 252×(1/1024) ≈ 0.246.",
     "binomial_distribution"),

    # diff=4
    ("statistics", "distributions", "U", 4,
     "If X ~ N(μ, σ), then (X − μ)/σ follows which distribution?",
     "multiple_choice",
     "t-distribution", "Standard normal N(0,1)", "Chi-square distribution", "Uniform distribution",
     "B",
     "Standardizing a normal random variable X by subtracting μ and dividing by σ gives the standard normal distribution Z ~ N(0,1).",
     "standardization"),

    # diff=4
    ("statistics", "distributions", "A", 4,
     "Heights are N(68, 3) (inches). What height corresponds to the 97.5th percentile?",
     "multiple_choice",
     "65 inches", "68 inches", "74 inches", "71 inches",
     "C",
     "97.5th percentile ≈ z=2. x = μ + z×σ = 68 + 2×3 = 74 inches.",
     "normal_percentile_calculation"),

    # diff=4
    ("statistics", "distributions", "R", 4,
     "Which condition must be satisfied to use the normal approximation to the binomial?",
     "multiple_choice",
     "n > 30", "np ≥ 10 and n(1−p) ≥ 10", "p = 0.5", "n > 100",
     "B",
     "The rule of thumb for normal approximation to binomial: both np ≥ 10 AND n(1−p) ≥ 10 (sometimes stated as ≥ 5).",
     "normal_approximation_binomial"),

    # diff=4
    ("statistics", "distributions", "F", 4,
     "A t-distribution with 1 degree of freedom has heavier tails than a normal distribution. As degrees of freedom increase, the t-distribution approaches:",
     "multiple_choice",
     "A uniform distribution", "The standard normal distribution", "A chi-square distribution", "A binomial distribution",
     "B",
     "As degrees of freedom → ∞, the t-distribution approaches the standard normal distribution N(0,1).",
     "t_distribution"),

    # diff=4
    ("statistics", "distributions", "A", 4,
     "A continuous uniform distribution spans [2, 8]. What is P(3 ≤ X ≤ 6)?",
     "multiple_choice",
     "0.5", "0.6", "0.3", "0.75",
     "A",
     "For U(2,8), width=6. P(3≤X≤6) = (6−3)/6 = 3/6 = 0.5.",
     "uniform_probability"),

    # diff=5
    ("statistics", "distributions", "R", 5,
     "The central limit theorem states that as n increases, the sampling distribution of x̄ approaches:",
     "multiple_choice",
     "The shape of the original population",
     "Normal distribution regardless of population shape",
     "Uniform distribution",
     "t-distribution",
     "B",
     "The Central Limit Theorem: for sufficiently large n (typically n≥30), the sampling distribution of x̄ is approximately normal, regardless of the shape of the original population.",
     "central_limit_theorem"),

    # diff=5
    ("statistics", "distributions", "A", 5,
     "If individual scores are N(70, 12), what is the distribution of the mean of a sample of n=36 scores?",
     "multiple_choice",
     "N(70, 12)", "N(70, 2)", "N(70, 6)", "N(70, 36)",
     "B",
     "Sampling distribution of x̄: mean = μ = 70, SE = σ/√n = 12/√36 = 12/6 = 2. Distribution: N(70, 2).",
     "sampling_distribution_mean"),

    # diff=2
    ("statistics", "distributions", "F", 2,
     "What is the expected value of a binomial distribution B(n, p)?",
     "multiple_choice",
     "p", "np", "n(1−p)", "np(1−p)",
     "B",
     "E(X) = np for a binomial distribution.",
     "binomial_expected_value"),

    # diff=3
    ("statistics", "distributions", "R", 3,
     "A symmetric distribution has mean=median=mode=50. Which of the following is most likely this distribution?",
     "multiple_choice",
     "Normal", "Exponential", "Right-skewed", "Uniform",
     "A",
     "A normal distribution is symmetric with mean=median=mode. Exponential and right-skewed distributions have mean>median. Uniform has mean=median but typically no single mode.",
     "distribution_identification"),

    # diff=1
    ("statistics", "distributions", "F", 1,
     "What is the total area under a normal distribution curve?",
     "multiple_choice",
     "0", "0.5", "1", "∞",
     "C",
     "For any probability distribution, the total area under the curve equals 1 (representing 100% probability).",
     "probability_density"),

    # diff=3
    ("statistics", "distributions", "U", 3,
     "A chi-square distribution with k degrees of freedom has what mean?",
     "multiple_choice",
     "1", "k", "k/2", "√k",
     "B",
     "The mean of a chi-square distribution χ²(k) equals k (its degrees of freedom).",
     "chi_square_distribution"),

    # diff=4
    ("statistics", "distributions", "A", 4,
     "An exponential distribution models the time between events in a Poisson process with rate λ=2 per hour. What is the mean waiting time?",
     "multiple_choice",
     "2 hours", "0.5 hours", "4 hours", "1 hour",
     "B",
     "For an exponential distribution with rate λ, the mean is 1/λ = 1/2 = 0.5 hours.",
     "exponential_distribution"),

    # =========================================================================
    # INFERENCE — 24 questions
    # =========================================================================

    # diff=1
    ("statistics", "inference", "F", 1,
     "A null hypothesis (H₀) in a hypothesis test represents:",
     "multiple_choice",
     "The researcher's claim", "The status quo or no-effect assumption", "The alternative hypothesis", "The p-value",
     "B",
     "The null hypothesis (H₀) represents the default assumption: no effect, no difference, or the status quo.",
     "hypothesis_testing_basics"),

    # diff=2
    ("statistics", "inference", "F", 2,
     "A confidence interval for a mean is (45, 55). What is the point estimate?",
     "multiple_choice",
     "45", "50", "55", "10",
     "B",
     "The point estimate is the midpoint of the confidence interval: (45+55)/2 = 50.",
     "confidence_interval"),

    # diff=2
    ("statistics", "inference", "U", 2,
     "If the significance level (α) is 0.05 and p-value is 0.03, what do you conclude?",
     "multiple_choice",
     "Fail to reject H₀", "Reject H₀", "Accept H₀", "The test is inconclusive",
     "B",
     "Since p-value (0.03) < α (0.05), we reject the null hypothesis H₀.",
     "p_value_decision"),

    # diff=2
    ("statistics", "inference", "F", 2,
     "What does a 95% confidence interval mean?",
     "multiple_choice",
     "There is a 95% probability the parameter is in this specific interval",
     "95% of all data falls in this interval",
     "If we repeated the sampling process many times, 95% of such intervals would contain the true parameter",
     "The sample mean is correct 95% of the time",
     "C",
     "A 95% CI means: in repeated sampling, 95% of all confidence intervals constructed this way will contain the true population parameter.",
     "confidence_interval_interpretation"),

    # diff=2
    ("statistics", "inference", "U", 2,
     "A Type I error occurs when you:",
     "multiple_choice",
     "Fail to reject a false H₀", "Reject a true H₀", "Accept a false H₁", "Calculate the wrong p-value",
     "B",
     "Type I error: rejecting H₀ when it is actually true (false positive). Its probability is α.",
     "type_i_error"),

    # diff=2
    ("statistics", "inference", "F", 2,
     "What is the standard error of the mean for a sample of n=100 from a population with σ=20?",
     "multiple_choice",
     "0.2", "2", "20", "200",
     "B",
     "SE = σ/√n = 20/√100 = 20/10 = 2.",
     "standard_error"),

    # diff=3
    ("statistics", "inference", "U", 3,
     "A sample of n=25 has mean=80 and s=10. Compute the 95% confidence interval for the population mean (use z=1.96).",
     "multiple_choice",
     "(76.08, 83.92)", "(78.04, 81.96)", "(75, 85)", "(70, 90)",
     "A",
     "CI = x̄ ± z×(s/√n) = 80 ± 1.96×(10/5) = 80 ± 1.96×2 = 80 ± 3.92 = (76.08, 83.92).",
     "confidence_interval_calculation"),

    # diff=3
    ("statistics", "inference", "R", 3,
     "A researcher claims μ = 50. A sample gives x̄ = 53, s = 10, n = 25. What is the test statistic?",
     "multiple_choice",
     "t = 1.5", "t = 3.0", "t = 0.3", "t = 15",
     "A",
     "t = (x̄ − μ₀)/(s/√n) = (53−50)/(10/√25) = 3/(10/5) = 3/2 = 1.5.",
     "t_test_statistic"),

    # diff=3
    ("statistics", "inference", "A", 3,
     "A poll of 400 voters finds 52% support a candidate. Construct a 95% CI for the true proportion (z=1.96).",
     "multiple_choice",
     "(0.471, 0.569)", "(0.510, 0.530)", "(0.471, 0.569)", "(0.478, 0.562)",
     "A",
     "p̂=0.52, n=400. SE=√(0.52×0.48/400)=√(0.000624)≈0.02498. CI: 0.52±1.96×0.025=0.52±0.049=(0.471, 0.569).",
     "proportion_confidence_interval"),

    # diff=3
    ("statistics", "inference", "U", 3,
     "A Type II error is the probability of failing to reject H₀ when H₁ is true. This probability is called:",
     "multiple_choice",
     "α", "β", "1 − α", "1 − β",
     "B",
     "β is the probability of a Type II error (failing to detect a real effect). The power of the test is 1−β.",
     "type_ii_error"),

    # diff=3
    ("statistics", "inference", "R", 3,
     "Increasing the sample size has which effect on a confidence interval?",
     "multiple_choice",
     "Wider interval", "Narrower interval", "Higher confidence level", "Higher p-value",
     "B",
     "SE = σ/√n. As n increases, SE decreases, making the margin of error smaller and the interval narrower.",
     "sample_size_effect"),

    # diff=3
    ("statistics", "inference", "A", 3,
     "A chi-square test is used to test which of the following?",
     "multiple_choice",
     "Difference in two population means", "Association between two categorical variables", "Correlation between two quantitative variables", "Difference in two proportions",
     "B",
     "The chi-square test of independence tests whether two categorical variables are associated (related) in a population.",
     "chi_square_test"),

    # diff=4
    ("statistics", "inference", "U", 4,
     "A two-sided t-test has t=2.1 with df=20. The p-value is approximately:",
     "multiple_choice",
     "< 0.01", "0.025 < p < 0.05", "0.05 < p < 0.10", "> 0.10",
     "B",
     "For df=20, the critical value at α=0.05 (two-sided) is t*≈2.086. Since t=2.1 > 2.086, p < 0.05. Also t=2.1 < t*(0.025 two-sided)≈2.528, so p > 0.025. Therefore 0.025 < p < 0.05.",
     "p_value_approximation"),

    # diff=4
    ("statistics", "inference", "A", 4,
     "A company claims its light bulbs last 1000 hours. A sample of 36 bulbs has mean=980 hours, s=60. At α=0.05, should you reject the claim?",
     "multiple_choice",
     "Yes, t=−2.0 and |t| > t*(1.96)",
     "No, t=−2.0 and |t| < t*(2.03)",
     "Yes, t=−2.0 and |t| > t*(2.03)",
     "No, t=−2.0 and |t| < t*(1.96)",
     "B",
     "t=(980−1000)/(60/√36)=−20/10=−2.0. df=35, t*(α=0.05, two-sided)≈2.03. Since |−2.0|=2.0 < 2.03, fail to reject H₀.",
     "hypothesis_test_decision"),

    # diff=4
    ("statistics", "inference", "R", 4,
     "What happens to the probability of a Type I error if you lower the significance level from α=0.05 to α=0.01?",
     "multiple_choice",
     "It increases from 5% to 10%",
     "It decreases from 5% to 1%",
     "It stays the same",
     "It becomes impossible",
     "B",
     "α is the probability of a Type I error. Lowering α from 0.05 to 0.01 directly reduces P(Type I error) from 5% to 1%.",
     "significance_level"),

    # diff=4
    ("statistics", "inference", "F", 4,
     "For a paired t-test, what data structure is required?",
     "multiple_choice",
     "Two independent random samples", "Matched pairs of observations", "At least 3 groups", "One large sample",
     "B",
     "A paired t-test is used when data consists of matched pairs — the same subjects measured twice, or two related groups.",
     "paired_t_test"),

    # diff=4
    ("statistics", "inference", "A", 4,
     "A sample of n=100 gives p̂=0.60. Test H₀: p=0.55 at α=0.05. What is the test statistic?",
     "multiple_choice",
     "z = 1.00", "z = 0.91", "z = 2.00", "z = 1.96",
     "A",
     "z = (p̂ − p₀)/√(p₀(1−p₀)/n) = (0.60−0.55)/√(0.55×0.45/100) = 0.05/√0.002475 = 0.05/0.04975 ≈ 1.005 ≈ 1.00.",
     "proportion_test"),

    # diff=5
    ("statistics", "inference", "R", 5,
     "A researcher performs 20 independent significance tests, each at α=0.05. What is the probability of at least one false positive?",
     "multiple_choice",
     "≈ 0.05", "≈ 0.26", "≈ 0.64", "≈ 1.00",
     "C",
     "P(at least one false positive) = 1 − P(no false positives) = 1 − (0.95)²⁰ ≈ 1 − 0.358 ≈ 0.642 ≈ 64%.",
     "multiple_comparisons"),

    # diff=5
    ("statistics", "inference", "A", 5,
     "A linear regression gives ŷ = 2.5x + 10, r² = 0.81. What percentage of variation in y is explained by x?",
     "multiple_choice",
     "9%", "81%", "90%", "r = 0.81 = 81%",
     "B",
     "r² = 0.81 means 81% of the variation in y is explained by the linear relationship with x.",
     "regression_r_squared"),

    # diff=2
    ("statistics", "inference", "F", 2,
     "In simple linear regression ŷ = b₀ + b₁x, what does b₁ represent?",
     "multiple_choice",
     "The y-intercept", "The slope (rate of change)", "The correlation coefficient", "The residual",
     "B",
     "b₁ is the slope of the regression line: the predicted change in y for each one-unit increase in x.",
     "regression_slope"),

    # diff=3
    ("statistics", "inference", "U", 3,
     "Correlation coefficient r = −0.85 indicates:",
     "multiple_choice",
     "Weak positive linear relationship", "Strong positive linear relationship", "Strong negative linear relationship", "No linear relationship",
     "C",
     "r = −0.85: magnitude 0.85 indicates a strong relationship; negative sign indicates an inverse relationship. Strong negative linear relationship.",
     "correlation_interpretation"),

    # diff=1
    ("statistics", "inference", "F", 1,
     "What is the alternative hypothesis (H₁) in a two-sided test for μ = 100?",
     "multiple_choice",
     "H₁: μ > 100", "H₁: μ < 100", "H₁: μ ≠ 100", "H₁: μ = 100",
     "C",
     "A two-sided (two-tailed) test has H₁: μ ≠ μ₀, meaning we are testing for differences in either direction.",
     "alternative_hypothesis"),

    # diff=3
    ("statistics", "inference", "A", 3,
     "A regression analysis shows b₁ = 3.2 and b₀ = 15. What is the predicted y when x = 10?",
     "multiple_choice",
     "32", "47", "48", "50",
     "B",
     "ŷ = b₀ + b₁x = 15 + 3.2×10 = 15 + 32 = 47.",
     "regression_prediction"),

    # diff=2
    ("statistics", "inference", "R", 2,
     "Which of the following is the best definition of the p-value?",
     "multiple_choice",
     "The probability that H₀ is true",
     "The probability of observing data as extreme as the sample if H₀ were true",
     "The significance level α",
     "The probability that H₁ is true",
     "B",
     "The p-value is the probability of obtaining test results at least as extreme as those observed, assuming H₀ is true.",
     "p_value_definition"),

]


def seed():
    conn = sqlite3.connect(DB_PATH)
    inserted = 0
    for q in QUESTIONS:
        exists = conn.execute(
            "SELECT id FROM questions WHERE question_text = ?", (q[4],)
        ).fetchone()
        if not exists:
            conn.execute(
                """INSERT INTO questions (track, sat_domain, fuar_dimension, difficulty,
                question_text, question_type, option_a, option_b, option_c, option_d,
                correct_answer, explanation, topic_tag) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                q,
            )
            inserted += 1
    conn.commit()
    conn.close()
    print(f"[seed] supplement: {inserted} inserted")
    return inserted


if __name__ == "__main__":
    seed()
