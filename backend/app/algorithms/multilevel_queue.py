"""
Multilevel Queue Scheduling
============================
Three fixed-priority queues:
  Queue 0 (System / highest priority) – Round Robin (quantum = 2)
  Queue 1 (Interactive)               – Round Robin (quantum = 4)
  Queue 2 (Batch / lowest priority)   – FCFS

Processes are assigned to queues based on their priority value:
  priority 0-3  → Queue 0
  priority 4-6  → Queue 1
  priority 7+   → Queue 2

Higher-priority queues preempt lower-priority queues.

Time Complexity: O(n × T)
"""

from __future__ import annotations
from collections import deque
from typing import List, Dict, Tuple


# Queue definitions: (queue_id, priority_range, scheduling_type, quantum)
QUEUE_CONFIG = [
    (0, range(0, 4), "rr", 2),
    (1, range(4, 7), "rr", 4),
    (2, range(7, 1000), "fcfs", None),
]


def multilevel_queue_schedule(processes: List[Dict], time_quantum: int = 2) -> Tuple[List[Dict], Dict]:
    """
    Run multilevel queue scheduling.

    Parameters
    ----------
    processes    : list of dict
    time_quantum : int – unused directly; queue has its own quantums.

    Returns
    -------
    gantt_chart, metrics
    """
    if not processes:
        return [], _empty_metrics()

    procs = sorted([dict(p) for p in processes], key=lambda p: (p["arrival_time"], p["pid"]))
    n = len(procs)

    # Assign each process to a queue level
    queue_assignment: Dict[str, int] = {}
    for p in procs:
        for qid, prange, _, _ in QUEUE_CONFIG:
            if p["priority"] in prange:
                queue_assignment[p["pid"]] = qid
                break
        else:
            queue_assignment[p["pid"]] = 2  # default: batch

    remaining = {p["pid"]: p["burst_time"] for p in procs}
    arrival_map = {p["pid"]: p["arrival_time"] for p in procs}
    burst_map = {p["pid"]: p["burst_time"] for p in procs}

    # Ready queues per level
    queues: Dict[int, deque] = {0: deque(), 1: deque(), 2: deque()}
    in_queue: set = set()

    gantt_chart: List[Dict] = []
    completion: Dict[str, int] = {}
    first_response: Dict[str, int] = {}
    current_time = 0
    proc_idx = 0

    # Zero-burst
    for p in procs:
        if p["burst_time"] == 0:
            completion[p["pid"]] = p["arrival_time"]
            first_response[p["pid"]] = 0

    def enqueue_arrivals(up_to_time: int):
        nonlocal proc_idx
        while proc_idx < n and procs[proc_idx]["arrival_time"] <= up_to_time:
            pid = procs[proc_idx]["pid"]
            if remaining.get(pid, 0) > 0 and pid not in in_queue:
                ql = queue_assignment[pid]
                queues[ql].append(pid)
                in_queue.add(pid)
            proc_idx += 1

    enqueue_arrivals(current_time)

    max_time = max(p["arrival_time"] for p in procs) + sum(p["burst_time"] for p in procs) + 1

    while current_time < max_time:
        # Check if all done
        if all(remaining[p["pid"]] <= 0 for p in procs if p["burst_time"] > 0):
            break

        enqueue_arrivals(current_time)

        # Find the highest-priority non-empty queue
        active_q = None
        for qid in [0, 1, 2]:
            if queues[qid]:
                active_q = qid
                break

        if active_q is None:
            # CPU idle
            future = [procs[i]["arrival_time"] for i in range(proc_idx, n) if remaining.get(procs[i]["pid"], 0) > 0]
            if not future:
                break
            next_arr = min(future)
            gantt_chart.append({"process": "Idle", "start": current_time, "end": next_arr})
            current_time = next_arr
            enqueue_arrivals(current_time)
            continue

        _, _, sched_type, quantum = QUEUE_CONFIG[active_q]
        pid = queues[active_q].popleft()
        in_queue.discard(pid)

        if pid not in first_response:
            first_response[pid] = current_time - arrival_map[pid]

        if sched_type == "rr":
            exec_time = min(quantum, remaining[pid])
        else:
            # FCFS – run to completion BUT can be preempted if a higher-queue process arrives
            exec_time = remaining[pid]

        # For FCFS queue, simulate one unit at a time to allow preemption by higher queues
        if sched_type == "fcfs":
            exec_time = 1  # will loop

        # Execute
        start_t = current_time

        if sched_type == "rr":
            # Run for exec_time, but check for higher-priority arrivals each unit
            ran = 0
            seg_start = current_time
            while ran < exec_time:
                current_time += 1
                ran += 1
                remaining[pid] -= 1
                enqueue_arrivals(current_time)
                # If a higher-priority queue now has something, preempt
                if remaining[pid] > 0:
                    higher_ready = any(queues[q] for q in range(active_q))
                    if higher_ready:
                        break
                if remaining[pid] == 0:
                    break
            gantt_chart.append({"process": pid, "start": seg_start, "end": current_time})
        else:
            # FCFS: one tick
            current_time += 1
            remaining[pid] -= 1
            enqueue_arrivals(current_time)
            gantt_chart.append({"process": pid, "start": start_t, "end": current_time})

        if remaining[pid] > 0:
            queues[active_q].append(pid)
            in_queue.add(pid)
        else:
            completion[pid] = current_time

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
