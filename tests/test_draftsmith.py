import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest
from unittest.mock import patch, MagicMock

from src.agents.draftsmith import Draftsmith

DUMMY_OUTLINE = (
    "# Outline Option 1\n"
    "## Section 1: Hook\n"
    "Brief description of the hook.\n\n"
    "## Section 2: Data\n"
    "Include relevant data points.\n\n"
    "## Subject Line Candidates\n"
    "- Subject A\n"
    "- Subject B\n"
    "- Subject C"
)


@patch("src.agents.draftsmith.get_groq_client")
def test_create_draft_success(mock_get_client):
    mock_client = MagicMock()
    mock_get_client.return_value = mock_client
    dummy = (
        "<!-- COVER_IMAGE_HOOK -->\n"
        "# Building Habit Loops\n\n"
        "Body..."
    )
    mock_response = MagicMock()
    mock_response.choices = [MagicMock(message=MagicMock(content=dummy))]
    mock_client.chat.completions.create.return_value = mock_response

    smith = Draftsmith()
    result = smith.create_draft(DUMMY_OUTLINE)
    assert result.startswith("<!-- COVER_IMAGE_HOOK -->")


@patch("src.agents.draftsmith.get_groq_client")
def test_create_draft_empty_outline(mock_get_client):
    smith = Draftsmith()
    with pytest.raises(ValueError):
        smith.create_draft("")


@patch("src.agents.draftsmith.get_groq_client")
def test_create_draft_api_error(mock_get_client):
    mock_client = MagicMock()
    mock_client.chat.completions.create.side_effect = Exception("boom")
    mock_get_client.return_value = mock_client
    smith = Draftsmith()
    with pytest.raises(RuntimeError):
        smith.create_draft(DUMMY_OUTLINE)
