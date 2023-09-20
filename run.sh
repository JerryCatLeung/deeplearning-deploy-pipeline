model_dir_ckpt="./model_ckpt/criteo/"
model_dir_pb="./model_pb/"
model_dir_onnx="./model_onnx/"
data_dir_raw="./data/criteo/raw"
data_dir_processed="./data/criteo/processed"

# 以DeepFM为例
# 1.特征处理
python3 ./ctr/feature/get_criteo_feature.py --input_dir=${data_dir_raw} --output_dir=${data_dir_processed} --cutoff=200
# 2.模型训练
python3 ./ctr/model/DeepFM.py --learning_rate=0.0001 --optimizer=Adam --num_epochs=1 --embedding_size=32 --batch_size=256 --field_size=39 --feature_size=117581 --deep_layers=400,400,400 --dropout=0.5,0.5,0.5 --l2_reg=0.0001 --log_steps=1000 --num_threads=8 --model_dir=${model_dir_ckpt}/DeepFM/ --data_dir=${data_dir_processed}
# 3.模型导出 checkpoint -> pb
python3 ./ctr/model/DeepFM.py --task_type=export --learning_rate=0.0005 --optimizer=Adam --batch_size=256 --field_size=39 --feature_size=117581 --deep_layers=400,400,400 --dropout=0.5,0.5,0.5 --log_steps=1000 --num_threads=8 --model_dir=${model_dir_ckpt}/DeepFM/ --servable_model_dir=${model_dir_pb}
# 4.模型转换 pb -> onnx
python3 -m tf2onnx.convert --saved-model ${model_dir_pb}/1694745305 --output ${model_dir_onnx}/1694745305/model.onnx --opset 13
# 5.验证模型 onnx <-> pb
python3 verification_onnx.py
# 5.模型推理 onnxruntime
