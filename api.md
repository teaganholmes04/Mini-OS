Document explaining how the API works.

1. Initialization
   *int sched_init(int max_procs) sets up the scheduler.
   Parameters:
       max_procs - max # of processes scheduler can have
   Returns:
       0 if successful
       -1 if max_procs is invalid
   
2. Shutdown
    void sched_shutdown(void)
    * Shuts down scheduler
    
3. Process Management

3.1 Create Process
    int sched_create_process(int pid, int arrival, int burst)
    * Adds new process to scheduler
    Parameters:
        *pid: unique process ID
        *arrival: process arrival time
        *burst: CPU burst time
    Returns:
        0 if successful
        -1 if table full
        -2 if pid already exists
        -3 if arrival or burst times are invalid
3.2 Terminate Process
    int sched_terminate_process(int pid)
    *Terminates a process based on its pid
    Parameters:
        *pid: process ID
    Returns:
        *0 when successful
        *-1 if process doesn't exist
4. Scheduling Algorithms
    4.1: Run FCFS algorithm
        int sched_run_fcfs(list[sched_slice_t] slices, int max_slices)
        Parameters:
            *slices: list storing sched_slice_t data
            *max_slices: max # of slices the list can hold
        Returns:
            *0 when successful
            *-1 if no active proccesses
            *-2 if no enough slices in list
    4.2: Run Round Robin Algorithm
        int sched_run_rr(int quantum, list[sched_slice_t] slices, int max_slices)
        * Runs Round Robin algorithm
        Parameters:
            *
        Returns:
            *0 when successful
            *-1 if no active proccesses
            *-2 if no enough slices in list
            *-3 if invalid quantum value
5. Get Metrics
    sched_get_metrics(int pid) -> (waiting, turnaround, completion) | -1
    * Gets performance metrics for proccesses after scheduling is done
    Parameters:
        *pid: Proccess ID
    Returns:
        *waiting, turnaround, completion data if successful (proccess exists & scheduled)
        *-1 if proccess doesn't exist or hasn't been scheduled yet
