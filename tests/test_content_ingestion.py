import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import pytest

from src.agents.data_collector import ingest_content


def test_ingest_content_success(tmp_path):
    md_dir = tmp_path / "mds"
    md_dir.mkdir()
    (md_dir / "file1.md").write_text("# Title 1\nContent", encoding="utf-8")
    (md_dir / "file2.md").write_text("# Title 2\nContent", encoding="utf-8")
    docs = ingest_content(str(md_dir))
    assert len(docs) == 2
    assert docs[0]["metadata"]["filename"].endswith(".md")


def test_ingest_content_no_files(tmp_path):
    empty = tmp_path / "empty"
    empty.mkdir()
    with pytest.raises(ValueError):
        ingest_content(str(empty))
