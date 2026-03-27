"""Seed Grade 8 Math questions — Algebra Ready track.
48 questions across 6 content areas, balanced across FUAR dimensions.
Focus: Linear equations/systems, functions, exponents/radicals, transformations, data modeling.
Original 24: F=2, U=3, A=3, R=4 per area.
Added 24: F=1, U=2, A=4, R=5 per area (widens MST difficulty range).
"""

import sqlite3
import os

DB_PATH = os.environ.get('DATABASE_PATH', 'college_ready.db')

QUESTIONS = [
    # --- Linear Equations & Systems (4 questions) ---
    {
        'track': 'grade_8', 'sat_domain': 'linear_equations_systems', 'fuar_dimension': 'F', 'difficulty': 2,
        'question_text': 'Solve: 4x - 3 = 2x + 9',
        'option_a': 'x = 3', 'option_b': 'x = 6', 'option_c': 'x = -3', 'option_d': 'x = 12',
        'correct_answer': 'B', 'explanation': '4x - 3 = 2x + 9 → 2x = 12 → x = 6.',
        'topic_tag': 'multi_step_equations',
    },
    {
        'track': 'grade_8', 'sat_domain': 'linear_equations_systems', 'fuar_dimension': 'U', 'difficulty': 3,
        'question_text': 'A system of two linear equations has no solution. What does this mean graphically?',
        'option_a': 'The lines intersect at one point', 'option_b': 'The lines are the same line',
        'option_c': 'The lines are parallel (never intersect)', 'option_d': 'The lines are perpendicular',
        'correct_answer': 'C', 'explanation': 'No solution means no point satisfies both equations — the lines never meet, so they are parallel.',
        'topic_tag': 'systems_concepts',
    },
    {
        'track': 'grade_8', 'sat_domain': 'linear_equations_systems', 'fuar_dimension': 'A', 'difficulty': 3,
        'question_text': 'Two friends are saving money. Alex has $50 and saves $15/week. Jordan has $110 and saves $5/week. When will they have the same amount?',
        'option_a': '4 weeks', 'option_b': '6 weeks', 'option_c': '8 weeks', 'option_d': '10 weeks',
        'correct_answer': 'B', 'explanation': '50 + 15w = 110 + 5w → 10w = 60 → w = 6 weeks.',
        'topic_tag': 'systems_word_problems',
    },
    {
        'track': 'grade_8', 'sat_domain': 'linear_equations_systems', 'fuar_dimension': 'R', 'difficulty': 4,
        'question_text': 'The equation 3(x - 2) = 3x - 6 has how many solutions?',
        'option_a': 'No solution', 'option_b': 'Exactly one solution', 'option_c': 'Exactly two solutions', 'option_d': 'Infinitely many solutions',
        'correct_answer': 'D', 'explanation': '3x - 6 = 3x - 6 is always true. Every value of x is a solution — infinitely many.',
        'topic_tag': 'equation_reasoning',
    },

    # --- Functions (4 questions) ---
    {
        'track': 'grade_8', 'sat_domain': 'functions', 'fuar_dimension': 'F', 'difficulty': 2,
        'question_text': 'If f(x) = 2x + 5, what is f(3)?',
        'option_a': '8', 'option_b': '11', 'option_c': '16', 'option_d': '6',
        'correct_answer': 'B', 'explanation': 'f(3) = 2(3) + 5 = 6 + 5 = 11.',
        'topic_tag': 'function_evaluation',
    },
    {
        'track': 'grade_8', 'sat_domain': 'functions', 'fuar_dimension': 'U', 'difficulty': 3,
        'question_text': 'Is the set of ordered pairs {(1,3), (2,5), (3,7), (1,4)} a function? Why or why not?',
        'option_a': 'Yes, because all y-values are different', 'option_b': 'Yes, because it has four pairs',
        'option_c': 'No, because the input 1 has two different outputs (3 and 4)', 'option_d': 'No, because the outputs are odd numbers',
        'correct_answer': 'C', 'explanation': 'A function assigns exactly one output to each input. Since x=1 maps to both y=3 and y=4, this is not a function.',
        'topic_tag': 'function_definition',
    },
    {
        'track': 'grade_8', 'sat_domain': 'functions', 'fuar_dimension': 'A', 'difficulty': 3,
        'question_text': 'A taxi charges $3 base fare plus $2 per mile. Write the function for total cost C as a function of miles m, and find the cost for 8 miles.',
        'option_a': 'C = 2m + 3; $19', 'option_b': 'C = 3m + 2; $26', 'option_c': 'C = 5m; $40', 'option_d': 'C = 2m + 3; $16',
        'correct_answer': 'A', 'explanation': 'C(m) = 2m + 3. C(8) = 2(8) + 3 = 16 + 3 = 19.',
        'topic_tag': 'linear_functions',
    },
    {
        'track': 'grade_8', 'sat_domain': 'functions', 'fuar_dimension': 'R', 'difficulty': 4,
        'question_text': 'A function has a rate of change of 4 and passes through (2, 11). What is the y-intercept?',
        'option_a': '1', 'option_b': '3', 'option_c': '7', 'option_d': '11',
        'correct_answer': 'B', 'explanation': 'y = 4x + b. Plug in (2,11): 11 = 4(2) + b → 11 = 8 + b → b = 3. Y-intercept is 3.',
        'topic_tag': 'function_reasoning',
    },

    # --- Exponents & Radicals (4 questions) ---
    {
        'track': 'grade_8', 'sat_domain': 'exponents_radicals', 'fuar_dimension': 'F', 'difficulty': 2,
        'question_text': 'Simplify: 2³ × 2⁴',
        'option_a': '2⁷', 'option_b': '2¹²', 'option_c': '4⁷', 'option_d': '2¹',
        'correct_answer': 'A', 'explanation': 'When multiplying with the same base, add exponents: 2³⁺⁴ = 2⁷ = 128.',
        'topic_tag': 'exponent_rules',
    },
    {
        'track': 'grade_8', 'sat_domain': 'exponents_radicals', 'fuar_dimension': 'U', 'difficulty': 3,
        'question_text': 'Why does any non-zero number raised to the power of 0 equal 1?',
        'option_a': 'Because 0 is the identity element', 'option_b': 'Because x^n ÷ x^n = x^(n-n) = x^0 = 1',
        'option_c': 'Because zero means nothing', 'option_d': 'It\'s just a rule with no reason',
        'correct_answer': 'B', 'explanation': 'x^n ÷ x^n = 1 (anything divided by itself). But the exponent rule gives x^(n-n) = x^0. So x^0 must equal 1.',
        'topic_tag': 'exponent_concepts',
    },
    {
        'track': 'grade_8', 'sat_domain': 'exponents_radicals', 'fuar_dimension': 'A', 'difficulty': 3,
        'question_text': 'A bacteria population doubles every hour. If it starts at 100, how many bacteria are there after 5 hours?',
        'option_a': '500', 'option_b': '1,000', 'option_c': '3,200', 'option_d': '10,000',
        'correct_answer': 'C', 'explanation': 'Population = 100 × 2⁵ = 100 × 32 = 3,200.',
        'topic_tag': 'exponential_growth',
    },
    {
        'track': 'grade_8', 'sat_domain': 'exponents_radicals', 'fuar_dimension': 'R', 'difficulty': 4,
        'question_text': 'If 3^x = 81, what is 3^(x+1)?',
        'option_a': '82', 'option_b': '162', 'option_c': '243', 'option_d': '324',
        'correct_answer': 'C', 'explanation': '3^x = 81, so 3^(x+1) = 3^x × 3 = 81 × 3 = 243. No need to find x.',
        'topic_tag': 'exponent_reasoning',
    },

    # --- Geometry & Transformations (4 questions) ---
    {
        'track': 'grade_8', 'sat_domain': 'geometry_transformations', 'fuar_dimension': 'F', 'difficulty': 2,
        'question_text': 'What are the coordinates of point (3, -2) after reflecting over the x-axis?',
        'option_a': '(-3, -2)', 'option_b': '(3, 2)', 'option_c': '(-3, 2)', 'option_d': '(2, -3)',
        'correct_answer': 'B', 'explanation': 'Reflecting over the x-axis changes the sign of the y-coordinate: (3, -2) → (3, 2).',
        'topic_tag': 'reflections',
    },
    {
        'track': 'grade_8', 'sat_domain': 'geometry_transformations', 'fuar_dimension': 'U', 'difficulty': 3,
        'question_text': 'Which transformation changes the SIZE of a figure?',
        'option_a': 'Translation', 'option_b': 'Rotation', 'option_c': 'Reflection', 'option_d': 'Dilation',
        'correct_answer': 'D', 'explanation': 'Only dilation changes the size. Translations, rotations, and reflections are rigid motions that preserve size.',
        'topic_tag': 'transformation_concepts',
    },
    {
        'track': 'grade_8', 'sat_domain': 'geometry_transformations', 'fuar_dimension': 'A', 'difficulty': 3,
        'question_text': 'A triangle has vertices at (1,1), (4,1), and (2,5). If it is translated 3 units right and 2 units down, what are the new coordinates of the vertex that was at (2,5)?',
        'option_a': '(5, 3)', 'option_b': '(-1, 7)', 'option_c': '(5, 7)', 'option_d': '(2, 3)',
        'correct_answer': 'A', 'explanation': 'Right 3: x + 3. Down 2: y - 2. (2+3, 5-2) = (5, 3).',
        'topic_tag': 'coordinate_transformations',
    },
    {
        'track': 'grade_8', 'sat_domain': 'geometry_transformations', 'fuar_dimension': 'R', 'difficulty': 4,
        'question_text': 'Two triangles are similar with a scale factor of 3. If the area of the smaller triangle is 5 cm², what is the area of the larger triangle?',
        'option_a': '15 cm²', 'option_b': '25 cm²', 'option_c': '45 cm²', 'option_d': '125 cm²',
        'correct_answer': 'C', 'explanation': 'When lengths scale by k, areas scale by k². Scale factor 3: area scales by 3² = 9. Area = 5 × 9 = 45 cm².',
        'topic_tag': 'similarity_reasoning',
    },

    # --- Data Modeling (4 questions) ---
    {
        'track': 'grade_8', 'sat_domain': 'data_modeling', 'fuar_dimension': 'F', 'difficulty': 2,
        'question_text': 'A scatter plot shows that as study hours increase, test scores increase. This is an example of:',
        'option_a': 'No correlation', 'option_b': 'Negative correlation', 'option_c': 'Positive correlation', 'option_d': 'Causation',
        'correct_answer': 'C', 'explanation': 'When both variables increase together, it is a positive correlation.',
        'topic_tag': 'scatter_plots',
    },
    {
        'track': 'grade_8', 'sat_domain': 'data_modeling', 'fuar_dimension': 'U', 'difficulty': 3,
        'question_text': 'A line of best fit for a scatter plot has the equation y = 2x + 10. What does the slope of 2 mean in context if x = hours studied and y = test score?',
        'option_a': 'The test starts at 2 points', 'option_b': 'For each additional hour studied, the score increases by about 2 points',
        'option_c': 'You need 2 hours to pass', 'option_d': 'The maximum score is 2',
        'correct_answer': 'B', 'explanation': 'The slope represents the rate of change — each unit increase in x (1 hour) corresponds to a 2-point increase in y (score).',
        'topic_tag': 'line_of_best_fit',
    },
    {
        'track': 'grade_8', 'sat_domain': 'data_modeling', 'fuar_dimension': 'A', 'difficulty': 3,
        'question_text': 'Using the model y = 2x + 10, predict the score for a student who studies 7 hours.',
        'option_a': '17', 'option_b': '19', 'option_c': '24', 'option_d': '27',
        'correct_answer': 'C', 'explanation': 'y = 2(7) + 10 = 14 + 10 = 24.',
        'topic_tag': 'prediction',
    },
    {
        'track': 'grade_8', 'sat_domain': 'data_modeling', 'fuar_dimension': 'R', 'difficulty': 4,
        'question_text': 'A study shows a strong positive correlation between ice cream sales and drowning incidents. Does eating ice cream cause drowning?',
        'option_a': 'Yes, the correlation proves it', 'option_b': 'No — a third variable (hot weather) likely causes both',
        'option_c': 'Yes, because the correlation is strong', 'option_d': 'There is no connection at all',
        'correct_answer': 'B', 'explanation': 'Correlation does not imply causation. Hot weather is a confounding variable — it increases both ice cream sales and swimming (which increases drowning risk).',
        'topic_tag': 'correlation_vs_causation',
    },

    # --- Linear Equations & Systems — Extended (4 questions, F=1/U=2/A=4/R=5) ---
    {
        'track': 'grade_8', 'sat_domain': 'linear_equations_systems', 'fuar_dimension': 'F', 'difficulty': 1,
        'question_text': 'Which value of x makes 2x + 4 = 10 true?',
        'option_a': 'x = 2', 'option_b': 'x = 3', 'option_c': 'x = 5', 'option_d': 'x = 7',
        'correct_answer': 'B', 'explanation': '2x + 4 = 10 → 2x = 6 → x = 3.',
        'topic_tag': 'one_step_equations',
    },
    {
        'track': 'grade_8', 'sat_domain': 'linear_equations_systems', 'fuar_dimension': 'U', 'difficulty': 2,
        'question_text': 'A linear equation is graphed as a straight line. What determines how steeply that line rises or falls?',
        'option_a': 'The y-intercept', 'option_b': 'The x-intercept', 'option_c': 'The slope', 'option_d': 'The number of variables',
        'correct_answer': 'C', 'explanation': 'Slope measures the rate of change — steeper slope means the line rises or falls more quickly.',
        'topic_tag': 'slope_concepts',
    },
    {
        'track': 'grade_8', 'sat_domain': 'linear_equations_systems', 'fuar_dimension': 'A', 'difficulty': 4,
        'question_text': 'A plumber charges a $40 flat fee plus $25 per hour. An electrician charges a $10 flat fee plus $40 per hour. For how many hours will they charge the same total?',
        'option_a': '1 hour', 'option_b': '2 hours', 'option_c': '3 hours', 'option_d': '4 hours',
        'correct_answer': 'B', 'explanation': '40 + 25h = 10 + 40h → 30 = 15h → h = 2.',
        'topic_tag': 'systems_word_problems',
    },
    {
        'track': 'grade_8', 'sat_domain': 'linear_equations_systems', 'fuar_dimension': 'R', 'difficulty': 5,
        'question_text': 'The system y = 2x + 1 and y = 2x − 3 is graphed. Which statement is true?',
        'option_a': 'They intersect at (0, 1)', 'option_b': 'They intersect at (2, 5)', 'option_c': 'They never intersect because they have the same slope', 'option_d': 'They intersect at all points',
        'correct_answer': 'C', 'explanation': 'Both lines have slope 2 but different y-intercepts (1 and −3), so they are parallel and never intersect — no solution.',
        'topic_tag': 'systems_reasoning',
    },

    # --- Functions — Extended (4 questions, F=1/U=2/A=4/R=5) ---
    {
        'track': 'grade_8', 'sat_domain': 'functions', 'fuar_dimension': 'F', 'difficulty': 1,
        'question_text': 'Which of the following tables represents a function?',
        'option_a': 'x: 1,1,2,3 → y: 5,6,7,8 (x=1 gives two outputs)', 'option_b': 'x: 1,2,3,4 → y: 5,5,5,5 (every x gives y=5)', 'option_c': 'x: 1,2,2,3 → y: 4,5,6,7 (x=2 gives two outputs)', 'option_d': 'x: 1,2,3,1 → y: 4,5,6,7 (x=1 gives two outputs)',
        'correct_answer': 'B', 'explanation': 'A function requires each input to have exactly one output. Only option B has unique inputs — even though all outputs are the same, each x maps to exactly one y.',
        'topic_tag': 'function_definition',
    },
    {
        'track': 'grade_8', 'sat_domain': 'functions', 'fuar_dimension': 'U', 'difficulty': 2,
        'question_text': 'On a graph of a function, what does the y-intercept represent?',
        'option_a': 'The slope of the function', 'option_b': 'The output when the input is zero', 'option_c': 'The maximum value of the function', 'option_d': 'The input when the output is zero',
        'correct_answer': 'B', 'explanation': 'The y-intercept is the point where x = 0, so it represents the output (y-value) when the input is zero.',
        'topic_tag': 'function_concepts',
    },
    {
        'track': 'grade_8', 'sat_domain': 'functions', 'fuar_dimension': 'A', 'difficulty': 4,
        'question_text': 'Function f(x) = −3x + 12. For what value of x does f(x) = 0? What does this point represent on the graph?',
        'option_a': 'x = 4; the x-intercept', 'option_b': 'x = 12; the y-intercept', 'option_c': 'x = −4; the x-intercept', 'option_d': 'x = 3; the origin',
        'correct_answer': 'A', 'explanation': '−3x + 12 = 0 → −3x = −12 → x = 4. When f(x) = 0, that is the x-intercept of the graph.',
        'topic_tag': 'function_zeros',
    },
    {
        'track': 'grade_8', 'sat_domain': 'functions', 'fuar_dimension': 'R', 'difficulty': 5,
        'question_text': 'f(x) = 5x − 3 and g(x) = 2x + 9. For what value of x does f(x) = g(x)?',
        'option_a': 'x = 2', 'option_b': 'x = 3', 'option_c': 'x = 4', 'option_d': 'x = 6',
        'correct_answer': 'C', 'explanation': 'Set equal: 5x − 3 = 2x + 9 → 3x = 12 → x = 4. This is the intersection point of the two functions.',
        'topic_tag': 'function_intersection',
    },

    # --- Exponents & Radicals — Extended (4 questions, F=1/U=2/A=4/R=5) ---
    {
        'track': 'grade_8', 'sat_domain': 'exponents_radicals', 'fuar_dimension': 'F', 'difficulty': 1,
        'question_text': 'What is the value of 5²?',
        'option_a': '10', 'option_b': '25', 'option_c': '52', 'option_d': '7',
        'correct_answer': 'B', 'explanation': '5² = 5 × 5 = 25.',
        'topic_tag': 'exponent_basics',
    },
    {
        'track': 'grade_8', 'sat_domain': 'exponents_radicals', 'fuar_dimension': 'U', 'difficulty': 2,
        'question_text': 'What does a negative exponent mean? For example, 2⁻³ = ?',
        'option_a': '−8', 'option_b': '−6', 'option_c': '1/8', 'option_d': '1/6',
        'correct_answer': 'C', 'explanation': 'A negative exponent means the reciprocal: 2⁻³ = 1/2³ = 1/8.',
        'topic_tag': 'negative_exponents',
    },
    {
        'track': 'grade_8', 'sat_domain': 'exponents_radicals', 'fuar_dimension': 'A', 'difficulty': 4,
        'question_text': 'Simplify: (3²)³ ÷ 3²',
        'option_a': '3²', 'option_b': '3⁴', 'option_c': '3⁵', 'option_d': '3⁶',
        'correct_answer': 'B', 'explanation': '(3²)³ = 3⁶ (power rule: multiply exponents). Then 3⁶ ÷ 3² = 3⁴ (quotient rule: subtract exponents).',
        'topic_tag': 'exponent_rules',
    },
    {
        'track': 'grade_8', 'sat_domain': 'exponents_radicals', 'fuar_dimension': 'R', 'difficulty': 5,
        'question_text': 'The expression √(75) can be simplified to a form a√b where a and b are integers and b has no perfect-square factor. What is a + b?',
        'option_a': '5', 'option_b': '8', 'option_c': '10', 'option_d': '18',
        'correct_answer': 'B', 'explanation': '√75 = √(25 × 3) = 5√3. So a = 5 and b = 3. a + b = 5 + 3 = 8.',
        'topic_tag': 'radical_simplification',
    },

    # --- Geometry & Transformations — Extended (4 questions, F=1/U=2/A=4/R=5) ---
    {
        'track': 'grade_8', 'sat_domain': 'geometry_transformations', 'fuar_dimension': 'F', 'difficulty': 1,
        'question_text': 'Point A is at (2, 5). If it is translated 4 units to the right, what are the new coordinates?',
        'option_a': '(6, 5)', 'option_b': '(2, 9)', 'option_c': '(−2, 5)', 'option_d': '(6, 1)',
        'correct_answer': 'A', 'explanation': 'Translating right adds to the x-coordinate: (2 + 4, 5) = (6, 5).',
        'topic_tag': 'translations',
    },
    {
        'track': 'grade_8', 'sat_domain': 'geometry_transformations', 'fuar_dimension': 'U', 'difficulty': 2,
        'question_text': 'After any rigid transformation (translation, rotation, or reflection), what is preserved?',
        'option_a': 'The position of the figure', 'option_b': 'The orientation of the figure', 'option_c': 'The size and shape (congruence) of the figure', 'option_d': 'The coordinates of every point',
        'correct_answer': 'C', 'explanation': 'Rigid transformations do not change the size or shape — the figure before and after is congruent. Position and orientation may change.',
        'topic_tag': 'transformation_concepts',
    },
    {
        'track': 'grade_8', 'sat_domain': 'geometry_transformations', 'fuar_dimension': 'A', 'difficulty': 4,
        'question_text': 'Triangle ABC has vertices A(0,0), B(4,0), C(0,3). It is dilated by a scale factor of 2 centered at the origin. What is the perimeter of the new triangle?',
        'option_a': '7 units', 'option_b': '12 units', 'option_c': '14 units', 'option_d': '24 units',
        'correct_answer': 'D', 'explanation': 'Original triangle is a 3-4-5 right triangle: AB=4, AC=3, BC=5. Perimeter=12. Dilation by scale factor 2 multiplies every side length by 2. New sides: 8, 6, 10. New perimeter = 24 units.',
        'topic_tag': 'dilation_applications',
    },
    {
        'track': 'grade_8', 'sat_domain': 'geometry_transformations', 'fuar_dimension': 'R', 'difficulty': 5,
        'question_text': 'A figure is rotated 90° clockwise about the origin. The rule for this transformation is (x, y) → (y, −x). If point P is at (−3, 4), where does it land?',
        'option_a': '(−4, −3)', 'option_b': '(4, 3)', 'option_c': '(3, 4)', 'option_d': '(−3, −4)',
        'correct_answer': 'B', 'explanation': 'Apply (x, y) → (y, −x): (−3, 4) → (4, −(−3)) = (4, 3).',
        'topic_tag': 'rotation_rules',
    },

    # --- Data Modeling — Extended (4 questions, F=1/U=2/A=4/R=5) ---
    {
        'track': 'grade_8', 'sat_domain': 'data_modeling', 'fuar_dimension': 'F', 'difficulty': 1,
        'question_text': 'In a scatter plot, the points are clustered closely around a line going up from left to right. This pattern shows:',
        'option_a': 'No association', 'option_b': 'A negative linear association', 'option_c': 'A strong positive linear association', 'option_d': 'A non-linear association',
        'correct_answer': 'C', 'explanation': 'Points clustered tightly around an upward-sloping line indicate a strong positive linear association.',
        'topic_tag': 'scatter_plots',
    },
    {
        'track': 'grade_8', 'sat_domain': 'data_modeling', 'fuar_dimension': 'U', 'difficulty': 2,
        'question_text': 'A line of best fit passes through (0, 5) and (10, 25). What is the equation of this line?',
        'option_a': 'y = 5x + 5', 'option_b': 'y = 2x + 5', 'option_c': 'y = 0.5x + 5', 'option_d': 'y = 2x + 10',
        'correct_answer': 'B', 'explanation': 'Slope = (25−5)/(10−0) = 20/10 = 2. Y-intercept = 5 (from point (0,5)). Equation: y = 2x + 5.',
        'topic_tag': 'line_of_best_fit',
    },
    {
        'track': 'grade_8', 'sat_domain': 'data_modeling', 'fuar_dimension': 'A', 'difficulty': 4,
        'question_text': 'A data set has a line of best fit y = −1.5x + 60, where x = age of a car (years) and y = resale value ($thousands). What does the model predict for a 10-year-old car, and is this reasonable?',
        'option_a': '$45,000; reasonable if new car was $60,000', 'option_b': '$75,000; reasonable for a luxury car', 'option_c': '$45,000; unreasonable because cars stop losing value after year 5', 'option_d': '$15,000; the slope represents the starting value',
        'correct_answer': 'A', 'explanation': 'y = −1.5(10) + 60 = −15 + 60 = 45 ($45,000). This is reasonable if the car started at $60,000 (the y-intercept) and depreciates $1,500/year.',
        'topic_tag': 'model_interpretation',
    },
    {
        'track': 'grade_8', 'sat_domain': 'data_modeling', 'fuar_dimension': 'R', 'difficulty': 5,
        'question_text': 'Two students each analyze the same scatter plot. Student A says the line of best fit should pass through the most points. Student B says it should minimize the total distance from all points to the line. Who is correct?',
        'option_a': 'Student A — passing through more points gives a better fit', 'option_b': 'Student B — the best fit line minimizes residuals across all data', 'option_c': 'Both are correct, they describe the same thing', 'option_d': 'Neither — the best fit line must pass through the origin',
        'correct_answer': 'B', 'explanation': 'A line of best fit (least squares regression) minimizes the sum of squared vertical distances (residuals) from all data points — not just the count of points it touches.',
        'topic_tag': 'line_of_best_fit_reasoning',
    },

    # --- Irrational Numbers (4 questions) ---
    {
        'track': 'grade_8', 'sat_domain': 'irrational_numbers', 'fuar_dimension': 'F', 'difficulty': 2,
        'question_text': 'Between which two consecutive integers does √50 fall?',
        'option_a': '6 and 7', 'option_b': '7 and 8', 'option_c': '24 and 26', 'option_d': '49 and 51',
        'correct_answer': 'B', 'explanation': '7² = 49 and 8² = 64. Since 49 < 50 < 64, √50 is between 7 and 8.',
        'topic_tag': 'square_roots',
    },
    {
        'track': 'grade_8', 'sat_domain': 'irrational_numbers', 'fuar_dimension': 'U', 'difficulty': 3,
        'question_text': 'Which number is irrational?',
        'option_a': '0.333...', 'option_b': '√9', 'option_c': '√2', 'option_d': '22/7',
        'correct_answer': 'C', 'explanation': '0.333... = 1/3 (rational). √9 = 3 (rational). 22/7 is rational. √2 cannot be expressed as a fraction — it is irrational.',
        'topic_tag': 'number_classification',
    },
    {
        'track': 'grade_8', 'sat_domain': 'irrational_numbers', 'fuar_dimension': 'A', 'difficulty': 3,
        'question_text': 'A square has an area of 72 cm². What is the exact length of one side?',
        'option_a': '6√2 cm', 'option_b': '36 cm', 'option_c': '8.5 cm', 'option_d': '9 cm',
        'correct_answer': 'A', 'explanation': 'Side = √72 = √(36 × 2) = 6√2 cm ≈ 8.49 cm.',
        'topic_tag': 'radical_applications',
    },
    {
        'track': 'grade_8', 'sat_domain': 'irrational_numbers', 'fuar_dimension': 'R', 'difficulty': 4,
        'question_text': 'If you add two irrational numbers, is the result always irrational?',
        'option_a': 'Yes, always', 'option_b': 'No — for example, √2 + (-√2) = 0, which is rational',
        'option_c': 'Only if both are positive', 'option_d': 'Only if they have different values',
        'correct_answer': 'B', 'explanation': 'The sum of two irrational numbers can be rational. √2 + (-√2) = 0. So the answer is not always irrational.',
        'topic_tag': 'number_system_reasoning',
    },

    # --- Irrational Numbers — Extended (4 questions, F=1/U=2/A=4/R=5) ---
    {
        'track': 'grade_8', 'sat_domain': 'irrational_numbers', 'fuar_dimension': 'F', 'difficulty': 1,
        'question_text': 'Which of the following is a rational number?',
        'option_a': '√5', 'option_b': 'π', 'option_c': '0.75', 'option_d': '√3',
        'correct_answer': 'C', 'explanation': '0.75 = 3/4, which can be written as a fraction — so it is rational. The others (√5, π, √3) cannot be expressed as exact fractions.',
        'topic_tag': 'number_classification',
    },
    {
        'track': 'grade_8', 'sat_domain': 'irrational_numbers', 'fuar_dimension': 'U', 'difficulty': 2,
        'question_text': 'What makes a decimal number irrational?',
        'option_a': 'It has a decimal point', 'option_b': 'It has more than 2 decimal places', 'option_c': 'Its decimal expansion is non-terminating and non-repeating', 'option_d': 'It is greater than 1',
        'correct_answer': 'C', 'explanation': 'Irrational numbers have decimal expansions that go on forever without any repeating pattern (e.g., π = 3.14159…). Rational numbers either terminate or repeat.',
        'topic_tag': 'number_classification',
    },
    {
        'track': 'grade_8', 'sat_domain': 'irrational_numbers', 'fuar_dimension': 'A', 'difficulty': 4,
        'question_text': 'The diagonal of a square with side length 5 cm equals √50 cm. Expressed in simplest radical form and then estimated to one decimal place, the diagonal is closest to:',
        'option_a': '5.0 cm', 'option_b': '6.5 cm', 'option_c': '7.1 cm', 'option_d': '10.0 cm',
        'correct_answer': 'C', 'explanation': '√50 = 5√2. Since √2 ≈ 1.414, the diagonal ≈ 5 × 1.414 = 7.07 cm, which rounds to 7.1 cm.',
        'topic_tag': 'radical_applications',
    },
    {
        'track': 'grade_8', 'sat_domain': 'irrational_numbers', 'fuar_dimension': 'R', 'difficulty': 5,
        'question_text': 'A student claims: "The product of any two irrational numbers is always irrational." Which counterexample proves this wrong?',
        'option_a': '√2 × √3 = √6 (irrational)', 'option_b': '√2 × √2 = 2 (rational)', 'option_c': 'π × 2 = 2π (irrational)', 'option_d': '√5 × √7 = √35 (irrational)',
        'correct_answer': 'B', 'explanation': '√2 × √2 = 2, which is a rational number. Since two irrational numbers can multiply to give a rational, the student\'s claim is false.',
        'topic_tag': 'number_system_reasoning',
    },
]


def seed():
    conn = sqlite3.connect(DB_PATH)
    existing = conn.execute("SELECT COUNT(*) FROM questions WHERE track = 'grade_8'").fetchone()[0]
    if existing > 0:
        print(f"[Grade 8] Already has {existing} questions. Skipping seed.")
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
    count = conn.execute("SELECT COUNT(*) FROM questions WHERE track = 'grade_8'").fetchone()[0]
    print(f"[Grade 8] Seeded {count} questions.")
    conn.close()
    return count


if __name__ == '__main__':
    seed()
