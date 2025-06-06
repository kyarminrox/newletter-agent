from groq import Groq
from src.utils import get_groq_client

class Draftsmith:
    """Generate a newsletter draft from an outline using Groq."""

    def __init__(self):
        self.client = get_groq_client()

    def create_draft(self, outline_md: str) -> str:
        """Return a Markdown draft. Raises ValueError on empty outline."""
        if not outline_md.strip():
            raise ValueError("Outline Markdown cannot be empty.")

        prompt = (
            "You are an expert newsletter writer. Using this outline:\n\n"
            f"{outline_md}\n\n"
            "Write a 1,200-word draft in a minimal, direct tone. "
            "Insert a cover image placeholder <!-- COVER_IMAGE_HOOK --> at the top.\n"
            "Include any relevant data points or examples from the outline. "
            "Output the result as Markdown."
        )

        try:
            response = self.client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": "You are a skilled newsletter writer."},
                    {"role": "user", "content": prompt},
                ],
            )
        except Exception as exc:
            raise RuntimeError(f"Groq API call failed: {exc}")

        return response.choices[0].message.content
