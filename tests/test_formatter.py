import os
import json
import zipfile
from datetime import datetime
import pytest

from src.agents.formatter import Formatter


def write_temp_file(tmp_dir, name, content, binary=False):
    path = os.path.join(tmp_dir, name)
    mode = "wb" if binary else "w"
    with open(path, mode) as f:
        if binary:
            f.write(content)
        else:
            f.write(content)
    return path


def test_package_success(tmp_path):
    draft_path = write_temp_file(tmp_path, "draft.md", "# Title\nContent")
    cover_path = write_temp_file(tmp_path, "cover.png", b"\x89PNG\r\n\x1a\n", binary=True)
    fmt = Formatter(output_root=str(tmp_path / "pkg"))
    zip_path = fmt.package_for_substack(
        draft_path,
        cover_path,
        "Title",
        "slug",
        ["tag1", "tag2"],
        "2025-07-01T09:00:00+03:00",
    )
    assert os.path.isfile(zip_path)
    with zipfile.ZipFile(zip_path) as zf:
        names = set(zf.namelist())
        date_folder = datetime.now().strftime("%Y-%m-%d")
        base = f"{date_folder}"
        assert f"{base}/Issue.md" in names
        assert f"{base}/images/cover.png" in names
        assert f"{base}/metadata.json" in names
        with zf.open(f"{base}/metadata.json") as f:
            metadata = json.load(f)
        assert metadata["title"] == "Title"


def test_package_missing_files(tmp_path):
    cover_path = write_temp_file(tmp_path, "cover.png", b"img", binary=True)
    fmt = Formatter(output_root=str(tmp_path / "pkg"))
    with pytest.raises(FileNotFoundError):
        fmt.package_for_substack(
            "no_draft.md",
            cover_path,
            "T",
            "s",
            ["t"],
            "2025-07-01T09:00:00+03:00",
        )
    draft_path = write_temp_file(tmp_path, "draft.md", "content")
    with pytest.raises(FileNotFoundError):
        fmt.package_for_substack(
            draft_path,
            "no_cover.png",
            "T",
            "s",
            ["t"],
            "2025-07-01T09:00:00+03:00",
        )


def test_package_invalid_metadata(tmp_path):
    draft_path = write_temp_file(tmp_path, "draft.md", "content")
    cover_path = write_temp_file(tmp_path, "cover.png", b"img", binary=True)
    fmt = Formatter(output_root=str(tmp_path / "pkg"))
    with pytest.raises(ValueError):
        fmt.package_for_substack(draft_path, cover_path, "", "s", ["t"], "2025-07-01T09:00:00+03:00")
    with pytest.raises(ValueError):
        fmt.package_for_substack(draft_path, cover_path, "T", "", ["t"], "2025-07-01T09:00:00+03:00")
    with pytest.raises(ValueError):
        fmt.package_for_substack(draft_path, cover_path, "T", "s", [], "2025-07-01T09:00:00+03:00")
    with pytest.raises(ValueError):
        fmt.package_for_substack(draft_path, cover_path, "T", "s", ["t"], "bad-date")
