from app.rag_pipeline import RAGPipeline, FALLBACK_MESSAGE


class FakeVectorStore:
    def __init__(self, hits):
        self._hits = hits

    def query(self, embedding, top_k=3, query_text=None):
        return self._hits[:top_k]


def test_low_similarity_triggers_fallback():
    hits = [{"id": "chunk_00", "document": "irrelevant", "metadata": {}, "similarity": 0.1}]
    pipeline = RAGPipeline(vectorstore=FakeVectorStore(hits), embed_fn=lambda q: [0.0])
    result = pipeline.answer("some out of scope question")
    assert result.answer == FALLBACK_MESSAGE
    assert result.sources == []
    assert result.tokens_used == 0


def test_no_hits_triggers_fallback():
    pipeline = RAGPipeline(vectorstore=FakeVectorStore([]), embed_fn=lambda q: [0.0])
    assert pipeline.answer("anything").answer == FALLBACK_MESSAGE


def test_strong_keyword_match_can_pass_low_similarity_threshold(monkeypatch):
    hits = [{
        "id": "chunk_00",
        "document": "Production backup tests are retained for one year.",
        "metadata": {},
        "similarity": 0.3357,
        "max_similarity": 0.449,
        "keyword_overlap": 5,
    }]
    monkeypatch.setattr("app.rag_pipeline.llm.generate_answer", lambda question, context: ("One year.", 12))
    pipeline = RAGPipeline(vectorstore=FakeVectorStore(hits), embed_fn=lambda q: [0.0])

    result = pipeline.answer("What is the retention requirement for production backup tests?")

    assert result.answer == "One year."
    assert result.sources[0].chunk_id == "chunk_00"