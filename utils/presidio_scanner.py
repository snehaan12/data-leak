from presidio_analyzer import AnalyzerEngine, PatternRecognizer, Pattern

analyzer = AnalyzerEngine()

# Add custom recognizer for BANK_ACCOUNT
bank_pattern = Pattern(name="BANK_ACCOUNT", regex=r"\b\d{9,18}\b", score=0.85)
bank_recognizer = PatternRecognizer(supported_entity="BANK_ACCOUNT", patterns=[bank_pattern])
analyzer.registry.add_recognizer(bank_recognizer)

# Scan for only selected entities
ENTITY_FILTER = [
    "EMAIL_ADDRESS",
    "PHONE_NUMBER",
    "CREDIT_CARD_NUMBER",
    "US_SOCIAL_SECURITY_NUMBER",
    "AADHAAR",
    "BANK_ACCOUNT"  # ✅ newly added
]

def scan_with_presidio(text: str):
    results = analyzer.analyze(
        text=text,
        entities=ENTITY_FILTER,
        language='en'
    )
    findings = []
    for result in results:
        findings.append({
            "entity_type": result.entity_type,
            "score": result.score,
            "text": text[result.start:result.end]
        })
    return findings
