"""
Shortest Remaining Time First (SRTF) – Preemptive SJF
======================================================
- Preemptive: at each time unit, the process with the shortest remaining
  burst time is selected. A running process can be interrupted.
- Ties are broken by arrival time, then by PID.

Time Complexity: O(n × T) where T is the total time span.
"""

from __future__ import annotations
from typing import List, Dict, Tuple


def srtf_schedule(processes: List[Dict]) -> Tuple[List[Dict], Dict]:
    """
    Run preemptive SRTF scheduling.

    Parameters
    ----------
    processes : list of dict

    Returns
    -------
    gantt_chart, metrics
    """
    if not processes:
        return [], _empty_metrics()

    procs = [dict(p) for p in processes]
    n = len(procs)
    remaining = [p["burst_time"] for p in procs]
    completed_count = 0
    current_time = 0

    completion: Dict[str, int] = {}
    first_response: Dict[str, int] = {p["pid"]: -1 for p in procs}

    gantt_chart: List[Dict] = []
    prev_pid: str | None = None
    segment_start = 0

    # Handle zero-burst processes upfront
    for i, p in enumerate(procs):
        if p["burst_time"] == 0:
            completion[p["pid"]] = p["arrival_time"]
            first_response[p["pid"]] = 0
            completed_count += 1

    max_time = max(p["arrival_time"] for p in procs) + sum(p["burst_time"] for p in procs) + 1

    while completed_count < n and current_time < max_time:
        # Ready processes: arrived, remaining > 0
        ready = [
            i for i in range(n)
            if procs[i]["arrival_time"] <= current_time and remaining[i] > 0
        ]

        if not ready:
            # CPU idle – advance to the next arrival among unfinished processes
            future = [
                procs[i]["arrival_time"]
                for i in range(n) if remaining[i] > 0
            ]
            if not future:
                break
            next_arrival = min(future)
            if prev_pid is not None:
                gantt_chart.append({"process": prev_pid, "start": segment_start, "end": current_time})
            prev_pid = "Idle"
            segment_start = current_time
            current_time = next_arrival
            gantt_chart.append({"process": "Idle", "start": segment_start, "end": current_time})
            prev_pid = None
            segment_start = current_time
            continue

        # Pick process with shortest remaining time
        idx = min(ready, key=lambda i: (remaining[i], procs[i]["arrival_time"], procs[i]["pid"]))
        pid = procs[idx]["pid"]

        # Record first response
        if first_response[pid] == -1:
            first_response[pid] = current_time - procs[idx]["arrival_time"]

        # Context switch detection → save previous segment
        if pid != prev_pid:
            if prev_pid is not None:
                gantt_chart.append({"process": prev_pid, "start": segment_start, "end": current_time})
            prev_pid = pid
            segment_start = current_time

        # Execute for 1 time unit
        remaining[idx] -= 1
        current_time += 1

        # Check completion
        if remaining[idx] == 0:
            completion[pid] = current_time
            completed_count += 1
            gantt_chart.append({"process": pid, "start": segment_start, "end": current_time})
            prev_pid = None
            segment_start = current_time

    # Flush last segment
    if prev_pid is not None:
        gantt_chart.append({"process": prev_pid, "start": segment_start, "end": current_time})

    # Merge consecutive identical entries
    gantt_chart = _merge_gantt(gantt_chart)

    metrics = _compute_metrics(procs, completion, first_response, current_time)
    return gantt_chart, metrics


def _merge_gantt(chart: List[Dict]) -> List[Dict]:
    """Merge consecutive Gantt entries for the same process."""
    if not chart:
        return chart
    merged = [chart[0]]
    for entry in chart[1:]:
        if entry["process"] == merged[-1]["process"] and entry["start"] == merged[-1]["end"]:
            merged[-1]["end"] = entry["end"]
        else:
            merged.append(entry)
    return merged


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
        response[pid] = first_response.get(pid, 0) if first_response.get(pid, -1) >= 0 else 0

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
