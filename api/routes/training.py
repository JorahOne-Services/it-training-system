from fastapi import APIRouter, Depends, HTTPException, Request, UploadFile, File, Query
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy import desc
from typing import Literal
import httpx
import os
import logging

from app import get_db
from app import User, Video, Quiz, QuizAttempt, LearningPath, LearningPathItem, UserEvent

logger = logging.getLogger("training.routes")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_ADMIN_CHAT_ID = os.getenv("TELEGRAM_ADMIN_CHAT_ID")
BASE_URL = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}" if TELEGRAM_TOKEN else None


async def send_telegram(chat_id: str, text: str):
    if not BASE_URL:
        return
    async with httpx.AsyncClient(timeout=15) as client:
        await client.post(f"{BASE_URL}/sendMessage", json={"chat_id": chat_id, "text": text})


router = APIRouter()


class NotifyBody(BaseModel):
    user_id: int
    event_type: str = "training"
    message: str


class NotifyWebhookPathRequest(BaseModel):
    message: str


# Telegram commands
@router.post("/telegram/webhook")
async def telegram_webhook(request: Request):
    try:
        data = await request.json()
    except Exception:
        raise HTTPException(status_code=400, detail="invalid json")

    message = (data.get("message") or {})
    text = message.get("text", "") or ""
    chat_id = str(message.get("chat", {}).get("id", ""))
    command = text.split()[0].lower() if text else ""

    if command == "/team_progress" and TELEGRAM_ADMIN_CHAT_ID and chat_id == TELEGRAM_ADMIN_CHAT_ID:
        await send_telegram(chat_id, "Team progress: use FastAPI /training/team for now.")
    elif command == "/my_training":
        await send_telegram(chat_id, "Fetching your assigned learning path...")
    elif command == "/next_lesson":
        await send_telegram(chat_id, "Loading next lesson.")
    elif command == "/quiz":
        await send_telegram(chat_id, "Here is your active quiz.")
    elif command == "/ask":
        query = text[len("/ask"):].strip()
        msg = f"Answer to: {query}" if query else "Usage: /ask What is VLAN trunking?"
        await send_telegram(chat_id, msg)
    else:
        await send_telegram(chat_id, "Commands: /my_training /next_lesson /quiz /ask <question>")

    return {"ok": True}


# Training endpoints
@router.get("/team")
def team_overview(manager_id: int = Query(...), db: Session = Depends(get_db)):
    users = db.query(User).filter(User.manager_id == manager_id).all()
    result = []
    for user in users:
        attempts = (
            db.query(QuizAttempt)
            .filter(QuizAttempt.user_id == user.id)
            .order_by(desc(QuizAttempt.completed_at))
            .limit(5)
            .all()
        )
        result.append(
            {
                "user_id": user.id,
                "name": user.name,
                "current_level": user.current_level,
                "recent_scores": [a.score for a in attempts],
                "latest_score": attempts[0].score if attempts else None,
            }
        )
    return result


@router.post("/enroll")
def enroll_user(user_id: int, path_title: str, description: str | None = None, db: Session = Depends(get_db)):
    path = LearningPath(user_id=user_id, title=path_title, description=description, status="active")
    db.add(path)
    db.commit()
    db.refresh(path)
    return path


@router.post("/learning-paths/{path_id}/items")
def add_path_item(
    path_id: int,
    item_type: Literal["video", "quiz", "lesson"],
    item_id: int,
    order: int = 0,
    db: Session = Depends(get_db),
):
    item = LearningPathItem(path_id=path_id, item_type=item_type, item_id=item_id, item_order=order)
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


@router.get("/learning-paths/{path_id}/progress")
def path_progress(path_id: int, db: Session = Depends(get_db)):
    items = db.query(LearningPathItem).filter(LearningPathItem.path_id == path_id).order_by(LearningPathItem.item_order).all()
    completed = sum(1 for i in items if i.completed)
    return {"total": len(items), "completed": completed}


@router.post("/events")
def record_event(user_id: int, event_type: str, metadata: dict | None = None, db: Session = Depends(get_db)):
    event = UserEvent(user_id=user_id, event_type=event_type, metadata_json=str(metadata or {}))
    db.add(event)
    db.commit()
    db.refresh(event)
    return event


@router.post("/notify")
async def notify_user(body: NotifyBody):
    await send_telegram(str(body.user_id), f"[{body.event_type}] {body.message}")
    return {"ok": True}
