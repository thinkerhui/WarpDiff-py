import os
import sys
from time import perf_counter
import func_timeout
from func_timeout import func_set_timeout
from numpy import mean
import csv
import traceback
from compile_to_target_pywasm import BENCHMARKS, TARGET_DIR, TARGET_SUFFIX
from pywasm_testdata import data,error_case
from io import StringIO
import subprocess
from common_utils import get_logger,write_txt
# 获取logger
logger = get_logger('runtime_profiling_total_pywasm')

TEST_TIMES = 5

NATIVE = 'x86native'
WASMER = 'wasmer'
WASMTIME = 'wasmtime'
WASM3 = 'wasm3'
WASMEDGE = 'wasmedge'
WASMEDGE_AOT = 'wasmedge_aot'
WAMR = 'wamr'
WAVM = 'wavm'
# RUNTIMES = [NATIVE, WASMER, WASMTIME, WASM3, WAMR, WAVM]
RUNTIMES = [WASMTIME, WASMEDGE_AOT, WASM3, WAMR]
# RUNTIMES = [WASMTIME]
# RUNTIMES = [WASMTIME, WASMEDGE]
TARGET_DIR = os.path.join('..', 'targets_pywasm')
PROFILINGDATA_DIR = os.path.join('..', 'profiling_data_pywasm')

EXECUTE_COMMAND_TEMPLATE = {
    NATIVE: './%s',
    WASMER: 'wasmer %s',
    WASMTIME: 'wasmtime %s',
    WASM3: 'wasm3 %s',
    WASMEDGE: 'wasmedge %s',
    WASMEDGE_AOT: 'wasmedge %s',
    # WASMEDGE_AOT: 'wasmedgec %s %s && wasmedge %s',
    WAMR: 'iwasm %s',
    WAVM: 'wavm run %s'
}

LONGINPUT_BENCHMARK = ["knucleotide","regexdna","revcomp"]

def write_csv(data, file):
    logger.info('Write to ' + file)
    if not os.path.exists(file):
        with open(file, 'w') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(data)
    else:
        with open(file, 'a+') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(data)  
    

def profile_bin_size_by_target(target, out_dir):
    target_name = os.path.basename(target)
    target_size = os.path.getsize(target)
    data = ['bin_size', target_name, target_size]
    if target.endswith(TARGET_SUFFIX):
        out_file = os.path.join(out_dir, 'wasm_bin_size.csv')
    else:
        out_file = os.path.join(out_dir, 'native_bin_size.csv')
    write_csv(data, out_file)


def profile_bin_size(native_target, wasm_target, out_dir):
    target_size_out_dir = os.path.join(out_dir, 'bin_size')
    os.makedirs(target_size_out_dir, exist_ok=True)
    profile_bin_size_by_target(native_target, target_size_out_dir)
    profile_bin_size_by_target(wasm_target, target_size_out_dir)
    

def profile_execution_time(wasm_target, out_dir, args, test_data_file):
    # 遍历RUNTIMES列表中每个运行时环境
    for runtime in RUNTIMES:
        # 确定 target 的路径
        if runtime == WASMEDGE_AOT:
            # a.wasm -> a_aot.wasm
            wasm_aot_target = os.path.join(os.path.dirname(wasm_target), 
                os.path.splitext(os.path.basename(wasm_target))[0] + '_wasmedge_aot.wasm')
            aot_compile_command = 'wasmedgec %s %s' % (wasm_target, wasm_aot_target)
            logger.info(aot_compile_command)
            os.system(aot_compile_command)
            target = wasm_aot_target
        else: 
            target = wasm_target
        # 构建运行命令
        execute_command = EXECUTE_COMMAND_TEMPLATE[runtime] % target
        execute_command_with_args = execute_command + ' ' + str(args)
        logger.info(execute_command_with_args)
        # 读取test_data_file的输入数据(如果有的话)
        input_data = None
        if test_data_file is not None:
            with open(test_data_file, 'r') as f:
                input_data = f.read()
        # 执行命令并测试执行时间
        times = []
        for i in range(TEST_TIMES):
            try: 
                start = perf_counter()
                run(execute_command_with_args,input_data)
                end = perf_counter()
                execution_time = end - start
                times.append(execution_time)
                # global correct_case
                # correct_case.append(target)
            # except func_timeout.exceptions.FunctionTimedOut as e:
            #     logger.error(e)
            #     error_case.append(target)
            #     break
            except Exception as e:
                logger.error(e)
                # global error_case
                # error_case.append(target)
                break
        avg_time = mean(times)
        logger.info('Average time: '+str(avg_time))
        
        target_name = os.path.basename(target)
        data = ['execution_time', runtime, target_name, avg_time]
        execution_time_out_dir = os.path.join(out_dir, 'execution_time')
        os.makedirs(execution_time_out_dir, exist_ok=True)
        out_file = os.path.join(execution_time_out_dir, 'execution_time_' + runtime + '.csv')
        write_csv(data, out_file)


@func_set_timeout(300)
def run(command, input_str = None):
    process = subprocess.Popen(args=command,shell=True,stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    stdout, stderr = process.communicate(input=input_str)
    if process.returncode:
        logger.warning(process.returncode)
    if stderr:
        logger.info(stdout)
        # logger.error(stderr)
        raise Exception('Error in executing command: ' + command)
    # logger.info(stdout)


def profile_by_source(wasm_target, out_dir, args, test_data_file = None):
    # profile_bin_size(native_target, wasm_target, out_dir)
    profile_execution_time( wasm_target, out_dir, args, test_data_file)


def profile_by_benchmark(benchmark):
    logger.info('Profile ' + benchmark + ':')
    benchmark_out_dir = os.path.join(PROFILINGDATA_DIR, benchmark)
    os.makedirs(benchmark_out_dir, exist_ok=True)
    # 如果原始代码有对应的WASM代码，则进行性能测试
    benchmark_dir = os.path.join(TARGET_DIR, benchmark)
    for file in os.listdir(benchmark_dir):
        if file.endswith(TARGET_SUFFIX) and 'aot' not in file:
            wasm_target_path = os.path.join(benchmark_dir, file)
            # 检测target是否在不可运行列表
            if wasm_target_path in error_case:
                continue
            args = data[benchmark]
            test_data_file = None
            if benchmark in LONGINPUT_BENCHMARK:
                test_data_file = data['testdata'][benchmark]
                logger.info("testdata:"+test_data_file[:20])
            logger.info(wasm_target_path+" "+str(args))
            
            profile_by_source(wasm_target_path, benchmark_out_dir, args, test_data_file)


def profile_all():
    for benchmark in BENCHMARKS:
        profile_by_benchmark(benchmark)


def main():
        # record error/corrrect cases when running
        # global error_case
        # error_case = []
        # global correct_case
        # correct_case = []
        profile_all()
        # profile_by_benchmark('knucleotide')
        # logger.info('Error cases:'+str(error_case))
        # write_txt(str(error_case), 'error_case.txt')
        # logger.info('Correct cases:'+str(correct_case))
        # write_txt(str(correct_case), 'correct_case.txt')

if __name__=="__main__":
    main()
