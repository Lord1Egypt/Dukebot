from .auth import is_admin
from .config import (
    ALLOWED_USERS, ALLOWED_GROUPS, GOOGLE_API_KEY, OPENAI_API_KEY,
    PRESET_PROMPT_LABELS, IS_DEBUG_MODE,
    help_text, admin_auch_info, debug_mode_info, command_format_error_info,
    new_chat_info,
)
from .context import chat_manager
from .models import get_all_models
from .printLog import send_log
from .telegram import send_message, send_inline_keyboard
from .user_settings import get_settings, set_awaiting_custom_prompt


def _model_keyboard(current_model: str):
    models = get_all_models()
    rows = []
    for i in range(0, len(models), 2):
        row = []
        for m in models[i:i + 2]:
            label = f"✅ {m}" if m == current_model else m
            row.append({"text": label, "callback_data": f"model:{m}"})
        rows.append(row)
    return rows


def _prompt_keyboard(current_key: str):
    rows = []
    for key, label in PRESET_PROMPT_LABELS.items():
        display = f"✅ {label}" if key == current_key else label
        rows.append([{"text": display, "callback_data": f"prompt:{key}"}])
    custom_label = "✅ ✏️ Custom" if current_key == "custom" else "✏️ Custom"
    rows.append([{"text": custom_label, "callback_data": "prompt:custom"}])
    return rows


def cmd_help() -> str:
    return help_text


def cmd_new(from_id: int, chat_id: int, is_group: bool, group_mode: str) -> str:
    history_id = from_id if (is_group and group_mode == "2") else chat_id
    chat_manager.reset_chat(history_id)
    return new_chat_info


def cmd_model(from_id: int, chat_id: int) -> str:
    s = get_settings(from_id)
    keyboard = _model_keyboard(s.model)
    send_inline_keyboard(chat_id, f"Current model: {s.model}\n\nSelect a model:", keyboard)
    return ""


def cmd_prompt(from_id: int, chat_id: int) -> str:
    s = get_settings(from_id)
    label = PRESET_PROMPT_LABELS.get(s.prompt_key, "Custom")
    keyboard = _prompt_keyboard(s.prompt_key)
    send_inline_keyboard(chat_id, f"Current prompt: {label}\n\nSelect a system prompt:", keyboard)
    return ""


def cmd_get_my_info(from_id: int) -> str:
    return f"Your Telegram ID: `{from_id}`"


def cmd_get_group_info(from_type: str, chat_id: int) -> str:
    if from_type in ("supergroup", "group"):
        return f"Group ID: `{chat_id}`"
    return "Please use this command in a group."


def _require_admin_debug(from_id: int) -> str:
    if not is_admin(from_id):
        return admin_auch_info
    if IS_DEBUG_MODE == "0":
        return debug_mode_info
    return ""


def cmd_get_allowed_users(from_id: int) -> str:
    err = _require_admin_debug(from_id)
    if err:
        return err
    send_log(f"Allowed users:\n{ALLOWED_USERS}")
    return ""


def cmd_get_allowed_groups(from_id: int) -> str:
    err = _require_admin_debug(from_id)
    if err:
        return err
    send_log(f"Allowed groups:\n{ALLOWED_GROUPS}")
    return ""


def cmd_get_api_keys(from_id: int) -> str:
    err = _require_admin_debug(from_id)
    if err:
        return err
    gemini_count = len(GOOGLE_API_KEY)
    openai_set = bool(OPENAI_API_KEY)
    send_log(f"Gemini keys: {gemini_count} configured\nOpenAI-compat key set: {openai_set}")
    return ""


def cmd_list_models(from_id: int) -> str:
    err = _require_admin_debug(from_id)
    if err:
        return err
    models = get_all_models()
    send_log(f"Available models:\n" + "\n".join(models))
    return ""


def cmd_send_message(from_id: int, command: str) -> str:
    if not is_admin(from_id):
        return admin_auch_info
    parts = command.split(" ", 2)
    if len(parts) < 3:
        return command_format_error_info
    _, to_id, text = parts
    try:
        send_message(to_id, text)
        send_log(f"Test message sent to {to_id}")
    except Exception as e:
        send_log(f"Send error: {e}")
    return ""


def execute_command(from_id: int, command: str, from_type: str, chat_id: int,
                    is_group: bool, group_mode: str) -> str:
    cmd = command.split()[0].lower() if command else ""

    if cmd in ("start", "help"):
        return cmd_help()
    if cmd == "new":
        return cmd_new(from_id, chat_id, is_group, group_mode)
    if cmd == "model":
        return cmd_model(from_id, chat_id)
    if cmd == "prompt":
        return cmd_prompt(from_id, chat_id)
    if cmd in ("get_my_info", "getmyinfo"):
        return cmd_get_my_info(from_id)
    if cmd in ("get_group_info", "getgroupinfo"):
        return cmd_get_group_info(from_type, chat_id)
    if cmd == "get_allowed_users":
        return cmd_get_allowed_users(from_id)
    if cmd == "get_allowed_groups":
        return cmd_get_allowed_groups(from_id)
    if cmd in ("get_api_key", "get_api_keys"):
        return cmd_get_api_keys(from_id)
    if cmd == "list_models":
        return cmd_list_models(from_id)
    if cmd == "send_message":
        return cmd_send_message(from_id, command)

    return f"Unknown command. Use /help for the list of commands."
