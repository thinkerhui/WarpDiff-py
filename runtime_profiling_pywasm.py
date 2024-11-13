import os
import sys
from time import perf_counter, sleep
import func_timeout
from func_timeout import func_set_timeout
from numpy import mean
import csv
import traceback
import subprocess
from datetime import datetime
from common_utils import get_logger, write_csv
from pywasm_testdata import data, error_case
from compile_to_target_pywasm import BENCHMARKS, TARGET_DIR, TARGET_SUFFIX

logger = get_logger()
TEST_TIMES = 1
NATIVE = "x86native"
WASMER = "wasmer"
WASMTIME = "wasmtime"
WASM3 = "wasm3"
WASMEDGE = "wasmedge"
WASMEDGE_AOT = "wasmedge_aot"
WAMR = "wamr"
WAVM = "wavm"

# 路径变量
PROFILINGDATA_DIR = os.path.join("..", "profiling_data_perf_pywasm")
TARGET_DIR = os.path.join("..", "targets_pywasm")
PERF_LOG_DIR = os.path.join("..", "perf_log")

# RUNTIMES = [WASMTIME, WASMEDGE, WASMEDGE_AOT, WASM3, WAMR]
RUNTIMES = [WASM3]
EXECUTE_COMMAND_TEMPLATE = {
    NATIVE: "./%s",
    WASMER: "wasmer %s",
    WASMTIME: "wasmtime %s",
    WASM3: "wasm3 %s",
    WASMEDGE: "wasmedge %s",
    WASMEDGE_AOT: "wasmedge %s",
    # WASMEDGE_AOT: 'wasmedgec %s %s && wasmedge %s',
    WAMR: "iwasm %s",
    WAVM: "wavm run %s",
}
LONGINPUT_BENCHMARK = ["knucleotide", "regexdna", "revcomp"]
TIME_UNIT = 1000000
PROBE_NUM = 5
RUNTIMES_PROBES = {
    WASMER: [
        "sched:sched_process_exec",
        "probe_wasmer:abs_591f00",
        "probe_wasmer:abs_8d5ee0",
        "sched:sched_process_exit",
    ],
    WASMTIME: [
        "sched:sched_process_exec",
        "probe_wasmtime:abs_2e73c0",
        "probe_wasmtime:abs_398ce0",
        "sched:sched_process_exit",
    ],
    WASM3: [
        "sched:sched_process_exec",
        "probe_wasm3:main",
        "probe_wasm3:repl_call",
        "sched:sched_process_exit",
    ],
    WASMEDGE: [
        "sched:sched_process_exec",
        "probe_libwasmedge:abs_59710",
        "probe_libwasmedge:abs_d4de0",
        "sched:sched_process_exit",
    ],
    WASMEDGE_AOT: ["probe_libwasmedge:abs_15eda0", "probe_libwasmedge:abs_167e90"],
    WAMR: [
        "sched:sched_process_exec",
        "probe_iwasm:abs_8850",
        "probe_iwasm:abs_e2d0",
        "sched:sched_process_exit",
    ],
}
PERF_LOG_PROC_NAME_IDX = 0
PERF_LOG_TIMESTAMP_IDX = 3
PERF_LOG_PROBE_IDX = 4
RUNTIME_PATH = {
    WASMER: "wasmer",
    WASMTIME: "wasmtime",
    WASM3: "wasm3",
    WASMEDGE: "wasmedge",
    WASMEDGE_AOT: "wasmedgec",
    WAMR: "iwasm",
}
# RUNTIME_CMDS = {
#     WASMER: [
#         ["{runtime} {wasm}", f"make {WASMER}-perf-record", RUNTIMES_PROBES[WASMER], WASMER, WASMER],
#     ],
#     WASMTIME: [
#         ["{runtime} {wasm} --disable-cache", f"make {WASMTIME}-perf-record", RUNTIMES_PROBES[WASMTIME], WASMTIME, WASMTIME],
#     ],
#     WASM3: [
#         ["{runtime} {wasm}", f"make {WASM3}-perf-record", RUNTIMES_PROBES[WASM3], WASM3, WASM3],
#         ["{runtime} --compile {wasm}", f"make {WASM3}-perf-record", RUNTIMES_PROBES[WASM3], WASM3, f"{WASM3}--compile"],
#     ],
#     WASMEDGE_AOT: [
#         ["{runtime} {wasm} {wasm_aot}", f"make {WASMEDGE_AOT}-perf-record", RUNTIMES_PROBES[WASMEDGE_AOT], WASMEDGE_AOT, WASMEDGE_AOT],
#     ],
#     WASMEDGE: [
#         ["{runtime} {wasm_aot}", f"make {WASMEDGE}-perf-record", RUNTIMES_PROBES[WASMEDGE], WASMEDGE, f"{WASMEDGE}_aot"],
#     ],
#     WAMR: [
#         ["{runtime} {wasm}", f"make {WAMR}-perf-record", RUNTIMES_PROBES[WAMR], WAMR, WAMR],
#     ]
# }
RUNTIME_CMDS = {
    WASM3: [
        [
            "{runtime} {wasm}",
            f"make {WASM3}-perf-record",
            RUNTIMES_PROBES[WASM3],
            WASM3,
            WASM3,
        ],
        [
            "{runtime} --compile {wasm}",
            f"make {WASM3}-perf-record",
            RUNTIMES_PROBES[WASM3],
            WASM3,
            f"{WASM3}--compile",
        ],
    ],
}


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


