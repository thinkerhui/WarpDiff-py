## 网络问题

由于各种环境的配置都需要连接github或者其他在国外源，所以最好配置科学上网环境。

尝试在ubuntu22.04.05使用clash-verge，出现各种依赖问题（WebView2相关）。最后的解决办法是采用命令行clash加上网页UI。

### clash-verge的坑

```Plain
dpkg: 依赖关系问题使得 clash-verge 的配置工作不能继续：
 clash-verge 依赖于 libwebkit2gtk-4.0-37；然而：
  未安装软件包 libwebkit2gtk-4.0-37。
```

上面是**deb**版本clash-verge的报错，现在换为**AppImage**版本的。

```TypeScript
thinkerhui@thinkerhui-Redmi-Book-Pro-15-2022:~/下载$ ./clashcn.com_clash-verge_1.5.11_amd64.AppImage 
dlopen(): error loading libfuse.so.2

AppImages require FUSE to run. 
You might still be able to extract the contents of this AppImage 
if you run it with the --appimage-extract option. 
See https://github.com/AppImage/AppImageKit/wiki/FUSE 
for more information
```

于是加上 --appimage-extract 来运行

```TypeScript
./clashcn.com_clash-verge_1.5.11_amd64.AppImage --appimage-extract
thinkerhui@thinkerhui-Redmi-Book-Pro-15-2022:~$ clash-verge
clash-verge: error while loading shared libraries: libwebkit2gtk-4.0.so.37: cannot open shared object file: No such file or directory
```

尝试安装libwebkit2gtk发现有更多报错：

```TypeScript
dpkg: 依赖关系问题使得 libwebkit2gtk-4.0-37:amd64 的配置工作不能继续：
 libwebkit2gtk-4.0-37:amd64 依赖于 libjavascriptcoregtk-4.0-18 (= 2.44.2-1~deb12u1)；然而：
  未安装软件包 libjavascriptcoregtk-4.0-18。
 libwebkit2gtk-4.0-37:amd64 依赖于 libavif15 (>= 0.11.1)；然而：
  未安装软件包 libavif15。
 libwebkit2gtk-4.0-37:amd64 依赖于 libgstreamer-plugins-bad1.0-0 (>= 1.22.0)；然而：
  未安装软件包 libgstreamer-plugins-bad1.0-0。
 libwebkit2gtk-4.0-37:amd64 依赖于 libicu72 (>= 72.1~rc-1~)；然而：
  未安装软件包 libicu72。
 libwebkit2gtk-4.0-37:amd64 依赖于 libjpeg62-turbo (>= 1.3.1)；然而：
  未安装软件包 libjpeg62-turbo。

dpkg: 处理软件包 libwebkit2gtk-4.0-37:amd64 (--install)时出错：
 依赖关系问题 - 仍未被配置
正在处理用于 libc-bin (2.39-0ubuntu8.3) 的触发器 ...
在处理时有错误发生：
 libwebkit2gtk-4.0-37:amd64
```

还是老实用AppRun好了,AppRun似乎也不好用......

在吃饭路上想了一下，

