# WarpDiff-py: Differential Testing of Wasm Runtime Performance with py2wasm

this project is based on [WarpDiff](https://github.com/ShuyaoJiang/WarpDiff)

## Usage

### Step 0: Environment and Data Preparation
* **Runtime Installation:** Install Wasm runtimes on your local environment for testing, including [Wasmer](https://github.com/wasmerio/wasmer), [Wasmtime](https://github.com/bytecodealliance/wasmtime), [Wasm3](https://github.com/wasm3/wasm3), [WasmEdge](https://github.com/WasmEdge/WasmEdge), and [WAMR](https://github.com/bytecodealliance/wasm-micro-runtime).
* **Programming Language:** Python 3.11
* **Dataset**: pybenchmark




### Step 1: Test Case Compilation
```
python3 compile_to_target_pywasm.py
```

### Step 2: Runtime Performance Profiling
To obtain the total running time: 
```
python3 runtime_profiling_total_pywasm.py
```


### Step 3: Differential Testing on Runtime Performance Data
```
python3 analyze_performance_pywasm.py
```
