#### 基础环境安装
1. Boost.Asio

   `sudo apt update && sudo apt install libboost-all-dev`

2. 编译

    2.1 服务端

    `g++ server.cc -o server ../onnxruntime/build/Linux/Release/libonnxruntime.so.1.10.0 -I../onnxruntime/include/ -std=c++11`

    2.2 客户端

