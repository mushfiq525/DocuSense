import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from pydantic import BaseModel, Field
from sentence_transformers import SentenceTransformer

from app.config import settings
from app.vectorstore import VectorStore
from app.rag_pipeline import RAGPipeline

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

_state = {}


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Loading embedding model %s", settings.EMBEDDING_MODEL)
    model = SentenceTransformer(settings.EMBEDDING_MODEL)
    store = VectorStore()
    _state["pipeline"] = RAGPipeline(
        vectorstore=store,
        embed_fn=lambda text: model.encode(text, normalize_embeddings=True).tolist(),
    )
    logger.info("DocuSense ready (%d chunks indexed)", store.count())
    yield
    _state.clear()


app = FastAPI(title="DocuSense", version="0.1.0", lifespan=lifespan)


def _ensure_pipeline():
    if "pipeline" not in _state:
        logger.info("Initializing pipeline lazily")
        model = SentenceTransformer(settings.EMBEDDING_MODEL)
        store = VectorStore()
        _state["pipeline"] = RAGPipeline(
            vectorstore=store,
            embed_fn=lambda text: model.encode(text, normalize_embeddings=True).tolist(),
        )
    return _state["pipeline"]


class QueryRequest(BaseModel):
    question: str = Field(..., min_length=1, max_length=2000)


class SourceItem(BaseModel):
    chunk_id: str
    similarity_score: float
    text_snippet: str


class QueryResponse(BaseModel):
    answer: str
    sources: list[SourceItem]
    tokens_used: int


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/api/query", response_model=QueryResponse)
def query(req: QueryRequest):
    pipeline: RAGPipeline = _ensure_pipeline()
    try:
        result = pipeline.answer(req.question)
    except Exception:
        logger.exception("Unhandled error answering question")
        return QueryResponse(
            answer="The provided documentation does not contain sufficient information to answer this question.",
            sources=[],
            tokens_used=0,
        )
    return QueryResponse(
        answer=result.answer,
        sources=[SourceItem(**vars(s)) for s in result.sources],
        tokens_used=result.tokens_used,
    )