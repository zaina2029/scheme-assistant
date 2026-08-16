git from flask import Flask, render_template, request, jsonify
from eligibility import get_eligible_schemes

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/check-eligibility", methods=["POST"])
def check_eligibility():
    data = request.get_json()

    # Basic validation
    required_fields = ["age", "category", "income", "education_level", "state", "gender"]
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Missing field: {field}"}), 400

    user = {
        "age": int(data["age"]),
        "category": data["category"],
        "income": int(data["income"]),
        "education_level": data["education_level"],
        "state": data["state"],
        "gender": data["gender"],
        "has_disability": data.get("has_disability", False)
    }

    results = get_eligible_schemes(user)
    return jsonify(results)


if __name__ == "__main__":
    app.run(debug=True, port=5000)
