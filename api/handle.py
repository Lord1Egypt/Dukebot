from .auth import is_authorized
from .command import execute_command
from .config import (
    GROUP_MODE, prompt_new_threshold, prompt_new_info,
    unable_to_recognize_content,
    group_no_permission_info, user_no_permission_info,
    event_received, group_label, the_content_sent_is, the_reply_content_is,
    the_accompanying_message_is, the_logarithm_of_historical_conversations_is,
    no_rights_to_use, send_unrecognized_content, PRESET_PROMPT_LABELS,
)
from .context import chat_manager, ImageChatManager
from .printLog import send_log, send_image_log
from .telegram import (
    Update, CallbackUpdate, send_message, send_inline_keyboard,
    answer_callback_query, edit_message,
)
from .user_settings import (
    get_settings, set_model, set_prompt,
    set_awaiting_custom_prompt, is_awaiting_custom_prompt,
)


def _history_id(update: Update) -> int:
    if update.is_group and GROUP_MODE == "2":
        return update.from_id
    return update.chat_id


def _model_keyboard(current_model: str):
    from .models import get_all_models
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


def handle_message(update_data: dict) -> None:
    update = Update(update_data)

    log_prefix = (
        f"{event_received} @{update.user_name} id:`{update.from_id}` "
        f"{group_label} @{update.group_name} id:`{update.chat_id}`"
        if update.is_group
        else f"{event_received} @{update.user_name} id:`{update.from_id}`"
    )
    send_log(f"{log_prefix}\n{the_content_sent_is} {update.text}")

    history_id = _history_id(update)

    # ── Check if awaiting custom prompt input ─────────────────────────────────
    if update.type == "text" and is_awaiting_custom_prompt(update.from_id):
        set_prompt(update.from_id, "custom", update.text)
        set_awaiting_custom_prompt(update.from_id, False)
        chat_manager.reset_chat(history_id)
        send_message(update.chat_id, f"Custom prompt set. Starting a fresh conversation.")
        return

    # ── Commands don't require auth ───────────────────────────────────────────
    if update.type == "command":
        response = execute_command(
            update.from_id, update.text, update.from_type,
            update.chat_id, update.is_group, GROUP_MODE,
        )
        if response:
            send_message(update.chat_id, response)
        return

    # ── Auth check for chat/photo ─────────────────────────────────────────────
    authorized = is_authorized(
        update.is_group, update.from_id, update.user_name,
        update.chat_id, update.group_name,
    )
    if not authorized:
        if update.is_group:
            send_message(update.chat_id, f"{group_no_permission_info}\nID:`{update.chat_id}`")
        else:
            send_message(update.from_id, f"{user_no_permission_info}\nID:`{update.from_id}`")
        send_log(f"{log_prefix} {no_rights_to_use}")
        return

    # ── Text chat ─────────────────────────────────────────────────────────────
    if update.type == "text":
        settings = get_settings(update.from_id)
        chat = chat_manager.get_chat(history_id, settings.model, settings.system_prompt)
        answer = chat.send_message(update.text)
        extra = f"\n\n{prompt_new_info}" if chat.history_length >= prompt_new_threshold * 2 else ""
        response = f"{answer}{extra}"
        send_message(update.chat_id, response)
        send_log(
            f"{log_prefix}\n{the_content_sent_is} {update.text}\n"
            f"{the_reply_content_is} {response}\n"
            f"{the_logarithm_of_historical_conversations_is} {chat.history_length // 2}"
        )

    # ── Photo ─────────────────────────────────────────────────────────────────
    elif update.type == "photo":
        settings = get_settings(update.from_id)
        img_chat = ImageChatManager(update.photo_caption, update.file_id, settings.model)
        response = img_chat.send_image()
        send_message(update.chat_id, response, reply_to_message_id=update.message_id)
        send_log(
            f"{log_prefix} [photo] {the_accompanying_message_is} {update.photo_caption}\n"
            f"{the_reply_content_is} {response}"
        )
        send_image_log("", update.file_id)

    else:
        send_message(update.chat_id, f"{unable_to_recognize_content}\n\n/help")
        send_log(f"{log_prefix} {send_unrecognized_content}")


def handle_callback(update_data: dict) -> None:
    cq = CallbackUpdate(update_data)
    answer_callback_query(cq.callback_query_id)

    data = cq.data
    from_id = cq.from_id

    if data.startswith("model:"):
        model_name = data[len("model:"):]
        set_model(from_id, model_name)
        # Reset both possible history_id variants so the next message starts fresh
        chat_manager.reset_chat(from_id)
        chat_manager.reset_chat(cq.chat_id)
        keyboard = _model_keyboard(model_name)
        edit_message(
            cq.chat_id, cq.message_id,
            f"Model set to: {model_name}\n\nSelect a model:",
            keyboard,
        )

    elif data.startswith("prompt:"):
        prompt_key = data[len("prompt:"):]
        if prompt_key == "custom":
            set_awaiting_custom_prompt(from_id, True)
            edit_message(
                cq.chat_id, cq.message_id,
                "Please type your custom system prompt in the next message:",
            )
        else:
            set_prompt(from_id, prompt_key)
            chat_manager.reset_chat(from_id)
            chat_manager.reset_chat(cq.chat_id)
            label = PRESET_PROMPT_LABELS.get(prompt_key, prompt_key)
            keyboard = _prompt_keyboard(prompt_key)
            edit_message(
                cq.chat_id, cq.message_id,
                f"Prompt set to: {label}\n\nSelect a system prompt:",
                keyboard,
            )
