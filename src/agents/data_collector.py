import glob
import os
from typing import List, Dict

import pandas as pd
import numpy as np

from ..utils import get_groq_client


def ingest_metrics(csv_path: str) -> pd.DataFrame:
    """Parse metrics CSV into DataFrame with validated columns."""
    if not os.path.isfile(csv_path):
        raise FileNotFoundError(f"Metrics CSV not found at {csv_path}")

    df = pd.read_csv(csv_path)
    required = {"IssueDate", "SubjectLine", "OpenRate", "ClickRate", "ReplyCount", "Subscribers"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"Metrics CSV is missing required columns: {missing}")

    df["IssueDate"] = pd.to_datetime(df["IssueDate"], format="%Y-%m-%d")
    df["OpenRate"] = df["OpenRate"].astype(float)
    df["ClickRate"] = df["ClickRate"].astype(float)
    df["ReplyCount"] = df["ReplyCount"].astype(int)
    df["Subscribers"] = df["Subscribers"].astype(int)

    df = df.sort_values("IssueDate", ascending=False).reset_index(drop=True)
    return df


def ingest_content(markdown_dir: str) -> List[Dict[str, str]]:
    """Load all markdown files from directory."""
    pattern = os.path.join(markdown_dir, "*.md")
    files = glob.glob(pattern)
    if not files:
        raise ValueError(f"No Markdown files found in {markdown_dir}")

    docs = []
    for path in files:
        with open(path, "r", encoding="utf-8") as f:
            text = f.read()
        docs.append({"path": path, "content": text, "metadata": {"filename": os.path.basename(path)}})
    return docs


def compute_embeddings(documents: List[str], model: str = "llama-3.1-8b-instant") -> np.ndarray:
    """Generate embeddings for documents using Groq via a language model."""
    client = get_groq_client()
    vectors = []
    for doc in documents:
        prompt = (
            "Generate a fixed-length embedding vector (as a JSON array) for the following text:\n\n" + doc
        )
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are an embedding generator."},
                {"role": "user", "content": prompt},
            ],
        )
        text = response.choices[0].message.content.strip()
        try:
            vector = np.array(eval(text), dtype=float)
        except Exception as exc:
            raise RuntimeError(f"Failed to parse embedding vector from Groq: {exc}")
        vectors.append(vector)

    return np.vstack(vectors)
