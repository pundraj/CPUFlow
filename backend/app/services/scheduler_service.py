"""
Scheduler Service – orchestrates algorithm execution and response formatting.

This service layer decouples the route handlers from the algorithm
implementations, making it easy to swap or extend algorithms independently.
"""

from __future__ import annotations
from typing import Dict, List, Optional

from app.models.schemas import (
    AlgorithmInfo,
    AlgorithmType,
    GanttEntry,
    ScheduleMetrics,
    ScheduleResponse,
)
from app.algorithms.fcfs import fcfs_schedule
from app.algorithms.sjf import sjf_schedule
from app.algorithms.srtf import srtf_schedule
from app.algorithms.priority import (
    priority_schedule_nonpreemptive,
    priority_schedule_preemptive,
)
from app.algorithms.round_robin import round_robin_schedule
from app.algorithms.multilevel_queue import multilevel_queue_schedule
from app.algorithms.mlfq import mlfq_schedule


# ---------------------------------------------------------------------------
# Algorithm registry – maps AlgorithmType → (callable, human-readable name)
# ---------------------------------------------------------------------------

_ALGORITHM_MAP = {
    AlgorithmType.FCFS: (fcfs_schedule, "First Come First Serve (FCFS)"),
    AlgorithmType.SJF: (sjf_schedule, "Shortest Job First (SJF)"),
    AlgorithmType.SRTF: (srtf_schedule, "Shortest Remaining Time First (SRTF)"),
    AlgorithmType.PRIORITY_NP: (priority_schedule_nonpreemptive, "Priority (Non-Preemptive)"),
    AlgorithmType.PRIORITY_P: (priority_schedule_preemptive, "Priority (Preemptive)"),
    AlgorithmType.ROUND_ROBIN: (round_robin_schedule, "Round Robin (RR)"),
    AlgorithmType.MULTILEVEL_QUEUE: (multilevel_queue_schedule, "Multilevel Queue"),
    AlgorithmType.MLFQ: (mlfq_schedule, "Multilevel Feedback Queue (MLFQ)"),
}


def run_algorithm(
    algorithm: AlgorithmType,
    processes: List[Dict],
    time_quantum: int = 2,
) -> ScheduleResponse:
    """
    Execute a single scheduling algorithm and return a structured response.
    """
    func, name = _ALGORITHM_MAP[algorithm]

    proc_dicts = [
        {
            "pid": p["pid"],
            "arrival_time": p["arrival_time"],
            "burst_time": p["burst_time"],
            "priority": p.get("priority", 0),
        }
        for p in processes
    ]

    # Algorithms that accept time_quantum
    if algorithm in (
        AlgorithmType.ROUND_ROBIN,
        AlgorithmType.MULTILEVEL_QUEUE,
        AlgorithmType.MLFQ,
    ):
        gantt_raw, metrics_raw = func(proc_dicts, time_quantum)
    else:
        gantt_raw, metrics_raw = func(proc_dicts)

    gantt_chart = [GanttEntry(**entry) for entry in gantt_raw]
    metrics = ScheduleMetrics(**metrics_raw)

    return ScheduleResponse(algorithm=name, gantt_chart=gantt_chart, metrics=metrics)


def run_comparison(
    processes: List[Dict],
    time_quantum: int = 2,
    algorithms: Optional[List[AlgorithmType]] = None,
) -> Dict[str, ScheduleResponse]:
    """
    Run multiple algorithms on the same input for side-by-side comparison.
    """
    if algorithms is None:
        algorithms = list(AlgorithmType)

    results: Dict[str, ScheduleResponse] = {}
    for algo in algorithms:
        try:
            result = run_algorithm(algo, processes, time_quantum)
            results[algo.value] = result
        except Exception as exc:
            # Include a minimal error response so the comparison still returns
            results[algo.value] = ScheduleResponse(
                algorithm=f"{algo.value} (error: {exc})",
                gantt_chart=[],
                metrics=ScheduleMetrics(),
            )
    return results


# ---------------------------------------------------------------------------
# Algorithm metadata for the frontend
# ---------------------------------------------------------------------------

ALGORITHM_INFO: List[AlgorithmInfo] = [
    AlgorithmInfo(
        name="First Come First Serve",
        key="fcfs",
        description="Processes are served in order of arrival. Non-preemptive.",
        time_complexity="O(n log n)",
        preemptive=False,
    ),
    AlgorithmInfo(
        name="Shortest Job First",
        key="sjf",
        description="Selects the process with the shortest burst time. Non-preemptive.",
        time_complexity="O(n²)",
        preemptive=False,
    ),
    AlgorithmInfo(
        name="Shortest Remaining Time First",
        key="srtf",
        description="Preemptive version of SJF – always runs the process with the least remaining burst.",
        time_complexity="O(n × T)",
        preemptive=True,
    ),
    AlgorithmInfo(
        name="Priority (Non-Preemptive)",
        key="priority_np",
        description="Selects the highest-priority (lowest number) ready process. Non-preemptive.",
        time_complexity="O(n²)",
        preemptive=False,
        needs_priority=True,
    ),
    AlgorithmInfo(
        name="Priority (Preemptive)",
        key="priority_p",
        description="Preemptive priority – a newly arrived higher-priority process preempts the running one.",
        time_complexity="O(n × T)",
        preemptive=True,
        needs_priority=True,
    ),
    AlgorithmInfo(
        name="Round Robin",
        key="round_robin",
        description="Each process gets a fixed time quantum in cyclic order.",
        time_complexity="O(n × T/Q)",
        preemptive=True,
        needs_time_quantum=True,
    ),
    AlgorithmInfo(
        name="Multilevel Queue",
        key="multilevel_queue",
        description="Processes are assigned to fixed queues based on priority. Higher queues preempt lower.",
        time_complexity="O(n × T)",
        preemptive=True,
        needs_priority=True,
    ),
    AlgorithmInfo(
        name="Multilevel Feedback Queue",
        key="mlfq",
        description="Dynamic queue assignment – processes are demoted when they use their full quantum.",
        time_complexity="O(n × T)",
        preemptive=True,
        needs_time_quantum=True,
    ),
]
