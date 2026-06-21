"""
utils.py - Risk scoring, keyword detection, and priority assignment
"""

import re

# Words that often appear in phishing or fraudulent emails
PHISHING_KEYWORDS = [
    "urgent", "verify", "otp", "click", "password", "account", "suspended",
    "limited", "locked", "compromised", "unauthorized", "illegal", "fraud",
    "bank", "paypal", "apple", "google", "microsoft", "confirm", "login",
    "expire", "immediately", "action", "required", "update", "credentials",
    "secure", "alert", "suspicious", "detected", "blocked", "warning",
    "security", "breach", "threat", "identity", "stolen", "hack", "protect",
]

# Words that suggest high urgency / importance
HIGH_URGENCY_WORDS = [
    "urgent", "deadline", "asap", "immediately", "emergency", "critical",
    "required", "action", "today", "now", "expire", "suspended",
]

# Words commonly found in promotional emails
PROMOTION_WORDS = [
    "sale", "discount", "offer", "deal", "free", "save", "buy", "shop",
    "price", "off", "exclusive", "limited", "special", "promo", "code",
    "coupon", "percent", "weekend", "flash", "clearance",
]


def detect_urls(text):
    """Find all URLs in the email text."""
    url_pattern = re.compile(
        r'https?://[^\s<>"{}|\\^`\[\]]+'
        r'|www\.[^\s<>"{}|\\^`\[\]]+'
        r'|\b[a-zA-Z0-9.-]+\.(com|net|org|io|co|info|biz|xyz|site|online)[^\s]*'
    )
    return url_pattern.findall(text)


def detect_phishing_keywords(text):
    """
    Find phishing-related keywords in the original (uncleaned) text.
    Returns a list of suspicious words found.
    """
    text_lower = text.lower()
    found = []
    for keyword in PHISHING_KEYWORDS:
        # Use word boundary matching so 'bank' matches 'bank' but not 'banking'
        pattern = r'\b' + re.escape(keyword) + r'\b'
        if re.search(pattern, text_lower):
            found.append(keyword)
    return found


def calculate_risk_score(category, confidence, text, suspicious_words, urls):
    """
    Calculate a 0-100 risk score based on multiple signals:
    - The predicted category and model confidence
    - Number of suspicious keywords found
    - Presence of URLs (links are often used in phishing)
    """
    text_lower = text.lower()
    score = 0

    # Base score from the predicted category
    category_base = {
        "phishing": 70,
        "spam": 40,
        "promotion": 20,
        "important": 5,
    }
    score = category_base.get(category, 10)

    # Add points for each suspicious keyword (up to 20 bonus points)
    keyword_bonus = min(len(suspicious_words) * 3, 20)
    score += keyword_bonus

    # Add points for URLs found in the email
    url_count = len(urls)
    if url_count >= 3:
        score += 10
    elif url_count >= 1:
        score += 5

    # Check for all-caps words (shouting = higher risk)
    caps_words = re.findall(r'\b[A-Z]{3,}\b', text)
    if len(caps_words) >= 3:
        score += 8

    # Exclamation marks are a red flag
    exclamation_count = text.count('!')
    if exclamation_count >= 3:
        score += 5

    # Scale by model confidence
    score = int(score * (0.6 + confidence * 0.4))

    # Clamp between 0 and 100
    return max(0, min(100, score))


def determine_priority(category, risk_score, text):
    """
    Assign a priority level based on category and content signals.
    - High: urgent matters or security threats
    - Medium: regular emails that need attention
    - Low: promotions, spam, obvious junk
    """
    text_lower = text.lower()

    # Security threats are always high priority (you need to know!)
    if category == "phishing":
        return "High"

    # Check for urgency words in the text
    urgency_count = sum(
        1 for word in HIGH_URGENCY_WORDS
        if re.search(r'\b' + re.escape(word) + r'\b', text_lower)
    )

    if category == "important":
        if urgency_count >= 2 or risk_score > 50:
            return "High"
        return "Medium"

    if category == "spam":
        return "Low"

    if category == "promotion":
        return "Low"

    return "Medium"
