import os

import httpx
from fastapi import APIRouter, Request

router = APIRouter()

TELEGRAM_TOKEN=os.environ.get("TELEGRAM_BOT_TOKEN")
TELEGRAM_ADMIN_CHAT_ID=os.environ.get("TELEGRAM_ADMIN_CHAT_ID")
BASE_URL = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}" if TELEGRAM_TOKEN else None


async def send_message(chat_id: str, text: str):
    if not BASE_URL:
        return
    async with httpx.AsyncClient(timeout=15) as client:
        await client.post(f"{BASE_URL}/sendMessage", json={"chat_id": chat_id, "text": text})


def _is_chat_admin(chat_id: str) -> bool:
    return bool(TELEGRAM_ADMIN_CHAT_ID and str(chat_id) == str(TELEGRAM_ADMIN_CHAT_ID))


@router.post("/telegram/webhook")
async def telegram_webhook(request: Request):
    try:
        data = await request.json()
    except Exception:
        return {"ok": True}

    message = (data.get("message") or {})
    text = (message.get("text") or "")
    chat_id = str(message.get("chat", {}).get("id", ""))
    command = text.split()[0].lower() if text else ""

    if command == "/start":
        await send_message(chat_id, "Training Bot ready. /help")
        return {"ok": True}

    if command == "/help":
        await send_message(chat_id, "Commands: /my_training, /next_lesson, /quiz, /ask <question>, /team_progress (admin only)")
        return {"ok": True}

    if command == "/team_progress":
        if not _is_chat_admin(chat_id):
            await send_message(chat_id, "Forbidden: admin only.")
            return {"ok": True}
        await send_message(chat_id, "Use FastAPI /training/team?manager_id=<id>")
        return {"ok": True}

    if command == "/my_training":
        await send_message(chat_id, "MyTraining view: call FastAPI /training/learning-paths/user/{user_id}")
        return {"ok": True}

    if command == "/next_lesson":
        await send_message(chat_id, "Fetching next lesson...")
        return {"ok": True}

    if command == "/quiz":
        await send_message(chat_id, "Latest quizzes: /training/quizzes")
        return {"ok": True}

    if command == "/ask":
        query = text[len("/ask"):].strip()
        if not query:
            await send_message(chat_id, "Missing query. Example: /ask What is DNS hijacking?")
        else:
            await send_message(chat_id, f"LLM bridge not connected yet for: {query}")
        return {"ok": True}

    await send_message(chat_id, "Unknown command. /help")
    return {"ok": True}


@router.post("/training/notify/user/{user_id}")
async def notify_user(user_id: int, request: Request):
    body = await request.json()
    message = body.get("message", "")
    event_type = body.get("event_type", "training")
    await send_message(str(user_id), f"[{event_type}] {message}")
    return {"ok": True}
