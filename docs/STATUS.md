# STATUS — Live Task Board

> **Single source of truth. Both devs + their AIs check here to know who's doing what.**
> Claim a task (move to *In Progress* with Owner + Branch) and **push that first** before
> coding. One task = one branch = one PR. Mark *Done* + link PR after merge.
> If a task expands substantially, update STATUS before taking more work.
> Ownership split: see [DECISIONS.md](DECISIONS.md).

_Last updated: 2026-08-26._

---

## 🟢 Done

| ID | Task | Owner | PR / Commit |
|----|------|-------|-------------|
| — | Sprint 1 backend foundation (routing, config, core, health) | Qasim (Muhammad Ali) | `11e5a9b` |
| — | Repo analysis + collaboration docs + decisions | Huzaifah-Analyst | [PR #1](https://github.com/jobsforyougi-collab/shopintel/pull/1) |

## 🟡 In Progress

| ID | Task | Owner | Branch | Notes |
|----|------|-------|--------|-------|
| INF-02 | `backend/.env.development.example` (keys matched to settings.py) | Huzaifah-Analyst | docs/initial-analysis | in PR #1 |

## 🔵 To Do

### Qasim (backend core)
| ID | Task | Notes |
|----|------|-------|
| BE-01..03 | DB/ORM foundation, Alembic, models | **Push existing work** (see blocker Q7) |
| BE-04 | Auth (JWT, HS256) | |
| — | Catalog + pricing backend | Qasim says substantially done — needs pushing |

### Huzaifah (frontend + notifications + alerts)
| ID | Task | Depends on |
|----|------|-----------|
| FE-01 | Confirm styling (Tailwind?) | Qasim OK |
| FE-02 | Scaffold `web/` (Next.js + TS) | FE-01 |
| FE-03 | Typed API client from OpenAPI | backend endpoints |
| FE-04/05 | Auth screens, dashboard shell, tracked-products list | backend + design spec |
| BE-09 | Price-drop detection + alert rules | **Q7** (product/price schema) + coordinate alert tables w/ Qasim |
| BE-10 | Notifications backend (email→push→WhatsApp, bilingual) | BE-09 |
| QA-01/02 | Test scaffold + health/settings tests | — (safe to start anytime) |

### Shared / infra
| ID | Task | Notes |
|----|------|-------|
| INF-03 | Ruff config | agreed |
| INF-04 | GitHub Actions CI (pytest) | |
| INF-05 | Fill `docker-compose.yml` (backend + Postgres) | |

---

## 🔴 Blockers
- **Q7:** Existing pricing/catalog/models work is **not in the repo** — Qasim must push it or
  point to the branch before alerts/notifications backend can start. See
  [OPEN-QUESTIONS.md](OPEN-QUESTIONS.md).

### Legend
- **Done** = merged to `main` + (features) passing tests. **In Progress** = branch exists, owned now. **To Do** = agreed, not started.
