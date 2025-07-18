import json
import os

SETTINGS_FILE = "user_settings.json"

def load_settings():
    if not os.path.exists(SETTINGS_FILE):
        return {}
    with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_settings(data):
    with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# ✅ Сохраняет ID группы для пользователя
def set_group(user_id: int, group_id: str):
    settings = load_settings()
    user_id = str(user_id)
    if user_id not in settings:
        settings[user_id] = {}
    settings[user_id]["group_id"] = group_id
    save_settings(settings)

# ✅ Получает ID группы по пользователю
def get_group(user_id: int):
    settings = load_settings()
    return settings.get(str(user_id), {}).get("group_id")

# ✅ Сохраняет пользовательские настройки (стиль, темы, расписание)
def set_user_settings(user_id: int, data: dict):
    settings = load_settings()
    user_id = str(user_id)
    if user_id not in settings:
        settings[user_id] = {}
    settings[user_id].update(data)
    save_settings(settings)

# ✅ Получает все настройки пользователя
def get_user_settings(user_id: int):
    settings = load_settings()
    return settings.get(str(user_id), {})

# ✅ Получает все сохранённые настройки (для автопостинга)
def get_all_user_settings():
    return load_settings()
