# Scheduling Algorithms Package
from .fcfs import fcfs_schedule
from .sjf import sjf_schedule
from .srtf import srtf_schedule
from .priority import priority_schedule_nonpreemptive, priority_schedule_preemptive
from .round_robin import round_robin_schedule
from .multilevel_queue import multilevel_queue_schedule
from .mlfq import mlfq_schedule

__all__ = [
    "fcfs_schedule",
    "sjf_schedule",
    "srtf_schedule",
    "priority_schedule_nonpreemptive",
    "priority_schedule_preemptive",
    "round_robin_schedule",
    "multilevel_queue_schedule",
    "mlfq_schedule",
]
