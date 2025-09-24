# aieb_evaluation_svc

This service implements the backend for the AI Agent Evaluation system. It includes a FastAPI application for handling API requests and Celery for asynchronous task processing.

## Prerequisites

- Poetry installed
- Redis available (local install or Docker)

## Installation

Install dependencies using Poetry:

```bash
poetry install
```

## Environment Configuration

The application uses environment variables for configuration. You can set them using a `.env` file (automatically loaded via python-dotenv) or export them in your shell.

### Required Environment Variables

Create a `.env` file in the project root or set the following environment variables:

```bash
# .env file example
REDIS_BROKER_URL="redis://localhost:6379/0"
OPENAI_API_KEY="your_openai_api_key"
OPENAI_MODEL="your_openai_model"
```

### Setting Environment Variables in Shell

**macOS/Linux:**
```bash
export REDIS_BROKER_URL="redis://localhost:6379/0"
```

**Windows PowerShell:**
```powershell
$env:REDIS_BROKER_URL = "redis://localhost:6379/0"
```

**Note:** Both the FastAPI application and Celery worker read the same `.env` file for configuration.

## Running the Services

### 1. Start Redis

The easiest way to run Redis locally is using Docker:

```bash
docker run -d --name redis -p 6379:6379 redis:7-alpine
```

Alternatively, you can install and run Redis locally following the [Redis installation guide](https://redis.io/docs/getting-started/installation/).

### 2. Start the FastAPI Application

**Using uvicorn (recommended for development):**
```bash
poetry run uvicorn aieb_evaluation_svc.app:app --host 0.0.0.0 --port 8000 --reload
```

**Using the packaged entrypoint:**
```bash
poetry run aieb_evaluation_svc
```

The API will be available at `http://localhost:8000`. You can view the interactive API documentation at `http://localhost:8000/docs`.

### 3. Start the Celery Worker

In a separate terminal, start the Celery worker:

```bash
poetry run celery -A aieb_evaluation_svc.worker.celery_app worker -l info
```

**Note:** If your shell/Celery version requires specifying the attribute explicitly, use:
```bash
poetry run celery -A aieb_evaluation_svc.worker.celery_app:celery_app worker -l info
```

## Testing Asynchronous Tasks

### Test the Celery Integration

Once both the FastAPI application and Celery worker are running, you can test the asynchronous task processing:

1. **Trigger a test task:**
   ```bash
   curl "http://localhost:8000/api/test-celery-task?x=2&y=3"
   ```

2. **Expected response:**
   ```json
   {"task_id": "<uuid>"}
   ```

3. **Verify in worker logs:** Check the Celery worker terminal for logs showing the task was received and processed. The result should be 5 (2 + 3).

4. **Retrieve task result (optional):** Use this Python one-liner to get the task result:
   ```bash
   poetry run python -c "from celery.result import AsyncResult; from aieb_evaluation_svc.worker.celery_app import celery_app; import sys; rid=sys.argv[1]; print(AsyncResult(rid, app=celery_app).get(timeout=10))" <task_id>
   ```

   Replace `<task_id>` with the actual task ID returned from step 1.

## Running Tests

Run the test suite:

```bash
poetry run pytest
```

## Development

### Project Structure

- `src/aieb_evaluation_svc/` - Main application package
  - `api/` - FastAPI routers and endpoints
  - `core/` - Configuration and core utilities
  - `models/` - SQLAlchemy database models
  - `worker/` - Celery application and tasks
  - `app.py` - FastAPI application setup
  - `main.py` - Application entry point

### Adding New Celery Tasks

Add new Celery tasks in `src/aieb_evaluation_svc/worker/celery_app.py` and expose them through API endpoints in the `api/` directory.