```TypeScript
dpkg: 依赖关系问题使得 libwebkit2gtk-4.0-37:amd64 的配置工作不能继续：
 libwebkit2gtk-4.0-37:amd64 依赖于 libjavascriptcoregtk-4.0-18 (= 2.44.2-1~deb12u1)；然而：
  系统中 libjavascriptcoregtk-4.0-18:amd64 的版本为 2.43.3-1。
 libwebkit2gtk-4.0-37:amd64 依赖于 libavif15 (>= 0.11.1)；然而：
  未安装软件包 libavif15。
 libwebkit2gtk-4.0-37:amd64 依赖于 libgstreamer-plugins-bad1.0-0 (>= 1.22.0)；然而：
  未安装软件包 libgstreamer-plugins-bad1.0-0。
 libwebkit2gtk-4.0-37:amd64 依赖于 libicu72 (>= 72.1~rc-1~)；然而：
  未安装软件包 libicu72。
 libwebkit2gtk-4.0-37:amd64 依赖于 libjpeg62-turbo (>= 1.3.1)；然而：
  未安装软件包 libjpeg62-turbo。
W: GPG 错误：http://security.debian.org/debian-security bullseye-security InRelease: 由于没有公钥，无法验证下列签名： NO_PUBKEY 112695A0E562B32A NO_PUBKEY 54404762BBB6E853
E: 仓库 “http://security.debian.org/debian-security bullseye-security InRelease” 没有数字签名。
N: 无法安全地用该源进行更新，所以默认禁用该源。
N: 参见 apt-secure(8) 手册以了解仓库创建和用户配置方面的细节。
E: 仓库 “https://ppa.launchpadcontent.net/linuxuprising/libpng12/ubuntu noble Release” 没有 Release 文件。
N: 无法安全地用该源进行更新，所以默认禁用该源。
N: 参见 apt-secure(8) 手册以了解仓库创建和用户配置方面的细节。
```

左右折腾了一下，**安装了fuse**，好像当时提示要删掉一大堆库，我直接yes了。下午ubuntu已经坏掉了......

