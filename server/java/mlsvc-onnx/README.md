## 打包方法
> 需要实现安装java，要求java8以上，并设置PATH、JAVA_HOME环境变量
```shell
# 无需单独安装maven，使用mvnw即可
./mvnw clean package -Dmaven.test.skip=true
```

## 配置属性
> 可以通过环境变量或者application.properties文件配置
```yaml
reactor:
  netty:
    io-select-count: 1   // io selector num
    io-worker-count: 4   // io worker num

onnxruntime:
  inter-op-num-threads: 4 // onnxruntime inter op num threads
```

## 执行方法
```shell
# 通过环境变量设置需要加载的模型路径
export ENV_TEST_MODEL_PATH=/workspaces/mlsvc-onnx/models/cnn_mnist_pytorch.onnx
java -jar target mlsvc-onnx-0.0.1.jar
```

## REST接口
> 具体可参考rest.http文件
```shell
curl -X POST http://127.0.0.1:8080/model/onnx/infer -d {"feat_ids":[1,2,3...],"feat_vals":[1,2,3..],"shape":[1,2]}
```

## GRPC接口
TODO