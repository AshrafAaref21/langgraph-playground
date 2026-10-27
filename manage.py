import argparse

from dotenv import load_dotenv

from ai_research_assistant.main import ai_research_assistant_demo

load_dotenv(override=True)


def main():
    parser = argparse.ArgumentParser(description="Run project commands.")
    parser.add_argument(
        "command",
        choices=["research_assistant"],
        help="Command to run.",
    )
    args = parser.parse_args()

    if args.command == "research_assistant":
        ai_research_assistant_demo()


if __name__ == "__main__":
    main()
