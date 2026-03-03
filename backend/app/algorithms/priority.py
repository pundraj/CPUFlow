"""
Priority Scheduling Algorithm – Preemptive & Non-Preemptive
===========================================================
- Lower numeric value = higher priority (convention).
- Non-preemptive: once a process starts, it runs to completion.
- Preemptive: at every time unit, the highest-priority ready process runs.
- Ties: broken by arrival time, then PID.

Time Complexity:
  - Non-preemptive: O(n²)
  - Preemptive:     O(n × T)
"""

from __future__ import annotations
from typing import List, Dict, Tuple


# ============================= NON-PREEMPTIVE =============================

def priority_schedule_nonpreemptive(processes: List[Dict]) -> Tuple[List[Dict], Dict]:
    """Run non-preemptive priority scheduling."""
    if not processes:
        return [], _empty_metrics()

    procs = [dict(p) for p in processes]
    n = len(procs)

    gantt_chart: List[Dict] = []
    current_time = 0
    done = [False] * n
    completed = 0
    completion: Dict[str, int] = {}
    first_response: Dict[str, int] = {}

    while completed < n:
        ready = [
            i for i in range(n)
            if not done[i]
            and procs[i]["arrival_time"] <= current_time
            and procs[i]["burst_time"] > 0
        ]

        if not ready:
            # Handle zero-burst
            zeros = [i for i in range(n) if not done[i] and procs[i]["burst_time"] == 0]
            if zeros:
                for z in zeros:
                    done[z] = True
                    completion[procs[z]["pid"]] = procs[z]["arrival_time"]
                    first_response[procs[z]["pid"]] = 0
                    completed += 1
                continue

            next_arrival = min(
                procs[i]["arrival_time"] for i in range(n) if not done[i]
            )
            gantt_chart.append({"process": "Idle", "start": current_time, "end": next_arrival})
            current_time = next_arrival
            continue

        # Select highest priority (lowest number), tie-break: arrival, pid
        idx = min(ready, key=lambda i: (procs[i]["priority"], procs[i]["arrival_time"], procs[i]["pid"]))
        proc = procs[idx]

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


# =============================== PREEMPTIVE ===============================

def priority_schedule_preemptive(processes: List[Dict]) -> Tuple[List[Dict], Dict]:
    """Run preemptive priority scheduling."""
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
    prev_pid = None
    segment_start = 0

    # Zero-burst upfront
    for i, p in enumerate(procs):
        if p["burst_time"] == 0:
            completion[p["pid"]] = p["arrival_time"]
            first_response[p["pid"]] = 0
            completed_count += 1

    max_time = max(p["arrival_time"] for p in procs) + sum(p["burst_time"] for p in procs) + 1

    while completed_count < n and current_time < max_time:
        ready = [
            i for i in range(n)
            if procs[i]["arrival_time"] <= current_time and remaining[i] > 0
        ]

        if not ready:
            future = [procs[i]["arrival_time"] for i in range(n) if remaining[i] > 0]
            if not future:
                break
            next_arrival = min(future)
            if prev_pid is not None:
                gantt_chart.append({"process": prev_pid, "start": segment_start, "end": current_time})
            gantt_chart.append({"process": "Idle", "start": current_time, "end": next_arrival})
            current_time = next_arrival
            prev_pid = None
            segment_start = current_time
            continue

        idx = min(ready, key=lambda i: (procs[i]["priority"], procs[i]["arrival_time"], procs[i]["pid"]))
        pid = procs[idx]["pid"]

        if first_response[pid] == -1:
            first_response[pid] = current_time - procs[idx]["arrival_time"]

        if pid != prev_pid:
            if prev_pid is not None:
                gantt_chart.append({"process": prev_pid, "start": segment_start, "end": current_time})
            prev_pid = pid
            segment_start = current_time

        remaining[idx] -= 1
        current_time += 1

        if remaining[idx] == 0:
            completion[pid] = current_time
            completed_count += 1
            gantt_chart.append({"process": pid, "start": segment_start, "end": current_time})
            prev_pid = None
            segment_start = current_time

    if prev_pid is not None:
        gantt_chart.append({"process": prev_pid, "start": segment_start, "end": current_time})

    gantt_chart = _merge_gantt(gantt_chart)
    metrics = _compute_metrics(procs, completion, first_response, current_time)
    return gantt_chart, metrics


# ---------------------------------------------------------------------------
# Shared helpers
# ---------------------------------------------------------------------------

def _merge_gantt(chart):
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
