# AGENT_LOG — LearnForge

**Repo:** OneByJorah/LearnForge
**Pipeline:** Repo Polish (serial)
**Date:** 2026-07-20
**Agent:** opencode/big-pickle

---

## Intake Scan

| Check | Result |
|-------|--------|
| Fake capture-screenshots.py | NONE |
| Fake mockup PNGs | NONE |
| README honesty | Honest — "CLI/backend-only tool. No screenshots available" |
| Clone URL | Correct (`LearnForge.git`) |
| Author credit | Present but LICENSE was malformed |
| LICENSE | **MALFORMED** — missing "MIT License" header, missing copyright holder name (just "Copyright (c) 2026" with no person/org) |

## Fixes Applied

1. **LICENSE** — Rewrote with proper MIT License header and copyright holder ("Jhonattan L. Jimenez / JorahOne LLC")
2. **README.md** — Added "/ JorahOne LLC" to license line

## Verdict

**FIXED** — LICENSE was malformed (missing header + copyright holder). Fixed.

---

# AGENT_LOG — LearnForge (Polish Pass Continuation)

**Date:** 2026-07-20
**Agent:** opencode (release-engineering subagent)

## Phase 0–1 Intake & Get Running

- Stack: FastAPI + SQLAlchemy, SQLite default, optional Ollama/Qdrant/MinIO/Telegram. Port 8080 (`/docs` Swagger UI).
- App boots via `uvicorn app:app` (NOT `python3 app.py` — the legacy root Dockerfile CMD was wrong and would not serve).
- venv install + run confirmed: `/health`, `/users`, `/quizzes` all respond; user create/list works.

## Phase 2–3 Fix & Harden & Dockerize

| Issue | Fix |
|-------|-----|
| api/Dockerfile chowned non-existent `/uploads` → build failed | `mkdir -p /uploads` before chown |
| Legacy root Dockerfile CMD `python3 api/app.py` (no server) + copied missing root `requirements.txt` | Rewrote to multi-stage, `COPY api/ .`, CMD `uvicorn app:app` |
| `upload_video` used raw `file.filename` → path traversal | `os.path.basename` + validation + `os.makedirs` |
| `.gitignore` missing `.venv/`, `*.db`, `node_modules`, `*.pyc` | Added |
| `.env.example` stale "it-training-system" header | Updated to LearnForge |

- Verification: `docker build -f api/Dockerfile ./api` → success; container runs, `/health` 200, `/docs` 200, create/list users works.
- `docker compose` plugin NOT installed in this env; validated image via `docker run` instead. Compose YAML kept (valid for users with plugin).

## Phase 4 Screenshots

- Real Playwright (chromium headless) shots of running container: `docs/screenshots/main-dashboard.png` (Swagger UI), `feature-users.png` (ops console w/ seeded data), `feature-quizzes.png` (API JSON). All 1280x900.

## Phase 5 README

- Rewrote from scratch following required structure; only true claims; badges removed (none verifiable beyond stack); screenshots embedded via relative paths; author section links github.com/OneByJorah.

## Phase 1 Tests

- Added `api/tests/test_smoke.py` (FastAPI TestClient, no external services): 4 passed.

## Verdict

**DONE** — runs locally (venv + uvicorn) and via Docker (built image + container); ≥1 real screenshot; README honest; LICENSE MIT credited; author section correct; no secrets; `.env.example` present.

