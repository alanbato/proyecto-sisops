import copy


class Process:

    def __init__(self, pid, arrival_time, cpu_time, priority, io_operations):
        self.pid = pid
        self.arrival_time = arrival_time
        self.cpu_time = cpu_time
        self.remaining_time = cpu_time
        self.priority = priority
        self.io_operations = io_operations
        self.io_operation_duration = 0
        self.waiting_time = 0
        self.execution_time = 0
        self.completion_time = 0


def comp2(g, h):
    x = cmp(g.cpu_time, h.cpu_time)
    if x == 0:
        x = cmp(g.pid, h.pid)
    return x


def updateque(ready, runtime, master):
    for x in master[:]:
        if x.arrival_time <= runtime:
            ready.append(x)
            j = master.index(x)
            del master[j]
    return ready


def block_status(blocked, ready):
    for process in blocked:
        process.io_operation_duration -= 1
        if process.io_operation_duration == 0:
            ready.append(process)


def sjf(process_total, master):
    print("\nSJF schduler")
    runtime = 0
    all_done = False
    ready = []
    done = []
    blocked = []
    ready = updateque(ready, runtime, master)  # Get process that were submitted
    while not all_done:
        ready.sort(cmp=comp2)  # Sort shortest burst time first
        print(runtime, ready[0].pid)

        while ready[0].execution_time != ready[0].cpu_time:  # Execute process until it finishes
            if ready[0].execution_time in ready[0].io_operations:
                ready[0].io_operation_duration = ready[0].io_operations[ready[0].execution_time]
                ready[0].execution_time += 1
                ready[0].remaining_time -= 1
                blocked.append(ready[0])
                del ready[0] 
            else:
                ready[0].execution_time += 1
                ready[0].remaining_time -= 1
            runtime += 1
            block_status(blocked, ready)
            # Get process that were submitted
            ready = updateque(ready, runtime, master)

        ready[0].completion_time = runtime  # Record the time process finished
        done.append(ready[0])  # Put process in the done queue
        del ready[0]  # Take process of the ready queue
        if len(done) == process_total:
            all_done = True
    print runtime, "Complete"
    return done


def main(processes):
    process_total = len(processes)
    master = []
    master = copy.deepcopy(processes)

    sjf(process_total, master)
