import os
import pandas as pd

from ..utils import get_groq_client


class InsightScout:
    """Combine metrics analysis with Groq compound-beta search."""

    def __init__(self):
        self.client = get_groq_client()

    def _extract_pain_points(self, df: pd.DataFrame, top_n: int = 3) -> list[str]:
        """Return a list of pain point strings based on reply engagement."""
        df = df.copy()
        df["RepliesPerK"] = df["ReplyCount"] / (df["Subscribers"] / 1000)
        df_sorted = df.sort_values("RepliesPerK", ascending=True).head(top_n)
        points = []
        for _, row in df_sorted.iterrows():
            date_str = row["IssueDate"].strftime("%Y-%m-%d")
            rp = round(row["RepliesPerK"], 2)
            points.append(
                f"- **{date_str}**: only {rp} replies per 1k subscribers "
                f"(ReplyCount={row['ReplyCount']}, Subscribers={row['Subscribers']})"
            )
        return points

    def fetch_research_brief(self, csv_path: str, query: str) -> str:
        """Return Markdown brief of pain points plus trending articles."""
        if not os.path.isfile(csv_path):
            raise FileNotFoundError(f"Metrics CSV not found at {csv_path}")

        df = pd.read_csv(csv_path)
        required = {"IssueDate", "SubjectLine", "OpenRate", "ClickRate", "ReplyCount", "Subscribers"}
        missing = required - set(df.columns)
        if missing:
            raise ValueError(f"Metrics CSV is missing required columns: {missing}")

        df["IssueDate"] = pd.to_datetime(df["IssueDate"], format="%Y-%m-%d")
        pain_points = self._extract_pain_points(df, top_n=3)
        pain_markdown = "## Pain Points\n" + "\n".join(pain_points)

        recent = df.sort_values("IssueDate", ascending=False).head(3)
        metrics_excerpt = "\n".join(
            f"{row.IssueDate.strftime('%Y-%m-%d')}, {row.OpenRate}%, {row.ClickRate}%, {row.ReplyCount} replies, {row.Subscribers} subs"
            for _, row in recent.iterrows()
        )

        prompt = (
            "You are a data-driven newsletter researcher.\n"
            "Here are the 3 most recent issues (Date, OpenRate%, ClickRate%, ReplyCount, Subscribers):\n\n"
            f"{metrics_excerpt}\n\n"
            f"(1) Based on these numbers, briefly summarize the top 3 reader pain points under '## Pain Points'.\n"
            f"(2) Perform a web search for \"{query}\" and list 3 recent article headlines + URLs under '## Trending Articles'.\n"
            "(3) Format the entire response as Markdown, with the two sections '## Pain Points' and '## Trending Articles'."
        )

        try:
            response = self.client.chat.completions.create(
                model="compound-beta",
                messages=[
                    {"role": "system", "content": "You are an expert research assistant."},
                    {"role": "user", "content": prompt},
                ],
            )
        except Exception as exc:
            raise RuntimeError(f"Groq API call failed: {exc}")

        content = response.choices[0].message.content
        if "## Pain Points" not in content:
            content = pain_markdown + "\n\n" + content
        return content
