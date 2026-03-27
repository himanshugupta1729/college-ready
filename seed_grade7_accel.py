"""Seed Grade 7 Accelerated questions — Pre-Algebra track.
52 questions across 7 content areas, balanced across FUAR dimensions.
Difficulty range 1-5 (wide range for MST adaptive routing). These students
are heading toward Algebra 1.

Batch 1 (questions 1-24): difficulty roughly F=2/3, U=3/4, A=3/4, R=4/5
Batch 2 (questions 25-52): difficulty F=1, U=2, A=4, R=5
FUAR totals: F=15, U=12, A=12, R=13
"""

import sqlite3
import os

DB_PATH = os.environ.get('DATABASE_PATH', 'college_ready.db')

QUESTIONS = [
    # --- Proportional Relationships (3-4 questions, 15%) ---
    {
        'track': 'grade_7_accelerated', 'sat_domain': 'proportional_relationships', 'fuar_dimension': 'F', 'difficulty': 3,
        'question_text': 'A recipe calls for 2.5 cups of flour for every 4 dozen cookies. How many cups of flour are needed for 10 dozen cookies?',
        'option_a': '5 cups', 'option_b': '6.25 cups', 'option_c': '7.5 cups', 'option_d': '10 cups',
        'correct_answer': 'B', 'explanation': 'Set up proportion: 2.5/4 = x/10. Cross multiply: 4x = 25, x = 6.25 cups.',
        'topic_tag': 'proportional_computation',
    },
    {
        'track': 'grade_7_accelerated', 'sat_domain': 'proportional_relationships', 'fuar_dimension': 'U', 'difficulty': 4,
        'question_text': 'The equation y = 3.5x passes through the origin. Which statement is FALSE?',
        'option_a': 'The constant of proportionality is 3.5', 'option_b': 'When x doubles, y doubles',
        'option_c': 'The graph is a straight line', 'option_d': 'The y-intercept is 3.5',
        'correct_answer': 'D', 'explanation': 'y = 3.5x passes through the origin, so the y-intercept is 0, not 3.5. The 3.5 is the slope/constant of proportionality.',
        'topic_tag': 'proportionality_concepts',
    },
    {
        'track': 'grade_7_accelerated', 'sat_domain': 'proportional_relationships', 'fuar_dimension': 'R', 'difficulty': 5,
        'question_text': 'Car A travels at 55 mph. Car B starts 30 miles ahead of Car A, traveling at 40 mph in the same direction. After how many hours does Car A catch Car B?',
        'option_a': '1 hour', 'option_b': '2 hours', 'option_c': '3 hours', 'option_d': '6 hours',
        'correct_answer': 'B', 'explanation': 'Car A gains 55 - 40 = 15 mph on Car B. To close a 30-mile gap: 30/15 = 2 hours.',
        'topic_tag': 'proportional_reasoning',
    },

    # --- Rational Numbers (3-4 questions, 15%) ---
    {
        'track': 'grade_7_accelerated', 'sat_domain': 'rational_numbers', 'fuar_dimension': 'F', 'difficulty': 3,
        'question_text': 'Evaluate: (-3/4) ÷ (2/5)',
        'option_a': '-15/8', 'option_b': '-6/20', 'option_c': '-3/10', 'option_d': '15/8',
        'correct_answer': 'A', 'explanation': '(-3/4) ÷ (2/5) = (-3/4) × (5/2) = -15/8.',
        'topic_tag': 'rational_operations',
    },
    {
        'track': 'grade_7_accelerated', 'sat_domain': 'rational_numbers', 'fuar_dimension': 'A', 'difficulty': 4,
        'question_text': 'The temperature dropped from 5.5°F to -8.3°F overnight. What was the total change in temperature?',
        'option_a': '-2.8°F', 'option_b': '-13.8°F', 'option_c': '13.8°F', 'option_d': '2.8°F',
        'correct_answer': 'B', 'explanation': 'Change = final - initial = -8.3 - 5.5 = -13.8°F. The temperature dropped 13.8 degrees.',
        'topic_tag': 'rational_applications',
    },
    {
        'track': 'grade_7_accelerated', 'sat_domain': 'rational_numbers', 'fuar_dimension': 'R', 'difficulty': 4,
        'question_text': 'Which expression is ALWAYS negative when a < 0 and b > 0?',
        'option_a': 'a + b', 'option_b': 'a × b', 'option_c': 'a - b', 'option_d': 'Both B and C',
        'correct_answer': 'D', 'explanation': 'a × b: negative × positive = always negative. a - b: negative minus positive = always negative. a + b could be positive if b > |a|.',
        'topic_tag': 'rational_reasoning',
    },

    # --- Linear Equations Intro (5 questions, 20%) ---
    {
        'track': 'grade_7_accelerated', 'sat_domain': 'linear_equations_intro', 'fuar_dimension': 'F', 'difficulty': 3,
        'question_text': 'Solve for x: 4x - 7 = 2x + 9',
        'option_a': 'x = 1', 'option_b': 'x = 8', 'option_c': 'x = 2', 'option_d': 'x = -8',
        'correct_answer': 'B', 'explanation': '4x - 7 = 2x + 9 → 2x = 16 → x = 8.',
        'topic_tag': 'two_step_equations',
    },
    {
        'track': 'grade_7_accelerated', 'sat_domain': 'linear_equations_intro', 'fuar_dimension': 'F', 'difficulty': 4,
        'question_text': 'Solve: 3(2x - 1) + 4 = 5x + 7',
        'option_a': 'x = 6', 'option_b': 'x = 4', 'option_c': 'x = 10', 'option_d': 'x = -6',
        'correct_answer': 'A', 'explanation': '6x - 3 + 4 = 5x + 7 → 6x + 1 = 5x + 7 → x = 6.',
        'topic_tag': 'multi_step_equations',
    },
    {
        'track': 'grade_7_accelerated', 'sat_domain': 'linear_equations_intro', 'fuar_dimension': 'U', 'difficulty': 4,
        'question_text': 'The equation 2(x + 3) = 2x + 6 has how many solutions?',
        'option_a': 'No solutions', 'option_b': 'Exactly one solution', 'option_c': 'Exactly two solutions', 'option_d': 'Infinitely many solutions',
        'correct_answer': 'D', 'explanation': 'Distributing: 2x + 6 = 2x + 6. This is always true for any x, so there are infinitely many solutions (it is an identity).',
        'topic_tag': 'equation_concepts',
    },
    {
        'track': 'grade_7_accelerated', 'sat_domain': 'linear_equations_intro', 'fuar_dimension': 'A', 'difficulty': 4,
        'question_text': 'A pool has 50 gallons and is being filled at 10 gallons per minute. A second pool has 200 gallons and is draining at 5 gallons per minute. After how many minutes do they have the same amount?',
        'option_a': '8 minutes', 'option_b': '10 minutes', 'option_c': '15 minutes', 'option_d': '20 minutes',
        'correct_answer': 'B', 'explanation': 'Pool 1: 50 + 10m. Pool 2: 200 - 5m. Set equal: 50 + 10m = 200 - 5m → 15m = 150 → m = 10 minutes.',
        'topic_tag': 'equation_word_problems',
    },
    {
        'track': 'grade_7_accelerated', 'sat_domain': 'linear_equations_intro', 'fuar_dimension': 'R', 'difficulty': 5,
        'question_text': 'For the equation 3x + k = 5x - 7 to have a solution of x = 4, what must k equal?',
        'option_a': '1', 'option_b': '-1', 'option_c': '5', 'option_d': '7',
        'correct_answer': 'A', 'explanation': 'Substitute x = 4: 3(4) + k = 5(4) - 7 → 12 + k = 13 → k = 1.',
        'topic_tag': 'equation_reasoning',
    },

    # --- Functions Intro (3-4 questions, 15%) ---
    {
        'track': 'grade_7_accelerated', 'sat_domain': 'functions_intro', 'fuar_dimension': 'F', 'difficulty': 3,
        'question_text': 'If f(x) = 2x + 5, what is f(3)?',
        'option_a': '8', 'option_b': '11', 'option_c': '10', 'option_d': '6',
        'correct_answer': 'B', 'explanation': 'f(3) = 2(3) + 5 = 6 + 5 = 11.',
        'topic_tag': 'function_evaluation',
    },
    {
        'track': 'grade_7_accelerated', 'sat_domain': 'functions_intro', 'fuar_dimension': 'U', 'difficulty': 4,
        'question_text': 'Which table does NOT represent a function?',
        'option_a': 'x: 1,2,3 → y: 4,5,6', 'option_b': 'x: 1,2,1 → y: 3,5,7',
        'option_c': 'x: 1,2,3 → y: 4,4,4', 'option_d': 'x: -1,0,1 → y: 1,0,1',
        'correct_answer': 'B', 'explanation': 'A function assigns exactly one output to each input. In B, input x=1 maps to both y=3 and y=7 — that violates the function rule.',
        'topic_tag': 'function_concepts',
    },
    {
        'track': 'grade_7_accelerated', 'sat_domain': 'functions_intro', 'fuar_dimension': 'A', 'difficulty': 4,
        'question_text': 'A gym charges a $30 registration fee plus $15 per month. Which function represents the total cost C after m months?',
        'option_a': 'C = 30m + 15', 'option_b': 'C = 15m + 30', 'option_c': 'C = 45m', 'option_d': 'C = 30m',
        'correct_answer': 'B', 'explanation': 'Total cost = monthly rate × months + one-time fee = 15m + 30.',
        'topic_tag': 'linear_function_applications',
    },
    {
        'track': 'grade_7_accelerated', 'sat_domain': 'functions_intro', 'fuar_dimension': 'R', 'difficulty': 5,
        'question_text': 'A linear function passes through (2, 7) and (5, 16). What is the rate of change?',
        'option_a': '3', 'option_b': '9', 'option_c': '2', 'option_d': '4.5',
        'correct_answer': 'A', 'explanation': 'Rate of change = (16 - 7)/(5 - 2) = 9/3 = 3.',
        'topic_tag': 'rate_of_change',
    },

    # --- Geometry Transformations (3-4 questions, 15%) ---
    {
        'track': 'grade_7_accelerated', 'sat_domain': 'geometry_transformations', 'fuar_dimension': 'F', 'difficulty': 3,
        'question_text': 'Point A(3, -2) is reflected over the x-axis. What are the coordinates of the image?',
        'option_a': '(-3, -2)', 'option_b': '(3, 2)', 'option_c': '(-3, 2)', 'option_d': '(2, -3)',
        'correct_answer': 'B', 'explanation': 'Reflecting over the x-axis changes the sign of the y-coordinate: (3, -2) → (3, 2).',
        'topic_tag': 'reflections',
    },
    {
        'track': 'grade_7_accelerated', 'sat_domain': 'geometry_transformations', 'fuar_dimension': 'U', 'difficulty': 4,
        'question_text': 'A dilation with scale factor 2 centered at the origin maps point (3, 5) to what point?',
        'option_a': '(5, 7)', 'option_b': '(1.5, 2.5)', 'option_c': '(6, 10)', 'option_d': '(3, 10)',
        'correct_answer': 'C', 'explanation': 'A dilation with scale factor 2 multiplies both coordinates by 2: (3×2, 5×2) = (6, 10).',
        'topic_tag': 'dilations',
    },
    {
        'track': 'grade_7_accelerated', 'sat_domain': 'geometry_transformations', 'fuar_dimension': 'A', 'difficulty': 4,
        'question_text': 'Triangle ABC has vertices A(1,1), B(4,1), C(1,5). It is translated 3 units right and 2 units down. What are the new coordinates of C?',
        'option_a': '(4, 3)', 'option_b': '(4, 7)', 'option_c': '(-2, 7)', 'option_d': '(1, 3)',
        'correct_answer': 'A', 'explanation': 'Translation: add 3 to x, subtract 2 from y. C(1,5) → (1+3, 5-2) = (4, 3).',
        'topic_tag': 'translations',
    },

    # --- Exponents & Scientific Notation (2-3 questions, 10%) ---
    {
        'track': 'grade_7_accelerated', 'sat_domain': 'exponents_scientific_notation', 'fuar_dimension': 'F', 'difficulty': 3,
        'question_text': 'Simplify: 2³ × 2⁴',
        'option_a': '2⁷', 'option_b': '2¹²', 'option_c': '4⁷', 'option_d': '4¹²',
        'correct_answer': 'A', 'explanation': 'When multiplying powers with the same base, add exponents: 2³ × 2⁴ = 2^(3+4) = 2⁷.',
        'topic_tag': 'exponent_rules',
    },
    {
        'track': 'grade_7_accelerated', 'sat_domain': 'exponents_scientific_notation', 'fuar_dimension': 'U', 'difficulty': 4,
        'question_text': 'The distance from Earth to the Sun is about 93,000,000 miles. In scientific notation, this is:',
        'option_a': '93 × 10⁶', 'option_b': '9.3 × 10⁷', 'option_c': '9.3 × 10⁸', 'option_d': '0.93 × 10⁸',
        'correct_answer': 'B', 'explanation': '93,000,000 = 9.3 × 10⁷. In proper scientific notation, the coefficient must be between 1 and 10.',
        'topic_tag': 'scientific_notation',
    },
    {
        'track': 'grade_7_accelerated', 'sat_domain': 'exponents_scientific_notation', 'fuar_dimension': 'R', 'difficulty': 5,
        'question_text': 'If 3ⁿ = 81, what is the value of 3^(n+1)?',
        'option_a': '82', 'option_b': '162', 'option_c': '243', 'option_d': '324',
        'correct_answer': 'C', 'explanation': '3ⁿ = 81, so n = 4 (since 3⁴ = 81). Then 3^(n+1) = 3⁵ = 243.',
        'topic_tag': 'exponent_reasoning',
    },

    # --- Systems Intro (2-3 questions, 10%) ---
    {
        'track': 'grade_7_accelerated', 'sat_domain': 'systems_intro', 'fuar_dimension': 'F', 'difficulty': 4,
        'question_text': 'Solve the system: x + y = 10 and x - y = 2. What is x?',
        'option_a': '4', 'option_b': '6', 'option_c': '8', 'option_d': '5',
        'correct_answer': 'B', 'explanation': 'Add both equations: 2x = 12, so x = 6. Then y = 10 - 6 = 4.',
        'topic_tag': 'systems_elimination',
    },
    {
        'track': 'grade_7_accelerated', 'sat_domain': 'systems_intro', 'fuar_dimension': 'A', 'difficulty': 4,
        'question_text': 'Adult tickets cost $8 and child tickets cost $5. A family buys 6 tickets for $39. How many adult tickets did they buy?',
        'option_a': '2', 'option_b': '3', 'option_c': '4', 'option_d': '5',
        'correct_answer': 'B', 'explanation': 'Let a = adult, c = child. a + c = 6 and 8a + 5c = 39. From first: c = 6-a. Substitute: 8a + 5(6-a) = 39 → 8a + 30 - 5a = 39 → 3a = 9 → a = 3.',
        'topic_tag': 'systems_word_problems',
    },
    {
        'track': 'grade_7_accelerated', 'sat_domain': 'systems_intro', 'fuar_dimension': 'R', 'difficulty': 5,
        'question_text': 'The system y = 2x + 1 and y = 2x + 5 has:',
        'option_a': 'One solution', 'option_b': 'Two solutions', 'option_c': 'No solution', 'option_d': 'Infinitely many solutions',
        'correct_answer': 'C', 'explanation': 'Both lines have slope 2 but different y-intercepts (1 and 5). Parallel lines never intersect, so there is no solution.',
        'topic_tag': 'systems_reasoning',
    },

    # ============================================================
    # BATCH 2 — 24 questions, difficulty F=1, U=2, A=4, R=5
    # Adds easier and harder ends for MST adaptive routing.
    # ============================================================

    # --- Proportional Relationships (Batch 2) ---
    {
        'track': 'grade_7_accelerated', 'sat_domain': 'proportional_relationships', 'fuar_dimension': 'F', 'difficulty': 1,
        'question_text': 'A car travels 60 miles in 2 hours at a constant speed. How many miles does it travel in 1 hour?',
        'option_a': '20 miles', 'option_b': '30 miles', 'option_c': '40 miles', 'option_d': '120 miles',
        'correct_answer': 'B', 'explanation': '60 miles ÷ 2 hours = 30 miles per hour. In 1 hour it travels 30 miles.',
        'topic_tag': 'unit_rate',
    },
    {
        'track': 'grade_7_accelerated', 'sat_domain': 'proportional_relationships', 'fuar_dimension': 'U', 'difficulty': 2,
        'question_text': 'Which of the following tables shows a proportional relationship between x and y?',
        'option_a': 'x: 1,2,3 → y: 3,6,10', 'option_b': 'x: 2,4,6 → y: 6,12,18',
        'option_c': 'x: 1,3,5 → y: 4,6,8', 'option_d': 'x: 1,2,3 → y: 2,5,8',
        'correct_answer': 'B', 'explanation': 'A proportional relationship has a constant ratio y/x. In B: 6/2 = 12/4 = 18/6 = 3. The ratio is always 3.',
        'topic_tag': 'proportionality_concepts',
    },
    {
        'track': 'grade_7_accelerated', 'sat_domain': 'proportional_relationships', 'fuar_dimension': 'A', 'difficulty': 4,
        'question_text': 'A store sells 3 notebooks for $4.50. At the same rate, a school needs to buy 45 notebooks. What is the total cost?',
        'option_a': '$60.00', 'option_b': '$67.50', 'option_c': '$45.00', 'option_d': '$54.00',
        'correct_answer': 'B', 'explanation': 'Unit price = $4.50 ÷ 3 = $1.50 per notebook. Total = 45 × $1.50 = $67.50.',
        'topic_tag': 'proportional_computation',
    },
    {
        'track': 'grade_7_accelerated', 'sat_domain': 'proportional_relationships', 'fuar_dimension': 'R', 'difficulty': 5,
        'question_text': 'Two quantities x and y are proportional. When x = 6, y = 10. A student claims: "When x increases by 3, y always increases by 5." Is this claim correct, and why?',
        'option_a': 'Yes — because y increases by 5/3 for every 1 unit increase in x, so 3 units gives exactly 5', 'option_b': 'No — proportional relationships only hold for whole-number x values',
        'option_c': 'Yes — but only when x is a multiple of 6', 'option_d': 'No — the constant of proportionality is 6/10, not 3/5',
        'correct_answer': 'A', 'explanation': 'The constant of proportionality is 10/6 = 5/3. So for every 1-unit increase in x, y increases by 5/3. For a 3-unit increase: 3 × (5/3) = 5. The claim is correct.',
        'topic_tag': 'proportional_reasoning',
    },

    # --- Rational Numbers (Batch 2) ---
    {
        'track': 'grade_7_accelerated', 'sat_domain': 'rational_numbers', 'fuar_dimension': 'F', 'difficulty': 1,
        'question_text': 'What is the absolute value of -7?',
        'option_a': '-7', 'option_b': '0', 'option_c': '7', 'option_d': '1/7',
        'correct_answer': 'C', 'explanation': 'The absolute value of a number is its distance from zero on the number line. |-7| = 7.',
        'topic_tag': 'absolute_value',
    },
    {
        'track': 'grade_7_accelerated', 'sat_domain': 'rational_numbers', 'fuar_dimension': 'U', 'difficulty': 2,
        'question_text': 'Which list correctly orders these numbers from least to greatest? -1.5, 0.75, -0.5, -2',
        'option_a': '-2, -1.5, -0.5, 0.75', 'option_b': '-0.5, -1.5, -2, 0.75',
        'option_c': '0.75, -0.5, -1.5, -2', 'option_d': '-2, -0.5, -1.5, 0.75',
        'correct_answer': 'A', 'explanation': 'On the number line from left (least) to right (greatest): -2 < -1.5 < -0.5 < 0.75.',
        'topic_tag': 'rational_number_ordering',
    },
    {
        'track': 'grade_7_accelerated', 'sat_domain': 'rational_numbers', 'fuar_dimension': 'A', 'difficulty': 4,
        'question_text': 'A submarine is at -180 feet (below sea level). It ascends 65 feet, then descends 120 feet. What is its final depth?',
        'option_a': '-235 feet', 'option_b': '-115 feet', 'option_c': '-245 feet', 'option_d': '-180 feet',
        'correct_answer': 'A', 'explanation': 'Start: -180. After ascending 65 ft: -180 + 65 = -115. After descending 120 ft: -115 - 120 = -235 feet.',
        'topic_tag': 'rational_applications',
    },
    {
        'track': 'grade_7_accelerated', 'sat_domain': 'rational_numbers', 'fuar_dimension': 'R', 'difficulty': 5,
        'question_text': 'For which values of a and b is the expression (a ÷ b) a positive rational number? Select the correct pair.',
        'option_a': 'a = -3/4, b = -3/4', 'option_b': 'a = -5, b = 2',
        'option_c': 'a = 0, b = -4', 'option_d': 'a = 3/5, b = -1/2',
        'correct_answer': 'A', 'explanation': '(-3/4) ÷ (-3/4) = 1, which is positive. In B: negative ÷ positive = negative. In C: 0 ÷ anything = 0, not positive. In D: positive ÷ negative = negative.',
        'topic_tag': 'rational_reasoning',
    },

    # --- Linear Equations Intro (Batch 2) ---
    {
        'track': 'grade_7_accelerated', 'sat_domain': 'linear_equations_intro', 'fuar_dimension': 'F', 'difficulty': 1,
        'question_text': 'Solve for x: x + 9 = 15',
        'option_a': 'x = 4', 'option_b': 'x = 6', 'option_c': 'x = 24', 'option_d': 'x = 9',
        'correct_answer': 'B', 'explanation': 'Subtract 9 from both sides: x = 15 - 9 = 6.',
        'topic_tag': 'one_step_equations',
    },
    {
        'track': 'grade_7_accelerated', 'sat_domain': 'linear_equations_intro', 'fuar_dimension': 'U', 'difficulty': 2,
        'question_text': 'The equation 5x + 3 = 18 can be solved by first doing which operation to both sides?',
        'option_a': 'Multiply by 5', 'option_b': 'Divide by 5',
        'option_c': 'Subtract 3', 'option_d': 'Add 18',
        'correct_answer': 'C', 'explanation': 'To isolate the term with x, first undo the addition by subtracting 3 from both sides: 5x = 15. Then divide by 5.',
        'topic_tag': 'equation_concepts',
    },
    {
        'track': 'grade_7_accelerated', 'sat_domain': 'linear_equations_intro', 'fuar_dimension': 'A', 'difficulty': 4,
        'question_text': 'A candle is 24 cm tall when lit. It burns down 3 cm every hour. A second candle starts at 18 cm and burns down 1.5 cm every hour. After how many hours h are the two candles the same height?',
        'option_a': 'h = 3', 'option_b': 'h = 4', 'option_c': 'h = 6', 'option_d': 'h = 8',
        'correct_answer': 'B', 'explanation': 'Candle 1 height: 24 - 3h. Candle 2 height: 18 - 1.5h. Set equal: 24 - 3h = 18 - 1.5h → 24 - 18 = 3h - 1.5h → 6 = 1.5h → h = 4 hours.',
        'topic_tag': 'equation_word_problems',
    },
    {
        'track': 'grade_7_accelerated', 'sat_domain': 'linear_equations_intro', 'fuar_dimension': 'R', 'difficulty': 5,
        'question_text': 'The equation ax + 4 = 2x + b has infinitely many solutions. What must be true about a and b?',
        'option_a': 'a = 2 and b = 4', 'option_b': 'a = 2 and b can be anything',
        'option_c': 'a can be anything and b = 4', 'option_d': 'a ≠ 2 and b ≠ 4',
        'correct_answer': 'A', 'explanation': 'For infinitely many solutions, both sides must be identical. Matching coefficients: a = 2. Matching constants: 4 = b, so b = 4. Both conditions must hold simultaneously.',
        'topic_tag': 'equation_reasoning',
    },

    # --- Functions Intro (Batch 2) ---
    {
        'track': 'grade_7_accelerated', 'sat_domain': 'functions_intro', 'fuar_dimension': 'F', 'difficulty': 1,
        'question_text': 'If g(x) = x + 4, what is g(0)?',
        'option_a': '0', 'option_b': '4', 'option_c': '-4', 'option_d': '1',
        'correct_answer': 'B', 'explanation': 'g(0) = 0 + 4 = 4.',
        'topic_tag': 'function_evaluation',
    },
    {
        'track': 'grade_7_accelerated', 'sat_domain': 'functions_intro', 'fuar_dimension': 'U', 'difficulty': 2,
        'question_text': 'A vending machine dispenses one item per button press. Is this an example of a function? Why?',
        'option_a': 'No — because you can press the button many times', 'option_b': 'Yes — each button press (input) produces exactly one item (output)',
        'option_c': 'No — because different buttons can give the same item', 'option_d': 'Yes — but only if every button gives a different item',
        'correct_answer': 'B', 'explanation': 'A function assigns exactly one output to each input. Each button press gives exactly one item, so it qualifies. Different inputs can share the same output — that is allowed.',
        'topic_tag': 'function_concepts',
    },
    {
        'track': 'grade_7_accelerated', 'sat_domain': 'functions_intro', 'fuar_dimension': 'A', 'difficulty': 4,
        'question_text': 'A taxi company charges a flat fee of $2.50 plus $1.75 per mile. A second company charges $1.00 flat fee plus $2.25 per mile. For what number of miles m do both companies charge the same total amount?',
        'option_a': '2 miles', 'option_b': '3 miles', 'option_c': '4 miles', 'option_d': '5 miles',
        'correct_answer': 'B', 'explanation': 'Set equal: 2.50 + 1.75m = 1.00 + 2.25m → 1.50 = 0.50m → m = 3 miles.',
        'topic_tag': 'linear_function_applications',
    },
    {
        'track': 'grade_7_accelerated', 'sat_domain': 'functions_intro', 'fuar_dimension': 'R', 'difficulty': 5,
        'question_text': 'A function f has the property f(2) = 7 and f(5) = 13. If f is linear, what is f(11)?',
        'option_a': '19', 'option_b': '23', 'option_c': '25', 'option_d': '29',
        'correct_answer': 'C', 'explanation': 'Slope = (13 - 7)/(5 - 2) = 6/3 = 2. Using f(2) = 7: f(x) = 2x + b → 7 = 4 + b → b = 3. So f(x) = 2x + 3. f(11) = 22 + 3 = 25.',
        'topic_tag': 'rate_of_change',
    },

    # --- Geometry Transformations (Batch 2) ---
    {
        'track': 'grade_7_accelerated', 'sat_domain': 'geometry_transformations', 'fuar_dimension': 'F', 'difficulty': 1,
        'question_text': 'Point P(4, 3) is translated 2 units left and 1 unit up. What are the new coordinates?',
        'option_a': '(6, 4)', 'option_b': '(2, 4)', 'option_c': '(4, 2)', 'option_d': '(2, 2)',
        'correct_answer': 'B', 'explanation': '2 units left: 4 - 2 = 2. 1 unit up: 3 + 1 = 4. New point: (2, 4).',
        'topic_tag': 'translations',
    },
    {
        'track': 'grade_7_accelerated', 'sat_domain': 'geometry_transformations', 'fuar_dimension': 'U', 'difficulty': 2,
        'question_text': 'Which transformation changes the SIZE of a figure?',
        'option_a': 'Reflection', 'option_b': 'Translation',
        'option_c': 'Rotation', 'option_d': 'Dilation',
        'correct_answer': 'D', 'explanation': 'A dilation scales a figure by a factor, changing its size. Reflections, translations, and rotations are rigid motions that preserve size and shape.',
        'topic_tag': 'dilations',
    },
    {
        'track': 'grade_7_accelerated', 'sat_domain': 'geometry_transformations', 'fuar_dimension': 'A', 'difficulty': 4,
        'question_text': 'Rectangle ABCD has vertices A(0,0), B(4,0), C(4,3), D(0,3). It is dilated by scale factor 1/2 centered at the origin. What is the perimeter of the image rectangle?',
        'option_a': '7 units', 'option_b': '3.5 units', 'option_c': '14 units', 'option_d': '28 units',
        'correct_answer': 'A', 'explanation': 'After dilation by 1/2: A(0,0), B(2,0), C(2,1.5), D(0,1.5). Width = 2, height = 1.5. Perimeter = 2(2 + 1.5) = 2(3.5) = 7 units.',
        'topic_tag': 'dilations',
    },
    {
        'track': 'grade_7_accelerated', 'sat_domain': 'geometry_transformations', 'fuar_dimension': 'R', 'difficulty': 5,
        'question_text': 'Triangle PQR is reflected over the y-axis, then translated 4 units down. Point P was originally at (-2, 5). What are the final coordinates of the image of P?',
        'option_a': '(-2, 1)', 'option_b': '(2, 1)', 'option_c': '(2, 9)', 'option_d': '(-2, -5)',
        'correct_answer': 'B', 'explanation': 'Step 1 — reflect over y-axis: changes sign of x-coordinate. (-2, 5) → (2, 5). Step 2 — translate 4 units down: subtract 4 from y. (2, 5) → (2, 1).',
        'topic_tag': 'composite_transformations',
    },

    # --- Exponents & Scientific Notation (Batch 2) ---
    {
        'track': 'grade_7_accelerated', 'sat_domain': 'exponents_scientific_notation', 'fuar_dimension': 'F', 'difficulty': 1,
        'question_text': 'What is the value of 5²?',
        'option_a': '10', 'option_b': '7', 'option_c': '25', 'option_d': '15',
        'correct_answer': 'C', 'explanation': '5² = 5 × 5 = 25.',
        'topic_tag': 'exponent_rules',
    },
    {
        'track': 'grade_7_accelerated', 'sat_domain': 'exponents_scientific_notation', 'fuar_dimension': 'U', 'difficulty': 2,
        'question_text': 'Which number is written in correct scientific notation?',
        'option_a': '0.45 × 10³', 'option_b': '45 × 10²',
        'option_c': '4.5 × 10³', 'option_d': '4.5 × 100',
        'correct_answer': 'C', 'explanation': 'Scientific notation requires a coefficient between 1 and 10 multiplied by a power of 10. Only 4.5 × 10³ meets both requirements.',
        'topic_tag': 'scientific_notation',
    },
    {
        'track': 'grade_7_accelerated', 'sat_domain': 'exponents_scientific_notation', 'fuar_dimension': 'A', 'difficulty': 4,
        'question_text': 'A bacterium divides in two every 20 minutes. Starting with 1 bacterium, how many bacteria are there after 2 hours?',
        'option_a': '12', 'option_b': '64', 'option_c': '128', 'option_d': '4096',
        'correct_answer': 'B', 'explanation': '2 hours = 120 minutes. Number of divisions = 120 ÷ 20 = 6. Number of bacteria = 2⁶ = 64.',
        'topic_tag': 'exponent_applications',
    },
    {
        'track': 'grade_7_accelerated', 'sat_domain': 'exponents_scientific_notation', 'fuar_dimension': 'R', 'difficulty': 5,
        'question_text': 'The mass of a proton is approximately 1.67 × 10⁻²⁷ kg. The mass of an electron is approximately 9.11 × 10⁻³¹ kg. Approximately how many times heavier is a proton than an electron?',
        'option_a': 'About 180 times', 'option_b': 'About 1,800 times',
        'option_c': 'About 18,000 times', 'option_d': 'About 18 times',
        'correct_answer': 'B', 'explanation': '(1.67 × 10⁻²⁷) ÷ (9.11 × 10⁻³¹) = (1.67 ÷ 9.11) × 10⁻²⁷⁺³¹ = 0.183 × 10⁴ ≈ 1,830 ≈ 1,800 times heavier.',
        'topic_tag': 'scientific_notation',
    },

    # --- Systems Intro (Batch 2) ---
    {
        'track': 'grade_7_accelerated', 'sat_domain': 'systems_intro', 'fuar_dimension': 'F', 'difficulty': 1,
        'question_text': 'Is the point (2, 5) a solution to the system: y = x + 3 and y = 2x + 1?',
        'option_a': 'Yes — it satisfies both equations', 'option_b': 'No — it only satisfies y = x + 3',
        'option_c': 'No — it does not satisfy either equation', 'option_d': 'No — it only satisfies y = 2x + 1',
        'correct_answer': 'A', 'explanation': 'Check y = x + 3: 5 = 2 + 3 = 5 ✓. Check y = 2x + 1: 5 = 4 + 1 = 5 ✓. Since (2, 5) satisfies both equations, it is the solution.',
        'topic_tag': 'systems_substitution',
    },
    {
        'track': 'grade_7_accelerated', 'sat_domain': 'systems_intro', 'fuar_dimension': 'U', 'difficulty': 2,
        'question_text': 'Two lines on a graph intersect at exactly one point. What does this mean for the system of equations they represent?',
        'option_a': 'The system has no solution', 'option_b': 'The system has exactly one solution',
        'option_c': 'The system has infinitely many solutions', 'option_d': 'The lines are parallel',
        'correct_answer': 'B', 'explanation': 'Each intersection point represents a solution. One intersection point means exactly one (x, y) pair satisfies both equations — exactly one solution.',
        'topic_tag': 'systems_concepts',
    },
    {
        'track': 'grade_7_accelerated', 'sat_domain': 'systems_intro', 'fuar_dimension': 'A', 'difficulty': 4,
        'question_text': 'A store sells two types of pens. Ballpoint pens cost $1.20 each and gel pens cost $2.00 each. Priya buys 10 pens and spends $16.00 total. How many gel pens did she buy?',
        'option_a': '4', 'option_b': '5', 'option_c': '6', 'option_d': '7',
        'correct_answer': 'B', 'explanation': 'Let g = gel pens, b = ballpoint pens. b + g = 10 and 1.20b + 2.00g = 16.00. From first: b = 10 - g. Substitute: 1.20(10 - g) + 2.00g = 16 → 12 - 1.20g + 2.00g = 16 → 0.80g = 4 → g = 5.',
        'topic_tag': 'systems_word_problems',
    },
    {
        'track': 'grade_7_accelerated', 'sat_domain': 'systems_intro', 'fuar_dimension': 'R', 'difficulty': 5,
        'question_text': 'The system 3x + ky = 12 and 6x + 4y = 24 has infinitely many solutions. What is the value of k?',
        'option_a': 'k = 1', 'option_b': 'k = 2', 'option_c': 'k = 4', 'option_d': 'k = 8',
        'correct_answer': 'B', 'explanation': 'For infinitely many solutions, the equations must be identical (or multiples of each other). Multiply the first equation by 2: 6x + 2ky = 24. This must match 6x + 4y = 24. So 2k = 4, which gives k = 2.',
        'topic_tag': 'systems_reasoning',
    },
]


