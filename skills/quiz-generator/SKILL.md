name: quiz-generator
description: Generate quizzes from video transcripts and store them in the training database.
---

## Steps
1. Fetch latest transcript from `/videos`.
2. Ask LLM to create 10–20 multiple-choice questions.
3. Persist as `/quizzes`.
4. Optionally attach to learning path item.
