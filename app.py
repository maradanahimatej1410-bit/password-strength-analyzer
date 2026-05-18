import io
import math
import secrets
import string
import os
from datetime import datetime

from flask import Flask, jsonify, make_response, render_template, request
from zxcvbn import zxcvbn

from database import store


app = Flask(__name__)

MAX_PASSWORD_LENGTH = 256
DEFAULT_GENERATOR_LENGTH = 18

COMMON_PASSWORDS = {
    "123456",
    "12345678",
    "123456789",
    "password",
    "qwerty",
    "abc123",
    "111111",
    "123123",
    "admin",
    "letmein",
    "welcome",
    "monkey",
    "dragon",
    "iloveyou",
    "password1",
    "qwerty123",
}


store.init_db()


@app.after_request
def apply_security_headers(response):
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "SAMEORIGIN"
    response.headers["Referrer-Policy"] = "same-origin"
    response.headers["Permissions-Policy"] = "clipboard-write=(self)"
    response.headers["Content-Security-Policy"] = (
        "default-src 'self'; "
        "style-src 'self'; "
        "script-src 'self'; "
        "img-src 'self' data:; "
        "font-src 'self'; "
        "connect-src 'self'; "
        "base-uri 'self'; "
        "form-action 'self'"
    )
    return response


@app.route("/")
def index():
    return render_template("index.html")


@app.post("/api/analyze")
def analyze_password():
    payload = request.get_json(silent=True) or {}
    password = payload.get("password", "")

    if not isinstance(password, str):
        return jsonify({"error": "Password must be a string."}), 400

    if len(password) > MAX_PASSWORD_LENGTH:
        return jsonify({"error": f"Password exceeds {MAX_PASSWORD_LENGTH} characters."}), 413

    analysis = build_analysis(password)
    return jsonify(analysis)


@app.post("/api/generate")
def generate_password():
    payload = request.get_json(silent=True) or {}
    length = clamp_int(payload.get("length", DEFAULT_GENERATOR_LENGTH), 12, 64)
    options = {
        "uppercase": bool(payload.get("uppercase", True)),
        "lowercase": bool(payload.get("lowercase", True)),
        "numbers": bool(payload.get("numbers", True)),
        "symbols": bool(payload.get("symbols", True)),
    }

    if not any(options.values()):
        return jsonify({"error": "Select at least one character type."}), 400

    password = create_secure_password(length, options)
    return jsonify({"password": password, "analysis": build_analysis(password)})


@app.post("/api/history")
def save_analysis():
    payload = request.get_json(silent=True) or {}
    password = payload.get("password", "")

    if not isinstance(password, str) or not password:
        return jsonify({"error": "Enter a password before saving an analysis."}), 400

    if len(password) > MAX_PASSWORD_LENGTH:
        return jsonify({"error": f"Password exceeds {MAX_PASSWORD_LENGTH} characters."}), 413

    analysis = build_analysis(password)
    record = store.save_analysis(password, analysis)
    return jsonify({"record": record, "history": store.get_history()})


@app.get("/api/history")
def get_history():
    return jsonify({"history": store.get_history()})


@app.delete("/api/history/<int:record_id>")
def delete_history_item(record_id):
    deleted = store.delete_history_item(record_id)
    if not deleted:
        return jsonify({"error": "History item not found."}), 404
    return jsonify({"history": store.get_history()})


@app.delete("/api/history")
def clear_history():
    store.clear_history()
    return jsonify({"history": []})


@app.post("/api/export")
def export_report():
    payload = request.get_json(silent=True) or {}
    password = payload.get("password", "")

    if not isinstance(password, str) or not password:
        return jsonify({"error": "Enter a password before exporting a report."}), 400

    if len(password) > MAX_PASSWORD_LENGTH:
        return jsonify({"error": f"Password exceeds {MAX_PASSWORD_LENGTH} characters."}), 413

    analysis = build_analysis(password)
    report = render_text_report(analysis)
    response = make_response(report)
    response.headers["Content-Type"] = "text/plain; charset=utf-8"
    response.headers["Content-Disposition"] = "attachment; filename=password-analysis-report.txt"
    return response


def build_analysis(password):
    empty = password == ""
    zx = zxcvbn(password) if not empty else empty_zxcvbn_result()
    requirements = get_requirements(password)
    missing = [label for key, label in requirement_labels().items() if not requirements[key]]
    reused = store.is_password_reused(password) if password else False
    common = password.lower() in COMMON_PASSWORDS if password else False
    entropy_bits = calculate_entropy_bits(zx, password)
    percentage = calculate_strength_percentage(zx["score"], entropy_bits, requirements, reused, common, password)
    rating = classify_strength(percentage)
    feedback = build_feedback(zx, missing, reused, common, password, percentage)

    return {
        "length": len(password),
        "score": zx["score"],
        "percentage": percentage,
        "rating": rating,
        "entropy_bits": entropy_bits,
        "crack_time": readable_crack_time(zx, empty, reused),
        "requirements": requirements,
        "missing_requirements": missing,
        "feedback": feedback,
        "is_reused": reused,
        "is_common": common,
        "generated_at": datetime.utcnow().isoformat(timespec="seconds") + "Z",
    }


def empty_zxcvbn_result():
    return {
        "score": 0,
        "guesses_log10": 0,
        "crack_times_display": {"offline_slow_hashing_1e4_per_second": "not calculated"},
        "feedback": {"warning": "", "suggestions": []},
    }