def profile_time_in_one_case(
    runtime, execute_command_with_args, perf_record_cmd, probes, perf_log_path, input_data
):
    probes_num = len(probes)
    # start perf record cmd, different runtimes have different probe
    perf_record = subprocess.Popen(perf_record_cmd.split())
    sleep(2)

    def kill_perf():
        f = os.popen("ps aux | grep 'perf record' | awk '{print $2}'")
        res = f.read().split("\n")
        os.popen(f"sudo kill {' '.join(res)}")

    try:
        run(execute_command_with_args,input_data)
    except Exception as e:
        # stop perf record cmd
        kill_perf()
        logger.error("error occur!", e)
        return

    # stop perf record cmd
    sleep(1)
    kill_perf()
    sleep(1)

    # run perf script to get the perf log, and save in perf_log_path
    subprocess.run(f"sudo perf script --ns -f".split(), stdout=open(perf_log_path, "w"))
    sleep(1)

    # extract 5 timestamp from perf log, compute the above time range
    timestamps = []
    with open(perf_log_path, "r") as f:
        i = 0
        line = f.readline()
        exit_time = None
        while line is not None and line != "":
            line = line.strip()
            items = line.split()
            # 判断当前行是否是当前探针，如果不是，则读下一行
            if (
                items[PERF_LOG_PROC_NAME_IDX] != runtime
                or items[PERF_LOG_PROBE_IDX][:-1] != probes[i]
            ):
                line = f.readline()
                continue

            if i == probes_num - 1:
                exit_time = float(items[PERF_LOG_TIMESTAMP_IDX][:-1])
            else:
                timestamps.append(float(items[PERF_LOG_TIMESTAMP_IDX][:-1]))
                i += 1
            line = f.readline()

    if i < probes_num - 1 or exit_time is None:
        print("Something wrong....\n", i, " != ", probes_num)
        return

    timestamps.append(exit_time)
    print(timestamps)

    range_compute = lambda x, y: (x * TIME_UNIT - y * TIME_UNIT)
    time_range = [range_compute(timestamps[probes_num - 1], timestamps[0])]
    i = 0
    if probes_num > 2:
        while i < probes_num - 1:
            time_range.append(range_compute(timestamps[i + 1], timestamps[i]))
            i += 1
    print(time_range, "\n\n")
    return time_range


