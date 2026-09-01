import re

def extract_signals(snippet: str) -> dict:
    text = snippet.lower()

    risk_flags = []

    # Risk flags
    if "litigation" in text:
        risk_flags.append("litigation")

    if "regulatory" in text or "regulator" in text:
        risk_flags.append("regulatory")

    if (
        "top three customers" in text
        or "customer concentration" in text
        or "customers together account" in text
    ):
        risk_flags.append("customer concentration")

    # Hedging detection
    hedging_phrases = ["assuming", "cautiously", "visibility"]

    hedging_detected = any(
        phrase in text for phrase in hedging_phrases
    )

    # Sentiment classification
    if "confident" in text or "approved" in text:
        sentiment = "confident"
    elif hedging_detected:
        sentiment = "cautious"
    else:
        sentiment = "neutral"

    return {
        "risk_flags": risk_flags,
        "hedging_detected": hedging_detected,
        "sentiment": sentiment
    }
