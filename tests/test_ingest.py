from pathlib import Path
import tempfile

from app.ingest import load_sections


def test_load_sections_splits_only_on_page_break_marker():
    content = (
        "<!-- PAGE_BREAK -->\n## Page One\n\n<!-- source: https://example.com/one -->\n\n"
        "Body one text.\n\n## Purpose\n\nA subheading inside page one that must NOT split it.\n\n"
        "<!-- PAGE_BREAK -->\n## Page Two\n\n<!-- source: https://example.com/two -->\n\nBody two text.\n"
    )
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "source.md"
        path.write_text(content, encoding="utf-8")
        sections = load_sections(path)

    assert len(sections) == 2
    assert sections[0][0] == "Page One"
    assert sections[0][1] == "https://example.com/one"
    assert "Body one text." in sections[0][2]
    assert "subheading inside page one" in sections[0][2]  # proves it wasn't split
    assert sections[1][0] == "Page Two"