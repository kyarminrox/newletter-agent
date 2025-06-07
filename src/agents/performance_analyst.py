import os
import pandas as pd
from groq import Groq
from src.utils import get_groq_client


class PerformanceAnalyst:
    """Compare forecast with actual metrics and summarize lessons learned."""

    def __init__(self):
        self.client = get_groq_client()

    def analyze(self, forecast_md: str, actuals_csv_path: str) -> str:
        """Return a Markdown lessons-learned report."""
        if not forecast_md.strip():
            raise ValueError("Forecast Markdown cannot be empty.")
        if not os.path.isfile(actuals_csv_path):
            raise FileNotFoundError(f"Actuals CSV not found at {actuals_csv_path}")

        df = pd.read_csv(actuals_csv_path)
        required = {"IssueDate", "OpenRate", "ClickRate"}
        missing = required - set(df.columns)
        if missing:
            raise ValueError(f"Actuals CSV missing columns: {missing}")

        df["IssueDate"] = pd.to_datetime(df["IssueDate"], format="%Y-%m-%d")
        df = df.sort_values("IssueDate", ascending=False)
        rows = df.head(5).to_dict(orient="records")
        actuals_lines = "\n".join(
            f"- {r['IssueDate'].strftime('%Y-%m-%d')}: OpenRate={r['OpenRate']}%, ClickRate={r['ClickRate']}%"
            for r in rows
        )

        prompt = (
            "You are a performance analyst. Here is the forecast:\n\n"
            f"{forecast_md}\n\n"
            "And here are the actual post-send metrics (Date: OpenRate%, ClickRate%):\n"
            f"{actuals_lines}\n\n"
            "Compare predicted vs. actual. Under '## Lessons Learned', list 3 bullet points noting accuracy, discrepancies, and recommendations. Output as Markdown."
        )

        try:
            resp = self.client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": "You are a data-driven performance analyst."},
                    {"role": "user", "content": prompt},
                ],
            )
        except Exception as exc:
            raise RuntimeError(f"Groq API call failed: {exc}")

        return resp.choices[0].message.content
