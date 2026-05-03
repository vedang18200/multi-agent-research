# frontend/app.py
import streamlit as st
import requests

API_URL = "http://localhost:8000/api/research"

st.set_page_config(page_title="AI Research Agent", page_icon="🔍")
st.title("Multi-Agent Research Pipeline")
st.caption("Powered by LangGraph + Groq (LLaMA 3.3)")

query = st.text_input("Enter your research topic", placeholder="e.g. Impact of AI on software jobs in 2025")

if st.button("Run Research", type="primary"):
    if query:
        with st.spinner("Agents working..."):
            try:
                res = requests.post(API_URL, json={"query": query}, timeout=120)
                data = res.json()

                st.success(f"Confidence score: {data['confidence_score']:.0%}")

                with st.expander("Subtasks planned"):
                    for i, t in enumerate(data["subtasks"], 1):
                        st.write(f"{i}. {t}")

                st.markdown("## Research Report")
                st.markdown(data["report"])

                if data["sources"]:
                    with st.expander("Sources"):
                        for s in data["sources"]:
                            st.write(s)
            except Exception as e:
                st.error(f"Error: {e}")
    else:
        st.warning("Please enter a query")
