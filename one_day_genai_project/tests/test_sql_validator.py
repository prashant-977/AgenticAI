from app.guardrails.sql_validator import validate_sql

def test_blocks_delete():
    ok, _, error = validate_sql('DELETE FROM orders')
    assert not ok
    assert 'Only SELECT' in error or 'Blocked' in error

def test_enforces_limit():
    ok, sql, error = validate_sql('SELECT * FROM orders')
    assert ok
    assert 'LIMIT' in sql.upper()
