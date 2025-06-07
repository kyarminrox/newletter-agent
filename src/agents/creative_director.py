from groq import Groq
from src.utils import get_groq_client


class CreativeDirector:
    """Generate cover image concepts from a draft excerpt using Groq."""

    def __init__(self):
        self.client = get_groq_client()

    def suggest_visuals(self, draft_excerpt: str) -> str:
        """Return plain-text visual prompts for the provided excerpt."""
        if not draft_excerpt.strip():
            raise ValueError("Draft excerpt cannot be empty.")

        excerpt = draft_excerpt.strip()
        if len(excerpt) > 1500:
            excerpt = excerpt[:1500] + "\u2026"

        prompt = (
            "You are a creative director specialized in minimal design. "
            "Given these first paragraphs:\n\n"
            f"{excerpt}\n\n"
            "Suggest 3 cover image concepts in plain text. For each concept, provide:\n"
            "- A brief description (e.g., \"Charcoal background, yellow barbell vs. gloves\").\n"
            "- A text-to-image prompt string suitable for DALL·E or Stable Diffusion.\n\n"
            "Format as plain text, one concept per line, with description and prompt separated by a tab."
        )

        try:
            response = self.client.chat.completions.create(
                model="compound-beta-mini",
                messages=[
                    {"role": "system", "content": "You are a creative director."},
                    {"role": "user", "content": prompt},
                ],
            )
        except Exception as e:
            raise RuntimeError(f"Groq API call failed: {e}")

        return response.choices[0].message.content
