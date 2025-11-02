# src/tools.py
import httpx
import logging
import re
from .currency import CurrencyTool  # ← новый импорт
logger = logging.getLogger(__name__)
_currency_tool = CurrencyTool()
async def get_usd_rate() -> str:
    """Получает курс доллара к рублю."""
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            r = await client.get("https://api.exchangerate-api.com/v4/latest/USD")
            r.raise_for_status()
            data = r.json()
            rub = data["rates"].get("RUB")
            if rub:
                return f"💱 Курс доллара: {rub:.2f} RUB"
            else:
                return "Курс RUB не найден."
    except Exception as e:
        logger.error(f"Ошибка API курса: {e}")
        return "Не удалось получить курс доллара."

async def get_weather_moscow() -> str:
    """Получает текущую погоду в Москве через Open-Meteo (бесплатно, без ключа)."""
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            r = await client.get(
                "https://api.open-meteo.com/v1/forecast",
                params={
                    "latitude": 55.7522,   # широта Москвы
                    "longitude": 37.6156,  # долгота Москвы
                    "current_weather": "true"
                }
            )
            r.raise_for_status()
            data = r.json()
            current = data.get("current_weather")
            if current and "temperature" in current:
                temp = current["temperature"]
                return f"🌤 Погода в Москве: {temp}°C"
            else:
                return "Данные о погоде недоступны."
    except Exception as e:
        logger.error(f"Ошибка API погоды: {e}")
        return "Не удалось получить погоду."

async def detect_tool(query: str) -> str | None:
    """
    Определяет, нужно ли вызывать внешний инструмент.
    Возвращает ответ инструмента или None.
    """
    q = query.lower()
    if re.search(r"курс.*доллар|курс.*usd", q):
        return await _currency_tool.run(query)
    if re.search(r"погода.*москв", q):
        # Позже добавите WeatherTool аналогично
        return "Погода пока не реализована."
    return None
    # Курс доллара
    if re.search(r"курс.*доллар", query_lower) or re.search(r"курс.*usd", query_lower):
        return await get_usd_rate()

    # Погода в Москве
    if re.search(r"погода", query_lower) and re.search(r"москв", query_lower):
        return await get_weather_moscow()

    # Сюда можно добавлять новые инструменты
    return None
