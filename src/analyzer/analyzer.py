import json
from pathlib import Path
from datetime import datetime, timedelta
from .models import TelegramMessage
from src.utils.anonymize import anonymize_text


def count_messages_yesterday(json_path: Path) -> int:
    # 1. Читаем JSON
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    messages = []
    # 2. Парсим каждое сообщение
    for msg in data.get("messages", []):
        if (
            msg.get("type") != "message"
        ):  # пропускаем "service_message", "pinned_message"
            continue
        try:
            m = TelegramMessage(**msg)  # валидация через pydantic
            messages.append(m)
        except Exception:
            continue  # игнорируем битые сообщения — инженерная зрелость

    # 3. Считаем за вчера
    yesterday = datetime.utcnow().date() - timedelta(days=1)
    count = 0
    for m in messages:
        if m.date.date() == yesterday:
            anonymize_text(
                m.text
            )  # вызываем для анонимизации (можно сохранить результат)
            count += 1

    return count
