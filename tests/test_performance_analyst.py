import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pandas as pd
import pytest
from unittest.mock import patch, MagicMock

from src.agents.performance_analyst import PerformanceAnalyst

DUMMY_FORECAST = "## Forecast\n- \"X\": Predicted open = 20%\n"


def write_csv(path, rows):
    pd.DataFrame(rows).to_csv(path, index=False)


@patch("src.agents.performance_analyst.get_groq_client")
def test_analyze_success(mock_get_client, tmp_path):
    rows = [
        {"IssueDate": "2025-06-01", "OpenRate": 19.0, "ClickRate": 3.5},
        {"IssueDate": "2025-05-15", "OpenRate": 18.0, "ClickRate": 3.0},
    ]
    csv_path = tmp_path / "actuals.csv"
    write_csv(csv_path, rows)

    mock_client = MagicMock()
    mock_get_client.return_value = mock_client
    dummy_output = (
        "## Lessons Learned\n"
        "- Forecast was within 1% of actual open rates.\n"
        "- Click rates underperformed forecast; consider stronger CTAs.\n"
        "- Consider A/B testing subject lines with < 2% variance.\n"
    )
    resp = MagicMock()
    resp.choices = [MagicMock(message=MagicMock(content=dummy_output))]
    mock_client.chat.completions.create.return_value = resp

    analyst = PerformanceAnalyst()
    result = analyst.analyze(DUMMY_FORECAST, str(csv_path))
    assert "## Lessons Learned" in result
    assert "Forecast was within" in result


@patch("src.agents.performance_analyst.get_groq_client")
def test_analyze_empty_forecast(mock_get_client, tmp_path):
    mock_get_client.return_value = MagicMock()
    analyst = PerformanceAnalyst()
    with pytest.raises(ValueError):
        analyst.analyze("", str(tmp_path / "x.csv"))


@patch("src.agents.performance_analyst.get_groq_client")
def test_analyze_csv_not_found(mock_get_client):
    mock_get_client.return_value = MagicMock()
    analyst = PerformanceAnalyst()
    with pytest.raises(FileNotFoundError):
        analyst.analyze(DUMMY_FORECAST, "no.csv")


@patch("src.agents.performance_analyst.get_groq_client")
def test_analyze_missing_columns(mock_get_client, tmp_path):
    rows = [{"IssueDate": "2025-06-01", "OpenRate": 19.0}]
    csv_path = tmp_path / "bad.csv"
    write_csv(csv_path, rows)
    mock_get_client.return_value = MagicMock()
    analyst = PerformanceAnalyst()
    with pytest.raises(ValueError):
        analyst.analyze(DUMMY_FORECAST, str(csv_path))


@patch("src.agents.performance_analyst.get_groq_client")
def test_analyze_api_error(mock_get_client, tmp_path):
    rows = [
        {"IssueDate": "2025-06-01", "OpenRate": 19.0, "ClickRate": 3.5},
        {"IssueDate": "2025-05-15", "OpenRate": 18.0, "ClickRate": 3.0},
    ]
    csv_path = tmp_path / "act.csv"
    write_csv(csv_path, rows)

    mock_client = MagicMock()
    mock_client.chat.completions.create.side_effect = Exception("Timeout")
    mock_get_client.return_value = mock_client

    analyst = PerformanceAnalyst()
    with pytest.raises(RuntimeError):
        analyst.analyze(DUMMY_FORECAST, str(csv_path))
