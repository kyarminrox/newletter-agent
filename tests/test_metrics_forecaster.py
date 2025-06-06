import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pandas as pd
import pytest
from unittest.mock import patch, MagicMock

from src.agents.metrics_forecaster import MetricsForecaster


def write_csv(tmp_path, rows):
    path = tmp_path / "metrics.csv"
    pd.DataFrame(rows).to_csv(path, index=False)
    return str(path)


@patch("src.agents.metrics_forecaster.get_groq_client")
def test_forecast_stub_with_insufficient_data(mock_get_client, tmp_path):
    rows = [
        {"IssueDate": "2025-06-01", "SubjectLine": "A", "OpenRate": 19.2},
        {"IssueDate": "2025-05-15", "SubjectLine": "B", "OpenRate": 18.5},
    ]
    csv_path = write_csv(tmp_path, rows)
    mock_get_client.return_value = MagicMock()
    forecaster = MetricsForecaster()
    result = forecaster.forecast(csv_path, ["Test Subject"])
    assert "## Stub Forecast" in result
    assert "Insufficient historical data" in result
    assert '"Test Subject": Predicted open rate' in result


@patch("src.agents.metrics_forecaster.get_groq_client")
def test_forecast_file_not_found(mock_get_client):
    mock_get_client.return_value = MagicMock()
    forecaster = MetricsForecaster()
    with pytest.raises(FileNotFoundError):
        forecaster.forecast("/no.csv", ["x"])


@patch("src.agents.metrics_forecaster.get_groq_client")
def test_forecast_missing_columns(mock_get_client, tmp_path):
    rows = [
        {"IssueDate": "2025-06-01", "SubjectLine": "A"},
        {"IssueDate": "2025-05-15", "SubjectLine": "B"},
        {"IssueDate": "2025-05-01", "SubjectLine": "C"},
    ]
    csv_path = write_csv(tmp_path, rows)
    mock_get_client.return_value = MagicMock()
    forecaster = MetricsForecaster()
    with pytest.raises(ValueError) as exc:
        forecaster.forecast(csv_path, ["S"])
    assert "missing required columns" in str(exc.value)


@patch("src.agents.metrics_forecaster.get_groq_client")
def test_forecast_empty_subjects(mock_get_client, tmp_path):
    rows = [
        {"IssueDate": "2025-06-01", "SubjectLine": "A", "OpenRate": 19.2},
        {"IssueDate": "2025-05-15", "SubjectLine": "B", "OpenRate": 18.5},
        {"IssueDate": "2025-05-01", "SubjectLine": "C", "OpenRate": 17.9},
    ]
    csv_path = write_csv(tmp_path, rows)
    mock_get_client.return_value = MagicMock()
    forecaster = MetricsForecaster()
    with pytest.raises(ValueError):
        forecaster.forecast(csv_path, ["", "   "])


@patch("src.agents.metrics_forecaster.get_groq_client")
def test_forecast_success(mock_get_client, tmp_path):
    rows = [
        {"IssueDate": "2025-06-01", "SubjectLine": "A", "OpenRate": 19.2},
        {"IssueDate": "2025-05-15", "SubjectLine": "B", "OpenRate": 18.5},
        {"IssueDate": "2025-05-01", "SubjectLine": "C", "OpenRate": 17.9},
        {"IssueDate": "2025-04-15", "SubjectLine": "D", "OpenRate": 17.0},
    ]
    csv_path = write_csv(tmp_path, rows)

    mock_client = MagicMock()
    mock_get_client.return_value = mock_client
    dummy_output = (
        "## Forecast\n"
        "- \"Subj\": Predicted open rate = 20%\n\n"
        "Recommended send date/time: 2025-07-02 at 09:00 UTC+3\n\n"
        "Suggested segmentation: Top 20% engaged subscribers.\n"
    )
    mock_response = MagicMock()
    mock_response.choices = [MagicMock(message=MagicMock(content=dummy_output))]
    mock_client.chat.completions.create.return_value = mock_response

    forecaster = MetricsForecaster()
    result = forecaster.forecast(csv_path, ["Subj"])
    assert "## Forecast" in result
    assert "Predicted open rate" in result
    assert "Recommended send date/time" in result


@patch("src.agents.metrics_forecaster.get_groq_client")
def test_forecast_api_error(mock_get_client, tmp_path):
    rows = [
        {"IssueDate": "2025-06-01", "SubjectLine": "A", "OpenRate": 19.2},
        {"IssueDate": "2025-05-15", "SubjectLine": "B", "OpenRate": 18.5},
        {"IssueDate": "2025-05-01", "SubjectLine": "C", "OpenRate": 17.9},
    ]
    csv_path = write_csv(tmp_path, rows)

    mock_client = MagicMock()
    mock_client.chat.completions.create.side_effect = Exception("Timeout")
    mock_get_client.return_value = mock_client

    forecaster = MetricsForecaster()
    with pytest.raises(RuntimeError) as exc:
        forecaster.forecast(csv_path, ["Subj"])
    assert "Groq API call failed" in str(exc.value)
