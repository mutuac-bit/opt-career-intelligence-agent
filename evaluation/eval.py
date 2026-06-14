import json
from pathlib import Path
import sys

sys.path.append("..")

from tools import check_sponsorship

BASE_DIR = Path(__file__).parent

with open(BASE_DIR / "test_cases.json", "r") as f:
    test_cases = json.load(f)

correct = 0
total = len(test_cases)

print("\n🚀 Starting Evaluation\n")

for case in test_cases:

    company = case["company"]
    expected = case["expected"]

    prediction = check_sponsorship(company)

    actual = prediction["rating"]

    if actual == expected:
        correct += 1
        print(f"✅ {company} -> {actual}")
    else:
        print(
            f"❌ {company} -> {actual} "
            f"(expected {expected})"
        )

accuracy = correct / total

print("\n========================")
print("Evaluation Results")
print("========================")
print(f"Total Cases: {total}")
print(f"Correct: {correct}")
print(f"Accuracy: {accuracy:.2%}")

results = {
    "accuracy": round(accuracy, 3),
    "total_cases": total,
    "correct_predictions": correct
}

with open(BASE_DIR / "results.json", "w") as f:
    json.dump(results, f, indent=2)

print("\nSaved results.json")