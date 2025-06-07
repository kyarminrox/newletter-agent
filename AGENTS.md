# Agents Overview

This document summarizes the agents in the newsletter pipeline. Each section describes the agent's role, inputs, outputs, and example usage.

## Table of Contents
- [DataCollector](#datacollector)
- [InsightScout](#insightscout)
- [OutlineArchitect](#outlinearchitect)
- [Draftsmith](#draftsmith)
- [EditorInChief](#editorinchief)
- [CreativeDirector](#creativedirector)
- [MetricsForecaster](#metricsforecaster)
- [Formatter](#formatter)
- [PerformanceAnalyst](#performanceanalyst)

## DataCollector
**Purpose**: Parse metrics CSV files and load past Markdown issues.

### Inputs
- `ingest_metrics(csv_path: str)` – path to a metrics CSV.
- `ingest_content(markdown_dir: str)` – directory containing `.md` files.

### Outputs
- `ingest_metrics` returns a `pandas.DataFrame` sorted by `IssueDate`.
- `ingest_content` returns a list of dictionaries with `path`, `content`, and `metadata`.

### Example
```python
from src.agents.data_collector import ingest_metrics, ingest_content

metrics_df = ingest_metrics("data/metrics/metrics_2025-06-01.csv")
all_docs = ingest_content("data/content")
```

## InsightScout
**Purpose**: Combine metrics analysis with Groq `compound-beta` search to produce a research brief.

### Inputs
- POST `/api/generate-research` with JSON body:
  - `csv_path`: path to metrics CSV
  - `query`: search query string

### Outputs
- JSON `{ "research_brief": "...markdown..." }`

### Example
```python
from src.agents.insight_scout import InsightScout

scout = InsightScout()
brief_md = scout.fetch_research_brief("data/metrics/metrics_2025-06-01.csv", "habit loops")
```

## OutlineArchitect
**Purpose**: Generate multiple newsletter outlines from a research brief and issue brief.

### Inputs
- POST `/api/generate-outlines` with JSON body:
  - `research_brief`: Markdown text
  - `issue_brief`: short description

### Outputs
- JSON `{ "outlines_markdown": "...markdown..." }`

### Example
```python
from src.agents.outline_architect import OutlineArchitect

arch = OutlineArchitect()
outlines = arch.generate_outlines(research_md, "Topic: Habit Loops")
```

## Draftsmith
**Purpose**: Expand an outline into a full newsletter draft (includes `<!-- COVER_IMAGE_HOOK -->`).

### Inputs
- POST `/api/create-draft` with JSON body:
  - `outline_markdown`: chosen outline in Markdown

### Outputs
- JSON `{ "draft_markdown": "...markdown..." }`

### Example
```python
from src.agents.draftsmith import Draftsmith

smith = Draftsmith()
draft = smith.create_draft(outline_md)
```

## EditorInChief
**Purpose**: Polish a draft, inserting inline comments and a revision summary.

### Inputs
- POST `/api/edit-draft` with JSON body:
  - `draft_markdown`: raw draft Markdown

### Outputs
- JSON with fields:
  - `polished_markdown`
  - `revision_summary`

### Example
```python
from src.agents.editor_in_chief import EditorInChief

editor = EditorInChief()
polished, summary = editor.edit_draft(draft_md)
```

## CreativeDirector
**Purpose**: Suggest cover image concepts from a draft excerpt.

### Inputs
- POST `/api/suggest-visuals` with JSON body:
  - `draft_excerpt`: first paragraphs of the polished draft

### Outputs
- JSON `{ "visual_prompts": "description\tprompt" }`

### Example
```python
from src.agents.creative_director import CreativeDirector

director = CreativeDirector()
ideas = director.suggest_visuals(polished_md[:500])
```

## MetricsForecaster
**Purpose**: Predict open rates and send-time recommendations for subject lines.

### Inputs
- POST `/api/forecast-performance` with JSON body:
  - `csv_path`: historical metrics CSV
  - `subject_lines`: list of candidate subject lines

### Outputs
- JSON `{ "forecast_markdown": "...markdown..." }`

### Example
```python
from src.agents.metrics_forecaster import MetricsForecaster

forecaster = MetricsForecaster()
report = forecaster.forecast("data/metrics/metrics_2025-06-01.csv", ["A", "B"])
```

## Formatter
**Purpose**: Package a final draft, cover image, and metadata into a dated ZIP for Substack upload.

### Inputs
- POST `/api/package-for-substack` with JSON body:
  - `draft_path`: path to polished draft
  - `cover_image_path`: path to cover image file
  - `title`: article title
  - `slug`: URL slug
  - `tags`: list of tags
  - `publish_date`: ISO 8601 datetime

### Outputs
- JSON `{ "package_zip_path": "package/YYYY-MM-DD.zip" }`

### Example
```python
from src.agents.formatter import Formatter

fmt = Formatter()
zip_path = fmt.package_for_substack(
    "data/final/FinalIssue.md",
    "assets/cover.png",
    "My Title",
    "my-title",
    ["email", "marketing"],
    "2025-07-01T09:00:00+03:00",
)
```

## PerformanceAnalyst
**Purpose**: Compare forecasted metrics with actual results and summarize lessons learned.

### Inputs
- POST `/api/analyze-performance` with JSON body:
  - `forecast_markdown`: Markdown forecast report
  - `actuals_csv_path`: CSV file with post-send metrics

### Outputs
- JSON `{ "analysis_markdown": "...markdown..." }`

### Example
```python
from src.agents.performance_analyst import PerformanceAnalyst

analyst = PerformanceAnalyst()
lessons = analyst.analyze(forecast_md, "data/metrics/post_send.csv")
```
