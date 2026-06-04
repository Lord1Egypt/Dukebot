from io import BytesIO
from typing import Optional

import PIL.Image
from google import genai
from google.genai import types

from .config import GOOGLE_API_KEY, generation_config, ai_err_info

_client: Optional[genai.Client] = None


def _get_client() -> genai.Client:
    global _client
    if _client is None:
        if not GOOGLE_API_KEY or not GOOGLE_API_KEY[0]:
            raise RuntimeError("GOOGLE_API_KEY is not configured.")
        _client = genai.Client(api_key=GOOGLE_API_KEY[0])
    return _client


def generate_text_with_image(prompt: str, image_bytes: BytesIO, model: str = "gemini-flash-latest") -> str:
    img = PIL.Image.open(image_bytes)
    try:
        response = _get_client().models.generate_content(
            model=model,
            contents=[img, prompt],
        )
        return response.text
    except Exception as e:
        return f"{ai_err_info}\n{repr(e)}"


class ChatConversation:
    def __init__(self, model: str = "gemini-flash-latest", system_prompt: str = "") -> None:
        self.model = model
        self.system_prompt = system_prompt
        cfg = types.GenerateContentConfig(
            max_output_tokens=generation_config.get("max_output_tokens", 2048),
            system_instruction=system_prompt if system_prompt else None,
        )
        self._chat = _get_client().chats.create(model=model, config=cfg)

    def send_message(self, prompt: str) -> str:
        try:
            response = self._chat.send_message(prompt)
            return response.text
        except Exception as e:
            return f"{ai_err_info}\n{repr(e)}"

    @property
    def history_length(self) -> int:
        return len(self._chat.get_history())
