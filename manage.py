import argparse

from dotenv import load_dotenv

from ai_research_assistant.main import ai_research_assistant_demo
from langgraph_examples.first_example import exercise_first_langgraph

load_dotenv(override=True)


def main():
    parser = argparse.ArgumentParser(description="Run project commands.")
    parser.add_argument(
        "command",
        choices=[
            "research_assistant",
            "exercise_first_langgraph",
            "first_workflow",
            "multi_agent_research_system",
        ],
        help="Command to run.",
    )
    args = parser.parse_args()

    if args.command == "research_assistant":
        ai_research_assistant_demo()
    elif args.command == "exercise_first_langgraph":
        exercise_first_langgraph()
    elif args.command == "first_workflow":
        from langgraph_examples.first_workflow import demo_conversation

        demo_conversation()
    elif args.command == "multi_agent_research_system":
        from multi_agent_research_system.demo import demo_full_research

        demo_full_research()


if __name__ == "__main__":
    main()
