# WarpDiff-py: Differential Testing of Wasm Runtime Performance with py2wasm

this project is based on [WarpDiff](https://github.com/ShuyaoJiang/WarpDiff)

## Usage

### Step 0: Environment and Data Preparation
* **Runtime Installation:** Install Wasm runtimes on your local environment for testing, including [Wasmer](https://github.com/wasmerio/wasmer), [Wasmtime](https://github.com/bytecodealliance/wasmtime), [Wasm3](https://github.com/wasm3/wasm3), [WasmEdge](https://github.com/WasmEdge/WasmEdge), and [WAMR](https://github.com/bytecodealliance/wasm-micro-runtime).
* **Programming Language:** Python 3.11 **(must!)**
* **Dataset**: pybenchmarks



### Step 1: Test Case Compilation

```sh
# download pybenchmarks
git clone https://github.com/dundee/pybenchmarks
```

```Bash
# install py2wasm
pip install py2wasm
# pybenchmarks dependency
pip install jinja2 gmpy2 numpy
# if needed
sudo apt install patchelf
```

Adjust `BENCHMARK_DIR` of compile_to_target_pywasm.py based on your path of pybenchmarks.

You can also adjust `TARGET_DIR` to change the path you want to save the wasm target.

Then, run :

```
python3 compile_to_target_pywasm.py
```

### Step 2: Runtime Performance Profiling
```
pip install numpy func_timeout
```

To obtain the total running time: 

```
python3 runtime_profiling_total_pywasm.py
```

You may change `PROFILINGDATA_DIR`

### Step 3: Differential Testing on Runtime Performance Data

```
pip install scikit-learn pandas
```

```
python3 analyze_performance_pywasm.py
```

You may change `PROFILINGDATA_DIR`
