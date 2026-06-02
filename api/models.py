"""
Fetches available models dynamically from provider APIs.
Results are cached for 1 hour per process instance.
Falls back to the static lists in config.py if the API call fails.
"""
import time
from typing import List, Optional

_gemini_cache: Optional[List[str]] = None
_openai_cache: Optional[List[str]] = None
_gemini_cache_ts: float = 0
_openai_cache_ts: float = 0
_CACHE_TTL = 3600  # 1 hour


def _strip_models_prefix(name: str) -> str:
    return name.removeprefix("models/")


def fetch_gemini_models() -> List[str]:
    """Return all Gemini text-generation models available with the configured API key."""
    global _gemini_cache, _gemini_cache_ts

    if _gemini_cache is not None and (time.time() - _gemini_cache_ts) < _CACHE_TTL:
        return _gemini_cache

    from .config import GOOGLE_API_KEY, GEMINI_MODELS

    if not GOOGLE_API_KEY or not GOOGLE_API_KEY[0]:
        return GEMINI_MODELS

    try:
        from google import genai
        client = genai.Client(api_key=GOOGLE_API_KEY[0])
        found = []
        for m in client.models.list():
            name = _strip_models_prefix(m.name)
            if "gemini" not in name.lower():
                continue
            methods = getattr(m, "supported_generation_methods", None)
            if methods is None:
                methods = getattr(m, "supported_actions", None)
            if methods and "generateContent" not in methods:
                continue
            found.append(name)
        if found:
            _gemini_cache = sorted(found)
            _gemini_cache_ts = time.time()
            return _gemini_cache
    except Exception:
        pass

    return GEMINI_MODELS


def fetch_openai_models() -> List[str]:
    """Return all models available from the configured OpenAI-compatible endpoint."""
    global _openai_cache, _openai_cache_ts

    if _openai_cache is not None and (time.time() - _openai_cache_ts) < _CACHE_TTL:
        return _openai_cache

    from .config import OPENAI_API_KEY, OPENAI_BASE_URL, OPENAI_MODELS

    if not OPENAI_API_KEY:
        return []

    try:
        from openai import OpenAI
        client = OpenAI(api_key=OPENAI_API_KEY, base_url=OPENAI_BASE_URL)
        found = sorted(m.id for m in client.models.list().data)
        if found:
            _openai_cache = found
            _openai_cache_ts = time.time()
            return found
    except Exception:
        pass

    return OPENAI_MODELS if OPENAI_API_KEY else []


def get_all_models() -> List[str]:
    """Combined list of all available models across providers."""
    return fetch_gemini_models() + fetch_openai_models()


def invalidate_cache() -> None:
    """Force a fresh fetch on next call (e.g. after API key change)."""
    global _gemini_cache, _openai_cache
    _gemini_cache = None
    _openai_cache = None
