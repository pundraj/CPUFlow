"""
CSV Export Service – generate CSV content from scheduling results.
"""

from __future__ import annotations
import csv
import io
from typing import Dict

from app.models.schemas import ScheduleResponse


def export_single_csv(response: ScheduleResponse) -> str:
    """
    Convert a ScheduleResponse into CSV text.

    The CSV includes:
      - Gantt chart entries
      - Per-process metrics
      - Summary metrics
    """
    output = io.StringIO()
    writer = csv.writer(output)

    # Section 1: Algorithm name
    writer.writerow(["Algorithm", response.algorithm])
    writer.writerow([])

    # Section 2: Gantt Chart
    writer.writerow(["=== Gantt Chart ==="])
    writer.writerow(["Process", "Start", "End"])
    for entry in response.gantt_chart:
        writer.writerow([entry.process, entry.start, entry.end])
    writer.writerow([])

    # Section 3: Per-process metrics
    writer.writerow(["=== Per-Process Metrics ==="])
    writer.writerow(["PID", "Completion Time", "Turnaround Time", "Waiting Time", "Response Time"])
    m = response.metrics
    all_pids = sorted(m.completion_times.keys())
    for pid in all_pids:
        writer.writerow([
            pid,
            m.completion_times.get(pid, ""),
            m.turnaround_times.get(pid, ""),
            m.waiting_times.get(pid, ""),
            m.response_times.get(pid, ""),
        ])
    writer.writerow([])

    # Section 4: Summary metrics
    writer.writerow(["=== Summary Metrics ==="])
    writer.writerow(["Average Waiting Time", m.average_waiting_time])
    writer.writerow(["Average Turnaround Time", m.average_turnaround_time])
    writer.writerow(["CPU Utilization (%)", m.cpu_utilization])
    writer.writerow(["Throughput (proc/unit)", m.throughput])

    return output.getvalue()


def export_comparison_csv(results: Dict[str, ScheduleResponse]) -> str:
    """
    Export comparison results – all algorithms in one CSV.
    """
    output = io.StringIO()
    writer = csv.writer(output)

    writer.writerow(["=== Algorithm Comparison ==="])
    writer.writerow([])

    # Summary table
    writer.writerow([
        "Algorithm",
        "Avg Waiting Time",
        "Avg Turnaround Time",
        "CPU Utilization (%)",
        "Throughput",
    ])
    for key, resp in results.items():
        writer.writerow([
            resp.algorithm,
            resp.metrics.average_waiting_time,
            resp.metrics.average_turnaround_time,
            resp.metrics.cpu_utilization,
            resp.metrics.throughput,
        ])

    writer.writerow([])

    # Detailed sections
    for key, resp in results.items():
        writer.writerow([f"--- {resp.algorithm} ---"])
        writer.writerow(["Process", "Start", "End"])
        for entry in resp.gantt_chart:
            writer.writerow([entry.process, entry.start, entry.end])
        writer.writerow([])

    return output.getvalue()
