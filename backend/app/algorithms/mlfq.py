"""
Multilevel Feedback Queue (MLFQ) Scheduling
=============================================
Three queues with increasing time quantums:
  Queue 0 (highest priority) – RR with quantum Q
  Queue 1                    – RR with quantum 2Q
  Queue 2 (lowest priority)  – FCFS

Rules:
  1. New processes enter Queue 0.
  2. If a process uses its full quantum without completing, it is demoted
     to the next lower queue.
  3. If a process voluntarily gives up the CPU (completes early), it stays
     at its current level.
  4. Higher-priority queues always preempt lower-priority queues.

Time Complexity: O(n × T)
"""

from __future__ import annotations
from collections import deque
from typing import List, Dict, Tuple


def mlfq_schedule(processes: List[Dict], time_quantum: int = 2) -> Tuple[List[Dict], Dict]:
    """
    Run MLFQ scheduling.

    Parameters
    ----------
    processes    : list of dict
    time_quantum : int – base quantum Q for Queue 0.

    Returns
    -------
    gantt_chart, metrics
    """
    if not processes:
        return [], _empty_metrics()

    Q = time_quantum
    quantums = [Q, 2 * Q, None]  # None → FCFS (run to completion)

    procs = sorted([dict(p) for p in processes], key=lambda p: (p["arrival_time"], p["pid"]))
    n = len(procs)

    remaining = {p["pid"]: p["burst_time"] for p in procs}
    arrival_map = {p["pid"]: p["arrival_time"] for p in procs}
    burst_map = {p["pid"]: p["burst_time"] for p in procs}
    queue_level: Dict[str, int] = {}  # tracks current queue level per process

    queues: Dict[int, deque] = {0: deque(), 1: deque(), 2: deque()}
    in_queue: set = set()

    gantt_chart: List[Dict] = []
    completion: Dict[str, int] = {}
    first_response: Dict[str, int] = {}
    current_time = 0
    proc_idx = 0

    # Handle zero-burst
    for p in procs:
        if p["burst_time"] == 0:
            completion[p["pid"]] = p["arrival_time"]
            first_response[p["pid"]] = 0

    def enqueue_arrivals(up_to: int):
        nonlocal proc_idx
        while proc_idx < n and procs[proc_idx]["arrival_time"] <= up_to:
            pid = procs[proc_idx]["pid"]
            if remaining.get(pid, 0) > 0 and pid not in in_queue:
                # New processes always enter Queue 0
                queue_level[pid] = 0
                queues[0].append(pid)
                in_queue.add(pid)
            proc_idx += 1

    enqueue_arrivals(current_time)

    max_time = max(p["arrival_time"] for p in procs) + sum(p["burst_time"] for p in procs) + 1

    while current_time < max_time:
        if all(remaining[p["pid"]] <= 0 for p in procs if p["burst_time"] > 0):
            break

        enqueue_arrivals(current_time)

        # Find highest-priority non-empty queue
        active_q = None
        for qid in [0, 1, 2]:
            if queues[qid]:
                active_q = qid
                break

        if active_q is None:
            future = [procs[i]["arrival_time"] for i in range(proc_idx, n) if remaining.get(procs[i]["pid"], 0) > 0]
            if not future:
                break
            next_arr = min(future)
            gantt_chart.append({"process": "Idle", "start": current_time, "end": next_arr})
            current_time = next_arr
            enqueue_arrivals(current_time)
            continue

        pid = queues[active_q].popleft()
        in_queue.discard(pid)

        if pid not in first_response:
            first_response[pid] = current_time - arrival_map[pid]

        q = quantums[active_q]
        exec_budget = q if q is not None else remaining[pid]

        seg_start = current_time
        ran = 0

        while ran < exec_budget and remaining[pid] > 0:
            current_time += 1
            ran += 1
            remaining[pid] -= 1
            enqueue_arrivals(current_time)

            # Preemption check: if a higher-priority queue has a process, stop
            if remaining[pid] > 0 and ran < exec_budget:
                higher = any(queues[qq] for qq in range(active_q))
                if higher:
                    break

        gantt_chart.append({"process": pid, "start": seg_start, "end": current_time})

        if remaining[pid] <= 0:
            completion[pid] = current_time
        else:
            # Determine if the process used its full quantum → demote
            used_full = (ran >= exec_budget) if exec_budget else False
            if used_full and active_q < 2:
                new_level = active_q + 1
            else:
                new_level = active_q  # stay at same level
            queue_level[pid] = new_level
            queues[new_level].append(pid)
            in_queue.add(pid)

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

    nn = len(active)
    total_burst = sum(burst_map[p["pid"]] for p in active)
    min_arrival = min(p["arrival_time"] for p in procs) if procs else 0

    return {
        "completion_times": completion,
        "turnaround_times": turnaround,
        "waiting_times": waiting,
        "response_times": response,
        "average_waiting_time": round(sum(waiting.values()) / nn, 2) if nn else 0,
        "average_turnaround_time": round(sum(turnaround.values()) / nn, 2) if nn else 0,
        "cpu_utilization": round((total_burst / (total_time - min_arrival)) * 100, 2) if total_time > min_arrival else 0,
        "throughput": round(nn / (total_time - min_arrival), 4) if total_time > min_arrival else 0,
    }


def _empty_metrics():
    return {
        "completion_times": {}, "turnaround_times": {}, "waiting_times": {},
        "response_times": {}, "average_waiting_time": 0,
        "average_turnaround_time": 0, "cpu_utilization": 0, "throughput": 0,
    }
