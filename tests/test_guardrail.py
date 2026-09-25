from app.rag_pipeline import RAGPipeline, FALLBACK_MESSAGE


class FakeVectorStore:
    def __init__(self, hits):
        self._hits = hits

    def query(self, embedding, top_k=3):
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