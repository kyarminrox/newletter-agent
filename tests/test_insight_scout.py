import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pandas as pd
import pytest
from unittest.mock import patch, MagicMock

from src.agents.insight_scout import InsightScout


@pytest.fixture
def temp_metrics_csv(tmp_path):
    path = tmp_path / "metrics.csv"
    df = pd.DataFrame({
        "IssueDate": ["2025-06-01", "2025-05-15", "2025-05-01"],
        "SubjectLine": ["A", "B", "C"],
        "OpenRate": [19.2, 18.5, 17.9],
        "ClickRate": [3.4, 2.9, 2.5],
        "ReplyCount": [45, 38, 41],
        "Subscribers": [10000, 9950, 9900],
    })
    df.to_csv(path, index=False)
    return str(path)


@patch("src.agents.insight_scout.get_groq_client")
def test_extract_pain_points(mock_get_client):
    mock_get_client.return_value = MagicMock()
    scout = InsightScout()
    df = pd.DataFrame({
        "IssueDate": pd.to_datetime(["2025-06-01", "2025-05-15", "2025-05-01"]),
        "SubjectLine": ["A", "B", "C"],
        "OpenRate": [19.2, 18.5, 17.9],
        "ClickRate": [3.4, 2.9, 2.5],
        "ReplyCount": [45, 38, 41],
        "Subscribers": [10000, 9950, 9900],
    })
    points = scout._extract_pain_points(df, top_n=2)
    assert len(points) == 2
    assert "2025-05-15" in points[0]


@patch("src.agents.insight_scout.get_groq_client")
def test_fetch_research_brief_success(mock_get_client, temp_metrics_csv):
    mock_client = MagicMock()
    mock_get_client.return_value = mock_client
    dummy = (
        "## Pain Points\n- A\n- B\n\n"
        "## Trending Articles\n- Art (https://one.com)"
    )
    mock_response = MagicMock()
    mock_response.choices = [MagicMock(message=MagicMock(content=dummy))]
    mock_client.chat.completions.create.return_value = mock_response

    scout = InsightScout()
    result = scout.fetch_research_brief(temp_metrics_csv, "habit loops")
    assert "## Pain Points" in result
    assert "## Trending Articles" in result
    assert "https://one.com" in result


@patch("src.agents.insight_scout.get_groq_client")
def test_fetch_research_brief_missing_csv(mock_get_client):
    scout = InsightScout()
    with pytest.raises(FileNotFoundError):
        scout.fetch_research_brief("/no.csv", "x")


@patch("src.agents.insight_scout.get_groq_client")
def test_fetch_research_brief_missing_columns(mock_get_client, tmp_path):
    bad = tmp_path / "bad.csv"
    pd.DataFrame({"IssueDate": ["2025-06-01"]}).to_csv(bad, index=False)
    scout = InsightScout()
    with pytest.raises(ValueError):
        scout.fetch_research_brief(str(bad), "x")
