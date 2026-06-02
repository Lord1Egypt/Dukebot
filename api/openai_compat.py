from typing import List, Dict, Optional

from .config import OPENAI_API_KEY, OPENAI_BASE_URL, ai_err_info

_client = None


def _get_client():
    global _client
    if _client is None:
        if not OPENAI_API_KEY:
            raise RuntimeError("OPENAI_API_KEY is not configured.")
        from openai import OpenAI
        _client = OpenAI(api_key=OPENAI_API_KEY, base_url=OPENAI_BASE_URL)
    return _client


class ChatConversation:
    def __init__(self, model: str = "gpt-4o-mini", system_prompt: str = "") -> None:
        self.model = model
        self.system_prompt = system_prompt
        self._history: List[Dict[str, str]] = []
        if system_prompt:
            self._history.append({"role": "system", "content": system_prompt})

    def send_message(self, prompt: str) -> str:
        self._history.append({"role": "user", "content": prompt})
        try:
            response = _get_client().chat.completions.create(
                model=self.model,
                messages=self._history,
            )
            result = response.choices[0].message.content or ""
            self._history.append({"role": "assistant", "content": result})
            return result
        except Exception as e:
            self._history.pop()
            return f"{ai_err_info}\n{repr(e)}"

    @property
    def history_length(self) -> int:
        return sum(1 for m in self._history if m["role"] != "system")
