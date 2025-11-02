# src/tools/currency.py
import httpx
from src.tools.base import Tool

class CurrencyTool(Tool):
    name = "курс_валют"
    description = "Получает курс доллара к рублю"

    async def run(self, query: str) -> str:
        try:
            r = await httpx.get("https://www.cbr-xml-daily.ru/daily_json.js", timeout=10.0)
            data = r.json()
            rub = data["Valute"]["USD"]["Value"]
            return f"💱 Курс доллара: {rub:.2f} RUB"
        except:
            return "Не удалось получить курс."
