# IT Training System — Production Setup

## 1. Prereqs on Ubuntu

```bash
sudo apt update
sudo apt install -y ca-certificates curl git ufw jq
sudo snap install docker
# OR sudo apt install -y docker.io docker-compose-plugin
```

## 2. Clone repo

```bash
git clone https://github.com/OneByJorah/it-training-system.git
cd it-training-system
cp compose.env.example .env
```

## 3. Fill .env values

Required placeholders:
- `MINIO_ROOT_PASSWORD`
- `SECRET_KEY`
- `TELEGRAM_BOT_TOKEN`
- `TELEGRAM_ADMIN_CHAT_ID`

Recommended:
- `DATABASE_URL=sqlite:///./app.db` for first run
- Switch to Postgres later if load increases

## 4. Open ports

```bash
sudo ufw allow 8080/tcp
sudo ufw allow 9000/tcp
sudo ufw allow 6333/tcp
sudo ufw allow 11434/tcp
```

## 5. Start

```bash
export DOCKER_HOST=unix:///var/run/docker.sock
make deploy
```

## 6. Verify

```bash
curl -s http://localhost:8080/health
make test
```

## 7. Telegram webhook

```bash
curl -F "url=https://<your-host>/training/telegram/webhook" \
  https://api.telegram.org/bot<TOKEN>/setWebhook
```
