# src/rag_engine.py
import re
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Document
from llama_index.llms.ollama import Ollama
from llama_index.embeddings.ollama import OllamaEmbedding
from src.config import OLLAMA_MODEL, DATA_PATH
import logging

logger = logging.getLogger(__name__)

def anonymize_text(text: str) -> str:
    """Удаляет персональные данные (email, телефоны, упоминания)."""
    text = re.sub(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', '[EMAIL]', text)
    text = re.sub(r'\+?\d[\s\-()]?\d{2,}', '[PHONE]', text)
    text = re.sub(r'\b(from|от)\s+[A-Za-zА-Яа-яёЁ][A-Za-zА-Яа-яёЁ0-9_]*', r'\1 [USER]', text, flags=re.IGNORECASE)
    return text

def load_and_anonymize_documents():
    """Загружает JSON и применяет анонимизацию."""
    logger.info(f"Загрузка данных из: {DATA_PATH}")
    
    # Кастомный загрузчик: извлекаем только поле "text" из JSON
    def json_text_extractor(file_path):
        import json
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        if isinstance(data, dict) and "messages" in data:
            messages = data["messages"]
        else:
            messages = data
        texts = []
        for msg in messages:
            if isinstance(msg, dict) and "text" in msg and isinstance(msg["text"], str):
                texts.append(msg["text"])
        return texts

    raw_texts = json_text_extractor(DATA_PATH)
    
    anonymized_docs = []
    for text in raw_texts:
        clean_text = anonymize_text(text)
        if clean_text.strip():
            anonymized_docs.append(Document(text=clean_text))
    
    logger.info(f"Загружено и анонимизировано {len(anonymized_docs)} документов.")
    return anonymized_docs

def create_rag_index():
    """
    Создаёт RAG-индекс с использованием:
    - Локальной LLM через Ollama,
    - Эмбеддингов через Ollama (nomic-embed-text).
    """
    documents = load_and_anonymize_documents()

    # Используем OllamaEmbedding — никаких путей к кэшу не нужно
    embed_model = OllamaEmbedding(model_name="nomic-embed-text")

    llm = Ollama(model=OLLAMA_MODEL, request_timeout=120.0)

    index = VectorStoreIndex.from_documents(documents, embed_model=embed_model)
    logger.info("✅ RAG-индекс успешно создан с nomic-embed-text.")
    
    return index, llm
