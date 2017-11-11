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
    io_operations = {}
    io_operation_duration = 0
    finish_time = 0

    def __init__(self, pid, arrival_time, cpu_time, priority=0,
        io_operation=False, io_operations=0, io_operation_duration=0):
        self.arrival_time = arrival_time
        self.cpu_time = cpu_time
        self.priority = priority
        self.io_operations = io_operations
        self.io_operation_duration

    def has_io(self):
        return io_operations.has_key(cpu_time - remaining_time)

    def perform_io(self):
        io_operation_duration = io_operation_start[cpu_time - remaining_time]

def processes_comp_arrival_time(a,b):
    return a.arrival_time < b.arrival_time

# Funciones auxiliares.
def processes_comp_srt(a,b):
    # Comparar tiempo restante de ejecución
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

# Procesos disponibles inicialmente.
processes = []

# Cola de listos ordenados pro SRT.
processes_ready = []

# Cola de procesos bloqueados por I/O.
processes_blocked = []

# Lista con los procesos que ya han terminado su ejecución.
processes_finished = []

# Instrucción de trabajo.
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

    processes.append(Process(pid=pid, arrival_time=arrival_time,
        cpu_time=cpu_time))

    command = raw_input("")
    command = command.split(" ")

# Total execution time in seconds.
time = 0

# Ejecución de los procesos
while len(processes) > 0:
    # Añadir los procesos a medida que pasa el tiempo.
    for process in processes:
        if process.arrival_time <= time:
            processes_ready.append(process)
            processes.remove(process)

    # Procesos Bloqueados
    for process in processes_blocked:
        process.io_operation_duration -= 1
        if process.io_operation_duration <= 0:
            processes_ready.append(process)
            processes_blocked.remove(process)

    # Ordenar los procesos en la cola de listos por su tiempo restante de
    # ejecución (SRT)
    processes_ready.sort(cmp=processes_comp_srt)

    # Ejectuar los primeros "N" elementos de la cola de listos, donde "N" es
    # la cantidad de CPU's disponibles, para simular que "N" CPU's corren esos
    # procesos.
    for i in range(0, min(cpus, len(processes_ready))):
        process = processes_ready[i]
        process.cpu_time -= 1
        # La interrupción I/O bloquea el proceso.
        if process.has_io():
            process.perform_io()
            processes_blocked.append(process)
            processes_ready.remove(process)
        if process.cpu_time <= 0:
            process.exit_time = time
            processes_finished.append(process)
            processes_ready.remove(process)

    time += 1
