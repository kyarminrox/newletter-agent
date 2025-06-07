import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch

from src.api import app

client = TestClient(app)

@patch("src.api.run_pipeline")
def test_run_pipeline_success(mock_run):
    mock_run.return_value = "output/2025-06-01.zip"
    payload = {
        "metrics_csv": "m.csv",
        "research_query": "q",
        "issue_brief": "b",
        "cover_image": "c.png",
        "title": "T",
        "slug": "s",
        "tags": ["x", "y"],
        "publish_date": "2025-07-01T09:00:00+03:00",
    }
    resp = client.post("/api/run-pipeline", json=payload)
    assert resp.status_code == 200
    assert resp.json() == {"package_zip_path": "output/2025-06-01.zip"}


def test_run_pipeline_missing_field():
    resp = client.post("/api/run-pipeline", json={})
    assert resp.status_code == 422


@patch("src.api.run_pipeline")
def test_run_pipeline_error(mock_run):
    mock_run.side_effect = Exception("boom")
    payload = {
        "metrics_csv": "m.csv",
        "research_query": "q",
        "issue_brief": "b",
        "cover_image": "c.png",
        "title": "T",
        "slug": "s",
        "tags": ["x"],
        "publish_date": "2025-07-01T09:00:00+03:00",
    }
    resp = client.post("/api/run-pipeline", json=payload)
    assert resp.status_code == 500
    assert "boom" in resp.text
