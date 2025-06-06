import os
from typing import List
import pandas as pd

from src.utils import get_groq_client


class MetricsForecaster:
    """Forecast open rates for candidate subject lines based on past metrics."""

    def __init__(self):
        self.client = get_groq_client()

    def forecast(self, csv_path: str, subject_lines: List[str]) -> str:
        """Return a Markdown forecast report given a metrics CSV and subjects."""
        if not subject_lines or not any(s.strip() for s in subject_lines):
            raise ValueError("At least one subject line is required.")

        if not os.path.isfile(csv_path):
            raise FileNotFoundError(f"Metrics CSV not found at {csv_path}")

        df = pd.read_csv(csv_path)
        required_cols = {"IssueDate", "SubjectLine", "OpenRate"}
        missing = required_cols - set(df.columns)
        if missing:
            raise ValueError(f"Metrics CSV is missing required columns: {missing}")

        df["IssueDate"] = pd.to_datetime(df["IssueDate"], format="%Y-%m-%d")
        df_sorted = df.sort_values("IssueDate", ascending=False).reset_index(drop=True)
        recent = df_sorted.head(5)

        hist_lines = [
            f"- {row.IssueDate.strftime('%Y-%m-%d')}: \"{row.SubjectLine}\" \u2192 {row.OpenRate}%"
            for _, row in recent.iterrows()
        ]
        hist_markdown = "\n".join(hist_lines)

        if len(recent) < 3:
            stub = (
                "## Stub Forecast\n"
                "Insufficient historical data (fewer than 3 issues). Using generic benchmark:\n\n"
                "- Subject Lines to test:\n"
            )
            for s in subject_lines:
                stub += f"  - \"{s}\": Predicted open rate = ~15%\n"
            stub += (
                "\n- Recommended send date/time: Next weekday at 09:00 UTC+3\n"
                "- Suggested segmentation: Top 20% most engaged subscribers as a test group.\n"
            )
            return stub

        subj_md = "\n".join(f'- "{s}"' for s in subject_lines)
        prompt = (
            f"You are a data analyst. Here are the last {len(recent)} issues (Date: Subject \u2192 OpenRate%):\n"
            f"{hist_markdown}\n\n"
            f"Predict an open rate for each of these candidate subject lines:\n{subj_md}\n\n"
            "Also recommend an optimal send date/time (weekday at 09:00 UTC+3) "
            "and a segmentation strategy for the top 20% engaged subscribers. "
            "Format your response in Markdown."
        )

        try:
            response = self.client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[
                    {"role": "system", "content": "You are a forecasting expert."},
                    {"role": "user", "content": prompt},
                ],
            )
        except Exception as e:
            raise RuntimeError(f"Groq API call failed: {e}")

        return response.choices[0].message.content
