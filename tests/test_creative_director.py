import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest
from unittest.mock import patch, MagicMock

from src.agents.creative_director import CreativeDirector

DUMMY_EXCERPT = (
    "# Building Habit Loops\n\n"
    "Habit loops—composed of a cue, routine, and reward—can transform your newsletter. "
    "They encourage subscribers to open and engage regularly."
)


@patch("src.agents.creative_director.get_groq_client")
def test_suggest_visuals_success(mock_get_client):
    mock_client = MagicMock()
    mock_get_client.return_value = mock_client

    dummy_output = (
        "Charcoal background with a golden barbell: a minimal fit motif\t\"/imagine charcoal background, golden barbell, minimal style, centered\"\n"
        "Hand-drawn habit loop diagram in pastel colors\t\"/imagine pastel hand-drawn diagram of cue-routine-reward, minimalist layout\"\n"
        "Simple white notebook and coffee cup on a wooden table\t\"/imagine overhead shot minimal wooden table, white notebook, coffee cup, soft shadows\""
    )
    mock_response = MagicMock()
    mock_response.choices = [MagicMock(message=MagicMock(content=dummy_output))]
    mock_client.chat.completions.create.return_value = mock_response

    director = CreativeDirector()
    result = director.suggest_visuals(DUMMY_EXCERPT)
    lines = result.split("\n")
    assert len(lines) == 3
    assert "\t" in lines[0]
    assert "barbell" in lines[0]


@patch("src.agents.creative_director.get_groq_client")
def test_suggest_visuals_empty_excerpt(mock_get_client):
    director = CreativeDirector()
    with pytest.raises(ValueError):
        director.suggest_visuals("")


@patch("src.agents.creative_director.get_groq_client")
def test_suggest_visuals_api_error(mock_get_client):
    mock_client = MagicMock()
    mock_client.chat.completions.create.side_effect = Exception("Timeout")
    mock_get_client.return_value = mock_client

    director = CreativeDirector()
    with pytest.raises(RuntimeError) as exc:
        director.suggest_visuals(DUMMY_EXCERPT)
    assert "Groq API call failed" in str(exc.value)
