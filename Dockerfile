FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY manage.py .
COPY ai_research_assistant ./ai_research_assistant
COPY langgraph_examples ./langgraph_examples


CMD ["python", "manage.py", "exercise_first_langgraph"]

