# 01 — Findings (Current State of the Repo)

_Reviewed at commit `11e5a9b` "Complete Sprint 1 backend foundation" (branch `main`)._

## 1. What the project is

**ShopIntel** — "AI-powered Shopping Intelligence Platform" (per `README.md`).

Planned features (from README):
- Price Tracking
- Deal Intelligence
- Seller Intelligence
- Price Alerts
- Multi-Marketplace Support
- AI Recommendations

Status per README: 🚧 **Under Development**.

## 2. Tech stack (confirmed from files)

| Area | Choice | Evidence |
|------|--------|----------|
| Language | Python 3.11 | `backend/.python-version`, `pyproject.toml` `requires-python>=3.11` |
| Web framework | FastAPI (`>=0.141`) | `pyproject.toml`, `app/main.py` |
| Server | uvicorn (`>=0.52`) | `pyproject.toml` |
| Config | pydantic-settings (`>=2.14`) | `pyproject.toml`, `app/config/settings.py` |
| Package manager | **uv** (lockfile present) | `backend/uv.lock` |
| Testing | pytest (`>=8.4`) — dev dep only | `pyproject.toml` |
| Frontend | **None yet** | — (`.gitignore` hints Node/Next.js + Flutter) |
| Database | **Not wired yet** | `database_url` in settings, but no ORM/driver in deps |

## 3. Repo structure (actual)

```
shopintel/
├── README.md               # project intro
├── .gitignore              # Python + Node + Flutter + env ignores
├── .editorconfig           # EMPTY (0 bytes)
├── .env.example            # EMPTY (0 bytes)
├── LICENSE                 # EMPTY (0 bytes)
├── Makefile                # EMPTY (0 bytes)
├── docker-compose.yml      # EMPTY (0 bytes)
└── backend/
    ├── .env.example        # keys only, no values
    ├── .python-version     # 3.11
    ├── pyproject.toml
    ├── uv.lock
    ├── README.md           # EMPTY
    ├── logs/shopintel.log  # ⚠ runtime log committed to git (see risks)
    └── app/
        ├── main.py                 # create_app(), registers routes/cors/exc/mw
        ├── api/
        │   ├── router.py           # mounts v1 under /api/v1
        │   └── v1/
        │       ├── router.py       # mounts root + health
        │       ├── root.py         # GET / -> welcome
        │       └── health.py       # GET /health -> status/version/debug
        ├── config/settings.py      # pydantic Settings (reads .env.development)
        ├── core/
        │   ├── cors.py             # CORS from settings
        │   ├── exceptions.py       # global 500 handler
        │   ├── logging.py          # rotating file + console logging
        │   └── middleware.py       # request timing logger
        ├── modules/                # 9 EMPTY domain modules (see below)
        └── shared/                 # EMPTY
```

**Empty domain modules** (only `__init__.py`, no code):
`auth`, `users`, `products`, `tracking`, `alerts`, `analytics`,
`marketplaces`, `notifications`, `recommendations`.

These map 1:1 to the planned features → this is where all the real work is.

## 4. What actually works today

- App boots via `app.main:app`.
- `GET /api/v1/` → `{"message": "Welcome to <app_name>"}`
- `GET /api/v1/health` → `{"status":"healthy","version":..,"debug":..}`
- Global exception handler returns clean `500 {"success":false,"message":"Internal Server Error"}`.
- CORS, request-timing middleware, and rotating file logging are wired.
- Interactive docs at `/docs`, `/redoc`, `/openapi.json`.

The runtime log confirms it was run and `/api/v1/health` returned `200`.

## 5. ⚠ Findings / issues / risks

| # | Severity | Finding | Suggested fix |
|---|----------|---------|---------------|
| F1 | Medium | `backend/logs/shopintel.log` (a runtime log with stack traces + local paths like `D:\shopintel`) is **committed to git**. | Add `logs/` to `.gitignore`, then `git rm --cached backend/logs/shopintel.log`. |
| F2 | High (onboarding blocker) | `settings.py` has **no defaults** for `app_name, app_version, debug, database_url, secret_key, algorithm, access_token_expire_minutes`, and reads from `.env.development` — which is **gitignored and not provided**. A new dev **cannot boot the app**. | Get a documented `.env.development` template (with safe example values) from the team; commit it as `.env.development.example`. |
| F3 | Medium | Env filename mismatch: examples are named `.env.example`, but code loads `.env.development`. Root `.env.example` is empty; backend one has blank values. | Standardize the env filename + fill example values. |
| F4 | Low | Placeholder files are empty: `docker-compose.yml`, `Makefile`, `LICENSE`, `.editorconfig`, root `.env.example`. | Fill or remove; decide license. |
| F5 | Low | No linter/formatter/CI config (e.g. ruff/black, pre-commit, GitHub Actions). | Agree on tooling early to avoid style churn between two devs. |
| F6 | Info | No database layer, no auth logic, no tests despite settings/deps hinting at them. | Tracked as work items in [05-PLAN.md](05-PLAN.md). |

## 6. Access note (for the human, not the code)

- The repo is **readable/clonable anonymously** (we cloned it without login).
- The GitHub **invitation error** is only about *write/collaborator* access (needed to `git push`).
  See the chat message / [OPEN-QUESTIONS.md](OPEN-QUESTIONS.md) for how to resolve it.
