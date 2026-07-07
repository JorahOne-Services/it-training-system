#!/usr/bin/env bash
set -euo pipefail

if [ ! -f .env ]; then
  cp compose.env.example .env
  echo "Created .env from compose.env.example"
fi

echo "Starting training stack..."
docker compose up -d

echo "Done."
echo "API: http://localhost:8080"
echo "MinIO: http://localhost:9001"
echo "Qdrant: http://localhost:6333/dashboard"