![img](https://oiv4vv80gv6.feishu.cn/space/api/box/stream/download/asynccode/?code=MWQwMDVhODc3ZjgzMTQ1NzUxZGMyMDJmYTBlMzBmZjRfc1FZRVdsYXppdFVRdWNkRHBzRUFDYlE5RzJrYWliS3NfVG9rZW46SWZETmI4MDZ6b2daRUR4WUN4SmNtWUgzblJlXzE3MzIzNzU5OTU6MTczMjM3OTU5NV9WNA)

难绷，看来ubuntu当主力真不行...或者是我太菜了。

原本准备放弃，但是google搜索了一下发现还是有人和我出现了同样的问题。

https://www.reddit.com/r/Ubuntu/comments/15adjzp/ubuntu_2304_does_not_boot_after_installing_fuse/

https://github.com/AppImage/AppImageKit/wiki/FUSE

我发现官方也有这个说明，确实直接安装会导致系统损坏。

**重新安装ubuntu-desktop**可以解决问题：

```Nginx
sudo apt install ubuntu-desktop
```

后面搞了个命令行的clash（在之前rust-chore的文件夹找到到了），就一个二进制文件，反而十分好用......

Ok，经过两天的生不如死，现在可以开始跑实验了。

**搞好了网络环境，后面配置环境就比较通畅了。**

## 配置Webassembly运行时环境

### WasmEdge

为所有用户安装

此前，需要你安装 curl

```TypeScript
sudo curl -sSf https://raw.githubusercontent.com/WasmEdge/WasmEdge/master/utils/install.sh | bash -s -- -p d
```

额，遇到了报错，感觉是**网络问题**

```TypeScript
busercontent.com/WasmEdge/WasmEdge/master/utils/install.sh | bash -s -- -p /usr/local
Using Python: /usr/bin/python3 
<stdin>:250: SyntaxWarning: invalid escape sequence '\d'
<stdin>:1129: SyntaxWarning: invalid escape sequence '\+'
INFO    - Cannot find libcudart.so
INFO    - Compatible with current configuration
Traceback (most recent call last):
  File "/usr/lib/python3.12/urllib/request.py", line 1344, in do_open
    h.request(req.get_method(), req.selector, req.data, headers,
  File "/usr/lib/python3.12/http/client.py", line 1336, in request
    self._send_request(method, url, body, headers, encode_chunked)
  File "/usr/lib/python3.12/http/client.py", line 1382, in _send_request
    self.endheaders(body, encode_chunked=encode_chunked)
  File "/usr/lib/python3.12/http/client.py", line 1331, in endheaders
    self._send_output(message_body, encode_chunked=encode_chunked)
  File "/usr/lib/python3.12/http/client.py", line 1091, in _send_output
    self.send(msg)
  File "/usr/lib/python3.12/http/client.py", line 1035, in send
    self.connect()
  File "/usr/lib/python3.12/http/client.py", line 1470, in connect
    super().connect()
  File "/usr/lib/python3.12/http/client.py", line 1001, in connect
    self.sock = self._create_connection(
                ^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/lib/python3.12/socket.py", line 852, in create_connection
    raise exceptions[0]
  File "/usr/lib/python3.12/socket.py", line 837, in create_connection
    sock.connect(sa)
ConnectionRefusedError: [Errno 111] Connection refused

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "<stdin>", line 1562, in <module>
  File "<stdin>", line 1336, in main
  File "<stdin>", line 44, in wrap_download_url
  File "/usr/lib/python3.12/urllib/request.py", line 240, in urlretrieve
    with contextlib.closing(urlopen(url, data)) as fp:
                            ^^^^^^^^^^^^^^^^^^
  File "/usr/lib/python3.12/urllib/request.py", line 215, in urlopen
    return opener.open(url, data, timeout)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/lib/python3.12/urllib/request.py", line 515, in open
    response = self._open(req, data)
               ^^^^^^^^^^^^^^^^^^^^^
  File "/usr/lib/python3.12/urllib/request.py", line 532, in _open
    result = self._call_chain(self.handle_open, protocol, protocol +
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/lib/python3.12/urllib/request.py", line 492, in _call_chain
    result = func(*args)
             ^^^^^^^^^^^
  File "/usr/lib/python3.12/urllib/request.py", line 1392, in https_open
    return self.do_open(http.client.HTTPSConnection, req,
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/lib/python3.12/urllib/request.py", line 1347, in do_open
    raise URLError(err)
urllib.error.URLError: <urlopen error [Errno 111] Connection refused>
```

直接浏览器打开url把脚本复制到本地，保存在wasm-edge-install.sh , 加执行权限

```TypeScript
chmod +x wasm-edge-install.sh
./wasm-edge-install.sh -p /usr/local
```

发现还有一个python的install脚本

然后上面的执行错误可能还和python版本有关。使用pyenv管理多版本python

https://github.com/pyenv/pyenv

```TypeScript
curl https://pyenv.run | bash
```

然后把pyenv加到命令行环境中：

![img](https://oiv4vv80gv6.feishu.cn/space/api/box/stream/download/asynccode/?code=MTM5YjkxMjFiOGM0NjMyNDk0MDliMTkzMmI3MGUyMjVfVjFqMFRzQm5zaUkxNkFsTnd5V1NESU01bGhMVWZEOWpfVG9rZW46UHhDUWJjU1Qwb0JnYUh4UnlJZWNyRTJyblJnXzE3MzIzNzU5OTU6MTczMjM3OTU5NV9WNA)

配置好pyenv后就可以直接愉快使用了

```TypeScript
pyenv install 3.10
```

但是发现缺少了一大堆依赖。。。。。

摆烂，直接装：

```TypeScript
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt-get update
sudo apt-get install python3.10
curl -sSf https://raw.githubusercontent.com/WasmEdge/WasmEdge/master/utils/install.sh | bash
Using Python: /home/thinkerhui/micromamba/bin/python3 
INFO    - Cannot find libcudart.so
INFO    - Compatible with current configuration
INFO    - Running Uninstaller
WARNING - Uninstaller did not find previous installation
WARNING - SHELL variable not found. Using bash as SHELL
INFO    - shell configuration updated
INFO    - Downloading WasmEdge
|============================================================|100.00 %INFO    - Downloaded
INFO    - Installing WasmEdge
INFO    - WasmEdge Successfully installed
INFO    - Run:
source /home/thinkerhui/.bashrc
```

好吧，直接就成功了

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

有可能需要添加执行权限：

```TypeScript
chmod +x /usr/local/bin/wasm3
```

经过测试，发现wasm3跑各种程序都会core dump，所以重新构建试一下。

```Bash
sudo apt install ninja-build
```

官方用的是clang-12,似乎clang-12已经是很老的版本,尝试直接用安装好的clang18来构建，出错了：

```Bash
CMake Error at CMakeLists.txt:102 (add_executable):
  The install of the wasm3 target requires changing an RPATH from the build
  tree, but this is not supported with the Ninja generator unless on an
  ELF-based or XCOFF-based platform.  The CMAKE_BUILD_WITH_INSTALL_RPATH
  variable may be set to avoid this relinking step.


CMake Error at build/_deps/libuv-src/CMakeLists.txt:391 (add_library):
  The install of the uv target requires changing an RPATH from the build
  tree, but this is not supported with the Ninja generator unless on an
  ELF-based or XCOFF-based platform.  The CMAKE_BUILD_WITH_INSTALL_RPATH
  variable may be set to avoid this relinking step.


CMake Error at build/_deps/libuv-src/CMakeLists.txt:391 (add_library):
  The install of the uv target requires changing an RPATH from the build
  tree, but this is not supported with the Ninja generator unless on an
  ELF-based or XCOFF-based platform.  The CMAKE_BUILD_WITH_INSTALL_RPATH
  variable may be set to avoid this relinking step.


-- Generating done (0.0s)
CMake Generate step failed.  Build files cannot be regenerated correctly.
```

使用zig构建

```Bash
zig build
```

发现还是core dump了

使用clang-14构建（因为clang-14是我系统最近一个可以直接apt安装的版本）

```Bash
export CC=/usr/bin/clang-14
export CXX=/usr/bin/clang++-14
rm -rf build
mkdir build
cd build
cmake -GNinja .. 
ninja
```

终于可以跑了！！

删除原来的软链接，然后再重新建立软链接：

```Bash
sudo rm /usr/local/bin/wasm3
sudo ln -s /home/thinkerhui/wasm/wasm_runtime/wasm3/build/wasm3 /usr/local/bin/wasm3
```

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

## 测试集编译

### Llvm-test-suite

首先，编译Warpdiff原本的数据集试一下。

下载并数据集并放到和Warpdiff同一级的位置。

![img](https://oiv4vv80gv6.feishu.cn/space/api/box/stream/download/asynccode/?code=ZTA1ZTY5MWRkOGU4Y2IyYjI0MTA1ODA3MDIwZjIyZTVfNU4wVXhkajJGalVhTlRxQzUxMEJ3a2p0azVlQ2hwcXNfVG9rZW46WTBEZWJTcE9ybzBEYVd4WmNnemNjeWk1blRlXzE3MzIzNzU5OTU6MTczMjM3OTU5NV9WNA)

要先安装enscripten和clang两个编译器：

```Bash
sudo apt install emscripten clang
```

然后执行编译脚本：

```Bash
python compile_to_target.py O2
```

### Pybenchmark

安装Python3.11,因为目前py2wasm只支持python3.11

```Bash
sudo apt install python3.11
```

安装py2wasm，换了清华源会更快一点（我用默认源下载巨慢，连外网代理也没用）：

![img](https://sse-market-source-1320172928.cos.ap-guangzhou.myqcloud.com/blog/asynccode)

```Bash
python -m pip install --upgrade pip
pip config set global.index-url https://mirrors.tuna.tsinghua.edu.cn/pypi/web/simple
# 安装py2wasm构建程序
pip install py2wasm
# pybenchmarks测试程序本身依赖的库
pip install jinja2 gmpy2 numpy
```

安装patchelf：

```Bash
sudo apt install patchelf
```

运行构建程序：

```Bash
python compile_to_target_pywasm.py 
```

一开始会自动下载安装wasi-sdk：

```Bash
py2wasm ../pybenchmarks/bencher/programs/binarytrees/binarytrees.python3 -o ../targets_pywasm/binarytrees/binarytrees.python3.wasm
py2wasm: wasi-sdk not found in /home/thinkerhui/wasm/.venv/lib/python3.11/site-packages/nuitka/wasi-sdk/21/sdk-Linux, downloading the SDK
py2wasm: Downloading wasi-sdk-21.0-linux.tar.gz
wasi-sdk-21.0-linux.tar.gz: 100%|███████████████| 74.9M/74.9M [00:32<00:00, 2.40MMiB/s]
py2wasm: Extracting wasi-sdk-21.0-linux.tar.gz
py2wasm: wasi-sdk installed at: /home/thinkerhui/wasm/.venv/lib/python3.11/site-packages/nuitka/wasi-sdk/21/sdk
```

![img](https://oiv4vv80gv6.feishu.cn/space/api/box/stream/download/asynccode/?code=MWMzNzhmZTgxNGEwYjI2NTc0ZTY5OTgyMjU2OWE4MWZfcDZZdHNtUkRxZzdabmZJWms3T3ZqdVNPV1VXZ0JrQUhfVG9rZW46Wmp2MmJYbEVZb1QxemJ4bTZLS2NZeHdLbjhkXzE3MzIzNzU5OTU6MTczMjM3OTU5NV9WNA)

## 总时间测试

不知道为啥wasmer没办法在有限时间内跑出python编译来的wasm文件，一时debug不出来，先放一放这个。

"fastaredux": 2500000  在20：06：01的时候不知道为啥卡住了，实际应该是几秒钟就可以跑完的。难道是因为日志太长了？

好吧，应该要先确认一下哪些程序可以跑，然后再开始正常跑。似乎一个wasmruntime可以跑的，其他的一般也可以跑，所以不妨先用wasmtime所有跑一次，然后计算量也可以根据wasmtime的结果来进行调整。

fannkuchredux 可以跑的：

fannkuchredux.python3-3.python3

fannkuchredux.python3-4.python3

fannkuchredux.python3-6.python3

fasta 可以跑的：

...

感觉靠人肉看日志来确定哪些可以跑非常低效，所以直接在程序里记录了。

记录了用例之后，再看看计算量，慢的wasm3等慢的运行时在跑相同用例大概是wasmtime的10倍。

| prgram        | 输入1   | time1(秒) |
| ------------- | ------- | --------- |
| binarytrees   | 14      | 1.5       |
| fannkuchredux | 10      | 5         |
| fasta         | 2500000 | 6         |
| fastaredux    | 2500000 | 2.5       |
| fib50         | 1000000 | 6.5       |
| jsonbench     | 1       | 3.5       |
| meteor        | 2098    | 4         |
| nbody         | 5000000 | 47        |
| pidigits      | 50000   | 2.5       |
| pystone       | 50000   | 0.4       |
| regexdna      | 10000   | 0.3       |
| revcomp       | 1000    | 0.8       |
| richards      | 10      | 1.2       |
| spectralnorm  | 550     | 3.7       |
| threadring    | 5000000 | 0.7       |
| knucleotide   | 10000   | 0.2       |

## perf性能测试

### 三阶段性能测试

安装python依赖

```Bash
pip install numpy func_timeout
```

#### 错误

似乎报了和WSL同样的错误...... 这让我很不安

```Bash
(.venv) (.venv) (base) thinkerhui@thinkerhui-Redmi-Book-Pro-15-2022:~/wasm/WarpDiff-py$ python runtime_profiling.py O2
Profile Polybench:
wasmer ../targets/O2/Polybench/wasm/mvt.wasm ['{runtime} {wasm}', 'make wasmer-perf-record', ['sched:sched_process_exec', 'probe_wasmer:abs_591f00', 'probe_wasmer:abs_8d5ee0', 'sched:sched_process_exit'], 'wasmer', 'wasmer']
Wasmer cache cleaned successfully.
sudo perf record -e probe_wasmer:abs_591f00 -e probe_wasmer:abs_8d5ee0 -e probe_wasmer:abs_6d5cb0 -e sched:sched_process_exec -e sched:sched_process_exit -a -T
event syntax error: 'probe_wasmer:abs_591f00'
                     \___ unknown tracepoint

Error:  File /sys/kernel/tracing//events/probe_wasmer/abs_591f00 not found.
Hint:   Perhaps this kernel misses some CONFIG_ setting to enable this feature?.

Run 'perf list' for a list of valid events

 Usage: perf record [<options>] [<command>]
    or: perf record [<options>] -- <command> [<options>]

    -e, --event <event>   event selector. use 'perf list' to list available events
make: *** [makefile:2：wasmer-perf-record] 错误 129
0.011827
kill: (47839): 没有那个进程
kill: (47841): 没有那个进程
failed to open perf.data: No such file or directory  (try 'perf record' first)
Something wrong....
 0  !=  4
Traceback (most recent call last):
  File "/home/thinkerhui/wasm/WarpDiff-py/runtime_profiling.py", line 385, in <module>
    main()
  File "/home/thinkerhui/wasm/WarpDiff-py/runtime_profiling.py", line 373, in main
    profile_by_benchmark(POLYBENCH)
  File "/home/thinkerhui/wasm/WarpDiff-py/runtime_profiling.py", line 341, in profile_by_benchmark
    profile_by_source(native_target_path, wasm_target_path, benchmark_out_dir, now_perf_log_for_target_dir)
  File "/home/thinkerhui/wasm/WarpDiff-py/runtime_profiling.py", line 318, in profile_by_source
    profile_time_during_execution(wasm_target, out_dir, source_perf_log_dir)
  File "/home/thinkerhui/wasm/WarpDiff-py/runtime_profiling.py", line 282, in profile_time_during_execution
    if len(tmp) == 4:
       ^^^^^^^^
TypeError: object of type 'NoneType' has no len()
```

不过我想起来这个三阶段性能测试是为了更具体定位性能问题，或者我可以用更好的方式来实现这个？

后面经过仔细分析，是因为perf命令中有一些probe，比如probe_wasmer没有定义。

下面分析wamer的perf命令：

```Bash
sudo perf record -e probe_wasmer:abs_591f00 -e probe_wasmer:abs_8d5ee0 -e probe_wasmer:abs_6d5cb0 -e sched:sched_process_exec -e sched:sched_process_exit -a -T
```

perf record 用于记录性能事件

`-e`: 指定性能事件。

首先指定了三个**自定义**的 `probe_wasmer` 事件（`probe_wasmer:abs_591f00`, `probe_wasmer:abs_8d5ee0`, `probe_wasmer:abs_6d5cb0`）

`probe_wasmer`: 这看起来是与 Wasmer相关的事件。具体这些事件代表什么取决于系统中的事件定义。也就是说这部分应该是需要自己去定义的，这应该也是报错的来源（因为我们并没有事先去定义）。

`abs_591f00`, `abs_8d5ee0`, `abs_6d5cb0`: 这些通常是特定内存地址的探针事件，意味着在这几个地址处发生的事件将会被记录。具体这些事件是做什么的，需要通过 Wasmer 或系统中定义的探针来理解。

```
-e sched:sched_process_exec -e sched:sched_process_exit
```

- 这些是标准的调度器事件，用来监控进程的执行情况。
  - `sched:sched_process_exec`: 记录每当进程开始执行时的事件。
  - `sched:sched_process_exit`: 记录每当进程退出时的事件。

#### 尝试定义probe

下面尝试给wasmtime来创建探针。

probe_wasmtime:abs_2e73c0

probe_wasmtime:abs_398ce0

查找wasmtime的路径

```Bash
# 方法一
which wasmtime
# 方法二
whereis wasmtime
# 方法三
sudo find / -name wasmtime
# 方法四 列出wasmtime依赖的共享库
ldd $(which wasmtime)
```

如果不出意外的话论文代码的探针对应的是wasmtime的可执行文件，确定执行文件路径如下：

```Bash
/home/thinkerhui/.wasmtime/bin/wasmtime
```

检查wasmtime符号表

`nm` 命令可以用于查看可执行文件、目标文件（object file）和共享库（shared library）的符号表。符号表包含了该文件中的函数、变量等符号信息，并可以帮助了解程序的内部结构。

```Bash
nm /home/thinkerhui/.wasmtime/bin/wasmtime
```

不过符号表有点多，我们重点看一下我们的两个地址对应的：

```Bash
nm /home/thinkerhui/.wasmtime/bin/wasmtime | grep -e 2e73c0 -e 398ce0
```

令人沮丧的是并没有输出任何东西.....有可能是**版本变更引起的（我并没有安装论文实验的版本）**。

试了一下检查wasmedge的符号表，发现它的可执行文件和三个依赖的libwasmedge都没办法用nm来检查符号表......

唯一**有希望直接复现的是wasm3**，因为它似乎没有更新过，而且论文代码相应探针是用的函数名表示而不是绝对地址。

```Bash
# 找出wasm3路径
which wasm3
# 检查符号
nm /usr/local/bin/wasm3 | grep -e main -e repl_call
# 添加探针
sudo perf probe -x /usr/local/bin/wasm3 main
sudo perf probe -x /usr/local/bin/wasm3 repl_call
```

一开始gpt4o给我的添加探针的命令如下，但是始终报错，后面查阅文档发现**并不是这么写**：

```Bash
sudo perf probe -x /usr/local/bin/wasm3 --add 'probe_wasm3:main'
sudo perf probe -x /usr/local/bin/wasm3 --add 'probe_wasm3:repl_call'
```

还有一个需要注意的是这个添加的是动态指针，所以系统重启后会消失（需要重新添加）

定义好之后，就可以跑三阶段perf性能测试了：

```Bash
python python runtime_profiling_pywasm.py 
```

在跑的过程中kill掉perf record总是失败，不过似乎跑的结果是没问题的。

其实三阶段性能测试是为了给更精确定位问题服务的，所以这步可以归为更准确定位用例的性能问题的一个步骤之一。目前的想法是给有问题的用例创建火焰图。

### 火焰图

在差分分析中，定位出来

下载使用FlameGraph来生成火焰图

```Bash
# 克隆FlameGraph仓库
git clone https://github.com/brendangregg/FlameGraph.git
cd FlameGraph
# 使用stackcollapse-perf.pl和flamegraph.pl来生成火焰图，下面命令采用管道写法
perf script | ./stackcollapse-perf.pl | ./flamegraph.pl > flamegraph.svg
```

## 差分分析

差分分析的程序要安装以下依赖：

```Bash
pip install scikit-learn pandas
```

对原本的差分分析程序进行修改，根据实际情况，主要改三处地方：

1. 将total_time 改为 execution_time
2. 要分析的运行时列表改为5个：wasmtime,wasmedge,wasmedge_aot,wasm3,wamr 其中，wasmedge的性能确实太差，后面应该要去掉。wasmer由于无法正常跑，所以也去掉。
3. normalize_case_vectors()的sum初始化原本是固定7个0,改为根据case_vector_array的列数（每行的长度）来进行初始化。

运行差分测试

```Bash
python analyze_performance_pywasm.py 
```

第一轮（每个用例只运行测试一次，花了1个小时）的分析结果（前10）：

| case                                          | wasmtime     | wasm3        | wasmedge_aot | wamr         |
| --------------------------------------------- | ------------ | ------------ | ------------ | ------------ |
| revcomp-revcomp.python3-6.python3             | 0.155730746  | -0.08739965  | 0.078480278  | 0.026816293  |
| revcomp-revcomp.python3-4.python3             | 0.146575341  | -0.094282827 | 0.078094194  | 0.034890671  |
| revcomp-revcomp.python3-5.python3             | 0.145847764  | -0.089254376 | 0.07365105   | 0.032552635  |
| revcomp-revcomp.python3-3.python3             | 0.13998953   | -0.079437779 | 0.091317335  | 0.02193178   |
| fasta-fasta.python3-4.python3                 | -0.038264563 | 0.084500081  | -0.01341118  | -0.073591829 |
| regexdna-regexdna.python3-5.python3           | 0.097605184  | -0.032066045 | 0.034242721  | 0.009613805  |
| jsonbench-jsonbench.python3                   | -0.048669494 | 0.024762807  | -0.081128269 | -0.003363684 |
| fannkuchredux-fannkuchredux.python3-6.python3 | -0.049441251 | 0.036652037  | -0.071850425 | -0.015385131 |
| pidigits-pidigits.python3                     | -0.023682578 | 0.031376305  | -0.071605108 | -0.01196861  |

其实初步来看，**大概只有revcomp这个用例在wasmtime上有问题**（相比较于论文的偏离度其实比较小）

后面就进一步在该用例上进行分析。

## 问题定位

最后一步就是通过人工分析出性能问题

由于我比较菜，对wasmtime的具体运行机制并没有深入了解。

之前在学习node的时候，知道了确实可以用perf这样的工具来具体分析一个程序在各个部分所花的时间。

[Nodejs学习笔记](https://oiv4vv80gv6.feishu.cn/docx/LjNFdh0VVorb9txclyscbF8onxd)

https://nodejs.cn/en/learn/getting-started/profiling

于是，决定采用没有任何probe的perf record来生成火焰图分析。

```Bash
# 为了方便生成火焰图，直接进入FlameGraph
cd FlameGraph
# wasmtime
# perf record
sudo perf record -g wasmtime ../targets_pywasm/revcomp/revcomp.python3-3.python3.wasm 1000 < ../pybenchmarks/bencher/data/revcomp-input1000.txt
# 生成火焰图
sudo perf script  | ./stackcollapse-perf.pl | ./flamegraph.pl > flamegraph-wasmtime.svg
```

为了更好分析，我也对其他wasm runtime生成了火焰图

```Bash
# wasm3
sudo perf record -g /usr/local/bin/wasm3 ../targets_pywasm/revcomp/revcomp.python3-3.python3.wasm 1000 < ../pybenchmarks/bencher/data/revcomp-input1000.txt
sudo perf script  | ./stackcollapse-perf.pl | ./flamegraph.pl > flamegraph-wasm3.svg
# wamr
sudo perf record -g /usr/local/bin/iwasm ../targets_pywasm/revcomp/revcomp.python3-3.python3.wasm 1000 < ../pybenchmarks/bencher/data/revcomp-input1000.txt
sudo perf script  | ./stackcollapse-perf.pl | ./flamegraph.pl > flamegraph-iwasm.svg
```

-g 参数用于指定生成调用图，而实际上有多种生成的方式。

[perf学习笔记](https://oiv4vv80gv6.feishu.cn/docx/D4sGd2D0oo0SN0xJ3RvcCzKvnBf)  其他一些事项可以看该文档。

**最终的分析结果是wasmtime并没有运行时性能问题**。之所以在差分分析计算出其延迟了一些，是因为revcomp这里用例比较特殊，其代码执行时间极短，只有0.3s左右，而python程序转化为的wasm都特别大，wasmtime有**缓存**机制，简单来说就是使用过的wasm程序会缓存进内存，为了确保可以知道其更新，会对wasm文件计算sha256,由于wasm比较大计算sha256会占用一些时间，这对0.3s的执行时间有比较明显的影响。