import os
import sqlite3
from contextlib import contextmanager
from pathlib import Path

DB_PATH = Path(os.getenv('DATABASE_URL', 'data/sales_onboarding.db'))

@contextmanager
def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()

def run_select(sql: str) -> list[dict]:
    with get_conn() as conn:
        rows = conn.execute(sql).fetchall()
        return [dict(r) for r in rows]
