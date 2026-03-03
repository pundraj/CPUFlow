"""
CPU Scheduling Algorithm Visualizer – FastAPI Application Entry Point
=====================================================================
Initializes the FastAPI app, configures CORS, and mounts all routes.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes.scheduling import router as scheduling_router

# ---------------------------------------------------------------------------
# App initialization
# ---------------------------------------------------------------------------

app = FastAPI(
    title="CPU Scheduling Algorithm Visualizer API",
    description=(
        "A production-ready REST API that simulates FCFS, SJF, SRTF, Priority, "
        "Round Robin, Multilevel Queue, and MLFQ scheduling algorithms. "
        "Returns Gantt charts and comprehensive performance metrics."
    ),
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# ---------------------------------------------------------------------------
# CORS – allow the React frontend (dev & production origins)
# ---------------------------------------------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",   # Vite dev server
        "http://localhost:3000",
        "http://localhost:4173",   # Vite preview
        "http://127.0.0.1:5173",
        "*",                       # For easy deployment – tighten in production
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------------------------------------
# Register routers
# ---------------------------------------------------------------------------

app.include_router(scheduling_router)


# ---------------------------------------------------------------------------
# Health check
# ---------------------------------------------------------------------------

@app.get("/", tags=["health"])
async def root():
    return {
        "status": "ok",
        "service": "CPU Scheduling Visualizer API",
        "version": "1.0.0",
    }


@app.get("/health", tags=["health"])
async def health_check():
    return {"status": "healthy"}
