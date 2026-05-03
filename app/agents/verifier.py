# app/agents/verifier.py
from langchain_groq import ChatGroq
from app.config import GROQ_API_KEY, MODEL_NAME
from app.graph.state import ResearchState

llm = ChatGroq(api_key=GROQ_API_KEY, model=MODEL_NAME)

def verifier_node(state: ResearchState) -> ResearchState:
    prompt = f"""Review this research report for quality.
Score it from 0.0 to 1.0 on: accuracy, completeness, clarity.
Return ONLY a JSON object like: {{"score": 0.85, "issues": ["issue1"]}}

Report:
{state['draft_report']}"""

    response = llm.invoke(prompt)
    try:
        import json, re
        match = re.search(r'\{.*\}', response.content, re.DOTALL)
        data = json.loads(match.group()) if match else {"score": 0.7, "issues": []}
        score = float(data.get("score", 0.7))
    except Exception:
        score = 0.7

    return {
        **state,
        "confidence_score": score,
        "verified_report": state["draft_report"],
        "retry_count": state.get("retry_count", 0)
    }
