"""
Filename: test_sched.py
Description: For running basic tests for FCFS ordering, metric sanity,
and RR premption
Author: Teagan Holmes
Date: 5/12/2026

"""
import pytest #test library
from scheduler import ( #import scheduler methods
    sched_init,
    sched_shutdown,
    sched_create_process,
    sched_run_fcfs,
    sched_run_rr,
    sched_get_metrics,
    sched_slice_t,
)


@pytest.fixture(autouse=True) #refresh scheduler - runs before/after every test
def reset_scheduler():
    sched_shutdown()
    sched_init(10)
    yield #test running here
    sched_shutdown() #clear out info post-test

#test FCFS
def test_fcfs_simple_order():
    sched_create_process(1, 0, 3) #process 1
    sched_create_process(2, 1, 2) #process 2
    slices: list[sched_slice_t] = [] #empty list for slices
    
    rc = sched_run_fcfs(slices, max_slices=10) #run FCFS
    assert rc == 0 #make sure FCFS worked
    first_real = next(s for s in slices if s.pid != -1) # -1 skips idle slices; pulls real slices to add to list
    assert first_real.pid == 1 #ensures CPU runs in exact order

#Test Round Robin
def test_rr_quantum_effect():
    sched_create_process(1, 0, 5) # process 1
    sched_create_process(2, 0, 5) # process 2
    slices: list[sched_slice_t] = [] #empty list to store slices here
    
    rc = sched_run_rr(quantum=2, slices=slices, max_slices=20) #run RR
    assert rc == 0 # make sure alternates between slices
    pids = [s.pid for s in slices if s.pid != -1][:4] # get first 4 real
    assert pids == [1, 2, 1, 2] # alternate between slices

def test_metrics_non_negative():
    sched_create_process(1, 0, 4) 
    slices: list[sched_slice_t] = [] 
    rc = sched_run_fcfs(slices, max_slices=10) # run FCFS
    assert rc == 0
    
    res = sched_get_metrics(1) # get metrics
    assert res != -1 # make sure they exist
    wait, turn, comp = res # unpack values
    assert wait >= 0 #make sure valid wait, turn, comp times (non neg numbers)
    assert turn >= 0
    assert comp >= 0
