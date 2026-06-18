# Hermes wiring guide

## skill paths
- skills/training-ingestion
- skills/quiz-generator
- skills/learning-path-engine
- skills/progress-tracker
- skills/content-creator
- skills/telegram-training-bot

## composer path
Primary entrypoint used by Hermes runner: `api/app.py` (FastAPI app at `app:app`).

## required runtime
- Python 3.11+
- Docker 24+ and docker compose plugin
- Outbound internet for Telegram webhook and Ollama pulls
- At least 2 CPU cores and 4 GB RAM recommended

## Telegram prerequisites
1. Bot token via BotFather
2. Admin chat ID
3. Webhook registered to `/training/telegram/webhook`
