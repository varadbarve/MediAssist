"""
Layer 7 — AI Prompt Injection Protection
Sanitizes input data before it reaches the AI prompt and validates
AI output to ensure it doesn't contain forbidden medical content.
"""

import re
from typing import Dict


# --- Injection patterns to strip from extracted data ---
# These are phrases that an attacker might embed in a crafted PDF
# to hijack the AI prompt behavior.
INJECTION_PATTERNS = [
    r"ignore\s+(all\s+)?(previous|prior|above)\s+(instructions?|prompts?|rules?)",
    r"disregard\s+(all\s+)?(previous|prior|above)",
    r"system\s+prompt",
    r"you\s+are\s+now",
    r"act\s+as\s+(a\s+)?",
    r"pretend\s+(to\s+be|you\s+are)",
    r"forget\s+(all|everything|your)\s+(instructions?|rules?|training)",
    r"new\s+instructions?",
    r"override\s+(your|all|the)\s+",
    r"do\s+not\s+follow",
    r"jailbreak",
    r"DAN\s+mode",
    r"bypass\s+(safety|filter|restriction)",
]

# Compiled regex for efficiency
_INJECTION_REGEX = re.compile(
    "|".join(INJECTION_PATTERNS),
    re.IGNORECASE
)

# --- Forbidden output patterns ---
# The AI must NEVER output these kinds of content
FORBIDDEN_OUTPUT_PATTERNS = [
    r"you\s+have\s+(been\s+)?diagnosed\s+with",
    r"you\s+(definitely|certainly|clearly)\s+have\s+\w+\s+(disease|cancer|disorder|syndrome)",
    r"stop\s+taking\s+(your\s+)?medication",
    r"stop\s+taking\s+(your\s+)?insulin",
    r"you\s+should\s+stop\s+(your\s+)?treatment",
    r"you\s+don'?t\s+need\s+(a\s+)?doctor",
    r"ignore\s+your\s+doctor",
    r"don'?t\s+(go|visit|see)\s+(a\s+|the\s+)?doctor",
    r"(call|dial)\s+911",  # Should not give emergency advice
    r"go\s+to\s+(the\s+)?(emergency|ER|hospital)\s+immediately",
]

_FORBIDDEN_OUTPUT_REGEX = re.compile(
    "|".join(FORBIDDEN_OUTPUT_PATTERNS),
    re.IGNORECASE
)

# Safety disclaimer that must be appended
SAFETY_DISCLAIMER = (
    "\n\nDisclaimer: This is an AI-generated summary for informational purposes only. "
    "It is not a medical diagnosis. Please consult your doctor for professional medical advice."
)


def sanitize_input(extracted_data: Dict) -> Dict:
    """
    Sanitize extracted medical data before passing to the AI prompt.
    Removes any injection attempts embedded in the extracted text.

    Args:
        extracted_data: Dictionary of extracted medical values from PDF.

    Returns:
        Cleaned dictionary safe for prompt inclusion.
    """
    sanitized = {}

    for key, value in extracted_data.items():
        # Clean the key: only allow alphanumeric and underscores
        clean_key = re.sub(r"[^a-zA-Z0-9_]", "", str(key))
        if not clean_key:
            continue

        clean_value = str(value).strip()

        # Check for injection patterns in the value
        if _INJECTION_REGEX.search(clean_value):
            # Log and skip this suspicious value
            print(f"[SECURITY] Prompt injection attempt detected in key '{clean_key}': {clean_value[:100]}")
            continue

        # Truncate excessively long values (legit lab values are short)
        if len(clean_value) > 100:
            clean_value = clean_value[:100]

        sanitized[clean_key] = clean_value

    return sanitized


def validate_output(ai_response: str) -> str:
    """
    Validate AI output to ensure it doesn't contain forbidden medical content.
    If forbidden content is detected, replace with a safe fallback.

    Args:
        ai_response: The raw text response from the AI model.

    Returns:
        Validated (and potentially modified) response string.
    """
    if not ai_response:
        return "No summary available. Please consult your doctor for report interpretation."

    # Check for forbidden patterns
    if _FORBIDDEN_OUTPUT_REGEX.search(ai_response):
        print(f"[SECURITY] AI output contained forbidden medical content. Replacing with safe fallback.")
        return (
            "Your report has been reviewed. Some values may need attention. "
            "For a detailed interpretation of your results and any recommended actions, "
            "please consult with your doctor directly." + SAFETY_DISCLAIMER
        )

    # Ensure disclaimer is present
    if "not a medical diagnosis" not in ai_response.lower() and "consult" not in ai_response.lower():
        ai_response += SAFETY_DISCLAIMER

    return ai_response
