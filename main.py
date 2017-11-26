import iohelp as io
import SJF as sjf
import SRT as srt

test_cases = io.read_input('input.txt')

# Itera por cada caso de pruba del input.
for test_case in test_cases:
    if test_case is not None:
        # Llama el shceduler adecuado del caso de prueba.
        if test_case[0][0] == 'SRT':
            print('SRT')
            process = srt.srt_scheduling(test_case[0], test_case[1])
        elif test_case[0][0] == 'SJF':
            print('SJF')
            process = sjf.sjf_scheduling(test_case[0], test_case[1])
