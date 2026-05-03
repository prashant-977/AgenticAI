from datetime import date

SCHEMA_REGISTRY = """
orders(id, customer_id, product_id, quantity, created_at)
products(id, name, category, price)
customers(id, name, region_id, segment)
regions(id, name)
onboarding_events(id, rep_name, event_type, completed_at)
"""

def classify_route(question: str) -> str:
    q = question.lower()
    if any(w in q for w in ['policy', 'onboarding', 'playbook', 'qualify', 'lead', 'implementation support', 'refund']):
        return 'rag'
    if any(w in q for w in ['revenue', 'sales', 'orders', 'products', 'region', 'customer']):
        return 'sql'
    return 'hybrid'

def plan_sql(question: str) -> str:
    """Deterministic one-day demo planner. Replace with LLM structured output later."""
    q = question.lower()
    if 'top' in q and 'product' in q:
        return """
        SELECT p.name AS product, ROUND(SUM(o.quantity * p.price), 2) AS revenue, SUM(o.quantity) AS units
        FROM orders o JOIN products p ON p.id = o.product_id
        WHERE date(o.created_at) >= date('2026-04-01')
        GROUP BY p.name
        ORDER BY revenue DESC
        LIMIT 3
        """
    if 'region' in q:
        return """
        SELECT r.name AS region, ROUND(SUM(o.quantity * p.price), 2) AS revenue
        FROM orders o
        JOIN products p ON p.id = o.product_id
        JOIN customers c ON c.id = o.customer_id
        JOIN regions r ON r.id = c.region_id
        WHERE date(o.created_at) BETWEEN date('2026-01-01') AND date('2026-03-31')
        GROUP BY r.name
        ORDER BY revenue DESC
        LIMIT 100
        """
    return """
    SELECT c.name AS customer, p.name AS product, o.quantity, o.created_at
    FROM orders o
    JOIN customers c ON c.id = o.customer_id
    JOIN products p ON p.id = o.product_id
    ORDER BY o.created_at DESC
    LIMIT 20
    """
