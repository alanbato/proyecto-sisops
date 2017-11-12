# Sistemas Operativos LuJu 10
# Proyecto Final
# Equipo #8

# SRT:
# > Process with the smallest estimated run time to completion is run next.
# > Once a job begin executing, it runs to completion.
# > In SRT a running process may be preempted by a user process with a
#   shorter estimated run time.

# Funciones auxiliares.
import iohelper as io


def srt_scheduling(input_filename):
    '''Política de Scheduling de SRT'''
    # Procesos disponibles inicialmente.
    setup, processes = io.read_input(input_filename)
    policy, context_switch, cpus = setup

    # Verifica que la política sea SRT
    assert(policy == 'SRT')

    # Cola de listos ordenados pro SRT.
    processes_ready = []

    # Cola de procesos bloqueados por I/O.
    processes_blocked = []

    # Lista con los procesos que ya han terminado su ejecución.
    processes_finished = []

    # Total execution time in seconds.
    time = 0

    # Función que revisa si aún hay procesos que procesar
    def pending_processes():
        return (len(processes) +
                len(processes_ready) +
                len(processes_blocked))

    # Ejecución de los procesos
    while pending_processes() > 0:
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
        processes_ready.sort(key=lambda x: x.remaining_time)

        # Ejectuar los primeros "N" elementos de la cola de listos,
        # donde "N" es la cantidad de CPU's disponibles,
        # para simular que "N" CPU's corren esos procesos.
        for i in range(0, min(cpus, len(processes_ready))):
            process = processes_ready[i]
            process.remaining_time -= 1
            # La interrupción I/O bloquea el proceso.
            if process.has_io():
                process.perform_io()
                processes_blocked.append(process)
                processes_ready.remove(process)
            if process.remaining_time <= 0:
                process.exit_time = time
                processes_finished.append(process)
                processes_ready.remove(process)
        print('Tiempo {}:'.format(time))
        print('Procesos en Cola de Listos:')
        print([proc.status() for proc in processes_ready])
        for i in range(1, cpus):
            print('CPU {}:'.format(i))
            # TODO: Imprimir el proceso en ejecución de cada CPU
        print('Procesos Bloqueados:')
        print([proc.status() for proc in processes_blocked])
        time += 1
    return processes_finished
