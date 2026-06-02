import requests
from md2tgmd import escape

from .config import IS_DEBUG_MODE, ADMIN_ID, BOT_TOKEN

TELEGRAM_API = f"https://api.telegram.org/bot{BOT_TOKEN}"


def send_log(text: str) -> None:
    if IS_DEBUG_MODE != "1":
        return
    payload = {
        "chat_id": ADMIN_ID,
        "text": escape(text),
        "parse_mode": "MarkdownV2",
    }
    requests.post(f"{TELEGRAM_API}/sendMessage", data=payload)


def send_image_log(text: str, image_id: str) -> None:
    if IS_DEBUG_MODE != "1":
        return
    payload = {
        "chat_id": ADMIN_ID,
        "caption": escape(text),
        "parse_mode": "MarkdownV2",
        "photo": image_id,
    }
    requests.post(f"{TELEGRAM_API}/sendPhoto", data=payload)
