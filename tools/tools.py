import os
from typing import List
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.utilities import GoogleSerperAPIWrapper

from langchain_core.messages import ToolMessage
from langchain_core.runnables import RunnableLambda

from langgraph.prebuilt import ToolNode
from langgraph.prebuilt import tools_condition
from langchain_core.tools import tool, BaseTool
from langchain_community.tools import DuckDuckGoSearchResults
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_community.document_loaders import WebBaseLoader
# from agent.tools import calculator


search = GoogleSerperAPIWrapper()

# @tool("Scrape the web")
# def scraper(urls: List[str]) -> str:
#     "Use requests and bs4 to scrape the provided web pages for detailed information."
#     loader = WebBaseLoader(urls)
#     docs = loader.load()
#     return "\n\n".join(
#         [
#             f'<Document name="{doc.metadata.get("title", "")}">\n{doc.page_content}\n</Document>'
#             for doc in docs
#         ]
#     )


# @tool("from RAG vectors")
# def loadDocuments(documents: List) -> str: 
#     pass
#     # return ragvectors.retriever


# Set up the tool
duckduckgo_search = DuckDuckGoSearchResults(name="duckduckgo_search")

# tavily_search = TavilySearchResults(name="tavily_search",max_results=3)

# web_search_tools = [duckduckgo_search, tavily_search]

# web_search_tool_node = ToolNode(web_search_tools)