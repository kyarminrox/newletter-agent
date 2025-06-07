from groq import Groq
from src.utils import get_groq_client

class OutlineArchitect:
    """Generate newsletter outlines from research and issue briefs using Groq."""

    def __init__(self):
        self.client = get_groq_client()

    def generate_outlines(self, research_brief: str, issue_brief: str) -> str:
        """Return Markdown outlines. Raises ValueError on empty input."""
        if not research_brief.strip():
            raise ValueError("Research brief cannot be empty.")
        if not issue_brief.strip():
            raise ValueError("Issue brief cannot be empty.")

        prompt = (
            "You are a professional newsletter strategist.\n\n"
            f"Research Brief:\n{research_brief}\n\n"
            f"Issue Brief: \"{issue_brief}\"\n\n"
            "Generate 3 distinct outlines. Each outline must include:\n"
            "- A heading `# Outline Option N` (where N is 1, 2, or 3).\n"
            "- 3\u20135 section headers with 1\u20132 sentence descriptions.\n"
            "- 3 candidate subject lines under a subheading `## Subject Line Candidates`.\n\n"
            "Format the entire response in Markdown."
        )

        try:
            response = self.client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": "You are a newsletter outline expert."},
                    {"role": "user", "content": prompt},
                ],
            )
        except Exception as exc:
            raise RuntimeError(f"Groq API call failed: {exc}")

        outlines_md = response.choices[0].message.content
        return outlines_md
