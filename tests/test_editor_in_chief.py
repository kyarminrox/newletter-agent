import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest
from unittest.mock import patch, MagicMock

from src.agents.editor_in_chief import EditorInChief

DUMMY_DRAFT = (
    "<!-- COVER_IMAGE_HOOK -->\n"
    "# Building Habit Loops\n\n"
    "Habit loops—composed of a cue, routine, and reward—can transform your newsletter. "
    "Here is some raw text that needs clarity.\n"
)

@patch("src.agents.editor_in_chief.get_groq_client")
def test_edit_draft_success(mock_get_client):
    mock_client = MagicMock()
    mock_get_client.return_value = mock_client
    polished_content = (
        "<!-- COVER_IMAGE_HOOK -->\n"
        "# Building Habit Loops\n\n"
        "Habit loops—composed of a cue, routine, and reward—can transform your newsletter.\n"
        ">> COMMENT: Consider simplifying this sentence.\n\n"
        "## Revision Summary\n"
        "- Improved clarity in opening paragraph\n"
        "- Added inline comment"
    )
    mock_response = MagicMock()
    mock_response.choices = [MagicMock(message=MagicMock(content=polished_content))]
    mock_client.chat.completions.create.return_value = mock_response

    editor = EditorInChief()
    polished, summary = editor.edit_draft(DUMMY_DRAFT)
    assert ">> COMMENT:" in polished
    assert summary.startswith("## Revision Summary")

@patch("src.agents.editor_in_chief.get_groq_client")
def test_edit_draft_empty_input(mock_get_client):
    editor = EditorInChief()
    with pytest.raises(ValueError):
        editor.edit_draft("")

@patch("src.agents.editor_in_chief.get_groq_client")
def test_edit_draft_api_error(mock_get_client):
    mock_client = MagicMock()
    mock_client.chat.completions.create.side_effect = Exception("Timeout")
    mock_get_client.return_value = mock_client

    editor = EditorInChief()
    with pytest.raises(RuntimeError) as exc:
        editor.edit_draft(DUMMY_DRAFT)
    assert "Groq API call failed" in str(exc.value)
