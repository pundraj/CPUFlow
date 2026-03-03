"""
Scheduling API routes.

Endpoints:
  POST /api/schedule          – schedule processes with a chosen algorithm
  POST /api/compare           – compare multiple algorithms on the same input
  GET  /api/algorithms        – list supported algorithms with metadata
  POST /api/export/csv        – export single result as CSV
  POST /api/export/compare    – export comparison results as CSV
"""

from __future__ import annotations
from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
import io

from app.models.schemas import (
    ScheduleRequest,
    ScheduleResponse,
    CompareRequest,
    CompareResponse,
    AlgorithmInfo,
)
from app.services.scheduler_service import (
    run_algorithm,
    run_comparison,
    ALGORITHM_INFO,
)
from app.services.export_service import export_single_csv, export_comparison_csv

router = APIRouter(prefix="/api", tags=["scheduling"])


# ---------------------------------------------------------------------------
# POST /api/schedule – run one algorithm
# ---------------------------------------------------------------------------

@router.post("/schedule", response_model=ScheduleResponse)
async def schedule(request: ScheduleRequest):
    """
    Schedule a list of processes using the selected algorithm.
    Returns the Gantt chart and performance metrics.
    """
    try:
        proc_dicts = [p.model_dump() for p in request.processes]
        result = run_algorithm(request.algorithm, proc_dicts, request.time_quantum)
        return result
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc))


# ---------------------------------------------------------------------------
# POST /api/compare – run multiple algorithms
# ---------------------------------------------------------------------------

@router.post("/compare", response_model=CompareResponse)
async def compare(request: CompareRequest):
    """
    Run multiple (or all) algorithms on the same set of processes and
    return results for each, enabling side-by-side comparison.
    """
    try:
        proc_dicts = [p.model_dump() for p in request.processes]
        results = run_comparison(proc_dicts, request.time_quantum, request.algorithms)
        return CompareResponse(results=results)
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc))


# ---------------------------------------------------------------------------
# GET /api/algorithms – list metadata
# ---------------------------------------------------------------------------

@router.get("/algorithms", response_model=list[AlgorithmInfo])
async def list_algorithms():
    """Return metadata for all supported scheduling algorithms."""
    return ALGORITHM_INFO


# ---------------------------------------------------------------------------
# POST /api/export/csv – export single result
# ---------------------------------------------------------------------------

@router.post("/export/csv")
async def export_csv(request: ScheduleRequest):
    """Run algorithm and return result as downloadable CSV."""
    try:
        proc_dicts = [p.model_dump() for p in request.processes]
        result = run_algorithm(request.algorithm, proc_dicts, request.time_quantum)
        csv_content = export_single_csv(result)
        return StreamingResponse(
            io.StringIO(csv_content),
            media_type="text/csv",
            headers={"Content-Disposition": "attachment; filename=schedule_result.csv"},
        )
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc))


# ---------------------------------------------------------------------------
# POST /api/export/compare – export comparison as CSV
# ---------------------------------------------------------------------------

@router.post("/export/compare")
async def export_compare_csv(request: CompareRequest):
    """Run comparison and return result as downloadable CSV."""
    try:
        proc_dicts = [p.model_dump() for p in request.processes]
        results = run_comparison(proc_dicts, request.time_quantum, request.algorithms)
        csv_content = export_comparison_csv(results)
        return StreamingResponse(
            io.StringIO(csv_content),
            media_type="text/csv",
            headers={"Content-Disposition": "attachment; filename=comparison_result.csv"},
        )
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc))
