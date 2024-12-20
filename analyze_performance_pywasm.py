import os
import numpy as np
import pandas as pd
import math
import csv
import time
from sklearn import preprocessing as pp
from compile_to_target_pywasm import BENCHMARKS

PROFILINGDATA_DIR = os.path.join('..', 'profiling_data_pywasm')

WASMTIME = 'wasmtime'
WASM3 = 'wasm3'
WASMEDGE = 'wasmedge'
WASMEDGE_AOT = 'wasmedge_aot'
WAMR = 'wamr'
RUNTIME_LIST = [WASMTIME, WASM3, WASMEDGE_AOT, WAMR]

def get_case_vector(case, benchmark_dir):
    if case == 'recursive.wasm' or case == 'ackermann.wasm':
        return []
     
    case_vector = []
    for runtime in RUNTIME_LIST:
        time_file = os.path.join(benchmark_dir, 'execution_time_' + runtime + '.csv')
        if os.path.exists(time_file):
            target_case = case
            if runtime == 'wasmedge_aot':
                target_case = case[:-5]+'_wasmedge_aot.wasm'
            pd_reader = pd.read_csv(time_file, header=None, names=['data_type','runtime','target','execution_time'])
            case_time = pd_reader.loc[pd_reader['target'] == target_case, 'execution_time'].values[0]
            if math.isnan(case_time):
                return []
            else:
                case_vector.append(case_time)
    return case_vector


def get_case_vector_by_benchmark(benchmark):
    benchmark_execution_time_dir = os.path.join(PROFILINGDATA_DIR, benchmark, 'execution_time')
    wasmer_time_file = os.path.join(benchmark_execution_time_dir, 'execution_time_wasmtime.csv')
    if os.path.exists(wasmer_time_file):
        benchmark_case_vector_dic = {}
        pd_reader = pd.read_csv(wasmer_time_file, header=None)
        case_name_list = pd_reader.iloc[:,2]

        for case in case_name_list:
            case_vector = get_case_vector(case, benchmark_execution_time_dir)
            if case_vector:
                case_key = benchmark + '-' + os.path.splitext(case)[0]
                benchmark_case_vector_dic.update({case_key: case_vector})       
        # print(benchmark_case_vector_dic)

        case_vector_dict.update(benchmark_case_vector_dic)


def normalize_case_vectors():
    case_vector_array = np.array(list(case_vector_dict.values()))
    # print(case_vector_array)
    # 根据case_vector_array的列数初始化sum数组
    sum = np.zeros(case_vector_array.shape[1])
    for array in case_vector_array:
        #print(array)
        sum = sum + array
    print(sum)

    normalized_case_vector_array = pp.normalize(case_vector_array)
    # print(normalized_case_vector_array)
    
    global normalized_case_vector_dict
    normalized_case_vector_dict = {}
    case_name_list = list(case_vector_dict.keys())
    case_size = len(case_vector_dict)
    for i in range(case_size):
        normalized_case_vector = normalized_case_vector_array[i]
        normalized_case_vector_dict.update({case_name_list[i]: normalized_case_vector})
    # print(normalized_case_vector_dict)


def get_all_case_vectors():
    global case_vector_dict
    case_vector_dict = {}
    for benchmark in BENCHMARKS:
        get_case_vector_by_benchmark(benchmark)
    # print(case_vector_dict)
    normalize_case_vectors()
 

def rank_all_cases():
    global vector_center
    vector_center = np.mean(np.array(list(normalized_case_vector_dict.values())), axis=0)
    # print(vector_center)

    distance_dict = {}
    for case_name, normalized_case_vector in normalized_case_vector_dict.items():
        distance = math.dist(normalized_case_vector, vector_center)
        distance_dict.update({case_name: distance})
    # print(distance_dict)

    global sorted_distance_list
    sorted_distance_list = sorted(distance_dict.items(), key=lambda x: x[1], reverse=True)
    # print(sorted_distance_list)

    
def find_buggy_runtimes():
    sorted_distance_dict_by_runtime = {}
    for case in sorted_distance_list:
        case_name = case[0]
        normalized_case_vector = normalized_case_vector_dict[case_name]
        distance_to_center = normalized_case_vector - vector_center
        sorted_distance_dict_by_runtime.update({case_name: distance_to_center})
    # print(sorted_distance_dict_by_runtime)

    result_file = os.path.join('..', 'results2.csv')
    write_csv(sorted_distance_dict_by_runtime, result_file)


def write_csv(data, file):
    df = pd.DataFrame(data.values(), columns=RUNTIME_LIST)
    df.insert(0, 'case', data.keys())
    # print(df)
    print('Write to ' + file)
    df.to_csv(file, index=False)


def main():
    global error_case_dict
    error_case_dict = {}
    #start = time.time()
    get_all_case_vectors()
    rank_all_cases()
    find_buggy_runtimes()
    #end = time.time()
    #print('total time:', end - start)
    

if __name__=="__main__":
    main()