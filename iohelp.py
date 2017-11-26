import pandas as pd
pd.set_option('expand_frame_repr', False)
pd.set_option('colheader_justify', 'left')

class Process:
    ''' Estructura de datos que representa a un proceso '''
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
        if self.io_operations is None:
            return False
        # Tiempo de CPU total - Tiempo restante = Tiempo que ya lleva ejecutado
        return (self.cpu_time - self.remaining_time) in self.io_operations

    def perform_io(self):
        self.io_operation_duration = self.io_operations[self.cpu_time -
                                                        self.remaining_time]

    def status(self):
        return '{}({})'.format(self.pid, self.remaining_time)


class OutputTable:
    ''' Estructura de datos que almacena y muestra el scheduling.'''

    def __init__(self, num_cpus=1):
        self.columns = ['waiting', 'ready']
        self.columns.extend(['cpu_{}'.format(i)
                             for i in range(1, num_cpus + 1)])
        self.columns.append('blocked')
        self.df = pd.DataFrame(columns=self.columns)

    def update(self, data):
        new_row = pd.DataFrame(data, columns=self.columns)
        self.df = pd.concat([self.df, new_row], ignore_index=True)
        self.df.index.name = 't'

    def __str__(self):
        return str(self.df)

    def __repr__(self):
        return repr(self.df)


def read_input(filename):
    '''Lee el archivo de entrada y regresa una lista de procesos'''
    test_cases = []
    with open(filename) as input_file:
        while reading:
            processes = []
            setup = None
            policy = input_file.readline().strip()
            assert(policy in ['SJF', 'SRT'])
            quantum_line = input_file.readline().strip().split()
            assert(quantum_line[0] == 'QUANTUM')
            quantum_time = int(quantum_line[1])
            assert(quantum_time == 0)
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
                processes.append(
                    Process(pid, int(arrival), int(cpu_time), io_operations))
            setup = (policy, context_switch, num_cpus)
            test_cases.append((setup, processes))
    return test_cases
