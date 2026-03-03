"""
Vercel Serverless Function entry point.
Exposes the FastAPI app so Vercel's @vercel/python runtime can serve it.
"""
import sys
import os

# Add the backend directory to the Python path so imports work
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from app.main import app  # noqa: E402, F401
