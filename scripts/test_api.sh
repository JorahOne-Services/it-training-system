#!/usr/bin/env bash
set -euo pipefail

API="http://localhost:8080"

echo "== health =="
curl -s "$API/health" | jq .

echo "== create user =="
USER=$(curl -s -X POST "$API/users?name=Jane+Doe&telegram_id=999&role=engineer")
echo "$USER" | jq .

USER_ID=$(echo "$USER" | jq -r '.id')

echo "== upload placeholder video (local test only) =="
if [ ! -f /tmp/it-sample.mp4 ]; then
  echo "Place a training video at /tmp/it-sample.mp4 to test upload."
else
  VIDEO=$(curl -s -X POST "$API/videos/upload?title=Sample+Training&uploaded_by=$USER_ID" \
    -F "file=@/tmp/it-sample.mp4")
  echo "$VIDEO" | jq .
fi
