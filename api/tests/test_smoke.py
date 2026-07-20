"""Smoke tests for the LearnForge training API.

Run with: pytest api/tests/test_smoke.py
No external services (Ollama/Qdrant/MinIO) required.
"""

import os
import tempfile

os.environ.setdefault("DATABASE_URL", f"sqlite:///{tempfile.mkdtemp()}/test.db")

from fastapi.testclient import TestClient  # noqa: E402

from app import app  # noqa: E402


def test_health():
    with TestClient(app) as client:
        res = client.get("/health")
        assert res.status_code == 200
        assert res.json()["status"] == "ok"


def test_create_and_list_user():
    with TestClient(app) as client:
        created = client.post("/users", params={"name": "SmokeUser"})
        assert created.status_code == 200
        uid = created.json()["id"]

        listing = client.get("/users")
        assert listing.status_code == 200
        assert any(u["id"] == uid for u in listing.json())


def test_quizzes_empty():
    with TestClient(app) as client:
        res = client.get("/quizzes")
        assert res.status_code == 200
        assert isinstance(res.json(), list)


def test_learning_path_progress():
    with TestClient(app) as client:
        created = client.post(
            "/learning-paths", params={"user_id": 1, "title": "SmokePath"}
        )
        assert created.status_code == 200
        path_id = created.json()["path_id"]

        prog = client.get(f"/learning-paths/{path_id}/progress")
        assert prog.status_code == 200
        assert prog.json()["total"] == 0
        assert prog.json()["progress"] == 0
