#!/usr/bin/env python3
import json
import os

INPUT_PATH = "data/sample_chat.json"
OUTPUT_PATH = "data/sample_chat.json"

def main():
    if not os.path.exists(INPUT_PATH):
        print(f"❌ Файл не найден: {INPUT_PATH}")
        return

    try:
        with open(INPUT_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
        print(f"✅ Загружено. Тип данных: {type(data)}")
    except Exception as e:
        print(f"❌ Ошибка чтения JSON: {e}")
        return

    # Обработка: если это словарь с ключом 'messages'
    if isinstance(data, dict):
        if "messages" in data:
            messages = data["messages"]
            print(f"📦 Найден ключ 'messages', извлекаем {len(messages)} записей.")
        else:
            print("❌ JSON — словарь, но нет ключа 'messages'.")
            return
    elif isinstance(data, list):
        messages = data
        print(f"📄 Данные уже в виде списка ({len(messages)} сообщений).")
    else:
        print("❌ Неподдерживаемый формат JSON.")
        return

    # Оставляем только сообщения с текстом
    cleaned = []
    for msg in messages:
        if isinstance(msg, dict) and msg.get("text") and isinstance(msg["text"], str):
            cleaned.append(msg)

    print(f"🧹 Оставлено {len(cleaned)} сообщений с текстом.")

    # Сохраняем
    try:
        with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
            json.dump(cleaned, f, ensure_ascii=False, indent=2)
        print(f"✅ Файл сохранён: {OUTPUT_PATH}")
    except Exception as e:
        print(f"❌ Ошибка записи: {e}")

if __name__ == "__main__":
    main()
