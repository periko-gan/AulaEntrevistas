# Tests

This directory contains the test suite for the Aula Virtual backend.

## Running Tests

Install development dependencies:
```bash
pip install -r requirements-dev.txt
```

Run all tests:
```bash
pytest
```

Run with coverage:
```bash
pytest --cov=app --cov-report=html
```

Run specific test file:
```bash
pytest tests/test_auth.py
```

Run tests matching a pattern:
```bash
pytest -k "test_register"
```

## Test Structure

- `conftest.py` - Pytest configuration and shared fixtures
- `test_auth.py` - Authentication endpoint tests
- `test_chats.py` - Chat CRUD tests
- `test_messages.py` - Message tests (to be added)
- `test_ai.py` - AI endpoints tests (to be added)

## Writing Tests

Use the provided fixtures:
```python
def test_example(client, auth_headers):
    response = client.get("/api/v1/endpoint", headers=auth_headers)
    assert response.status_code == 200
```

Available fixtures:
- `client` - Test client with clean database
- `db_session` - Database session for direct DB operations
- `auth_headers` - Authentication headers for test user
