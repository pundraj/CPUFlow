"""
Shortest Job First (SJF) – Non-Preemptive Scheduling Algorithm
===============================================================
- Non-preemptive: the running process is not interrupted.
- Among ready processes, the one with the shortest burst time is selected.
- Ties are broken by arrival time, then by PID.

Time Complexity: O(n²) in the worst case (selection at each step).
"""

from __future__ import annotations
from typing import List, Dict, Tuple


def sjf_schedule(processes: List[Dict]) -> Tuple[List[Dict], Dict]:
    """
    Run non-preemptive SJF scheduling.

    Parameters
    ----------
    processes : list of dict
        Each dict has keys: pid, arrival_time, burst_time, priority.

    Returns
    -------
    gantt_chart, metrics
    """
    if not processes:
        return [], _empty_metrics()

    procs = [dict(p) for p in processes]  # shallow copy
    n = len(procs)

    gantt_chart: List[Dict] = []
    current_time = 0
    completed = 0
    done = [False] * n
    completion: Dict[str, int] = {}
    first_response: Dict[str, int] = {}

    while completed < n:
        # Find all ready processes (arrived and not done)
        ready = [
            i for i in range(n)
            if not done[i]
            and procs[i]["arrival_time"] <= current_time
            and procs[i]["burst_time"] > 0
        ]

        if not ready:
            # CPU is idle – advance to the nearest arrival
            next_arrival = min(
                procs[i]["arrival_time"] for i in range(n) if not done[i]
            )
            gantt_chart.append({"process": "Idle", "start": current_time, "end": next_arrival})
            current_time = next_arrival
            continue

        # Select process with shortest burst time (tie-break: arrival, then pid)
        idx = min(ready, key=lambda i: (procs[i]["burst_time"], procs[i]["arrival_time"], procs[i]["pid"]))
        proc = procs[idx]

        # Skip zero-burst
        if proc["burst_time"] == 0:
            done[idx] = True
            completion[proc["pid"]] = current_time
            first_response[proc["pid"]] = 0
            completed += 1
            continue

        first_response[proc["pid"]] = current_time - proc["arrival_time"]
        gantt_chart.append({
            "process": proc["pid"],
            "start": current_time,
            "end": current_time + proc["burst_time"],
        })
        current_time += proc["burst_time"]
        completion[proc["pid"]] = current_time
        done[idx] = True
        completed += 1

    metrics = _compute_metrics(procs, completion, first_response, current_time)
    return gantt_chart, metrics


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _compute_metrics(procs, completion, first_response, total_time):
    turnaround, waiting, response = {}, {}, {}
    active = [p for p in procs if p["burst_time"] > 0]

    for p in active:
        pid = p["pid"]
        ct = completion.get(pid, 0)
        tat = ct - p["arrival_time"]
        wt = tat - p["burst_time"]
        turnaround[pid] = tat
        waiting[pid] = wt
        response[pid] = first_response.get(pid, 0)

    n = len(active)
    total_burst = sum(p["burst_time"] for p in active)
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


def _empty_metrics():
    return {
        "completion_times": {}, "turnaround_times": {}, "waiting_times": {},
        "response_times": {}, "average_waiting_time": 0,
        "average_turnaround_time": 0, "cpu_utilization": 0, "throughput": 0,
    }