def get_requirements(password):
    return {
        "length": len(password) >= 12,
        "uppercase": any(char.isupper() for char in password),
        "lowercase": any(char.islower() for char in password),
        "numbers": any(char.isdigit() for char in password),
        "symbols": any(char in string.punctuation for char in password),
    }


def requirement_labels():
    return {
        "length": "Use at least 12 characters",
        "uppercase": "Add an uppercase letter",
        "lowercase": "Add a lowercase letter",
        "numbers": "Add a number",
        "symbols": "Add a symbol",
    }


def calculate_entropy_bits(zx_result, password):
    if not password:
        return 0.0
    zxcvbn_entropy = float(zx_result.get("guesses_log10", 0)) * math.log2(10)
    pool_entropy = estimate_pool_entropy(password)
    return round(max(zxcvbn_entropy, pool_entropy * 0.75), 1)


def estimate_pool_entropy(password):
    pool_size = 0
    if any(char.islower() for char in password):
        pool_size += 26
    if any(char.isupper() for char in password):
        pool_size += 26
    if any(char.isdigit() for char in password):
        pool_size += 10
    if any(char in string.punctuation for char in password):
        pool_size += len(string.punctuation)
    if pool_size == 0:
        return 0
    return len(password) * math.log2(pool_size)


def calculate_strength_percentage(score, entropy_bits, requirements, reused, common, password):
    if not password:
        return 0

    score_points = (score / 4) * 50
    entropy_points = min(entropy_bits, 100) * 0.3
    requirement_points = (sum(requirements.values()) / len(requirements)) * 20
    length_bonus = min(max(len(password) - 12, 0), 12) * 0.8
    percentage = score_points + entropy_points + requirement_points + length_bonus

    if common:
        percentage = min(percentage, 18)
    if reused:
        percentage = min(percentage, 22)
    if len(password) < 8:
        percentage = min(percentage, 30)

    return int(max(0, min(100, round(percentage))))


def classify_strength(percentage):
    if percentage < 35:
        return "Weak"
    if percentage < 70:
        return "Medium"
    return "Strong"


def readable_crack_time(zx_result, empty, reused):
    if empty:
        return "Not calculated"
    if reused:
        return "Already used in local history"
    return zx_result["crack_times_display"].get("offline_slow_hashing_1e4_per_second", "Unknown")


def build_feedback(zx_result, missing, reused, common, password, percentage):
    messages = []
    suggestions = list(zx_result.get("feedback", {}).get("suggestions", []))
    warning = zx_result.get("feedback", {}).get("warning", "")

    if not password:
        return {
            "summary": "Enter a password to start the analysis.",
            "messages": [],
            "recommendations": [],
        }

    if reused:
        messages.append("This password matches a hash already saved in your local history.")
        suggestions.insert(0, "Choose a new password instead of reusing this one.")
    if common:
        messages.append("This is a commonly used password and is easy to guess.")
        suggestions.insert(0, "Avoid dictionary words, keyboard patterns, and common passwords.")
    if warning:
        messages.append(warning)
    if missing:
        suggestions.extend(missing)
    if percentage >= 70 and not messages:
        messages.append("This password has good length, variety, and guessing resistance.")

    unique_recommendations = []
    for item in suggestions:
        if item and item not in unique_recommendations:
            unique_recommendations.append(item)

    return {
        "summary": classify_strength(percentage),
        "messages": messages,
        "recommendations": unique_recommendations[:6],
    }


def create_secure_password(length, options):
    groups = []
    if options["uppercase"]:
        groups.append(string.ascii_uppercase)
    if options["lowercase"]:
        groups.append(string.ascii_lowercase)
    if options["numbers"]:
        groups.append(string.digits)
    if options["symbols"]:
        groups.append("!@#$%^&*()-_=+[]{};:,.?")

    password_chars = [secrets.choice(group) for group in groups if length >= len(groups)]
    all_chars = "".join(groups)
    while len(password_chars) < length:
        password_chars.append(secrets.choice(all_chars))

    secrets.SystemRandom().shuffle(password_chars)
    return "".join(password_chars)


def clamp_int(value, minimum, maximum):
    try:
        number = int(value)
    except (TypeError, ValueError):
        return minimum
    return max(minimum, min(maximum, number))


def render_text_report(analysis):
    buffer = io.StringIO()
    buffer.write("Password Strength Analysis Report\n")
    buffer.write("=================================\n")
    buffer.write(f"Generated: {analysis['generated_at']}\n")
    buffer.write("Note: This report never includes the password text.\n\n")
    buffer.write(f"Length: {analysis['length']} characters\n")
    buffer.write(f"Strength: {analysis['percentage']}% ({analysis['rating']})\n")
    buffer.write(f"Entropy: {analysis['entropy_bits']} bits\n")
    buffer.write(f"Estimated crack time: {analysis['crack_time']}\n")
    buffer.write(f"Reused locally: {'Yes' if analysis['is_reused'] else 'No'}\n")
    buffer.write(f"Common weak password: {'Yes' if analysis['is_common'] else 'No'}\n\n")

    buffer.write("Feedback\n")
    buffer.write("--------\n")
    for message in analysis["feedback"]["messages"] or ["No major weaknesses detected."]:
        buffer.write(f"- {message}\n")
    for recommendation in analysis["feedback"]["recommendations"]:
        buffer.write(f"- {recommendation}\n")

    return buffer.getvalue()




if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
