from typing import Literal

from langgraph.graph import END, START, StateGraph
from langgraph.types import Send

from multi_agent_research_system.agents import (
    analyst,
    quality_checker,
    report_writer,
    search_agent,
    supervisor,
)
from multi_agent_research_system.state import ResearchState


def dispatch_searches(state: ResearchState) -> list[Send]:
    """Create parallel search tasks for each planned query."""
    return [
        Send("search_agent", {"search_query": query, "findings": []})
        for query in state["search_queries"]
    ]


def quality_gate(state: ResearchState) -> Literal["report_writer", "end"]:
    """Route back to the writer when the report needs another revision."""
    if state["quality_score"] >= 0.7 or state["iteration"] >= 2:
        return "end"
    return "report_writer"


def create_research_system():
    """Build and compile the multi-agent research graph."""
    graph = StateGraph(ResearchState)
    graph.add_node("supervisor", supervisor)
    graph.add_node("search_agent", search_agent)
    graph.add_node("analyst", analyst)
    graph.add_node("report_writer", report_writer)
    graph.add_node("quality_checker", quality_checker)

    graph.add_edge(START, "supervisor")
    graph.add_conditional_edges("supervisor", dispatch_searches, ["search_agent"])
    graph.add_edge("search_agent", "analyst")
    graph.add_edge("analyst", "report_writer")
    graph.add_edge("report_writer", "quality_checker")
    graph.add_conditional_edges(
        "quality_checker",
        quality_gate,
        {"report_writer": "report_writer", "end": END},
    )
    return graph.compile()
