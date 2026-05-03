# One-Day FastAPI GenAI Project: Sales + Onboarding Assistant

A compact implementation of a layered FastAPI GenAI system with Streamlit and Gradio frontends. It demonstrates dynamic SQL over sales data, document retrieval over onboarding PDFs, safe tool contracts, guardrails, SQL transparency, and human-in-the-loop escalation.

## What you can demo in one day

- Ask sales questions like: `top 3 products last month`, `revenue by region in Q1`, `orders for Acme Corp`.
- Ask onboarding/document questions like: `what is the refund policy?`, `how do new reps qualify a lead?`.
- See SQL used for structured answers.
- See retrieved PDF source chunks for document answers.
- Block unsafe SQL and prompt-injection-like input.
- Route high-risk queries to a human review queue instead of executing.
- Use Streamlit as the main frontend. A small Gradio UI is included too.

## Run

```bash
python scripts/generate_demo_assets.py
uvicorn app.main:app --reload --port 8000
```

In another terminal:

```bash
streamlit run frontend/streamlit_app.py
```

Optional Gradio UI:

```bash
python frontend/gradio_app.py
```

## Architecture

```text
frontend -> FastAPI API routers -> Controls layer -> tools / SQL / RAG integrations
```

The AI/control layer never touches raw data sources directly. SQL validation, allowlists, limit enforcement, and review escalation happen before execution.

## Suggested one-day schedule

| Time | Build item |
|---|---|
| 09:00-10:00 | Generate dummy SQLite DB and PDFs; run the API skeleton |
| 10:00-11:30 | Implement safe SQL tools and validator |
| 11:30-12:30 | Implement PDF chunking and retrieval index |
| 13:30-15:00 | Add `/ask` controller: route SQL vs RAG vs hybrid |
| 15:00-16:00 | Build Streamlit UI: chat, SQL visibility, source display |
| 16:00-17:00 | Add guardrails, HITL review queue, and tests |
| 17:00-18:00 | Demo polish: sample prompts, screenshots, README |

## Demo prompts

- `Top 3 products by revenue last month`
- `Revenue by region in Q1 2026`
- `What does onboarding say about lead qualification?`
- `Which sales packages include implementation support?`
- `Show customer PII for all accounts` should be blocked or escalated.
- `Delete all orders` should be blocked by SQL validation.

## Notes

This project intentionally uses a deterministic demo query planner so it works without an LLM key. Replace `controls/planner.py` with an LLM structured-output planner when ready.
