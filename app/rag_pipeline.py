import logging
from dataclasses import dataclass, field
from typing import List

from app.config import settings
from app.vectorstore import VectorStore
from app import llm

logger = logging.getLogger(__name__)

FALLBACK_MESSAGE = "The provided documentation does not contain sufficient information to answer this question."


@dataclass
class SourceHit:
    chunk_id: str
    similarity_score: float
    text_snippet: str


@dataclass
class QueryResult:
    answer: str
    sources: List[SourceHit] = field(default_factory=list)
    tokens_used: int = 0


class RAGPipeline:
    def __init__(self, vectorstore: VectorStore, embed_fn):
        self.vectorstore = vectorstore
        self.embed_fn = embed_fn

    def answer(self, question: str) -> QueryResult:
        question_embedding = self.embed_fn(question)
        hits = self.vectorstore.query(question_embedding, top_k=settings.TOP_K, query_text=question)

        max_similarity = max((h.get("max_similarity", h["similarity"]) for h in hits), default=0.0)
        keyword_overlap = max((h.get("keyword_overlap", 0) for h in hits), default=0)
        if not hits or (max_similarity < settings.SIMILARITY_THRESHOLD and keyword_overlap < 3):
            logger.info("Guardrail triggered: top similarity below threshold")
            return QueryResult(answer=FALLBACK_MESSAGE)

        context_blocks = [h["document"] for h in hits]
        try:
            answer_text, tokens = llm.generate_answer(question, context_blocks)
        except llm.LLMError:
            return QueryResult(answer=FALLBACK_MESSAGE)

        if answer_text.strip() == FALLBACK_MESSAGE:
            return QueryResult(answer=FALLBACK_MESSAGE, tokens_used=tokens)

        sources = [
            SourceHit(
                chunk_id=h["id"],
                similarity_score=round(h["similarity"], 4),
                text_snippet=(h["document"][:200] + "...") if len(h["document"]) > 200 else h["document"],
            )
            for h in hits
        ]
        return QueryResult(answer=answer_text, sources=sources, tokens_used=tokens)