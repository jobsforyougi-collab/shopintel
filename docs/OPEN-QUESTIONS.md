# OPEN QUESTIONS — for the other team (Qasim's side)

Most items are now resolved (see [DECISIONS.md](DECISIONS.md)). Q7 is the remaining blocker.

---

### Q1 — Collaborator access — ✅ RESOLVED
`Huzaifah-Analyst` has push access (verified `push: true`).

### Q2 — `.env.development` values — ✅ RESOLVED (being handled)
Huzaifah is adding `backend/.env.development.example` with safe placeholders, keys matched
**exactly** to `app/config/settings.py` (no invented keys).

### Q3 — Ownership + task split — ✅ RESOLVED
See [DECISIONS.md](DECISIONS.md). Qasim: DB/auth/catalog/pricing/core. Huzaifah:
frontend/notifications/alerts/env-example.

### Q4 — Database choice — ✅ RESOLVED
PostgreSQL + SQLAlchemy + Alembic. Driver `postgresql+psycopg`.

### Q5 — Frontend framework — ✅ RESOLVED (styling pending)
Next.js web; Flutter later. **Styling not yet agreed** — proposal: Tailwind CSS. Please
confirm before we add a UI dependency stack.

### Q6 — Conventions — ✅ RESOLVED
No success envelope (return schemas directly); keep the existing error convention. Ruff for
Python; ESLint/Prettier for TS.

---

### Q7 — ⚠ BLOCKER: existing pricing/catalog work is not in the repo
Qasim's assistant says catalog/pricing models + pricing service/repository + Alembic
migrations already exist and should be treated as the baseline. **But the remote has none of
it** — only `main` (Sprint-1 skeleton with empty `app/modules/*`) and our docs branch.

**We need one of:**
- Qasim **pushes** the existing SQLAlchemy models / Alembic / pricing work to a branch + opens a PR, **or**
- points us to the exact branch/commit where it lives.

Reason: alerts/notifications (Huzaifah's scope) depend on the product/price schema. We can't
build against models we can't see, and we must not re-create them (duplication risk).

**Answer:** …
