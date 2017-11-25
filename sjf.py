'''
 Sistemas Operativos LuJu 10
 Proyecto Final
 Equipo #8

 SJF:
 > Process with the smallest estimated run time to completion is run next.
 > Once a job begin executing, it runs to completion.
 > In SRT a running process may be preempted by a user process with a
   shorter estimated run time.
'''
import copy
import iohelper as io

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


def sjf(input_filename):

    print("SJF schduler")

    setup, processes = io.read_input(input_filename)
    policy, context_switch, cpus = setup

    # Verifica que la política sea SRT
    assert policy == 'SJF'

    process_total = len(processes)
    master = []
    master = copy.deepcopy(processes)

    runtime = 0
    all_done = False
    ready = []
    done = []
    blocked = []
    # Get process that were submitted
    ready = updateque(ready, runtime, master)
    while not all_done:
        ready.sort(cmp=comp2)  # Sort shortest burst time first
        process = ready[0]
        print(runtime, process.pid)

        while process.execution_time != process.cpu_time:  # Execute process until it finishes
            if process.has_io():
                print("Operacion I/O de {}".format(process.pid))
                process.perform_io()
                process.execution_time += 1
                process.remaining_time -= 1
                blocked.append(process)
                del process
                ready.sort(cmp=comp2)
            else:
                process.execution_time += 1
                process.remaining_time -= 1
            runtime += 1
            block_status(blocked, ready)
            # Get process that were submitted
            ready = updateque(ready, runtime, master)

        process.completion_time = runtime  # Record the time process finished
        done.append(process)  # Put process in the done queue
        del process  # Take process of the ready queue
        if len(done) == process_total:
            all_done = True
    print(runtime, "Complete")
    return done
