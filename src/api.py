import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from src.agents.insight_scout import InsightScout
from src.orchestrator import run_pipeline

app = FastAPI(title="Newsletter Agent API")


class ResearchRequest(BaseModel):
    csv_path: str
    query: str


class ResearchResponse(BaseModel):
    research_brief: str


@app.post("/api/generate-research", response_model=ResearchResponse)
async def generate_research(req: ResearchRequest):
    """Generate a research brief from metrics CSV and search query."""
    scout = InsightScout()
    try:
        brief = scout.fetch_research_brief(req.csv_path, req.query)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Metrics CSV not found.")
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except RuntimeError as re:
        raise HTTPException(status_code=502, detail=str(re))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {e}")

    return ResearchResponse(research_brief=brief)


@app.get("/api/health")
async def health_check():
    return {"status": "ok"}

from src.agents.outline_architect import OutlineArchitect

class OutlineRequest(BaseModel):
    research_brief: str
    issue_brief: str

class OutlineResponse(BaseModel):
    outlines_markdown: str

@app.post("/api/generate-outlines", response_model=OutlineResponse)
async def generate_outlines(req: OutlineRequest):
    """Generate newsletter outlines from research and issue briefs."""
    architect = OutlineArchitect()
    try:
        md = architect.generate_outlines(req.research_brief, req.issue_brief)
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except RuntimeError as re:
        raise HTTPException(status_code=502, detail=str(re))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {e}")

    return OutlineResponse(outlines_markdown=md)

from src.agents.draftsmith import Draftsmith

class DraftRequest(BaseModel):
    outline_markdown: str

class DraftResponse(BaseModel):
    draft_markdown: str

@app.post("/api/create-draft", response_model=DraftResponse)
async def create_draft(req: DraftRequest):
    """Expand an outline into a full newsletter draft."""
    smith = Draftsmith()
    try:
        draft_md = smith.create_draft(req.outline_markdown)
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except RuntimeError as re:
        raise HTTPException(status_code=502, detail=str(re))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {e}")

    return DraftResponse(draft_markdown=draft_md)

from src.agents.editor_in_chief import EditorInChief

class EditRequest(BaseModel):
    draft_markdown: str

class EditResponse(BaseModel):
    polished_markdown: str
    revision_summary: str

@app.post("/api/edit-draft", response_model=EditResponse)
async def edit_draft(req: EditRequest):
    """Polish a draft and return polished content plus revision summary."""
    editor = EditorInChief()
    try:
        polished, summary = editor.edit_draft(req.draft_markdown)
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except RuntimeError as re:
        raise HTTPException(status_code=502, detail=str(re))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {e}")

    return EditResponse(polished_markdown=polished, revision_summary=summary)

from src.agents.creative_director import CreativeDirector

class VisualRequest(BaseModel):
    draft_excerpt: str

class VisualResponse(BaseModel):
    visual_prompts: str

@app.post("/api/suggest-visuals", response_model=VisualResponse)
async def suggest_visuals(req: VisualRequest):
    """Generate cover image concepts from a draft excerpt."""
    director = CreativeDirector()
    try:
        prompts = director.suggest_visuals(req.draft_excerpt)
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except RuntimeError as re:
        raise HTTPException(status_code=502, detail=str(re))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {e}")

    return VisualResponse(visual_prompts=prompts)

from typing import List
from src.agents.metrics_forecaster import MetricsForecaster

class ForecastRequest(BaseModel):
    csv_path: str
    subject_lines: List[str]

class ForecastResponse(BaseModel):
    forecast_markdown: str

@app.post("/api/forecast-performance", response_model=ForecastResponse)
async def forecast_performance(req: ForecastRequest):
    """Generate a performance forecast from metrics CSV and subject lines."""
    forecaster = MetricsForecaster()
    try:
        md = forecaster.forecast(req.csv_path, req.subject_lines)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Metrics CSV not found.")
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except RuntimeError as re:
        raise HTTPException(status_code=502, detail=str(re))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {e}")

    return ForecastResponse(forecast_markdown=md)

from typing import List
from src.agents.formatter import Formatter

class PackageRequest(BaseModel):
    draft_path: str
    cover_image_path: str
    title: str
    slug: str
    tags: List[str]
    publish_date: str

class PackageResponse(BaseModel):
    package_zip_path: str

@app.post("/api/package-for-substack", response_model=PackageResponse)
async def package_for_substack(req: PackageRequest):
    """Package final draft and assets into a Substack-ready ZIP."""
    fmt = Formatter()
    try:
        zip_path = fmt.package_for_substack(
            draft_path=req.draft_path,
            cover_image_path=req.cover_image_path,
            title=req.title,
            slug=req.slug,
            tags=req.tags,
            publish_date=req.publish_date,
        )
    except FileNotFoundError as fnf:
        raise HTTPException(status_code=404, detail=str(fnf))
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except RuntimeError as re:
        raise HTTPException(status_code=500, detail=str(re))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {e}")

    return PackageResponse(package_zip_path=zip_path)

from src.agents.performance_analyst import PerformanceAnalyst


class AnalyzeRequest(BaseModel):
    forecast_markdown: str
    actuals_csv_path: str


class AnalyzeResponse(BaseModel):
    analysis_markdown: str


@app.post("/api/analyze-performance", response_model=AnalyzeResponse)
async def analyze_performance(req: AnalyzeRequest):
    """Compare forecast vs. actual metrics and return lessons learned."""
    analyst = PerformanceAnalyst()
    try:
        md = analyst.analyze(req.forecast_markdown, req.actuals_csv_path)
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except FileNotFoundError as fnf:
        raise HTTPException(status_code=404, detail=str(fnf))
    except RuntimeError as re:
        raise HTTPException(status_code=502, detail=str(re))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {e}")

    return AnalyzeResponse(analysis_markdown=md)

class PipelineRequest(BaseModel):
    metrics_csv: str
    research_query: str
    issue_brief: str
    cover_image: str
    title: str
    slug: str
    tags: List[str]
    publish_date: str


class PipelineResponse(BaseModel):
    package_zip_path: str


@app.post("/api/run-pipeline", response_model=PipelineResponse)
async def run_pipeline_api(req: PipelineRequest):
    """Run the full newsletter pipeline and return the package ZIP path."""
    try:
        zip_path = run_pipeline(
            metrics_csv=req.metrics_csv,
            research_query=req.research_query,
            issue_brief=req.issue_brief,
            cover_image=req.cover_image,
            title=req.title,
            slug=req.slug,
            tags=req.tags,
            publish_date=req.publish_date,
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Pipeline error: {e}")
    return PipelineResponse(package_zip_path=zip_path)
