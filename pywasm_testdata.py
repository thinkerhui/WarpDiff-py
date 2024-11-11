data = {
    "binarytrees": 14,
    "chameneosredux": 6000000,
    "fannkuchredux": 10,
    "fasta": 1250000,
    "fastaredux": 2500000,
    "fibonacci": 1000000,
    "fib50": 500000,
    "iobench": 1,
    "jsonbench": 1,
    "knucleotide": 10000,
    "mandelbrot": 16000,
    "meteor": 2098,
    "nbody": 500000,
    "pidigits": 10000,
    "pystone": 100000,
    "regexdna": 10000,
    "revcomp": 1000,
    "richards": 10,
    "spectralnorm": 550,
    "templates": 1000,
    "threadring": 5000000,
    "testdata": {
        "knucleotide": "../pybenchmarks/bencher/data/knucleotide-input10000.txt",
        "regexdna": "../pybenchmarks/bencher/data/regexdna-input10000.txt",
        "revcomp": "../pybenchmarks/bencher/data/revcomp-input1000.txt",
    },
}
correct_case = [
    "../targets_pywasm/binarytrees/binarytrees.python3-7.python3.wasm",
    "../targets_pywasm/binarytrees/binarytrees.python3-6.python3.wasm",
    "../targets_pywasm/binarytrees/binarytrees.python3.wasm",
    "../targets_pywasm/fannkuchredux/fannkuchredux.python3-4.python3.wasm",
    "../targets_pywasm/fannkuchredux/fannkuchredux.python3-3.python3.wasm",
    "../targets_pywasm/fannkuchredux/fannkuchredux.python3-6.python3.wasm",
    "../targets_pywasm/fastaredux/fastaredux.python3-7.python3.wasm",
    "../targets_pywasm/fastaredux/fastaredux.python3.wasm",
    "../targets_pywasm/fastaredux/fastaredux.python3-6.python3.wasm",
    "../targets_pywasm/jsonbench/jsonbench.python3.wasm",
    "../targets_pywasm/nbody/nbody.python3.wasm",
    "../targets_pywasm/pystone/pystone.python3.wasm",
    "../targets_pywasm/revcomp/revcomp.python3-6.python3.wasm",
    "../targets_pywasm/revcomp/revcomp.python3-3.python3.wasm",
    "../targets_pywasm/revcomp/revcomp.python3-4.python3.wasm",
    "../targets_pywasm/revcomp/revcomp.python3-5.python3.wasm",
    "../targets_pywasm/spectralnorm/spectralnorm.python3-6.python3.wasm",
    "../targets_pywasm/spectralnorm/spectralnorm.python3-8.python3.wasm",
    "../targets_pywasm/threadring/threadring.python3.wasm",
    "../targets_pywasm/fasta/fasta.python3.wasm",
    "../targets_pywasm/fasta/fasta.python3-2.python3.wasm",
    "../targets_pywasm/fasta/fasta.python3-4.python3.wasm",
    "../targets_pywasm/fasta/fasta.python3-3.python3.wasm",
    "../targets_pywasm/fib50/fib50.python3.wasm",
    "../targets_pywasm/knucleotide/knucleotide.python3-3.python3.wasm",
    "../targets_pywasm/knucleotide/knucleotide.python3.wasm",
    "../targets_pywasm/meteor/meteor.python3.wasm",
    "../targets_pywasm/meteor/meteor.python3-3.python3.wasm",
    "../targets_pywasm/meteor/meteor.python3-2.python3.wasm",
    "../targets_pywasm/pidigits/pidigits.python3.wasm",
    "../targets_pywasm/regexdna/regexdna.python3-5.python3.wasm",
    "../targets_pywasm/richards/richards.python3.wasm",
]
error_case = [
    "../targets_pywasm/fannkuchredux/fannkuchredux.python3.wasm",
    "../targets_pywasm/fannkuchredux/fannkuchredux.python3-2.python3.wasm",
    "../targets_pywasm/fibonacci/fibonacci.python3-2.python3.wasm",
    "../targets_pywasm/fibonacci/fibonacci.python3.wasm",
    "../targets_pywasm/fibonacci/fibonacci.python3-3.python3.wasm",
    "../targets_pywasm/mandelbrot/mandelbrot.python3-6.python3.wasm",
    "../targets_pywasm/spectralnorm/spectralnorm.python3-5.python3.wasm",
    "../targets_pywasm/spectralnorm/spectralnorm.python3-2.python3.wasm",
    "../targets_pywasm/spectralnorm/spectralnorm.python3-3.python3.wasm",
    "../targets_pywasm/threadring/threadring.python3-2.python3.wasm",
    "../targets_pywasm/chameneosredux/chameneosredux.python3-2.python3.wasm",
    "../targets_pywasm/chameneosredux/chameneosredux.python3.wasm",
    "../targets_pywasm/fasta/fasta.python3-5.python3.wasm",
    "../targets_pywasm/iobench/iobench.python3.wasm",
    "../targets_pywasm/knucleotide/knucleotide.python3-2.python3.wasm",
    "../targets_pywasm/knucleotide/knucleotide.python3-8.python3.wasm",
    "../targets_pywasm/pidigits/pidigits.python3-2.python3.wasm",
    "../targets_pywasm/pidigits/pidigits.python3-5.python3.wasm",
    "../targets_pywasm/pidigits/pidigits.python3-4.python3.wasm",
    "../targets_pywasm/pidigits/pidigits.python3-3.python3.wasm",
    "../targets_pywasm/regexdna/regexdna.python3.wasm",
    "../targets_pywasm/templates/templates.python3.wasm",
]
