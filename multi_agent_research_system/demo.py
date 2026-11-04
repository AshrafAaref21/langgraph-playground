from langchain_core.messages import AIMessage

from multi_agent_research_system.agents import search_agent
from multi_agent_research_system.graph import create_research_system
from multi_agent_research_system.state import SearchTaskState, initial_research_state


def demo_research_with_streaming() -> None:
    """Run the research system with step-by-step streaming output."""
    system = create_research_system()
    graph_image = system.get_graph().draw_mermaid_png()

    with open("research_graph.png", "wb") as graph_file:
        graph_file.write(graph_image)

    topic = "Best practices for building multi-agent AI systems"
    print(f"Streaming Research: {topic}\n")

    for step in system.stream(initial_research_state(topic), stream_mode="updates"):
        for node_name, update in step.items():
            print(f"[{node_name}] completed")
            if update.get("search_queries"):
                print(f"  Planned queries: {update['search_queries']}")
            if update.get("findings"):
                print(f"  Found {len(update['findings'])} results")
            if update.get("quality_score") is not None:
                print(f"  Quality score: {update['quality_score']:.1f}")
            if update.get("report"):
                print(f"  Report length: {len(update['report'])} chars")
        print()


def demo_individual_search() -> None:
    """Run the search agent against a sample query."""
    print("Individual Search Agent Test:\n")
    task: SearchTaskState = {
        "search_query": "LangGraph multi-agent patterns",
        "findings": [],
    }
    result = search_agent(task)

    print("Findings from search:")
    for finding in result["findings"]:
        print(
            f"  - {finding.get('title', 'N/A')}: "
            f"{finding.get('detail', 'N/A')[:80]}..."
        )


def demo_full_research() -> None:
    """Run the complete research pipeline and print its report."""
    system = create_research_system()
    topic = "The impact of AI agents on software development in 2026"
    print("Multi-Agent Research System Demo")
    print("=" * 60)
    print(f"Topic: {topic}\n")

    result = system.invoke(initial_research_state(topic))

    print("Agent Activity Log:")
    print("-" * 40)
    for message in result["messages"]:
        if isinstance(message, AIMessage):
            print(f"  {message.content[:120]}...")
    print()

    print(f"Total findings collected: {len(result['findings'])}")
    print(f"Quality score: {result['quality_score']:.1f}")
    print(f"Iterations: {result['iteration']}")
    print()

    print("=" * 60)
    print("FINAL RESEARCH REPORT")
    print("=" * 60)
    print(result["report"])
