"""Optional Qdrant adapter placeholder.

One-day version uses a lightweight local keyword index in pdf_index.py so the demo
runs without model downloads. To switch to Qdrant:
1. Start docker compose up -d qdrant.
2. Generate embeddings for each PDF chunk.
3. Upsert points with payload fields: source, page, text, doc_type.
4. Query with vector + optional payload filters.
"""

COLLECTION_NAME = 'sales_onboarding_docs'
PAYLOAD_SCHEMA = {'source': 'keyword', 'page': 'integer', 'doc_type': 'keyword', 'text': 'text'}
