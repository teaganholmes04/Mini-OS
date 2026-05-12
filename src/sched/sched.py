"""
File Name: sched.py
Description:
Author: Teagan Holmes
Date: 5/12/2026

Rules for API:
* no printing inside scheduler methods
* scheduler state in this file only
* 0 = success; - = failure/error (All methods return 0 when successful (unless stated); Negatives mean errors which are expanded on in comments)
* all public methods start with sched_


"""
#imports
from dataclasses import dataclass, field
from typing import List, Optional, Tuple

#internal data structures
@dataclass
class _PCB: #PCB used by scheduler
    pid: int
    arrival: int
    burst: int
    remaining: int = field(init=False)
    start: int = -1
    completion: int = -1
    waiting: int = 0
    turnaround: int = 0
    active: bool = True

    def __post_init__(self):
        self.remaining = self.burst #start remaining time = burst time

@dataclass
class sched_slice_t:
    """
    class for single chunk of CPU execution time.
    pid = -1 means CPU was idle
    """
    pid: int
    start_time: int
    end_time: int

#scheduler state
_table: List[_PCB] = []
_capacity: int = 0
_scheduled: bool = False


#start scheduler
def sched_init(max_procs: int) -> int:
    """
    set up/start scheduler.
    errors:
    1  if max_procs is invalid
    """
    global _table, _capacity, _scheduled
    if max_procs <= 0:
        return -1
    
    _capacity = max_procs
    _table = []
    _scheduled = False
    return 0
#restart/term scheduler
def sched_shutdown() -> None:
    """clear all info from scheduler."""
    global _table, _capacity, _scheduled
    _table = []
    _capacity = 0
    _scheduled = False

# process methods
def _find(pid: int) -> Optional[_PCB]:
    """search for process using pid."""
    for p in _table:
        if p.pid == pid and p.active:
            return p
    return None
#add process
def sched_create_process(pid: int, arrival: int, burst: int) -> int:
    """
    add a process to the schuedler.
    errors:
       -1   if table full
       -2   if pid exists prior
       -3   if values invalid
    """
    global _scheduled #unsched

    if len(_table) >= _capacity: # check capacityy
        return -1
    if arrival < 0 or burst <= 0: # make sure inputs arent 0/exist
        return -3
    if _find(pid) is not None: # make sure no duplicates
        return -2

    _table.append(_PCB(pid, arrival, burst)) # add the process
    _scheduled = False
    return 0 # success

#term process
def sched_terminate_process(pid: int) -> int:
    """
    show process as inactive
    errors:
    -1   if pid not found
    """
    global _scheduled
    p = _find(pid)
    if p is None:
        return -1
    
    p.active = False
    _scheduled = False
    return 0


# FCFS scheduling methods
def sched_run_fcfs(slices: List[sched_slice_t], max_slices: int) -> int:
    """
    runs FCFS scheduling.
    parameters:
        slices: a list that will be filled with sched_slice_t data
        max_slices: max # of slices allowed
    errors:
       -1   no active processes
       -2   slices buffer is too small
    """
    global _scheduled
    active = [p for p in _table if p.active]
    if not active:
        return -1
    
    active.sort(key=lambda p: p.arrival) #sort by arrival time
    time = 0
    slice_count = 0
    for p in active:
        if time < p.arrival: #CPU waits for next process to arrive
            if slice_count >= max_slices: #too many slices -> stop
                return -2
            slices.append(sched_slice_t(-1, time, p.arrival)) #idle slice
            slice_count += 1 #count and go to next
            time = p.arrival #move time up     
        if slice_count >= max_slices: #process runs until fin
            return -2
        
        p.start = time #start tie
        time += p.burst # run process
        p.completion = time # fin time
        p.turnaround = p.completion - p.arrival # calc total turnaround 
        p.waiting = p.turnaround - p.burst # get wait time
        slices.append(sched_slice_t(p.pid, p.start, p.completion)) # append slice
        slice_count += 1 # go to next
        
    _scheduled = True
    return 0

# round robin scheduling
def sched_run_rr(quantum: int, slices: List[sched_slice_t], max_slices: int) -> int:
    """
    Round Robin scheduling.
    Parameters:
        quantum: time slice (must be > 0)
        slices: list with sched_slice_t data
        max_slices: max # of slices allowed

    errors:
       -1   no active processes
       -2   slices buffer is too small
       -3   quantum is invalid
    """
    global _scheduled

    if quantum <= 0: #make sure quantum is not negative (invalid)
        return -3
    active = [p for p in _table if p.active] # only use active processes
    if not active: # no active -> no run
        return -1

    # reset values before startinf RR
    for p in active: 
        p.remaining = p.burst 
        p.start = -1
        p.completion = -1

    active.sort(key=lambda p: p.arrival) # sort by arrival
    time = 0 # system clock
    queue: List[_PCB] = [] #queue
    slice_count = 0 #slice counter
    completed = 0 # amt of finished processes
    
    # add any process thats already there (time 0)
    for p in active:
        if p.arrival == 0:
            queue.append(p)

    while completed < len(active): # keeps running until all r done
        # if queue empty, CPU does nothing
        if not queue:
            next_arrival = min(p.arrival for p in active if p.remaining > 0)
            if slice_count >= max_slices: #if maxed out slices
                return -2
            slices.append(sched_slice_t(-1, time, next_arrival)) #add slice
            slice_count += 1
            time = next_arrival
            for p in active: # add new proccesses
                if p.arrival <= time and p.remaining > 0 and p not in queue:
                    queue.append(p)
            continue
        
        p = queue.pop(0) # next process
        if p.remaining <= 0 or p.arrival > time: #skip any invalid
            continue
        if p.start == -1:
            p.start = time

        run_time = min(quantum, p.remaining)
        start = time
        time += run_time
        p.remaining -= run_time
        if slice_count >= max_slices:
            return -2

        slices.append(sched_slice_t(p.pid, start, time))
        slice_count += 1
        # add processes to queue that arrived during this time slot
        for q in active:
            if q.remaining > 0 and q.arrival > start and q.arrival <= time and q not in queue:
                queue.append(q)
        if p.remaining > 0:
            queue.append(p)
        else:
            p.completion = time
            p.turnaround = p.completion - p.arrival
            p.waiting = p.turnaround - p.burst
            completed += 1

    _scheduled = True
    return 0

# metrics
def sched_get_metrics(pid: int) -> Tuple[int, int, int] | int:
    """
    retrurns sched stats for processes

    errors:
        (waiting, turnaround, completion) on success
        -1 error means pid unfound, thus no metrics
    """
    if not _scheduled:
        return -1
    p = _find(pid)
    if p is None or p.completion < 0:
        return -1
    return p.waiting, p.turnaround, p.completion
