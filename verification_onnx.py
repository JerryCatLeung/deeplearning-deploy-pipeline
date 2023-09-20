import onnxruntime as ort
import numpy as np

sess = ort.InferenceSession("./model_onnx/model.onnx", providers=["CUDAExecutionProvider"])
feat_ids = np.asarray([[113995, 46083, 86323, 25806, 45678, 81769, 3948, 100714, 67679, 86021, 15761, 107961, 111813, 29150, 26991, 47468, 110431, 91142, 105117, 39091, 64180, 83621, 52327, 38212, 8810, 85661, 81799, 65109, 102601, 55306, 52315, 51648, 95763, 66291, 11107, 74377, 45597, 109698, 115471]], np.int64)
feat_vals = np.asarray([[1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]], np.float32)
results_ort = sess.run(["prob"], {"feat_ids": feat_ids, "feat_vals": feat_vals})
print(results_ort)