def seed():
    """Insert Grade 7 Accelerated questions into the database."""
    conn = sqlite3.connect(DB_PATH)
    existing = conn.execute(
        "SELECT COUNT(*) FROM questions WHERE track = 'grade_7_accelerated'"
    ).fetchone()[0]

    if existing > 0:
        print(f"[seed_grade7_accel] Already has {existing} questions, skipping.")
        conn.close()
        return

    for q in QUESTIONS:
        conn.execute("""
            INSERT INTO questions (track, sat_domain, fuar_dimension, difficulty,
                                   question_text, question_type, option_a, option_b,
                                   option_c, option_d, correct_answer, explanation, topic_tag)
            VALUES (?, ?, ?, ?, ?, 'multiple_choice', ?, ?, ?, ?, ?, ?, ?)
        """, (
            q['track'], q['sat_domain'], q['fuar_dimension'], q['difficulty'],
            q['question_text'], q['option_a'], q['option_b'],
            q['option_c'], q['option_d'], q['correct_answer'], q['explanation'],
            q['topic_tag'],
        ))

    conn.commit()
    count = conn.execute(
        "SELECT COUNT(*) FROM questions WHERE track = 'grade_7_accelerated'"
    ).fetchone()[0]
    print(f"[seed_grade7_accel] Seeded {count} Grade 7 Accelerated questions.")
    conn.close()


if __name__ == '__main__':
    seed()
