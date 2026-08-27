# 05 — Plan, Agents & Collaboration Protocol

This is how the two developers (and their AI assistants) divide and track work.

---

## A. Proposed division of labour

Two devs. Qasim's side ("Muhammad Ali" in git history) built the backend foundation and
is actively on backend. The cleanest, low-collision split:

| Track | Owner (proposed) | Scope |
|-------|------------------|-------|
| **Track 1 — Backend core** | Qasim's side (already here) | Database layer, auth, core domain modules |
| **Track 2 — Frontend + selected modules** | Us (new dev) | Frontend scaffold + API client; plus 1–2 backend modules we own end-to-end (e.g. `notifications`, `alerts`) |
| **Shared** | Both | `docs/`, conventions, CI, review each other's PRs |

> ⚠ This split is a **proposal**. It must be confirmed with the team before deep work —
> otherwise both sides may scaffold the DB/auth differently. See
> [OPEN-QUESTIONS.md](OPEN-QUESTIONS.md).

**Golden rule to avoid collisions:** the **database layer and auth** are foundational and
touched by everything. Exactly **one** side should own building them first; the other
builds on top. Do not both start the DB.

---

## B. Work broken into tasks

Each task below becomes a row on [STATUS.md](STATUS.md) when we start.

### Backend
- [ ] BE-01 Choose DB + ORM; add deps; DB engine/session setup
- [ ] BE-02 Alembic migrations setup
- [ ] BE-03 Base models + standard success/response envelope
- [ ] BE-04 `auth`: register/login, JWT issue/verify, password hashing, `get_current_user`
- [ ] BE-05 `users`: model + profile endpoints
- [ ] BE-06 `marketplaces`: registry + adapter interface
- [ ] BE-07 `products`: model + ingest/lookup
- [ ] BE-08 `tracking`: price-point model + price fetch job
- [ ] BE-09 `alerts`: alert rules + evaluation
- [ ] BE-10 `notifications`: email/push/WhatsApp delivery
- [ ] BE-11 `analytics`: price history stats + deal/seller scoring
- [ ] BE-12 `recommendations`: recommendation engine + AI integration
- [ ] BE-13 Background scheduler/queue for periodic price fetches

### Frontend
- [ ] FE-01 Confirm framework (Next.js?) + styling
- [ ] FE-02 Scaffold `web/`
- [ ] FE-03 Typed API client from OpenAPI
- [ ] FE-04 Auth screens (UI)
- [ ] FE-05 Dashboard shell + tracked-products list

### Testing / Infra
- [ ] QA-01 Test scaffold (`tests/`, fixtures, `TestClient`)
- [ ] QA-02 Tests for health/root/settings
- [ ] QA-03 Per-module tests (with each feature)
- [ ] INF-01 Fix `.gitignore` + un-track `logs/` (finding F1)
- [ ] INF-02 Commit `.env.development.example` (finding F2/F3)
- [ ] INF-03 Linter/formatter (ruff) + config
- [ ] INF-04 GitHub Actions CI running pytest on PRs
- [ ] INF-05 Fill `docker-compose.yml` (backend + DB)

---

## C. Agents (who does what, on our side)

We have specialized AI agents available. Map tasks → agents so each piece of work has a
clear driver. **Note:** agents only start *after* we have (a) push access sorted and
(b) the task split confirmed with the team — see chat.

| Agent | Responsible for |
|-------|-----------------|
| `database-engineer` | BE-01, BE-02, BE-03 (schema, migrations, models) — **before** any query code |
| `backend-architect` | BE-04…BE-13 API/business logic (uses schema from database-engineer) |
| `security-auditor` | Reviews every auth / token / user-data change (read-only, reports issues) |
| `notifications-engineer` | BE-10 notifications (email/SMS/WhatsApp), bilingual messages |
| `ui-ux-designer` | FE-01, FE-04, FE-05 screen specs **before** any UI is coded |
| `mobile-frontend` / web frontend | FE-02…FE-05 implementation from the design spec |
| `qa-tester` | QA-01…QA-03; a feature isn't "Done" until it has a passing test |

**Workflow per feature:** design/schema agent → implementer agent → qa-tester → security
review (if auth/data) → PR → move to Done on STATUS.md.

---

## D. Collaboration protocol (both sides follow)

1. **Branch per task:** `feat/be-04-auth`, `feat/fe-02-scaffold`, etc. Never push to `main`.
2. **Claim before you start:** move the task to *In Progress* in [STATUS.md](STATUS.md) with
   your name + branch. This is how the other AI knows it's taken.
3. **Small PRs**, reviewed by the other side before merge.
4. **Commit style:** `feat(scope): ...`, `fix(scope): ...`, `chore: ...` (matches existing history).
5. **When done:** move task to *Done* in STATUS.md + link the PR. This is the signal the
   other side's AI reads to know the work is complete.
6. **Don't guess shared decisions** (DB, auth shape, response envelope, frontend framework).
   Put them in [OPEN-QUESTIONS.md](OPEN-QUESTIONS.md) and resolve together first.
7. **Keep `docs/` current** — it's the shared memory between the two AIs.

---

## E. Immediate next steps (before feature work)

1. ✅ Repo analysed, docs written (this folder).
2. ⏳ Resolve GitHub collaborator invite so we can **push** (see chat / OPEN-QUESTIONS Q1).
3. ⏳ Get `.env.development` values so the app boots locally (OPEN-QUESTIONS Q2).
4. ⏳ Confirm DB/auth ownership + frontend framework + task split (OPEN-QUESTIONS Q3–Q5).
5. ▶ Then: spin up agents per Section C and start Track 2.
