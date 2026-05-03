from typing import TypedDict, List, Optional

class ResearchState(TypedDict):
    query: str
    subtasks: List[str]
    search_results: List[dict]
    draft_report: str
    verified_report: str
    sources: List[str]
    confidence_score: float
    retry_count: int
    error: Optional[str]
