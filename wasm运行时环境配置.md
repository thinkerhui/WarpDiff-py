# wasm运行时环境配置

如果是在中国大陆的网络环境中，**需要配置科学上网**才能确保正常通畅地安装。

下面的安装步骤在 Ubuntu 24.04.1 LTS 经过测试。

### WasmEdge

为所有用户安装

此前，需要你安装 curl

```TypeScript
sudo curl -sSf https://raw.githubusercontent.com/WasmEdge/WasmEdge/master/utils/install.sh | bash -s -- -p d
```

### Wasmtime

https://github.com/bytecodealliance/wasmtime

直接使用官方脚本：

```TypeScript
curl https://wasmtime.dev/install.sh -sSf | bash
```

### Wasmer

https://github.com/wasmerio/wasmer

```TypeScript
curl https://get.wasmer.io -sSfL | sh
```

### Wasm3

https://github.com/wasm3/wasm3/releases

把下载的elf文件存储并建立软链接：

```TypeScript
sudo ln -s /home/thinkerhui/wasm/wasm_runtime/wasm3-linux-x64.elf /usr/local/bin/wasm3
```

有可能需要添加执权限：

```TypeScript
chmod +x /usr/local/bin/wasm3
```

经过测试，发现wasm3跑各种程序都会core dump，所以重新构建试一下。

```Bash
sudo apt install ninja-build
```

官方用的是clang-12,clang-12已经是很老的版本。

使用clang-14构建（因为clang-14是我系统最近一个可以直接apt安装的最老版本）。

```Bash
# clone wasm3 source code
git clone https://github.com/wasm3/wasm3.git
cd wasm3
export CC=/usr/bin/clang-14
export CXX=/usr/bin/clang++-14
rm -rf build
mkdir build
cd build
cmake -GNinja .. 
ninja
```

终于可以跑了！！

删除原来的软链接（如果有），然后再重新建立软链接：

```Bash
sudo rm /usr/local/bin/wasm3
sudo ln -s /home/thinkerhui/wasm/wasm_runtime/wasm3/build/wasm3 /usr/local/bin/wasm3
```

`/home/thinkerhui/wasm/wasm_runtime/wasm3/build/wasm3` 替换为你构建出来的wasm3可执行文件的路径。

### Wamr

```Bash
# 克隆仓库/下载源代码
cd wasm_runtime
git clone https://github.com/bytecodealliance/wasm-micro-runtime.git
#安装依赖
sudo apt install build-essential cmake g++-multilib libgcc-11-dev lib32gcc-11-dev ccache
#构建
cd wasm-micro-runtime
cd product-mini/platforms/linux/
mkdir build && cd build
cmake ..
make
# iwasm is generated under current directory
```

加上软链接：

```Bash
sudo ln -s /home/thinkerhui/wasm/wasm_runtime/wasm-micro-runtime/product-mini/platforms/linux/build/iwasm /usr/local/bin/iwasm
```

`/home/thinkerhui/wasm/wasm_runtime/wasm-micro-runtime/product-mini/platforms/linux/build/iwasm` 替换为你构建出来的wamr（iwasm）可执行文件的路径。

