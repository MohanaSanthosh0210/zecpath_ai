# Deployment & Setup Guide

This guide covers local development setup and production deployment notes.

Prerequisites
- Python 3.10+ (3.11 recommended)
- pip, virtualenv
- Optional: Docker for containerized deployment

Install dependencies (local dev)

```bash
python -m venv .venv
source .venv/bin/activate   # Linux/macOS
\.venv\Scripts\activate    # Windows PowerShell
pip install --upgrade pip
pip install -r requirements.txt
```

Notes about included wheels
- The repository includes prebuilt wheels for `torch` and `transformers` intended for offline installation. If you use the wheels, install with `pip install path/to/wheel.whl` before installing other packages.

Running the system locally

```bash
python main.py
# or, if a FastAPI server is used:
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Docker (minimal)

Create a `Dockerfile` that installs Python, copies the repository, installs wheels/requirements, and exposes the server port. Example (high-level):

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY . /app
RUN pip install --upgrade pip && pip install -r requirements.txt
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

Production considerations
- Use a process manager (gunicorn/uvicorn with workers) behind a reverse proxy (nginx).
- Secure secrets via environment variables or a secrets manager — do NOT check secrets into the repo.
- Monitor logs (log files and observability pipelines). See `logs/` and `observability/` directories.
