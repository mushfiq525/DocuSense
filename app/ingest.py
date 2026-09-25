"""One-time CLI: chunk docs/source.md, embed, persist to Chroma.
Usage: python -m app.ingest
"""
import re
import logging
from pathlib import Path

from langchain_text_splitters import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer

from app.config import settings
from app.vectorstore import VectorStore

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

PAGE_BREAK_RE = re.compile(r"<!--\s*PAGE_BREAK\s*-->")
TITLE_RE = re.compile(r"^##\s+(.+)$", re.MULTILINE)
SOURCE_COMMENT_RE = re.compile(r"<!--\s*source:\s*(\S+)\s*-->")


def load_sections(source_path: Path):
    """Split source.md into (page_title, source_url, page_text) sections.

    Splits only on the injected <!-- PAGE_BREAK --> marker, never on '##'
    headings that occur naturally inside a fetched page's own content
    (Purpose, Scope, Roles & Responsibilities, etc.) — those stay part of
    the same page's chunk pool.
    """
    text = source_path.read_text(encoding="utf-8")
    raw_sections = [s for s in PAGE_BREAK_RE.split(text) if s.strip()]

    sections = []
    for raw in raw_sections:
        title_match = TITLE_RE.search(raw)
        title = title_match.group(1).strip() if title_match else "Untitled"
        url_match = SOURCE_COMMENT_RE.search(raw)
        url = url_match.group(1) if url_match else ""

        body = raw[title_match.end():] if title_match else raw
        body = SOURCE_COMMENT_RE.sub("", body).strip()
        sections.append((title, url, body))
    return sections


def main():
    source_path = Path(settings.SOURCE_MD_PATH)
    if not source_path.exists():
        raise FileNotFoundError(f"{source_path} not found. Run scripts/fetch_corpus.py first.")

    sections = load_sections(source_path)
    logger.info("Loaded %d page sections from %s", len(sections), source_path)

    splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
        encoding_name="cl100k_base",
        chunk_size=settings.CHUNK_SIZE,
        chunk_overlap=settings.CHUNK_OVERLAP,
    )

    ids, documents, metadatas = [], [], []
    chunk_counter = 0
    for title, url, body in sections:
        for piece in splitter.split_text(body):
            ids.append(f"chunk_{chunk_counter:02d}")
            documents.append(piece)
            metadatas.append({"source_page": title, "source_url": url})
            chunk_counter += 1

    logger.info("Split into %d chunks (size=%d, overlap=%d)", len(ids), settings.CHUNK_SIZE, settings.CHUNK_OVERLAP)

    logger.info("Loading embedding model: %s", settings.EMBEDDING_MODEL)
    model = SentenceTransformer(settings.EMBEDDING_MODEL)
    embeddings = model.encode(documents, show_progress_bar=True, normalize_embeddings=True).tolist()

    store = VectorStore()
    store.add(ids=ids, embeddings=embeddings, documents=documents, metadatas=metadatas)
    logger.info("Persisted %d chunks to Chroma at %s", store.count(), settings.CHROMA_DIR)


if __name__ == "__main__":
    main()