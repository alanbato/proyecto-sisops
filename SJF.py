'''
 Sistemas Operativos LuJu 10
 Proyecto Final
 Equipo #8

 SJF:
 > Process with the smallest estimated run time to completion is run next.
 > Once a job begin executing, it runs to completion.
'''

import iohelp as io
import pandas as pd

def sjf_scheduling(setup, processes):
    '''Política de Scheduling de SJF'''
    # Obtención de los parámetros del simulador
    policy, context_switch, cpus = setup
    cpu_dict = {'cpu_{}'.format(i): None for i in range(1, cpus + 1)}
    context_dict = {'cpu_{}'.format(i): 0 for i in range(1, cpus + 1)}

    # Verifica que la política sea SJF
    assert(policy == 'SJF')

    # Cola de listos ordenados a ser ordenada por SJF.
    processes_ready = []

    # Cola de procesos bloqueados por I/O.
    processes_blocked = []

    # Lista con los procesos que ya han terminado su ejecución.
    processes_finished = []

    # Tiempo total de ejecución
    time = 0

    # Tabla con para mostrar los resultados
    output_table = io.OutputTable(num_cpus=cpus)

    # Función que revisa si aún hay procesos que procesar
    def pending_processes():
        return (len(processes) +
                len(processes_ready) +
                len(processes_blocked) +
                len([proc for proc in cpu_dict.values()
                     if proc is not None]))

    # Ejecución de los procesos
    while pending_processes() > 0:
        for cpu, process in cpu_dict.items():
            if process is not None:
                if context_dict[cpu] > 0:
                    context_dict[cpu] -= 1
                    continue
                process.remaining_time -= 1
                # Si el proceso ya terminó, lo agrega a la lista de terminados
                if process.remaining_time == 0:
                    cpu_dict[cpu] = None
                    process.finish_time = time
                    processes_finished.append(process)
                # Si el proceso tiene IO, lo bloquea y hace su IO
                elif process.has_io():
                    cpu_dict[cpu] = None
                    process.perform_io()
                    processes_blocked.append(process)
        # Agrega los procesos que terminaron su IO a la cola de listos
        for process in processes_blocked:
            process.io_operation_duration -= 1
            if process.io_operation_duration < 0:
                processes_ready.append(process)
        # Remueve todos los que terminaron su IO de la lista de bloqueados
        processes_blocked = [process for process in processes_blocked
                             if process.io_operation_duration >= 0]

        # Añadir los procesos a medida que pasa el tiempo.
        for process in processes:
            if process.arrival_time <= time:
                processes_ready.append(process)
        # Remueve los procesos que acaban de agregados
        processes = [process for process in processes
                     if process not in processes_ready]

        # Ordenar los procesos en la cola de listos por su tiempo restante de
        # ejecución (SJF), si hay un empate, desempatar con tiempo de llegada,
        # Si sigue habiendo empate, desempatar don el PID
        processes_ready.sort(key=lambda x: (x.remaining_time,
                                            x.arrival_time,
                                            x.pid),
                             reverse=True)

        # Cargar los primeros "N" elementos de la cola de listos,
        # donde "N" es la cantidad de CPU's disponibles,
        for cpu, slot in cpu_dict.items():
            if slot is None and len(processes_ready) > 0:
                cpu_dict[cpu] = processes_ready.pop()
                context_dict[cpu] = context_switch

        output_data = {}
        waiting_status_list = [proc.status() for proc in processes]
        output_data['waiting'] = [', '.join(waiting_status_list)]
        ready_status_list = [proc.status() for proc in processes_ready]
        output_data['ready'] = [', '.join(ready_status_list)]
        # Agrega los cpus al output
        for cpu, process in cpu_dict.items():
            if process is not None:
                output_data[cpu] = [process.status()]
            else:
                output_data[cpu] = ''
        blocked_status_list = [proc.status() for proc in processes_blocked]
        output_data['blocked'] = [', '.join(blocked_status_list)]
        output_table.update(output_data)

        time += 1
    # Imprime el resultado de la política de scheduling
    pd.set_option('display.max_colwidth', -1)
    pd.set_option('display.max_rows', -1)
    print(output_table)

    # Imprime los tiempos de retorno de los procesos y el tiempo de retorno
    # promedio.
    turnaround_time_total = 0
    print("\nTurnaround Times:")
    for process in processes_finished:
        turnaround_time_total += process.finish_time-process.arrival_time
        print("Process {}: {}".format(process.pid,
            process.finish_time-process.arrival_time))
    print("Average: {}".format(turnaround_time_total/len(processes_finished)))
    print("\n")

    # Imprime los tiempos de espera de los procesos y el tiempo de espera
    # promedio.
    wait_time_total = 0
    print("Waiting Times:")
    for process in processes_finished:
        wait_time = process.finish_time-process.arrival_time-process.cpu_time
        if process.io_operations is not None:
            wait_time -= sum(process.io_operations.values())
        wait_time_total += wait_time
        print("Process {}: {}".format(process.pid, wait_time))
    print("Average: {}".format(wait_time_total/len(processes_finished)))
    print("\n")

    return processes_finished
