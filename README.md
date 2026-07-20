<div align="center">
  <img src="https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white">
  <img src="https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white">
  <img src="https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white">
  <img src="https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white">
</div>

<br>

<div align="center">
  <h1>🎓 LearnForge</h1>
  <p><strong>Self-Hosted IT Training Management Platform</strong></p>
  <p>Structured learning paths, automated quizzes, progress tracking, and video ingestion</p>
  <p>
    <a href="#-features">Features</a> •
    <a href="#-quick-start">Quick Start</a> •
    <a href="#-architecture">Architecture</a> •
    <a href="#-tech-stack">Tech Stack</a>
  </p>
</div>

---

## 📸 Screenshot

This is a CLI/backend-only tool. No screenshots available.

## ✨ Features

- **Learning Paths** — Structured IT training curricula
- **Automated Quizzes** — AI-generated quiz synthesis with Ollama
- **Progress Tracking** — Monitor trainee progress and completion
- **Video Ingestion** — Training media ingestion via MinIO
- **Semantic Search** — Qdrant vector search for training content
- **Telegram Bot** — Notifications and interaction
- **FastAPI Backend** — Modern, async Python backend

## 🚀 Quick Start

```bash
git clone https://github.com/OneByJorah/LearnForge.git
cd LearnForge
cp compose.env.example .env
# Edit .env with your configuration
docker-compose up -d
```

API available at **http://localhost:8080**.

## 🏗️ Architecture

```
LearnForge/
├── api/                       # FastAPI backend
├── db/                        # SQLite schema definition
├── ops/                       # Operations & deployment
├── scripts/                   # Utility scripts
├── skills/                    # Hermes agent skills
├── docs/                      # Documentation
├── docker-compose.yml         # Deployment
├── Makefile                   # Build automation
└── README.md
```

## 🛠️ Tech Stack

| Component | Technology |
|-----------|------------|
| Backend | Python, FastAPI, SQLAlchemy |
| Database | SQLite (PostgreSQL upgrade path) |
| Vector Store | Qdrant |
| Object Storage | MinIO (S3-compatible) |
| LLM | Ollama |
| Notifications | Telegram Bot |
| Agents | Hermes AgentOS |
| Deployment | Docker Compose |

## 📄 License

MIT © Jhonattan L. Jimenez / JorahOne LLC

---

<div align="center">
  <p>📚 Train your team, self-hosted</p>
  <p><a href="https://github.com/OneByJorah">@OneByJorah</a></p>
</div>
