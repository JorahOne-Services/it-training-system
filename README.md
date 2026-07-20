# 🔧 LearnForge
### Self-hosted IT training management platform — learning paths, quizzes, progress tracking, and video ingestion via a FastAPI backend.

LearnForge is a backend service for delivering structured IT training to a team. It persists trainees, videos, auto-generated quizzes, learning paths, and progress events in SQLite, and exposes a REST API (with interactive OpenAPI docs) that a Telegram bot and the Hermes agent skills consume. LLM quiz generation, semantic search, and media storage are wired for Ollama, Qdrant, and MinIO but degrade gracefully — the API runs standalone with just SQLite.

![Main screenshot](docs/screenshots/main-dashboard.png)

## ✨ Features

- **REST API (FastAPI)** — users, videos, quizzes, learning paths, attempts, events, team overview. Interactive docs at `/docs`.
- **Learning Paths** — compose ordered video/quiz/lesson/assignment items and track completion progress.
- **Quizzes & Attempts** — store AI-generated quizzes (questions + options), record scored attempts, compute trainee averages.
- **Progress Tracking** — per-user quiz averages, per-path completion, and manager team overviews.
- **Video Ingestion** — upload endpoint validates and stores training media to a local `/uploads` volume (MinIO-compatible swap-in available).
- **Telegram Bot Webhook** — `/start`, `/help`, `/my_training`, `/next_lesson`, `/quiz`, `/ask`, `/team_progress` (admin-gated) commands.
- **Local-first AI hooks** — optional Ollama (quiz synthesis) and Qdrant (semantic search) integration points for self-hosted inference.
- **Observability-friendly** — `/health` endpoint, security headers (CSP, X-Frame-Options, etc.), and a non-root container.

## 🚀 Quick Start

### Docker (recommended)

```bash
git clone https://github.com/OneByJorah/LearnForge.git
cd LearnForge
cp .env.example .env          # edit secrets: SECRET_KEY, MINIO_ROOT_PASSWORD, TELEGRAM_BOT_TOKEN
docker compose up -d training-api   # API only (SQLite, no external services needed)
# or the full stack:
docker compose up -d
```

API available at **http://localhost:8080** — interactive docs at **http://localhost:8080/docs**.

> The full `docker compose up -d` also starts `ollama`, `qdrant`, and `minio` (with health-gated startup). These are optional for the core API.

Without the Compose plugin, run the API image directly:

```bash
docker build -t learnforge-api -f api/Dockerfile ./api
docker run -p 8080:8080 \
  -e DATABASE_URL=sqlite:///./app.db \
  -e SECRET_KEY=change_me_generate_random_secret \
  learnforge-api
```

### Manual / from source

```bash
git clone https://github.com/OneByJorah/LearnForge.git
cd LearnForge
python3 -m venv .venv && source .venv/bin/activate
pip install -r api/requirements.txt
cd api
DATABASE_URL=sqlite:///./app.db uvicorn app:app --host 0.0.0.0 --port 8080
```

Smoke test:

```bash
pytest api/tests/test_smoke.py -q
```

## 📸 Screenshots

- **[Swagger UI](docs/screenshots/main-dashboard.png)** — interactive API docs at `/docs`.
- **[Operations console](docs/screenshots/feature-users.png)** — trainees, learning paths, and path progress.
- **[API response](docs/screenshots/feature-quizzes.png)** — raw JSON from `GET /quizzes`.

## 🏗️ Architecture / How It Works

```
LearnForge/
├── api/                 # FastAPI backend (app.py, models.py, routes/, bots/)
├── db/schema.sql        # SQLite schema (10 tables)
├── docs/screenshots/    # Real screenshots
├── ops/                 # Roadmap + Hermes agent wiring
├── skills/              # Hermes agent skill definitions (6)
├── scripts/             # bootstrap.sh, test_api.sh
├── docker-compose.yml   # training-api + ollama + qdrant + minio
└── Dockerfile           # multi-stage build for the API
```

The API boots, creates tables via SQLAlchemy (`Base.metadata.create_all`), and serves REST routes under `/training/*`. SQLite is the default store (`DATABASE_URL`); the schema is SQLite-compatible. Ollama/Qdrant/MinIO are referenced through environment config and are only required for LLM quiz generation, semantic search, and S3-style media storage respectively. A Telegram webhook (`/telegram/webhook`) bridges chat commands to the API.

## ⚙️ Configuration

Copy `.env.example` to `.env`. Variables:

| Variable | Purpose | Default |
|----------|---------|---------|
| `DATABASE_URL` | SQLAlchemy DB URL | `sqlite:///./app.db` |
| `SECRET_KEY` | App secret (required in compose) | — |
| `TELEGRAM_BOT_TOKEN` | Telegram bot token (optional) | — |
| `TELEGRAM_ADMIN_CHAT_ID` | Admin chat for `/team_progress` | — |
| `MINIO_ROOT_USER` | MinIO console user | `admin` |
| `MINIO_ROOT_PASSWORD` | MinIO console password | — |
| `OLLAMA_ORIGINS` | Ollama CORS origins | `*` |
| `LOG_LEVEL` | Logging verbosity | `INFO` |

## 🧪 Testing

```bash
source .venv/bin/activate
pip install -r api/requirements.txt pytest httpx
pytest api/tests/test_smoke.py -q
```

The smoke suite uses FastAPI `TestClient` and exercises `/health`, user create/list, quizzes, and learning-path progress without external services. A shell smoke test (`scripts/test_api.sh`) and API bootstrap (`scripts/bootstrap.sh`) are also provided.

## 🗺️ Roadmap

- PostgreSQL upgrade path for multi-host deployments.
- Ollama-backed automatic quiz generation from video transcripts.
- Qdrant semantic search over training content.
- Hermes agent orchestration of the 6 training skills.

## 🤝 Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) and [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md). Report security issues per [SECURITY.md](SECURITY.md).

## 📄 License

MIT — see [LICENSE](LICENSE)

## 👤 Author

Built by **Jhonattan L. Jimenez** ([@OneByJorah](https://github.com/OneByJorah)) under **JorahOne LLC**. More projects: [github.com/OneByJorah](https://github.com/OneByJorah)
