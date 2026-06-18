name: training-ingestion
description: Watch upload storage, transcribe videos with Whisper, summarize, tag skills, and index into Qdrant.
---

## Steps
1. Watch `/uploads` or MinIO bucket for new files.
2. Run Whisper to produce transcript.
3. Use Ollama to summarize into timestamped chapters.
4. Auto-tag skill associations.
5. Insert into Postgres + index transcript into Qdrant.
6. Notify via `/training/telegram/webhook`.

## Verification
- Appear in `/videos`
- Skills attached in `/skills`
- Chunks searchable via Qdrant API
