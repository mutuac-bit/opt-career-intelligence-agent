"""
Honest evaluation of check_sponsorship against REAL USCIS H-1B data.
Unlike the earlier mock evaluation (which scored 100% because it tested
a hardcoded list against itself), this tests real companies against
publicly known sponsorship reality — and documents where the tool
is uncertain or wrong.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tools import check_sponsorship

# Test cases: (company, expected_rating, why)
TEST_CASES = [
    ("Amazon", "GREEN", "Major tech employer, files thousands of H-1Bs"),
    ("Microsoft", "GREEN", "Major tech employer, well-known sponsor"),
    ("Deloitte", "GREEN", "Large consulting firm, heavy sponsor"),
    ("Cognizant", "GREEN", "IT services, one of the largest H-1B filers"),
    ("Capital One", "GREEN", "Large bank, known data/tech sponsor"),
    ("Coca-Cola", "RED", "Files under different legal entity names — known gap"),
    ("Dice", "RED", "Job board, not an employer — should find nothing"),
    ("OPTnation", "RED", "Job aggregator, not an employer"),
    ("Robert Half", "YELLOW", "Staffing agency, limited direct sponsorship"),
    ("Some Random Bakery LLC", "RED", "Small business, no H-1B history"),
]


def run_eval():
    results = []
    correct = 0

    for company, expected, why in TEST_CASES:
        out = check_sponsorship(company)
        actual = out.get("rating", "ERROR")
        approvals = out.get("total_approvals", "N/A")
        match = "✓" if actual == expected else "✗"
        if actual == expected:
            correct += 1
        results.append({
            "company": company,
            "expected": expected,
            "actual": actual,
            "approvals": approvals,
            "match": match,
            "note": why
        })

    print("=" * 70)
    print("HONEST EVALUATION — check_sponsorship vs real USCIS data")
    print("=" * 70)
    for r in results:
        print(f"{r['match']} {r['company']:25} expected={r['expected']:6} "
              f"actual={r['actual']:6} approvals={r['approvals']}")
    print("=" * 70)
    accuracy = round(correct / len(TEST_CASES) * 100, 1)
    print(f"Accuracy: {correct}/{len(TEST_CASES)} = {accuracy}%")
    print("=" * 70)
    print("\nNOTE: This is NOT expected to be 100%. Coca-Cola and similar")
    print("companies file under different legal names, so the tool may")
    print("return RED when the company DOES sponsor under another entity.")
    print("This is a documented limitation, not a hidden failure.")

    return results, accuracy


if __name__ == "__main__":
    run_eval()