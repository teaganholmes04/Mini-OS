"""
File Name: main.py
Description: Runs FCFS & RR, Prints gantt chart & metrics (All printing happens here)
Author: Teagan Holmes
Date: 5/12/2026
"""
from scheduler import ( #get scheduler methods
    sched_init,
    sched_shutdown,
    sched_create_process,
    sched_run_fcfs,
    sched_run_rr,
    sched_get_metrics,
    sched_slice_t,
)

#prints Gantt chart from slices.
def print_gantt(title: str, slices: list[sched_slice_t]) -> None:
    print(f"\n{title}") # title
    print("-" * len(title)) # underline title
    timeline = "|" #start timeline
    
    #loop through slices
    for s in slices:
        label = "idle" if s.pid == -1 else f"P{s.pid}" #label idle or process
        timeline += f" {label}({s.start_time}-{s.end_time}) |" # add timeline
    print(timeline)

#print metrics using sched api (wait, turn, completion)
def print_metrics(pids: list[int]) -> None:
    print("\nPID\tWait\tTurn\tComp")
    for pid in pids: # get results for each process
        res = sched_get_metrics(pid)
        if res == -1: #no data case
            print(f"{pid}\t<no data>") 
        else:
            wait, turn, comp = res
            print(f"{pid}\t{wait}\t{turn}\t{comp}") #final metrics

def main() -> None:
    #sample processes with a mix of arrival times
    processes = [
        (1, 0, 5),
        (2, 1, 3),
        (3, 2, 8),
        (4, 2, 6),
    ]
    pids = [p[0] for p in processes] # get pids
    assert sched_init(max_procs=10) == 0 # start sched
    for pid, arr, burst in processes: # add all processes
        rc = sched_create_process(pid, arr, burst) # create proccesses
        if rc != 0: # stop if failed
            raise RuntimeError(f"Failed to create process {pid}, rc={rc}")

    # fcfs
    fcfs_slices: list[sched_slice_t] = [] 
    rc = sched_run_fcfs(fcfs_slices, max_slices=64)
    if rc != 0:
        raise RuntimeError(f"FCFS scheduling failed, rc={rc}")
    print_gantt("FCFS Schedule", fcfs_slices)
    print_metrics(pids)

    # rr
    rr_slices: list[sched_slice_t] = []
    rc = sched_run_rr(quantum=2, slices=rr_slices, max_slices=128)
    if rc != 0:
        raise RuntimeError(f"RR scheduling failed, rc={rc}")

    print_gantt("Round Robin (q=2) Schedule", rr_slices)
    print_metrics(pids)

    sched_shutdown()


if __name__ == "__main__":
    main()
