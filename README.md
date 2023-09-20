### deeplearning-deploy-pipeline

* 数据：采用libsvm格式，使用Dataset API，支持 parallel and prefetch读取
* 模型：使用Estimator进行算法封装，增加新算法仅需改写model_fn部分
* 训练：支持单机多线程、分布式训练
* 服务：支持模型导出，使用TensorFlow Serving或onnxruntime提供线上预测服务

## 如何使用
特征处理、模型训练以及模型服务相关脚本在根目录ctr目录下
pipline: feature → model → serving

## 特征框架

实验数据集用criteo
连续特征处理

    --不做embedding
      |1、concat[continuous, emb_vec]做fc
    --做embedding
      |2、离散化之后embedding
      |3、与FM二阶部分类似, 统一做embedding, <id, val> 离散特征val=1.0

    python3 ./ctr/feature/get_criteo_feature.py --input_dir=${data_dir_raw} --output_dir=${data_dir_processed} --cutoff=200

以下用DeepFM为例

``train``:

    python3 ./ctr/model/DeepFM.py --learning_rate=0.0001 --optimizer=Adam --num_epochs=1 --embedding_size=32 --batch_size=256 --field_size=39 --feature_size=117581 --deep_layers=400,400,400 --dropout=0.5,0.5,0.5 --l2_reg=0.0001 --log_steps=1000 --num_threads=8 --model_dir=${model_dir_ckpt}/DeepFM/ --data_dir=${data_dir_processed}
    
``模型导出 checkpoint -> pb``

    python3 ./ctr/model/DeepFM.py --task_type=export --learning_rate=0.0005 --optimizer=Adam --batch_size=256 --field_size=39 --feature_size=117581 --deep_layers=400,400,400 --dropout=0.5,0.5,0.5 --log_steps=1000 --num_threads=8 --model_dir=${model_dir_ckpt}/DeepFM/ --servable_model_dir=${model_dir_pb}
    
``模型转换 pb -> onnx``


    python3 -m tf2onnx.convert --saved-model ${model_dir_pb}/1694745305 --output ${model_dir_onnx}/1694745305/model.onnx --opset 13

### 服务框架 -- request in，pctr out
方式1、线上预测服务使用TensorFlow Serving+TAF搭建。使用 gRPC 作为接口接受外部调用，它支持模型热更新与自动模型版本管理。
``1、导出TF-Serving能识别的模型文件``

     python3 ./ctr/model/DeepFM.py --task_type=export --learning_rate=0.0005 --optimizer=Adam --batch_size=256 --field_size=39 --feature_size=117581 --deep_layers=400,400,400 --dropout=0.5,0.5,0.5 --log_steps=1000 --num_threads=8 --model_dir=${model_dir_ckpt}/DeepFM/ --servable_model_dir=${model_dir_pb}

``默认以时间戳来管理版本，生成文件如下``

      $ ls -lh servable_model/161793023
      |--saved_model.pb
      |--variables
        |--variables.data-00000-of-00001
        |--variables.index

``2、写client发送请求，参考ctr目录下server``

方式2、线上预测服务使用onnxruntime进行搭建。
1）导出TF-Serving能识别的模型文件：

     python3 ./ctr/model/DeepFM.py --task_type=export --learning_rate=0.0005 --optimizer=Adam --batch_size=256 --field_size=39 --feature_size=117581 --deep_layers=400,400,400 --dropout=0.5,0.5,0.5 --log_steps=1000 --num_threads=8 --model_dir=${model_dir_ckpt}/DeepFM/ --servable_model_dir=${model_dir_pb}
     
``onnxruntime模型推理``

    python3 verification_onnx.py