def profile_time_during_execution(
    wasm_target, out_dir, args, test_data_file, source_perf_log_dir
):
    for runtime in RUNTIMES:
        wasm_aot_target = os.path.join(
            os.path.dirname(wasm_target),
            os.path.splitext(os.path.basename(wasm_target))[0] + "_wasmedge_aot.wasm",
        )
        for runtime_cmd in RUNTIME_CMDS[runtime]:
            execute_command = runtime_cmd[0].format(
                runtime=RUNTIME_PATH[runtime],
                wasm=wasm_target,
                wasm_aot=wasm_aot_target,
            )
            execute_command_with_args = execute_command + ' ' + str(args)
            print(execute_command_with_args, runtime_cmd)
            
            # 读取test_data_file的输入数据(如果有的话)
            input_data = None
            if test_data_file is not None:
                with open(test_data_file, 'r') as f:
                    input_data = f.read()
            
            source_runtime_perf_log_dir = os.path.join(
                source_perf_log_dir, runtime_cmd[4]
            )
            os.makedirs(source_runtime_perf_log_dir, exist_ok=True)
            start_time = []
            code_loaded_time = []
            code_execution_time = []
            aot_compilation_time = []
            total_time = []
            for i in range(TEST_TIMES):
                if runtime == WASMER:
                    run(f"{RUNTIME_PATH[runtime]} cache clean")
                try:
                    tmp = profile_time_in_one_case(
                        runtime_cmd[3],
                        execute_command_with_args,
                        runtime_cmd[1],
                        runtime_cmd[2],
                        os.path.join(source_runtime_perf_log_dir, f"log_{i}.txt"),
                        input_data
                    )
                    if len(tmp) == 4:
                        total_time.append(tmp[0])
                        start_time.append(tmp[1])
                        code_loaded_time.append(tmp[2])
                        code_execution_time.append(tmp[3])
                    elif len(tmp) == 1:
                        aot_compilation_time.append(tmp[0])
                    else:
                        raise Exception("The length of the perf result is wrong")
                except func_timeout.exceptions.FunctionTimedOut as e:
                    print(e)
                    break
                sleep(2)

            target_name = os.path.basename(wasm_target)

            def write_res_to_csv(time_tag, arr):
                if len(arr) == 0:
                    return
                avg_time = mean(arr)
                data = [time_tag, runtime_cmd[4], target_name, avg_time]
                execution_time_out_dir = os.path.join(out_dir, time_tag)
                os.makedirs(execution_time_out_dir, exist_ok=True)
                out_file = os.path.join(
                    execution_time_out_dir, f"{time_tag}_" + runtime_cmd[4] + ".csv"
                )
                write_csv(data, out_file)

            write_res_to_csv("start_time", start_time)
            write_res_to_csv("code_loaded_time", code_loaded_time)
            write_res_to_csv("code_execution_time", code_execution_time)
            write_res_to_csv("aot_compilation_time", aot_compilation_time)
            write_res_to_csv("total_time", total_time)
            print("================\n\n")


def profile_by_benchmark(benchmark):
    logger.info("Profile " + benchmark + ":")
    benchmark_out_dir = os.path.join(PROFILINGDATA_DIR, benchmark)
    os.makedirs(benchmark_out_dir, exist_ok=True)

    now_perf_log_dir = os.path.join(
        PERF_LOG_DIR, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), benchmark
    )
    os.makedirs(now_perf_log_dir, exist_ok=True)

    # 如果原始代码有对应的WASM代码，则进行性能测试
    benchmark_dir = os.path.join(TARGET_DIR, benchmark)
    for file in os.listdir(benchmark_dir):
        if file.endswith(TARGET_SUFFIX) and "aot" not in file:
            wasm_target_path = os.path.join(benchmark_dir, file)
            # 检测target是否在不可运行列表
            if wasm_target_path in error_case:
                continue
            args = data[benchmark]
            test_data_file = None
            if benchmark in LONGINPUT_BENCHMARK:
                test_data_file = data["testdata"][benchmark]
                logger.info("testdata:" + test_data_file[:20])
            logger.info(wasm_target_path + " " + str(args))

            profile_by_source(
                wasm_target_path,
                benchmark_out_dir,
                args,
                test_data_file,
                now_perf_log_dir,
            )


def profile_all():
    for benchmark in BENCHMARKS:
        profile_by_benchmark(benchmark)


def profile_by_source(
    wasm_target, out_dir, args, test_data_file=None, now_perf_log_dir=None
):
    profile_time_during_execution(
        wasm_target, out_dir, args, test_data_file, now_perf_log_dir
    )


def main():
    # profile_all()
    profile_by_benchmark("binarytrees")


if __name__ == "__main__":
    main()
