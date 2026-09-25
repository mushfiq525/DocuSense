#!/bin/sh
set -e
if [ ! -d "/app/chroma_db" ] || [ -z "$(ls -A /app/chroma_db 2>/dev/null)" ]; then
  echo "No existing vector store — running ingestion..."
  python -m app.ingest
fi
exec uvicorn app.api:app --host 0.0.0.0 --port 8000