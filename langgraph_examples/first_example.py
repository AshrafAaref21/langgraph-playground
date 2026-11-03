from typing import TypedDict

from langchain.chat_models import init_chat_model
from langgraph.graph import END, START, StateGraph


def exercise_first_langgraph():
    """
    EXERCISE: Create a LangGraph that:
    1. Takes a topic as input
    2. Node 1: Generates 3 questions about the topic
    3. Node 2: Answers one of the questions
    4. Returns both questions and answer
    """

    class QA(TypedDict):
        topic: str
        questions: list[str]
        answer: str

    llm = init_chat_model("gpt-4o-mini", temperature=0)

    def generate_questions(state: QA) -> dict[str, list[str]]:
        response = llm.invoke(
            f"Generate exactly 3 questions about this topic, one per line: {state['topic']}"
        )
        questions = [
            line.strip()
            for line in response.content.splitlines()
            if line.strip()
        ]
        return {"questions": questions}

    def answer_question(state: QA) -> dict[str, str]:
        question = state["questions"][0]
        response = llm.invoke(f"Answer the provided question: {question}")
        return {"answer": response.content}

    graph = StateGraph(QA)

    graph.add_node("generate_questions", generate_questions)
    graph.add_node("answer_question", answer_question)
    graph.add_edge(START, "generate_questions")
    graph.add_edge("generate_questions", "answer_question")
    graph.add_edge("answer_question", END)

    app = graph.compile()

    result = app.invoke({"topic": "Artificial Intelligence"})
    print(result)
