# Production LangGraph API

A standalone FastAPI service that exposes a LangGraph-powered chat endpoint. The example brings together request validation, basic input/output security checks, an in-memory response cache, rate limiting, structured logs, metrics, and optional LangSmith tracing.

This is a learning/reference project, not a complete security or operations solution. The cache and metrics are process-local and reset on restart; security filters are heuristic and should not be treated as a guarantee against prompt injection, harmful output, or data leakage. The API does not provide authentication or persistent conversation history.

## Features

- **LangGraph agent** with a primary model, fallback model, and a graceful error response.
- **Input/output checks** that detect a set of prompt-injection patterns, mask common PII formats, and apply basic output filters.
- **In-memory response cache** with configurable TTL and case-insensitive query keys.
- **Rate limiting** per client IP using SlowAPI.
- **Health, metrics, and cache-stat endpoints.**
- **JSON structured logging** and optional LangSmith tracing.
- **Docker Compose** and Render deployment configuration.

## Requirements

- Python 3.12 (see `.python-version`)
- [`uv`](https://docs.astral.sh/uv/)
- An OpenAI API key
- Docker, if you want to run the containerized service

## Local setup

From this directory, create the environment file and install the locked dependencies:

```powershell
Copy-Item .env.example .env
uv sync --dev
```

On macOS or Linux:

```bash
cp .env.example .env
uv sync --dev
```

Edit `.env` and set `OPENAI_API_KEY`. LangSmith tracing is enabled in the example environment file; set `LANGCHAIN_TRACING_V2=false` to disable it, or configure `LANGCHAIN_API_KEY` to send traces to LangSmith. Do not commit `.env` or real API keys.

Start the API locally:

```bash
uv run uvicorn app.main:app --reload
```

The server listens on `http://127.0.0.1:8000`. Interactive API documentation is available at `/docs`.

## API

### `POST /chat`

Request:

```json
{
  "message": "What is LangGraph?",
  "thread_id": "demo"
}
```

`message` is required and must contain 1-10,000 characters. `thread_id` is optional and defaults to `"default"`; it is echoed in the response for correlation, but it does not create persistent conversation memory.

Example response:

```json
{
  "response": "LangGraph is ...",
  "thread_id": "demo",
  "model_used": "primary",
  "cached": false,
  "processing_time_ms": 842.5,
  "security_notes": [],
  "timestamp": "2026-11-07T10:00:00+00:00"
}
```

The service allows 20 requests per minute per client IP by default. Change `RATE_LIMIT` to configure the limit.

### Other endpoints

| Method | Path | Purpose |
| --- | --- | --- |
| `GET` | `/health` | Reports application startup checks and environment |
| `GET` | `/metrics` | Returns in-memory request, error, latency, token-estimate, and cache-hit metrics |
| `GET` | `/cache/stats` | Returns in-memory cache hit, miss, and entry counts |
| `GET` | `/docs` | Interactive OpenAPI documentation |

## Configuration

Settings are loaded from environment variables or `.env`. Defaults are defined in `app/config.py`.

| Variable | Required | Default | Description |
| --- | --- | --- | --- |
| `OPENAI_API_KEY` | Yes | - | OpenAI API key |
| `PRIMARY_MODEL` | No | `gpt-4o-mini` | Primary chat model |
| `FALLBACK_MODEL` | No | `gpt-4o-mini` | Model used after the primary attempt fails |
| `APP_ENV` | No | `development` | Application environment label |
| `LOG_LEVEL` | No | `INFO` | Structured logger level, applied at application startup |
| `RATE_LIMIT` | No | `20/minute` | Per-client request limit |
| `CACHE_TTL_SECONDS` | No | `300` | In-memory response cache lifetime |
| `MAX_RETRIES` | No | `3` | Retry threshold before using the fallback route |
| `LANGCHAIN_TRACING_V2` | No | `true` | Enable LangSmith tracing |
| `LANGCHAIN_API_KEY` | No | empty | LangSmith API key |
| `LANGCHAIN_PROJECT` | No | `production-api` | LangSmith project name |

The cache is keyed by the cleaned message only, so it is shared across thread IDs within a process. Do not use this in a multi-tenant deployment without adapting the cache key and adding authentication/authorization.

## Tests

The automated tests cover the security and cache modules and do not call an LLM:

```bash
uv run pytest
```

`Production-test-commands.sh` contains additional manual examples, including requests to a running API.

## Docker

From this directory, copy/configure `.env`, then run:

```bash
docker compose up --build
```

The API is exposed on port `8000`. The image runs Uvicorn as a non-root user and defines a health check for `/health`.

## Render

`render.yml` describes a Render web service. Set the Render service's **Root Directory** to `production-api`. Configure `OPENAI_API_KEY` and, if tracing is enabled, `LANGCHAIN_API_KEY` as secrets in Render before deployment. Review the service plan, region, and configuration for your own deployment.

## Project layout

```text
app/
  agent.py       LangGraph agent and model fallback
  cache.py       TTL response cache
  config.py      Environment-backed settings
  main.py        FastAPI app, lifecycle, middleware handlers, and routes
  models.py      Request and response schemas
  monitoring.py  Structured logging, metrics, and request timer
  security.py    Input sanitizer, PII masking, and output validation
tests/
  test_cache.py
  test_security.py
```
