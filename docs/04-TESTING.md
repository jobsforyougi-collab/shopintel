# 04 — Testing

## Current state

- **No tests exist.** There is no `tests/` directory.
- `pytest>=8.4` is declared as a **dev dependency** in `backend/pyproject.toml`, so the
  intent to test is there — nothing is written yet.
- No CI pipeline, no coverage config, no test fixtures.

## Proposed test strategy (backend)

Use **pytest + FastAPI `TestClient`** (or `httpx.AsyncClient` for async).
Add `httpx` and `pytest-asyncio` to dev deps when we start.

Proposed structure:

```
backend/
└── tests/
    ├── conftest.py          # app + client fixtures, test settings/env
    ├── test_health.py       # GET /api/v1/health, GET /api/v1/
    ├── test_settings.py     # settings load correctly from env
    └── modules/
        ├── test_auth.py
        ├── test_products.py
        └── ...              # one file per module as it's built
```

## First tests to write (fast wins, no DB needed)

- [ ] `GET /api/v1/health` returns `200` + `status: healthy` + correct version/debug
- [ ] `GET /api/v1/` returns welcome message with the configured app name
- [ ] Global exception handler returns `500` + `{"success": false, ...}` for an
      unhandled error (can add a temporary throwaway route in a test app)
- [ ] Settings raise clearly when required env vars are missing

## Testing rule for this project

> **Every new module/endpoint ships with at least one test.**
> A feature isn't "Done" on the [STATUS.md](STATUS.md) board until it has a passing test.

This matters more than usual here because **two people + their AIs** are pushing to the
same repo — tests are how each side trusts the other's work didn't break something.

## Later (when DB + auth land)

- Test DB via a separate test database or SQLite in-memory + transaction rollback per test.
- Auth: token issue/verify, protected-route rejection without token.
- Integration tests for marketplace adapters (mock external HTTP).
- Add CI (GitHub Actions) to run `pytest` on every PR — blocks merge on failure.
