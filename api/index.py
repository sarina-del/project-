from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import re

app = Flask(__name__)
CORS(app)


@app.route('/')
def home():
    return render_template('index.html')

#modified by shayaan-
@app.route('/api/data', methods=['GET'])
def get_data():
    return jsonify({"message": "Hello from Vercel Serverless Python!"})


def analyse_misinformation(text):
    """Simple rule-based demo analyser for the prototype."""
    if not text or not text.strip():
        return {
            "score": 0,
            "label": "No Content Provided",
            "reasons": ["Please paste an article, claim, or social media post to analyse."],
            "suggestions": ["Add text and try again."]
        }

    text_lower = text.lower()
    score = 100
    reasons = []
    suggestions = []

    emotional_words = [
        "shocking", "urgent", "breaking", "exposed", "secret", "scam",
        "must share", "danger", "they don't want you to know", "miracle",
        "guaranteed", "unbelievable", "viral", "panic"
    ]

    source_words = [
        "source", "according to", "reported by", "study", "research",
        "evidence", "official", "published", "university", "government"
    ]

    if len(text) < 80:
        score -= 15
        reasons.append("The text is very short, so there is not enough context to verify the claim.")

    if any(word in text_lower for word in emotional_words):
        score -= 20
        reasons.append("The text contains emotional or sensational language.")
        suggestions.append("Be careful with content designed to create fear, anger, or panic.")

    uppercase_letters = sum(1 for c in text if c.isupper())
    letters = sum(1 for c in text if c.isalpha())
    if letters > 0 and uppercase_letters / letters > 0.35:
        score -= 15
        reasons.append("The text uses many capital letters, which can be a sign of exaggeration.")

    if "!!!" in text or "???" in text:
        score -= 10
        reasons.append("The text uses repeated punctuation, which can indicate clickbait or emotional persuasion.")

    if not any(word in text_lower for word in source_words):
        score -= 20
        reasons.append("No clear source or evidence is mentioned.")
        suggestions.append("Check whether the claim appears on trusted news or official websites.")

    if re.search(r"share (this|now)|forward this|send this", text_lower):
        score -= 10
        reasons.append("The text pressures users to share it quickly.")
        suggestions.append("Do not share urgent claims until they are verified.")

    if not reasons:
        reasons.append("No major warning signs were detected by the demo rules.")
        suggestions.append("Still verify the information with at least two reliable sources.")

    suggestions.extend([
        "Check the original source of the information.",
        "Compare the claim with trusted news platforms or official organisations.",
        "Check the publication date and author details."
    ])

    score = max(0, min(100, score))

    if score >= 75:
        label = "Likely Reliable"
    elif score >= 45:
        label = "Needs Verification"
    else:
        label = "Possibly Misleading"

    return {
        "score": score,
        "label": label,
        "reasons": reasons,
        "suggestions": list(dict.fromkeys(suggestions))
    }


def summarise_policy(policy):
    """Simple rule-based privacy policy summariser for the prototype."""
    if not policy or not policy.strip():
        return {
            "summary": "Please paste a privacy policy to summarise.",
            "data_collected": [],
            "risks": [],
            "rights": [],
            "risk_level": "No Content Provided"
        }

    text = policy.lower()

    data_collected = []
    risks = []
    rights = []
    risk_points = 0

    checks = {
        "Name": ["name", "full name"],
        "Email address": ["email", "e-mail"],
        "Phone number": ["phone", "mobile number", "telephone"],
        "Location data": ["location", "gps", "geolocation"],
        "Device information": ["device", "ip address", "browser", "operating system"],
        "Cookies": ["cookies", "tracking technologies"],
        "Payment information": ["payment", "credit card", "billing"]
    }

    for label, keywords in checks.items():
        if any(keyword in text for keyword in keywords):
            data_collected.append(label)

    if any(word in text for word in ["third party", "third-party", "partners", "advertisers"]):
        risks.append("Data may be shared with third-party services or partners.")
        risk_points += 2

    if any(word in text for word in ["location", "gps", "geolocation"]):
        risks.append("Location tracking may affect user privacy.")
        risk_points += 2

    if any(word in text for word in ["advertising", "ads", "marketing", "personalized"]):
        risks.append("User data may be used for advertising or personalised content.")
        risk_points += 1

    if any(word in text for word in ["cookies", "tracking"]):
        risks.append("Cookies or tracking technologies may monitor user behaviour.")
        risk_points += 1

    if any(word in text for word in ["delete", "deletion", "erase"]):
        rights.append("User may request data deletion.")

    if any(word in text for word in ["consent", "withdraw"]):
        rights.append("User may withdraw or manage consent settings.")

    if any(word in text for word in ["access", "correct", "update"]):
        rights.append("User may request access to or correction of personal data.")

    if not data_collected:
        data_collected.append("No specific data types were detected by the demo rules.")

    if not risks:
        risks.append("No major privacy risks were detected by the demo rules.")

    if not rights:
        rights.append("No clear user rights were detected in the pasted text.")

    if risk_points >= 4:
        risk_level = "High Risk"
    elif risk_points >= 2:
        risk_level = "Medium Risk"
    else:
        risk_level = "Low Risk"

    summary = (
        "This policy explains how the service may collect, use, and manage user data. "
        "The summary below is simplified for easier understanding and should be checked against the full policy."
    )

    return {
        "summary": summary,
        "data_collected": data_collected,
        "risks": risks,
        "rights": rights,
        "risk_level": risk_level
    }


@app.route('/api/check-misinformation', methods=['POST'])
def check_misinformation():
    data = request.get_json() or {}
    text = data.get('text', '')
    return jsonify(analyse_misinformation(text))


@app.route('/api/summarise-policy', methods=['POST'])
def summarise_policy_api():
    data = request.get_json() or {}
    policy = data.get('policy', '')
    return jsonify(summarise_policy(policy))


if __name__ == '__main__':
    app.run(debug=True)
