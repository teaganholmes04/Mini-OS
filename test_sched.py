"""
Basic tests for the scheduling subsystem.

These are not exhaustive, but they demonstrate:
- FCFS ordering
- RR preemption
- Metric sanity
"""

import pytest
from sched import (
    sched_init,
    sched_shutdown,
    sched_create_process,
    sched_run_fcfs,
    sched_run_rr,
    sched_get_metrics,
    sched_slice_t,
)


@pytest.fixture(autouse=True)
def reset_scheduler():
    sched_shutdown()
    sched_init(10)
    yield
    sched_shutdown()


def test_fcfs_simple_order():
    sched_create_process(1, 0, 3)
    sched_create_process(2, 1, 2)

    slices: list[sched_slice_t] = []
    rc = sched_run_fcfs(slices, max_slices=10)
    assert rc == 0

    # First non-idle slice should be P1
    first_real = next(s for s in slices if s.pid != -1)
    assert first_real.pid == 1


def test_rr_quantum_effect():
    sched_create_process(1, 0, 5)
    sched_create_process(2, 0, 5)

    slices: list[sched_slice_t] = []
    rc = sched_run_rr(quantum=2, slices=slices, max_slices=20)
    assert rc == 0

    # Expect alternating pattern at least at the start
    pids = [s.pid for s in slices if s.pid != -1][:4]
    assert pids == [1, 2, 1, 2]


def test_metrics_non_negative():
    sched_create_process(1, 0, 4)
    slices: list[sched_slice_t] = []
    rc = sched_run_fcfs(slices, max_slices=10)
    assert rc == 0

    res = sched_get_metrics(1)
    assert res != -1
    wait, turn, comp = res
    assert wait >= 0
    assert turn >= 0
    assert comp >= 0
