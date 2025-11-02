# src/services/rag_service.py
from llama_index.core import PromptTemplate
from src.rag_engine import create_rag_index

class RAGService:
    def __init__(self):
        self._query_engine = None

    async def initialize(self):
        if self._query_engine is None:
            index, llm = create_rag_index()
            system_prompt = (
                "Ты — умный помощник, который отвечает на вопросы на русском языке. "
                "Используй только информацию из документов. Отвечай кратко."
            )
            self._query_engine = index.as_query_engine(
                llm=llm,
                streaming=False,
                system_prompt=system_prompt
            )

    async def query(self, user_query: str) -> str:
        if self._query_engine is None:
            await self.initialize()
        response = await self._query_engine.aquery(user_query)  # асинхронный вызов
        answer = str(response.response).strip()
        source = "Источник не найден"
        if response.source_nodes:
            raw = response.source_nodes[0].node.text
            source = raw.replace('\n', ' ')[:200] + ("..." if len(raw) > 200 else "")
        return f"{answer}\n\n📌 Источник: {source}"
