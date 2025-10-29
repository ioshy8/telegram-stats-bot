# src/bot/main.py
import os
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from dotenv import load_dotenv
from src.analyzer.analyzer import count_messages_yesterday
from pathlib import Path

# Загружаем переменные из .env
load_dotenv()

# Получаем токен
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("TELEGRAM_BOT_TOKEN не найден в .env")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message is None:
        return  # или логгировать, но не падать
    await update.message.reply_text("Привет! Отправь команду /stats для анализа.")


async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message is None:
        return
    try:
        count = count_messages_yesterday(Path("data/sample_chat.json"))
        await update.message.reply_text(f"Сообщений за вчера: {count}")
    except Exception as e:
        await update.message.reply_text(f"Ошибка: {str(e)}")


def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("stats", stats))
    app.run_polling()


if __name__ == "__main__":
    main()
