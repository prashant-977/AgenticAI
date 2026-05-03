# One-Day Feature Checklist

## Must-have
- FastAPI app with `/ask`, `/health`, SQL validator, sales tools, review queue.
- Streamlit frontend with chat input, route label, confidence, SQL block, table output, PDF sources.
- SQLite sales database with products, customers, regions, orders, onboarding events.
- Dummy PDFs: sales playbook and new-hire onboarding guide.
- Input guardrails: unsafe keywords, prompt injection patterns, PII patterns.
- SQL guardrails: SELECT-only, keyword blocklist, table allowlist, LIMIT enforcement.
- RAG: PDF text extraction, chunking, searchable index, source display.
- Human-in-loop: sensitive SQL routes to review queue.

## Nice-to-have
- Gradio alternate UI.
- Role selector.
- Feedback buttons.
- Query history panel.
- Docker Compose with Qdrant.
- Replace deterministic planner with LLM structured output.
