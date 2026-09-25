from app.vectorstore import VectorStore


def test_hybrid_search_promotes_lexical_match(tmp_path):
    store = VectorStore(persist_dir=str(tmp_path), collection_name="hybrid-test")
    store.add(
        ids=["dense", "lexical", "noise_1", "noise_2"],
        embeddings=[[1.0, 0.0], [0.8, 0.6], [0.7, 0.7], [-1.0, 0.0]],
        documents=[
            "General security controls for the platform.",
            "Production backup tests are retained for one year.",
            "Account access and authentication procedures.",
            "Monitoring and logging requirements for systems.",
        ],
        metadatas=[
            {"source_page": "General"},
            {"source_page": "Backups"},
            {"source_page": "Access"},
            {"source_page": "Monitoring"},
        ],
    )

    hits = store.query(
        [1.0, 0.0],
        top_k=1,
        query_text="What is the retention requirement for production backup tests?",
    )

    assert hits[0]["id"] == "lexical"
    assert hits[0]["keyword_overlap"] >= 3
    assert hits[0]["max_similarity"] > 0.99