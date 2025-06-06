from groq import Groq
import re
from src.utils import get_groq_client

class EditorInChief:
    """Polish a draft with inline comments and summary using Groq."""

    def __init__(self):
        self.client = get_groq_client()

    def edit_draft(self, draft_md: str) -> tuple[str, str]:
        """Return polished markdown and revision summary."""
        if not draft_md.strip():
            raise ValueError("Draft Markdown cannot be empty.")

        prompt = (
            "You are a meticulous editor. Polish the following draft:\n\n"
            f"{draft_md}\n\n"
            "- Improve clarity and flow.\n"
            "- Enforce a minimal, direct brand voice.\n"
            "- Insert inline comments prefaced by \">> COMMENT:\" where suggestions apply.\n"
            "- At the end, include a \"## Revision Summary\" section that lists major changes.\n\n"
            "Output the entire result as Markdown."
        )

        try:
            response = self.client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[
                    {"role": "system", "content": "You are an expert editor."},
                    {"role": "user", "content": prompt},
                ],
            )
        except Exception as exc:
            raise RuntimeError(f"Groq API call failed: {exc}")

        edited_md = response.choices[0].message.content

        match = re.search(r"## Revision Summary", edited_md, re.IGNORECASE)
        if match:
            idx = match.start()
            polished = edited_md[:idx].rstrip()
            summary = edited_md[idx:].strip()
        else:
            polished = edited_md
            summary = ""

        return polished, summary
