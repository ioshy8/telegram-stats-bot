# src/config.py
import os
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
if not TELEGRAM_TOKEN:
    raise ValueError("TELEGRAM_BOT_TOKEN не задан в .env")

OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3-local")

# ✅ Используем правильное имя файла
DATA_PATH = "data/sample_chat.json"

if not os.path.exists(DATA_PATH):
    raise FileNotFoundError(f"Файл данных не найден: {DATA_PATH}")
