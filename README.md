# IT Training Management System

![License](https://img.shields.io/badge/License-MIT-FFB300) ![Status](https://img.shields.io/badge/Status-Active_Development-FFB300) ![Language](https://img.shields.io/badge/Language-Python-FFB300) ![Stack](https://img.shields.io/badge/Stack-Docker_Compose%2FFastAPI-FFB300) ![Platform](https://img.shields.io/badge/Platform-Docker-FFB300)

Self-hosted IT training platform with Hermes as the orchestrator and a FastAPI backend.

---

## Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Technology Stack](#technology-stack)
- [Features](#features)
- [Getting Started](#getting-started)
- [Environment Variables](#environment-variables)
- [Service Management](#service-management)
- [Project Structure](#project-structure)
- [Screenshots](#screenshots)
- [Contributing](#contributing)
- [License](#license)
- [Author](#author)

---

## Overview

The IT Training Management System combines a FastAPI backend with supporting services (Ollama, Qdrant, MinIO, Telegram bot) to deliver structured IT training: learning paths, quizzes, video ingestion, and progress tracking. Hermes agent skills extend the platform with content creation, ingestion, and reporting.

---

## Architecture

Client → FastAPI backend (`api/app.py`, port `8080`) → supporting services:

- **Ollama** (port `11434`) — local LLM for content generation and quiz synthesis.
- **Qdrant** (port `6333`) — vector memory for semantic content retrieval.
- **MinIO** (ports `9000`/`9001`) — object storage for uploaded training media.
- **Telegram bot** — optional notification channel via `api/bots/telegram.py`.

Hermes skills in `skills/` wire into the backend for orchestration.

---

## Technology Stack

| Layer | Stack |
|---|---|
| Runtime | Docker Compose (Ollama, Qdrant, MinIO, FastAPI) |
| Backend | Python / FastAPI / Uvicorn |
| Storage | MinIO (S3-compatible) |
| Vector DB | Qdrant |
| LLM | Ollama |
| Database | SQLAlchemy + SQLite / Postgres (via `DATABASE_URL`) |
| Orchestration | Hermes Agent skills |
| VCS | Git + GitHub (`github.com/OneByJorah/it-training-system`) |

---

## Features

- **Learning paths**: structured courses with ordered items.
- **Quiz engine**: question generation and scoring.
- **Progress tracking**: per-user event and completion tracking.
- **Video ingestion**: upload and index training videos.
- **Telegram integration**: bot-driven training notifications and interactions.
- **Semantic search**: Qdrant-backed retrieval over training content.
- **Docker compose**: one-stack deploy with `docker-compose.yml`.

---

## Getting Started

```bash
# 1. Clone
git clone https://github.com/OneByJorah/it-training-system.git
cd it-training-system

# 2. Environment
cp compose.env.example .env

# 3. Start the stack
docker compose up -d

# 4. Bootstrap
./scripts/bootstrap.sh
```

---

## Environment Variables

Configured via `.env` (see `compose.env.example`):

| Variable | Purpose |
|---|---|
| `DATABASE_URL` | SQLAlchemy database connection |
| `SECRET_KEY` | FastAPI secret |
| `TELEGRAM_BOT_TOKEN` | Telegram bot token |
| `TELEGRAM_ADMIN_CHAT_ID` | Admin chat for notifications |
| MinIO | `MINIO_ROOT_USER` / `MINIO_ROOT_PASSWORD` |

Keep `.env` out of VCS.

---

## Service Management

```bash
# Start
docker compose up -d

# Logs
docker compose logs -f training-api

# Stop
docker compose down
```

---

## Project Structure

```
it-training-system/
├── api/
│   ├── app.py
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── routes/
│   │   └── training.py
│   └── bots/
│       └── telegram.py
├── db/
│   └── schema.sql
├── docker-compose.yml
├── compose.env.example
├── scripts/
│   ├── bootstrap.sh
│   └── test_api.sh
├── skills/
│   ├── content-creator/SKILL.md
│   ├── learning-path-engine/SKILL.md
│   ├── progress-tracker/SKILL.md
│   ├── quiz-generator/SKILL.md
│   ├── telegram-training-bot/SKILL.md
│   └── training-ingestion/SKILL.md
├── docs/
│   ├── setup.md, deploy.md, overview.md, reference.md, observability.md
├── ops/
│   └── roadmap.md
└── README.md
```

---

## Screenshots

_(Screenshots will be added after build/run capture.)_

---

## Contributing

1. Create a feature branch off `main`.
2. Update schema/docs when changing the data model.
3. Submit a PR with description and screenshots for UI changes.

---

## License

MIT

Copyright (c) 2026 JorahOne, LLC

---

## Author

Built by **Jhonattan L. Jimenez**.

*Built by [JorahOne, LLC](https://github.com/JorahOne-Services) — ...*
