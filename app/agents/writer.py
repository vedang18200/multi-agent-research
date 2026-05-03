# app/agents/writer.py
from langchain_groq import ChatGroq
from app.config import GROQ_API_KEY, MODEL_NAME
from app.graph.state import ResearchState
import json

llm = ChatGroq(api_key=GROQ_API_KEY, model=MODEL_NAME)

def writer_node(state: ResearchState) -> ResearchState:
    context = json.dumps(state["search_results"], indent=2)

    prompt = f"""You are a research writer. Using the search results below, write a
comprehensive, well-structured report on: "{state['query']}"

Format:
- Use markdown headers
- Cite sources inline as [Source N]
- Include a summary section at the top
- End with a numbered list of key findings

Search Results:
{context}"""

    response = llm.invoke(prompt)
    return {**state, "draft_report": response.content}
