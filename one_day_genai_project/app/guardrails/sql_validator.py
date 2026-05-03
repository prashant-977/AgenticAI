import re

ALLOWED_TABLES = {'orders', 'products', 'customers', 'regions', 'onboarding_events'}
SENSITIVE_TABLES = {'customer_pii', 'finance_summary', 'employee_comp'}
BLOCKED_KEYWORDS = {'DROP','DELETE','UPDATE','INSERT','EXEC','ALTER','TRUNCATE','CREATE','REPLACE'}

def _extract_tables(sql: str) -> set[str]:
    # Simple demo parser: enough for one-day project. Replace with sqlglot for production.
    candidates = re.findall(r"(?:from|join)\s+([a-zA-Z_][\w]*)", sql, flags=re.I)
    return {c.lower() for c in candidates}

def validate_sql(sql: str) -> tuple[bool, str, str | None]:
    if not sql or not sql.strip():
        return False, sql, "Empty SQL"
    upper = sql.upper()
    if not re.match(r"^\s*SELECT\b", sql, flags=re.I):
        return False, sql, "Only SELECT queries are allowed"
    for word in BLOCKED_KEYWORDS:
        if re.search(rf"\b{word}\b", upper):
            return False, sql, f"Blocked keyword: {word}"
    tables = _extract_tables(sql)
    unknown = tables - ALLOWED_TABLES - SENSITIVE_TABLES
    if unknown:
        return False, sql, f"Unknown or disallowed table(s): {', '.join(sorted(unknown))}"
    if not re.search(r"\blimit\b", sql, flags=re.I):
        sql = sql.rstrip(';') + ' LIMIT 100'
    return True, sql, None

def requires_human_approval(sql: str) -> bool:
    tables = _extract_tables(sql)
    return bool(tables & SENSITIVE_TABLES) or 'revenue by customer' in sql.lower()
