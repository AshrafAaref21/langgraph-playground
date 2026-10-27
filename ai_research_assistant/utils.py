from .parsers import ResearchResponse


def print_research_response(question: str, response: ResearchResponse):
    """Pretty print a structured research response."""

    print(f"\nQ: {question}")
    print(f"\n  Answer: {response.answer}")
    print(f"\n  Confidence: {response.confidence}")
    print(f"  Sources: {', '.join(response.sources)}")

    if response.key_quotes:
        print("\n  Key Quotes:")
        for q in response.key_quotes:
            print(f'    - "{q}"')

    print("\n  Follow-up Questions:")
    for fq in response.follow_up_questions:
        print(f"    - {fq}")
