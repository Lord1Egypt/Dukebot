from typing import Dict, Optional


class UserSettings:
    def __init__(self, model: str, prompt_key: str, system_prompt: str):
        self.model = model
        self.prompt_key = prompt_key
        self.system_prompt = system_prompt
        self.awaiting_custom_prompt: bool = False


_settings: Dict[int, UserSettings] = {}


def _defaults():
    from .config import DEFAULT_MODEL, PRESET_PROMPTS
    return DEFAULT_MODEL, "default", PRESET_PROMPTS["default"]


def get_settings(user_id: int) -> UserSettings:
    if user_id not in _settings:
        model, key, prompt = _defaults()
        _settings[user_id] = UserSettings(model=model, prompt_key=key, system_prompt=prompt)
    return _settings[user_id]


def set_model(user_id: int, model: str) -> None:
    get_settings(user_id).model = model


def set_prompt(user_id: int, prompt_key: str, custom_text: Optional[str] = None) -> None:
    from .config import PRESET_PROMPTS
    s = get_settings(user_id)
    s.prompt_key = prompt_key
    if prompt_key == "custom" and custom_text:
        s.system_prompt = custom_text
    elif prompt_key in PRESET_PROMPTS:
        s.system_prompt = PRESET_PROMPTS[prompt_key]


def set_awaiting_custom_prompt(user_id: int, value: bool) -> None:
    get_settings(user_id).awaiting_custom_prompt = value


def is_awaiting_custom_prompt(user_id: int) -> bool:
    return get_settings(user_id).awaiting_custom_prompt
