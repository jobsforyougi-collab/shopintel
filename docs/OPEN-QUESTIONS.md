# OPEN QUESTIONS — for the other team (Qasim's side)

These block deep work. Please answer inline (edit this file or reply in chat), so both
AIs build on the same assumptions instead of guessing.

---

### Q1 — Collaborator access — ✅ RESOLVED
Invite accepted. New dev **`Huzaifah-Analyst`** now has push access (verified: `push: true`).
No action needed.

### Q2 — `.env.development` values (blocking local run)
`settings.py` requires `app_name, app_version, debug, database_url, secret_key,
algorithm, access_token_expire_minutes` and reads `.env.development`, which is gitignored.
The app **won't boot** without it.

**We need:** a filled `.env.development.example` (real keys, safe/placeholder values —
no production secrets) committed to the repo.

### Q3 — Ownership of foundation + task split
To avoid both sides scaffolding the DB/auth differently:
- Who owns the **database layer + auth** (BE-01…BE-04)?
- What is Qasim currently working on **right now** (so we don't collide)?
- Which modules should **we** take end-to-end? (Our proposal: frontend + `notifications`/`alerts`.)

### Q4 — Database choice
Which DB + ORM? (e.g. **PostgreSQL + SQLAlchemy + Alembic**? SQLModel? Tortoise?)
`database_url` exists but no driver/ORM is in `pyproject.toml` yet.

### Q5 — Frontend framework
`.gitignore` hints **Next.js** (web) + **Flutter** (mobile). Confirm:
- Web framework + styling (Next.js + Tailwind? something else?)
- Is mobile (Flutter) in scope now or later?

### Q6 — Conventions
- Response envelope: the error handler returns `{"success": false, "message": ...}`.
  Is there a matching **success** envelope shape we should follow?
- Linter/formatter preference (ruff? black?) so both sides format the same way.
- Any existing design doc / Sprint plan / Jira/Trello board we should read?

---

**Answers:**
- Q1: ✅ Resolved — Huzaifah-Analyst has push access.
- Q2: …
- Q3: …
- Q4: …
- Q5: …
- Q6: …
