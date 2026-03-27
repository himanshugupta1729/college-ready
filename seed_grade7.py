"""Seed Grade 7 Math questions — Bridge Builder track.
24 questions across 6 content areas, balanced across FUAR dimensions.
Focus: Proportional relationships, rational numbers, expressions/equations, geometry, probability.
"""

import sqlite3
import os

DB_PATH = os.environ.get('DATABASE_PATH', 'college_ready.db')

QUESTIONS = [
    # --- Proportional Relationships (4 questions) ---
    {
        'track': 'grade_7', 'sat_domain': 'proportional_relationships', 'fuar_dimension': 'F', 'difficulty': 2,
        'question_text': 'If 4 notebooks cost $12, how much do 7 notebooks cost?',
        'option_a': '$16', 'option_b': '$19', 'option_c': '$21', 'option_d': '$28',
        'correct_answer': 'C', 'explanation': 'Unit rate: $12/4 = $3 per notebook. 7 × $3 = $21.',
        'topic_tag': 'unit_rates',
    },
    {
        'track': 'grade_7', 'sat_domain': 'proportional_relationships', 'fuar_dimension': 'U', 'difficulty': 3,
        'question_text': 'Which table shows a proportional relationship?',
        'option_a': 'x: 1,2,3 → y: 3,6,10', 'option_b': 'x: 1,2,3 → y: 4,8,12',
        'option_c': 'x: 1,2,3 → y: 2,5,8', 'option_d': 'x: 1,2,3 → y: 1,4,9',
        'correct_answer': 'B', 'explanation': 'In a proportional relationship, y/x is constant. Only B gives 4/1 = 8/2 = 12/3 = 4.',
        'topic_tag': 'proportionality_concepts',
    },
    {
        'track': 'grade_7', 'sat_domain': 'proportional_relationships', 'fuar_dimension': 'A', 'difficulty': 3,
        'question_text': 'A map uses a scale of 1 inch = 25 miles. Two cities are 3.5 inches apart on the map. What is the actual distance?',
        'option_a': '75 miles', 'option_b': '82.5 miles', 'option_c': '87.5 miles', 'option_d': '100 miles',
        'correct_answer': 'C', 'explanation': '3.5 × 25 = 87.5 miles.',
        'topic_tag': 'scale_drawings',
    },
    {
        'track': 'grade_7', 'sat_domain': 'proportional_relationships', 'fuar_dimension': 'R', 'difficulty': 4,
        'question_text': 'Mia earns $y for x hours of work. She says "If I work twice as many hours, I earn twice as much." Is this always true if the relationship is proportional?',
        'option_a': 'Yes, always', 'option_b': 'No, never', 'option_c': 'Only if she earns more than $10/hour', 'option_d': 'Only if x > 0',
        'correct_answer': 'A', 'explanation': 'In a proportional relationship y = kx. If x doubles to 2x, then y = k(2x) = 2kx = 2y. It always doubles.',
        'topic_tag': 'proportional_reasoning',
    },

    # --- Rational Numbers (4 questions) ---
    {
        'track': 'grade_7', 'sat_domain': 'rational_numbers', 'fuar_dimension': 'F', 'difficulty': 2,
        'question_text': 'What is (-3) × (-5)?',
        'option_a': '-15', 'option_b': '-8', 'option_c': '8', 'option_d': '15',
        'correct_answer': 'D', 'explanation': 'Negative × negative = positive. 3 × 5 = 15.',
        'topic_tag': 'integer_multiplication',
    },
    {
        'track': 'grade_7', 'sat_domain': 'rational_numbers', 'fuar_dimension': 'U', 'difficulty': 3,
        'question_text': 'Why is -2/3 located between -1 and 0 on the number line?',
        'option_a': 'Because 2/3 is less than 1', 'option_b': 'Because negative fractions are always between -1 and 0',
        'option_c': 'Because -2/3 means 2/3 of the way from 0 toward -1', 'option_d': 'Because the numerator is smaller than the denominator',
        'correct_answer': 'C', 'explanation': '-2/3 is 2/3 of a unit in the negative direction from 0, placing it between 0 and -1.',
        'topic_tag': 'rational_number_concepts',
    },
    {
        'track': 'grade_7', 'sat_domain': 'rational_numbers', 'fuar_dimension': 'A', 'difficulty': 3,
        'question_text': 'A submarine descends 120 feet in 4 minutes. What is its rate of descent as an integer?',
        'option_a': '-480 ft/min', 'option_b': '-30 ft/min', 'option_c': '30 ft/min', 'option_d': '-116 ft/min',
        'correct_answer': 'B', 'explanation': 'Descending = negative direction. Rate = -120/4 = -30 feet per minute.',
        'topic_tag': 'rational_number_applications',
    },
    {
        'track': 'grade_7', 'sat_domain': 'rational_numbers', 'fuar_dimension': 'R', 'difficulty': 4,
        'question_text': 'If a/b is negative and b is positive, what must be true about a?',
        'option_a': 'a is positive', 'option_b': 'a is negative', 'option_c': 'a is zero', 'option_d': 'Cannot determine',
        'correct_answer': 'B', 'explanation': 'For a/b to be negative with b positive, a must be negative. Negative ÷ positive = negative.',
        'topic_tag': 'rational_number_reasoning',
    },

    # --- Expressions & Equations (4 questions) ---
    {
        'track': 'grade_7', 'sat_domain': 'expressions_equations', 'fuar_dimension': 'F', 'difficulty': 2,
        'question_text': 'Solve: 3x - 7 = 14',
        'option_a': 'x = 3', 'option_b': 'x = 7', 'option_c': 'x = 7/3', 'option_d': 'x = 21',
        'correct_answer': 'B', 'explanation': '3x - 7 = 14 → 3x = 21 → x = 7.',
        'topic_tag': 'solving_equations',
    },
    {
        'track': 'grade_7', 'sat_domain': 'expressions_equations', 'fuar_dimension': 'U', 'difficulty': 3,
        'question_text': 'When we solve 2(x + 3) = 14, why do we distribute the 2 first?',
        'option_a': 'Because multiplication comes before addition in PEMDAS', 'option_b': 'Because we need to isolate x by removing the parentheses',
        'option_c': 'Because we always multiply before dividing', 'option_d': 'Because 2 is the largest number',
        'correct_answer': 'B', 'explanation': 'Distributing removes parentheses so we can isolate x: 2x + 6 = 14 → 2x = 8 → x = 4. Alternatively, divide both sides by 2 first.',
        'topic_tag': 'equation_concepts',
    },
    {
        'track': 'grade_7', 'sat_domain': 'expressions_equations', 'fuar_dimension': 'A', 'difficulty': 3,
        'question_text': 'A phone plan costs $30/month plus $0.10 per text. If the bill was $37, how many texts were sent?',
        'option_a': '7', 'option_b': '37', 'option_c': '70', 'option_d': '370',
        'correct_answer': 'C', 'explanation': '30 + 0.10t = 37 → 0.10t = 7 → t = 70 texts.',
        'topic_tag': 'equation_word_problems',
    },
    {
        'track': 'grade_7', 'sat_domain': 'expressions_equations', 'fuar_dimension': 'R', 'difficulty': 4,
        'question_text': 'If 5x + 3 > 2x + 15, which values of x are solutions?',
        'option_a': 'x > 4', 'option_b': 'x > 3', 'option_c': 'x < 4', 'option_d': 'x > 6',
        'correct_answer': 'A', 'explanation': '5x + 3 > 2x + 15 → 3x > 12 → x > 4.',
        'topic_tag': 'inequality_reasoning',
    },

    # --- Geometry: Circles & Angles (4 questions) ---
    {
        'track': 'grade_7', 'sat_domain': 'geometry_circles_angles', 'fuar_dimension': 'F', 'difficulty': 2,
        'question_text': 'Two angles are supplementary. One measures 65°. What is the other angle?',
        'option_a': '25°', 'option_b': '65°', 'option_c': '115°', 'option_d': '295°',
        'correct_answer': 'C', 'explanation': 'Supplementary angles add to 180°. 180 - 65 = 115°.',
        'topic_tag': 'angle_relationships',
    },
    {
        'track': 'grade_7', 'sat_domain': 'geometry_circles_angles', 'fuar_dimension': 'U', 'difficulty': 3,
        'question_text': 'Why is the area of a circle π r² and not π d²?',
        'option_a': 'Because r is always smaller than d', 'option_b': 'Because the formula uses the radius, not the diameter',
        'option_c': 'Because using d² would give 4 times the correct area', 'option_d': 'Both B and C are correct',
        'correct_answer': 'D', 'explanation': 'The formula is defined using radius. If you used diameter: π(d)² = π(2r)² = 4πr², which is 4x too large.',
        'topic_tag': 'circle_concepts',
    },
    {
        'track': 'grade_7', 'sat_domain': 'geometry_circles_angles', 'fuar_dimension': 'A', 'difficulty': 3,
        'question_text': 'A circular garden has a radius of 7 feet. How much fencing is needed to go around it? (Use π ≈ 22/7)',
        'option_a': '22 feet', 'option_b': '44 feet', 'option_c': '154 feet', 'option_d': '88 feet',
        'correct_answer': 'B', 'explanation': 'Circumference = 2πr = 2 × (22/7) × 7 = 44 feet.',
        'topic_tag': 'circle_applications',
    },
    {
        'track': 'grade_7', 'sat_domain': 'geometry_circles_angles', 'fuar_dimension': 'R', 'difficulty': 4,
        'question_text': 'If you double the radius of a circle, what happens to its area?',
        'option_a': 'It doubles', 'option_b': 'It triples', 'option_c': 'It quadruples', 'option_d': 'It increases by π',
        'correct_answer': 'C', 'explanation': 'Area = πr². If r → 2r: π(2r)² = 4πr². The area quadruples (multiplied by 4).',
        'topic_tag': 'geometric_reasoning',
    },

    # --- Probability & Statistics (4 questions) ---
    {
        'track': 'grade_7', 'sat_domain': 'probability_statistics', 'fuar_dimension': 'F', 'difficulty': 2,
        'question_text': 'A bag has 3 red and 5 blue marbles. What is the probability of drawing a red marble?',
        'option_a': '3/5', 'option_b': '3/8', 'option_c': '5/8', 'option_d': '5/3',
        'correct_answer': 'B', 'explanation': 'P(red) = favorable/total = 3/8.',
        'topic_tag': 'basic_probability',
    },
    {
        'track': 'grade_7', 'sat_domain': 'probability_statistics', 'fuar_dimension': 'U', 'difficulty': 3,
        'question_text': 'An event has probability 0. What does this mean?',
        'option_a': 'It is very unlikely', 'option_b': 'It is impossible', 'option_c': 'It happens about half the time', 'option_d': 'It is certain',
        'correct_answer': 'B', 'explanation': 'P = 0 means the event cannot occur. P = 1 means it is certain.',
        'topic_tag': 'probability_concepts',
    },
    {
        'track': 'grade_7', 'sat_domain': 'probability_statistics', 'fuar_dimension': 'A', 'difficulty': 3,
        'question_text': 'A spinner has 4 equal sections: red, blue, green, yellow. If you spin 200 times, about how many times would you expect to land on blue?',
        'option_a': '25', 'option_b': '40', 'option_c': '50', 'option_d': '100',
        'correct_answer': 'C', 'explanation': 'P(blue) = 1/4. Expected: 200 × 1/4 = 50 times.',
        'topic_tag': 'experimental_probability',
    },
    {
        'track': 'grade_7', 'sat_domain': 'probability_statistics', 'fuar_dimension': 'R', 'difficulty': 4,
        'question_text': 'You flip a coin 3 times. What is the probability of getting exactly 2 heads?',
        'option_a': '1/4', 'option_b': '1/3', 'option_c': '3/8', 'option_d': '1/2',
        'correct_answer': 'C', 'explanation': 'Total outcomes: 2³ = 8. Exactly 2 heads: HHT, HTH, THH = 3 ways. P = 3/8.',
        'topic_tag': 'compound_probability',
    },

    # --- Inequalities (4 questions) ---
    {
        'track': 'grade_7', 'sat_domain': 'inequalities', 'fuar_dimension': 'F', 'difficulty': 2,
        'question_text': 'Solve: x + 5 > 12',
        'option_a': 'x > 7', 'option_b': 'x > 17', 'option_c': 'x < 7', 'option_d': 'x = 7',
        'correct_answer': 'A', 'explanation': 'x + 5 > 12 → x > 7.',
        'topic_tag': 'solving_inequalities',
    },
    {
        'track': 'grade_7', 'sat_domain': 'inequalities', 'fuar_dimension': 'U', 'difficulty': 3,
        'question_text': 'When you multiply both sides of an inequality by a negative number, what happens to the inequality sign?',
        'option_a': 'It stays the same', 'option_b': 'It reverses direction', 'option_c': 'It becomes an equals sign', 'option_d': 'It disappears',
        'correct_answer': 'B', 'explanation': 'Multiplying or dividing by a negative reverses the inequality. For example: -2 < 3, but multiplying both by -1 gives 2 > -3.',
        'topic_tag': 'inequality_concepts',
    },
    {
        'track': 'grade_7', 'sat_domain': 'inequalities', 'fuar_dimension': 'A', 'difficulty': 3,
        'question_text': 'A roller coaster requires riders to be at least 48 inches tall. Which inequality represents this?',
        'option_a': 'h < 48', 'option_b': 'h > 48', 'option_c': 'h ≥ 48', 'option_d': 'h ≤ 48',
        'correct_answer': 'C', 'explanation': '"At least 48" means 48 or more, so h ≥ 48.',
        'topic_tag': 'inequality_word_problems',
    },
    {
        'track': 'grade_7', 'sat_domain': 'inequalities', 'fuar_dimension': 'R', 'difficulty': 4,
        'question_text': 'If -2x + 1 ≤ 7 and x is a positive integer, what is the smallest possible value of x?',
        'option_a': '1', 'option_b': '2', 'option_c': '3', 'option_d': '-3',
        'correct_answer': 'A', 'explanation': '-2x + 1 ≤ 7 → -2x ≤ 6 → x ≥ -3 (reverse inequality when dividing by negative). Smallest positive integer is 1.',
        'topic_tag': 'inequality_reasoning',
    },

    # ===== BATCH 2: F=1, U=2, A=4, R=5 =====

    # --- Proportional Relationships — Batch 2 (4 questions) ---
    {
        'track': 'grade_7', 'sat_domain': 'proportional_relationships', 'fuar_dimension': 'F', 'difficulty': 1,
        'question_text': 'A car travels 60 miles in 1 hour. How far does it travel in 3 hours at the same speed?',
        'option_a': '20 miles', 'option_b': '63 miles', 'option_c': '120 miles', 'option_d': '180 miles',
        'correct_answer': 'D', 'explanation': 'Distance = speed × time. 60 × 3 = 180 miles.',
        'topic_tag': 'unit_rates',
    },
    {
        'track': 'grade_7', 'sat_domain': 'proportional_relationships', 'fuar_dimension': 'U', 'difficulty': 2,
        'question_text': 'In a proportional relationship y = kx, what does the constant k represent?',
        'option_a': 'The starting value', 'option_b': 'The unit rate (how much y changes per 1 unit of x)', 'option_c': 'The total value of y', 'option_d': 'The difference between y and x',
        'correct_answer': 'B', 'explanation': 'k is the constant of proportionality, also called the unit rate. It tells you how much y increases for every 1-unit increase in x.',
        'topic_tag': 'proportionality_concepts',
    },
    {
        'track': 'grade_7', 'sat_domain': 'proportional_relationships', 'fuar_dimension': 'A', 'difficulty': 4,
        'question_text': 'A recipe calls for 2.5 cups of flour for every 12 cookies. A baker wants to make 84 cookies. How many cups of flour are needed?',
        'option_a': '14 cups', 'option_b': '15.5 cups', 'option_c': '17.5 cups', 'option_d': '21 cups',
        'correct_answer': 'C', 'explanation': 'Unit rate: 2.5/12 cups per cookie. For 84 cookies: 84 × (2.5/12) = 84 × 0.2083... = 17.5 cups.',
        'topic_tag': 'scale_drawings',
    },
    {
        'track': 'grade_7', 'sat_domain': 'proportional_relationships', 'fuar_dimension': 'R', 'difficulty': 5,
        'question_text': 'Two friends drive toward each other from towns 300 miles apart. Friend A drives at 50 mph and Friend B at 70 mph. After how many hours do they meet?',
        'option_a': '2 hours', 'option_b': '2.5 hours', 'option_c': '3 hours', 'option_d': '4.3 hours',
        'correct_answer': 'B', 'explanation': 'Their combined speed is 50 + 70 = 120 mph. Time = 300/120 = 2.5 hours.',
        'topic_tag': 'proportional_reasoning',
    },

    # --- Rational Numbers — Batch 2 (4 questions) ---
    {
        'track': 'grade_7', 'sat_domain': 'rational_numbers', 'fuar_dimension': 'F', 'difficulty': 1,
        'question_text': 'What is the absolute value of -9?',
        'option_a': '-9', 'option_b': '-1/9', 'option_c': '1/9', 'option_d': '9',
        'correct_answer': 'D', 'explanation': 'Absolute value is the distance from zero, always non-negative. |-9| = 9.',
        'topic_tag': 'integer_operations',
    },
    {
        'track': 'grade_7', 'sat_domain': 'rational_numbers', 'fuar_dimension': 'U', 'difficulty': 2,
        'question_text': 'Which of these represents the same value as -3/4?',
        'option_a': '3/(-4)', 'option_b': '-(3/4)', 'option_c': '(-3)/4', 'option_d': 'All of the above',
        'correct_answer': 'D', 'explanation': 'A negative sign on a fraction can be placed in the numerator, denominator, or in front. All three: 3/(-4), -(3/4), and (-3)/4 equal -3/4.',
        'topic_tag': 'rational_number_concepts',
    },
    {
        'track': 'grade_7', 'sat_domain': 'rational_numbers', 'fuar_dimension': 'A', 'difficulty': 4,
        'question_text': 'The temperature at midnight was -8°F. By noon, it had risen 15°F, then dropped 4°F by evening. What was the evening temperature?',
        'option_a': '-11°F', 'option_b': '3°F', 'option_c': '7°F', 'option_d': '11°F',
        'correct_answer': 'B', 'explanation': 'Start: -8. After rise: -8 + 15 = 7. After drop: 7 - 4 = 3°F.',
        'topic_tag': 'rational_number_applications',
    },
    {
        'track': 'grade_7', 'sat_domain': 'rational_numbers', 'fuar_dimension': 'R', 'difficulty': 5,
        'question_text': 'If p and q are both negative integers, which expression is always positive?',
        'option_a': 'p + q', 'option_b': 'p - q', 'option_c': 'p × q', 'option_d': 'p ÷ q',
        'correct_answer': 'C', 'explanation': 'Negative × negative = positive, so p × q is always positive. p + q is always negative. p - q and p ÷ q could be positive or negative depending on the values.',
        'topic_tag': 'rational_number_reasoning',
    },

    # --- Expressions & Equations — Batch 2 (4 questions) ---
    {
        'track': 'grade_7', 'sat_domain': 'expressions_equations', 'fuar_dimension': 'F', 'difficulty': 1,
        'question_text': 'What is the value of 4x - 3 when x = 5?',
        'option_a': '7', 'option_b': '17', 'option_c': '20', 'option_d': '23',
        'correct_answer': 'B', 'explanation': 'Substitute x = 5: 4(5) - 3 = 20 - 3 = 17.',
        'topic_tag': 'evaluating_expressions',
    },
    {
        'track': 'grade_7', 'sat_domain': 'expressions_equations', 'fuar_dimension': 'U', 'difficulty': 2,
        'question_text': 'Which expression is equivalent to 3(2x - 4)?',
        'option_a': '6x - 4', 'option_b': '5x - 7', 'option_c': '6x - 12', 'option_d': '6x + 12',
        'correct_answer': 'C', 'explanation': 'Distribute the 3: 3 × 2x = 6x and 3 × (-4) = -12. Result: 6x - 12.',
        'topic_tag': 'equation_concepts',
    },
    {
        'track': 'grade_7', 'sat_domain': 'expressions_equations', 'fuar_dimension': 'A', 'difficulty': 4,
        'question_text': 'A rectangle\'s length is 3 more than twice its width. If the perimeter is 48 cm, what is the width?',
        'option_a': '5 cm', 'option_b': '7 cm', 'option_c': '9 cm', 'option_d': '11 cm',
        'correct_answer': 'B', 'explanation': 'Width = w, Length = 2w + 3. Perimeter: 2(w + 2w + 3) = 48 → 2(3w + 3) = 48 → 6w + 6 = 48 → 6w = 42 → w = 7 cm.',
        'topic_tag': 'equation_word_problems',
    },
    {
        'track': 'grade_7', 'sat_domain': 'expressions_equations', 'fuar_dimension': 'R', 'difficulty': 5,
        'question_text': 'If 3(x - 2) = 2(x + 5), what is x?',
        'option_a': 'x = 4', 'option_b': 'x = 10', 'option_c': 'x = 16', 'option_d': 'x = 20',
        'correct_answer': 'C', 'explanation': '3x - 6 = 2x + 10 → 3x - 2x = 10 + 6 → x = 16.',
        'topic_tag': 'multi_step_equations',
    },

    # --- Geometry: Circles & Angles — Batch 2 (4 questions) ---
    {
        'track': 'grade_7', 'sat_domain': 'geometry_circles_angles', 'fuar_dimension': 'F', 'difficulty': 1,
        'question_text': 'Two angles are complementary. One measures 35°. What is the other angle?',
        'option_a': '35°', 'option_b': '45°', 'option_c': '55°', 'option_d': '145°',
        'correct_answer': 'C', 'explanation': 'Complementary angles add to 90°. 90 - 35 = 55°.',
        'topic_tag': 'angle_relationships',
    },
    {
        'track': 'grade_7', 'sat_domain': 'geometry_circles_angles', 'fuar_dimension': 'U', 'difficulty': 2,
        'question_text': 'What is the difference between the diameter and the radius of a circle?',
        'option_a': 'The diameter is the distance around the circle; the radius goes to the center', 'option_b': 'The diameter passes through the center connecting two points; the radius goes from center to edge', 'option_c': 'The radius is twice the diameter', 'option_d': 'They are the same thing with different names',
        'correct_answer': 'B', 'explanation': 'The diameter is a chord that passes through the center (d = 2r). The radius goes from the center to any point on the circle (r = d/2).',
        'topic_tag': 'circle_concepts',
    },
    {
        'track': 'grade_7', 'sat_domain': 'geometry_circles_angles', 'fuar_dimension': 'A', 'difficulty': 4,
        'question_text': 'A circular pizza has a diameter of 14 inches. What is the area of the pizza? (Use π ≈ 22/7)',
        'option_a': '44 sq in', 'option_b': '88 sq in', 'option_c': '154 sq in', 'option_d': '616 sq in',
        'correct_answer': 'C', 'explanation': 'Radius = 14/2 = 7 inches. Area = πr² = (22/7) × 7² = (22/7) × 49 = 22 × 7 = 154 sq in.',
        'topic_tag': 'circle_applications',
    },
    {
        'track': 'grade_7', 'sat_domain': 'geometry_circles_angles', 'fuar_dimension': 'R', 'difficulty': 5,
        'question_text': 'A triangle has angles in the ratio 2:3:5. What is the measure of the largest angle?',
        'option_a': '36°', 'option_b': '54°', 'option_c': '72°', 'option_d': '90°',
        'correct_answer': 'D', 'explanation': 'Angles sum to 180°. Parts: 2 + 3 + 5 = 10. Each part = 180/10 = 18°. Largest angle: 5 × 18 = 90°.',
        'topic_tag': 'geometric_reasoning',
    },

    # --- Probability & Statistics — Batch 2 (4 questions) ---
    {
        'track': 'grade_7', 'sat_domain': 'probability_statistics', 'fuar_dimension': 'F', 'difficulty': 1,
        'question_text': 'A die has 6 faces numbered 1–6. What is the probability of rolling a 4?',
        'option_a': '1/4', 'option_b': '1/6', 'option_c': '4/6', 'option_d': '4',
        'correct_answer': 'B', 'explanation': 'There is 1 favorable outcome (rolling a 4) out of 6 equally likely outcomes. P = 1/6.',
        'topic_tag': 'basic_probability',
    },
    {
        'track': 'grade_7', 'sat_domain': 'probability_statistics', 'fuar_dimension': 'U', 'difficulty': 2,
        'question_text': 'What is the difference between theoretical probability and experimental probability?',
        'option_a': 'Theoretical is based on what should happen; experimental is based on what actually happened in trials', 'option_b': 'Theoretical uses fractions; experimental uses decimals', 'option_c': 'They are the same thing', 'option_d': 'Experimental is always more accurate than theoretical',
        'correct_answer': 'A', 'explanation': 'Theoretical probability is calculated from equally likely outcomes (e.g., 1/6 for a fair die). Experimental probability is the ratio of observed outcomes to total trials.',
        'topic_tag': 'probability_concepts',
    },
    {
        'track': 'grade_7', 'sat_domain': 'probability_statistics', 'fuar_dimension': 'A', 'difficulty': 4,
        'question_text': 'A class survey shows 12 students prefer soccer, 8 prefer basketball, and 5 prefer tennis. If a student is chosen at random, what is the probability they prefer soccer or basketball?',
        'option_a': '12/25', 'option_b': '4/5', 'option_c': '8/25', 'option_d': '3/5',
        'correct_answer': 'B', 'explanation': 'Total students: 12 + 8 + 5 = 25. Soccer or basketball: 12 + 8 = 20. P = 20/25 = 4/5.',
        'topic_tag': 'experimental_probability',
    },
    {
        'track': 'grade_7', 'sat_domain': 'probability_statistics', 'fuar_dimension': 'R', 'difficulty': 5,
        'question_text': 'A bag has 4 red, 3 blue, and 3 green marbles. You draw one marble, do NOT replace it, then draw another. What is the probability that both marbles are red?',
        'option_a': '2/15', 'option_b': '4/25', 'option_c': '8/45', 'option_d': '16/100',
        'correct_answer': 'A', 'explanation': 'P(first red) = 4/10. After removing one red, P(second red) = 3/9. P(both red) = (4/10) × (3/9) = 12/90 = 2/15.',
        'topic_tag': 'compound_probability',
    },

    # --- Inequalities — Batch 2 (4 questions) ---
    {
        'track': 'grade_7', 'sat_domain': 'inequalities', 'fuar_dimension': 'F', 'difficulty': 1,
        'question_text': 'Which number is a solution to x < 5?',
        'option_a': '5', 'option_b': '6', 'option_c': '4', 'option_d': '10',
        'correct_answer': 'C', 'explanation': 'x < 5 means x must be less than 5. Only 4 satisfies this — 5 is not less than 5.',
        'topic_tag': 'solving_inequalities',
    },
    {
        'track': 'grade_7', 'sat_domain': 'inequalities', 'fuar_dimension': 'U', 'difficulty': 2,
        'question_text': 'On a number line, how is the solution to x ≥ 3 represented differently from x > 3?',
        'option_a': 'x ≥ 3 uses an open circle at 3; x > 3 uses a closed circle', 'option_b': 'x ≥ 3 uses a closed circle at 3; x > 3 uses an open circle', 'option_c': 'Both use open circles', 'option_d': 'Both use closed circles',
        'correct_answer': 'B', 'explanation': 'A closed circle means the endpoint IS included (≥ or ≤). An open circle means it is NOT included (> or <). x ≥ 3 includes 3 (closed); x > 3 does not (open).',
        'topic_tag': 'inequality_concepts',
    },
    {
        'track': 'grade_7', 'sat_domain': 'inequalities', 'fuar_dimension': 'A', 'difficulty': 4,
        'question_text': 'A store charges $5 per item plus a $2 shipping fee. You want to spend at most $32. What is the maximum number of items you can buy?',
        'option_a': '5 items', 'option_b': '6 items', 'option_c': '7 items', 'option_d': '8 items',
        'correct_answer': 'B', 'explanation': '5n + 2 ≤ 32 → 5n ≤ 30 → n ≤ 6. Maximum is 6 items.',
        'topic_tag': 'inequality_word_problems',
    },
    {
        'track': 'grade_7', 'sat_domain': 'inequalities', 'fuar_dimension': 'R', 'difficulty': 5,
        'question_text': 'Sam needs to save more than $50. He already has $14 and earns $6 per hour babysitting. He also owes a $2 fee. Which inequality correctly models the minimum hours h he must work?',
        'option_a': '6h - 2 > 50', 'option_b': '6h + 14 - 2 > 50', 'option_c': '6h + 14 > 50', 'option_d': '6h > 50',
        'correct_answer': 'B', 'explanation': 'Total savings = 14 + 6h - 2 > 50. Simplify: 6h + 12 > 50 → 6h > 38 → h > 6.33, so at least 7 hours. Option B correctly includes starting savings ($14) and the fee (-$2).',
        'topic_tag': 'inequality_reasoning',
    },
]


def seed():
    conn = sqlite3.connect(DB_PATH)
    existing = conn.execute("SELECT COUNT(*) FROM questions WHERE track = 'grade_7'").fetchone()[0]
    if existing > 0:
        print(f"[Grade 7] Already has {existing} questions. Skipping seed.")
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
    count = conn.execute("SELECT COUNT(*) FROM questions WHERE track = 'grade_7'").fetchone()[0]
    print(f"[Grade 7] Seeded {count} questions.")
    conn.close()
    return count


if __name__ == '__main__':
    seed()
