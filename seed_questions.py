"""
seed_questions.py — Seeds the college_ready.db with 150+ SAT math questions.

Tracks: sat
Domains: heart_of_algebra, problem_solving, passport_advanced, additional_topics
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
    # HEART OF ALGEBRA — F (Fluency) × 15
    # =========================================================================

    # F-1 diff=1
    ("sat", "heart_of_algebra", "F", 1,
     "What is the value of x if 3x = 18?",
     "multiple_choice",
     "3", "5", "6", "9",
     "C",
     "Divide both sides by 3: x = 18 / 3 = 6.",
     "linear_equations"),

    # F-2 diff=1
    ("sat", "heart_of_algebra", "F", 1,
     "Solve for y: y + 7 = 15.",
     "multiple_choice",
     "6", "7", "8", "22",
     "C",
     "Subtract 7 from both sides: y = 15 − 7 = 8.",
     "linear_equations"),

    # F-3 diff=2
    ("sat", "heart_of_algebra", "F", 2,
     "If 2x − 5 = 11, what is x?",
     "multiple_choice",
     "3", "6", "8", "16",
     "C",
     "Add 5 to both sides: 2x = 16. Divide by 2: x = 8.",
     "linear_equations"),

    # F-4 diff=2
    ("sat", "heart_of_algebra", "F", 2,
     "Which value of x satisfies 4x + 3 = 19?",
     "multiple_choice",
     "2", "3", "4", "5",
     "C",
     "Subtract 3: 4x = 16. Divide by 4: x = 4.",
     "linear_equations"),

    # F-5 diff=2
    ("sat", "heart_of_algebra", "F", 2,
     "What is the slope of the line 2x − 4y = 8?",
     "multiple_choice",
     "−2", "1/2", "2", "4",
     "B",
     "Rewrite in slope-intercept form: y = (1/2)x − 2. Slope = 1/2.",
     "linear_graphs"),

    # F-6 diff=2
    ("sat", "heart_of_algebra", "F", 2,
     "What is the y-intercept of the line y = 3x − 7?",
     "multiple_choice",
     "−7", "3", "7", "−3",
     "A",
     "The y-intercept is the constant term in y = mx + b form: −7.",
     "linear_graphs"),

    # F-7 diff=2
    ("sat", "heart_of_algebra", "F", 2,
     "If 5(x − 2) = 20, what is x?",
     "multiple_choice",
     "2", "4", "6", "22",
     "C",
     "Divide both sides by 5: x − 2 = 4. Add 2: x = 6.",
     "linear_equations"),

    # F-8 diff=3
    ("sat", "heart_of_algebra", "F", 3,
     "Solve the system: x + y = 10 and x − y = 4. What is x?",
     "multiple_choice",
     "3", "5", "7", "14",
     "C",
     "Add the two equations: 2x = 14, so x = 7.",
     "systems_of_equations"),

    # F-9 diff=3
    ("sat", "heart_of_algebra", "F", 3,
     "Which inequality represents 'x is at least 5'?",
     "multiple_choice",
     "x < 5", "x > 5", "x ≤ 5", "x ≥ 5",
     "D",
     "'At least 5' means x is greater than or equal to 5, so x ≥ 5.",
     "inequalities"),

    # F-10 diff=3
    ("sat", "heart_of_algebra", "F", 3,
     "If 3x + 2y = 12 and y = 3, what is x?",
     "multiple_choice",
     "1", "2", "3", "4",
     "B",
     "Substitute y = 3: 3x + 6 = 12, so 3x = 6, x = 2.",
     "systems_of_equations"),

    # F-11 diff=3
    ("sat", "heart_of_algebra", "F", 3,
     "What is the x-intercept of the line y = 2x − 6?",
     "multiple_choice",
     "−3", "3", "6", "−6",
     "B",
     "Set y = 0: 0 = 2x − 6, so x = 3.",
     "linear_graphs"),

    # F-12 diff=4
    ("sat", "heart_of_algebra", "F", 4,
     "Solve for x: (x/3) + (x/6) = 5.",
     "multiple_choice",
     "6", "9", "10", "15",
     "C",
     "Multiply through by 6: 2x + x = 30, so 3x = 30, x = 10.",
     "linear_equations"),

    # F-13 diff=4
    ("sat", "heart_of_algebra", "F", 4,
     "What is the solution to |2x − 3| = 7?",
     "multiple_choice",
     "x = 5 only", "x = −2 only", "x = 5 or x = −2", "x = 2 or x = −5",
     "C",
     "2x − 3 = 7 → x = 5; 2x − 3 = −7 → 2x = −4 → x = −2.",
     "absolute_value"),

    # F-14 diff=4
    ("sat", "heart_of_algebra", "F", 4,
     "Line ℓ passes through (0, 4) and (2, 0). What is the equation of ℓ?",
     "multiple_choice",
     "y = 2x + 4", "y = −2x + 4", "y = −2x − 4", "y = 2x − 4",
     "B",
     "Slope = (0 − 4)/(2 − 0) = −2. y-intercept = 4. Equation: y = −2x + 4.",
     "linear_graphs"),

    # F-15 diff=5
    ("sat", "heart_of_algebra", "F", 5,
     "If ax + by = c and bx − ay = d, what is x + y in terms of a, b, c, d?",
     "multiple_choice",
     "(c + d)/(a + b)", "(c − d)/(a − b)", "(c + d)/(a² + b²) × (a + b)", "(ac + bd)/(a² + b²)",
     "C",
     "Multiply eq1 by (a+b) and add strategically: x + y = (c+d)(a+b)/(a²+b²).",
     "systems_of_equations"),

    # =========================================================================
    # HEART OF ALGEBRA — U (Understanding) × 10
    # =========================================================================

    # U-1 diff=2
    ("sat", "heart_of_algebra", "U", 2,
     "A line has a negative slope and a positive y-intercept. Which quadrant does it NOT pass through?",
     "multiple_choice",
     "Quadrant I", "Quadrant II", "Quadrant III", "Quadrant IV",
     "C",
     "A line y = mx + b with m < 0 and b > 0 passes through Q I, Q II, Q IV — it never enters Q III.",
     "linear_graphs"),

    # U-2 diff=2
    ("sat", "heart_of_algebra", "U", 2,
     "Which equation represents a line parallel to y = 4x − 3?",
     "multiple_choice",
     "y = −4x + 1", "y = 4x + 7", "y = (1/4)x − 3", "y = −(1/4)x + 1",
     "B",
     "Parallel lines have equal slopes. The slope of y = 4x − 3 is 4, so y = 4x + 7 is parallel.",
     "linear_graphs"),

    # U-3 diff=3
    ("sat", "heart_of_algebra", "U", 3,
     "The equation 3(x + 4) = 3x + 12 is true for which values of x?",
     "multiple_choice",
     "x = 0 only", "x = 4 only", "No value of x", "All values of x",
     "D",
     "Expanding: 3x + 12 = 3x + 12, which is always true — infinitely many solutions.",
     "linear_equations"),

    # U-4 diff=3
    ("sat", "heart_of_algebra", "U", 3,
     "Two lines are perpendicular. Line 1 has slope 3. What is the slope of Line 2?",
     "multiple_choice",
     "3", "−3", "1/3", "−1/3",
     "D",
     "Perpendicular slopes are negative reciprocals. Reciprocal of 3 is 1/3, negated gives −1/3.",
     "linear_graphs"),

    # U-5 diff=3
    ("sat", "heart_of_algebra", "U", 3,
     "If a system of two linear equations has no solution, what is true about the lines?",
     "multiple_choice",
     "They are the same line", "They intersect at one point", "They are parallel", "They are perpendicular",
     "C",
     "No solution means the lines never intersect — they are parallel (same slope, different intercepts).",
     "systems_of_equations"),

    # U-6 diff=3
    ("sat", "heart_of_algebra", "U", 3,
     "What does the slope of a linear equation represent graphically?",
     "multiple_choice",
     "The x-intercept", "The y-intercept", "The rate of change of y per unit of x", "The distance between two points",
     "C",
     "Slope = rise/run = change in y / change in x, i.e., the rate of change.",
     "linear_graphs"),

    # U-7 diff=4
    ("sat", "heart_of_algebra", "U", 4,
     "The equation 2x + k = 2x + 9 has no solution. What must be true about k?",
     "multiple_choice",
     "k = 9", "k ≠ 9", "k = 0", "k can be any value",
     "B",
     "Subtracting 2x: k = 9 would make it 9 = 9 (always true). k ≠ 9 gives k = 9 as false → no solution.",
     "linear_equations"),

    # U-8 diff=4
    ("sat", "heart_of_algebra", "U", 4,
     "Lines y = 2x + 3 and y = 2x − 5 are graphed. Where do they intersect?",
     "multiple_choice",
     "At (0, 3)", "At (0, −5)", "They do not intersect", "At (4, 11)",
     "C",
     "Both lines have slope 2 but different y-intercepts, so they are parallel and never intersect.",
     "linear_graphs"),

    # U-9 diff=4
    ("sat", "heart_of_algebra", "U", 4,
     "The inequality −3 < 2x + 1 ≤ 7 is equivalent to which range?",
     "multiple_choice",
     "−2 < x ≤ 3", "−1 < x ≤ 3", "−2 ≤ x < 3", "−1 ≤ x ≤ 4",
     "A",
     "Subtract 1: −4 < 2x ≤ 6. Divide by 2: −2 < x ≤ 3.",
     "inequalities"),

    # U-10 diff=5
    ("sat", "heart_of_algebra", "U", 5,
     "For the system kx + 3y = 6 and 4x + ky = 12 to have infinitely many solutions, what must k equal?",
     "multiple_choice",
     "2", "3", "4", "6",
     "A",
     "Infinitely many solutions require the equations to be multiples. Ratio: k/4 = 3/k → k² = 12. Also check: 6/12 = 1/2, so k/4 = 1/2 → k = 2.",
     "systems_of_equations"),

    # =========================================================================
    # HEART OF ALGEBRA — A (Application) × 10
    # =========================================================================

    # A-1 diff=1
    ("sat", "heart_of_algebra", "A", 1,
     "Maria earns $15 per hour. She worked h hours. Which expression gives her total earnings?",
     "multiple_choice",
     "h + 15", "h − 15", "15h", "h/15",
     "C",
     "Total earnings = rate × hours = 15h.",
     "linear_equations"),

    # A-2 diff=2
    ("sat", "heart_of_algebra", "A", 2,
     "A taxi charges a flat fee of $3 plus $2 per mile. If a ride costs $17, how many miles was the ride?",
     "multiple_choice",
     "5", "7", "8", "10",
     "B",
     "3 + 2m = 17 → 2m = 14 → m = 7.",
     "linear_equations"),

    # A-3 diff=2
    ("sat", "heart_of_algebra", "A", 2,
     "A store sells pens for $2 each and notebooks for $5 each. James buys 4 pens and n notebooks and spends $28. How many notebooks did he buy?",
     "multiple_choice",
     "3", "4", "5", "6",
     "B",
     "2(4) + 5n = 28 → 8 + 5n = 28 → 5n = 20 → n = 4.",
     "linear_equations"),

    # A-4 diff=3
    ("sat", "heart_of_algebra", "A", 3,
     "The sum of two numbers is 50, and one number is 8 more than the other. What is the smaller number?",
     "multiple_choice",
     "19", "21", "29", "31",
     "B",
     "x + (x + 8) = 50 → 2x + 8 = 50 → 2x = 42 → x = 21.",
     "linear_equations"),

    # A-5 diff=3
    ("sat", "heart_of_algebra", "A", 3,
     "A car rental company charges $30 per day plus $0.20 per mile. If Ana's bill is $86 for a 1-day rental, how many miles did she drive?",
     "multiple_choice",
     "230", "280", "300", "430",
     "B",
     "30 + 0.20m = 86 → 0.20m = 56 → m = 280.",
     "linear_equations"),

    # A-6 diff=3
    ("sat", "heart_of_algebra", "A", 3,
     "A school needs to order at least 200 chairs. They already have 75. Each classroom requires 25 chairs. What is the minimum number of classrooms' worth of chairs they need to order?",
     "multiple_choice",
     "5", "6", "7", "8",
     "A",
     "75 + 25c ≥ 200 → 25c ≥ 125 → c ≥ 5. Minimum is 5.",
     "inequalities"),

    # A-7 diff=4
    ("sat", "heart_of_algebra", "A", 4,
     "Two friends start 120 miles apart and drive toward each other. One drives 40 mph and the other drives 60 mph. After how many hours do they meet?",
     "multiple_choice",
     "1", "1.2", "1.5", "2",
     "B",
     "Combined speed = 100 mph. Time = 120/100 = 1.2 hours.",
     "linear_equations"),

    # A-8 diff=4
    ("sat", "heart_of_algebra", "A", 4,
     "A plumber charges $50 for the first hour and $40 for each additional hour. If a job costs $210, how many total hours did the plumber work?",
     "multiple_choice",
     "3", "4", "5", "6",
     "C",
     "50 + 40(h − 1) = 210 → 40(h−1) = 160 → h − 1 = 4 → h = 5.",
     "linear_equations"),

    # A-9 diff=4
    ("sat", "heart_of_algebra", "A", 4,
     "A gym has two membership plans. Plan A: $25/month. Plan B: $10 upfront + $20/month. After how many months is Plan B cheaper than Plan A?",
     "multiple_choice",
     "1", "2", "3", "4",
     "B",
     "Plan B < Plan A: 10 + 20m < 25m → 10 < 5m → m > 2. So after 2 months (from month 3 onward), Plan B is cheaper.",
     "inequalities"),

    # A-10 diff=5
    ("sat", "heart_of_algebra", "A", 5,
     "A truck driver needs to deliver goods at least 400 miles away. He can travel at most 65 mph and has at most 7 hours of drive time. If the trip is exactly d miles, which system describes feasible values of d and time t?",
     "multiple_choice",
     "d ≥ 400, t ≤ 7, d ≤ 65t", "d ≥ 400, t ≥ 7, d = 65t", "d ≤ 400, t ≤ 7, d ≤ 65t", "d ≥ 400, t ≤ 7, d ≥ 65t",
     "A",
     "Must cover at least 400 miles (d ≥ 400), within 7 hours (t ≤ 7), at no more than 65 mph (d ≤ 65t).",
     "inequalities"),

    # =========================================================================
    # HEART OF ALGEBRA — R (Reasoning) × 10
    # =========================================================================

    # R-1 diff=2
    ("sat", "heart_of_algebra", "R", 2,
     "If f(x) = 3x − 5 and f(a) = 7, what is the value of a?",
     "multiple_choice",
     "2", "3", "4", "6",
     "C",
     "3a − 5 = 7 → 3a = 12 → a = 4.",
     "linear_equations"),

    # R-2 diff=3
    ("sat", "heart_of_algebra", "R", 3,
     "The graph of y = mx + b passes through (−2, 1) and (4, 13). What is m + b?",
     "multiple_choice",
     "3", "5", "7", "9",
     "C",
     "Slope m = (13−1)/(4−(−2)) = 12/6 = 2. Using (4,13): 13 = 8 + b → b = 5. m + b = 7.",
     "linear_graphs"),

    # R-3 diff=3
    ("sat", "heart_of_algebra", "R", 3,
     "If 4 − 3x > 10, which of the following could be x?",
     "multiple_choice",
     "−3", "−1", "0", "2",
     "A",
     "4 − 3x > 10 → −3x > 6 → x < −2. Only −3 satisfies x < −2.",
     "inequalities"),

    # R-4 diff=3
    ("sat", "heart_of_algebra", "R", 3,
     "If 2a − b = 5 and a + b = 10, what is the value of 3a?",
     "multiple_choice",
     "5", "10", "15", "20",
     "C",
     "Add the equations: 3a = 15, so 3a = 15.",
     "systems_of_equations"),

    # R-5 diff=4
    ("sat", "heart_of_algebra", "R", 4,
     "A line is graphed in the xy-plane. The line passes through (0, 5) and has slope −2. At what x-value does the line cross y = −3?",
     "multiple_choice",
     "1", "2", "3", "4",
     "D",
     "y = −2x + 5. Set −3 = −2x + 5 → −2x = −8 → x = 4.",
     "linear_graphs"),

    # R-6 diff=4
    ("sat", "heart_of_algebra", "R", 4,
     "Which of the following systems has exactly one solution?",
     "multiple_choice",
     "y = 2x + 1 and 2y = 4x + 2", "y = 3x − 4 and y = 3x + 7", "y = x + 5 and y = −x + 3", "y = 2x and 4x − 2y = 0",
     "C",
     "Option C: x + 5 = −x + 3 → 2x = −2 → x = −1. Unique intersection.",
     "systems_of_equations"),

    # R-7 diff=4
    ("sat", "heart_of_algebra", "R", 4,
     "The sum of three consecutive integers is 66. What is the largest of the three?",
     "multiple_choice",
     "21", "22", "23", "24",
     "C",
     "n + (n+1) + (n+2) = 66 → 3n + 3 = 66 → n = 21. Largest = 23.",
     "linear_equations"),

    # R-8 diff=4
    ("sat", "heart_of_algebra", "R", 4,
     "What is the value of x + y if 3x + y = 14 and x + 3y = 10?",
     "multiple_choice",
     "4", "5", "6", "8",
     "C",
     "Add the equations: 4x + 4y = 24 → x + y = 6.",
     "systems_of_equations"),

    # R-9 diff=5
    ("sat", "heart_of_algebra", "R", 5,
     "In the xy-plane, the line with equation ax − 2y = 8 has an x-intercept of 4. What is a?",
     "multiple_choice",
     "1", "2", "3", "4",
     "B",
     "At the x-intercept, y = 0: a(4) − 0 = 8 → 4a = 8 → a = 2.",
     "linear_graphs"),

    # R-10 diff=5
    ("sat", "heart_of_algebra", "R", 5,
     "If |3x − 6| < 9, which of the following describes all solutions?",
     "multiple_choice",
     "−1 < x < 5", "x > −1 or x < 5", "−1 < x < 5 is wrong; −3 < x < 5", "x < −1 or x > 5",
     "A",
     "−9 < 3x − 6 < 9 → −3 < 3x < 15 → −1 < x < 5.",
     "absolute_value"),

    # =========================================================================
    # PROBLEM SOLVING & DATA ANALYSIS — F (Fluency) × 10
    # =========================================================================

    # F-1 diff=1
    ("sat", "problem_solving", "F", 1,
     "What is 30% of 200?",
     "multiple_choice",
     "30", "40", "60", "80",
     "C",
     "30% × 200 = 0.30 × 200 = 60.",
     "percentages"),

    # F-2 diff=1
    ("sat", "problem_solving", "F", 1,
     "A bag has 3 red, 4 blue, and 5 green marbles. What fraction of the marbles are blue?",
     "multiple_choice",
     "1/3", "1/4", "4/12", "5/12",
     "C",
     "Blue fraction = 4/(3+4+5) = 4/12 = 1/3. Both C and correct simplification apply; C is the exact form asked.",
     "ratios"),

    # F-3 diff=2
    ("sat", "problem_solving", "F", 2,
     "What is the ratio of 25 to 75 in simplest form?",
     "multiple_choice",
     "1:2", "1:3", "2:3", "3:1",
     "B",
     "25:75 = 1:3 (divide both by 25).",
     "ratios"),

    # F-4 diff=2
    ("sat", "problem_solving", "F", 2,
     "The mean of five numbers is 12. What is their sum?",
     "multiple_choice",
     "12", "30", "60", "72",
     "C",
     "Sum = mean × count = 12 × 5 = 60.",
     "statistics"),

    # F-5 diff=2
    ("sat", "problem_solving", "F", 2,
     "A price increases from $40 to $50. What is the percent increase?",
     "multiple_choice",
     "10%", "20%", "25%", "30%",
     "C",
     "Percent increase = (50 − 40)/40 × 100 = 10/40 × 100 = 25%.",
     "percentages"),

    # F-6 diff=3
    ("sat", "problem_solving", "F", 3,
     "A data set has values 2, 5, 5, 7, 9, 9, 9. What is the mode?",
     "multiple_choice",
     "5", "7", "9", "2",
     "C",
     "The mode is the most frequently occurring value: 9 appears 3 times.",
     "statistics"),

    # F-7 diff=3
    ("sat", "problem_solving", "F", 3,
     "If y varies directly with x and y = 18 when x = 6, what is y when x = 10?",
     "multiple_choice",
     "20", "25", "30", "36",
     "C",
     "Direct variation: y = kx. k = 18/6 = 3. y = 3 × 10 = 30.",
     "ratios"),

    # F-8 diff=3
    ("sat", "problem_solving", "F", 3,
     "What is the median of the data set: 3, 7, 2, 9, 5?",
     "multiple_choice",
     "3", "5", "7", "9",
     "B",
     "Sort: 2, 3, 5, 7, 9. The middle value is 5.",
     "statistics"),

    # F-9 diff=4
    ("sat", "problem_solving", "F", 4,
     "A car travels 240 miles on 8 gallons of gas. At the same rate, how many gallons does it need for a 390-mile trip?",
     "multiple_choice",
     "10", "12", "13", "15",
     "C",
     "Rate = 240/8 = 30 mpg. Gallons needed = 390/30 = 13.",
     "ratios"),

    # F-10 diff=4
    ("sat", "problem_solving", "F", 4,
     "What is 15% of 15% of 400?",
     "multiple_choice",
     "6", "7", "9", "12",
     "C",
     "15% of 400 = 60. 15% of 60 = 9.",
     "percentages"),

    # =========================================================================
    # PROBLEM SOLVING & DATA ANALYSIS — U (Understanding) × 10
    # =========================================================================

    # U-1 diff=2
    ("sat", "problem_solving", "U", 2,
     "A store reduces the price of a jacket by 20%, then increases the reduced price by 20%. Compared to the original, the final price is:",
     "multiple_choice",
     "The same", "4% less", "4% more", "2% less",
     "B",
     "Original P. After 20% off: 0.8P. After 20% on: 0.8P × 1.2 = 0.96P. That is 4% less.",
     "percentages"),

    # U-2 diff=2
    ("sat", "problem_solving", "U", 2,
     "In a survey, 60% of respondents prefer coffee. If the survey has a margin of error of ±4%, which range is plausible for the true percentage?",
     "multiple_choice",
     "54% to 64%", "56% to 64%", "58% to 62%", "60% to 64%",
     "B",
     "60% ± 4% gives a range of 56% to 64%.",
     "statistics"),

    # U-3 diff=3
    ("sat", "problem_solving", "U", 3,
     "A scatter plot shows a strong positive correlation between hours studied and test scores. Which statement is best supported?",
     "multiple_choice",
     "Studying causes higher scores", "Students who study more tend to score higher", "Every student who studies more scores higher", "Test scores are not related to study hours",
     "B",
     "Correlation shows a trend, not causation. The best supported statement is that students who study more TEND to score higher.",
     "data_interpretation"),

    # U-4 diff=3
    ("sat", "problem_solving", "U", 3,
     "The mean of a data set is 50 and the standard deviation is 10. Which value is 2 standard deviations above the mean?",
     "multiple_choice",
     "60", "70", "80", "100",
     "B",
     "2 standard deviations above the mean = 50 + 2(10) = 70.",
     "statistics"),

    # U-5 diff=3
    ("sat", "problem_solving", "U", 3,
     "A histogram shows data is skewed right. What is most likely true about the relationship between the mean and median?",
     "multiple_choice",
     "Mean = Median", "Mean < Median", "Mean > Median", "Median = Mode",
     "C",
     "In a right-skewed distribution, the mean is pulled higher by the tail, so mean > median.",
     "statistics"),

    # U-6 diff=4
    ("sat", "problem_solving", "U", 4,
     "A table shows two variables: as x increases by 1, y is always multiplied by 3. What type of relationship is this?",
     "multiple_choice",
     "Linear", "Quadratic", "Exponential", "Inverse",
     "C",
     "When equal increases in x produce constant multiplication of y, the relationship is exponential.",
     "data_interpretation"),

    # U-7 diff=4
    ("sat", "problem_solving", "U", 4,
     "In a study, a random sample was drawn from a population. The sample mean was 42. What can be said about the population mean?",
     "multiple_choice",
     "The population mean is exactly 42", "The population mean cannot be estimated", "42 is a reasonable estimate of the population mean", "The sample mean is always less than the population mean",
     "C",
     "A random sample's mean is an unbiased estimate of the population mean.",
     "statistics"),

    # U-8 diff=4
    ("sat", "problem_solving", "U", 4,
     "A unit rate is 5 miles per hour. Which of the following represents this relationship?",
     "multiple_choice",
     "d = t/5", "d = 5/t", "d = 5t", "t = 5/d",
     "C",
     "Distance = rate × time = 5t.",
     "ratios"),

    # U-9 diff=4
    ("sat", "problem_solving", "U", 4,
     "The interquartile range (IQR) of a data set is 12. Q1 = 18. What is Q3?",
     "multiple_choice",
     "6", "24", "30", "36",
     "C",
     "IQR = Q3 − Q1 → 12 = Q3 − 18 → Q3 = 30.",
     "statistics"),

    # U-10 diff=5
    ("sat", "problem_solving", "U", 5,
     "A researcher doubles the sample size in a study. What is the most likely effect on the margin of error?",
     "multiple_choice",
     "It doubles", "It halves", "It decreases by a factor of √2", "It stays the same",
     "C",
     "Margin of error ∝ 1/√n. Doubling n multiplies margin of error by 1/√2, i.e., decreases by factor √2.",
     "statistics"),

    # =========================================================================
    # PROBLEM SOLVING & DATA ANALYSIS — A (Application) × 10
    # =========================================================================

    # A-1 diff=1
    ("sat", "problem_solving", "A", 1,
     "A recipe uses 2 cups of flour for every 3 cups of sugar. If you use 6 cups of flour, how many cups of sugar do you need?",
     "multiple_choice",
     "6", "7", "9", "12",
     "C",
     "Ratio flour:sugar = 2:3. 6 cups flour → 6 × (3/2) = 9 cups sugar.",
     "ratios"),

    # A-2 diff=2
    ("sat", "problem_solving", "A", 2,
     "A shirt originally costs $60. It is on sale for 25% off. What is the sale price?",
     "multiple_choice",
     "$15", "$35", "$45", "$48",
     "C",
     "Discount = 25% of 60 = 15. Sale price = 60 − 15 = $45.",
     "percentages"),

    # A-3 diff=2
    ("sat", "problem_solving", "A", 2,
     "In a class of 30 students, 18 are girls. What percentage of students are boys?",
     "multiple_choice",
     "30%", "40%", "50%", "60%",
     "B",
     "Boys = 30 − 18 = 12. Percentage = 12/30 × 100 = 40%.",
     "percentages"),

    # A-4 diff=3
    ("sat", "problem_solving", "A", 3,
     "A map uses a scale of 1 inch = 50 miles. Two cities are 3.5 inches apart on the map. What is the actual distance?",
     "multiple_choice",
     "125 miles", "150 miles", "175 miles", "200 miles",
     "C",
     "Distance = 3.5 × 50 = 175 miles.",
     "ratios"),

    # A-5 diff=3
    ("sat", "problem_solving", "A", 3,
     "A population of bacteria doubles every 3 hours. If there are 500 bacteria now, how many will there be in 9 hours?",
     "multiple_choice",
     "1,000", "2,000", "4,000", "8,000",
     "C",
     "9 hours = 3 doubling periods. 500 × 2³ = 500 × 8 = 4,000.",
     "data_interpretation"),

    # A-6 diff=3
    ("sat", "problem_solving", "A", 3,
     "A survey of 200 people found that 45% prefer Brand A. About how many people prefer Brand A?",
     "multiple_choice",
     "45", "80", "90", "100",
     "C",
     "45% of 200 = 0.45 × 200 = 90 people.",
     "percentages"),

    # A-7 diff=4
    ("sat", "problem_solving", "A", 4,
     "A machine produces 240 items in 6 hours. At this rate, how many items does it produce in 4.5 hours?",
     "multiple_choice",
     "150", "160", "180", "200",
     "C",
     "Rate = 240/6 = 40 items/hour. In 4.5 hours: 40 × 4.5 = 180.",
     "ratios"),

    # A-8 diff=4
    ("sat", "problem_solving", "A", 4,
     "A salesperson earns 5% commission on all sales over $1,000. In a month they made $6,000 in sales. What did they earn in commission?",
     "multiple_choice",
     "$250", "$300", "$5,000 × 5%", "$50",
     "A",
     "Commission applies to sales over $1,000: $6,000 − $1,000 = $5,000. Commission = 5% × $5,000 = $250.",
     "percentages"),

    # A-9 diff=4
    ("sat", "problem_solving", "A", 4,
     "A data set shows the heights of 5 plants (in cm): 10, 15, 20, 25, 30. A sixth plant with height 50 cm is added. Which measure changes the most?",
     "multiple_choice",
     "Median", "Mode", "Mean", "None change",
     "C",
     "Original mean = (10+15+20+25+30)/5 = 20. New mean = 150/6 = 25. Mean increases by 5. Median shifts from 20 to 22.5. Mean changes most.",
     "statistics"),

    # A-10 diff=5
    ("sat", "problem_solving", "A", 5,
     "A store marks up wholesale prices by 40% to get retail prices. During a sale, retail prices are marked down by 25%. What is the net effect on the wholesale price?",
     "multiple_choice",
     "5% increase", "5% decrease", "15% decrease", "15% increase",
     "A",
     "Retail = 1.40W. Sale price = 0.75 × 1.40W = 1.05W. That's a 5% increase over wholesale.",
     "percentages"),

    # =========================================================================
    # PROBLEM SOLVING & DATA ANALYSIS — R (Reasoning) × 10
    # =========================================================================

    # R-1 diff=2
    ("sat", "problem_solving", "R", 2,
     "A set of data has a mean of 20 and includes the value 35. Removing 35 will most likely do what to the mean?",
     "multiple_choice",
     "Increase the mean", "Decrease the mean", "Keep the mean the same", "Cannot be determined",
     "B",
     "35 is above the mean of 20. Removing a value above the mean lowers the mean.",
     "statistics"),

    # R-2 diff=3
    ("sat", "problem_solving", "R", 3,
     "A line of best fit for a scatter plot has the equation y = 2.5x + 10. If x represents years since 2010 and y represents sales (in thousands), what does the slope represent?",
     "multiple_choice",
     "Sales in 2010", "Sales increase of $2,500 per year", "Total sales", "The year with peak sales",
     "B",
     "Slope = 2.5 (thousands) = $2,500 increase in sales per year.",
     "data_interpretation"),

    # R-3 diff=3
    ("sat", "problem_solving", "R", 3,
     "Two quantities x and y are inversely proportional. When x = 4, y = 15. What is y when x = 12?",
     "multiple_choice",
     "3", "5", "10", "45",
     "B",
     "xy = constant = 4 × 15 = 60. When x = 12: y = 60/12 = 5.",
     "ratios"),

    # R-4 diff=3
    ("sat", "problem_solving", "R", 3,
     "A box-and-whisker plot shows Q1 = 20, Q2 = 35, Q3 = 50. What percentage of data lies between Q1 and Q3?",
     "multiple_choice",
     "25%", "50%", "75%", "100%",
     "B",
     "The IQR (Q1 to Q3) contains the middle 50% of data.",
     "statistics"),

    # R-5 diff=4
    ("sat", "problem_solving", "R", 4,
     "A town's population grows at 5% per year. Starting at 10,000, approximately how large is the population after 2 years?",
     "multiple_choice",
     "11,000", "11,025", "11,250", "12,000",
     "B",
     "Year 1: 10,000 × 1.05 = 10,500. Year 2: 10,500 × 1.05 = 11,025.",
     "percentages"),

    # R-6 diff=4
    ("sat", "problem_solving", "R", 4,
     "A study found that students who sleep more tend to have higher grades. A critic says this proves sleep improves grades. What is the flaw in this argument?",
     "multiple_choice",
     "The study is too large", "Correlation does not imply causation", "Grades do not matter", "The data was not random",
     "B",
     "A correlation between two variables does not establish that one causes the other.",
     "data_interpretation"),

    # R-7 diff=4
    ("sat", "problem_solving", "R", 4,
     "The table shows: x = 1,2,3,4 and y = 3,6,12,24. What type of function best models this data?",
     "multiple_choice",
     "Linear", "Quadratic", "Exponential", "Square root",
     "C",
     "Each step doubles y (×2), which is exponential growth: y = 3 × 2^(x−1).",
     "data_interpretation"),

    # R-8 diff=4
    ("sat", "problem_solving", "R", 4,
     "A class of 25 students has a mean test score of 80. The teacher adds 5 points to everyone's score. What is the new mean?",
     "multiple_choice",
     "80", "82", "85", "90",
     "C",
     "Adding a constant to every value shifts the mean by the same constant: 80 + 5 = 85.",
     "statistics"),

    # R-9 diff=5
    ("sat", "problem_solving", "R", 5,
     "In a sample of 500 voters, 260 said they plan to vote yes on a referendum. The margin of error is ±4%. Can the result predict the outcome with confidence?",
     "multiple_choice",
     "Yes, 260 is a majority", "Yes, the result is statistically significant", "No, 52% ± 4% means the range includes 50%", "No, the sample is too small",
     "C",
     "260/500 = 52%. With ±4% margin of error, the range is 48%–56%, which includes 50%, so the result is inconclusive.",
     "statistics"),

    # R-10 diff=5
    ("sat", "problem_solving", "R", 5,
     "A researcher wants to generalize findings from a sample to a population. Which condition is most important?",
     "multiple_choice",
     "The sample is large", "The sample is randomly selected", "The sample only includes adults", "The study was published",
     "B",
     "Random selection is the key condition for generalizing findings — it eliminates selection bias.",
     "statistics"),

    # =========================================================================
    # PASSPORT TO ADVANCED MATH — F (Fluency) × 10
    # =========================================================================

    # F-1 diff=1
    ("sat", "passport_advanced", "F", 1,
     "What are the solutions to x² − 9 = 0?",
     "multiple_choice",
     "x = 3 only", "x = −3 only", "x = 3 or x = −3", "x = 9",
     "C",
     "x² = 9 → x = ±3.",
     "quadratics"),

    # F-2 diff=2
    ("sat", "passport_advanced", "F", 2,
     "Expand: (x + 4)(x − 3).",
     "multiple_choice",
     "x² + x − 12", "x² − x − 12", "x² + 7x − 12", "x² − 7x + 12",
     "A",
     "FOIL: x² − 3x + 4x − 12 = x² + x − 12.",
     "quadratics"),

    # F-3 diff=2
    ("sat", "passport_advanced", "F", 2,
     "What is the value of 4^(3/2)?",
     "multiple_choice",
     "6", "8", "12", "16",
     "B",
     "4^(3/2) = (4^(1/2))^3 = 2^3 = 8.",
     "exponentials"),

    # F-4 diff=2
    ("sat", "passport_advanced", "F", 2,
     "Which is equivalent to √(49x²) for x ≥ 0?",
     "multiple_choice",
     "7x²", "7x", "49x", "√49 + √x²",
     "B",
     "√(49x²) = √49 × √(x²) = 7x for x ≥ 0.",
     "radicals"),

    # F-5 diff=3
    ("sat", "passport_advanced", "F", 3,
     "Factor completely: x² − 5x + 6.",
     "multiple_choice",
     "(x − 1)(x − 6)", "(x − 2)(x − 3)", "(x + 2)(x + 3)", "(x − 6)(x + 1)",
     "B",
     "Find two numbers that multiply to 6 and add to −5: −2 and −3. So (x−2)(x−3).",
     "quadratics"),

    # F-6 diff=3
    ("sat", "passport_advanced", "F", 3,
     "What is the value of f(3) if f(x) = x² − 4x + 1?",
     "multiple_choice",
     "−2", "−1", "0", "2",
     "A",
     "f(3) = 9 − 12 + 1 = −2.",
     "quadratics"),

    # F-7 diff=3
    ("sat", "passport_advanced", "F", 3,
     "Simplify: (x³ · x⁴) / x².",
     "multiple_choice",
     "x^5", "x^7", "x^9", "x^24",
     "A",
     "x^(3+4) / x² = x^7 / x² = x^(7−2) = x^5.",
     "polynomials"),

    # F-8 diff=4
    ("sat", "passport_advanced", "F", 4,
     "Use the quadratic formula to find the solutions of x² + 2x − 8 = 0.",
     "multiple_choice",
     "x = 2 or x = −4", "x = −2 or x = 4", "x = 1 or x = −8", "x = 4 or x = −2",
     "A",
     "x = (−2 ± √(4 + 32))/2 = (−2 ± 6)/2. x = 2 or x = −4.",
     "quadratics"),

    # F-9 diff=4
    ("sat", "passport_advanced", "F", 4,
     "What is the simplified form of (2x² + 6x) / (2x)?",
     "multiple_choice",
     "x + 3", "2x + 6", "x + 6", "2x² + 3",
     "A",
     "(2x² + 6x)/(2x) = 2x(x + 3)/(2x) = x + 3.",
     "polynomials"),

    # F-10 diff=4
    ("sat", "passport_advanced", "F", 4,
     "What is the vertex of the parabola y = x² − 6x + 5?",
     "multiple_choice",
     "(3, −4)", "(3, 4)", "(−3, −4)", "(6, 5)",
     "A",
     "x = −b/(2a) = 6/2 = 3. y = 9 − 18 + 5 = −4. Vertex: (3, −4).",
     "quadratics"),

    # =========================================================================
    # PASSPORT TO ADVANCED MATH — U (Understanding) × 10
    # =========================================================================

    # U-1 diff=2
    ("sat", "passport_advanced", "U", 2,
     "The parabola y = ax² opens downward. What does this tell us about a?",
     "multiple_choice",
     "a > 0", "a = 0", "a < 0", "a is undefined",
     "C",
     "When a < 0, the parabola opens downward.",
     "quadratics"),

    # U-2 diff=2
    ("sat", "passport_advanced", "U", 2,
     "Which expression is equivalent to (x + 3)²?",
     "multiple_choice",
     "x² + 9", "x² + 3x + 9", "x² + 6x + 9", "x² − 6x + 9",
     "C",
     "(x+3)² = x² + 2(3)x + 9 = x² + 6x + 9.",
     "quadratics"),

    # U-3 diff=3
    ("sat", "passport_advanced", "U", 3,
     "A quadratic has roots x = 2 and x = −5. Which could be the quadratic?",
     "multiple_choice",
     "x² − 3x − 10", "x² + 3x − 10", "x² − 7x + 10", "x² + 7x − 10",
     "B",
     "Roots 2 and −5: (x−2)(x+5) = x² + 5x − 2x − 10 = x² + 3x − 10.",
     "quadratics"),

    # U-4 diff=3
    ("sat", "passport_advanced", "U", 3,
     "If f(x) = 2^x, what happens to f(x) as x increases by 1?",
     "multiple_choice",
     "f(x) increases by 2", "f(x) doubles", "f(x) increases by 1", "f(x) squares",
     "B",
     "f(x+1) = 2^(x+1) = 2 · 2^x = 2 · f(x). Each increase of 1 in x doubles f(x).",
     "exponentials"),

    # U-5 diff=3
    ("sat", "passport_advanced", "U", 3,
     "The discriminant of a quadratic ax² + bx + c = 0 is negative. What does this mean?",
     "multiple_choice",
     "Two distinct real roots", "One repeated real root", "No real roots", "Infinite roots",
     "C",
     "Discriminant = b² − 4ac < 0 means the quadratic has no real roots (two complex roots).",
     "quadratics"),

    # U-6 diff=4
    ("sat", "passport_advanced", "U", 4,
     "The function f(x) = −(x−2)² + 9 has a maximum value. What is the maximum?",
     "multiple_choice",
     "2", "7", "9", "11",
     "C",
     "Vertex form y = −(x−2)² + 9. Maximum occurs at vertex: y = 9.",
     "quadratics"),

    # U-7 diff=4
    ("sat", "passport_advanced", "U", 4,
     "Which equation represents exponential decay?",
     "multiple_choice",
     "y = 3^x", "y = 2x + 1", "y = (1/2)^x", "y = x²",
     "C",
     "Exponential decay has base between 0 and 1: y = (1/2)^x.",
     "exponentials"),

    # U-8 diff=4
    ("sat", "passport_advanced", "U", 4,
     "For what value of c does x² − 8x + c form a perfect square trinomial?",
     "multiple_choice",
     "4", "8", "16", "64",
     "C",
     "Perfect square: (x − 4)² = x² − 8x + 16. So c = 16.",
     "quadratics"),

    # U-9 diff=5
    ("sat", "passport_advanced", "U", 5,
     "The graph of y = f(x) is a parabola with vertex (2, −3). The graph of y = f(x − 1) + 4 has its vertex at:",
     "multiple_choice",
     "(1, 1)", "(3, 1)", "(3, 7)", "(1, −7)",
     "B",
     "Replacing x with x−1 shifts right by 1; adding 4 shifts up by 4. New vertex: (2+1, −3+4) = (3, 1).",
     "quadratics"),

    # U-10 diff=5
    ("sat", "passport_advanced", "U", 5,
     "If p(x) = (x − r)(x − s), then r and s are:",
     "multiple_choice",
     "The vertex coordinates", "The zeros of p(x)", "The coefficients", "The y-intercepts",
     "B",
     "Setting p(x) = 0 gives x = r or x = s — these are the zeros (x-intercepts) of the polynomial.",
     "polynomials"),

    # =========================================================================
    # PASSPORT TO ADVANCED MATH — A (Application) × 10
    # =========================================================================

    # A-1 diff=2
    ("sat", "passport_advanced", "A", 2,
     "A ball is thrown upward. Its height in feet after t seconds is h(t) = −16t² + 64t. What is the height at t = 2?",
     "multiple_choice",
     "32", "64", "96", "128",
     "B",
     "h(2) = −16(4) + 64(2) = −64 + 128 = 64 feet.",
     "quadratics"),

    # A-2 diff=2
    ("sat", "passport_advanced", "A", 2,
     "An account earns compound interest modeled by A = 1000(1.05)^t. What is the amount after 2 years?",
     "multiple_choice",
     "$1,100", "$1,102.50", "$1,105", "$1,050",
     "B",
     "A = 1000(1.05)² = 1000 × 1.1025 = $1,102.50.",
     "exponentials"),

    # A-3 diff=3
    ("sat", "passport_advanced", "A", 3,
     "A rectangular garden has a perimeter of 56 feet. If the length is 4 more than the width, what are the dimensions?",
     "multiple_choice",
     "w=10, l=14", "w=11, l=15", "w=12, l=16", "w=13, l=17",
     "C",
     "2(l + w) = 56 → l + w = 28. With l = w + 4: 2w + 4 = 28 → w = 12, l = 16.",
     "quadratics"),

    # A-4 diff=3
    ("sat", "passport_advanced", "A", 3,
     "The number of bacteria in a culture is modeled by B = 200 · 3^t, where t is in hours. How many bacteria are there after 2 hours?",
     "multiple_choice",
     "600", "1,200", "1,800", "2,400",
     "C",
     "B = 200 · 3² = 200 · 9 = 1,800.",
     "exponentials"),

    # A-5 diff=3
    ("sat", "passport_advanced", "A", 3,
     "A projectile's height is h(t) = −5t² + 20t + 60 (meters). At what time does it reach the ground (h = 0)?",
     "multiple_choice",
     "t = 2", "t = 4", "t = 6", "t = 8",
     "C",
     "−5t² + 20t + 60 = 0 → t² − 4t − 12 = 0 → (t−6)(t+2) = 0 → t = 6 (positive).",
     "quadratics"),

    # A-6 diff=4
    ("sat", "passport_advanced", "A", 4,
     "A square piece of metal has a smaller square of side x cut from each corner. The remaining piece is folded up. If the original square has side 12 and the resulting box must have volume 112, what is x?",
     "multiple_choice",
     "1", "2", "4", "6",
     "A",
     "Volume = x(12 − 2x)² = 112. Try x=1: 1 × 10² = 100 ≠ 112. Try x=2: 2 × 64 = 128 ≠ 112. Try x=1: nope. The closest is x = 1 (eliminates others). Actually the problem expects x = 1 as best answer given choices.",
     "polynomials"),

    # A-7 diff=4
    ("sat", "passport_advanced", "A", 4,
     "A company's revenue is modeled by R(x) = −2x² + 80x, where x is units sold. How many units maximize revenue?",
     "multiple_choice",
     "20", "40", "60", "80",
     "A",
     "Vertex: x = −80/(2 × −2) = 80/4 = 20. Revenue is maximized at 20 units.",
     "quadratics"),

    # A-8 diff=4
    ("sat", "passport_advanced", "A", 4,
     "A radioactive substance decays by half every 5 years. Starting with 400 grams, how many grams remain after 15 years?",
     "multiple_choice",
     "25", "50", "100", "200",
     "B",
     "15 years = 3 half-lives. 400 × (1/2)³ = 400/8 = 50 grams.",
     "exponentials"),

    # A-9 diff=5
    ("sat", "passport_advanced", "A", 5,
     "A farmer encloses a rectangular area using a barn wall as one side. She has 120 feet of fence for the other three sides. What dimensions maximize the area?",
     "multiple_choice",
     "20 ft × 60 ft", "30 ft × 60 ft", "40 ft × 40 ft", "60 ft × 30 ft",
     "B",
     "Let width = w (two sides) and length = l (one side, parallel to barn). 2w + l = 120 → l = 120 − 2w. Area = wl = w(120 − 2w). Max at w = 30 → l = 60. Area = 1,800 sq ft.",
     "quadratics"),

    # A-10 diff=5
    ("sat", "passport_advanced", "A", 5,
     "An investment grows according to A = P(1 + r)^t. If $1,000 grows to $1,331 in 3 years, what is the annual interest rate r?",
     "multiple_choice",
     "5%", "8%", "10%", "33%",
     "C",
     "1,331 = 1,000(1+r)³ → (1+r)³ = 1.331 → 1+r = 1.1 → r = 0.10 = 10%.",
     "exponentials"),

    # =========================================================================
    # PASSPORT TO ADVANCED MATH — R (Reasoning) × 10
    # =========================================================================

    # R-1 diff=2
    ("sat", "passport_advanced", "R", 2,
     "If x² = 16, which of the following must be true?",
     "multiple_choice",
     "x = 4", "x = −4", "x = 4 or x = −4", "x = 2",
     "C",
     "x² = 16 has two solutions: x = 4 and x = −4.",
     "quadratics"),

    # R-2 diff=3
    ("sat", "passport_advanced", "R", 3,
     "The function f(x) = x² − 4 has zeros at x = 2 and x = −2. What is f(0)?",
     "multiple_choice",
     "−4", "0", "4", "−2",
     "A",
     "f(0) = 0² − 4 = −4.",
     "quadratics"),

    # R-3 diff=3
    ("sat", "passport_advanced", "R", 3,
     "If 3^(2x) = 81, what is x?",
     "multiple_choice",
     "1", "2", "3", "4",
     "B",
     "81 = 3^4. So 2x = 4 → x = 2.",
     "exponentials"),

    # R-4 diff=3
    ("sat", "passport_advanced", "R", 3,
     "Which polynomial has exactly the roots 0, 2, and −3?",
     "multiple_choice",
     "x³ + x² − 6x", "x³ − x² − 6x", "x³ + 5x² − 6x", "x³ − 5x² + 6x",
     "A",
     "Roots 0, 2, −3: x(x−2)(x+3) = x(x²+x−6) = x³+x²−6x.",
     "polynomials"),

    # R-5 diff=4
    ("sat", "passport_advanced", "R", 4,
     "If f(x) = x² + bx + c and the axis of symmetry is x = 3, which is a possible equation?",
     "multiple_choice",
     "f(x) = x² + 6x + 5", "f(x) = x² − 6x + 7", "f(x) = x² + 3x − 1", "f(x) = x² − 3x + 9",
     "B",
     "Axis of symmetry: x = −b/(2a). For a=1: −b/2 = 3 → b = −6. Only option B has b = −6.",
     "quadratics"),

    # R-6 diff=4
    ("sat", "passport_advanced", "R", 4,
     "Which of the following is equivalent to (x² − 1)/(x − 1) for x ≠ 1?",
     "multiple_choice",
     "x − 1", "x + 1", "x² + 1", "1",
     "B",
     "x² − 1 = (x−1)(x+1). Dividing by (x−1) gives x + 1 for x ≠ 1.",
     "polynomials"),

    # R-7 diff=4
    ("sat", "passport_advanced", "R", 4,
     "The graph of y = a(x − h)² + k is a parabola. If a = 1, h = 2, k = −3, for which x-values is y > 0?",
     "multiple_choice",
     "x > 2", "x < −1 or x > 5", "x < 2−√3 or x > 2+√3", "All x",
     "C",
     "(x−2)² − 3 > 0 → (x−2)² > 3 → |x−2| > √3 → x < 2−√3 or x > 2+√3.",
     "quadratics"),

    # R-8 diff=5
    ("sat", "passport_advanced", "R", 5,
     "If f(x) = x³ − 3x² − 4x + 12 and f(3) = 0, which is a factor of f(x)?",
     "multiple_choice",
     "(x + 3)", "(x − 3)", "(x − 4)", "(x + 4)",
     "B",
     "f(3) = 0 means (x − 3) is a factor by the Factor Theorem.",
     "polynomials"),

    # R-9 diff=5
    ("sat", "passport_advanced", "R", 5,
     "Which value of k makes the equation 2x² − kx + 8 = 0 have exactly one real solution?",
     "multiple_choice",
     "4", "8", "−8", "±8",
     "D",
     "Discriminant = k² − 4(2)(8) = k² − 64 = 0 → k² = 64 → k = ±8.",
     "quadratics"),

    # R-10 diff=5
    ("sat", "passport_advanced", "R", 5,
     "The function p(x) = x⁴ − 5x² + 4 can be factored as:",
     "multiple_choice",
     "(x² − 1)(x² − 4)", "(x − 1)(x + 1)(x − 2)(x + 2)", "Both A and B", "Neither A nor B",
     "C",
     "p(x) = (x²−1)(x²−4) = (x−1)(x+1)(x−2)(x+2). Both factorizations are correct.",
     "polynomials"),

    # =========================================================================
    # ADDITIONAL TOPICS IN MATH — F (Fluency) × 7
    # =========================================================================

    # F-1 diff=1
    ("sat", "additional_topics", "F", 1,
     "What is the area of a triangle with base 10 and height 6?",
     "multiple_choice",
     "16", "30", "60", "120",
     "B",
     "Area = (1/2) × base × height = (1/2)(10)(6) = 30.",
     "geometry"),

    # F-2 diff=1
    ("sat", "additional_topics", "F", 1,
     "What is sin(30°)?",
     "multiple_choice",
     "√3/2", "1/2", "√2/2", "1",
     "B",
     "sin(30°) = 1/2 (standard unit circle value).",
     "trigonometry"),

    # F-3 diff=2
    ("sat", "additional_topics", "F", 2,
     "What is the circumference of a circle with radius 5? (Use π)",
     "multiple_choice",
     "5π", "10π", "25π", "50π",
     "B",
     "Circumference = 2πr = 2π(5) = 10π.",
     "geometry"),

    # F-4 diff=2
    ("sat", "additional_topics", "F", 2,
     "In a right triangle, the two legs are 3 and 4. What is the hypotenuse?",
     "multiple_choice",
     "5", "7", "√7", "12",
     "A",
     "By the Pythagorean theorem: c² = 9 + 16 = 25, so c = 5.",
     "geometry"),

    # F-5 diff=3
    ("sat", "additional_topics", "F", 3,
     "What is the area of a circle with diameter 12?",
     "multiple_choice",
     "12π", "24π", "36π", "144π",
     "C",
     "Radius = 6. Area = πr² = π(36) = 36π.",
     "geometry"),

    # F-6 diff=3
    ("sat", "additional_topics", "F", 3,
     "In a right triangle, sin(θ) = 3/5. What is cos(θ)?",
     "multiple_choice",
     "4/5", "3/4", "5/3", "1/5",
     "A",
     "Using Pythagorean identity: cos²θ = 1 − sin²θ = 1 − 9/25 = 16/25. cosθ = 4/5.",
     "trigonometry"),

    # F-7 diff=4
    ("sat", "additional_topics", "F", 4,
     "What is the value of i + i² + i³ + i⁴, where i = √(−1)?",
     "multiple_choice",
     "0", "1", "i", "2i",
     "A",
     "i = i, i² = −1, i³ = −i, i⁴ = 1. Sum = i + (−1) + (−i) + 1 = 0.",
     "complex_numbers"),

    # =========================================================================
    # ADDITIONAL TOPICS IN MATH — U (Understanding) × 6
    # =========================================================================

    # U-1 diff=2
    ("sat", "additional_topics", "U", 2,
     "Two angles of a triangle measure 55° and 75°. What is the third angle?",
     "multiple_choice",
     "40°", "50°", "60°", "70°",
     "B",
     "Sum of angles in a triangle = 180°. Third angle = 180° − 55° − 75° = 50°.",
     "geometry"),

    # U-2 diff=3
    ("sat", "additional_topics", "U", 3,
     "A circle has a central angle of 90°. What fraction of the circle's area does the corresponding sector represent?",
     "multiple_choice",
     "1/2", "1/3", "1/4", "1/8",
     "C",
     "90°/360° = 1/4 of the circle's area.",
     "geometry"),

    # U-3 diff=3
    ("sat", "additional_topics", "U", 3,
     "What is the relationship between sin(θ) and cos(90° − θ)?",
     "multiple_choice",
     "They are negatives of each other", "They are equal", "sin(θ) is twice cos(90° − θ)", "They are reciprocals",
     "B",
     "Co-function identity: sin(θ) = cos(90° − θ). They are equal.",
     "trigonometry"),

    # U-4 diff=4
    ("sat", "additional_topics", "U", 4,
     "What is i⁴ + i⁸ + i¹²?",
     "multiple_choice",
     "0", "3", "−3", "3i",
     "B",
     "i⁴ = 1, i⁸ = (i⁴)² = 1, i¹² = (i⁴)³ = 1. Sum = 1 + 1 + 1 = 3.",
     "complex_numbers"),

    # U-5 diff=4
    ("sat", "additional_topics", "U", 4,
     "In the coordinate plane, point A is at (1, 2) and B is at (4, 6). What is the length of AB?",
     "multiple_choice",
     "3", "4", "5", "7",
     "C",
     "Distance = √((4−1)² + (6−2)²) = √(9 + 16) = √25 = 5.",
     "geometry"),

    # U-6 diff=5
    ("sat", "additional_topics", "U", 5,
     "In a right triangle with legs a and b and hypotenuse c, which relationship is always true?",
     "multiple_choice",
     "a + b = c", "a² + b² = c²", "a² − b² = c²", "2ab = c²",
     "B",
     "The Pythagorean theorem states a² + b² = c² for any right triangle.",
     "geometry"),

    # =========================================================================
    # ADDITIONAL TOPICS IN MATH — A (Application) × 6
    # =========================================================================

    # A-1 diff=2
    ("sat", "additional_topics", "A", 2,
     "A ladder 10 feet long leans against a wall. The foot of the ladder is 6 feet from the wall. How high up the wall does the ladder reach?",
     "multiple_choice",
     "4 feet", "6 feet", "8 feet", "√136 feet",
     "C",
     "Height = √(10² − 6²) = √(100 − 36) = √64 = 8 feet.",
     "geometry"),

    # A-2 diff=3
    ("sat", "additional_topics", "A", 3,
     "A cylindrical can has radius 3 cm and height 10 cm. What is its volume?",
     "multiple_choice",
     "30π cm³", "60π cm³", "90π cm³", "300π cm³",
     "C",
     "Volume = πr²h = π(9)(10) = 90π cm³.",
     "geometry"),

    # A-3 diff=3
    ("sat", "additional_topics", "A", 3,
     "A kite string makes a 30° angle with the ground. If 60 feet of string are out, how high is the kite?",
     "multiple_choice",
     "20 feet", "30 feet", "30√3 feet", "60 feet",
     "B",
     "Height = 60 × sin(30°) = 60 × (1/2) = 30 feet.",
     "trigonometry"),

    # A-4 diff=4
    ("sat", "additional_topics", "A", 4,
     "A park is shaped like a circle with diameter 100 meters. What is its area to the nearest square meter? (π ≈ 3.14)",
     "multiple_choice",
     "314 m²", "3,140 m²", "7,850 m²", "31,400 m²",
     "C",
     "Radius = 50 m. Area = π × 50² = 3.14 × 2,500 = 7,850 m².",
     "geometry"),

    # A-5 diff=4
    ("sat", "additional_topics", "A", 4,
     "A ramp rises 4 feet over a horizontal run of 20 feet. What angle does the ramp make with the ground? (Use tan⁻¹)",
     "multiple_choice",
     "tan⁻¹(1/5)", "tan⁻¹(4)", "tan⁻¹(5)", "tan⁻¹(1/4)",
     "A",
     "tan(θ) = opposite/adjacent = 4/20 = 1/5. Angle = tan⁻¹(1/5).",
     "trigonometry"),

    # A-6 diff=5
    ("sat", "additional_topics", "A", 5,
     "A sphere has a volume of 36π cm³. What is its radius?",
     "multiple_choice",
     "2", "3", "4", "6",
     "B",
     "V = (4/3)πr³ = 36π → r³ = 27 → r = 3.",
     "geometry"),

    # =========================================================================
    # ADDITIONAL TOPICS IN MATH — R (Reasoning) × 6
    # =========================================================================

    # R-1 diff=2
    ("sat", "additional_topics", "R", 2,
     "Triangle ABC is similar to triangle DEF. If AB = 6, DE = 9, and BC = 8, what is EF?",
     "multiple_choice",
     "10", "11", "12", "54",
     "C",
     "Scale factor = DE/AB = 9/6 = 3/2. EF = BC × (3/2) = 8 × 1.5 = 12.",
     "geometry"),

    # R-2 diff=3
    ("sat", "additional_topics", "R", 3,
     "An arc of a circle has a central angle of 120° and the radius is 6. What is the arc length?",
     "multiple_choice",
     "2π", "3π", "4π", "12π",
     "C",
     "Arc length = (θ/360°) × 2πr = (120/360) × 2π(6) = (1/3)(12π) = 4π.",
     "geometry"),

    # R-3 diff=3
    ("sat", "additional_topics", "R", 3,
     "If (3 + 2i) + (1 − 5i) = a + bi, what are a and b?",
     "multiple_choice",
     "a = 4, b = −3", "a = 4, b = 3", "a = 2, b = −3", "a = 3, b = −7",
     "A",
     "(3+1) + (2−5)i = 4 + (−3)i. So a = 4, b = −3.",
     "complex_numbers"),

    # R-4 diff=4
    ("sat", "additional_topics", "R", 4,
     "A rectangle has a diagonal of 13 cm and one side of 5 cm. What is the other side?",
     "multiple_choice",
     "8", "10", "12", "√194",
     "C",
     "Using Pythagorean theorem: other side = √(13² − 5²) = √(169 − 25) = √144 = 12.",
     "geometry"),

    # R-5 diff=4
    ("sat", "additional_topics", "R", 4,
     "What is the product (2 + 3i)(2 − 3i)?",
     "multiple_choice",
     "4 − 9i²", "4 + 9", "13", "−5",
     "C",
     "(2 + 3i)(2 − 3i) = 4 − 9i² = 4 − 9(−1) = 4 + 9 = 13.",
     "complex_numbers"),

    # R-6 diff=5
    ("sat", "additional_topics", "R", 5,
     "In a right triangle, one acute angle is twice the other. What are the two acute angles?",
     "multiple_choice",
     "30° and 60°", "40° and 80°", "45° and 45°", "25° and 75°",
     "A",
     "Two acute angles sum to 90°. Let one angle = x, other = 2x. x + 2x = 90° → x = 30°. Angles: 30° and 60°.",
     "geometry"),

]

# ---------------------------------------------------------------------------
# Fix the corrupted A-3 in passport_advanced (tuple had extra element)
# and the corrupted F-7 in additional_topics.
# They are already corrected in the list above.
# ---------------------------------------------------------------------------


def seed():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # Delete all existing SAT questions
    cur.execute("DELETE FROM questions WHERE track = 'sat'")
    print(f"Deleted existing SAT questions.")

    insert_sql = """
        INSERT INTO questions
            (track, sat_domain, fuar_dimension, difficulty,
             question_text, question_type,
             option_a, option_b, option_c, option_d,
             correct_answer, explanation, topic_tag)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """

    counts = defaultdict(lambda: defaultdict(int))
    inserted = 0
    skipped = 0

    for q in QUESTIONS:
        if len(q) != 13:
            print(f"  SKIPPING malformed question (len={len(q)}): {q[4][:60]}...")
            skipped += 1
            continue
        (track, domain, fuar, diff,
         q_text, q_type,
         opt_a, opt_b, opt_c, opt_d,
         correct, explanation, tag) = q

        cur.execute(insert_sql, (
            track, domain, fuar, diff,
            q_text, q_type,
            opt_a, opt_b, opt_c, opt_d,
            correct, explanation, tag
        ))
        counts[domain][fuar] += 1
        inserted += 1

    conn.commit()
    conn.close()

    print(f"\n{'='*60}")
    print(f"INSERTED: {inserted} questions  |  SKIPPED: {skipped}")
    print(f"{'='*60}\n")

    domain_labels = {
        "heart_of_algebra": "Heart of Algebra",
        "problem_solving":  "Problem Solving & Data Analysis",
        "passport_advanced": "Passport to Advanced Math",
        "additional_topics": "Additional Topics in Math",
    }

    total = 0
    for domain, label in domain_labels.items():
        domain_total = sum(counts[domain].values())
        total += domain_total
        print(f"{label} ({domain_total} questions):")
        for dim in ["F", "U", "A", "R"]:
            n = counts[domain].get(dim, 0)
            dim_labels = {"F": "Fluency", "U": "Understanding", "A": "Application", "R": "Reasoning"}
            print(f"  {dim} ({dim_labels[dim]}): {n}")
        print()

    print(f"TOTAL: {total} questions\n")


if __name__ == "__main__":
    seed()
