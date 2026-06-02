import os
from re import split

# ── Required ──────────────────────────────────────────────────────────────────
BOT_TOKEN = os.environ.get("BOT_TOKEN", "")
GOOGLE_API_KEY = [k for k in split(r'[ ,;，；]+', os.environ.get("GOOGLE_API_KEY", "")) if k]

# ── OpenAI-compatible API (optional) ──────────────────────────────────────────
# Works with OpenAI, OpenCode, OpenRouter, Groq, Together AI, Mistral, etc.
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")
OPENAI_BASE_URL = os.environ.get("OPENAI_BASE_URL", "https://api.openai.com/v1")

# ── Access control (optional) ─────────────────────────────────────────────────
ALLOWED_USERS = [u for u in split(r'[ ,;，；]+', os.getenv("ALLOWED_USERS", "").replace("@", "").lower()) if u]
ALLOWED_GROUPS = [g for g in split(r'[ ,;，；]+', os.getenv("ALLOWED_GROUPS", "").replace("@", "").lower()) if g]

IS_DEBUG_MODE = os.getenv("IS_DEBUG_MODE", "0")
ADMIN_ID = os.getenv("ADMIN_ID", "1234567890")
AUCH_ENABLE = os.getenv("AUCH_ENABLE", "1")
GROUP_MODE = os.getenv("GROUP_MODE", "1")

# ── Models ────────────────────────────────────────────────────────────────────
_gemini_defaults = "gemini-2.0-flash,gemini-1.5-pro,gemini-1.5-flash"
_openai_defaults = "gpt-4o,gpt-4o-mini"

GEMINI_MODELS = [m for m in split(r'[ ,;，；]+', os.getenv("GEMINI_MODELS", _gemini_defaults)) if m]
OPENAI_MODELS = [m for m in split(r'[ ,;，；]+', os.getenv("OPENAI_MODELS", _openai_defaults)) if m]
DEFAULT_MODEL = os.getenv("DEFAULT_MODEL", GEMINI_MODELS[0] if GEMINI_MODELS else "gemini-2.0-flash")


# ── System prompt presets ─────────────────────────────────────────────────────
PRESET_PROMPTS = {
    "default": (
        "You are Duke Bot, a helpful and friendly AI assistant. "
        "Be concise, accurate, and conversational."
    ),
    "professional": (
        "You are an expert professional consultant. Provide detailed, "
        "structured, and well-researched answers with clear headings and "
        "bullet points when appropriate."
    ),
    "creative": (
        "You are a creative partner with a vivid imagination. Think outside "
        "the box, use metaphors, craft stories, and inspire with original ideas."
    ),
}

PRESET_PROMPT_LABELS = {
    "default": "🤖 Default",
    "professional": "💼 Professional",
    "creative": "✨ Creative",
}

# ── Thresholds & defaults ─────────────────────────────────────────────────────
prompt_new_threshold = 3
defaut_photo_caption = "Describe this image"

generation_config = {"max_output_tokens": 2048}

# ── Bot messages ──────────────────────────────────────────────────────────────
help_text = (
    "Duke Bot - Multi-model AI assistant\n\n"
    "Send me text or images and I'll respond using the selected AI model.\n"
    "In groups, mention me by name or reply to my messages.\n\n"
    "Commands:\n"
    "/new - Start a fresh conversation\n"
    "/model - Switch AI model\n"
    "/prompt - Change system prompt\n"
    "/get_my_info - Get your Telegram ID\n"
    "/get_group_info - Get group ID (group only)\n"
    "/help - Show this help"
)

admin_auch_info = "You are not the administrator or your administrator ID is set incorrectly."
debug_mode_info = "Debug mode is not enabled."
command_format_error_info = "Command format error."
user_no_permission_info = "You are not allowed to use this bot."
group_no_permission_info = "This group does not have permission to use this bot."
ai_err_info = "Something went wrong! The content may be inappropriate or there was an API error."
new_chat_info = "Starting a fresh conversation."
prompt_new_info = "Tip: type /new to start a fresh chat."
unable_to_recognize_content = "I couldn't recognize that content. Try sending text or an image."

# ── Log messages ──────────────────────────────────────────────────────────────
send_message_log = "Message sent:"
send_photo_log = "Photo sent:"
unnamed_user = "UnnamedUser"
unnamed_group = "UnnamedGroup"
event_received = "Event received"
group_label = "group"
the_content_sent_is = "Content:"
the_reply_content_is = "Reply:"
the_accompanying_message_is = "Caption:"
the_logarithm_of_historical_conversations_is = "History length:"
no_rights_to_use = "Unauthorized"
send_unrecognized_content = "Unrecognized content type"
