# debug_retrieval.py
from sentence_transformers import SentenceTransformer
from app.vectorstore import VectorStore
from app.config import settings

model = SentenceTransformer(settings.EMBEDDING_MODEL)
store = VectorStore()

question = "Are GitLab team members required to use multi-factor authentication?"
q_emb = model.encode(question, normalize_embeddings=True).tolist()

hits = store.query(q_emb, top_k=5)
for h in hits:
    print(f"\n--- similarity={h['similarity']:.4f} | id={h['id']} ---")
    print(h['document'][:300])

# find which chunk contains the real answer, and where it ranks
all_data = store.collection.get(include=["documents", "metadatas"])
for id_, doc in zip(all_data["ids"], all_data["documents"]):
    if "required to use" in doc and "Multi-Factor" in doc:
        print(f"Found in {id_}:\n{doc}\n{'='*60}")

# add to debug_retrieval.py, replace the top_k=5 call
hits = store.query(q_emb, top_k=20)
for i, h in enumerate(hits):
    marker = " <-- chunk_09" if h["id"] == "chunk_09" else ""
    print(f"{i+1}. similarity={h['similarity']:.4f} | id={h['id']}{marker}")