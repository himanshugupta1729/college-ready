"""Supplemental Grade 6 questions to reach 3x test variety."""
import sqlite3, os
DB_PATH = os.environ.get('DATABASE_PATH', 'college_ready.db')

# Target: 116 questions
# FUAR: F=29, U=29, A=29, R=29
# Difficulty: 1=12, 2=29, 3=35, 4=29, 5=11
# Topics: ratios, number_system, expressions, geometry_6, statistics_6
QUESTIONS = [
    # (track, sat_domain, fuar_dimension, difficulty, question_text, question_type,
    #  option_a, option_b, option_c, option_d, correct_answer, explanation, topic_tag)

    # ═══════════════════════════════════════════════════════════════
    # FLUENCY — 29 questions (F)
    # ═══════════════════════════════════════════════════════════════

    # --- RATIOS F ---
    ("grade_6", "ratios", "F", 1,
     "A car travels 120 miles in 2 hours. What is its speed in miles per hour?",
     "multiple_choice", "50 mph", "60 mph", "70 mph", "80 mph", "B",
     "120 ÷ 2 = 60 miles per hour.", "ratios"),

    ("grade_6", "ratios", "F", 1,
     "Out of 20 students, 8 are wearing glasses. What percentage of students are wearing glasses?",
     "multiple_choice", "30%", "35%", "40%", "45%", "C",
     "8 ÷ 20 = 0.40 = 40%.", "ratios"),

    ("grade_6", "ratios", "F", 2,
     "A store sells 3 notebooks for $4.50. What is the cost of one notebook?",
     "multiple_choice", "$1.00", "$1.25", "$1.50", "$2.00", "C",
     "$4.50 ÷ 3 = $1.50 per notebook.", "ratios"),

    ("grade_6", "ratios", "F", 2,
     "A recipe uses 2 cups of sugar for every 5 cups of flour. If you use 10 cups of flour, how many cups of sugar do you need?",
     "multiple_choice", "2 cups", "3 cups", "4 cups", "5 cups", "C",
     "2/5 = x/10 → x = 4 cups of sugar.", "ratios"),

    ("grade_6", "ratios", "F", 2,
     "A runner completes 5 laps in 20 minutes. How many laps per minute is that?",
     "multiple_choice", "1/3 lap/min", "1/4 lap/min", "1/5 lap/min", "1/6 lap/min", "B",
     "5 ÷ 20 = 1/4 lap per minute.", "ratios"),

    ("grade_6", "ratios", "F", 3,
     "A map has a scale of 1 inch = 50 miles. Two cities are 3.5 inches apart on the map. What is the actual distance?",
     "multiple_choice", "150 miles", "165 miles", "175 miles", "200 miles", "C",
     "3.5 × 50 = 175 miles.", "ratios"),

    ("grade_6", "ratios", "F", 3,
     "There are 18 girls and 12 boys in a class. What is the simplified ratio of girls to boys?",
     "multiple_choice", "18:12", "3:2", "2:3", "6:4", "B",
     "GCF(18,12)=6. 18÷6=3, 12÷6=2. Simplified ratio = 3:2.", "ratios"),

    # --- NUMBER SYSTEM F ---
    ("grade_6", "number_system", "F", 1,
     "What is the greatest common factor (GCF) of 24 and 36?",
     "multiple_choice", "4", "6", "8", "12", "D",
     "Factors of 24: 1,2,3,4,6,8,12,24. Factors of 36: 1,2,3,4,6,9,12,18,36. GCF = 12.", "number_system"),

    ("grade_6", "number_system", "F", 1,
     "What is the least common multiple (LCM) of 4 and 6?",
     "multiple_choice", "10", "12", "16", "24", "B",
     "Multiples of 4: 4,8,12... Multiples of 6: 6,12... LCM = 12.", "number_system"),

    ("grade_6", "number_system", "F", 2,
     "What is 3/4 + 5/6?",
     "multiple_choice", "8/10", "8/12", "1 and 7/12", "19/10", "C",
     "LCD = 12. 9/12 + 10/12 = 19/12 = 1 and 7/12.", "number_system"),

    ("grade_6", "number_system", "F", 2,
     "What is 5/8 − 1/4?",
     "multiple_choice", "4/4", "3/8", "3/4", "1/2", "B",
     "1/4 = 2/8. 5/8 − 2/8 = 3/8.", "number_system"),

    ("grade_6", "number_system", "F", 1,
     "Which number is the opposite of −7 on a number line?",
     "multiple_choice", "−14", "0", "7", "14", "C",
     "The opposite of −7 is 7 (same distance from 0, other side).", "number_system"),

    ("grade_6", "number_system", "F", 2,
     "What is 2.4 × 0.5?",
     "multiple_choice", "0.12", "0.48", "1.2", "12", "C",
     "2.4 × 0.5 = 1.2.", "number_system"),

    ("grade_6", "number_system", "F", 3,
     "What is the value of −3 × (−4)?",
     "multiple_choice", "−12", "−7", "7", "12", "D",
     "Negative × negative = positive: −3 × −4 = 12.", "number_system"),

    # --- EXPRESSIONS F ---
    ("grade_6", "expressions", "F", 1,
     "Evaluate 3x + 7 when x = 4.",
     "multiple_choice", "14", "17", "19", "21", "C",
     "3(4) + 7 = 12 + 7 = 19.", "expressions"),

    ("grade_6", "expressions", "F", 1,
     "Solve for n: n + 9 = 15.",
     "multiple_choice", "4", "5", "6", "7", "C",
     "n = 15 − 9 = 6.", "expressions"),

    ("grade_6", "expressions", "F", 2,
     "Solve for x: 5x = 35.",
     "multiple_choice", "5", "6", "7", "8", "C",
     "x = 35 ÷ 5 = 7.", "expressions"),

    ("grade_6", "expressions", "F", 2,
     "Solve for y: y/6 = 4.",
     "multiple_choice", "10", "18", "24", "36", "C",
     "y = 4 × 6 = 24.", "expressions"),

    ("grade_6", "expressions", "F", 3,
     "Simplify: 3(2x + 4).",
     "multiple_choice", "5x + 4", "6x + 4", "6x + 12", "6x + 7", "C",
     "Distribute: 3 × 2x = 6x, 3 × 4 = 12. Result: 6x + 12.", "expressions"),

    ("grade_6", "expressions", "F", 2,
     "Identify the coefficient in the expression 7m + 4.",
     "multiple_choice", "4", "7", "m", "7m", "B",
     "The coefficient is the number multiplied by the variable. In 7m, the coefficient is 7.", "expressions"),

    # --- GEOMETRY_6 F ---
    ("grade_6", "geometry_6", "F", 1,
     "What is the area of a rectangle with length 9 cm and width 5 cm?",
     "multiple_choice", "28 cm²", "40 cm²", "45 cm²", "54 cm²", "C",
     "Area = length × width = 9 × 5 = 45 cm².", "geometry_6"),

    ("grade_6", "geometry_6", "F", 1,
     "What is the area of a triangle with base 10 m and height 6 m?",
     "multiple_choice", "16 m²", "30 m²", "60 m²", "120 m²", "B",
     "Area = (1/2) × base × height = (1/2) × 10 × 6 = 30 m².", "geometry_6"),

    ("grade_6", "geometry_6", "F", 2,
     "A rectangular prism has length 5 cm, width 4 cm, and height 3 cm. What is its volume?",
     "multiple_choice", "40 cm³", "47 cm³", "60 cm³", "94 cm³", "C",
     "Volume = l × w × h = 5 × 4 × 3 = 60 cm³.", "geometry_6"),

    ("grade_6", "geometry_6", "F", 2,
     "What are the coordinates of a point that is 4 units right and 3 units up from the origin?",
     "multiple_choice", "(3, 4)", "(−4, 3)", "(4, −3)", "(4, 3)", "D",
     "Moving right increases x, moving up increases y: (4, 3).", "geometry_6"),

    ("grade_6", "geometry_6", "F", 3,
     "A point is located at (−3, 5). In which quadrant is it?",
     "multiple_choice", "Quadrant I", "Quadrant II", "Quadrant III", "Quadrant IV", "B",
     "x is negative, y is positive → Quadrant II.", "geometry_6"),

    # --- STATISTICS_6 F ---
    ("grade_6", "statistics_6", "F", 1,
     "Find the mean of: 4, 8, 6, 10, 2.",
     "multiple_choice", "5", "6", "7", "8", "B",
     "Sum = 30. Mean = 30 ÷ 5 = 6.", "statistics_6"),

    ("grade_6", "statistics_6", "F", 1,
     "Find the median of: 3, 7, 1, 9, 5.",
     "multiple_choice", "3", "5", "7", "9", "B",
     "Ordered: 1, 3, 5, 7, 9. Middle value = 5.", "statistics_6"),

    ("grade_6", "statistics_6", "F", 2,
     "Find the range of: 15, 22, 8, 31, 19.",
     "multiple_choice", "13", "19", "23", "39", "C",
     "Range = max − min = 31 − 8 = 23.", "statistics_6"),

    ("grade_6", "statistics_6", "F", 2,
     "A student's test scores are 78, 85, 90, 85, 72. What is the mode?",
     "multiple_choice", "72", "78", "85", "90", "C",
     "85 appears twice; all others appear once. Mode = 85.", "statistics_6"),

    # ═══════════════════════════════════════════════════════════════
    # UNDERSTANDING — 29 questions (U)
    # ═══════════════════════════════════════════════════════════════

    # --- RATIOS U ---
    ("grade_6", "ratios", "U", 2,
     "In a bag there are 8 red marbles and 12 blue marbles. What is the ratio of red to total marbles?",
     "multiple_choice", "2:3", "2:5", "3:5", "8:12", "B",
     "Total = 20. Red:Total = 8:20 = 2:5.", "ratios"),

    ("grade_6", "ratios", "U", 3,
     "A student answered 18 out of 24 questions correctly. What percent did the student get wrong?",
     "multiple_choice", "25%", "30%", "33%", "75%", "A",
     "Wrong: 24 − 18 = 6. Percent wrong: 6/24 = 0.25 = 25%.", "ratios"),

    ("grade_6", "ratios", "U", 3,
     "The ratio of boys to girls in a class is 3:4. There are 28 students total. How many are boys?",
     "multiple_choice", "10", "12", "14", "16", "B",
     "Boys = 3/(3+4) × 28 = 3/7 × 28 = 12.", "ratios"),

    ("grade_6", "ratios", "U", 4,
     "A recipe that serves 4 people calls for 3/4 cup of olive oil. How many cups are needed to serve 10 people?",
     "multiple_choice", "1 cup", "1 and 7/8 cups", "2 cups", "2 and 1/4 cups", "B",
     "(3/4) ÷ 4 × 10 = (3/16) × 10 = 30/16 = 1 and 7/8 cups.", "ratios"),

    ("grade_6", "ratios", "U", 4,
     "A shirt originally costs $40. It is on sale for 25% off. What is the sale price?",
     "multiple_choice", "$10", "$25", "$30", "$35", "C",
     "Discount = 25% × $40 = $10. Sale price = $40 − $10 = $30.", "ratios"),

    ("grade_6", "ratios", "U", 4,
     "A clothing store marks up items by 40%. If the store paid $25 for a shirt, what is the selling price?",
     "multiple_choice", "$10", "$30", "$35", "$40", "C",
     "Markup = 40% × $25 = $10. Selling price = $25 + $10 = $35.", "ratios"),

    # --- NUMBER SYSTEM U ---
    ("grade_6", "number_system", "U", 2,
     "Which point on a number line represents −4?",
     "multiple_choice",
     "4 units to the right of 0",
     "4 units to the left of 0",
     "Between 0 and −1",
     "Between −3 and −5, closer to −3", "B",
     "Negative numbers are to the left of 0. −4 is exactly 4 units left.", "number_system"),

    ("grade_6", "number_system", "U", 2,
     "What is the absolute value of −15?",
     "multiple_choice", "−15", "−1/15", "1/15", "15", "D",
     "|−15| = 15. Absolute value is always the distance from 0, so it is non-negative.", "number_system"),

    ("grade_6", "number_system", "U", 3,
     "A submarine is at −200 feet. A fish is at −50 feet. Which statement is true?",
     "multiple_choice",
     "The submarine is higher because −200 > −50",
     "The fish is higher because −50 > −200",
     "They are at the same depth",
     "The fish is lower because 50 < 200", "B",
     "On a number line −50 > −200, so −50 ft is closer to the surface (higher up).", "number_system"),

    ("grade_6", "number_system", "U", 4,
     "The GCF of 48 and 72 is 24. Use it to simplify 48/72.",
     "multiple_choice", "GCF=12, simplified=4/6", "2/3", "GCF=12, simplified=2/3", "6/9", "B",
     "48 ÷ 24 = 2, 72 ÷ 24 = 3. Simplified fraction = 2/3.", "number_system"),

    ("grade_6", "number_system", "U", 3,
     "Which of the following is equivalent to 0.375?",
     "multiple_choice", "3/8", "3/5", "3/4", "37/100", "A",
     "0.375 = 375/1000 = 3/8.", "number_system"),

    ("grade_6", "number_system", "U", 4,
     "Which is greater: 5/6 or 7/9? Use a common denominator.",
     "multiple_choice",
     "5/6, because 15/18 > 14/18",
     "7/9, because 14/18 > 15/18",
     "They are equal",
     "5/6, because the denominator 6 < 9", "A",
     "LCD = 18. 5/6 = 15/18; 7/9 = 14/18. Since 15 > 14, 5/6 is greater.", "number_system"),

    ("grade_6", "number_system", "U", 2,
     "What is the LCM of 8 and 12?",
     "multiple_choice", "4", "16", "24", "96", "C",
     "Multiples of 8: 8, 16, 24. Multiples of 12: 12, 24. LCM = 24.", "number_system"),

    # --- EXPRESSIONS U ---
    ("grade_6", "expressions", "U", 2,
     "Which equation represents 'a number divided by 3 equals 9'?",
     "multiple_choice", "3n = 9", "n − 3 = 9", "n/3 = 9", "n + 3 = 9", "C",
     "'A number divided by 3' = n/3. 'equals 9' → n/3 = 9.", "expressions"),

    ("grade_6", "expressions", "U", 3,
     "A store charges $4 per pound for cheese. Write an expression for the cost of p pounds and find the cost of 7 pounds.",
     "multiple_choice", "p + 4; $11", "4p; $28", "4p; $24", "4 + p; $11", "B",
     "Expression: 4p. Cost of 7 pounds: 4(7) = $28.", "expressions"),

    ("grade_6", "expressions", "U", 3,
     "Which property justifies 3(x + 5) = 3x + 15?",
     "multiple_choice", "Commutative Property", "Associative Property", "Distributive Property", "Identity Property", "C",
     "Multiplying 3 across (x+5) uses the Distributive Property.", "expressions"),

    ("grade_6", "expressions", "U", 4,
     "Evaluate 2x² − 3x + 1 when x = 2.",
     "multiple_choice", "3", "7", "9", "11", "A",
     "2(4) − 3(2) + 1 = 8 − 6 + 1 = 3.", "expressions"),

    ("grade_6", "expressions", "U", 4,
     "If 3n − 4 = 14, what is the value of n?",
     "multiple_choice", "4", "5", "6", "7", "C",
     "3n = 14 + 4 = 18. n = 18/3 = 6.", "expressions"),

    ("grade_6", "expressions", "U", 3,
     "Which expression shows the perimeter of a rectangle with length l and width w?",
     "multiple_choice", "lw", "2l + w", "2(l + w)", "l + w", "C",
     "Perimeter = l + w + l + w = 2(l + w).", "expressions"),

    ("grade_6", "expressions", "U", 3,
     "A variable expression uses n to represent a number. Which expression means 'six less than three times a number'?",
     "multiple_choice", "6 − 3n", "3n − 6", "3(n − 6)", "3 + n − 6", "B",
     "'Three times a number' = 3n. 'Six less than' means subtract 6: 3n − 6.", "expressions"),

    # --- GEOMETRY_6 U ---
    ("grade_6", "geometry_6", "U", 3,
     "A triangle has base 14 cm and area 63 cm². What is its height?",
     "multiple_choice", "4.5 cm", "7 cm", "9 cm", "18 cm", "C",
     "63 = (1/2)(14)(h) → 63 = 7h → h = 9 cm.", "geometry_6"),

    ("grade_6", "geometry_6", "U", 4,
     "A trapezoid has parallel sides of 8 cm and 12 cm and a height of 5 cm. What is its area?",
     "multiple_choice", "40 cm²", "50 cm²", "60 cm²", "100 cm²", "B",
     "Area = (1/2)(b₁+b₂)(h) = (1/2)(8+12)(5) = (1/2)(20)(5) = 50 cm².", "geometry_6"),

    ("grade_6", "geometry_6", "U", 2,
     "Point A is at (2, 3) and point B is at (2, −1). What is the distance between them?",
     "multiple_choice", "2 units", "4 units", "5 units", "6 units", "B",
     "Same x-coordinate, so distance = |3 − (−1)| = |4| = 4 units.", "geometry_6"),

    ("grade_6", "geometry_6", "U", 3,
     "A point is reflected across the y-axis from (5, −2). What are its new coordinates?",
     "multiple_choice", "(−5, 2)", "(−5, −2)", "(5, 2)", "(2, −5)", "B",
     "Reflecting across the y-axis changes the sign of the x-coordinate: (5,−2) → (−5,−2).", "geometry_6"),

    # --- STATISTICS_6 U ---
    ("grade_6", "statistics_6", "U", 2,
     "Find the mean of: 10, 14, 16, 18, 12.",
     "multiple_choice", "12", "13", "14", "15", "C",
     "Sum = 70. Mean = 70 ÷ 5 = 14.", "statistics_6"),

    ("grade_6", "statistics_6", "U", 2,
     "Which measure of center is most affected by an extreme value (outlier)?",
     "multiple_choice", "Mode", "Median", "Mean", "Range", "C",
     "The mean uses all values, so an outlier pulls it significantly.", "statistics_6"),

    ("grade_6", "statistics_6", "U", 3,
     "A class has scores: 70, 72, 74, 75, 98. Which measure best represents typical performance?",
     "multiple_choice", "Mean (≈ 77.8)", "Median (74)", "Mode (none)", "Range (28)", "B",
     "98 is an outlier that skews the mean. Median (74) better represents the typical student.", "statistics_6"),

    ("grade_6", "statistics_6", "U", 3,
     "In a dot plot, each dot represents one student's score. If there are 5 dots above the number 8, what does that mean?",
     "multiple_choice", "The mean is 8", "8 students scored 5", "5 students scored 8", "The median is 5", "C",
     "In a dot plot, dots above a value show how many data points equal that value.", "statistics_6"),

    ("grade_6", "statistics_6", "U", 3,
     "A box plot shows minimum=5, Q1=10, median=15, Q3=25, maximum=35. What is the interquartile range (IQR)?",
     "multiple_choice", "10", "15", "20", "30", "B",
     "IQR = Q3 − Q1 = 25 − 10 = 15.", "statistics_6"),

    # ═══════════════════════════════════════════════════════════════
    # APPLICATION — 29 questions (A)
    # ═══════════════════════════════════════════════════════════════

    # --- RATIOS A ---
    ("grade_6", "ratios", "A", 3,
     "Mia earns $8.50 per hour babysitting. She worked 6 hours on Saturday and 4 hours on Sunday. How much did she earn in total?",
     "multiple_choice", "$68", "$76", "$85", "$102", "C",
     "Total hours = 10. Earnings = 10 × $8.50 = $85.", "ratios"),

    ("grade_6", "ratios", "A", 4,
     "A school fundraiser sold 240 cookies. If 60% were chocolate chip, how many were NOT chocolate chip?",
     "multiple_choice", "72", "96", "144", "168", "B",
     "Chocolate chip: 60% × 240 = 144. Not chocolate chip: 240 − 144 = 96.", "ratios"),

    ("grade_6", "ratios", "A", 3,
     "On a soccer team the ratio of wins to losses is 5:2. If the team played 28 games (no ties), how many did they win?",
     "multiple_choice", "16", "18", "20", "22", "C",
     "Wins = 5/7 × 28 = 20.", "ratios"),

    ("grade_6", "ratios", "A", 2,
     "A grocery store sells 4 apples for $2.00. How much would 10 apples cost?",
     "multiple_choice", "$4.00", "$4.50", "$5.00", "$5.50", "C",
     "Unit cost = $2.00 ÷ 4 = $0.50. 10 × $0.50 = $5.00.", "ratios"),

    ("grade_6", "ratios", "A", 4,
     "A school survey found 45% of students prefer soccer and 30% prefer basketball. There are 200 students. How many prefer neither sport?",
     "multiple_choice", "40", "50", "60", "75", "B",
     "Soccer: 45% × 200 = 90. Basketball: 30% × 200 = 60. Neither: 200 − 90 − 60 = 50.", "ratios"),

    ("grade_6", "ratios", "A", 3,
     "A smoothie recipe calls for 2 cups of strawberries and 3 cups of mango. You want to scale up using 9 cups of mango. How many cups of strawberries do you need?",
     "multiple_choice", "4 cups", "5 cups", "6 cups", "7 cups", "C",
     "2/3 = x/9 → x = 6 cups of strawberries.", "ratios"),

    # --- NUMBER SYSTEM A ---
    ("grade_6", "number_system", "A", 3,
     "The temperature at noon was 8°F. By midnight it dropped 15°F. What was the midnight temperature?",
     "multiple_choice", "−23°F", "−7°F", "7°F", "23°F", "B",
     "8 − 15 = −7°F.", "number_system"),

    ("grade_6", "number_system", "A", 4,
     "A diver is at −30 feet. She swims up 12 feet, then dives 20 more feet. What is her final depth?",
     "multiple_choice", "−22 feet", "−38 feet", "−42 feet", "−62 feet", "B",
     "−30 + 12 = −18, then −18 − 20 = −38 feet.", "number_system"),

    ("grade_6", "number_system", "A", 2,
     "Maria ran 2.75 miles on Monday and 3.5 miles on Wednesday. How many total miles did she run?",
     "multiple_choice", "5.75 miles", "6.0 miles", "6.25 miles", "6.5 miles", "C",
     "2.75 + 3.5 = 6.25 miles.", "number_system"),

    ("grade_6", "number_system", "A", 3,
     "A pizza was cut into 8 equal slices. Carlos ate 3 slices and his sister ate 2 slices. What fraction of the pizza is left?",
     "multiple_choice", "3/8", "5/8", "3/5", "5/3", "A",
     "Eaten: 3+2=5 slices. Left: 8−5=3 slices. Fraction = 3/8.", "number_system"),

    ("grade_6", "number_system", "A", 5,
     "A stock dropped 3.50 points on Monday, rose 1.25 on Tuesday, and dropped 2.00 on Wednesday. What is the net change over the three days?",
     "multiple_choice", "+4.25", "−4.25", "−0.75", "+0.75", "B",
     "Net = −3.50 + 1.25 − 2.00 = −4.25 points.", "number_system"),

    ("grade_6", "number_system", "A", 4,
     "A mountain peak is at 4,500 ft elevation. A valley is at −200 ft. What is the total difference in elevation?",
     "multiple_choice", "4,300 ft", "4,500 ft", "4,700 ft", "4,900 ft", "C",
     "Difference = 4,500 − (−200) = 4,500 + 200 = 4,700 ft.", "number_system"),

    # --- EXPRESSIONS A ---
    ("grade_6", "expressions", "A", 3,
     "Kai has d dollars. He earns $15 more doing chores and then spends $8 at the movies. Write an expression for how much he has now.",
     "multiple_choice", "d + 15 + 8", "d + 15 − 8", "d − 15 + 8", "d + 23", "B",
     "Start with d, add $15, subtract $8: d + 15 − 8.", "expressions"),

    ("grade_6", "expressions", "A", 4,
     "A plumber charges a $50 flat fee plus $35 per hour. Find the cost for 3 hours of work.",
     "multiple_choice", "$105", "$155", "$185", "$255", "B",
     "C = 50 + 35h. For h = 3: C = 50 + 35(3) = 50 + 105 = $155.", "expressions"),

    ("grade_6", "expressions", "A", 3,
     "A library fines members $0.25 per day for late books. How much is the fine after 12 days?",
     "multiple_choice", "$2.50", "$2.75", "$3.00", "$3.25", "C",
     "Fine = 0.25 × 12 = $3.00.", "expressions"),

    ("grade_6", "expressions", "A", 5,
     "Sam is 3 years older than twice his sister's age. His sister is s years old. If Sam is 19, write and solve an equation to find s.",
     "multiple_choice", "s = 7", "s = 8", "s = 9", "s = 11", "B",
     "2s + 3 = 19 → 2s = 16 → s = 8.", "expressions"),

    ("grade_6", "expressions", "A", 4,
     "A phone plan charges $30 per month plus $0.10 per text. Last month's bill was $44. How many texts were sent?",
     "multiple_choice", "100", "120", "140", "160", "C",
     "30 + 0.10t = 44 → 0.10t = 14 → t = 140 texts.", "expressions"),

    ("grade_6", "expressions", "A", 2,
     "A cafeteria serves 6 classes each with 28 students. Write an expression and calculate the total number of students.",
     "multiple_choice", "6 + 28 = 34", "6 × 28 = 168", "28 − 6 = 22", "28 ÷ 6 ≈ 5", "B",
     "Total = 6 × 28 = 168 students.", "expressions"),

    # --- GEOMETRY_6 A ---
    ("grade_6", "geometry_6", "A", 3,
     "A farmer wants to fence a triangular field with sides 30 m, 45 m, and 60 m. How many meters of fencing are needed?",
     "multiple_choice", "90 m", "115 m", "135 m", "180 m", "C",
     "Perimeter = 30 + 45 + 60 = 135 m.", "geometry_6"),

    ("grade_6", "geometry_6", "A", 4,
     "A gift box (rectangular prism) is 10 in long, 6 in wide, and 4 in tall. How much wrapping paper (surface area) is needed?",
     "multiple_choice", "188 in²", "240 in²", "248 in²", "264 in²", "C",
     "SA = 2(lw + lh + wh) = 2(60 + 40 + 24) = 2(124) = 248 in².", "geometry_6"),

    ("grade_6", "geometry_6", "A", 2,
     "A sandbox is 6 feet long, 4 feet wide, and 1 foot deep. How many cubic feet of sand fill it?",
     "multiple_choice", "10 ft³", "20 ft³", "24 ft³", "48 ft³", "C",
     "Volume = 6 × 4 × 1 = 24 ft³.", "geometry_6"),

    ("grade_6", "geometry_6", "A", 3,
     "On a coordinate plane a square has corners at (1,1), (1,4), (4,4), and (4,1). What is its area?",
     "multiple_choice", "3 sq units", "6 sq units", "9 sq units", "12 sq units", "C",
     "Side length = 4 − 1 = 3. Area = 3² = 9 sq units.", "geometry_6"),

    ("grade_6", "geometry_6", "A", 5,
     "A rectangular room is 14 ft long and 10 ft wide. Carpet costs $3 per sq ft. How much does it cost to carpet the room?",
     "multiple_choice", "$360", "$380", "$400", "$420", "D",
     "Area = 14 × 10 = 140 ft². Cost = 140 × $3 = $420.", "geometry_6"),

    ("grade_6", "geometry_6", "A", 3,
     "A right triangle has legs of 6 cm and 8 cm. What is its area?",
     "multiple_choice", "14 cm²", "24 cm²", "28 cm²", "48 cm²", "B",
     "Area = (1/2)(6)(8) = 24 cm².", "geometry_6"),

    # --- STATISTICS_6 A ---
    ("grade_6", "statistics_6", "A", 3,
     "A basketball player scored 18, 22, 15, 25, and 20 points in five games. What is the mean score per game?",
     "multiple_choice", "18", "19", "20", "22", "C",
     "Sum = 100. Mean = 100 ÷ 5 = 20 points.", "statistics_6"),

    ("grade_6", "statistics_6", "A", 4,
     "A student has an average of 82 after 4 tests. What score does she need on the 5th test to raise her average to 85?",
     "multiple_choice", "88", "93", "95", "97", "D",
     "Current total = 82 × 4 = 328. Target total = 85 × 5 = 425. Score needed = 425 − 328 = 97.", "statistics_6"),

    ("grade_6", "statistics_6", "A", 3,
     "Daily high temperatures for a week: 68, 72, 65, 70, 74, 71, 69°F. What is the range?",
     "multiple_choice", "7°F", "9°F", "10°F", "12°F", "B",
     "Max = 74, Min = 65. Range = 74 − 65 = 9°F.", "statistics_6"),

    ("grade_6", "statistics_6", "A", 2,
     "Five friends compared books read last month: 3, 5, 2, 6, 4. What is the median?",
     "multiple_choice", "3", "4", "5", "6", "B",
     "Ordered: 2, 3, 4, 5, 6. Middle value = 4.", "statistics_6"),

    ("grade_6", "statistics_6", "A", 3,
     "A survey found 8 students walk, 12 bike, 15 take the bus, and 5 get dropped off. How many students were surveyed in total?",
     "multiple_choice", "35", "38", "40", "45", "C",
     "8 + 12 + 15 + 5 = 40 students.", "statistics_6"),

    # ═══════════════════════════════════════════════════════════════
    # REASONING — 29 questions (R)
    # ═══════════════════════════════════════════════════════════════

    # --- RATIOS R ---
    ("grade_6", "ratios", "R", 4,
     "Store A sells 5 pens for $3.00. Store B sells 8 pens for $4.40. Which store has the lower unit price?",
     "multiple_choice", "Store A at $0.55/pen", "Store B at $0.55/pen", "Store A at $0.60/pen", "Store B at $0.60/pen", "B",
     "Store A: $3.00/5 = $0.60/pen. Store B: $4.40/8 = $0.55/pen. Store B is cheaper.", "ratios"),

    ("grade_6", "ratios", "R", 5,
     "A tank fills at 15 gallons/min and drains at 9 gallons/min. The tank holds 180 gallons and starts empty. How many minutes to fill it?",
     "multiple_choice", "20 min", "25 min", "30 min", "36 min", "C",
     "Net fill rate = 15 − 9 = 6 gal/min. Time = 180 ÷ 6 = 30 minutes.", "ratios"),

    ("grade_6", "ratios", "R", 4,
     "A class took a test. 70% of the 30 students passed. How many students failed?",
     "multiple_choice", "7", "9", "10", "12", "B",
     "Passed = 70% × 30 = 21. Failed = 30 − 21 = 9.", "ratios"),

    ("grade_6", "ratios", "R", 5,
     "Jake and Maya share a prize in the ratio 3:5. Maya receives $40 more than Jake. What is the total prize?",
     "multiple_choice", "$100", "$120", "$140", "$160", "D",
     "Difference = 5 − 3 = 2 parts = $40, so 1 part = $20. Total = 8 parts = $160.", "ratios"),

    ("grade_6", "ratios", "R", 3,
     "At a school fair the ratio of game stalls to food stalls is 2:3. There are 15 stalls total. How many are game stalls?",
     "multiple_choice", "5", "6", "8", "10", "B",
     "Game stalls = 2/(2+3) × 15 = 2/5 × 15 = 6.", "ratios"),

    ("grade_6", "ratios", "R", 3,
     "A 12-ounce serving of sports drink provides 25% of the daily value of sodium. How many ounces give 100% of the daily value?",
     "multiple_choice", "36 oz", "40 oz", "48 oz", "50 oz", "C",
     "12 oz = 25%. So 100% = 4 × 12 = 48 oz.", "ratios"),

    # --- NUMBER SYSTEM R ---
    ("grade_6", "number_system", "R", 5,
     "Two numbers have a GCF of 6 and an LCM of 36. One number is 12. What is the other number?",
     "multiple_choice", "6", "18", "24", "36", "B",
     "GCF × LCM = product of the two numbers. 6 × 36 = 216. 216 ÷ 12 = 18.", "number_system"),

    ("grade_6", "number_system", "R", 4,
     "A number line shows points at −6 and 2. What is the distance between them?",
     "multiple_choice", "4", "6", "8", "10", "C",
     "Distance = |−6 − 2| = |−8| = 8.", "number_system"),

    ("grade_6", "number_system", "R", 5,
     "If a/b = 2/3 and b = 15, what is a?",
     "multiple_choice", "5", "8", "10", "12", "C",
     "a/15 = 2/3 → a = 15 × (2/3) = 10.", "number_system"),

    ("grade_6", "number_system", "R", 4,
     "Which expression has the greatest absolute value: |−12|, |8|, |−5|, or |10|?",
     "multiple_choice", "|8|", "|−5|", "|10|", "|−12|", "D",
     "|−12|=12, |8|=8, |−5|=5, |10|=10. Greatest is 12 = |−12|.", "number_system"),

    ("grade_6", "number_system", "R", 3,
     "Order these numbers from least to greatest: −3, 1.5, −0.5, 2, −2.5",
     "multiple_choice",
     "−3, −2.5, −0.5, 1.5, 2",
     "−2.5, −3, −0.5, 1.5, 2",
     "−3, −0.5, −2.5, 1.5, 2",
     "−0.5, −2.5, −3, 1.5, 2", "A",
     "On a number line: −3 < −2.5 < −0.5 < 1.5 < 2.", "number_system"),

    # --- EXPRESSIONS R ---
    ("grade_6", "expressions", "R", 4,
     "If x + 4 = 10 and y = 2x, what is y?",
     "multiple_choice", "8", "10", "12", "20", "C",
     "x = 10 − 4 = 6. y = 2(6) = 12.", "expressions"),

    ("grade_6", "expressions", "R", 5,
     "The expression 4(n + 3) equals 40. What is n?",
     "multiple_choice", "4", "7", "10", "13", "B",
     "4(n + 3) = 40 → n + 3 = 10 → n = 7.", "expressions"),

    ("grade_6", "expressions", "R", 5,
     "Two consecutive even numbers have a sum of 46. What is the smaller number?",
     "multiple_choice", "20", "22", "24", "26", "B",
     "Let n and n+2 be the numbers. n + n+2 = 46 → 2n = 44 → n = 22.", "expressions"),

    ("grade_6", "expressions", "R", 4,
     "Which value of x makes 5x − 3 > 17 true?",
     "multiple_choice", "x = 3", "x = 4", "x = 5", "x = 6", "C",
     "5x > 20 → x > 4. The smallest integer greater than 4 from the choices is x = 5.", "expressions"),

    ("grade_6", "expressions", "R", 3,
     "A student says 2 + 3 × 4 = 20. Is the student correct? What is the right answer?",
     "multiple_choice", "Yes, 20", "No, the answer is 14", "No, the answer is 18", "No, the answer is 24", "B",
     "Order of operations: multiply first. 3 × 4 = 12, then 2 + 12 = 14.", "expressions"),

    ("grade_6", "expressions", "R", 4,
     "The sum of three consecutive integers is 48. What is the largest integer?",
     "multiple_choice", "14", "15", "16", "17", "D",
     "n + (n+1) + (n+2) = 48 → 3n + 3 = 48 → 3n = 45 → n = 15. Largest = n + 2 = 17.", "expressions"),

    # --- GEOMETRY_6 R ---
    ("grade_6", "geometry_6", "R", 4,
     "A rectangular pool is 15 m long and 8 m wide. A path 1 m wide surrounds it. What is the area of just the path?",
     "multiple_choice", "46 m²", "48 m²", "50 m²", "52 m²", "C",
     "Outer dimensions: (15+2) × (8+2) = 17 × 10 = 170 m². Pool area = 15 × 8 = 120 m². Path = 170 − 120 = 50 m².", "geometry_6"),

    ("grade_6", "geometry_6", "R", 4,
     "Point P is at (−2, −3). It is reflected across the x-axis. What are its new coordinates?",
     "multiple_choice", "(2, 3)", "(2, −3)", "(−2, 3)", "(−2, −3)", "C",
     "Reflecting across the x-axis flips the sign of the y-coordinate: (−2, −3) → (−2, 3).", "geometry_6"),

    ("grade_6", "geometry_6", "R", 5,
     "A composite figure is made of a rectangle (8 cm × 5 cm) with a triangle on top (base 8 cm, height 3 cm). What is the total area?",
     "multiple_choice", "40 cm²", "52 cm²", "56 cm²", "64 cm²", "B",
     "Rectangle: 8 × 5 = 40 cm². Triangle: (1/2)(8)(3) = 12 cm². Total = 40 + 12 = 52 cm².", "geometry_6"),

    ("grade_6", "geometry_6", "R", 3,
     "A rectangular garden has perimeter 48 m. Its length is 3 times its width. What is the area?",
     "multiple_choice", "72 m²", "108 m²", "135 m²", "144 m²", "B",
     "2(l+w) = 48 → l+w = 24. l = 3w → 4w = 24 → w = 6, l = 18. Area = 6 × 18 = 108 m².", "geometry_6"),

    ("grade_6", "geometry_6", "R", 5,
     "A city park is shaped like a trapezoid with parallel sides 120 m and 80 m and a height of 60 m. What is the park's area?",
     "multiple_choice", "4,800 m²", "6,000 m²", "7,200 m²", "9,600 m²", "B",
     "Area = (1/2)(b₁+b₂)(h) = (1/2)(120+80)(60) = (1/2)(200)(60) = 6,000 m².", "geometry_6"),

    ("grade_6", "geometry_6", "R", 4,
     "A box-shaped fish tank is 50 cm long, 25 cm wide, and 30 cm high. How many liters of water can it hold? (1 L = 1,000 cm³)",
     "multiple_choice", "3.75 L", "37.5 L", "375 L", "3,750 L", "B",
     "Volume = 50 × 25 × 30 = 37,500 cm³ = 37.5 liters.", "geometry_6"),

    # --- STATISTICS_6 R ---
    ("grade_6", "statistics_6", "R", 4,
     "Two classes have the same mean score of 80. Class A has range 10; Class B has range 40. What can you conclude?",
     "multiple_choice",
     "Class A scored higher overall",
     "Class B's scores are more spread out",
     "Class A has more students",
     "Class B has a higher median", "B",
     "A larger range means greater spread (variability) in the data, not a higher average.", "statistics_6"),

    ("grade_6", "statistics_6", "R", 5,
     "A data set of 7 values has a median of 15. Six known values are 10, 12, 14, 16, 18, 20. What must the missing value be for the median to stay at 15?",
     "multiple_choice", "Any value below 14", "Any value between 14 and 16", "Exactly 15", "Any value above 16", "B",
     "With 7 ordered values the median is the 4th. The missing value must be between 14 and 16 so that position stays 15.", "statistics_6"),

    ("grade_6", "statistics_6", "R", 4,
     "A set of numbers has mean 10 and range 8. If the minimum is 6, what is the maximum?",
     "multiple_choice", "12", "14", "16", "18", "B",
     "Maximum = Minimum + Range = 6 + 8 = 14.", "statistics_6"),

    ("grade_6", "statistics_6", "R", 5,
     "A bar graph shows visitors: Mon=20, Tue=35, Wed=15, Thu=40, Fri=30. On which day is the count closest to the mean?",
     "multiple_choice", "Monday", "Tuesday", "Wednesday", "Friday", "D",
     "Mean = (20+35+15+40+30)/5 = 140/5 = 28. Closest to 28 is Friday (30).", "statistics_6"),

    ("grade_6", "statistics_6", "R", 3,
     "A student removes the highest value from a data set. How does this most likely affect the mean?",
     "multiple_choice", "The mean increases", "The mean stays the same", "The mean decreases", "The mean becomes the median", "C",
     "Removing the highest value reduces the total sum, so the recalculated mean decreases.", "statistics_6"),

    ("grade_6", "statistics_6", "R", 4,
     "A data set of 6 values has a mean of 10. Five of the values are 5, 8, 10, 12, 15. What is the sixth value?",
     "multiple_choice", "8", "9", "10", "11", "C",
     "Total needed = 10 × 6 = 60. Known sum = 5+8+10+12+15 = 50. Sixth value = 60 − 50 = 10.", "statistics_6"),
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
    print(f"[seed] Grade 6 supplement: {inserted} new questions inserted")
    return inserted
