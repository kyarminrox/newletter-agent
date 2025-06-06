# Newsletter Agent

This repository contains a prototype for an AI-powered Substack newsletter pipeline. The first implemented component is the **Data Collector** agent, which ingests metrics CSV files and past Markdown issues.

## Setup

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Set your `GROQ_API_KEY` in a `.env` file at the project root:

```dotenv
GROQ_API_KEY=your-api-key
```

3. Run tests:

```bash
pytest
```

### Insight Scout (Research Brief)

After ingesting metrics, you can create a research brief that mixes pain-point analysis with a live search.

```python
from src.agents.insight_scout import InsightScout

scout = InsightScout()
md = scout.fetch_research_brief(
    "./data/metrics/metrics_2025-06-01.csv",
    "habit loops email marketing",
)
print(md)
```

### API & Frontend: Generate Research Brief

1. **Run the FastAPI server**:
   ```bash
   uvicorn src.api:app --reload
   ```
   The server listens on `http://127.0.0.1:8000`.

2. **Open the frontend page**:
   Open `frontend/generate-research.html` in your browser (e.g., via `file://` URL).

3. **Fill the form**:
   - *Metrics CSV Path*: relative path to your CSV, e.g. `data/metrics/metrics_2025-06-01.csv`.
   - *Search Query*: your research query.

4. Click **Generate Research** to produce a Markdown brief. The output appears in the page.

```example
## Pain Points
- **2025-05-15**: only 3.82 replies per 1k subscribers (ReplyCount=38, Subscribers=9950)

## Trending Articles
- How Habit Loops Drive Email Engagement (https://example.com/habit-loops-2025)
- The Science of Habit Formation in Newsletters (https://news.example.org/habit-science)
```

### Outline Architect (Generate Outlines)

1. **Ensure you have a Research Brief** from Insight Scout and an Issue Brief.
2. **Run the FastAPI server** if it's not already running:
   ```bash
   uvicorn src.api:app --reload
   ```
3. **Open the frontend page**:
   `frontend/generate-outlines.html` (via `file://` URL).
4. Paste the Research Brief Markdown into the first textarea and enter your Issue Brief text.
5. Click **Generate Outlines**. The page will display three Markdown outlines, each beginning with `# Outline Option`.
