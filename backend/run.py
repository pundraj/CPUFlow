"""
ASGI entry point for deployment servers (e.g., Gunicorn with Uvicorn workers).

Usage:
  uvicorn run:app --host 0.0.0.0 --port 8000 --reload
"""
from app.main import app  # noqa: F401
