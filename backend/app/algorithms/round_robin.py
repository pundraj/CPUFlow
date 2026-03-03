"""
Round Robin (RR) Scheduling Algorithm
======================================
- Preemptive: each process gets a fixed *time quantum* on the CPU.
- If a process doesn't finish within the quantum, it goes to the back
  of the ready queue.
- Ties in arrival time are handled by insertion order.

Time Complexity: O(n × (total_burst / time_quantum))
"""

from __future__ import annotations
from collections import deque
from typing import List, Dict, Tuple


def round_robin_schedule(processes: List[Dict], time_quantum: int = 2) -> Tuple[List[Dict], Dict]:
    """
    Run Round Robin scheduling.

    Parameters
    ----------
    processes    : list of dict
    time_quantum : int (>= 1)

    Returns
    -------
    gantt_chart, metrics
    """
    if not processes:
        return [], _empty_metrics()

    procs = sorted([dict(p) for p in processes], key=lambda p: (p["arrival_time"], p["pid"]))
    n = len(procs)
    remaining = {p["pid"]: p["burst_time"] for p in procs}
    arrival_map = {p["pid"]: p["arrival_time"] for p in procs}
    burst_map = {p["pid"]: p["burst_time"] for p in procs}

    gantt_chart: List[Dict] = []
    completion: Dict[str, int] = {}
    first_response: Dict[str, int] = {}

    ready_queue: deque = deque()
    current_time = 0
    idx = 0  # pointer into sorted procs list
    in_queue = set()

    # Handle zero-burst processes
    while idx < n and procs[idx]["burst_time"] == 0:
        completion[procs[idx]["pid"]] = procs[idx]["arrival_time"]
        first_response[procs[idx]["pid"]] = 0
        idx += 1

    # Enqueue processes arriving at time 0
    while idx < n and procs[idx]["arrival_time"] <= current_time:
        if procs[idx]["burst_time"] > 0:
            ready_queue.append(procs[idx]["pid"])
            in_queue.add(procs[idx]["pid"])
        else:
            completion[procs[idx]["pid"]] = procs[idx]["arrival_time"]
            first_response[procs[idx]["pid"]] = 0
        idx += 1

    while ready_queue or idx < n:
        if not ready_queue:
            # CPU idle – advance time
            next_arrival = procs[idx]["arrival_time"]
            gantt_chart.append({"process": "Idle", "start": current_time, "end": next_arrival})
            current_time = next_arrival
            while idx < n and procs[idx]["arrival_time"] <= current_time:
                pid = procs[idx]["pid"]
                if remaining.get(pid, 0) > 0 and pid not in in_queue:
                    ready_queue.append(pid)
                    in_queue.add(pid)
                elif remaining.get(pid, 0) == 0:
                    completion[pid] = procs[idx]["arrival_time"]
                    first_response[pid] = 0
                idx += 1
            continue

        pid = ready_queue.popleft()
        in_queue.discard(pid)

        if pid not in first_response:
            first_response[pid] = current_time - arrival_map[pid]

        exec_time = min(time_quantum, remaining[pid])
        gantt_chart.append({
            "process": pid,
            "start": current_time,
            "end": current_time + exec_time,
        })
        current_time += exec_time
        remaining[pid] -= exec_time

        # Enqueue newly arrived processes BEFORE re-enqueueing the current one
        while idx < n and procs[idx]["arrival_time"] <= current_time:
            npid = procs[idx]["pid"]
            if remaining.get(npid, 0) > 0 and npid not in in_queue:
                ready_queue.append(npid)
                in_queue.add(npid)
            elif remaining.get(npid, 0) == 0 and npid not in completion:
                completion[npid] = procs[idx]["arrival_time"]
                first_response.setdefault(npid, 0)
            idx += 1

        if remaining[pid] > 0:
            ready_queue.append(pid)
            in_queue.add(pid)
        else:
            completion[pid] = current_time

    # Merge consecutive same-process entries
    gantt_chart = _merge_gantt(gantt_chart)

    metrics = _compute_metrics(procs, completion, first_response, current_time, burst_map)
    return gantt_chart, metrics


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


def _compute_metrics(procs, completion, first_response, total_time, burst_map):
    turnaround, waiting, response = {}, {}, {}
    active = [p for p in procs if p["burst_time"] > 0]
    for p in active:
        pid = p["pid"]
        ct = completion.get(pid, 0)
        tat = ct - p["arrival_time"]
        wt = tat - burst_map[pid]
        turnaround[pid] = tat
        waiting[pid] = wt
        response[pid] = first_response.get(pid, 0)

    n = len(active)
    total_burst = sum(burst_map[p["pid"]] for p in active)
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
