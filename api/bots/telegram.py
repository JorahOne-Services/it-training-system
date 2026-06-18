import logging
import os
import httpx
from fastapi import APIRouter, Request

logger = logging.getLogger("training.telegram")
router = APIRouter()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_ADMIN_CHAT_ID = os.getenv("TELEGRAM_ADMIN_CHAT_ID")
BASE_URL = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}" if TELEGRAM_TOKEN else None



async def send_message(chat_id: str, text: str):
    if not BASE_URL:
        return
    async with httpx.AsyncClient(timeout=15) as client:
        await client.post(f"{BASE_URL}/sendMessage", json={"chat_id": chat_id, "text": text})


@router.post("/telegram/webhook")
async def telegram_webhook(request: Request):
    data = await request.json()
    message = data.get("message") or {}
    text = message.get("text", "")
    chat_id = str(message.get("chat", {}).get("id", ""))
    user_id = message.get("from", {}).get("id")

    command = text.split()[0].lower()

    # -------- Manager commands --------
    if command == "/team_progress" and TELEGRAM_ADMIN_CHAT_ID and chat_id == TELEGRAM_ADMIN_CHAT_ID:
        await send_message(chat_id, "Team progress view not wired yet. Use FastAPI /training/team for now.")

    # -------- Employee commands --------
    elif command == "/my_training":
        await send_message(chat_id, "Fetching your assigned learning path...")

    elif command == "/next_lesson":
        await send_message(chat_id, "Loading next lesson.")

    elif command == "/quiz":
        await send_message(chat_id, "Here is your active quiz.")

    # -------- Ask Hermes --------
    elif command == "/ask":
        query = text[len("/ask"):].strip()
        if not query:
            await send_message(chat_id, "Usage: /ask What is VLAN trunking?")
        else:
            await send_message(chat_id, f"Answer to: {query}")

    else:
        await send_message(chat_id, "Commands: /my_training /next_lesson /quiz /ask <question>")

    return {"ok": True}


@router.post("/training/notify/user/{user_id}")
async def notify_user(user_id: int, event_type: str, message: str):
    await send_message(str(user_id), f"[{event_type}] {message}")
    return {"ok": True}
