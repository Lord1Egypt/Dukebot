import json
from typing import Dict, List

import requests
from md2tgmd import escape

from .config import BOT_TOKEN, defaut_photo_caption, unnamed_user, unnamed_group
from .printLog import send_log

TELEGRAM_API = f"https://api.telegram.org/bot{BOT_TOKEN}"


def send_message(chat_id, text: str, **kwargs):
    payload = {
        "chat_id": chat_id,
        "text": escape(text),
        "parse_mode": "MarkdownV2",
        **kwargs,
    }
    r = requests.post(f"{TELEGRAM_API}/sendMessage", data=payload)
    return r


def send_inline_keyboard(chat_id, text: str, keyboard: List[List[Dict]]):
    """
    keyboard: list of rows; each row is a list of {"text": str, "callback_data": str}
    """
    payload = {
        "chat_id": chat_id,
        "text": escape(text),
        "parse_mode": "MarkdownV2",
        "reply_markup": json.dumps({
            "inline_keyboard": [
                [{"text": btn["text"], "callback_data": btn["callback_data"]} for btn in row]
                for row in keyboard
            ]
        }),
    }
    r = requests.post(f"{TELEGRAM_API}/sendMessage", data=payload)
    return r


def edit_message(chat_id, message_id: int, text: str, keyboard: List[List[Dict]] = None):
    payload = {
        "chat_id": chat_id,
        "message_id": message_id,
        "text": escape(text),
        "parse_mode": "MarkdownV2",
    }
    if keyboard is not None:
        payload["reply_markup"] = json.dumps({
            "inline_keyboard": [
                [{"text": btn["text"], "callback_data": btn["callback_data"]} for btn in row]
                for row in keyboard
            ]
        })
    requests.post(f"{TELEGRAM_API}/editMessageText", data=payload)


def answer_callback_query(callback_query_id: str, text: str = ""):
    payload = {"callback_query_id": callback_query_id, "text": text}
    requests.post(f"{TELEGRAM_API}/answerCallbackQuery", data=payload)


def send_photo_message(chat_id, text: str, image_id: str):
    payload = {
        "chat_id": chat_id,
        "caption": escape(text),
        "parse_mode": "MarkdownV2",
        "photo": image_id,
    }
    r = requests.post(f"{TELEGRAM_API}/sendPhoto", data=payload)
    return r


class Update:
    def __init__(self, update: Dict) -> None:
        msg = update["message"]
        self.from_id = msg["from"]["id"]
        self.chat_id = msg["chat"]["id"]
        self.from_type = msg["chat"]["type"]
        self.is_group: bool = self.from_type in ("supergroup", "group")
        self.type = self._type(msg)
        self.text = self._text(msg)
        self.photo_caption = self._photo_caption(msg)
        self.file_id = self._file_id(msg)
        self.user_name = msg["from"].get(
            "username",
            f"[{unnamed_user}](tg://openmessage?user_id={self.from_id})"
        )
        self.group_name = msg["chat"].get(
            "username",
            f"[{unnamed_group}](tg://openmessage?chat_id={str(self.chat_id)[4:]})"
        )
        self.message_id: int = msg["message_id"]

    def _type(self, msg: Dict) -> str:
        if "text" in msg:
            return "command" if msg["text"].startswith("/") else "text"
        if "photo" in msg:
            return "photo"
        return ""

    def _text(self, msg: Dict) -> str:
        if "text" not in msg:
            return ""
        text = msg["text"]
        if text.startswith("/"):
            # Strip the command prefix and any bot @mention (e.g. /cmd@BotName)
            cmd = text[1:].split("@")[0].strip()
            return cmd
        return text

    def _photo_caption(self, msg: Dict) -> str:
        if "photo" in msg:
            return msg.get("caption", defaut_photo_caption)
        return ""

    def _file_id(self, msg: Dict) -> str:
        if "photo" in msg:
            return msg["photo"][-1]["file_id"]
        return ""


class CallbackUpdate:
    def __init__(self, update: Dict) -> None:
        cq = update["callback_query"]
        self.callback_query_id: str = cq["id"]
        self.from_id: int = cq["from"]["id"]
        self.chat_id: int = cq["message"]["chat"]["id"]
        self.message_id: int = cq["message"]["message_id"]
        self.data: str = cq.get("data", "")
        self.user_name: str = cq["from"].get("username", str(self.from_id))
