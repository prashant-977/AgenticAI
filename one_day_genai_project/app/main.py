from fastapi import FastAPI
from app.models import AskRequest, AskResponse
from app.controls.orchestrator import ask, REVIEW_QUEUE
from app.guardrails.sql_validator import validate_sql
from app.tools.sales_tools import get_top_products, get_revenue_by_region
from datetime import date

app = FastAPI(title='Sales + Onboarding GenAI Assistant')

@app.get('/health')
def health():
    return {'status': 'ok'}

@app.post('/ask', response_model=AskResponse)
def ask_endpoint(req: AskRequest):
    return ask(req)

@app.post('/sql/validate')
def validate(sql: str):
    ok, final_sql, error = validate_sql(sql)
    return {'valid': ok, 'sql': final_sql, 'error': error}

@app.get('/tools/top-products')
def top_products(start_date: date, end_date: date, limit: int = 3):
    return get_top_products(start_date, end_date, limit)

@app.get('/tools/revenue-by-region')
def revenue_by_region(start_date: date, end_date: date):
    return get_revenue_by_region(start_date, end_date)

@app.get('/review/queue')
def review_queue():
    return {'items': REVIEW_QUEUE, 'count': len(REVIEW_QUEUE)}
