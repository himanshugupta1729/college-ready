"""Supplemental Algebra 1 questions to reach 3x test variety."""
import sqlite3, os
DB_PATH = os.environ.get('DATABASE_PATH', 'college_ready.db')

QUESTIONS = [
    # (track, sat_domain, fuar_dimension, difficulty, question_text, question_type,
    #  option_a, option_b, option_c, option_d, correct_answer, explanation, topic_tag)

    # =========================================================================
    # LINEAR EQUATIONS — 18 questions
    # =========================================================================

    # diff=1 F
    ("algebra_1", "linear_equations", "F", 1,
     "Solve for x: x + 13 = 20.",
     "multiple_choice",
     "5", "6", "7", "8",
     "C",
     "Subtract 13 from both sides: x = 20 - 13 = 7.",
     "one_variable"),

    # diff=1 F
    ("algebra_1", "linear_equations", "F", 1,
     "Solve for x: 3x = 24.",
     "multiple_choice",
     "6", "7", "8", "9",
     "C",
     "Divide both sides by 3: x = 24 / 3 = 8.",
     "one_variable"),

    # diff=2 F
    ("algebra_1", "linear_equations", "F", 2,
     "Solve for x: 4x + 7 = 31.",
     "multiple_choice",
     "4", "5", "6", "7",
     "C",
     "Subtract 7: 4x = 24. Divide by 4: x = 6.",
     "one_variable"),

    # diff=2 F
    ("algebra_1", "linear_equations", "F", 2,
     "Solve for x: 2(x - 3) = 10.",
     "multiple_choice",
     "5", "7", "8", "11",
     "C",
     "Distribute: 2x - 6 = 10. Add 6: 2x = 16. Divide by 2: x = 8.",
     "multi_step"),

    # diff=2 U
    ("algebra_1", "linear_equations", "U", 2,
     "Which value of x satisfies 5x - 2 = 3x + 8?",
     "multiple_choice",
     "3", "4", "5", "6",
     "C",
     "Subtract 3x from both sides: 2x - 2 = 8. Add 2: 2x = 10. Divide by 2: x = 5.",
     "two_variable_sides"),

    # diff=2 U
    ("algebra_1", "linear_equations", "U", 2,
     "If 7 - 2x = x + 1, what is x?",
     "multiple_choice",
     "1", "2", "3", "4",
     "B",
     "Subtract x: 7 - 3x = 1. Subtract 7: -3x = -6. Divide: x = 2.",
     "two_variable_sides"),

    # diff=3 U
    ("algebra_1", "linear_equations", "U", 3,
     "Solve for x: (x / 4) + 3 = 7.",
     "multiple_choice",
     "8", "10", "12", "16",
     "D",
     "Subtract 3: x/4 = 4. Multiply by 4: x = 16.",
     "fraction_equations"),

    # diff=3 U
    ("algebra_1", "linear_equations", "U", 3,
     "Solve for x: 3(2x - 4) = 2(x + 6).",
     "multiple_choice",
     "4", "5", "6", "7",
     "C",
     "Distribute: 6x - 12 = 2x + 12. Subtract 2x: 4x = 24. Divide: x = 6.",
     "multi_step"),

    # diff=3 A
    ("algebra_1", "linear_equations", "A", 3,
     "A plumber charges $50 for a service call plus $40 per hour. The total bill was $210. How many hours did the plumber work?",
     "multiple_choice",
     "3", "4", "5", "6",
     "B",
     "50 + 40h = 210. Subtract 50: 40h = 160. Divide: h = 4.",
     "linear_modeling"),

    # diff=3 A
    ("algebra_1", "linear_equations", "A", 3,
     "Mia has $180 and spends $15 per week. After how many weeks will she have exactly $90 left?",
     "multiple_choice",
     "4", "5", "6", "7",
     "C",
     "180 - 15w = 90. Subtract 180: -15w = -90. Divide: w = 6.",
     "linear_modeling"),

    # diff=3 A
    ("algebra_1", "linear_equations", "A", 3,
     "Two friends split a $76 dinner bill equally and each leaves a $4 tip. How much does each person pay in total?",
     "multiple_choice",
     "$40", "$42", "$44", "$46",
     "B",
     "Each pays 76/2 + 4 = 38 + 4 = $42.",
     "multi_step"),

    # diff=3 R
    ("algebra_1", "linear_equations", "R", 3,
     "If 3(x + k) = 18 and x = 2, what is k?",
     "multiple_choice",
     "2", "3", "4", "6",
     "C",
     "3(2 + k) = 18. Divide by 3: 2 + k = 6. Subtract 2: k = 4.",
     "literal_equations"),

    # diff=4 R
    ("algebra_1", "linear_equations", "R", 4,
     "Solve for y in terms of x: 4x + 2y = 16.",
     "multiple_choice",
     "y = 8 - 2x", "y = 4 - 2x", "y = 8 + 2x", "y = 16 - 4x",
     "A",
     "Subtract 4x: 2y = 16 - 4x. Divide by 2: y = 8 - 2x.",
     "literal_equations"),

    # diff=4 R
    ("algebra_1", "linear_equations", "R", 4,
     "For what value of b does 2x + b = 5x - 7 have the solution x = 4?",
     "multiple_choice",
     "3", "5", "7", "9",
     "B",
     "Substitute x = 4: 8 + b = 20 - 7 = 13. So b = 5.",
     "literal_equations"),

    # diff=4 A
    ("algebra_1", "linear_equations", "A", 4,
     "Carlos earns $12/hr and $18/hr for overtime (hours beyond 40). He worked 46 hours. What were his total earnings?",
     "multiple_choice",
     "$540", "$580", "$588", "$600",
     "C",
     "Regular: 40 x 12 = $480. Overtime: 6 x 18 = $108. Total = 480 + 108 = $588.",
     "linear_modeling"),

    # diff=4 U
    ("algebra_1", "linear_equations", "U", 4,
     "The equation ax + 4 = 2x + b has infinitely many solutions. Which must be true?",
     "multiple_choice",
     "a = 2 and b = 4", "a = 4 and b = 2", "a = 2 and b = 2", "a = 4 and b = 4",
     "A",
     "For infinitely many solutions, both sides must be identical: coefficients match (a = 2) and constants match (4 = b).",
     "properties_of_solutions"),

    # diff=5 R
    ("algebra_1", "linear_equations", "R", 5,
     "Solve for x: (2/3)x - (1/4) = 5/12.",
     "multiple_choice",
     "1", "1/2", "3/2", "2",
     "A",
     "Add 1/4 to both sides: (2/3)x = 5/12 + 3/12 = 8/12 = 2/3. Multiply by 3/2: x = 1.",
     "fraction_equations"),

    # diff=5 R
    ("algebra_1", "linear_equations", "R", 5,
     "The sum of three consecutive even integers is 78. What is the largest?",
     "multiple_choice",
     "24", "26", "28", "30",
     "C",
     "Let n, n+2, n+4. Sum: 3n + 6 = 78. 3n = 72. n = 24. Largest = 24 + 4 = 28.",
     "multi_step"),

    # =========================================================================
    # LINEAR FUNCTIONS — 15 questions
    # =========================================================================

    # diff=1 F
    ("algebra_1", "linear_functions", "F", 1,
     "What is the slope of y = 3x - 7?",
     "multiple_choice",
     "-7", "3", "7", "-3",
     "B",
     "In y = mx + b, the slope m = 3.",
     "slope_intercept"),

    # diff=2 F
    ("algebra_1", "linear_functions", "F", 2,
     "What is the y-intercept of y = -2x + 9?",
     "multiple_choice",
     "-2", "2", "9", "-9",
     "C",
     "In y = mx + b, the y-intercept b = 9.",
     "slope_intercept"),

    # diff=2 F
    ("algebra_1", "linear_functions", "F", 2,
     "Find the slope of the line through (2, 5) and (6, 13).",
     "multiple_choice",
     "1", "2", "3", "4",
     "B",
     "Slope = (13 - 5) / (6 - 2) = 8 / 4 = 2.",
     "slope_from_points"),

    # diff=2 U
    ("algebra_1", "linear_functions", "U", 2,
     "Which equation has slope -3 and y-intercept 4?",
     "multiple_choice",
     "y = 3x + 4", "y = -3x - 4", "y = -3x + 4", "y = 4x - 3",
     "C",
     "Slope-intercept form: y = mx + b. m = -3, b = 4 gives y = -3x + 4.",
     "slope_intercept"),

    # diff=2 U
    ("algebra_1", "linear_functions", "U", 2,
     "A line passes through (0, 6) and (3, 0). What is its equation?",
     "multiple_choice",
     "y = 2x + 6", "y = -2x + 6", "y = 2x - 6", "y = -2x - 6",
     "B",
     "Slope = (0 - 6) / (3 - 0) = -2. y-intercept = 6. Equation: y = -2x + 6.",
     "slope_intercept"),

    # diff=3 U
    ("algebra_1", "linear_functions", "U", 3,
     "What is the x-intercept of 3x + 2y = 12?",
     "multiple_choice",
     "2", "3", "4", "6",
     "C",
     "Set y = 0: 3x = 12. x = 4.",
     "intercepts"),

    # diff=3 F
    ("algebra_1", "linear_functions", "F", 3,
     "Find the slope of the line 5x - 2y = 10.",
     "multiple_choice",
     "5/2", "-5/2", "2/5", "-2/5",
     "A",
     "Solve for y: 2y = 5x - 10, so y = (5/2)x - 5. Slope = 5/2.",
     "standard_form"),

    # diff=3 A
    ("algebra_1", "linear_functions", "A", 3,
     "A taxi charges $2.50 per mile plus a $3 base fare. Which equation gives total cost C for m miles?",
     "multiple_choice",
     "C = 3m + 2.50", "C = 2.50m + 3", "C = 2.50 + 3m", "C = 5.50m",
     "B",
     "Total cost = rate x miles + base fare = 2.50m + 3.",
     "linear_modeling"),

    # diff=3 A
    ("algebra_1", "linear_functions", "A", 3,
     "A table shows: (0, 4), (1, 7), (2, 10). What is the equation of this linear function?",
     "multiple_choice",
     "y = 2x + 4", "y = 3x + 4", "y = 4x + 3", "y = 3x + 3",
     "B",
     "Rate of change = (7 - 4) / 1 = 3. y-intercept = 4 (when x = 0). Equation: y = 3x + 4.",
     "slope_intercept"),

    # diff=3 R
    ("algebra_1", "linear_functions", "R", 3,
     "Line 1: y = 4x - 1. Line 2 is parallel to Line 1 and passes through (0, 7). What is Line 2's equation?",
     "multiple_choice",
     "y = -4x + 7", "y = (1/4)x + 7", "y = 4x + 7", "y = 4x - 7",
     "C",
     "Parallel lines have equal slopes. m = 4, y-intercept = 7. Equation: y = 4x + 7.",
     "slope_intercept"),

    # diff=4 A
    ("algebra_1", "linear_functions", "A", 4,
     "A 20 cm candle burns at 2 cm per hour. After how many hours will it be 8 cm tall?",
     "multiple_choice",
     "4", "5", "6", "7",
     "C",
     "20 - 2h = 8. Subtract 20: -2h = -12. Divide: h = 6.",
     "linear_modeling"),

    # diff=4 U
    ("algebra_1", "linear_functions", "U", 4,
     "Line p has slope 1/3. Line q is perpendicular to p. What is the slope of q?",
     "multiple_choice",
     "3", "-3", "1/3", "-1/3",
     "B",
     "Perpendicular slopes are negative reciprocals: -(1 / (1/3)) = -3.",
     "slope_relationships"),

    # diff=4 R
    ("algebra_1", "linear_functions", "R", 4,
     "A linear function f has f(2) = 11 and f(5) = 20. What is f(0)?",
     "multiple_choice",
     "2", "3", "5", "7",
     "C",
     "Slope = (20 - 11) / (5 - 2) = 3. Using (2, 11): 11 = 3(2) + b, so b = 5. f(0) = 5.",
     "slope_intercept"),

    # diff=4 R
    ("algebra_1", "linear_functions", "R", 4,
     "A line passes through (-3, 1) and (1, 9). What is its equation?",
     "multiple_choice",
     "y = 2x + 7", "y = 2x + 3", "y = 3x + 7", "y = 2x - 7",
     "A",
     "Slope = (9 - 1) / (1 - (-3)) = 8/4 = 2. Using (1, 9): 9 = 2(1) + b, b = 7. y = 2x + 7.",
     "slope_intercept"),

    # diff=5 R
    ("algebra_1", "linear_functions", "R", 5,
     "Line L: 3x - 4y = 12. Line M is parallel to L and passes through (4, 1). What is M's y-intercept?",
     "multiple_choice",
     "-2", "-1", "1", "2",
     "A",
     "Slope of L: y = (3/4)x - 3, so slope = 3/4. Line M: 1 = (3/4)(4) + b = 3 + b. b = -2.",
     "slope_relationships"),

    # =========================================================================
    # SYSTEMS OF EQUATIONS — 15 questions
    # =========================================================================

    # diff=1 F
    ("algebra_1", "systems", "F", 1,
     "Solve: x + y = 10 and x - y = 4.",
     "multiple_choice",
     "x = 5, y = 5", "x = 6, y = 4", "x = 7, y = 3", "x = 8, y = 2",
     "C",
     "Add equations: 2x = 14, x = 7. Substitute: 7 + y = 10, y = 3.",
     "elimination"),

    # diff=2 F
    ("algebra_1", "systems", "F", 2,
     "Solve by substitution: y = 2x and x + y = 12.",
     "multiple_choice",
     "x = 3, y = 6", "x = 4, y = 8", "x = 5, y = 10", "x = 6, y = 12",
     "B",
     "Substitute y = 2x: x + 2x = 12, 3x = 12, x = 4. y = 2(4) = 8.",
     "substitution"),

    # diff=2 F
    ("algebra_1", "systems", "F", 2,
     "Solve: 2x + y = 8 and y = x - 1.",
     "multiple_choice",
     "x = 2, y = 1", "x = 3, y = 2", "x = 4, y = 3", "x = 5, y = 4",
     "B",
     "Substitute y = x - 1: 2x + (x - 1) = 8, 3x = 9, x = 3. y = 3 - 1 = 2.",
     "substitution"),

    # diff=2 U
    ("algebra_1", "systems", "U", 2,
     "A system of two linear equations has no solution. What does this tell you about the graphs?",
     "multiple_choice",
     "The lines are the same", "The lines intersect at one point", "The lines are parallel", "The lines are perpendicular",
     "C",
     "No solution means the lines never meet. Parallel lines never intersect.",
     "graphing_systems"),

    # diff=3 F
    ("algebra_1", "systems", "F", 3,
     "Solve by elimination: 2x + y = 7 and x - y = 2.",
     "multiple_choice",
     "x = 2, y = 3", "x = 3, y = 1", "x = 4, y = -1", "x = 1, y = 5",
     "B",
     "Add equations: 3x = 9, x = 3. Substitute: 3 - y = 2, y = 1.",
     "elimination"),

    # diff=3 U
    ("algebra_1", "systems", "U", 3,
     "Which system has infinitely many solutions?",
     "multiple_choice",
     "y = 2x + 3 and y = 2x - 3",
     "y = 3x + 1 and 6x - 2y = -2",
     "y = x + 1 and y = -x + 1",
     "y = 4x and y = x + 4",
     "B",
     "Rewrite 6x - 2y = -2 as y = 3x + 1. Both equations are identical, so infinitely many solutions.",
     "properties_of_solutions"),

    # diff=3 A
    ("algebra_1", "systems", "A", 3,
     "Tickets cost $5 for students and $9 for adults. 200 tickets were sold for $1,180 total. How many adult tickets were sold?",
     "multiple_choice",
     "35", "40", "45", "55",
     "C",
     "Let s = students, a = adults. s + a = 200 and 5s + 9a = 1180. From first eq: s = 200 - a. Substitute: 5(200-a) + 9a = 1180. 1000 + 4a = 1180. 4a = 180. a = 45.",
     "systems_word_problems"),

    # diff=3 A
    ("algebra_1", "systems", "A", 3,
     "If 2x + 5y = 3.60 and 2x + y = 1.60, what is y?",
     "multiple_choice",
     "$0.40", "$0.50", "$0.55", "$0.60",
     "B",
     "Subtract second from first: 4y = 2.00. y = 0.50.",
     "elimination"),

    # diff=3 R
    ("algebra_1", "systems", "R", 3,
     "A jar has 40 coins — all nickels and dimes — worth $3.05. How many dimes are in the jar?",
     "multiple_choice",
     "17", "19", "21", "23",
     "C",
     "n + d = 40 and 5n + 10d = 305. n = 40 - d. 5(40-d) + 10d = 305. 200 + 5d = 305. d = 21.",
     "systems_word_problems"),

    # diff=3 U
    ("algebra_1", "systems", "U", 3,
     "How many solutions does 4x - 2y = 8 and -2x + y = -4 have?",
     "multiple_choice",
     "Zero", "Exactly one", "Exactly two", "Infinitely many",
     "D",
     "Multiply second equation by 2: -4x + 2y = -8. Add to first: 0 = 0. True for all x — infinitely many solutions.",
     "properties_of_solutions"),

    # diff=4 A
    ("algebra_1", "systems", "A", 4,
     "A boat travels 36 miles downstream in 2 hours and 36 miles upstream in 3 hours. What is the speed of the current?",
     "multiple_choice",
     "2 mph", "3 mph", "4 mph", "5 mph",
     "B",
     "Downstream: b + c = 18. Upstream: b - c = 12. Add: 2b = 30, b = 15. Subtract: 2c = 6, c = 3.",
     "systems_word_problems"),

    # diff=4 R
    ("algebra_1", "systems", "R", 4,
     "The system kx + 2y = 6 and 3x + y = 4 has no solution. What is k?",
     "multiple_choice",
     "3/2", "3", "6", "9/2",
     "C",
     "No solution when lines are parallel: slopes equal but intercepts differ. From eq2: y = -3x + 4 (slope -3). From eq1: y = -(k/2)x + 3. Set -k/2 = -3: k = 6. Check intercepts: 3 ≠ 4. Confirmed.",
     "properties_of_solutions"),

    # diff=4 F
    ("algebra_1", "systems", "F", 4,
     "Solve by elimination: 4x + y = 14 and 2x - y = 4.",
     "multiple_choice",
     "x = 2, y = 6", "x = 3, y = 2", "x = 4, y = -2", "x = 1, y = 10",
     "B",
     "Add equations: 6x = 18, x = 3. Substitute into 4(3) + y = 14: 12 + y = 14, y = 2.",
     "elimination"),

    # diff=4 R
    ("algebra_1", "systems", "R", 4,
     "Solve: 2x + 3y = 13 and x + y = 5.",
     "multiple_choice",
     "x = 1, y = 4", "x = 2, y = 3", "x = 3, y = 2", "x = 4, y = 1",
     "B",
     "From x + y = 5: x = 5 - y. Substitute: 2(5-y) + 3y = 13. 10 + y = 13. y = 3, x = 2.",
     "substitution"),

    # diff=5 R
    ("algebra_1", "systems", "R", 5,
     "A chemist mixes 30% and 70% acid solutions to make 400 mL of a 50% solution. How many mL of the 30% solution are needed?",
     "multiple_choice",
     "150 mL", "175 mL", "200 mL", "225 mL",
     "C",
     "Let x = mL of 30%, y = mL of 70%. x + y = 400 and 0.30x + 0.70y = 200. y = 400 - x. 0.30x + 0.70(400-x) = 200. 0.30x + 280 - 0.70x = 200. -0.40x = -80. x = 200.",
     "systems_word_problems"),

    # =========================================================================
    # QUADRATICS — 18 questions
    # =========================================================================

    # diff=1 F
    ("algebra_1", "quadratics", "F", 1,
     "What is the degree of 4x^2 + 3x - 7?",
     "multiple_choice",
     "1", "2", "3", "4",
     "B",
     "The highest exponent is 2, so the polynomial has degree 2.",
     "quadratic_basics"),

    # diff=2 F
    ("algebra_1", "quadratics", "F", 2,
     "Factor: x^2 - 9.",
     "multiple_choice",
     "(x - 3)^2", "(x + 3)(x - 3)", "(x + 9)(x - 1)", "(x - 3)(x + 1)",
     "B",
     "Difference of squares: x^2 - 9 = (x + 3)(x - 3).",
     "factoring"),

    # diff=2 F
    ("algebra_1", "quadratics", "F", 2,
     "Solve: x^2 = 25.",
     "multiple_choice",
     "x = 5 only", "x = -5 only", "x = 5 or x = -5", "x = 625",
     "C",
     "Take the square root: x = +5 or x = -5.",
     "solving_quadratics"),

    # diff=2 U
    ("algebra_1", "quadratics", "U", 2,
     "Factor: x^2 + 7x + 12.",
     "multiple_choice",
     "(x + 3)(x + 4)", "(x + 2)(x + 6)", "(x + 1)(x + 12)", "(x + 3)(x + 5)",
     "A",
     "Find two numbers that multiply to 12 and add to 7: 3 and 4. Factor: (x + 3)(x + 4).",
     "factoring"),

    # diff=3 F
    ("algebra_1", "quadratics", "F", 3,
     "Factor: x^2 - 5x - 14.",
     "multiple_choice",
     "(x - 7)(x + 2)", "(x - 2)(x + 7)", "(x - 14)(x + 1)", "(x + 5)(x - 2)",
     "A",
     "Find two numbers that multiply to -14 and add to -5: -7 and 2. Factor: (x - 7)(x + 2).",
     "factoring"),

    # diff=3 F
    ("algebra_1", "quadratics", "F", 3,
     "Use the quadratic formula to solve 2x^2 - 7x + 3 = 0. What are the solutions?",
     "multiple_choice",
     "x = 3 and x = 1/2", "x = 3 and x = -1/2", "x = -3 and x = 1/2", "x = 6 and x = 1",
     "A",
     "a=2, b=-7, c=3. Discriminant: (-7)^2 - 4(2)(3) = 49 - 24 = 25. x = (7 +/- 5) / 4. x = 12/4 = 3 or x = 2/4 = 1/2.",
     "quadratic_formula"),

    # diff=3 U
    ("algebra_1", "quadratics", "U", 3,
     "What are the zeros of f(x) = x^2 - 2x - 15?",
     "multiple_choice",
     "x = 3 and x = -5", "x = -3 and x = 5", "x = 5 and x = 3", "x = 15 and x = -1",
     "B",
     "Factor: (x - 5)(x + 3) = 0. Zeros: x = 5 and x = -3.",
     "zeros_of_quadratic"),

    # diff=3 U
    ("algebra_1", "quadratics", "U", 3,
     "The parabola y = x^2 + 4x + 4 touches the x-axis at exactly one point. What is that point?",
     "multiple_choice",
     "(2, 0)", "(-2, 0)", "(4, 0)", "(-4, 0)",
     "B",
     "y = (x + 2)^2. Set y = 0: x = -2. The vertex (and only x-intercept) is (-2, 0).",
     "zeros_of_quadratic"),

    # diff=3 A
    ("algebra_1", "quadratics", "A", 3,
     "A rectangle has length (x + 5) and width (x + 2). What is its area as a polynomial?",
     "multiple_choice",
     "x^2 + 7x + 10", "x^2 + 7x + 7", "x^2 + 10x + 7", "2x + 7",
     "A",
     "Area = (x+5)(x+2) = x^2 + 2x + 5x + 10 = x^2 + 7x + 10.",
     "quadratic_basics"),

    # diff=3 A
    ("algebra_1", "quadratics", "A", 3,
     "A ball's height in feet is h = -16t^2 + 64t, where t is seconds. When does it return to the ground?",
     "multiple_choice",
     "t = 2 sec", "t = 4 sec", "t = 6 sec", "t = 8 sec",
     "B",
     "Set h = 0: -16t^2 + 64t = 0. Factor: -16t(t - 4) = 0. t = 0 or t = 4. It returns at t = 4 sec.",
     "quadratic_applications"),

    # diff=3 R
    ("algebra_1", "quadratics", "R", 3,
     "What is the vertex of y = x^2 - 6x + 8?",
     "multiple_choice",
     "(3, -1)", "(3, 1)", "(-3, 1)", "(6, 8)",
     "A",
     "x = -b/(2a) = 6/2 = 3. y = 9 - 18 + 8 = -1. Vertex = (3, -1).",
     "vertex_form"),

    # diff=4 F
    ("algebra_1", "quadratics", "F", 4,
     "Factor completely: 2x^2 + 10x + 12.",
     "multiple_choice",
     "2(x + 2)(x + 3)", "(2x + 4)(x + 3)", "2(x + 1)(x + 6)", "(x + 2)(2x + 6)",
     "A",
     "Factor out 2: 2(x^2 + 5x + 6) = 2(x + 2)(x + 3).",
     "factoring"),

    # diff=4 U
    ("algebra_1", "quadratics", "U", 4,
     "Which equation has no real solutions?",
     "multiple_choice",
     "x^2 - 5x + 6 = 0", "x^2 + 4 = 0", "x^2 - 4x = 0", "x^2 - 1 = 0",
     "B",
     "Discriminant of x^2 + 4 = 0: b^2 - 4ac = 0 - 16 = -16 < 0. No real solutions.",
     "discriminant"),

    # diff=4 A
    ("algebra_1", "quadratics", "A", 4,
     "The product of two consecutive positive integers is 90. What are those integers?",
     "multiple_choice",
     "8 and 9", "9 and 10", "10 and 11", "7 and 8",
     "B",
     "n(n+1) = 90. n^2 + n - 90 = 0. Factor: (n + 10)(n - 9) = 0. n = 9. Integers: 9 and 10.",
     "quadratic_applications"),

    # diff=4 R
    ("algebra_1", "quadratics", "R", 4,
     "Solve by completing the square: x^2 + 6x = 7.",
     "multiple_choice",
     "x = 1 or x = -7", "x = -1 or x = 7", "x = 2 or x = -8", "x = 7 or x = 1",
     "A",
     "Add (6/2)^2 = 9: x^2 + 6x + 9 = 16. (x + 3)^2 = 16. x + 3 = +/-4. x = 1 or x = -7.",
     "completing_the_square"),

    # diff=5 R
    ("algebra_1", "quadratics", "R", 5,
     "For what value of k does x^2 - 4x + k = 0 have exactly one real solution?",
     "multiple_choice",
     "k = 2", "k = 4", "k = 6", "k = 8",
     "B",
     "One solution when discriminant = 0: 16 - 4k = 0. k = 4.",
     "discriminant"),

    # diff=5 A
    ("algebra_1", "quadratics", "A", 5,
     "A projectile's height is h(t) = -5t^2 + 20t + 25. What is the maximum height?",
     "multiple_choice",
     "40 m", "45 m", "50 m", "55 m",
     "B",
     "Vertex at t = -20 / (2 x (-5)) = 2. h(2) = -5(4) + 20(2) + 25 = -20 + 40 + 25 = 45.",
     "quadratic_applications"),

    # diff=5 F
    ("algebra_1", "quadratics", "F", 5,
     "Solve using the quadratic formula: 3x^2 + x - 2 = 0.",
     "multiple_choice",
     "x = 2/3 and x = -1", "x = 1 and x = -2/3", "x = -2/3 and x = -1", "x = 2/3 and x = 1",
     "A",
     "a=3, b=1, c=-2. Discriminant: 1 + 24 = 25. x = (-1 +/- 5) / 6. x = 4/6 = 2/3 or x = -6/6 = -1.",
     "quadratic_formula"),

    # =========================================================================
    # EXPONENTIALS — 12 questions
    # =========================================================================

    # diff=1 F
    ("algebra_1", "exponentials", "F", 1,
     "Evaluate: 2^5.",
     "multiple_choice",
     "10", "16", "32", "64",
     "C",
     "2^5 = 2 x 2 x 2 x 2 x 2 = 32.",
     "exponent_basics"),

    # diff=2 F
    ("algebra_1", "exponentials", "F", 2,
     "Simplify: x^3 * x^4.",
     "multiple_choice",
     "x^7", "x^12", "2x^7", "x^(3/4)",
     "A",
     "Multiply same base: add exponents. x^3 * x^4 = x^(3+4) = x^7.",
     "exponent_rules"),

    # diff=2 F
    ("algebra_1", "exponentials", "F", 2,
     "Simplify: (2x^2)^3.",
     "multiple_choice",
     "2x^6", "6x^5", "8x^6", "8x^5",
     "C",
     "(2x^2)^3 = 2^3 * (x^2)^3 = 8x^6.",
     "exponent_rules"),

    # diff=2 U
    ("algebra_1", "exponentials", "U", 2,
     "Bacteria double every hour. Starting with 50, how many are there after 4 hours?",
     "multiple_choice",
     "200", "400", "800", "1600",
     "C",
     "P = 50 * 2^4 = 50 * 16 = 800.",
     "exponential_growth"),

    # diff=3 U
    ("algebra_1", "exponentials", "U", 3,
     "Which equation represents exponential decay?",
     "multiple_choice",
     "y = 2(1.5)^x", "y = 5(0.8)^x", "y = 3x + 7", "y = x^2",
     "B",
     "Exponential decay has base between 0 and 1. The base 0.8 < 1, so y = 5(0.8)^x is decay.",
     "exponential_decay"),

    # diff=3 F
    ("algebra_1", "exponentials", "F", 3,
     "Simplify: x^8 / x^3.",
     "multiple_choice",
     "x^5", "x^11", "x^24", "x^(8/3)",
     "A",
     "Divide same base: subtract exponents. x^8 / x^3 = x^(8-3) = x^5.",
     "exponent_rules"),

    # diff=3 A
    ("algebra_1", "exponentials", "A", 3,
     "A car is worth $24,000 and depreciates 15% each year. What is its value after 2 years?",
     "multiple_choice",
     "$17,340", "$18,000", "$19,200", "$20,400",
     "A",
     "After 2 years: 24000 * (0.85)^2 = 24000 * 0.7225 = $17,340.",
     "exponential_decay"),

    # diff=3 A
    ("algebra_1", "exponentials", "A", 3,
     "An investment of $1,000 grows at 8% per year compounded annually. Which expression gives its value after n years?",
     "multiple_choice",
     "1000(0.08)^n", "1000(1.08)^n", "1000 + 80n", "1000(8)^n",
     "B",
     "Compound growth: A = P(1 + r)^n = 1000(1.08)^n.",
     "exponential_growth"),

    # diff=3 R
    ("algebra_1", "exponentials", "R", 3,
     "Solve for x: 2^x = 32.",
     "multiple_choice",
     "4", "5", "6", "16",
     "B",
     "32 = 2^5. So 2^x = 2^5, therefore x = 5.",
     "exponential_equations"),

    # diff=4 U
    ("algebra_1", "exponentials", "U", 4,
     "What is the value of 4^(-2)?",
     "multiple_choice",
     "-16", "-8", "1/8", "1/16",
     "D",
     "Negative exponent: 4^(-2) = 1 / 4^2 = 1/16.",
     "exponent_rules"),

    # diff=4 R
    ("algebra_1", "exponentials", "R", 4,
     "Solve for x: 3^(2x) = 81.",
     "multiple_choice",
     "x = 1", "x = 2", "x = 4", "x = 8",
     "B",
     "81 = 3^4. So 3^(2x) = 3^4, which means 2x = 4, x = 2.",
     "exponential_equations"),

    # diff=5 R
    ("algebra_1", "exponentials", "R", 5,
     "A population triples every 5 years. Starting with 200, which expression gives the population after t years?",
     "multiple_choice",
     "200 * 3^t", "200 * 3^(5t)", "200 * 3^(t/5)", "600t",
     "C",
     "The tripling period is 5 years, so the exponent is t/5. Population = 200 * 3^(t/5).",
     "exponential_growth"),

    # =========================================================================
    # DATA & STATISTICS — 12 questions
    # =========================================================================

    # diff=1 F
    ("algebra_1", "data_stats", "F", 1,
     "Find the mean of: 4, 8, 6, 10, 12.",
     "multiple_choice",
     "7", "8", "9", "10",
     "B",
     "Sum = 4 + 8 + 6 + 10 + 12 = 40. Mean = 40 / 5 = 8.",
     "mean_median"),

    # diff=1 F
    ("algebra_1", "data_stats", "F", 1,
     "Find the median of: 3, 7, 11, 15, 9.",
     "multiple_choice",
     "7", "9", "11", "15",
     "B",
     "Ordered: 3, 7, 9, 11, 15. The middle value is 9.",
     "mean_median"),

    # diff=2 F
    ("algebra_1", "data_stats", "F", 2,
     "What is the mode of: 5, 5, 7, 9, 14?",
     "multiple_choice",
     "5", "7", "9", "14",
     "A",
     "The mode is the value appearing most often. 5 appears twice; all others appear once.",
     "mean_median"),

    # diff=2 U
    ("algebra_1", "data_stats", "U", 2,
     "A scatter plot shows that as x increases, y generally decreases. What type of correlation is this?",
     "multiple_choice",
     "Positive", "Negative", "No correlation", "Perfect",
     "B",
     "When one variable increases as the other decreases, the correlation is negative.",
     "scatter_plots"),

    # diff=2 U
    ("algebra_1", "data_stats", "U", 2,
     "High temperatures for 5 days: 72, 75, 68, 80, 75. What is the range?",
     "multiple_choice",
     "7", "8", "12", "15",
     "C",
     "Range = Maximum - Minimum = 80 - 68 = 12.",
     "mean_median"),

    # diff=3 U
    ("algebra_1", "data_stats", "U", 3,
     "A student scored 82, 90, 78, and 94 on four tests. What score on the 5th test gives a mean of 87?",
     "multiple_choice",
     "88", "89", "90", "91",
     "D",
     "Needed total: 87 x 5 = 435. Sum so far: 82 + 90 + 78 + 94 = 344. Score needed: 435 - 344 = 91.",
     "mean_median"),

    # diff=3 A
    ("algebra_1", "data_stats", "A", 3,
     "A line of best fit is y = 2.5x + 10. Predict y when x = 8.",
     "multiple_choice",
     "28", "30", "32", "34",
     "B",
     "y = 2.5(8) + 10 = 20 + 10 = 30.",
     "scatter_plots"),

    # diff=3 A
    ("algebra_1", "data_stats", "A", 3,
     "A box plot shows Q1 = 20, Q2 = 35, Q3 = 50. What is the interquartile range (IQR)?",
     "multiple_choice",
     "15", "20", "25", "30",
     "D",
     "IQR = Q3 - Q1 = 50 - 20 = 30.",
     "data_display"),

    # diff=3 R
    ("algebra_1", "data_stats", "R", 3,
     "Adding a value that is much larger than all existing data points will most affect which measure?",
     "multiple_choice",
     "Mode", "Median", "Mean", "Range",
     "C",
     "An extreme outlier pulls the mean significantly but has little effect on the median or mode.",
     "mean_median"),

    # diff=4 A
    ("algebra_1", "data_stats", "A", 4,
     "Survey results: 0 books — 5 students, 1 book — 8, 2 books — 4, 3 books — 3. What is the mean number of books?",
     "multiple_choice",
     "1.1", "1.25", "1.3", "1.5",
     "B",
     "Total books: 0(5) + 1(8) + 2(4) + 3(3) = 0 + 8 + 8 + 9 = 25. Total students: 20. Mean = 25/20 = 1.25.",
     "mean_median"),

    # diff=4 R
    ("algebra_1", "data_stats", "R", 4,
     "A line of best fit is y = 3x - 5. A data point is at (4, 10). What is the residual for this point?",
     "multiple_choice",
     "-2", "0", "2", "3",
     "D",
     "Predicted value: y = 3(4) - 5 = 7. Residual = actual - predicted = 10 - 7 = 3.",
     "scatter_plots"),

    # diff=5 R
    ("algebra_1", "data_stats", "R", 5,
     "A data set has 9 values with mean 50. A 10th value of 95 is added. What is the new mean?",
     "multiple_choice",
     "52.5", "54.5", "55", "57.5",
     "B",
     "Original sum: 9 x 50 = 450. New sum: 450 + 95 = 545. New mean: 545 / 10 = 54.5.",
     "mean_median"),
]

def seed():
    conn = sqlite3.connect(DB_PATH)
    inserted = 0
    for q in QUESTIONS:
        exists = conn.execute("SELECT id FROM questions WHERE question_text = ?", (q[4],)).fetchone()
        if not exists:
            conn.execute("""INSERT INTO questions (track, sat_domain, fuar_dimension, difficulty,
                question_text, question_type, option_a, option_b, option_c, option_d,
                correct_answer, explanation, topic_tag) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)""", q)
            inserted += 1
    conn.commit()
    conn.close()
    print(f"[seed] supplement: {inserted} new questions inserted")
    return inserted

if __name__ == "__main__":
    seed()
