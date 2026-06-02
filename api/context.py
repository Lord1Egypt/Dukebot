from io import BytesIO
from typing import Dict, Any

import requests

from .config import BOT_TOKEN


def _make_conversation(model: str, system_prompt: str):
    if model.startswith("gemini"):
        from .gemini import ChatConversation
    else:
        from .openai_compat import ChatConversation
    return ChatConversation(model=model, system_prompt=system_prompt)


class ChatManager:
    def __init__(self):
        self._chats: Dict[int, Any] = {}

    def get_chat(self, history_id: int, model: str, system_prompt: str):
        if history_id not in self._chats:
            self._chats[history_id] = _make_conversation(model, system_prompt)
        return self._chats[history_id]

    def reset_chat(self, history_id: int) -> None:
        self._chats.pop(history_id, None)

    def has_chat(self, history_id: int) -> bool:
        return history_id in self._chats


# Module-level singleton shared across handle.py and command.py
chat_manager = ChatManager()


class ImageChatManager:
    def __init__(self, prompt: str, file_id: str, model: str = "gemini-2.0-flash") -> None:
        self.prompt = prompt
        self.file_id = file_id
        self.model = model if model.startswith("gemini") else "gemini-2.0-flash"

    def _photo_url(self) -> str:
        r = requests.get(f"https://api.telegram.org/bot{BOT_TOKEN}/getFile?file_id={self.file_id}")
        file_path = r.json()["result"]["file_path"]
        return f"https://api.telegram.org/file/bot{BOT_TOKEN}/{file_path}"

    def photo_url(self) -> str:
        return self._photo_url()

    def send_image(self) -> str:
        from .gemini import generate_text_with_image
        photo_bytes = BytesIO(requests.get(self._photo_url()).content)
        return generate_text_with_image(self.prompt, photo_bytes, self.model)
