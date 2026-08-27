# DECISIONS — Agreed between the two developers

Confirmed with Qasim's side on 2026-08-26. This is the authoritative record of shared
decisions; agents and both devs build against this.

## Coordination
- `docs/STATUS.md` is the **single source of truth**. No GitHub Projects for now.
- Rules: claim task → *In Progress* (name + branch) and **push that first** → one task = one
  branch = one PR → other dev reviews → after merge mark *Done* + attach PR.
- **Rule 7:** if a task expands substantially, update STATUS before taking on more work.
- The branch/status reservation is the anti-duplication mechanism (both sides use AI).

## Ownership split (confirmed)

| Owner | Area |
|-------|------|
| **Qasim** | DB foundation, SQLAlchemy models, PostgreSQL schema, Alembic, DB session/config, repositories/data-access, core backend architecture, **auth/authorization**, catalog + pricing backend, backend API contracts |
| **Huzaifah (me)** | Next.js web frontend, notifications, price-drop alerts, alert UX + API integration, frontend↔backend integration, `.env.development.example` |
| Flutter mobile | **Later** — not a current priority |
| Cross-cutting architecture changes | Discuss first (shared) |

**Hard rule:** if a task needs changing something the other person owns (e.g. an
alert-related DB table/field), **do not implement it silently on your branch** — raise it in
the task/PR and coordinate first. Alert schema in particular must be coordinated with Qasim.

## Tech decisions (confirmed)
- **Database:** PostgreSQL + **SQLAlchemy** + **Alembic**. NOT SQLModel / Tortoise.
  Build against the existing SQLAlchemy architecture — do not introduce a second data-access
  pattern.
- **DB URL driver:** `postgresql+psycopg://...`
- **Auth:** JWT, `ALGORITHM=HS256` (owned by Qasim).
- **API responses:** **No global success envelope.** Resource endpoints return their schema
  directly (`{"id": ..., "name": ...}`). The existing **error** convention stays:
  `{"success": false, "message": ...}`. Don't wrap successful responses.
- **Frontend:** Next.js (web). Flutter later. **Styling: not yet agreed** — must agree before
  adding a large UI dependency stack (proposal: Tailwind CSS — pending Qasim's OK).
- **Linting/formatting:** Python → **Ruff** (don't add Black+isort separately). TS/Next.js →
  project's ESLint/Prettier.

## ⚠ Baseline reality — IMPORTANT open item
Qasim's assistant describes substantial existing work (catalog/pricing models — brands,
categories, marketplaces, products, sellers, current prices — plus pricing service/repository
and Alembic migrations) and asks us to treat it as the baseline.

**As of 2026-08-26 this work is NOT in the repository.** The remote has only:
- `main` @ `11e5a9b` — the Sprint-1 skeleton (empty `app/modules/*`, no models, no Alembic,
  no SQLAlchemy), and
- `docs/initial-analysis` — our docs.

We **cannot build against models we can't see.** Before any alerts/notifications backend work
that touches the schema, Qasim must **push the existing pricing/catalog work** (or point us to
the branch/PR). Until then, the actual baseline = the Sprint-1 skeleton. Tracked in
[OPEN-QUESTIONS.md](OPEN-QUESTIONS.md) Q7.
