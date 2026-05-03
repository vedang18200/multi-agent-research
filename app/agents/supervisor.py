# app/agents/supervisor.py
from app.graph.state import ResearchState

def supervisor_node(state: ResearchState) -> ResearchState:
    # Just initialises routing — LangGraph handles flow
    return {**state, "retry_count": state.get("retry_count", 0)}
