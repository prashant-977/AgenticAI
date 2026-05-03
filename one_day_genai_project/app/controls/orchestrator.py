from app.models import AskRequest, AskResponse, SourceChunk
from app.controls.planner import classify_route, plan_sql
from app.guardrails.input_guardrails import check_user_question
from app.guardrails.sql_validator import validate_sql, requires_human_approval
from app.integrations.database import run_select
from app.rag.pdf_index import search_docs

REVIEW_QUEUE: list[dict] = []

def _answer_from_rows(rows: list[dict]) -> str:
    if not rows:
        return 'No matching rows found. I will not invent an answer.'
    first = rows[0]
    if 'product' in first and 'revenue' in first:
        return 'Top products: ' + '; '.join([f"{r['product']} (${r['revenue']}, {r.get('units', 'n/a')} units)" for r in rows])
    if 'region' in first and 'revenue' in first:
        return 'Revenue by region: ' + '; '.join([f"{r['region']}: ${r['revenue']}" for r in rows])
    return f'Found {len(rows)} recent records. See rows below.'

def _answer_from_sources(question: str, sources: list[dict]) -> str:
    if not sources:
        return 'I could not find supporting content in the indexed PDFs.'
    bullets = []
    for s in sources[:3]:
        excerpt = s['text'][:240].strip()
        bullets.append(f"- {excerpt}...")
    return 'Based on the onboarding/sales PDFs:\n' + '\n'.join(bullets)

def ask(req: AskRequest) -> AskResponse:
    guard = check_user_question(req.question, req.user_role)
    if not guard['allowed']:
        return AskResponse(route='blocked', answer=guard['reason'], confidence=0.95, message=guard['reason'])

    route = classify_route(req.question)
    if route == 'rag':
        docs = search_docs(req.question)
        return AskResponse(route='rag', answer=_answer_from_sources(req.question, docs), sources=[SourceChunk(**d) for d in docs], confidence=0.72)

    sql = plan_sql(req.question)
    ok, sql, error = validate_sql(sql)
    if not ok:
        return AskResponse(route='blocked', answer=f'SQL rejected: {error}', sql_executed=sql, confidence=0.95)
    if requires_human_approval(sql):
        REVIEW_QUEUE.append({'question': req.question, 'sql': sql, 'user_role': req.user_role})
        return AskResponse(route='review', answer='This query requires human approval before execution.', sql_executed=sql, review_required=True, confidence=0.8)
    rows = run_select(sql)
    return AskResponse(route='sql', answer=_answer_from_rows(rows), sql_executed=sql.strip(), rows=rows, confidence=0.78)
