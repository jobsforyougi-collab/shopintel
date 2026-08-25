# 02 — Backend

_FastAPI backend under `backend/app/`. This is the only part with code today._

## Architecture (as built)

The design is a clean, modular FastAPI setup:

- **Entry point** `app/main.py` → `create_app()` builds the `FastAPI` instance,
  then `register_exception_handlers`, `register_cors`, `register_middleware`.
- **Routing** is versioned:
  `main` → `api/router.py` (mounts everything at `/api/v1`)
  → `api/v1/router.py` (mounts `root` + `health`).
  Adding a new module = create its router and include it in `api/v1/router.py`.
- **Config** `config/settings.py` — pydantic `BaseSettings`, cached via `lru_cache`,
  loads from `.env.development`.
- **Core cross-cutting concerns** in `core/`: `cors.py`, `exceptions.py`,
  `logging.py` (rotating 5MB × 5), `middleware.py` (request timing).
- **Domain modules** in `modules/<feature>/` — the intended home for routers,
  services, schemas, and models per feature. All empty right now.

This is a solid foundation. The pattern to follow for each new feature is clear.

## Done ✅ vs Missing ❌

### Foundation
- ✅ App factory + startup logging
- ✅ Versioned API routing (`/api/v1`)
- ✅ Settings from env (pydantic-settings)
- ✅ CORS (configurable via env)
- ✅ Global exception handler (500)
- ✅ Rotating file + console logging
- ✅ Request-timing middleware
- ✅ Health + root endpoints
- ✅ `uv` dependency management + lockfile

### Not started
- ❌ **Database layer** — no ORM/driver (no SQLAlchemy/SQLModel/Tortoise), no models,
  no session/engine, no migrations (no Alembic). `database_url` exists but is unused.
- ❌ **Auth** — `secret_key/algorithm/access_token_expire_minutes` configured, but no
  JWT logic, no password hashing, no login/register, no dependency guards.
- ❌ **All 9 domain modules** (see per-module table below).
- ❌ **Pagination / standard response envelope** (exception handler returns
  `{"success": false, ...}` — no matching success envelope defined yet).
- ❌ **Validation schemas** (Pydantic request/response models per feature).
- ❌ **Background jobs / scheduler** (price tracking implies periodic scraping — no
  Celery/APScheduler/queue yet).
- ❌ **External marketplace integrations** (scrapers/API clients).
- ❌ **Tests** (see [04-TESTING.md](04-TESTING.md)).
- ❌ **Containerization** (`docker-compose.yml` empty).

## Per-module status

| Module | Maps to feature | Status | First things it needs |
|--------|-----------------|--------|-----------------------|
| `auth` | (foundation) | empty | JWT issue/verify, password hashing, login/register, `get_current_user` dep |
| `users` | user accounts | empty | User model, profile CRUD, wiring to auth |
| `products` | catalog | empty | Product model, ingest/lookup, marketplace linkage |
| `tracking` | Price Tracking | empty | Price-point model, tracked-item model, periodic price fetch |
| `alerts` | Price Alerts | empty | Alert rules (target price), evaluation on new price data |
| `marketplaces` | Multi-Marketplace | empty | Marketplace registry, per-marketplace fetch adapters |
| `analytics` | Deal / Seller Intelligence | empty | Price history stats, deal scoring, seller metrics |
| `recommendations` | AI Recommendations | empty | Recommendation engine + AI/model integration |
| `notifications` | (delivery) | empty | Email/push/WhatsApp delivery for alerts |

## Recommended build order (dependencies)

```
1. Database layer  ─┐
2. auth ─────────────┼─► 3. users
                     │
   marketplaces ─────┼─► products ─► tracking ─► alerts ─► notifications
                     │                    └─► analytics ─► recommendations
```

Rationale: nothing persists without the DB layer; most modules need `auth` + a
`products`/`marketplaces` base before they mean anything. **Database + auth are the
unblockers** and should be decided/built first (and coordinated with the other dev
so we don't both scaffold the DB differently).

## Conventions observed (follow these)

- Each router file exposes `router = APIRouter()` and is `include_router`-ed upward.
- Tags on endpoints (`tags=["Health"]`).
- Conventional commits: `feat(api): ...`, `feat(core): ...`, `chore: ...`.
- 4-space indent, type hints, docstrings on setup functions.
