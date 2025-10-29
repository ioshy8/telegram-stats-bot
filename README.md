# Telegram Stats Bot

Анализирует экспортированный чат Telegram и показывает статистику (сообщения за вчера).

## Установка

```bash
git clone https://github.com/ваш-логин/telegram-stats-bot.git
cd telegram-stats-bot
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env  # и вставьте свой токен от @BotFather
