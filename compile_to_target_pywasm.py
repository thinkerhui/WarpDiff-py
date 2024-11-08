import os

BENCHMARK_DIR = os.path.join('..', 'pybenchmarks', 'bencher', 'programs')
TARGET_DIR = os.path.join('..', 'targets_pywasm')

# BENCHMARKS = [
#     "binarytrees", "fannkuchredux", "fastaredux", "fibonacci", "jsonbench",
#     "mandelbrot", "nbody", "pystone", "revcomp", "spectralnorm", "threadring",
#     "chameneosredux", "fasta", "fib50", "iobench", "knucleotide", "meteor",
#     "pidigits", "regexdna", "richards", "templates"
# ]
BENCHMARKS = ['binarytrees',"knucleotide"]
SOURCE_SUFFIX = '.python3'
TARGET_SUFFIX = '.wasm'
COMPILER = 'py2wasm'

def compile_all():
    """
    将所有Python基准程序编译成WASM格式。
    遍历BENCHMARKS列表中的每个基准程序，利用py2wasm将其源代码编译成WASM格式，并保存到目标目录中。
    """
    for benchmark in BENCHMARKS:
        print('Compile '+ benchmark + ' to wasm...')
        out_dir = os.path.join(TARGET_DIR,benchmark)
        os.makedirs(out_dir, exist_ok=True)
        # 找出后缀为.python3的文件(有些benchmark只有一个.python3，一般有多个)
        for file in os.listdir(os.path.join(BENCHMARK_DIR, benchmark)):
            if file.endswith(SOURCE_SUFFIX):
                command = '%s %s -o %s' % (COMPILER, os.path.join(BENCHMARK_DIR, benchmark, file), os.path.join(out_dir,file)+TARGET_SUFFIX)
                print(command)
                os.system(command)
        print()
def main():
    compile_all()
    
if __name__ == '__main__':
    main()