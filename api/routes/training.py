import logging
import os
from typing import Literal

from fastapi import APIRouter, Depends, File, HTTPException, Query, UploadFile
from pydantic import BaseModel
from sqlalchemy.orm import Session

from models import (
    LearningPath,
    LearningPathItem,
    Question,
    Quiz,
    QuizAttempt,
    User,
    UserEvent,
    Video,
    get_db,
)

logger = logging.getLogger("training.routes")
router = APIRouter()


class NotifyRequest(BaseModel):
    user_id: int
    message: str
    event_type: str = "training"


@router.get("/health")
def training_health():
    return {"module": "training", "status": "ok"}


@router.get("/users")
def list_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return [{"id": u.id, "name": u.name, "role": u.role} for u in users]


@router.post("/users")
def create_user(name: str, telegram_id: str | None = None, role: str | None = None, manager_id: int | None = None, db: Session = Depends(get_db)):
    user = User(name=name, telegram_id=telegram_id, role=role, manager_id=manager_id)
    db.add(user)
    db.commit()
    db.refresh(user)
    return {"id": user.id, "name": user.name}


@router.get("/users/manager/{manager_id}")
def users_by_manager(manager_id: int, db: Session = Depends(get_db)):
    rows = db.query(User).filter(User.manager_id == manager_id).all()
    return [{"id": r.id, "name": r.name, "role": r.role} for r in rows]


@router.get("/videos")
def list_videos(db: Session = Depends(get_db)):
    videos = db.query(Video).order_by(Video.id.desc()).all()
    return [
        {
            "id": v.id,
            "title": v.title,
            "file_path": v.file_path,
            "duration": v.duration,
            "uploaded_by": v.uploaded_by,
            "created_at": v.created_at,
        }
        for v in videos
    ]


@router.get("/videos/{video_id}")
def get_video(video_id: int, db: Session = Depends(get_db)):
    v = db.query(Video).filter(Video.id == video_id).first()
    if not v:
        raise HTTPException(status_code=404, detail="video not found")
    return {
        "id": v.id,
        "title": v.title,
        "file_path": v.file_path,
        "summary": v.summary,
        "raw_transcript": v.raw_transcript,
        "duration": v.duration,
    }


@router.post("/videos/upload")
async def upload_video(title: str, uploaded_by: int, file: UploadFile = File(...), db: Session = Depends(get_db)):
    if not file.filename.lower().endswith((".mp4", ".mov", ".avi", ".mkv", ".webm")):
        raise HTTPException(status_code=400, detail="unsupported video format")

    safe_name = os.path.basename(file.filename)
    if not safe_name or "/" in safe_name or "\\" in safe_name:
        raise HTTPException(status_code=400, detail="invalid filename")

    upload_dir = "/uploads"
    os.makedirs(upload_dir, exist_ok=True)
    path = os.path.join(upload_dir, safe_name)
    with open(path, "wb") as f:
        f.write(await file.read())

    video = Video(title=title, file_path=path, uploaded_by=uploaded_by)
    db.add(video)
    db.commit()
    db.refresh(video)
    return {"video_id": video.id, "title": video.title, "file_path": video.file_path}


@router.get("/quizzes")
def list_quizzes(db: Session = Depends(get_db)):
    quizzes = db.query(Quiz).order_by(Quiz.id.desc()).all()
    return [{"id": q.id, "title": q.title, "video_id": q.video_id} for q in quizzes]


@router.get("/quizzes/{quiz_id}")
def get_quiz(quiz_id: int, db: Session = Depends(get_db)):
    q = db.query(Quiz).filter(Quiz.id == quiz_id).first()
    if not q:
        raise HTTPException(status_code=404, detail="quiz not found")
    return {"id": q.id, "title": q.title, "questions_json": q.questions_json}


