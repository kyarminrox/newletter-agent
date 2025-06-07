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

### Draftsmith (Create Draft from Outline)

1. **Ensure you have a chosen Outline** (Markdown) from Outline Architect.
2. **Run the FastAPI server** if it's not already running:
   ```bash
   uvicorn src.api:app --reload
   ```
3. **Open the frontend page**:
   `frontend/generate-draft.html` (via `file://` URL).
4. Paste one of the `# Outline Option` blocks into the textarea.
5. Click **Create Draft**.
   The page displays a full Markdown draft beginning with `<!-- COVER_IMAGE_HOOK -->`.

### Editor-in-Chief (Polish Draft)

1. **Ensure you have a full draft** (Markdown) from Draftsmith or uploaded.
2. **Run the FastAPI server** if it's not already running:
   ```bash
   uvicorn src.api:app --reload
   ```
3. **Open the frontend page**:
   `frontend/generate-edit.html` (via `file://` URL).
4. Paste the entire draft Markdown into the textarea.
5. Click **Edit Draft**.
   The page shows the polished Markdown and a revision summary under the respective headings.

### Creative Director (Suggest Visuals)

1. **Ensure you have a polished draft excerpt** from Editor-in-Chief.
2. **Run the FastAPI server** if it's not already running:
   ```bash
   uvicorn src.api:app --reload
   ```
3. **Open the frontend page**:
   `frontend/generate-visuals.html` (via `file://` URL).
4. Paste the first few paragraphs of your polished draft into the textarea.
5. Click **Suggest Visuals**. The page shows three lines, each containing a description and a text-to-image prompt separated by a tab.

### Metrics Forecaster (Forecast Performance)

1. **Ensure you have a metrics CSV** with at least 3 past issues (columns: `IssueDate`, `SubjectLine`, `OpenRate`).
2. **Run the FastAPI server** if it's not already running:
   ```bash
   uvicorn src.api:app --reload
   ```
3. **Open the frontend page**:
   `frontend/generate-forecast.html` (via `file://` URL).
4. In the *Metrics CSV Path* field, enter the relative path, e.g. `data/metrics/metrics_2025-06-01.csv`.
5. In *Subject Lines*, enter each candidate subject line on its own line.
6. Click **Forecast Performance**. The page displays a Markdown forecast. If too little history exists, a stub forecast explains the default assumptions.

### Formatter (Package for Substack)

1. **Ensure you have:**
   - A final draft Markdown file (e.g., `data/final/FinalIssue_2025-06-15.md`).
   - A cover image (PNG or JPG), e.g., `assets/cover_2025-06-15.png`.
2. **Run the FastAPI server** if not already running:
   ```bash
   uvicorn src.api:app --reload
   ```
3. **Open the frontend page**:
   `frontend/generate-package.html` (via `file://` URL).
4. Fill in all fields: draft path, cover path, title, slug, comma-separated tags, and publish datetime (ISO 8601).
5. Click **Package for Substack**. A download link appears for the generated ZIP, e.g., `package/2025-06-15.zip`.
   Inside the ZIP:
   - `2025-06-15/Issue.md` (with `![Cover](images/cover.png)` at the top)
   - `2025-06-15/images/cover.png`
   - `2025-06-15/metadata.json`


### Performance Analysis (Lessons Learned)

1. **Ensure you have:**
   - A forecast Markdown report from `/api/forecast-performance`.
   - A post-send metrics CSV with columns `IssueDate`, `OpenRate`, `ClickRate`.
2. **Run the FastAPI server**:
   ```bash
   uvicorn src.api:app --reload
   ```
3. **Open** `frontend/generate-analysis.html` in your browser.
4. Paste the forecast Markdown and enter the CSV path.
5. Click **Analyze Performance** to generate a Markdown summary under `## Lessons Learned`.

### Run Full Pipeline

Open `frontend/run-pipeline.html` and fill all fields to run the entire pipeline via `/api/run-pipeline`. The output shows the path to the generated package ZIP.