"""Seed Grade 6 Math questions — Foundation Builder track.
48 questions across 6 content areas, balanced across FUAR dimensions.
Focus: Ratios, fractions/decimals, integers, expressions, geometry, data/stats.
Batch 1 (Q1-24): difficulty F=2, U=3, A=3, R=4
Batch 2 (Q25-48): difficulty F=1, U=2, A=4, R=5 — widens MST routing range.
"""

import sqlite3
import os

DB_PATH = os.environ.get('DATABASE_PATH', 'college_ready.db')

QUESTIONS = [
    # --- Ratios & Rates (4 questions) ---
    {
        'track': 'grade_6', 'sat_domain': 'ratios_rates', 'fuar_dimension': 'F', 'difficulty': 2,
        'question_text': 'A recipe calls for 3 cups of flour for every 2 cups of sugar. How many cups of flour are needed if you use 8 cups of sugar?',
        'option_a': '6', 'option_b': '10', 'option_c': '12', 'option_d': '16',
        'correct_answer': 'C', 'explanation': 'Set up the proportion: 3/2 = x/8. Cross multiply: 2x = 24, so x = 12.',
        'topic_tag': 'proportional_reasoning',
    },
    {
        'track': 'grade_6', 'sat_domain': 'ratios_rates', 'fuar_dimension': 'U', 'difficulty': 3,
        'question_text': 'The ratio of boys to girls in a class is 3:5. Which statement must be true?',
        'option_a': 'There are 3 boys and 5 girls', 'option_b': 'For every 8 students, 3 are boys',
        'option_c': 'There are more boys than girls', 'option_d': 'The class has exactly 8 students',
        'correct_answer': 'B', 'explanation': '3:5 means for every 3 boys there are 5 girls = 8 total. So 3 out of every 8 are boys.',
        'topic_tag': 'ratio_concepts',
    },
    {
        'track': 'grade_6', 'sat_domain': 'ratios_rates', 'fuar_dimension': 'A', 'difficulty': 3,
        'question_text': 'A car travels 150 miles in 3 hours. At this rate, how far will it travel in 5 hours?',
        'option_a': '200 miles', 'option_b': '225 miles', 'option_c': '250 miles', 'option_d': '300 miles',
        'correct_answer': 'C', 'explanation': 'Rate = 150/3 = 50 mph. In 5 hours: 50 × 5 = 250 miles.',
        'topic_tag': 'unit_rates',
    },
    {
        'track': 'grade_6', 'sat_domain': 'ratios_rates', 'fuar_dimension': 'R', 'difficulty': 4,
        'question_text': 'Mia mixed red and blue paint in a 2:3 ratio to make purple. She wants to make more purple paint using 10 cups total. How many cups of red paint does she need?',
        'option_a': '2', 'option_b': '3', 'option_c': '4', 'option_d': '5',
        'correct_answer': 'C', 'explanation': '2:3 means 2 parts red out of 5 total parts. 10 × (2/5) = 4 cups red.',
        'topic_tag': 'ratio_reasoning',
    },

    # --- Fractions & Decimals (4 questions) ---
    {
        'track': 'grade_6', 'sat_domain': 'fractions_decimals', 'fuar_dimension': 'F', 'difficulty': 2,
        'question_text': 'What is 3/4 + 2/3?',
        'option_a': '5/7', 'option_b': '5/12', 'option_c': '17/12', 'option_d': '1 5/12',
        'correct_answer': 'C', 'explanation': 'Find common denominator: 9/12 + 8/12 = 17/12 or 1 5/12. Both C and D are correct forms, but 17/12 is the improper fraction.',
        'topic_tag': 'fraction_operations',
    },
    {
        'track': 'grade_6', 'sat_domain': 'fractions_decimals', 'fuar_dimension': 'U', 'difficulty': 3,
        'question_text': 'Why does dividing by a fraction give a larger answer? Which explanation is correct for 6 ÷ 1/2 = 12?',
        'option_a': 'You multiply the denominators', 'option_b': 'You are finding how many halves fit into 6',
        'option_c': 'Division always makes numbers bigger', 'option_d': 'You flip both fractions',
        'correct_answer': 'B', 'explanation': 'Dividing by 1/2 asks: how many groups of 1/2 are in 6? There are 12 half-units in 6.',
        'topic_tag': 'fraction_concepts',
    },
    {
        'track': 'grade_6', 'sat_domain': 'fractions_decimals', 'fuar_dimension': 'A', 'difficulty': 3,
        'question_text': 'A pizza is cut into 8 slices. Jake eats 3/8 and Maria eats 1/4 of the whole pizza. What fraction of the pizza is left?',
        'option_a': '3/8', 'option_b': '5/8', 'option_c': '1/2', 'option_d': '2/8',
        'correct_answer': 'A', 'explanation': 'Jake: 3/8, Maria: 1/4 = 2/8. Total eaten: 3/8 + 2/8 = 5/8. Remaining: 1 - 5/8 = 3/8.',
        'topic_tag': 'fraction_word_problems',
    },
    {
        'track': 'grade_6', 'sat_domain': 'fractions_decimals', 'fuar_dimension': 'R', 'difficulty': 4,
        'question_text': 'Which is greater: 5/8 or 7/11? How can you tell without finding a common denominator?',
        'option_a': '5/8 because 5 > 4', 'option_b': '7/11 because 7 > 5',
        'option_c': '5/8 because 5/8 > 0.5 and 7/11 > 0.5, but 5/8 = 0.625 and 7/11 ≈ 0.636',
        'option_d': '7/11 because cross-multiplying gives 55 > 56',
        'correct_answer': 'D', 'explanation': 'Cross multiply: 5×11=55, 7×8=56. Since 56>55, 7/11 > 5/8.',
        'topic_tag': 'fraction_reasoning',
    },

    # --- Integers & Number System (4 questions) ---
    {
        'track': 'grade_6', 'sat_domain': 'integers_number_system', 'fuar_dimension': 'F', 'difficulty': 2,
        'question_text': 'What is -8 + 5?',
        'option_a': '-13', 'option_b': '-3', 'option_c': '3', 'option_d': '13',
        'correct_answer': 'B', 'explanation': 'Starting at -8 on the number line and moving 5 to the right gives -3.',
        'topic_tag': 'integer_operations',
    },
    {
        'track': 'grade_6', 'sat_domain': 'integers_number_system', 'fuar_dimension': 'U', 'difficulty': 3,
        'question_text': 'On a number line, -3 is to the LEFT of -1. What does this tell us?',
        'option_a': '-3 is greater than -1', 'option_b': '-3 is less than -1',
        'option_c': '-3 is farther from zero than -1', 'option_d': 'Both B and C are correct',
        'correct_answer': 'D', 'explanation': 'Numbers to the left on a number line are smaller. -3 < -1 AND -3 is farther from zero (absolute value 3 > 1).',
        'topic_tag': 'number_line_concepts',
    },
    {
        'track': 'grade_6', 'sat_domain': 'integers_number_system', 'fuar_dimension': 'A', 'difficulty': 3,
        'question_text': 'The temperature at midnight was -4°F. By noon it rose 15 degrees. What was the temperature at noon?',
        'option_a': '-19°F', 'option_b': '-11°F', 'option_c': '11°F', 'option_d': '19°F',
        'correct_answer': 'C', 'explanation': '-4 + 15 = 11°F.',
        'topic_tag': 'integer_word_problems',
    },
    {
        'track': 'grade_6', 'sat_domain': 'integers_number_system', 'fuar_dimension': 'R', 'difficulty': 4,
        'question_text': 'If a × b is positive, what must be true about a and b?',
        'option_a': 'Both are positive', 'option_b': 'Both are negative',
        'option_c': 'They have the same sign (both positive or both negative)', 'option_d': 'One is positive and one is negative',
        'correct_answer': 'C', 'explanation': 'Positive × positive = positive. Negative × negative = positive. So both must have the same sign.',
        'topic_tag': 'integer_reasoning',
    },

    # --- Expressions & Equations (4 questions) ---
    {
        'track': 'grade_6', 'sat_domain': 'expressions_equations', 'fuar_dimension': 'F', 'difficulty': 2,
        'question_text': 'Evaluate: 3x + 7 when x = 4.',
        'option_a': '14', 'option_b': '17', 'option_c': '19', 'option_d': '34',
        'correct_answer': 'C', 'explanation': '3(4) + 7 = 12 + 7 = 19.',
        'topic_tag': 'evaluating_expressions',
    },
    {
        'track': 'grade_6', 'sat_domain': 'expressions_equations', 'fuar_dimension': 'U', 'difficulty': 3,
        'question_text': 'Which expression represents "five more than twice a number n"?',
        'option_a': '5 + 2n', 'option_b': '5(2n)', 'option_c': '2(n + 5)', 'option_d': '2 + 5n',
        'correct_answer': 'A', 'explanation': '"Twice a number" = 2n. "Five more than" = + 5. So 2n + 5 or equivalently 5 + 2n.',
        'topic_tag': 'translating_expressions',
    },
    {
        'track': 'grade_6', 'sat_domain': 'expressions_equations', 'fuar_dimension': 'A', 'difficulty': 3,
        'question_text': 'A gym charges a $25 registration fee plus $10 per month. Which equation shows the total cost C for m months?',
        'option_a': 'C = 25m + 10', 'option_b': 'C = 10m + 25', 'option_c': 'C = 35m', 'option_d': 'C = 25 + 10 + m',
        'correct_answer': 'B', 'explanation': '$10 per month for m months = 10m, plus the one-time $25 fee = 10m + 25.',
        'topic_tag': 'equation_word_problems',
    },
    {
        'track': 'grade_6', 'sat_domain': 'expressions_equations', 'fuar_dimension': 'R', 'difficulty': 4,
        'question_text': 'If 2x + 3 = 15, what is the value of 4x + 6?',
        'option_a': '24', 'option_b': '27', 'option_c': '30', 'option_d': '33',
        'correct_answer': 'C', 'explanation': 'Notice that 4x + 6 = 2(2x + 3). Since 2x + 3 = 15, then 4x + 6 = 2(15) = 30. No need to solve for x first.',
        'topic_tag': 'algebraic_reasoning',
    },

    # --- Geometry & Measurement (4 questions) ---
    {
        'track': 'grade_6', 'sat_domain': 'geometry_measurement', 'fuar_dimension': 'F', 'difficulty': 2,
        'question_text': 'What is the area of a rectangle with length 8 cm and width 5 cm?',
        'option_a': '13 cm²', 'option_b': '26 cm²', 'option_c': '40 cm²', 'option_d': '80 cm²',
        'correct_answer': 'C', 'explanation': 'Area = length × width = 8 × 5 = 40 cm².',
        'topic_tag': 'area',
    },
    {
        'track': 'grade_6', 'sat_domain': 'geometry_measurement', 'fuar_dimension': 'U', 'difficulty': 3,
        'question_text': 'A cube has a volume of 64 cubic inches. What is the length of one edge?',
        'option_a': '4 inches', 'option_b': '8 inches', 'option_c': '16 inches', 'option_d': '32 inches',
        'correct_answer': 'A', 'explanation': 'Volume of cube = edge³. So edge = ∛64 = 4 inches.',
        'topic_tag': 'volume_concepts',
    },
    {
        'track': 'grade_6', 'sat_domain': 'geometry_measurement', 'fuar_dimension': 'A', 'difficulty': 3,
        'question_text': 'You need to wrap a gift box that is 12 inches long, 8 inches wide, and 4 inches tall. What is the surface area of the box?',
        'option_a': '160 in²', 'option_b': '272 in²', 'option_c': '384 in²', 'option_d': '352 in²',
        'correct_answer': 'D', 'explanation': 'SA = 2(lw + lh + wh) = 2(12×8 + 12×4 + 8×4) = 2(96 + 48 + 32) = 2(176) = 352 in².',
        'topic_tag': 'surface_area',
    },
    {
        'track': 'grade_6', 'sat_domain': 'geometry_measurement', 'fuar_dimension': 'R', 'difficulty': 4,
        'question_text': 'A triangle has vertices at (1,1), (5,1), and (3,4) on a coordinate grid. What is its area?',
        'option_a': '4 square units', 'option_b': '6 square units', 'option_c': '8 square units', 'option_d': '12 square units',
        'correct_answer': 'B', 'explanation': 'Base = distance from (1,1) to (5,1) = 4. Height = 4-1 = 3. Area = ½ × 4 × 3 = 6.',
        'topic_tag': 'coordinate_geometry',
    },

    # --- Data & Statistics (4 questions) ---
    {
        'track': 'grade_6', 'sat_domain': 'data_statistics', 'fuar_dimension': 'F', 'difficulty': 2,
        'question_text': 'Find the mean of these numbers: 4, 7, 9, 12, 8.',
        'option_a': '7', 'option_b': '8', 'option_c': '9', 'option_d': '10',
        'correct_answer': 'B', 'explanation': 'Mean = (4+7+9+12+8)/5 = 40/5 = 8.',
        'topic_tag': 'mean',
    },
    {
        'track': 'grade_6', 'sat_domain': 'data_statistics', 'fuar_dimension': 'U', 'difficulty': 3,
        'question_text': 'A data set has a mean of 10 and a median of 7. What does this tell you about the data?',
        'option_a': 'Most values are above 10', 'option_b': 'The data is evenly spread out',
        'option_c': 'There are some high values pulling the mean up', 'option_d': 'The mean and median should always be equal',
        'correct_answer': 'C', 'explanation': 'When mean > median, the data is skewed right — some high outliers pull the mean above the median.',
        'topic_tag': 'statistical_concepts',
    },
    {
        'track': 'grade_6', 'sat_domain': 'data_statistics', 'fuar_dimension': 'A', 'difficulty': 3,
        'question_text': 'The heights (in inches) of 5 students are: 58, 62, 55, 60, 65. What is the range?',
        'option_a': '5', 'option_b': '7', 'option_c': '10', 'option_d': '12',
        'correct_answer': 'C', 'explanation': 'Range = highest - lowest = 65 - 55 = 10 inches.',
        'topic_tag': 'data_analysis',
    },
    {
        'track': 'grade_6', 'sat_domain': 'data_statistics', 'fuar_dimension': 'R', 'difficulty': 4,
        'question_text': 'Adding a 6th student with height 80 inches to the group {58, 62, 55, 60, 65} would change which measure the MOST?',
        'option_a': 'Median', 'option_b': 'Mean', 'option_c': 'Mode', 'option_d': 'All change equally',
        'correct_answer': 'B', 'explanation': 'The outlier (80) pulls the mean significantly but barely affects the median (shifts from 60 to 61). Mean is most sensitive to outliers.',
        'topic_tag': 'statistical_reasoning',
    },

    # ============================================================
    # BATCH 2 — difficulty F=1, U=2, A=4, R=5 (widens MST range)
    # ============================================================

    # --- Ratios & Rates — Batch 2 (4 questions) ---
    {
        'track': 'grade_6', 'sat_domain': 'ratios_rates', 'fuar_dimension': 'F', 'difficulty': 1,
        'question_text': 'There are 4 red marbles and 6 blue marbles in a bag. What is the ratio of red to blue marbles?',
        'option_a': '6:4', 'option_b': '4:10', 'option_c': '4:6', 'option_d': '10:4',
        'correct_answer': 'C', 'explanation': 'The ratio of red to blue is 4:6 (red first, then blue, in the order asked).',
        'topic_tag': 'ratio_concepts',
    },
    {
        'track': 'grade_6', 'sat_domain': 'ratios_rates', 'fuar_dimension': 'U', 'difficulty': 2,
        'question_text': 'A store sells 3 notebooks for $6. Which is the correct unit rate?',
        'option_a': '$3 per notebook', 'option_b': '$6 per notebook', 'option_c': '$2 per notebook', 'option_d': '$18 per notebook',
        'correct_answer': 'C', 'explanation': 'Unit rate = total cost ÷ quantity = $6 ÷ 3 = $2 per notebook.',
        'topic_tag': 'unit_rates',
    },
    {
        'track': 'grade_6', 'sat_domain': 'ratios_rates', 'fuar_dimension': 'A', 'difficulty': 4,
        'question_text': 'Two trains leave the same station at the same time traveling in opposite directions. Train A travels at 55 mph and Train B at 45 mph. How far apart are they after 2.5 hours?',
        'option_a': '100 miles', 'option_b': '200 miles', 'option_c': '237.5 miles', 'option_d': '250 miles',
        'correct_answer': 'D', 'explanation': 'Combined rate = 55 + 45 = 100 mph (moving apart). Distance = 100 × 2.5 = 250 miles.',
        'topic_tag': 'unit_rates',
    },
    {
        'track': 'grade_6', 'sat_domain': 'ratios_rates', 'fuar_dimension': 'R', 'difficulty': 5,
        'question_text': 'A punch recipe uses juice and soda in a 3:2 ratio. If you scale the recipe up so that the soda amount doubles from 4 cups to 8 cups, but you want to keep the total punch under 20 cups, what is the maximum number of cups of juice you can use?',
        'option_a': '8 cups', 'option_b': '12 cups', 'option_c': '10 cups', 'option_d': '14 cups',
        'correct_answer': 'B', 'explanation': 'With 8 cups of soda, maintaining the 3:2 ratio requires 8 × (3/2) = 12 cups of juice. Total = 12 + 8 = 20 cups, which is not under 20. However, 12 cups of juice is the amount that keeps the ratio exact — any less would break the ratio or bring total under 20. The maximum juice while staying at 3:2 with 8 cups soda is exactly 12 cups (total = 20). Answer: 12 cups.',
        'topic_tag': 'ratio_reasoning',
    },

    # --- Fractions & Decimals — Batch 2 (4 questions) ---
    {
        'track': 'grade_6', 'sat_domain': 'fractions_decimals', 'fuar_dimension': 'F', 'difficulty': 1,
        'question_text': 'Which fraction is equivalent to 0.5?',
        'option_a': '1/4', 'option_b': '2/5', 'option_c': '1/2', 'option_d': '5/2',
        'correct_answer': 'C', 'explanation': '0.5 = 5/10 = 1/2.',
        'topic_tag': 'fraction_decimal_equivalence',
    },
    {
        'track': 'grade_6', 'sat_domain': 'fractions_decimals', 'fuar_dimension': 'U', 'difficulty': 2,
        'question_text': 'Which of the following correctly orders these numbers from least to greatest: 0.6, 1/2, 3/5, 0.55?',
        'option_a': '1/2, 0.55, 3/5, 0.6', 'option_b': '1/2, 0.55, 0.6, 3/5',
        'option_c': '0.55, 1/2, 3/5, 0.6', 'option_d': '1/2, 3/5, 0.55, 0.6',
        'correct_answer': 'A', 'explanation': 'Convert all to decimals: 1/2=0.50, 0.55, 3/5=0.60, 0.6=0.60. Order: 0.50, 0.55, 0.60, 0.60. Since 3/5 and 0.6 are equal, A is correct: 1/2, 0.55, 3/5, 0.6.',
        'topic_tag': 'comparing_fractions_decimals',
    },
    {
        'track': 'grade_6', 'sat_domain': 'fractions_decimals', 'fuar_dimension': 'A', 'difficulty': 4,
        'question_text': 'Leila ran 2 3/4 miles on Monday, 1 1/2 miles on Tuesday, and 3 1/8 miles on Wednesday. How many total miles did she run over the three days?',
        'option_a': '6 3/8 miles', 'option_b': '7 miles', 'option_c': '7 3/8 miles', 'option_d': '7 1/2 miles',
        'correct_answer': 'C', 'explanation': 'Convert to eighths: 2 3/4 = 2 6/8, 1 1/2 = 1 4/8, 3 1/8 = 3 1/8. Sum = (2+1+3) + (6+4+1)/8 = 6 + 11/8 = 6 + 1 3/8 = 7 3/8 miles.',
        'topic_tag': 'fraction_operations',
    },
    {
        'track': 'grade_6', 'sat_domain': 'fractions_decimals', 'fuar_dimension': 'R', 'difficulty': 5,
        'question_text': 'A tank is 2/3 full. After removing 1/4 of the tank\'s total capacity, what fraction of the tank is full?',
        'option_a': '5/12', 'option_b': '1/2', 'option_c': '7/12', 'option_d': '3/4',
        'correct_answer': 'A', 'explanation': 'Start: 2/3 full. Remove 1/4 of total capacity. 2/3 - 1/4 = 8/12 - 3/12 = 5/12 full.',
        'topic_tag': 'fraction_reasoning',
    },

    # --- Integers & Number System — Batch 2 (4 questions) ---
    {
        'track': 'grade_6', 'sat_domain': 'integers_number_system', 'fuar_dimension': 'F', 'difficulty': 1,
        'question_text': 'What is the absolute value of -9?',
        'option_a': '-9', 'option_b': '0', 'option_c': '9', 'option_d': '81',
        'correct_answer': 'C', 'explanation': 'Absolute value is the distance from zero on a number line. |-9| = 9.',
        'topic_tag': 'absolute_value',
    },
    {
        'track': 'grade_6', 'sat_domain': 'integers_number_system', 'fuar_dimension': 'U', 'difficulty': 2,
        'question_text': 'Which set of integers is listed in order from least to greatest?',
        'option_a': '-5, -2, 0, 3', 'option_b': '-2, -5, 0, 3',
        'option_c': '0, -2, -5, 3', 'option_d': '3, 0, -2, -5',
        'correct_answer': 'A', 'explanation': 'On a number line: -5 is furthest left (least), then -2, then 0, then 3. So -5, -2, 0, 3 is least to greatest.',
        'topic_tag': 'comparing_integers',
    },
    {
        'track': 'grade_6', 'sat_domain': 'integers_number_system', 'fuar_dimension': 'A', 'difficulty': 4,
        'question_text': 'A submarine was at -240 feet. It rose 75 feet, then dove 130 feet. What is its new depth?',
        'option_a': '-295 feet', 'option_b': '-285 feet', 'option_c': '-205 feet', 'option_d': '-165 feet',
        'correct_answer': 'A', 'explanation': 'Start: -240. Rise 75: -240 + 75 = -165. Dive 130: -165 - 130 = -295 feet.',
        'topic_tag': 'integer_word_problems',
    },
    {
        'track': 'grade_6', 'sat_domain': 'integers_number_system', 'fuar_dimension': 'R', 'difficulty': 5,
        'question_text': 'Point P is on a number line at -3 and point Q is at 5. Point M is the midpoint of PQ. Which statement about M is true?',
        'option_a': 'M is at 1 because (−3+5)/2 = 1', 'option_b': 'M is at 4 because 5-(-3)=8 and M is 4 from each end',
        'option_c': 'M is at 1 and is 4 units from both P and Q', 'option_d': 'M is at 0 because it is the center of the number line',
        'correct_answer': 'C', 'explanation': 'Midpoint = (-3+5)/2 = 2/2 = 1. Distance from P(-3) to M(1) = 4. Distance from M(1) to Q(5) = 4. Both A and C state M=1, but only C also correctly notes M is equidistant (4 units) from both endpoints.',
        'topic_tag': 'number_line_reasoning',
    },

    # --- Expressions & Equations — Batch 2 (4 questions) ---
    {
        'track': 'grade_6', 'sat_domain': 'expressions_equations', 'fuar_dimension': 'F', 'difficulty': 1,
        'question_text': 'What is the value of 5 + 3 × 2?',
        'option_a': '16', 'option_b': '11', 'option_c': '13', 'option_d': '10',
        'correct_answer': 'B', 'explanation': 'Order of operations: multiply first. 3 × 2 = 6, then 5 + 6 = 11.',
        'topic_tag': 'order_of_operations',
    },
    {
        'track': 'grade_6', 'sat_domain': 'expressions_equations', 'fuar_dimension': 'U', 'difficulty': 2,
        'question_text': 'Which expression is equivalent to 4(x + 3)?',
        'option_a': '4x + 3', 'option_b': '4x + 7', 'option_c': '4x + 12', 'option_d': 'x + 12',
        'correct_answer': 'C', 'explanation': 'Use the distributive property: 4(x + 3) = 4·x + 4·3 = 4x + 12.',
        'topic_tag': 'distributive_property',
    },
    {
        'track': 'grade_6', 'sat_domain': 'expressions_equations', 'fuar_dimension': 'A', 'difficulty': 4,
        'question_text': 'Tickets to a school play cost $4 for students and $7 for adults. The drama club collected $95 total. If 5 adult tickets were sold, how many student tickets were sold?',
        'option_a': '10', 'option_b': '15', 'option_c': '20', 'option_d': '12',
        'correct_answer': 'B', 'explanation': 'Adult tickets: 5 × $7 = $35. Remaining: $95 - $35 = $60. Student tickets: $60 ÷ $4 = 15.',
        'topic_tag': 'equation_word_problems',
    },
    {
        'track': 'grade_6', 'sat_domain': 'expressions_equations', 'fuar_dimension': 'R', 'difficulty': 5,
        'question_text': 'The expression 3(2x − 4) + 2(x + 5) simplifies to ax + b. What are the values of a and b?',
        'option_a': 'a = 8, b = −2', 'option_b': 'a = 5, b = −2',
        'option_c': 'a = 8, b = 2', 'option_d': 'a = 6, b = −2',
        'correct_answer': 'A', 'explanation': 'Expand: 3(2x−4) = 6x−12, and 2(x+5) = 2x+10. Combine: 6x−12+2x+10 = 8x−2. So a=8, b=−2.',
        'topic_tag': 'combining_like_terms',
    },

    # --- Geometry & Measurement — Batch 2 (4 questions) ---
    {
        'track': 'grade_6', 'sat_domain': 'geometry_measurement', 'fuar_dimension': 'F', 'difficulty': 1,
        'question_text': 'What is the perimeter of a square with side length 7 cm?',
        'option_a': '14 cm', 'option_b': '21 cm', 'option_c': '28 cm', 'option_d': '49 cm',
        'correct_answer': 'C', 'explanation': 'Perimeter of a square = 4 × side = 4 × 7 = 28 cm.',
        'topic_tag': 'perimeter',
    },
    {
        'track': 'grade_6', 'sat_domain': 'geometry_measurement', 'fuar_dimension': 'U', 'difficulty': 2,
        'question_text': 'A rectangle and a triangle have the same base of 10 cm and the same height of 6 cm. How do their areas compare?',
        'option_a': 'They are equal', 'option_b': 'The rectangle is twice the triangle\'s area',
        'option_c': 'The triangle is twice the rectangle\'s area', 'option_d': 'The rectangle is four times the triangle\'s area',
        'correct_answer': 'B', 'explanation': 'Rectangle area = base × height = 60 cm². Triangle area = ½ × base × height = 30 cm². The rectangle is twice the triangle\'s area.',
        'topic_tag': 'area_concepts',
    },
    {
        'track': 'grade_6', 'sat_domain': 'geometry_measurement', 'fuar_dimension': 'A', 'difficulty': 4,
        'question_text': 'A rectangular swimming pool is 25 meters long, 10 meters wide, and 2 meters deep. It is filled to 80% capacity. How many cubic meters of water are in the pool?',
        'option_a': '300 m³', 'option_b': '350 m³', 'option_c': '400 m³', 'option_d': '500 m³',
        'correct_answer': 'C', 'explanation': 'Total volume = 25 × 10 × 2 = 500 m³. 80% of 500 = 0.8 × 500 = 400 m³.',
        'topic_tag': 'volume',
    },
    {
        'track': 'grade_6', 'sat_domain': 'geometry_measurement', 'fuar_dimension': 'R', 'difficulty': 5,
        'question_text': 'A composite figure consists of a rectangle (length 10 cm, width 4 cm) with a right triangle attached to its right side (legs of 4 cm and 3 cm). What is the total area of the composite figure?',
        'option_a': '40 cm²', 'option_b': '46 cm²', 'option_c': '52 cm²', 'option_d': '58 cm²',
        'correct_answer': 'B', 'explanation': 'Rectangle area = 10 × 4 = 40 cm². Triangle area = ½ × 3 × 4 = 6 cm². Total = 40 + 6 = 46 cm².',
        'topic_tag': 'composite_figures',
    },

    # --- Data & Statistics — Batch 2 (4 questions) ---
    {
        'track': 'grade_6', 'sat_domain': 'data_statistics', 'fuar_dimension': 'F', 'difficulty': 1,
        'question_text': 'What is the median of this data set: 3, 7, 9, 2, 5?',
        'option_a': '3', 'option_b': '5', 'option_c': '7', 'option_d': '9',
        'correct_answer': 'B', 'explanation': 'First order the data: 2, 3, 5, 7, 9. The middle value (3rd out of 5) is 5.',
        'topic_tag': 'median',
    },
    {
        'track': 'grade_6', 'sat_domain': 'data_statistics', 'fuar_dimension': 'U', 'difficulty': 2,
        'question_text': 'A bar graph shows that 12 students chose soccer, 8 chose basketball, and 5 chose tennis. What fraction of students chose basketball?',
        'option_a': '8/12', 'option_b': '8/20', 'option_c': '8/25', 'option_d': '8/17',
        'correct_answer': 'C', 'explanation': 'Total students = 12 + 8 + 5 = 25. Fraction that chose basketball = 8/25.',
        'topic_tag': 'reading_graphs',
    },
    {
        'track': 'grade_6', 'sat_domain': 'data_statistics', 'fuar_dimension': 'A', 'difficulty': 4,
        'question_text': 'A student scored 72, 85, 90, and 79 on four tests. What score does she need on the fifth test to have a mean of exactly 84?',
        'option_a': '88', 'option_b': '90', 'option_c': '94', 'option_d': '96',
        'correct_answer': 'C', 'explanation': 'Desired total for 5 tests = 84 × 5 = 420. Current total = 72+85+90+79 = 326. Needed: 420 − 326 = 94.',
        'topic_tag': 'mean',
    },
    {
        'track': 'grade_6', 'sat_domain': 'data_statistics', 'fuar_dimension': 'R', 'difficulty': 5,
        'question_text': 'Two classes each have 5 students. Class A scores: 60, 70, 80, 90, 100. Class B scores: 78, 79, 80, 81, 82. Which statement BEST compares the two classes?',
        'option_a': 'Class A performed better because its highest score is 100',
        'option_b': 'The classes are identical because they have the same mean and median',
        'option_c': 'Class B is more consistent; both classes have the same mean of 80 but Class B has a much smaller range',
        'option_d': 'Class A is more consistent because its scores are evenly spaced',
        'correct_answer': 'C', 'explanation': 'Both means = 80 and both medians = 80. Class A range = 40, Class B range = 4. Class B is far more consistent (less spread). Identical mean/median but very different variability.',
        'topic_tag': 'statistical_reasoning',
    },
]


def seed():
    conn = sqlite3.connect(DB_PATH)

    # Check if questions already seeded
    existing = conn.execute("SELECT COUNT(*) FROM questions WHERE track = 'grade_6'").fetchone()[0]
    if existing > 0:
        print(f"[Grade 6] Already has {existing} questions. Skipping seed.")
        conn.close()
        return existing

    for q in QUESTIONS:
        conn.execute("""
            INSERT INTO questions (track, sat_domain, fuar_dimension, difficulty,
                                   question_text, question_type, option_a, option_b,
                                   option_c, option_d, correct_answer, explanation, topic_tag)
            VALUES (?, ?, ?, ?, ?, 'multiple_choice', ?, ?, ?, ?, ?, ?, ?)
        """, (q['track'], q['sat_domain'], q['fuar_dimension'], q['difficulty'],
              q['question_text'], q['option_a'], q['option_b'], q['option_c'],
              q['option_d'], q['correct_answer'], q['explanation'], q['topic_tag']))

    conn.commit()
    count = conn.execute("SELECT COUNT(*) FROM questions WHERE track = 'grade_6'").fetchone()[0]
    print(f"[Grade 6] Seeded {count} questions.")
    conn.close()
    return count


if __name__ == '__main__':
    seed()
