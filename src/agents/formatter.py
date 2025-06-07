# src/agents/formatter.py

import os
import shutil
import json
import zipfile
from datetime import datetime
from pathlib import Path

class Formatter:
    """Create a Substack-ready package from draft, cover image, and metadata."""

    def __init__(self, output_root: str = "package"):
        self.output_root = Path(output_root)

    def package_for_substack(
        self,
        draft_path: str,
        cover_image_path: str,
        title: str,
        slug: str,
        tags: list[str],
        publish_date: str,
    ) -> str:
        """Create package/YYYY-MM-DD.zip and return its path."""

        draft_file = Path(draft_path)
        if not draft_file.is_file():
            raise FileNotFoundError(f"Draft file not found at {draft_path}")
        cover_file = Path(cover_image_path)
        if not cover_file.is_file():
            raise FileNotFoundError(f"Cover image not found at {cover_image_path}")

        if not title.strip():
            raise ValueError("Title cannot be empty.")
        if not slug.strip():
            raise ValueError("Slug cannot be empty.")
        if not tags:
            raise ValueError("At least one tag is required.")
        try:
            datetime.fromisoformat(publish_date)
        except Exception:
            raise ValueError("Publish date must be in ISO 8601 format.")

        date_folder = datetime.now().strftime("%Y-%m-%d")
        pkg_dir = self.output_root / date_folder
        images_dir = pkg_dir / "images"

        try:
            if pkg_dir.exists():
                shutil.rmtree(pkg_dir)
            images_dir.mkdir(parents=True)

            draft_text = draft_file.read_text(encoding="utf-8")
            issue_md = f"![Cover](images/cover.png)\n\n{draft_text}"
            (pkg_dir / "Issue.md").write_text(issue_md, encoding="utf-8")

            dest_cover = images_dir / "cover.png"
            shutil.copy2(cover_file, dest_cover)

            metadata = {
                "title": title,
                "slug": slug,
                "tags": tags,
                "publish_date": publish_date,
            }
            (pkg_dir / "metadata.json").write_text(
                json.dumps(metadata, ensure_ascii=False, indent=2), encoding="utf-8"
            )

            zip_path = self.output_root / f"{date_folder}.zip"
            with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
                for root, _, files in os.walk(pkg_dir):
                    for file in files:
                        fp = Path(root) / file
                        zf.write(fp, arcname=str(fp.relative_to(self.output_root)))
            return str(zip_path)
        except Exception as e:
            if pkg_dir.exists():
                shutil.rmtree(pkg_dir)
            zp = self.output_root / f"{date_folder}.zip"
            if zp.exists():
                zp.unlink()
            raise RuntimeError(f"Packaging failed: {e}")