@router.get("/quizzes/{quiz_id}/questions")
def list_questions(quiz_id: int, db: Session = Depends(get_db)):
    questions = db.query(Question).filter(Question.quiz_id == quiz_id).all()
    return [{"id": q.id, "text": q.text, "options_json": q.options_json, "correct_index": q.correct_index} for q in questions]


@router.post("/learning-paths")
def create_learning_path(user_id: int, title: str, description: str | None = None, db: Session = Depends(get_db)):
    path = LearningPath(user_id=user_id, title=title, description=description, status="active")
    db.add(path)
    db.commit()
    db.refresh(path)
    return {"path_id": path.id, "status": path.status}


@router.get("/learning-paths/user/{user_id}")
def paths_for_user(user_id: int, db: Session = Depends(get_db)):
    paths = db.query(LearningPath).filter(LearningPath.user_id == user_id).all()
    return [{"id": p.id, "title": p.title, "status": p.status} for p in paths]


@router.post("/learning-paths/{path_id}/items")
def add_path_item(
    path_id: int,
    item_type: Literal["video", "quiz", "lesson", "assignment"],
    item_id: int,
    order: int = 0,
    db: Session = Depends(get_db),
):
    item = LearningPathItem(path_id=path_id, item_type=item_type, item_id=item_id, item_order=order)
    db.add(item)
    db.commit()
    db.refresh(item)
    return {"item_id": item.id, "order": item.item_order}


@router.get("/learning-paths/{path_id}/progress")
def path_progress(path_id: int, db: Session = Depends(get_db)):
    items = db.query(LearningPathItem).filter(LearningPathItem.path_id == path_id).order_by(LearningPathItem.item_order).all()
    completed = sum(1 for i in items if i.completed)
    return {"total": len(items), "completed": completed, "progress": (completed / len(items) if items else 0)}


@router.get("/users/{user_id}/progress")
def user_progress(user_id: int, db: Session = Depends(get_db)):
    attempts = db.query(QuizAttempt).filter(QuizAttempt.user_id == user_id).order_by(QuizAttempt.completed_at.desc()).all()
    average = sum(a.score for a in attempts) / len(attempts) if attempts else 0
    return {"user_id": user_id, "quiz_attempts": len(attempts), "average_score": round(average, 2)}


@router.post("/attempts")
def record_attempt(user_id: int, quiz_id: int, score: float, db: Session = Depends(get_db)):
    attempt = QuizAttempt(user_id=user_id, quiz_id=quiz_id, score=score)
    db.add(attempt)
    db.commit()
    db.refresh(attempt)
    return {"attempt_id": attempt.id, "score": attempt.score}


@router.get("/team/overview")
def team_overview(manager_id: int = Query(...), db: Session = Depends(get_db)):
    users = db.query(User).filter(User.manager_id == manager_id).all()
    out = []
    for u in users:
        attempts = db.query(QuizAttempt).filter(QuizAttempt.user_id == u.id).order_by(QuizAttempt.completed_at.desc()).limit(10).all()
        out.append(
            {
                "user_id": u.id,
                "name": u.name,
                "role": u.role,
                "quiz_count": len(attempts),
                "average_score": round(sum(a.score for a in attempts) / len(attempts), 2) if attempts else 0,
                "last_attempt": attempts[0].completed_at if attempts else None,
            },
        )
    return out


@router.get("/events/user/{user_id}")
def user_events(user_id: int, db: Session = Depends(get_db)):
    events = db.query(UserEvent).filter(UserEvent.user_id == user_id).order_by(UserEvent.created_at.desc()).limit(50).all()
    return [{"id": e.id, "event_type": e.event_type, "metadata_json": e.metadata_json, "created_at": e.created_at} for e in events]


@router.post("/events")
def record_event(user_id: int, event_type: str, metadata: dict | None = None, db: Session = Depends(get_db)):
    event = UserEvent(user_id=user_id, event_type=event_type, metadata_json=str(metadata or {}))
    db.add(event)
    db.commit()
    db.refresh(event)
    return {"event_id": event.id, "event_type": event.event_type}
