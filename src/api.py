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
