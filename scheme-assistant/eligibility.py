"""
Eligibility Engine
-------------------
Rule-based matching of a user's profile against the scheme database.
Chosen over a black-box ML model because:
  - It's fully explainable (judges/users can see WHY a scheme matched)
  - Government eligibility criteria are rule-based by nature (income caps,
    category, age bands) — no training data needed
  - Easy to extend with new schemes without retraining anything
"""

import json
import os

SCHEMES_PATH = os.path.join(os.path.dirname(__file__), "schemes.json")


def load_schemes():
    with open(SCHEMES_PATH, "r") as f:
        return json.load(f)


def check_scheme(user, scheme):
    """
    Compares a single scheme's rules against the user profile.
    Returns a dict: {matched, score, reasons(list), missing(list)}
    """
    reasons = []
    missing = []
    total_checks = 0
    passed_checks = 0

    # Age check
    total_checks += 1
    if scheme["min_age"] <= user["age"] <= scheme["max_age"]:
        passed_checks += 1
        reasons.append(f"Age {user['age']} is within the eligible range "
                        f"({scheme['min_age']}-{scheme['max_age']})")
    else:
        missing.append(f"Age must be between {scheme['min_age']} and {scheme['max_age']}")

    # Category check
    total_checks += 1
    if "All" in scheme["categories"] or user["category"] in scheme["categories"]:
        passed_checks += 1
        reasons.append(f"Category '{user['category']}' is eligible")
    else:
        missing.append(f"Category must be one of: {', '.join(scheme['categories'])}")

    # Income check
    total_checks += 1
    if user["income"] <= scheme["max_income"]:
        passed_checks += 1
        reasons.append(f"Annual income within limit (≤ ₹{scheme['max_income']:,})")
    else:
        missing.append(f"Annual income must be ≤ ₹{scheme['max_income']:,}")

    # Education level check
    total_checks += 1
    if user["education_level"] in scheme["education_level"]:
        passed_checks += 1
        reasons.append(f"Education level '{user['education_level']}' matches")
    else:
        missing.append(f"Education level must be one of: {', '.join(scheme['education_level'])}")

    # State check
    total_checks += 1
    if "All" in scheme["states"] or user["state"] in scheme["states"]:
        passed_checks += 1
        reasons.append("State/UT is eligible")
    else:
        missing.append(f"Only available in: {', '.join(scheme['states'])}")

    # Gender check
    total_checks += 1
    if scheme["gender"] == "Any" or user["gender"] == scheme["gender"]:
        passed_checks += 1
        reasons.append(f"Gender criterion satisfied")
    else:
        missing.append(f"Only open to: {scheme['gender']} applicants")

    # Disability check
    total_checks += 1
    if not scheme["disability_required"] or user.get("has_disability", False):
        passed_checks += 1
        if scheme["disability_required"]:
            reasons.append("Disability certificate requirement satisfied")
    else:
        missing.append("Requires a valid disability certificate (40% or above)")

    score = round((passed_checks / total_checks) * 100)
    matched = len(missing) == 0

    return {
        "matched": matched,
        "score": score,
        "reasons": reasons,
        "missing": missing
    }


def get_eligible_schemes(user):
    """
    Runs the user profile against every scheme.
    Returns two lists: fully eligible schemes, and 'close matches'
    (score >= 70 but missing 1-2 criteria) so users see near-misses too.
    """
    schemes = load_schemes()
    eligible = []
    close_matches = []

    for scheme in schemes:
        result = check_scheme(user, scheme)
        entry = {
            "id": scheme["id"],
            "name": scheme["name"],
            "domain": scheme["domain"],
            "score": result["score"],
            "reasons": result["reasons"],
            "missing": result["missing"],
            "documents": scheme["documents"],
            "apply_link": scheme["apply_link"],
            "apply_steps": scheme["apply_steps"]
        }
        if result["matched"]:
            eligible.append(entry)
        elif result["score"] >= 70:
            close_matches.append(entry)

    eligible.sort(key=lambda x: x["score"], reverse=True)
    close_matches.sort(key=lambda x: x["score"], reverse=True)

    return {"eligible": eligible, "close_matches": close_matches}
