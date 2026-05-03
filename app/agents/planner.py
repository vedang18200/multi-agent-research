# app/agents/planner.py
from langchain_groq import ChatGroq
from app.config import GROQ_API_KEY, MODEL_NAME
from app.graph.state import ResearchState

llm = ChatGroq(api_key=GROQ_API_KEY, model=MODEL_NAME)

def planner_node(state: ResearchState) -> ResearchState:
    prompt = f"""Break this research query into 3-4 specific subtasks.
Return ONLY a numbered list, nothing else.

Query: {state['query']}"""

    response = llm.invoke(prompt)
    lines = [l.strip() for l in response.content.split("\n") if l.strip()]
    subtasks = [l.lstrip("0123456789. ") for l in lines if l]

    return {**state, "subtasks": subtasks}
