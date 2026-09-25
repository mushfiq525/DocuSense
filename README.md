# DocuSense — Grounded RAG Microservice

Answers questions about GitLab's Security Policies & Standards handbook
section, grounded strictly in the source documents, with a deterministic
fallback when the corpus doesn't cover the question.

## Stack
- Embeddings: `sentence-transformers/all-MiniLM-L6-v2` (local, free, CPU)
- Vector store: Chroma (embedded, persisted to `./chroma_db`)
- LLM: Google Gemini (`gemini-flash-latest`) with Groq (`openai/gpt-oss-20b`) as automatic fallback
- API: FastAPI

## Setup
```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # then paste your Gemini + Groq keys in
python scripts/fetch_corpus.py   # one-time: builds docs/source.md
python -m app.ingest              # one-time: builds ./chroma_db
uvicorn app.api:app --reload
```

Get a free Gemini key at https://aistudio.google.com/app/apikey and a free
Groq key at https://console.groq.com/keys — neither requires a credit card.

## Try it
```bash
curl -X POST http://localhost:8000/api/query \
  -H "Content-Type: application/json" \
  -d '{"question": "What is the minimum password length required by GitLab'\''s password standard?"}'

curl -X POST http://localhost:8000/api/query \
  -H "Content-Type: application/json" \
  -d '{"question": "What is GitLab'\''s parental leave policy?"}'
```

Grounded response example (verified):
```json
{
  "answer": "The minimum password length required by GitLab’s password standard is **12 characters**.",
  "sources": [
    {"chunk_id": "chunk_13", "similarity_score": 0.7064, "text_snippet": "### Password Requirements ... Minimum Length = 12 characters ..."},
    {"chunk_id": "chunk_07", "similarity_score": 0.6719, "text_snippet": "# GitLab Password Standards ..."},
    {"chunk_id": "chunk_08", "similarity_score": 0.65, "text_snippet": "### Password Requirements ... Minimum Length = 12 characters ..."}
  ],
  "tokens_used": 1296
}
```

Out-of-scope fallback example:
```json
{
  "answer": "The provided documentation does not contain sufficient information to answer this question.",
  "sources": [],
  "tokens_used": 0
}
```

## Design decisions
- **Chunking**: ~500 tokens with 50-token overlap. This keeps each policy section coherent enough to preserve the relevant sentence-level context, while still allowing adjacent chunks to overlap so related facts remain connected when a query spans a section boundary.
- **Similarity threshold**: 0.6. In live corpus checks, grounded questions returned top similarities around 0.65–0.71, while out-of-scope and adversarial prompts fell below the threshold. That gap gives a clear guardrail before the LLM call is made.
- **Corpus scope**: the GitLab Handbook Security Policies & Standards section
  (15 pages) — narrow enough to fact-check in an evening, broad enough to
  force genuine multi-document retrieval, with a clean out-of-scope boundary
  (anything from People Group, Engineering workflow, Sales/Marketing).
- **Guardrail**: a deterministic similarity check runs *before* the LLM call
  (cheap, fast, not reliant on the model self-policing), backed by a strict
  system prompt as a second line of defense against prompt injection.

## Docker
```bash
docker compose up --build
```

## Eval
```bash
uvicorn app.api:app &
python eval.py
```