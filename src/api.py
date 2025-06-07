import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from src.agents.insight_scout import InsightScout

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