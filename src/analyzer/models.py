from datetime import datetime
from pydantic import BaseModel, Field


class TelegramMessage(BaseModel):
    id: int
    date: datetime
    text: str = ""  # по умолчанию пустая строка
    from_: str = Field(alias="from")  # "from" — ключевое слово в Python, поэтому alias
