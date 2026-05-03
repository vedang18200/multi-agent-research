# app/graph/pipeline.py
from langgraph.graph import StateGraph, END
from app.graph.state import ResearchState
from app.agents.supervisor import supervisor_node
from app.agents.planner import planner_node
from app.agents.researcher import researcher_node
from app.agents.writer import writer_node
from app.agents.verifier import verifier_node
from app.config import MAX_RETRIES

def should_retry(state: ResearchState) -> str:
    if state["confidence_score"] < 0.75 and state["retry_count"] < MAX_RETRIES:
        return "retry"
    return "done"

def build_graph():
    graph = StateGraph(ResearchState)

    graph.add_node("supervisor", supervisor_node)
    graph.add_node("planner", planner_node)
    graph.add_node("researcher", researcher_node)
    graph.add_node("writer", writer_node)
    graph.add_node("verifier", verifier_node)

    graph.set_entry_point("supervisor")
    graph.add_edge("supervisor", "planner")
    graph.add_edge("planner", "researcher")
    graph.add_edge("researcher", "writer")
    graph.add_edge("writer", "verifier")

    graph.add_conditional_edges(
        "verifier",
        should_retry,
        {
            "retry": "researcher",   # re-search with same subtasks
            "done": END
        }
    )

    return graph.compile()

pipeline = build_graph()
