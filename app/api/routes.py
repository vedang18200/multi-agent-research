# app/api/routes.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.graph.pipeline import pipeline

router = APIRouter()

class ResearchRequest(BaseModel):
    query: str

class ResearchResponse(BaseModel):
    report: str
    sources: list
    confidence_score: float
    subtasks: list

@router.post("/research", response_model=ResearchResponse)
async def run_research(req: ResearchRequest):
    if not req.query.strip():
        raise HTTPException(status_code=400, detail="Query cannot be empty")

    initial_state = {
        "query": req.query,
        "subtasks": [],
        "search_results": [],
        "draft_report": "",
        "verified_report": "",
        "sources": [],
        "confidence_score": 0.0,
        "retry_count": 0,
        "error": None
    }

    result = pipeline.invoke(initial_state)

    return ResearchResponse(
        report=result["verified_report"],
        sources=result["sources"],
        confidence_score=result["confidence_score"],
        subtasks=result["subtasks"]
    )
