# LangGraph Playground

Small, runnable Python examples for learning LangChain and LangGraph patterns. The repository includes introductory workflows, a retrieval-augmented research assistant, and a multi-agent research pipeline.

## What's included

| Example | What it demonstrates | Run |
| --- | --- | --- |
| First LangGraph exercise | A basic graph that generates questions about a topic and answers one | `python manage.py exercise_first_langgraph` |
| Conversation workflow | A stateful graph that classifies sentiment and generates a response | `python manage.py first_workflow` |
| AI research assistant | Document ingestion, vector retrieval, conversational memory, and structured answers | `python manage.py research_assistant` |
| Multi-agent research system | Parallel research, synthesis, report writing, and iterative quality review | `python manage.py multi_agent_research_system` |
| Production API | A standalone FastAPI service that wraps a LangGraph agent with rate limiting, caching, security checks, and metrics | See [production-api](./production-api/README.md) |

## Requirements

- Python 3.10 or later
- An OpenAI API key for the examples that call a language model

## Setup

Create and activate a virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

On macOS or Linux, activate it with:

```bash
source .venv/bin/activate
```

Install the project dependencies:

```bash
python -m pip install -r requirements.txt
```

Copy `.env.example` to `.env` and set your API key:

```powershell
Copy-Item .env.example .env
```

On macOS or Linux:

```bash
cp .env.example .env
```

```dotenv
OPENAI_API_KEY=your_openai_api_key
```

The examples use `gpt-4o-mini`. Keep `.env` private; it is excluded from Git.

## Run an example

List available commands:

```bash
python manage.py --help
```

Run any of the examples listed above. For example:

```bash
python manage.py multi_agent_research_system
```

The multi-agent research graph follows this workflow:

1. A supervisor creates three research queries.
2. Search agents run in parallel and return findings.
3. An analyst synthesizes the findings.
4. A report writer drafts a structured report.
5. A quality checker scores the report and requests revisions when needed. The workflow ends when the score reaches `0.7` or after two review passes.

The streaming and individual-search demos are also available from Python:

```python
from multi_agent_research_system.demo import (
    demo_individual_search,
    demo_research_with_streaming,
)

demo_individual_search()
# or
demo_research_with_streaming()
```

The streaming demo writes a graph visualization to `research_graph.png`.

> **Note:** The research assistant demo recreates and removes the local `research_db/` directory while it runs.

## Project layout

```text
ai_research_assistant/       Retrieval-augmented research assistant
langgraph_examples/          Introductory LangGraph workflows
multi_agent_research_system/
  agents.py                  Research, analysis, writing, and review nodes
  demo.py                    Runnable demos
  graph.py                   Graph construction and routing
  models.py                  Chat model configuration
  state.py                   Graph state definitions
production-api/              Standalone FastAPI + LangGraph service (Python 3.12)
manage.py                    Command-line entry point
requirements.txt             Python dependencies
```

## Production API

The service is an independent project with its own dependencies, lock file, Docker setup, tests, and deployment configuration. It requires Python 3.12 and `uv`; the root `requirements.txt` does not install its dependencies.

See the [production API README](./production-api/README.md) for setup, configuration, local run instructions, endpoints, tests, and deployment details.

## Make targets

If `make` is installed, the repository also provides these convenience targets:

```bash
make install
make research_assistant
make multi_agent_research_system
make exercise_first_langgraph
```

## Docker

The current Docker image runs the introductory `exercise_first_langgraph` example by default:

```bash
docker compose up --build
```

Docker Compose reads environment variables from `.env`. The image currently includes the introductory examples and research assistant, but not the `multi_agent_research_system` package.
