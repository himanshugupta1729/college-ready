"""Supplemental Grade 7 questions to reach 3x test variety."""
import sqlite3, os
DB_PATH = os.environ.get('DATABASE_PATH', 'college_ready.db')

QUESTIONS = [
    # (track, sat_domain, fuar_dimension, difficulty, question_text, question_type,
    #  option_a, option_b, option_c, option_d, correct_answer, explanation, topic_tag)

    # ══════════════════════════════════════════════════════════════════════════
    # PROPORTIONAL RELATIONSHIPS  (24 questions)
    # ══════════════════════════════════════════════════════════════════════════

    # Proportional relationships — basic
    ("grade_7", "proportional", "F", 1,
     "A car travels 150 miles in 3 hours at a constant speed. What is the unit rate in miles per hour?",
     "multiple_choice", "45 mph", "50 mph", "55 mph", "60 mph", "B",
     "Unit rate = 150 ÷ 3 = 50 miles per hour.", "proportional"),

    ("grade_7", "proportional", "F", 1,
     "Which table shows a proportional relationship between x and y?\n"
     "Table A: x=1,2,3 → y=3,6,9\n"
     "Table B: x=1,2,3 → y=2,5,8\n"
     "Table C: x=1,2,3 → y=1,3,6\n"
     "Table D: x=1,2,3 → y=4,6,8",
     "multiple_choice",
     "Table A", "Table B", "Table C", "Table D", "A",
     "Table A: each ratio y/x = 3, so y = 3x. All others fail the constant-ratio test.", "proportional"),

    ("grade_7", "proportional", "F", 1,
     "If y = 0 when x = 0, and y = 24 when x = 8, what is the constant of proportionality?",
     "multiple_choice", "2", "3", "4", "16", "B",
     "k = y/x = 24/8 = 3.", "proportional"),

    ("grade_7", "proportional", "U", 2,
     "The constant of proportionality for a relationship is k = 4.5. If x = 6, what is y?",
     "multiple_choice", "24", "27", "28.5", "30", "B",
     "y = kx = 4.5 × 6 = 27.", "proportional"),

    ("grade_7", "proportional", "U", 2,
     "A recipe requires 2.5 cups of flour for every 12 cookies. How many cups are needed for 36 cookies?",
     "multiple_choice", "6.5 cups", "7 cups", "7.5 cups", "8 cups", "C",
     "36 ÷ 12 = 3 batches. 3 × 2.5 = 7.5 cups.", "proportional"),

    ("grade_7", "proportional", "U", 3,
     "A car uses 4 gallons of gas for every 96 miles. How many gallons are needed for 264 miles?",
     "multiple_choice", "10", "11", "12", "13", "B",
     "Rate = 96 ÷ 4 = 24 mpg. Gallons needed = 264 ÷ 24 = 11.", "proportional"),

    ("grade_7", "proportional", "A", 3,
     "The graph of a proportional relationship passes through (0, 0) and (5, 8). What is the constant of proportionality?",
     "multiple_choice", "1.4", "1.6", "1.8", "2.0", "B",
     "k = y/x = 8/5 = 1.6.", "proportional"),

    ("grade_7", "proportional", "A", 3,
     "A map uses scale 1 inch = 25 miles. Two cities are 3.6 inches apart on the map. What is the actual distance?",
     "multiple_choice", "80 miles", "85 miles", "90 miles", "95 miles", "C",
     "Actual distance = 3.6 × 25 = 90 miles.", "proportional"),

    ("grade_7", "proportional", "A", 3,
     "A recipe for 8 servings needs 3 cups of oats. How many cups are needed for 20 servings?",
     "multiple_choice", "6.5 cups", "7 cups", "7.5 cups", "8 cups", "C",
     "Rate = 3/8 cups per serving. For 20 servings: 20 × 3/8 = 7.5 cups.", "proportional"),

    ("grade_7", "proportional", "A", 4,
     "On a coordinate plane, a proportional relationship passes through (0, 0) and (8, 20). Which other point lies on the line?",
     "multiple_choice", "(4, 9)", "(6, 14)", "(10, 25)", "(12, 28)", "C",
     "k = 20/8 = 2.5. Check (10, 25): 2.5 × 10 = 25. Correct.", "proportional"),

    ("grade_7", "proportional", "R", 4,
     "Two variables x and y are proportional. When x = 14, y = 21. Find y when x = 22.",
     "multiple_choice", "y = 30", "y = 31", "y = 33", "y = 35", "C",
     "k = 21/14 = 1.5, so y = 1.5x. When x = 22: y = 1.5 × 22 = 33.", "proportional"),

    ("grade_7", "proportional", "R", 4,
     "A worker earns $13.50 per hour and works 37.5 hours in a week. What are her total earnings?",
     "multiple_choice", "$496.25", "$503.75", "$506.25", "$512.50", "C",
     "Earnings = 13.50 × 37.5 = $506.25.", "proportional"),

    # Percent problems
    ("grade_7", "proportional", "F", 2,
     "A jacket costs $80 and is on sale for 25% off. What is the sale price?",
     "multiple_choice", "$55", "$58", "$60", "$65", "C",
     "Discount = 25% × 80 = $20. Sale price = 80 − 20 = $60.", "percent"),

    ("grade_7", "proportional", "U", 2,
     "A store marks up a shirt from $15 to $21. What is the percent markup?",
     "multiple_choice", "30%", "35%", "40%", "45%", "C",
     "Markup = (21 − 15)/15 × 100 = 6/15 × 100 = 40%.", "percent"),

    ("grade_7", "proportional", "U", 3,
     "A town's population increased from 12,000 to 13,500. What is the percent increase?",
     "multiple_choice", "10.5%", "11%", "12%", "12.5%", "D",
     "Percent increase = (1500/12000) × 100 = 12.5%.", "percent"),

    ("grade_7", "proportional", "A", 3,
     "After a 20% discount, a video game costs $44. What was the original price?",
     "multiple_choice", "$52", "$54", "$55", "$58", "C",
     "0.80 × original = 44, so original = 44 ÷ 0.80 = $55.", "percent"),

    ("grade_7", "proportional", "A", 4,
     "A savings account earns 3% simple interest per year. $2,400 is deposited. How much interest is earned in 2.5 years?",
     "multiple_choice", "$160", "$172", "$180", "$192", "C",
     "I = P × r × t = 2400 × 0.03 × 2.5 = $180.", "percent"),

    ("grade_7", "proportional", "R", 4,
     "A restaurant bill is $54.00. A customer leaves an 18% tip. What is the total amount paid?",
     "multiple_choice", "$62.72", "$63.72", "$64.00", "$64.72", "B",
     "Tip = 0.18 × 54 = $9.72. Total = 54 + 9.72 = $63.72.", "percent"),

    # Scale drawings
    ("grade_7", "proportional", "F", 1,
     "A scale drawing uses 1 cm = 5 m. A room is 4 cm long on the drawing. What is the actual length?",
     "multiple_choice", "15 m", "18 m", "20 m", "25 m", "C",
     "Actual length = 4 × 5 = 20 m.", "scale_drawings"),

    ("grade_7", "proportional", "U", 2,
     "On a blueprint, a hallway is 6.5 cm long. The scale is 1 cm : 3 m. What is the actual length?",
     "multiple_choice", "17.5 m", "18.5 m", "19.0 m", "19.5 m", "D",
     "Actual length = 6.5 × 3 = 19.5 m.", "scale_drawings"),

    ("grade_7", "proportional", "A", 3,
     "A garden is 18 m long. On a scale drawing it appears 6 cm long. What scale is being used?",
     "multiple_choice", "1 cm : 2 m", "1 cm : 3 m", "1 cm : 4 m", "1 cm : 6 m", "B",
     "Scale = actual ÷ drawing = 18 ÷ 6 = 3 m per cm, so 1 cm : 3 m.", "scale_drawings"),

    ("grade_7", "proportional", "R", 4,
     "A map has scale 1 inch : 40 miles. Two cities are 175 miles apart. How many inches apart on the map?",
     "multiple_choice", "3.875 in", "4.125 in", "4.375 in", "4.625 in", "C",
     "Map distance = 175 ÷ 40 = 4.375 inches.", "scale_drawings"),

    ("grade_7", "proportional", "R", 5,
     "A candle burns at a constant rate. After 3 hours it is 14 cm tall; after 7 hours it is 6 cm tall. How fast is it burning?",
     "multiple_choice", "1 cm/hr", "2 cm/hr", "3 cm/hr", "4 cm/hr", "B",
     "Change in height = 14 − 6 = 8 cm over 4 hours. Rate = 8/4 = 2 cm/hr.", "proportional"),

    ("grade_7", "proportional", "R", 5,
     "Printer A prints 45 pages in 3 minutes. Printer B prints 80 pages in 5 minutes. Which is faster and by how many pages per minute?",
     "multiple_choice",
     "A is faster by 1 page/min",
     "B is faster by 1 page/min",
     "They are equal",
     "A is faster by 5 pages/min", "B",
     "Printer A: 45/3 = 15 ppm. Printer B: 80/5 = 16 ppm. B is faster by 1 ppm.", "proportional"),

    # ══════════════════════════════════════════════════════════════════════════
    # NUMBER SYSTEM — INTEGER OPS, RATIONAL NUMBERS, ABSOLUTE VALUE  (24 questions)
    # ══════════════════════════════════════════════════════════════════════════

    # Integer operations
    ("grade_7", "number_system_7", "F", 1,
     "What is (−8) + (−5)?",
     "multiple_choice", "−13", "−3", "3", "13", "A",
     "(−8) + (−5) = −13. Adding two negatives gives a larger negative.", "integer_operations"),

    ("grade_7", "number_system_7", "F", 1,
     "What is (−6) − (−10)?",
     "multiple_choice", "−16", "−4", "4", "16", "C",
     "(−6) − (−10) = −6 + 10 = 4.", "integer_operations"),

    ("grade_7", "number_system_7", "F", 1,
     "What is the absolute value of −23?",
     "multiple_choice", "−23", "0", "1", "23", "D",
     "|−23| = 23.", "absolute_value"),

    ("grade_7", "number_system_7", "U", 2,
     "What is (−4) × (−9)?",
     "multiple_choice", "−36", "−13", "13", "36", "D",
     "Negative × negative = positive. (−4) × (−9) = 36.", "integer_operations"),

    ("grade_7", "number_system_7", "U", 2,
     "What is (−72) ÷ 8?",
     "multiple_choice", "−9", "−8", "8", "9", "A",
     "Negative ÷ positive = negative. −72 ÷ 8 = −9.", "integer_operations"),

    ("grade_7", "number_system_7", "U", 2,
     "What is the sum of −14 and its additive inverse?",
     "multiple_choice", "−28", "−14", "0", "14", "C",
     "The additive inverse of −14 is 14. (−14) + 14 = 0.", "integer_operations"),

    ("grade_7", "number_system_7", "U", 2,
     "Which number is closest to zero: −3/4, 1/5, −2/3, or 3/8?",
     "multiple_choice", "−3/4", "1/5", "−2/3", "3/8", "B",
     "Decimals: −0.75, 0.2, −0.667, 0.375. Closest to 0 is 0.2 = 1/5.", "rational_numbers"),

    ("grade_7", "number_system_7", "A", 3,
     "The temperature was −12°F at midnight. By noon it rose 25°F. What was the noon temperature?",
     "multiple_choice", "11°F", "13°F", "15°F", "17°F", "B",
     "−12 + 25 = 13°F.", "integer_operations"),

    ("grade_7", "number_system_7", "A", 3,
     "A submarine is at −240 feet. It rises 65 feet, then descends 110 feet. What is its new depth?",
     "multiple_choice", "−280 feet", "−285 feet", "−290 feet", "−295 feet", "B",
     "−240 + 65 − 110 = −285 feet.", "integer_operations"),

    ("grade_7", "number_system_7", "A", 3,
     "Evaluate: (−3)² + (−2)³",
     "multiple_choice", "1", "−1", "17", "−17", "A",
     "(−3)² = 9. (−2)³ = −8. 9 + (−8) = 1.", "integer_operations"),

    ("grade_7", "number_system_7", "A", 3,
     "A diver descends 2.4 meters per minute. How far has she descended after 3.5 minutes?",
     "multiple_choice", "−7.4 m", "−8.0 m", "−8.4 m", "−8.8 m", "C",
     "2.4 × 3.5 = 8.4 m descended, so position is −8.4 m.", "rational_numbers"),

    ("grade_7", "number_system_7", "A", 4,
     "A bank account had −$48.75. After three equal deposits, the balance is $8.25. How much was each deposit?",
     "multiple_choice", "$18.25", "$19.00", "$19.25", "$19.75", "B",
     "Total deposited = 8.25 − (−48.75) = $57.00. Each deposit = 57.00 ÷ 3 = $19.00.", "rational_numbers"),

    ("grade_7", "number_system_7", "A", 4,
     "A football team gained 8 yards, lost 12 yards, gained 3 yards, and lost 5 yards. What is the net yardage?",
     "multiple_choice", "−8 yards", "−6 yards", "−4 yards", "6 yards", "B",
     "8 − 12 + 3 − 5 = −6 yards.", "integer_operations"),

    ("grade_7", "number_system_7", "R", 4,
     "On a number line, point A is at −15 and point B is at 9. What is the distance between A and B?",
     "multiple_choice", "6", "15", "24", "25", "C",
     "Distance = |−15 − 9| = |−24| = 24.", "integer_operations"),

    ("grade_7", "number_system_7", "R", 4,
     "Two points on a number line: P at −7 and Q at 4. Point R is the midpoint of PQ. What is |R|?",
     "multiple_choice", "0.5", "1.0", "1.5", "2.0", "C",
     "Midpoint = (−7 + 4)/2 = −3/2 = −1.5. |−1.5| = 1.5.", "absolute_value"),

    ("grade_7", "number_system_7", "R", 4,
     "The record high temperature in a city is 98°F and the record low is −17°F. What is the range?",
     "multiple_choice", "81°F", "95°F", "105°F", "115°F", "D",
     "Range = 98 − (−17) = 98 + 17 = 115°F.", "integer_operations"),

    # Rational numbers
    ("grade_7", "number_system_7", "F", 2,
     "What is −3/4 + 1/2?",
     "multiple_choice", "−1/2", "−1/4", "1/4", "1/2", "B",
     "−3/4 + 2/4 = −1/4.", "rational_numbers"),

    ("grade_7", "number_system_7", "U", 3,
     "What is (−2/3) × (3/4)?",
     "multiple_choice", "−1/2", "−1/3", "1/3", "1/2", "A",
     "(−2/3) × (3/4) = −6/12 = −1/2.", "rational_numbers"),

    ("grade_7", "number_system_7", "U", 3,
     "What is −5/6 ÷ 1/3?",
     "multiple_choice", "−5/18", "−5/2", "5/18", "5/2", "B",
     "−5/6 ÷ 1/3 = −5/6 × 3/1 = −15/6 = −5/2.", "rational_numbers"),

    ("grade_7", "number_system_7", "A", 3,
     "A submarine descends 3/4 mile per minute. How far has it descended after 2 2/3 minutes?",
     "multiple_choice", "1.5 miles", "2 miles", "2.5 miles", "3 miles", "B",
     "2 2/3 = 8/3. Distance = 3/4 × 8/3 = 24/12 = 2 miles.", "rational_numbers"),

    # Absolute value
    ("grade_7", "number_system_7", "U", 2,
     "Which of the following equals 5?\nA) |−5|\nB) −|5|\nC) |5 − 10|\nD) Both A and C",
     "multiple_choice", "|−5| = 5 only", "−|5| = −5", "|5 − 10| = 5 only", "Both A and C equal 5", "D",
     "|−5| = 5 and |5 − 10| = |−5| = 5. Both A and C equal 5.", "absolute_value"),

    ("grade_7", "number_system_7", "A", 3,
     "If |x| = 8, what are the possible values of x?",
     "multiple_choice", "x = 8 only", "x = −8 only", "x = 8 or x = −8", "x = 0", "C",
     "|x| = 8 means x = 8 or x = −8.", "absolute_value"),

    ("grade_7", "number_system_7", "R", 5,
     "Find all integers x such that |2x − 3| = 7.",
     "multiple_choice", "x = 5 only", "x = −2 only", "x = 5 or x = −2", "x = 2 or x = −5", "C",
     "Case 1: 2x − 3 = 7 → x = 5. Case 2: 2x − 3 = −7 → 2x = −4 → x = −2.", "absolute_value"),

    ("grade_7", "number_system_7", "R", 5,
     "Which expression has the greatest value?\nA) (−3)³\nB) (−2)⁴\nC) −(4²)\nD) (−5)²",
     "multiple_choice",
     "(−3)³ = −27", "(−2)⁴ = 16", "−(4²) = −16", "(−5)² = 25", "D",
     "(−3)³ = −27, (−2)⁴ = 16, −(4²) = −16, (−5)² = 25. Greatest is 25.", "integer_operations"),

    # ══════════════════════════════════════════════════════════════════════════
    # EXPRESSIONS & EQUATIONS  (28 questions)
    # ══════════════════════════════════════════════════════════════════════════

    # Combining like terms
    ("grade_7", "expressions_7", "F", 1,
     "Identify the coefficient of x in: 9x − 4",
     "multiple_choice", "−4", "4", "9", "−9", "C",
     "The coefficient is the number multiplied by the variable: 9.", "combining_like_terms"),

    ("grade_7", "expressions_7", "F", 1,
     "Simplify: 5x + 3 − 2x + 7",
     "multiple_choice", "3x + 4", "3x + 10", "7x + 10", "7x + 4", "B",
     "5x − 2x = 3x and 3 + 7 = 10. Result: 3x + 10.", "combining_like_terms"),

    ("grade_7", "expressions_7", "U", 2,
     "Simplify: 4a − 3b + 2a + 5b",
     "multiple_choice", "6a + 2b", "6a − 2b", "2a + 2b", "2a + 8b", "A",
     "4a + 2a = 6a and −3b + 5b = 2b. Result: 6a + 2b.", "combining_like_terms"),

    ("grade_7", "expressions_7", "U", 2,
     "Which expression is equivalent to 2x − (3 − x)?",
     "multiple_choice", "x − 3", "3x − 3", "x + 3", "3x + 3", "B",
     "2x − 3 + x = 3x − 3.", "combining_like_terms"),

    ("grade_7", "expressions_7", "A", 3,
     "Simplify: −2(3x − 5) + 4(x + 1)",
     "multiple_choice", "−2x + 14", "−2x + 6", "2x + 6", "2x + 14", "A",
     "−2(3x − 5) = −6x + 10. 4(x + 1) = 4x + 4. Sum: −2x + 14.", "combining_like_terms"),

    ("grade_7", "expressions_7", "A", 3,
     "A rectangle has length (5x − 2) and width (2x + 3). What is the perimeter in simplest form?",
     "multiple_choice", "14x + 2", "14x − 2", "10x + 2", "7x + 1", "A",
     "Perimeter = 2(5x − 2) + 2(2x + 3) = 10x − 4 + 4x + 6 = 14x + 2.", "combining_like_terms"),

    ("grade_7", "expressions_7", "R", 4,
     "If x = −3, evaluate: −2(x + 4) − 3(x − 1)",
     "multiple_choice", "7", "10", "−7", "−10", "B",
     "−2(1) − 3(−4) = −2 + 12 = 10. Here (x+4)=1 and (x−1)=−4 when x=−3.", "combining_like_terms"),

    # Distributive property
    ("grade_7", "expressions_7", "F", 1,
     "Use the distributive property: 7(3x − 2) = ?",
     "multiple_choice", "21x − 2", "21x − 14", "10x − 9", "21x + 14", "B",
     "7 × 3x = 21x and 7 × (−2) = −14. Result: 21x − 14.", "distributive_property"),

    ("grade_7", "expressions_7", "U", 2,
     "Which expression is equivalent to 3(2x − 4) + 5x?",
     "multiple_choice", "11x − 4", "11x − 12", "11x + 12", "6x − 12", "B",
     "3(2x − 4) = 6x − 12. 6x − 12 + 5x = 11x − 12.", "distributive_property"),

    ("grade_7", "expressions_7", "A", 3,
     "Expand and simplify: −3(2x − 4) − (5 − x)",
     "multiple_choice", "−5x + 7", "−5x − 7", "−5x + 17", "5x − 7", "A",
     "−3(2x − 4) = −6x + 12. −(5 − x) = −5 + x. Total: −5x + 7.", "distributive_property"),

    ("grade_7", "expressions_7", "R", 4,
     "A store sells pens for $p and notebooks for $n. Jordan buys 5 of each. The expression 5p + 5n can also be written as:",
     "multiple_choice", "5(p − n)", "5(p + n)", "10pn", "p + n", "B",
     "5p + 5n = 5(p + n) by the distributive property.", "distributive_property"),

    # Two-step equations
    ("grade_7", "expressions_7", "F", 1,
     "Solve: 2x + 5 = 13",
     "multiple_choice", "x = 3", "x = 4", "x = 5", "x = 9", "B",
     "2x = 13 − 5 = 8. x = 4.", "two_step_equations"),

    ("grade_7", "expressions_7", "F", 2,
     "Translate: 'Eight less than three times a number n.'",
     "multiple_choice", "8 − 3n", "3n − 8", "3(n − 8)", "3n + 8", "B",
     "'Three times a number' is 3n. 'Eight less than' means subtract 8: 3n − 8.", "two_step_equations"),

    ("grade_7", "expressions_7", "U", 2,
     "Solve: −4x + 9 = −3",
     "multiple_choice", "x = −3", "x = 1.5", "x = 3", "x = 4.5", "C",
     "−4x = −3 − 9 = −12. x = −12 ÷ −4 = 3.", "two_step_equations"),

    ("grade_7", "expressions_7", "U", 3,
     "Solve: x/3 + 4 = 9",
     "multiple_choice", "x = 5", "x = 13", "x = 15", "x = 39", "C",
     "x/3 = 9 − 4 = 5. x = 5 × 3 = 15.", "two_step_equations"),

    ("grade_7", "expressions_7", "U", 3,
     "Solve: 5 − 3x = −7",
     "multiple_choice", "x = −4", "x = 4", "x = −2/3", "x = 2/3", "B",
     "−3x = −7 − 5 = −12. x = 4.", "two_step_equations"),

    ("grade_7", "expressions_7", "A", 3,
     "A fitness app charges a $12 setup fee plus $8 per month. Find the total cost after 7 months.",
     "multiple_choice", "$60", "$64", "$68", "$72", "C",
     "C = 8(7) + 12 = 56 + 12 = $68.", "two_step_equations"),

    ("grade_7", "expressions_7", "A", 3,
     "A number is tripled and then 8 is subtracted. The result is 22. What is the number?",
     "multiple_choice", "8", "9", "10", "11", "C",
     "3n − 8 = 22. 3n = 30. n = 10.", "two_step_equations"),

    ("grade_7", "expressions_7", "A", 4,
     "Solve: 2(x − 3) = 14",
     "multiple_choice", "x = 4", "x = 7", "x = 8", "x = 10", "D",
     "2x − 6 = 14. 2x = 20. x = 10.", "two_step_equations"),

    ("grade_7", "expressions_7", "A", 4,
     "The sum of two consecutive integers is 89. What is the smaller integer?",
     "multiple_choice", "43", "44", "45", "46", "B",
     "n + (n+1) = 89. 2n = 88. n = 44.", "two_step_equations"),

    ("grade_7", "expressions_7", "R", 4,
     "Lena earns $11.50 per hour plus a $25 weekly bonus. She wants to earn at least $128.50 in a week. What is the minimum whole number of hours she must work?",
     "multiple_choice", "7 hours", "8 hours", "9 hours", "10 hours", "C",
     "11.50h + 25 ≥ 128.50. 11.50h ≥ 103.50. h ≥ 9. Minimum is 9 hours.", "two_step_equations"),

    ("grade_7", "expressions_7", "R", 5,
     "Three consecutive odd integers sum to 45. What is the largest integer?",
     "multiple_choice", "13", "15", "17", "19", "C",
     "Let integers be n, n+2, n+4. 3n + 6 = 45. 3n = 39. n = 13. Largest = 13 + 4 = 17.", "two_step_equations"),

    ("grade_7", "expressions_7", "R", 5,
     "The sum of three consecutive even integers is −18. What is the largest of the three?",
     "multiple_choice", "−8", "−6", "−4", "−2", "C",
     "n + (n+2) + (n+4) = −18. 3n + 6 = −18. 3n = −24. n = −8. Largest = −8 + 4 = −4.", "two_step_equations"),

    # Inequalities
    ("grade_7", "expressions_7", "F", 2,
     "Which value of x is a solution to 3x − 4 > 8?",
     "multiple_choice", "x = 2", "x = 3", "x = 4", "x = 5", "D",
     "3x > 12, so x > 4. Only x = 5 satisfies this.", "inequalities"),

    ("grade_7", "expressions_7", "U", 2,
     "Solve: −2x ≤ 10. Which describes the solution?",
     "multiple_choice", "x ≤ −5", "x ≥ −5", "x ≤ 5", "x ≥ 5", "B",
     "Dividing by −2 flips the inequality: x ≥ −5.", "inequalities"),

    ("grade_7", "expressions_7", "A", 3,
     "Maria has $65. She buys a $20 book and spends the rest on $3 apps. What is the maximum number of apps she can buy?",
     "multiple_choice", "13", "14", "15", "16", "C",
     "3a ≤ 65 − 20 = 45. a ≤ 15. Maximum = 15.", "inequalities"),

    ("grade_7", "expressions_7", "R", 4,
     "Which inequality has the same solution as −3x + 6 < 15?",
     "multiple_choice", "x > −3", "x < −3", "x > 3", "x < 3", "A",
     "−3x < 9. Dividing by −3 (flip): x > −3.", "inequalities"),

    ("grade_7", "expressions_7", "R", 5,
     "Which value of x satisfies BOTH: 2x + 1 > 5 AND 3x − 4 < 11?",
     "multiple_choice", "x = 2", "x = 3", "x = 5", "x = 6", "B",
     "Ineq 1: x > 2. Ineq 2: x < 5. So 2 < x < 5. x = 3 is the only choice in this range.", "inequalities"),

    # ══════════════════════════════════════════════════════════════════════════
    # GEOMETRY  (22 questions)
    # ══════════════════════════════════════════════════════════════════════════

    # Angle relationships
    ("grade_7", "geometry_7", "F", 1,
     "Two angles are supplementary. One angle measures 67°. What is the other angle?",
     "multiple_choice", "23°", "103°", "113°", "123°", "C",
     "Supplementary angles sum to 180°. 180 − 67 = 113°.", "angle_relationships"),

    ("grade_7", "geometry_7", "F", 1,
     "Two angles are complementary. One angle is 38°. What is the other angle?",
     "multiple_choice", "42°", "52°", "62°", "142°", "B",
     "Complementary angles sum to 90°. 90 − 38 = 52°.", "angle_relationships"),

    ("grade_7", "geometry_7", "U", 2,
     "Two vertical angles are formed when two lines intersect. One angle is (3x + 10)° and the other is (5x − 14)°. Find x.",
     "multiple_choice", "x = 10", "x = 11", "x = 12", "x = 13", "C",
     "Vertical angles are equal: 3x + 10 = 5x − 14. 24 = 2x. x = 12.", "angle_relationships"),

    ("grade_7", "geometry_7", "U", 2,
     "Two vertical angles are (6x − 5)° and (4x + 15)°. Find the measure of each angle.",
     "multiple_choice", "45°", "50°", "55°", "60°", "C",
     "6x − 5 = 4x + 15. 2x = 20. x = 10. Angle = 6(10) − 5 = 55°.", "angle_relationships"),

    ("grade_7", "geometry_7", "U", 3,
     "A straight line has three angles on one side: 45°, x°, and 2x°. What is x?",
     "multiple_choice", "40°", "42°", "45°", "48°", "C",
     "Angles on a straight line sum to 180°: 45 + 3x = 180. 3x = 135. x = 45°.", "angle_relationships"),

    ("grade_7", "geometry_7", "A", 3,
     "In triangle ABC, angle A = 55° and angle B = 72°. What is the measure of angle C?",
     "multiple_choice", "43°", "53°", "63°", "73°", "B",
     "Sum of angles in a triangle = 180°. C = 180 − 55 − 72 = 53°.", "angle_relationships"),

    ("grade_7", "geometry_7", "A", 4,
     "Two parallel lines are cut by a transversal. One co-interior (same-side interior) angle is 112°. What is the other co-interior angle?",
     "multiple_choice", "58°", "62°", "68°", "78°", "C",
     "Co-interior angles are supplementary: 180 − 112 = 68°.", "angle_relationships"),

    ("grade_7", "geometry_7", "R", 4,
     "An exterior angle of a triangle is 130°. One non-adjacent interior angle is 75°. What is the other non-adjacent interior angle?",
     "multiple_choice", "45°", "50°", "55°", "60°", "C",
     "Exterior angle = sum of two non-adjacent interior angles: 130 = 75 + x. x = 55°.", "angle_relationships"),

    ("grade_7", "geometry_7", "R", 5,
     "Two adjacent angles form a straight line. One angle is (2x + 15)° and the other is (4x − 9)°. What is the measure of the LARGER angle?",
     "multiple_choice", "73°", "90°", "107°", "115°", "C",
     "(2x+15) + (4x−9) = 180. 6x + 6 = 180. x = 29. Angles: 2(29)+15=73° and 4(29)−9=107°. Larger = 107°.", "angle_relationships"),

    # Circles
    ("grade_7", "geometry_7", "F", 1,
     "A circle has radius 7 cm. What is the circumference? (Use π ≈ 3.14)",
     "multiple_choice", "21.98 cm", "43.96 cm", "153.86 cm", "615.44 cm", "B",
     "C = 2πr = 2 × 3.14 × 7 = 43.96 cm.", "circles"),

    ("grade_7", "geometry_7", "F", 2,
     "A circle has diameter 10 m. What is the area? (Use π ≈ 3.14)",
     "multiple_choice", "31.4 m²", "62.8 m²", "78.5 m²", "314 m²", "C",
     "r = 5. A = πr² = 3.14 × 25 = 78.5 m².", "circles"),

    ("grade_7", "geometry_7", "U", 2,
     "A circular pizza has radius 8 inches. What is its area? (Use π ≈ 3.14, round to nearest whole number)",
     "multiple_choice", "50 in²", "100 in²", "201 in²", "251 in²", "C",
     "A = π × 8² = 3.14 × 64 ≈ 200.96 ≈ 201 in².", "circles"),

    ("grade_7", "geometry_7", "U", 3,
     "The circumference of a circle is 31.4 cm. What is the radius? (Use π ≈ 3.14)",
     "multiple_choice", "4 cm", "5 cm", "6 cm", "10 cm", "B",
     "31.4 = 2 × 3.14 × r = 6.28r. r = 31.4 ÷ 6.28 = 5 cm.", "circles"),

    ("grade_7", "geometry_7", "A", 3,
     "A sprinkler waters a circular area with diameter 14 ft. What area does it cover? (Use π ≈ 3.14)",
     "multiple_choice", "43.96 ft²", "87.92 ft²", "153.86 ft²", "615.44 ft²", "C",
     "r = 7. A = 3.14 × 49 = 153.86 ft².", "circles"),

    ("grade_7", "geometry_7", "A", 3,
     "A circle has circumference 50.24 m. What is its area? (Use π ≈ 3.14)",
     "multiple_choice", "50.24 m²", "100.48 m²", "200.96 m²", "401.92 m²", "C",
     "C = 2πr → r = 50.24/6.28 = 8 m. A = 3.14 × 64 = 200.96 m².", "circles"),

    ("grade_7", "geometry_7", "A", 4,
     "A circular pond has area 200.96 m². What is its diameter? (Use π ≈ 3.14)",
     "multiple_choice", "8 m", "10 m", "16 m", "20 m", "C",
     "200.96 = 3.14 × r². r² = 64. r = 8. Diameter = 16 m.", "circles"),

    ("grade_7", "geometry_7", "R", 4,
     "A circular wheel has circumference 75.36 cm. What is its area? (Use π ≈ 3.14)",
     "multiple_choice", "432.16 cm²", "452.16 cm²", "462.16 cm²", "472.16 cm²", "B",
     "r = 75.36 ÷ 6.28 = 12 cm. A = 3.14 × 144 = 452.16 cm².", "circles"),

    # Cross-sections
    ("grade_7", "geometry_7", "F", 2,
     "What shape is the cross-section when a cube is cut parallel to one of its faces?",
     "multiple_choice", "Triangle", "Rectangle", "Square", "Pentagon", "C",
     "Cutting a cube parallel to a face produces a square cross-section.", "cross_sections"),

    ("grade_7", "geometry_7", "U", 3,
     "A right circular cylinder is cut by a plane perpendicular to its base. What shape is the cross-section?",
     "multiple_choice", "Circle", "Ellipse", "Rectangle", "Triangle", "C",
     "A plane perpendicular to the base of a cylinder produces a rectangular cross-section.", "cross_sections"),

    ("grade_7", "geometry_7", "A", 3,
     "Which cross-section of a rectangular pyramid is a triangle?",
     "multiple_choice",
     "A cut parallel to the base",
     "A cut through the apex perpendicular to the base",
     "A cut parallel to a lateral face",
     "A cut along the base", "B",
     "A plane through the apex and perpendicular to the base creates a triangular cross-section.", "cross_sections"),

    ("grade_7", "geometry_7", "R", 4,
     "A cone has base radius 6 cm. A plane parallel to the base cuts it halfway up. What is the radius of the circular cross-section?",
     "multiple_choice", "2 cm", "3 cm", "4 cm", "6 cm", "B",
     "At half-height, the cross-section radius scales linearly: 6 × (1/2) = 3 cm.", "cross_sections"),

    # ══════════════════════════════════════════════════════════════════════════
    # PROBABILITY  (18 questions)
    # ══════════════════════════════════════════════════════════════════════════

    # Theoretical probability
    ("grade_7", "probability_7", "F", 1,
     "A bag has 4 red, 3 blue, and 5 green marbles. What is the probability of picking a blue marble?",
     "multiple_choice", "1/6", "1/4", "3/12", "1/3", "B",
     "P(blue) = 3/12 = 1/4.", "theoretical_probability"),

    ("grade_7", "probability_7", "F", 1,
     "A fair die is rolled. What is P(rolling a number greater than 4)?",
     "multiple_choice", "1/6", "1/3", "1/2", "2/3", "B",
     "Numbers greater than 4: {5, 6}. P = 2/6 = 1/3.", "theoretical_probability"),

    ("grade_7", "probability_7", "F", 1,
     "A standard 52-card deck is shuffled. What is P(drawing an ace)?",
     "multiple_choice", "1/52", "1/13", "1/4", "4/52", "B",
     "There are 4 aces. P = 4/52 = 1/13.", "theoretical_probability"),

    ("grade_7", "probability_7", "F", 2,
     "A bag has 5 green and 3 yellow cubes. What is P(picking yellow)?",
     "multiple_choice", "3/5", "3/8", "5/8", "5/3", "B",
     "P(yellow) = 3/8.", "theoretical_probability"),

    ("grade_7", "probability_7", "U", 2,
     "A student flipped a coin 40 times and got heads 18 times. What is the experimental P(heads)?",
     "multiple_choice", "9/20", "1/2", "11/20", "18/22", "A",
     "Experimental P(heads) = 18/40 = 9/20.", "experimental_probability"),

    ("grade_7", "probability_7", "U", 2,
     "Theoretical P(event) = 3/5. About how many times would it occur in 100 trials?",
     "multiple_choice", "30", "40", "60", "80", "C",
     "Expected = 3/5 × 100 = 60.", "theoretical_probability"),

    ("grade_7", "probability_7", "U", 3,
     "A spinner has 5 equal sections: 2 red, 1 blue, 2 green. In 60 spins, how many times is green expected?",
     "multiple_choice", "12", "20", "24", "30", "C",
     "P(green) = 2/5. Expected = 2/5 × 60 = 24.", "theoretical_probability"),

    ("grade_7", "probability_7", "U", 3,
     "A number cube (1–6) is rolled. What is P(even OR greater than 4)?",
     "multiple_choice", "1/2", "2/3", "5/6", "1", "B",
     "Even: {2,4,6}. Greater than 4: {5,6}. Union: {2,4,5,6} = 4 outcomes. P = 4/6 = 2/3.", "theoretical_probability"),

    ("grade_7", "probability_7", "A", 3,
     "12 out of 30 surveyed students chose soccer. If the school has 450 students, how many are expected to choose soccer?",
     "multiple_choice", "150", "160", "170", "180", "D",
     "P(soccer) = 12/30 = 2/5. Expected = 2/5 × 450 = 180.", "experimental_probability"),

    ("grade_7", "probability_7", "A", 4,
     "Two fair coins are flipped. What is P(at least one tail)?",
     "multiple_choice", "1/4", "1/2", "3/4", "1", "C",
     "P(at least one tail) = 1 − P(HH) = 1 − 1/4 = 3/4.", "theoretical_probability"),

    # Compound events
    ("grade_7", "probability_7", "F", 2,
     "A coin is flipped and a fair die is rolled. How many outcomes are in the sample space?",
     "multiple_choice", "6", "8", "10", "12", "D",
     "Sample space = 2 (coin) × 6 (die) = 12 outcomes.", "compound_events"),

    ("grade_7", "probability_7", "U", 3,
     "A bag has 3 red and 2 blue chips. A chip is drawn, replaced, then drawn again. What is P(red, then blue)?",
     "multiple_choice", "2/25", "3/25", "6/25", "1/5", "C",
     "P(red) = 3/5, P(blue) = 2/5. P(red then blue) = 3/5 × 2/5 = 6/25.", "compound_events"),

    ("grade_7", "probability_7", "U", 3,
     "A spinner with equal sections A, B, C, D is spun twice. What is P(A both times)?",
     "multiple_choice", "1/16", "1/8", "1/4", "3/8", "A",
     "P(A) = 1/4. P(A and A) = 1/4 × 1/4 = 1/16.", "compound_events"),

    ("grade_7", "probability_7", "A", 3,
     "A menu has 3 appetizers, 4 main courses, and 2 desserts. How many different three-course meals are possible?",
     "multiple_choice", "9", "12", "18", "24", "D",
     "Total = 3 × 4 × 2 = 24.", "compound_events"),

    ("grade_7", "probability_7", "A", 4,
     "3 students are selected from a class where 30% prefer math, 45% prefer science, 25% prefer English. What is P(all 3 prefer math)?",
     "multiple_choice", "0.009", "0.027", "0.09", "0.27", "B",
     "P(math)³ = 0.3³ = 0.027.", "compound_events"),

    ("grade_7", "probability_7", "R", 4,
     "A card is drawn from a standard 52-card deck. What is P(face card OR heart)?",
     "multiple_choice", "11/26", "5/13", "25/52", "7/13", "A",
     "P(face)=12/52, P(heart)=13/52, P(face AND heart)=3/52. P(union)=(12+13−3)/52=22/52=11/26.", "compound_events"),

    ("grade_7", "probability_7", "R", 5,
     "Cards 1–20 are in a bag. What is P(multiple of 3 OR multiple of 5)?",
     "multiple_choice", "7/20", "9/20", "11/20", "13/20", "B",
     "Mult of 3: {3,6,9,12,15,18}=6. Mult of 5: {5,10,15,20}=4. Overlap {15}=1. Union=9. P=9/20.", "theoretical_probability"),

    ("grade_7", "probability_7", "R", 5,
     "A bag has x red and 6 blue marbles. P(red) = 2/5. How many red marbles are in the bag?",
     "multiple_choice", "2", "3", "4", "5", "C",
     "x/(x+6) = 2/5. 5x = 2x + 12. 3x = 12. x = 4.", "theoretical_probability"),

    # ── Extra question to reach exactly 116 (F, diff 2) ──────────────────────
    ("grade_7", "proportional", "F", 2,
     "If y = 7x, what is y when x = 9?",
     "multiple_choice", "54", "56", "63", "72", "C",
     "y = 7 × 9 = 63.", "proportional"),
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
    print(f"[seed] Grade 7 supplement: {inserted} new questions inserted")
    return inserted
