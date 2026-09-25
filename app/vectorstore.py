import re

import chromadb
from rank_bm25 import BM25Okapi

from app.config import settings

TOKEN_RE = re.compile(r"[a-z0-9]+")
STOP_WORDS = {
    "a", "an", "and", "are", "as", "at", "be", "before", "by", "can", "does",
    "for", "from", "how", "in", "is", "it", "of", "on", "or", "that", "the",
    "their", "this", "to", "what", "when", "where", "which", "who", "why", "with",
}
RRF_CONSTANT = 10


def _tokenize(text: str) -> list[str]:
    return [token for token in TOKEN_RE.findall(text.lower()) if token not in STOP_WORDS]


def _expand_query_tokens(tokens: list[str]) -> list[str]:
    expanded = list(tokens)
    if "password" in tokens and {"periodically", "periodic", "regularly", "change", "rotate"}.intersection(tokens):
        expanded.extend(("expiration", "expiry", "expires"))
    return expanded


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

    def query(self, query_embedding, top_k: int = 3, query_text: str | None = None):
        collection_count = self.collection.count()
        if not collection_count:
            return []

        candidate_count = min(collection_count, max(top_k * 5, 30))
        result = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=candidate_count,
            include=["documents", "metadatas", "distances"],
        )
        ids = result.get("ids", [[]])[0]
        docs = result.get("documents", [[]])[0]
        metas = result.get("metadatas", [[]])[0]
        dists = result.get("distances", [[]])[0]
        dense_hits = [
            {"id": id_, "document": doc, "metadata": meta, "similarity": 1.0 - dist}
            for id_, doc, meta, dist in zip(ids, docs, metas, dists)
        ]
        if not query_text:
            return dense_hits[:top_k]

        all_data = self.collection.get(include=["documents", "metadatas"])
        all_ids = all_data["ids"]
        all_docs = all_data["documents"]
        all_metas = all_data["metadatas"]
        tokenized_docs = [_tokenize(doc or "") for doc in all_docs]
        query_tokens = _expand_query_tokens(_tokenize(query_text))
        bm25 = BM25Okapi(tokenized_docs)
        lexical_scores = bm25.get_scores(query_tokens)
        lexical_order = sorted(range(len(all_ids)), key=lambda index: lexical_scores[index], reverse=True)
        lexical_order = [index for index in lexical_order if lexical_scores[index] > 0][:candidate_count]

        dense_by_id = {hit["id"]: hit for hit in dense_hits}
        document_by_id = dict(zip(all_ids, all_docs))
        metadata_by_id = dict(zip(all_ids, all_metas))
        fused_scores = {}
        for rank, hit in enumerate(dense_hits, 1):
            fused_scores[hit["id"]] = fused_scores.get(hit["id"], 0) + 1 / (RRF_CONSTANT + rank)
        for rank, index in enumerate(lexical_order, 1):
            id_ = all_ids[index]
            fused_scores[id_] = fused_scores.get(id_, 0) + 1 / (RRF_CONSTANT + rank)

        max_similarity = dense_hits[0]["similarity"]
        query_terms = set(query_tokens)
        ranked_ids = sorted(fused_scores, key=fused_scores.get, reverse=True)[:top_k]
        hits = []
        for id_ in ranked_ids:
            document = document_by_id[id_]
            hits.append({
                "id": id_,
                "document": document,
                "metadata": metadata_by_id[id_],
                "similarity": dense_by_id.get(id_, {}).get("similarity", 0.0),
                "max_similarity": max_similarity,
                "keyword_overlap": len(query_terms.intersection(_tokenize(document or ""))),
            })
        return hits