from .config import ALLOWED_USERS, ALLOWED_GROUPS, ADMIN_ID, AUCH_ENABLE


def is_authorized(is_group: bool, from_id: int, user_name: str, chat_id, group_name) -> bool:
    if AUCH_ENABLE == "0":
        return True
    if is_group:
        return str(group_name).lower() in ALLOWED_GROUPS or str(chat_id) in ALLOWED_GROUPS
    return str(user_name).lower() in ALLOWED_USERS or str(from_id) in ALLOWED_USERS


def is_admin(from_id: int) -> bool:
    return str(from_id) == ADMIN_ID
