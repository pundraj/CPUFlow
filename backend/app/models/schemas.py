"""
Pydantic models for request validation and response serialization.

These schemas define the data contracts between the frontend and backend,
ensuring type safety and automatic validation of all scheduling requests.
"""

from __future__ import annotations
from typing import Dict, List, Optional
from enum import Enum
from pydantic import BaseModel, Field, field_validator


# ---------------------------------------------------------------------------
# Enum for supported algorithms
# ---------------------------------------------------------------------------

class AlgorithmType(str, Enum):
    """Enumeration of all supported CPU scheduling algorithms."""
    FCFS = "fcfs"
    SJF = "sjf"
    SRTF = "srtf"
    PRIORITY_NP = "priority_np"       # Non-preemptive
    PRIORITY_P = "priority_p"         # Preemptive
    ROUND_ROBIN = "round_robin"
    MULTILEVEL_QUEUE = "multilevel_queue"
    MLFQ = "mlfq"


# ---------------------------------------------------------------------------
# Request models
# ---------------------------------------------------------------------------

class Process(BaseModel):
    """Represents a single process submitted by the user."""
    pid: str = Field(..., description="Unique process identifier, e.g. P1")
    arrival_time: int = Field(..., ge=0, description="Time the process arrives in the ready queue")
    burst_time: int = Field(..., ge=0, description="Total CPU burst time required")
    priority: int = Field(default=0, ge=0, description="Priority level (lower number = higher priority)")

    @field_validator("burst_time")
    @classmethod
    def burst_time_check(cls, v):
        """Allow zero burst time but flag it – the algorithm will skip it."""
        return v


class ScheduleRequest(BaseModel):
    """Payload sent from the frontend to schedule a set of processes."""
    processes: List[Process] = Field(..., min_length=1, description="List of processes to schedule")
    algorithm: AlgorithmType = Field(..., description="Scheduling algorithm to use")
    time_quantum: int = Field(default=2, ge=1, description="Time quantum for Round Robin / MLFQ")

    @field_validator("processes")
    @classmethod
    def unique_pids(cls, v):
        pids = [p.pid for p in v]
        if len(pids) != len(set(pids)):
            raise ValueError("Process IDs must be unique")
        return v


class CompareRequest(BaseModel):
    """Payload for algorithm comparison mode – runs all algorithms on the same input."""
    processes: List[Process] = Field(..., min_length=1)
    time_quantum: int = Field(default=2, ge=1)
    algorithms: Optional[List[AlgorithmType]] = Field(
        default=None,
        description="Algorithms to compare. If None, all algorithms are compared.",
    )


# ---------------------------------------------------------------------------
# Response models
# ---------------------------------------------------------------------------

class GanttEntry(BaseModel):
    """One segment of the Gantt chart timeline."""
    process: str = Field(..., description="Process ID or 'Idle' for CPU idle time")
    start: int = Field(..., ge=0)
    end: int = Field(..., ge=0)


class ScheduleMetrics(BaseModel):
    """Comprehensive performance metrics for a scheduling result."""
    completion_times: Dict[str, int] = Field(default_factory=dict)
    turnaround_times: Dict[str, int] = Field(default_factory=dict)
    waiting_times: Dict[str, int] = Field(default_factory=dict)
    response_times: Dict[str, int] = Field(default_factory=dict)
    average_waiting_time: float = 0.0
    average_turnaround_time: float = 0.0
    cpu_utilization: float = 0.0       # percentage (0-100)
    throughput: float = 0.0            # processes per unit time


class ScheduleResponse(BaseModel):
    """Unified response returned by every scheduling endpoint."""
    algorithm: str
    gantt_chart: List[GanttEntry]
    metrics: ScheduleMetrics


class CompareResponse(BaseModel):
    """Response for algorithm comparison mode."""
    results: Dict[str, ScheduleResponse]


class AlgorithmInfo(BaseModel):
    """Metadata about a scheduling algorithm – displayed in the UI."""
    name: str
    key: str
    description: str
    time_complexity: str
    preemptive: bool
    needs_priority: bool = False
    needs_time_quantum: bool = False
