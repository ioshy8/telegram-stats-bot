# src/bot/main.py
import logging
import os
import json
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from src.config import TELEGRAM_TOKEN
from src.rag_engine import create_rag_index
from src.tools import detect_tool

# Настройка логгера
os.makedirs("logs", exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("logs/bot.log", encoding="utf-8"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Глобальные переменные для кэширования RAG
_index = None
_llm = None
_query_engine = None

def load_chat_data():
    with open("data/sample_chat.json", "r", encoding="utf-8") as f:
        return json.load(f)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привет! Я бот Спирали 1.\n"
        "Вы можете:\n"
        "• Спросить что-то по вашим сообщениям (например: «Что я писал о парсерах?»)\n"
        "• Узнать курс доллара (напишите: «курс доллара»)\n"
        "• Получить статистику чата: /stats"
    )

async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        data = load_chat_data()
        total_messages = len(data)
        user_messages = sum(1 for msg in data if msg.get("from") == "User")
        await update.message.reply_text(
            f"📊 Статистика чата:\n"
            f"Всего сообщений: {total_messages}\n"
            f"Ваших сообщений: {user_messages}"
        )
    except Exception as e:
        logger.error(f"Ошибка в /stats: {e}")
        await update.message.reply_text("Не удалось загрузить статистику.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global _index, _llm, _query_engine

    user_query = update.message.text.strip()
    if not user_query:
        return

    logger.info(f"Получен запрос: {user_query}")

    # Проверка внешних инструментов (заглушка на День 2)
    tool_response = await detect_tool(user_query)
    if tool_response:
        await update.message.reply_text(tool_response)
        return

    # Ленивая инициализация RAG
    if _query_engine is None:
        await update.message.reply_text("Инициализация RAG... Подождите 10–30 секунд.")
        try:
            _index, _llm = create_rag_index()

            # Системный промпт на русском
            system_prompt = (
                "Ты — умный помощник, который отвечает на вопросы на русском языке. "
                "Используй только информацию из предоставленных документов. "
                "Если не знаешь ответа — скажи, что не знаешь. Отвечай кратко и по делу."
            )
            from llama_index.core import PromptTemplate
            _query_engine = _index.as_query_engine(
                llm=_llm,
                streaming=False,
                system_prompt=system_prompt
            )
            logger.info("✅ RAG успешно инициализирован.")
        except Exception as e:
            logger.error(f"❌ Ошибка инициализации RAG: {e}")
            await update.message.reply_text("Не удалось запустить RAG. Проверьте логи.")
            return

    # Обработка запроса
    try:
        # Явно указываем, что нужен ответ на русском
        augmented_query = f"Отвечай строго на русском языке. Вопрос: {user_query}"
        response = _query_engine.query(augmented_query)
        answer_text = str(response.response).strip() or "Не удалось сформулировать ответ."

        # Источник
        source_text = "Источник не найден"
        if response.source_nodes:
            raw = response.source_nodes[0].node.text
            source_text = raw.replace('\n', ' ')[:200] + ("..." if len(raw) > 200 else "")

        reply = f"{answer_text}\n\n📌 Источник: {source_text}"
        await update.message.reply_text(reply)
    except Exception as e:
        logger.error(f"❌ Ошибка RAG-запроса: {e}")
        await update.message.reply_text("Произошла ошибка при поиске ответа.")

def main():
    if not TELEGRAM_TOKEN:
        raise ValueError("TELEGRAM_BOT_TOKEN не задан в .env")

    logger.info("🚀 Запуск Telegram-бота Спирали 1...")
    app = Application.builder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("stats", stats))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    logger.info("✅ Бот запущен. Ожидание сообщений...")
    app.run_polling()

if __name__ == "__main__":
    main()
