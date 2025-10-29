import re


def anonymize_text(text: str) -> str:
    # Заменяем email на [EMAIL]
    text = re.sub(
        r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b", "[EMAIL]", text
    )
    # Заменяем телефоны на [PHONE]
    text = re.sub(r"\+?\d[\d\s\-\(\)]{7,}\d", "[PHONE]", text)
    return text
