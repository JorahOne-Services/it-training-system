name: content-creator
description: Create supplementary lessons and audio from RAG context.
---

## Steps
1. Query Qdrant for missing topic coverage.
2. Generate lesson text via LLM.
3. TTS generate audio if needed.
4. Store content for path inclusion.
