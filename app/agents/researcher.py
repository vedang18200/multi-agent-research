# app/agents/researcher.py
from langchain_groq import ChatGroq
from app.config import GROQ_API_KEY, MODEL_NAME
from app.graph.state import ResearchState
from app.tools.search import get_search_tool

llm = ChatGroq(api_key=GROQ_API_KEY, model=MODEL_NAME)
search = get_search_tool()

def researcher_node(state: ResearchState) -> ResearchState:
    results = []
    sources = []

    for task in state["subtasks"]:
        raw = search.run(task)
        results.append({"task": task, "data": raw})
        # Extract URLs if present
        for chunk in raw.split("link: "):
            if chunk.startswith("http"):
                sources.append(chunk.split()[0])

    return {**state, "search_results": results, "sources": list(set(sources))}
