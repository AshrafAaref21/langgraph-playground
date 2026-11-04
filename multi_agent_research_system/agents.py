import json

from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from pydantic import BaseModel, Field

from multi_agent_research_system.models import research_llm, writing_llm
from multi_agent_research_system.state import ResearchState, SearchTaskState


class QualityReview(BaseModel):
    score: float = Field(description="Quality score from 0.0 to 1.0")
    feedback: str = Field(description="Specific feedback for improvement")
    approved: bool = Field(description="Whether the report meets quality standards")


def supervisor(state: ResearchState) -> dict:
    """Plan research by generating targeted search queries."""
    response = research_llm.invoke(
        [
            SystemMessage(
                content=(
                    "You are a research supervisor. Given a topic, generate exactly 3 "
                    "specific search queries that will cover different angles of the topic. "
                    "Return ONLY a JSON array of strings. No markdown formatting."
                )
            ),
            HumanMessage(content=f"Research topic: {state['topic']}"),
        ]
    )

    try:
        queries = json.loads(response.content)
    except json.JSONDecodeError:
        queries = [
            f"{state['topic']} overview",
            f"{state['topic']} latest developments",
            f"{state['topic']} practical applications",
        ]

    return {
        "search_queries": queries[:3],
        "messages": [
            AIMessage(
                content=f"[SUPERVISOR]: Planned {len(queries)} research queries: {queries}",
                name="supervisor",
            )
        ],
    }


def search_agent(state: SearchTaskState) -> dict:
    """Execute one search query and return its findings."""
    query = state["search_query"]
    response = research_llm.invoke(
        [
            SystemMessage(
                content=(
                    "You are a web research agent. For the given search query, "
                    "provide 2-3 key findings. Each finding should have a 'title' "
                    "and 'detail' field. Return a JSON array. No markdown."
                )
            ),
            HumanMessage(content=f"Search query: {query}"),
        ]
    )

    try:
        results = json.loads(response.content)
    except json.JSONDecodeError:
        results = [{"title": query, "detail": response.content}]

    for finding in results:
        finding["source_query"] = query

    return {"findings": results}


def analyst(state: ResearchState) -> dict:
    """Synthesize the collected findings into an analysis."""
    findings_text = json.dumps(state["findings"], indent=2)
    response = research_llm.invoke(
        [
            SystemMessage(
                content=(
                    "You are a research analyst. Synthesize the collected findings into "
                    "a clear analysis. Identify:\n"
                    "1. Key themes across all findings\n"
                    "2. Any contradictions or gaps\n"
                    "3. The most important insights\n\n"
                    "Write 2-3 paragraphs."
                )
            ),
            HumanMessage(
                content=(
                    f"Research topic: {state['topic']}\n\n"
                    f"Collected findings:\n{findings_text}"
                )
            ),
        ]
    )

    return {
        "analysis": response.content,
        "messages": [
            AIMessage(content=f"[ANALYST]: {response.content}", name="analyst")
        ],
    }


def report_writer(state: ResearchState) -> dict:
    """Write a structured research report from the analysis."""
    revision_note = ""
    if state["iteration"] > 0 and state.get("quality_feedback"):
        revision_note = (
            f"\n\nIMPORTANT — This is revision #{state['iteration']}. "
            f"Address this feedback: {state['quality_feedback']}"
        )

    response = writing_llm.invoke(
        [
            SystemMessage(
                content=(
                    "You are a report writer. Produce a well-structured research report "
                    "with these sections:\n"
                    "1. Executive Summary (2-3 sentences)\n"
                    "2. Key Findings (bullet points)\n"
                    "3. Analysis (1-2 paragraphs)\n"
                    "4. Recommendations (3 actionable items)\n\n"
                    "Use markdown formatting. Be specific and actionable."
                    f"{revision_note}"
                )
            ),
            HumanMessage(
                content=(
                    f"Topic: {state['topic']}\n\n"
                    f"Analysis:\n{state['analysis']}\n\n"
                    f"Raw findings:\n{json.dumps(state['findings'][:6], indent=2)}"
                )
            ),
        ]
    )

    return {
        "report": response.content,
        "messages": [
            AIMessage(
                content=f"[REPORT WRITER]: Report {'revised' if state['iteration'] > 0 else 'drafted'}.",
                name="report_writer",
            )
        ],
    }


def quality_checker(state: ResearchState) -> dict:
    """Review the report and record its score and revision feedback."""
    review_llm = research_llm.with_structured_output(QualityReview)
    review = review_llm.invoke(
        [
            SystemMessage(
                content=(
                    "You are a quality reviewer. Score the report on:\n"
                    "- Completeness: Does it cover the topic well?\n"
                    "- Clarity: Is it well-written and easy to understand?\n"
                    "- Actionability: Are recommendations specific?\n\n"
                    "Score from 0.0 to 1.0. Approve if score >= 0.7.\n"
                    "If this is iteration 2 or higher, be more lenient."
                )
            ),
            HumanMessage(
                content=(
                    f"Topic: {state['topic']}\n"
                    f"Iteration: {state['iteration']}\n\n"
                    f"Report:\n{state['report']}"
                )
            ),
        ]
    )

    approved = review.approved or state["iteration"] >= 2
    return {
        "quality_score": review.score,
        "quality_feedback": review.feedback,
        "iteration": state["iteration"] + 1,
        "messages": [
            AIMessage(
                content=(
                    f"[QUALITY CHECK]: Score {review.score:.1f} — "
                    f"{'APPROVED' if approved else 'REVISION NEEDED'}: {review.feedback}"
                ),
                name="quality_checker",
            )
        ],
    }
