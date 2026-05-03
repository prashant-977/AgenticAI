import re

BLOCK_PATTERNS = [
    r"\b(drop|delete|update|insert|alter|truncate|exec)\b",
    r"ignore previous instructions",
    r"system prompt",
]
PII_PATTERNS = [r"\bssn\b", r"social security", r"customer_pii", r"email addresses?", r"phone numbers?"]

class GuardrailResult(dict):
    pass

def check_user_question(question: str, user_role: str = 'sales_rep') -> GuardrailResult:
    q = question.lower()
    for pat in BLOCK_PATTERNS:
        if re.search(pat, q):
            return GuardrailResult(allowed=False, reason=f"Blocked unsafe request pattern: {pat}")
    for pat in PII_PATTERNS:
        if re.search(pat, q) and user_role != 'admin':
            return GuardrailResult(allowed=False, reason="PII-style request requires admin approval")
    return GuardrailResult(allowed=True, reason="ok")
