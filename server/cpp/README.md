### 编译onnxruntime
1. 源码下载

`git clone --depth=1 --branch v1.10.0 git@github.com:microsoft/onnxruntime.git && cd onnxruntime && git submodule update --init --force --recursive`

2. 源码编译

`sudo apt-get update && sudo apt-get install -y build-essential cmake curl libcurl4-openssl-dev libssl-dev uuid-dev && chmod +777 build.sh && ./build.sh --skip_tests --config Release --build_shared_lib --parallel`

`若需配合cuda使用，在命令行末尾应添加 -cuda_home /usr/local/cuda-11.3 --cudnn_home /usr/local/cuda-11.3`

`编译完成后，生成的文件会保存在onnxruntime/build/Linux/Release目录下`

3. 指定查找共享库（动态链接库）地址

`echo 'export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/path/onnxruntime/build/Linux/Release' >> ~/.bashrc`

4. 编译测试文件

`g++ inference.cc -o inference onnxruntime/build/Linux/Release/libonnxruntime.so.1.10.0 -Ionnxruntime/include/ -std=c++11`