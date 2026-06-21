"""
app.py - Flask API server for AI Email Guardian

Endpoints:
  POST /analyze  - Analyze an email and return classification results
  GET  /health   - Server health check
"""

import os
import sys
from flask import Flask, request, jsonify
from flask_cors import CORS

# Import our custom modules
from model import load_model, predict
from utils import (
    detect_phishing_keywords,
    detect_urls,
    calculate_risk_score,
    determine_priority,
)

app = Flask(__name__)

# Allow requests from the frontend (running on a different port in development)
CORS(app, origins="*")

# Load the trained model once at startup so each request is fast
print("Loading AI model...")
try:
    classifier, vectorizer = load_model()
    print("Model loaded successfully!")
except Exception as e:
    print(f"Error loading model: {e}")
    sys.exit(1)


@app.route('/health', methods=['GET'])
def health():
    """Simple health check so the frontend can confirm the API is running."""
    return jsonify({"status": "ok", "message": "AI Email Guardian is running"})


@app.route('/analyze', methods=['POST'])
def analyze():
    """
    Analyze an email and return:
    - category (important / spam / promotion / phishing)
    - confidence (0.0 to 1.0)
    - risk_score (0 to 100)
    - priority (High / Medium / Low)
    - highlighted_words (list of suspicious words found)
    - probabilities (breakdown for each category)
    - urls (list of URLs found in the email)
    """
    data = request.get_json(silent=True)

    if not data or 'text' not in data:
        return jsonify({
            "error": "Please provide an 'email text' in the request body."
        }), 400

    email_text = data['text'].strip()

    if not email_text:
        return jsonify({
            "error": "Email text cannot be empty."
        }), 400

    if len(email_text) > 10000:
        return jsonify({
            "error": "Email text is too long. Please keep it under 10,000 characters."
        }), 400

    # Run the ML classification
    category, confidence, probabilities = predict(email_text, classifier, vectorizer)

    # Detect suspicious keywords (for highlighting in the UI)
    suspicious_words = detect_phishing_keywords(email_text)

    # Find any URLs embedded in the email
    urls = detect_urls(email_text)

    # Calculate how risky this email is (0-100 scale)
    risk_score = calculate_risk_score(
        category, confidence, email_text, suspicious_words, urls
    )

    # Determine urgency level
    priority = determine_priority(category, risk_score, email_text)

    response = {
        "category": category,
        "confidence": round(confidence * 100, 1),
        "risk_score": risk_score,
        "priority": priority,
        "highlighted_words": suspicious_words,
        "probabilities": {
            k: round(v * 100, 1)
            for k, v in probabilities.items()
        },
        "urls_found": urls,
        "url_count": len(urls),
    }

    return jsonify(response)


if __name__ == '__main__':
    port = int(os.environ.get('FLASK_PORT', 5001))
    debug = os.environ.get('FLASK_DEBUG', 'false').lower() == 'true'
    print(f"Starting AI Email Guardian API on port {port}...")
    app.run(host='0.0.0.0', port=port, debug=debug)
