# Sistemas Operativos LuJu 10
# Proyecto Final
# Equipo #8

# SRT:
# > Process with the smallest estimated run time to completion is run next.
# > Once a job begin executing, it runs to completion.
# > In SRT a running process may be preempted by a user process with a
#   shorter estimated run time.

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

command = raw_input("")
command = command.split(" ")

# 2.2. Procesar información de las tareas

while command[0] != "FIN":
    # Validar tamaño mínimo del comando (debe al menos incluir PID, arrival time
    # y CPU time)

    pid = command[0]
    arrival_time = command[1]
    cpu_time = command[2]

    processes.append(pid, [arrival_time, cpu_time])

# Ejecución de los procesos
