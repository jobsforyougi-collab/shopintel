# 03 — Frontend

## Current state

**Nothing exists yet.** There is no frontend code in the repo.

The only evidence of frontend *intent* is in `.gitignore`, which ignores:

```
# Node
node_modules/
.next/

# Flutter
.dart_tool/
build/
```

This strongly implies the plan is:
- **Web app → Next.js** (`.next/` is Next.js's build dir), and
- **Mobile app → Flutter** (`.dart_tool/`).

> ⚠ This is inferred, **not confirmed**. Do not scaffold a frontend until the team
> confirms the framework(s) — see [OPEN-QUESTIONS.md](OPEN-QUESTIONS.md) Q3.

## Proposed structure (once confirmed)

If Next.js web is confirmed, a natural layout that keeps the monorepo clean:

```
shopintel/
├── backend/      # existing FastAPI
├── web/          # Next.js app  (proposed)
└── mobile/       # Flutter app  (proposed, later phase)
```

## What the frontend will need from the backend

To build any real screen, the web app needs these backend contracts to exist first:
1. **Auth** — login/register + token handling (blocks every authed screen).
2. **Products / search** — to render catalog + tracked items.
3. **Tracking + price history** — for price charts.
4. **Alerts** — create/list/delete alert rules.

So frontend work is **partly blocked on backend**. Good early frontend tasks that are
NOT blocked:
- Project scaffold (Next.js + TypeScript + chosen UI/styling).
- Design system / component library setup.
- API client layer + typed models (can be built against the OpenAPI schema at
  `/openapi.json` as endpoints land).
- Static pages: landing, auth screens (UI only), layout/nav shell.

## Suggested first frontend milestones

- [ ] Confirm framework + styling choice with team
- [ ] Scaffold `web/` (Next.js + TS)
- [ ] Shared API client generated/typed from backend OpenAPI
- [ ] Auth screens (UI) wired to `/api/v1/auth/*` once it exists
- [ ] Dashboard shell (tracked products list — placeholder data first)
