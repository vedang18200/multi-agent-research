from langchain_community.tools import DuckDuckGoSearchResults

def get_search_tool():
    return DuckDuckGoSearchResults(num_results=5)
