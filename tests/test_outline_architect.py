import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest
from unittest.mock import patch, MagicMock

from src.agents.outline_architect import OutlineArchitect

DUMMY_RESEARCH = (
    "## Pain Points\n"
    "- Low engagement on issue 1\n"
    "- Subscribers dropping off after week 2\n\n"
    "## Trending Articles\n"
    "- Article A (https://a.com)\n"
    "- Article B (https://b.com)"
)

DUMMY_ISSUE = "Topic: Habit Loops; Audience: 10k subscribers; Tone: minimal, direct."


@patch("src.agents.outline_architect.get_groq_client")
def test_generate_outlines_success(mock_get_client):
    mock_client = MagicMock()
    mock_get_client.return_value = mock_client
    dummy_md = (
        "# Outline Option 1\n"
        "## Section 1\n"
        "Something\n"
        "## Subject Line Candidates\n"
        "- A\n- B\n- C\n\n"
        "# Outline Option 2\n...\n"
        "# Outline Option 3\n..."
    )
    mock_response = MagicMock()
    mock_response.choices = [MagicMock(message=MagicMock(content=dummy_md))]
    mock_client.chat.completions.create.return_value = mock_response

    arch = OutlineArchitect()
    result = arch.generate_outlines(DUMMY_RESEARCH, DUMMY_ISSUE)

    assert result.startswith("# Outline Option 1")
    assert "# Outline Option 2" in result
    assert "# Outline Option 3" in result


@patch("src.agents.outline_architect.get_groq_client")
def test_generate_outlines_empty_research(mock_get_client):
    arch = OutlineArchitect()
    with pytest.raises(ValueError):
        arch.generate_outlines("", DUMMY_ISSUE)


@patch("src.agents.outline_architect.get_groq_client")
def test_generate_outlines_empty_issue(mock_get_client):
    arch = OutlineArchitect()
    with pytest.raises(ValueError):
        arch.generate_outlines(DUMMY_RESEARCH, "")
