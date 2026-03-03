"""
First Come First Serve (FCFS) Scheduling Algorithm
===================================================
- Non-preemptive: once a process starts, it runs to completion.
- Processes are served in order of arrival time.
- Ties in arrival time are broken by the order they appear in the input list.

Time Complexity: O(n log n)  (dominated by the initial sort)
"""

from __future__ import annotations
from typing import List, Dict, Tuple


def fcfs_schedule(processes: List[Dict]) -> Tuple[List[Dict], Dict]:
    """
    Run FCFS scheduling on the given process list.

    Parameters
    ----------
    processes : list of dict
        Each dict has keys: pid, arrival_time, burst_time, priority.

    Returns
    -------
    gantt_chart : list of dict  [{process, start, end}, ...]
    metrics     : dict          Comprehensive performance metrics.
    """
    if not processes:
        return [], _empty_metrics()

    # Sort by arrival time (stable sort preserves original order on ties)
    procs = sorted(processes, key=lambda p: p["arrival_time"])

    gantt_chart: List[Dict] = []
    current_time = 0
    completion: Dict[str, int] = {}
    first_response: Dict[str, int] = {}

    for proc in procs:
        pid = proc["pid"]
        arrival = proc["arrival_time"]
        burst = proc["burst_time"]

        # Skip zero-burst processes
        if burst == 0:
            completion[pid] = arrival
            first_response[pid] = 0
            continue

        # If CPU is idle, insert an idle block
        if current_time < arrival:
            gantt_chart.append({
                "process": "Idle",
                "start": current_time,
                "end": arrival,
            })
            current_time = arrival

        # Record response time (first time on CPU)
        first_response[pid] = current_time - arrival

        # Execute the process to completion
        gantt_chart.append({
            "process": pid,
            "start": current_time,
            "end": current_time + burst,
        })
        current_time += burst
        completion[pid] = current_time

    metrics = _compute_metrics(procs, completion, first_response, current_time)
    return gantt_chart, metrics


# ---------------------------------------------------------------------------
# Helper: compute standard metrics from completion times
# ---------------------------------------------------------------------------

def _compute_metrics(
    procs: List[Dict],
    completion: Dict[str, int],
    first_response: Dict[str, int],
    total_time: int,
) -> Dict:
    turnaround: Dict[str, int] = {}
    waiting: Dict[str, int] = {}
    response: Dict[str, int] = {}

    active_procs = [p for p in procs if p["burst_time"] > 0]

    for p in active_procs:
        pid = p["pid"]
        ct = completion.get(pid, 0)
        tat = ct - p["arrival_time"]
        wt = tat - p["burst_time"]
        turnaround[pid] = tat
        waiting[pid] = wt
        response[pid] = first_response.get(pid, 0)

    n = len(active_procs)
    total_burst = sum(p["burst_time"] for p in active_procs)
    min_arrival = min(p["arrival_time"] for p in procs) if procs else 0

    return {
        "completion_times": completion,
        "turnaround_times": turnaround,
        "waiting_times": waiting,
        "response_times": response,
        "average_waiting_time": round(sum(waiting.values()) / n, 2) if n else 0,
        "average_turnaround_time": round(sum(turnaround.values()) / n, 2) if n else 0,
        "cpu_utilization": round((total_burst / (total_time - min_arrival)) * 100, 2) if total_time > min_arrival else 0,
        "throughput": round(n / (total_time - min_arrival), 4) if total_time > min_arrival else 0,
    }


def _empty_metrics() -> Dict:
    return {
        "completion_times": {},
        "turnaround_times": {},
        "waiting_times": {},
        "response_times": {},
        "average_waiting_time": 0,
        "average_turnaround_time": 0,
        "cpu_utilization": 0,
        "throughput": 0,
    }
