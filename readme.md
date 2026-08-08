# Pravartak First Service

A small FastAPI service (with optional Streamlit front-ends) that wraps OpenAI-compatible chat completions behind a few REST endpoints, plus JSON file logging.

## Project layout

| File | Purpose |
|---|---|
| `service.py` | Main FastAPI app — defines the HTTP endpoints. Entry point for the service. |
| `utils.py` | OpenAI client setup + helpers (`call_open_ai`, `stream_answer`) used by `service.py`. |
| `settings.py` | Loads configuration from `.env` via `pydantic-settings`. |
| `my_logging.py` | Configures a JSON file logger that writes to `service.log`. |
| `service.log` | Log output from the running service (generated at runtime). |
| `requirements.txt` | Python dependencies. |
| `chat_ui.py` | Streamlit page that calls the running FastAPI service (`/first_endpoint`). |
| `simple_ui.py` | Standalone Streamlit demo (name/age form) — does not call the service. |
| `streamlit.py` | Minimal Streamlit chat-input demo — does not call the service. |
| `app.py` | Scratch script for testing the `settings.py` / `pydantic` models directly (not the service entry point). |
| `.env` | Local environment variables (API keys, etc.) — not committed to git. |

## Prerequisites

- Python 3.10+ (tested with 3.14)
- pip

## 1. Set up a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate      # on Windows: .venv\Scripts\activate
```

## 2. Install dependencies

```bash
pip install -r requirements.txt
```

## 3. Configure environment variables

The service reads its configuration from a `.env` file in the project root (loaded by `settings.py`). Create/update `.env` with:

```
OPEN_AI_API_KEY=your-api-key
OPEN_AI_BASE_URL=https://your-openai-compatible-endpoint/v1
OPEN_AI_RETRIES=3
OPEN_AI_TEMPERATURE=0.2
OPEN_AI_TIMEOUT=60
```

> **Note:** `.env` contains a live API key and is currently untracked by git. Do not commit it — consider adding a `.gitignore` entry for `.env` before your next commit.

## 4. Run the FastAPI service

From the project root, with the virtual environment active:

```bash
python service.py
```

or equivalently:

```bash
uvicorn service:app --reload --port 8000
```

The service starts on `http://127.0.0.1:8000` with auto-reload enabled.

Logs are written as JSON lines to `service.log`.

### Available endpoints

| Method | Path | Description |
|---|---|---|
| GET | `/` | Health/welcome message |
| GET | `/first_endpoint` | Sample welcome message |
| POST | `/user/registration` | Accepts a user object, echoes it back |
| POST | `/chat` | Body: `{"query": "..."}` — sends the query to OpenAI and returns the response |
| POST | `/streaming` | Body: `{"question": "..."}` — streams back a canned answer word-by-word (Server-Sent Events) |

Interactive API docs are available at `http://127.0.0.1:8000/docs` once the service is running.

### Quick test

```bash
curl http://127.0.0.1:8000/first_endpoint

curl -X POST http://127.0.0.1:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"query": "Hello!"}'
```

## 5. (Optional) Run the Streamlit UIs

With the FastAPI service running in one terminal, run a UI in another:

```bash
streamlit run chat_ui.py     # calls the running FastAPI service
streamlit run simple_ui.py   # standalone demo, no service dependency
streamlit run streamlit.py   # standalone demo, no service dependency
```
