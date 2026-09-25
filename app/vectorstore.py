import chromadb
from app.config import settings


class VectorStore:
    def __init__(self, persist_dir: str | None = None, collection_name: str | None = None):
        self.client = chromadb.PersistentClient(path=persist_dir or settings.CHROMA_DIR)
        self.collection = self.client.get_or_create_collection(
            name=collection_name or settings.COLLECTION_NAME,
            metadata={"hnsw:space": "cosine"},
        )

    def add(self, ids, embeddings, documents, metadatas):
        self.collection.upsert(ids=ids, embeddings=embeddings, documents=documents, metadatas=metadatas)

    def count(self) -> int:
        return self.collection.count()

    def query(self, query_embedding, top_k: int = 3):
        result = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
            include=["documents", "metadatas", "distances"],
        )
        hits = []
        ids = result.get("ids", [[]])[0]
        docs = result.get("documents", [[]])[0]
        metas = result.get("metadatas", [[]])[0]
        dists = result.get("distances", [[]])[0]
        for id_, doc, meta, dist in zip(ids, docs, metas, dists):
            hits.append({"id": id_, "document": doc, "metadata": meta, "similarity": 1.0 - dist})
        return hits