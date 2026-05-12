"""
Filename: __init__.py
Description: sets up sched package without needing to directly import everything from sched
Author: Teagan Holmes
Date: 5/12/2026

"""

from .sched import (
    # Start, term scheduler; Create & term processes; Run FCFS & RR; Get metrics; slice list
    sched_init,
    sched_shutdown,
    sched_create_process,
    sched_terminate_process,
    sched_run_fcfs,
    sched_run_rr,
    sched_get_metrics,
    sched_slice_t,
)
