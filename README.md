### deeplearning-deploy-pipeline

* 读数据采用Dataset API，支持 parallel and prefetch读取
* 通过Estimator封装算法f(x)，实验新算法边际成本比较低，只需要改写model_fn f(x)部分
* 支持分布式以及单机多线程训练
* 支持export model，然后用TensorFlow Serving提供线上预测服务

## How to use
pipline: feature → model → serving

## 特征框架 -- logs in，samples out
实验数据集用criteo，特征工程参考
连续特征处理
    --不做embedding
      |1--concat[continuous, emb_vec]做fc
    --做embedding
      |2--离散化之后embedding
      |3--类似FM二阶部分, 统一做embedding, <id, val> 离散特征val=1.0

    python get_criteo_feature.py --input_dir=../../data/criteo/ --output_dir=../../data/criteo/ --cutoff=200

以DeepFM为例来看看如何使用：

``train``:

    python DeepFM.py --task_type=train --learning_rate=0.0005 --optimizer=Adam --num_epochs=1 --batch_size=256 --field_size=39 --feature_size=117581 --deep_layers=400,400,400 --dropout=0.5,0.5,0.5 --log_steps=1000 --num_threads=8 --model_dir=./model_ckpt/criteo/DeepFM/ --data_dir=../../data/criteo/

``infer``:

    python DeepFM.py --task_type=infer --learning_rate=0.0005 --optimizer=Adam --num_epochs=1 --batch_size=256 --field_size=39 --feature_size=117581 --deep_layers=400,400,400 --dropout=0.5,0.5,0.5 --log_steps=1000 --num_threads=8 --model_dir=./model_ckpt/criteo/DeepFM/ --data_dir=../../data/criteo/

### 服务框架 -- request in，pctr out
线上预测服务使用TensorFlow Serving+TAF搭建。TensorFlow Serving是一个用于机器学习模型 serving 的高性能开源库，使用 gRPC 作为接口接受外部调用，它支持模型热更新与自动模型版本管理。
首先要导出TF-Serving能识别的模型文件：

    python DeepFM.py --task_type=export --learning_rate=0.0005 --optimizer=Adam --batch_size=256 --field_size=39 --feature_size=117581 --deep_layers=400,400,400 --dropout=0.5,0.5,0.5 --log_steps=1000 --num_threads=8 --model_dir=./model_ckpt/criteo/DeepFM/ --servable_model_dir=./servable_model/


默认以时间戳来管理版本，生成文件如下：

      $ ls -lh servable_model/1517971230
      |--saved_model.pb
      |--variables
        |--variables.data-00000-of-00001
        |--variables.index

然后写client发送请求，参考Serving_pipeline
