import iohelp as io
import SJF as sjf
import SRT as srt

test_cases = io.read_input('input.txt')

sjf_results = []
srt_results = []

case_count_sjf = 1
case_count_srt = 1
# Itera por cada caso de pruba del input.
for test_case in test_cases:
    if test_case is not None:
        # Llama el shceduler adecuado del caso de prueba.
        if test_case[0][0] == 'SRT':
            print("Case #{}".format(case_count_srt))
            print('SRT')
            result = srt.srt_scheduling(test_case[0], test_case[1])
            srt_results.append(result)
            case_count_srt += 1
        elif test_case[0][0] == 'SJF':
            print("Case #{}".format(case_count_sjf))
            print('SJF')
            result = sjf.sjf_scheduling(test_case[0], test_case[1])
            sjf_results.append(result)
            case_count_sjf += 1

# Comparación de ambos protocolos
if len(sjf_results) is not len(srt_results):
    print("En la especificación del archivo de entrada debe de haber la misma\n" +
          "cantidad de casos de ambas políticas (SRT y SJF).")

case_count = 1
for sjf_result, srt_result in zip(sjf_results, srt_results):
    print("Caso #{}".format(case_count))
    print("Tiempo de retorno promedio SJF {} contra SRT {}".format(sjf_result[0],
          srt_result[0]))
    print("Tiempo de espera promedio SJF {} contra SRT {}".format(sjf_result[1],
          srt_result[1]))
    case_count += 1
