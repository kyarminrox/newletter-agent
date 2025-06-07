# Newsletter Agent

This repository contains a prototype for an AI-powered Substack newsletter pipeline. The first implemented component is the **Data Collector** agent, which ingests metrics CSV files and past Markdown issues.

## Setup

1. Install dependencies:

   ```bash
   pip install -r requirements.txt
Set your GROQ_API_KEY in a .env file at the project root:

dotenv
Copy
Edit
GROQ_API_KEY=your-api-key
Run tests:

bash
Copy
Edit
pytest
Insight Scout (Research Brief)
After ingesting metrics, you can create a research brief that mixes pain-point analysis with a live search:

python
Copy
Edit
from src.agents.insight_scout import InsightScout

scout = InsightScout()
md = scout.fetch_research_brief(
    "./data/metrics/metrics_2025-06-01.csv",
    "habit loops email marketing",
)
print(md)
API & Frontend: Generate Research Brief
Run the FastAPI server:

bash
Copy
Edit
uvicorn src.api:app --reload
Open frontend/generate-research.html (via file:// URL).

Fill the form:

Metrics CSV Path: e.g. data/metrics/metrics_2025-06-01.csv

Search Query: your research query

Click Generate Research.

markdown
Copy
Edit
## Pain Points
- **2025-05-15**: only 3.82 replies per 1k subscribers (ReplyCount=38, Subscribers=9950)

## Trending Articles
- How Habit Loops Drive Email Engagement (https://example.com/habit-loops-2025)
- The Science of Habit Formation in Newsletters (https://news.example.org/habit-science)
Outline Architect (Generate Outlines)
Ensure you have a Research Brief and an Issue Brief.

Run uvicorn src.api:app --reload.

Open frontend/generate-outlines.html.

Paste the Research Brief into the first textarea and enter your Issue Brief.

Click Generate Outlines.

Draftsmith (Create Draft from Outline)
Choose an Outline from the previous step.

Run uvicorn src.api:app --reload.

Open frontend/generate-draft.html.

Paste the outline (one # Outline Option … block) into the textarea.

Click Create Draft.

Editor-in-Chief (Polish Draft)
Take the full draft from Draftsmith.

Run uvicorn src.api:app --reload.

Open frontend/generate-edit.html.

Paste the draft into the textarea.

Click Edit Draft.

Creative Director (Suggest Visuals)
Use a polished excerpt from Editor-in-Chief.

Run uvicorn src.api:app --reload.

Open frontend/generate-visuals.html.

Paste the excerpt into the textarea.

Click Suggest Visuals.

Metrics Forecaster (Forecast Performance)
Have a metrics CSV (≥3 issues with IssueDate, SubjectLine, OpenRate).

Run uvicorn src.api:app --reload.

Open frontend/generate-forecast.html.

Enter the CSV path and subject lines (one per line).

Click Forecast Performance.

Formatter (Package for Substack)
Prepare:

Final draft Markdown (e.g. data/final/FinalIssue_2025-06-15.md)

Cover image (e.g. assets/cover_2025-06-15.png)

Run uvicorn src.api:app --reload.

Open frontend/generate-package.html.

Fill in all fields (paths, title, slug, tags, publish date).

Click Package for Substack.

Download the ZIP (e.g. package/2025-06-15.zip) which contains:

2025-06-15/Issue.md

2025-06-15/images/cover.png

2025-06-15/metadata.json

Performance Analysis (Lessons Learned)
Have:

Forecast Markdown (from /api/forecast-performance)

Post-send metrics CSV (IssueDate, OpenRate, ClickRate)

Run uvicorn src.api:app --reload.

Open frontend/generate-analysis.html.

Paste the forecast and enter the CSV path.

Click Analyze Performance.

Example output:

markdown
Copy
Edit
## Lessons Learned
- Forecast open rates were within 1% of actuals, showing strong model accuracy.
- Click-throughs underperformed; consider testing stronger CTAs.
- Segment by engagement score for better targeting in future sends.
arduino
Copy
Edit

After pasting this, remove the conflict markers and run:

```bash
git add README.md
git commit