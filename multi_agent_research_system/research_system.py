"""Compatibility entry point for the multi-agent research system."""

from multi_agent_research_system.agents import (
    QualityReview,
    analyst,
    quality_checker,
    report_writer,
    search_agent,
    supervisor,
)
from multi_agent_research_system.demo import (
    demo_full_research,
    demo_individual_search,
    demo_research_with_streaming,
)
from multi_agent_research_system.graph import (
    create_research_system,
    dispatch_searches,
    quality_gate,
)
from multi_agent_research_system.models import research_llm as llm
from multi_agent_research_system.models import writing_llm as creative_llm
from multi_agent_research_system.state import (
    ResearchState,
    SearchTaskState,
    initial_research_state,
)

__all__ = [
    "QualityReview",
    "ResearchState",
    "SearchTaskState",
    "analyst",
    "create_research_system",
    "creative_llm",
    "demo_full_research",
    "demo_individual_search",
    "demo_research_with_streaming",
    "dispatch_searches",
    "initial_research_state",
    "llm",
    "quality_checker",
    "quality_gate",
    "report_writer",
    "search_agent",
    "supervisor",
]

if __name__ == "__main__":
    demo_full_research()
