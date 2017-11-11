# Sistemas Operativos LuJu 10
# Proyecto Final
# Equipo #8

# SRT:
# > Process with the smallest estimated run time to completion is run next.
# > Once a job begin executing, it runs to completion.
# > In SRT a running process may be preempted by a user process with a
#   shorter estimated run time.

# Estructuras de datos auxiliares.
class Process:
    pid = 0
    arrival_time = 0
    cpu_time = 0
    priority = 0
    io_operation = False
    io_operation_start = {}
    io_operation_duration = 0

    def __init__(self, pid, arrival_time, cpu_time, priority=0,
        io_operation=False, io_operation_start=0, io_operation_duration=0):
        self.arrival_time = arrival_time
        self.cpu_time = cpu_time
        self.priority = priority
        self.io_operation = io_operation
        self.io_operation_start = io_operation_start
        self.io_operation_duration

    def has_io(self, time):
        if io_operation_start[time] != 0:
            io_operation_duration = io_operation_start[time]
            io_operation = True

def processes_comp_arrival_time(a,b):
    return a.arrival_time < b.arrival_time

# Funciones auxiliares.
def processes_comp_srt(a,b):
    # Comparar tiempo restante de ejecución
    if a.io_operation != b.io_operation:
        return !a.io_operation
    if a.cpu_time != b.cpu_time:
        return a.cpu_time < b.cpu_time

# 2.1 Información inicial

# El sistema pide al usuario un string que indica la política de scheduling
# a utilizar.
scheduling_type = raw_input("")

# Validaciones de 'scheduling_type'

# El sistema pide al usuario el quantum en milisegundos (SRT no lo requiere)
quantum = raw_input("")

# Validaciones de 'quantum'

# El sistema pide al usuario el tiempo del cambio de contexto (context switch)
# en milisegundos.
context_switch_time = raw_input("")

# Validaciones de 'context_switch_time'

# El sistema pide al usuario indicar el numero de CPU's (1 al 10)
cpus = raw_input("")

# Validaciones de 'cpus'

# Inicialización del arreglo de procesos (el documento indica que en el
# input se van a recibir los procesos en orden.)
# Cada elemento es una tupla:
# (Llave (PID), [arrival_time, cpu_time, ...])
processes = []
processes_ready = []
processes_runnning = []
processes_blocked = []

command = raw_input("")
command = command.split(" ")

# 2.2. Procesar información de las tareas
while command[0] != "FIN":
    # Validar tamaño mínimo del comando (debe al menos incluir PID, arrival time
    # y CPU time)
    if (len(command) < 3):
        print("Formato inválido de proceso.")

    pid = command[0]
    arrival_time = command[1]
    cpu_time = command[2]

    # Process PRIORITY and IO input.
    if len(command) > 3:


    processes.append(Process(pid=pid, arrival_time=arrival_time,
        cpu_time=cpu_time))

    command = raw_input("")
    command = command.split(" ")

# Total execution time in seconds.
time = 0
# Ejecución de los procesos
while len(processes) > 0:
    processes_ready.sort(cmp=processes_comp_srt)

    for process in processes:
        if process.arrival_time <= time:
            processes_ready.append(process)
            processes.remove(process)

    for i in range(0, cpus, processes_running):
        processes_running.append(processes_ready[0])
        del processes_ready[0]

    for process in processes_running:
        process.cpu_time -= 1
        if process.has_io(time):
            processes_blocked.append(process)
            processes_runnning.remove(process)
        if process.cpu_time <= 0:
            processes_runnning.remove(process)

    time += 1
