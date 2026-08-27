# ShopIntel — Collaboration & Analysis Docs

This folder is the shared "source of truth" for the two developers working on ShopIntel.
Anything we discover, plan, or finish gets written here so **both sides (and their AI assistants) stay in sync**.

## Index

| File | What it is |
|------|-----------|
| [01-FINDINGS.md](01-FINDINGS.md) | Full analysis of the current repo — what exists, what's missing, risks/issues |
| [02-BACKEND.md](02-BACKEND.md) | Backend deep-dive: layer-by-layer status + Done/Missing checklist |
| [03-FRONTEND.md](03-FRONTEND.md) | Frontend state (none yet) + proposed structure |
| [04-TESTING.md](04-TESTING.md) | Testing state (none yet) + proposed test strategy |
| [05-PLAN.md](05-PLAN.md) | Task breakdown, agent/owner assignment, collaboration protocol |
| [DECISIONS.md](DECISIONS.md) | **Agreed decisions** — ownership split, DB, API conventions, tooling |
| [STATUS.md](STATUS.md) | **Live task board** — update this whenever a task starts/finishes |
| [OPEN-QUESTIONS.md](OPEN-QUESTIONS.md) | Questions we need the other team to answer before deep work |

## How we collaborate (short version)

1. **One task = one branch = one PR.** Never push straight to `main`.
2. Before starting a task, move it to **In Progress** in [STATUS.md](STATUS.md) with your name.
3. When done, move it to **Done** and link the PR.
4. Commit style follows what's already in the repo: `feat(scope): ...`, `fix(scope): ...`, `chore: ...`.
5. If something is unclear, add it to [OPEN-QUESTIONS.md](OPEN-QUESTIONS.md) instead of guessing.

> Generated during initial repo review. Update freely — this is a living document.
