import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import pandas as pd
import pytest

from src.agents.data_collector import ingest_metrics


def test_ingest_metrics_success(tmp_path):
    csv_file = tmp_path / "metrics.csv"
    df = pd.DataFrame({
        "IssueDate": ["2025-06-01", "2025-05-15"],
        "SubjectLine": ["A", "B"],
        "OpenRate": [19.2, 18.5],
        "ClickRate": [3.1, 2.0],
        "ReplyCount": [10, 5],
        "Subscribers": [1000, 1000],
    })
    df.to_csv(csv_file, index=False)
    result = ingest_metrics(str(csv_file))
    assert list(result.columns) == [
        "IssueDate",
        "SubjectLine",
        "OpenRate",
        "ClickRate",
        "ReplyCount",
        "Subscribers",
    ]
    assert result.iloc[0]["IssueDate"].strftime("%Y-%m-%d") == "2025-06-01"


def test_ingest_metrics_missing_columns(tmp_path):
    csv_file = tmp_path / "metrics.csv"
    df = pd.DataFrame({
        "IssueDate": ["2025-06-01"],
    })
    df.to_csv(csv_file, index=False)
    with pytest.raises(ValueError):
        ingest_metrics(str(csv_file))


def test_ingest_metrics_file_not_found():
    with pytest.raises(FileNotFoundError):
        ingest_metrics("/nonexistent.csv")
