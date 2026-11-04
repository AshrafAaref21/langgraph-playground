import operator
from typing import Annotated, TypedDict

from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages


class ResearchState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]
    topic: str
    search_queries: list[str]
    findings: Annotated[list[dict], operator.add]
    analysis: str
    report: str
    quality_score: float
    quality_feedback: str
    iteration: int


class SearchTaskState(TypedDict):
    search_query: str
    findings: Annotated[list[dict], operator.add]


def initial_research_state(topic: str) -> ResearchState:
    """Create the initial state required to run the research graph."""
    return {
        "messages": [],
        "topic": topic,
        "search_queries": [],
        "findings": [],
        "analysis": "",
        "report": "",
        "quality_score": 0.0,
        "quality_feedback": "",
        "iteration": 0,
    }
