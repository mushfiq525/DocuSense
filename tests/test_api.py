import os
import pytest
from fastapi.testclient import TestClient

from app.api import app

pytestmark = pytest.mark.skipif(
    not os.getenv("GEMINI_API_KEY") and not os.getenv("GROQ_API_KEY"),
    reason="Needs a live LLM key + `python -m app.ingest` already run.",
)


def test_out_of_scope_question_returns_fallback():
    with TestClient(app) as client:
        resp = client.post("/api/query", json={"question": "What is GitLab's parental leave policy?"})
        assert resp.status_code == 200
        body = resp.json()
        assert body["answer"] == "The provided documentation does not contain sufficient information to answer this question."
        assert body["sources"] == []


def test_in_scope_question_returns_grounded_answer():
    with TestClient(app) as client:
        resp = client.post("/api/query", json={"question": "What is the minimum password length required?"})
        assert resp.status_code == 200
        body = resp.json()
        assert len(body["sources"]) > 0
        assert body["answer"] != "The provided documentation does not contain sufficient information to answer this question."