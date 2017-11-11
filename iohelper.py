# Estructuras de datos auxiliares.
class Process:
    pid = 0
    arrival_time = 0
    cpu_time = 0
    priority = 0
    io_operation = False
    io_operation_start = {}
    io_operation_duration = 0

    def __init__(self, pid, arrival_time, cpu_time, io_operations):
        self.pid = pid
        self.arrival_time = arrival_time
        self.exit_time = None
        self.cpu_time = cpu_time
        self.remaining_time = cpu_time
        self.io_operations = io_operations
        self.io_operation_duration = 0

    def __str__(self):
        return ('Process {}: {}, {}, {}'.format(self.pid,
                                                self.arrival_time,
                                                self.cpu_time,
                                                self.io_operations,
                                                ))

    def __repr__(self):
        return ('Process(pid={}, arrival_time={}, cpu_time={}, io_operations={!r}'.format(
                self.pid,
                self.arrival_time,
                self.cpu_time,
                self.io_operations)
                )

    def has_io(self):
        '''Revisa si se requiere hacer una operación de I/O en este instante'''
        # Tiempo de CPU total - Tiempo restante = Tiempo que ya lleva ejecutado
        return (self.cpu_time - self.remaining_time) in self.io_operations

    def perform_io(self):
        io_operation_duration = io_operation_start[self.cpu_time -
                                                   self.remaining_time]


def read_input(filename):
    '''Lee el archivo de entrada y regresa una lista de procesos'''
    processes = []
    with open(filename) as input_file:
        policy = input_file.readline().strip()
        assert(policy in ['SJF', 'SRT'])
        quantum_line = input_file.readline().strip().split()
        assert(quantum_line[0] == 'QUANTUM')
        quantum_time = int(quantum_line[1])
        assert(quantum_time >= 0)
        context_line = input_file.readline().strip().rsplit(maxsplit=1)
        assert(context_line[0] == 'CONTEXT SWITCH')
        context_switch = int(context_line[1])
        assert(context_switch >= 0)
        cpu_line = input_file.readline().strip().split()
        assert(cpu_line[0] == 'CPUS')
        num_cpus = int(cpu_line[1])
        assert(num_cpus >= 1)
        for process_line in input_file.readlines():
            process_line = process_line.strip()
            if process_line == 'FIN':
                break
            pid, arrival, cpu_time, *io = process_line.strip().split()
            if io:
                io_operations = {}
                for i in range(1, len(io), 2):
                    io_operations[int(io[i])] = int(io[i + 1])
            else:
                io_operations = None
            # Agrega el proceso a la lista
            processes.append(Process(pid, arrival, cpu_time, io_operations))
    return processes
