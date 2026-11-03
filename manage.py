import argparse

from dotenv import load_dotenv

from ai_research_assistant.main import ai_research_assistant_demo
from langgraph_examples.first_example import exercise_first_langgraph

load_dotenv(override=True)


def main():
    parser = argparse.ArgumentParser(description="Run project commands.")
    parser.add_argument(
        "command",
        choices=["research_assistant", "exercise_first_langgraph", "first_workflow"],
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


if __name__ == "__main__":
    main()
