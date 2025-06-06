import os
from groq import Groq


def get_groq_client() -> Groq:
    """Return a Groq client using the API key from environment."""
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise RuntimeError("GROQ_API_KEY not set in environment")
    return Groq(api_key=api_key)
