from datetime import date
from app.integrations.database import run_select

class ToolError(Exception):
    pass

def get_top_products(start_date: date, end_date: date, limit: int = 3) -> dict:
    if limit < 1 or limit > 20:
        raise ToolError('limit must be between 1 and 20')
    if end_date < start_date:
        raise ToolError('end_date must be after start_date')
    sql = f'''
    SELECT p.name AS product, SUM(o.quantity * p.price) AS revenue, SUM(o.quantity) AS units
    FROM orders o
    JOIN products p ON p.id = o.product_id
    WHERE date(o.created_at) BETWEEN date('{start_date}') AND date('{end_date}')
    GROUP BY p.name
    ORDER BY revenue DESC
    LIMIT {limit}
    '''
    rows = run_select(sql)
    return {'status': 'success', 'data': rows, 'sql_executed': sql.strip(), 'row_count': len(rows)}

def get_revenue_by_region(start_date: date, end_date: date) -> dict:
    if end_date < start_date:
        raise ToolError('end_date must be after start_date')
    sql = f'''
    SELECT r.name AS region, ROUND(SUM(o.quantity * p.price), 2) AS revenue
    FROM orders o
    JOIN products p ON p.id = o.product_id
    JOIN customers c ON c.id = o.customer_id
    JOIN regions r ON r.id = c.region_id
    WHERE date(o.created_at) BETWEEN date('{start_date}') AND date('{end_date}')
    GROUP BY r.name
    ORDER BY revenue DESC
    LIMIT 100
    '''
    rows = run_select(sql)
    return {'status': 'success', 'data': rows, 'sql_executed': sql.strip(), 'row_count': len(rows)}
