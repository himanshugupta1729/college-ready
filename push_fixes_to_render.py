#!/usr/bin/env python3
"""Push question fixes to Render after deploying the /api/fix-questions endpoint."""
import json, requests, sys

RENDER_URL = "https://college-ready.onrender.com"

if len(sys.argv) < 2:
    print("Usage: python3 push_fixes_to_render.py <SECRET_KEY>")
    sys.exit(1)

secret_key = sys.argv[1]

fixes = [
    # 15 wrong answer fixes
    {"id": 1008, "correct_answer": "D", "explanation": "a − b = 1 → a = b + 1. Substitute: 3(b+1) + 2b = 18 → 5b = 15 → b = 3, a = 4. a + b = 7."},
    {"id": 1091, "correct_answer": "B", "explanation": "For continuity at x = 2: left limit = 2k + 1 must equal f(2) = 4 − 1 = 3. So 2k + 1 = 3 → k = 1."},
    {"id": 1139, "correct_answer": "C", "explanation": "V = x²h = 32 → h = 32/x². SA = 2x² + 4xh = 2x² + 128/x. dSA/dx = 4x − 128/x² = 0 → x³ = 32 → x = 2∛4."},
    {"id": 1149, "correct_answer": "A", "explanation": "Let u = x² + 1, du = 2x dx. ∫2x(x²+1)⁴ dx = ∫u⁴ du = u⁵/5 + C = (x²+1)⁵/5 + C."},
    {"id": 1169, "correct_answer": "A", "explanation": "On [0, π/4], cos x ≥ sin x. Area = ∫₀^(π/4)(cos x − sin x)dx = [sin x + cos x]₀^(π/4) = √2 − 1."},
    {"id": 1220, "correct_answer": "B", "explanation": "IBP twice: I = ∫eˣsin x dx. After two rounds: 2I = eˣ(sin x − cos x). So I = eˣ(sin x − cos x)/2 + C."},
    {"id": 1035, "correct_answer": "C", "explanation": "r(x) = (x²−9)/(x−3) = (x+3)(x−3)/(x−3). At x = 3, the function has a removable discontinuity (hole). r(3) is undefined."},
    {"id": 1084, "correct_answer": "D", "explanation": "cos A = 3/5, sin B = 12/13 (Q2, positive). sin(A+B) = (4/5)(−5/13) + (3/5)(12/13) = −20/65 + 36/65 = 16/65."},
    {"id": 1348, "correct_answer": "A", "explanation": "2(x + 4) = 18 → 2x + 8 = 18 → 2x = 10 → x = 5."},
    {"id": 1357, "correct_answer": "B", "explanation": "P = 2(w + l) = 54, l = 2w + 3. So 2(w + 2w + 3) = 54 → 6w + 6 = 54 → w = 8 cm."},
    {"id": 1409, "correct_answer": "C", "explanation": "Mean = (70 + 80 + 85 + 90 + 100)/5 = 425/5 = 85."},
    {"id": 1417, "correct_answer": "A", "explanation": "Original sum = 20 × 10 = 200. New sum = 200 + 40 = 240. New mean = 240/11 ≈ 21.8."},
    {"id": 1471, "correct_answer": "B", "explanation": "Power of a Point: tangent² = external × whole secant. 12² = 6 × whole → 144 = 6w → w = 24."},
    {"id": 1614, "correct_answer": "A", "explanation": "Let u = 2ˣ. u² − 5u + 4 = 0 → (u−1)(u−4) = 0 → u = 1 or u = 4. So 2ˣ = 1 → x = 0; 2ˣ = 4 → x = 2."},
    {"id": 1627, "correct_answer": "A", "explanation": "A=3, period=4π → B=2π/4π=1/2. Phase shift π/2 left: C = B×(π/2) = π/4. y = 3 sin(x/2 + π/4) − 1."},
    # 5 flawed question fixes
    {"id": 967, "correct_answer": "B",
     "question_text": "A square piece of metal has a smaller square of side x cut from each corner. The metal is then folded to form a box. If the original square has side 12 and the volume of the box is 128, what is x?",
     "explanation": "V = x(12−2x)² = 128. Testing x = 2: 2(12−4)² = 2 × 64 = 128. ✓"},
    {"id": 1150, "correct_answer": "C",
     "option_c": "(4√2 − 2)/3",
     "explanation": "u = x²+1, du = 2x dx. Bounds: u=1 to u=2. ∫√u du = [2u^(3/2)/3] from 1 to 2 = (4√2 − 2)/3."},
    {"id": 1248, "correct_answer": "B",
     "option_b": "9π/2",
     "explanation": "Area(circle r=3) = 9π. Area(r=2+cosθ) = (1/2)∫(2+cosθ)²dθ = 9π/2. Region = 9π − 9π/2 = 9π/2."},
    {"id": 1381, "correct_answer": "A",
     "question_text": "A canoe rental costs $12 to rent plus $4 per hour. A kayak costs $6 to rent plus $7 per hour. After how many hours will both rentals cost the same amount?",
     "explanation": "12 + 4h = 6 + 7h → 6 = 3h → h = 2 hours."},
    {"id": 1508, "correct_answer": "A",
     "question_text": "What is the remainder when 2x⁴ − 3x³ + x − 15 is divided by (x + 1)?",
     "explanation": "By the Remainder Theorem, evaluate p(−1): 2(1) − 3(−1) + (−1) − 15 = 2 + 3 − 1 − 15 = −11."},
]

print(f"Pushing {len(fixes)} fixes to {RENDER_URL}...")

resp = requests.post(
    f"{RENDER_URL}/api/fix-questions",
    json={"api_key": secret_key, "fixes": fixes},
    timeout=30
)

if resp.status_code == 200:
    result = resp.json()
    print(f"Success: {result['applied']}/{result['total']} fixes applied")
else:
    print(f"Error {resp.status_code}: {resp.text}")
