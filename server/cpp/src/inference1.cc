#include <iostream>
#include <assert.h>
#include <vector>
#include "onnxruntime/include/onnxruntime/core/session/onnxruntime_cxx_api.h"


int main(){
    Ort::Env env(ORT_LOGGING_LEVEL_WARNING, "test");
    Ort::SessionOptions session_options;
    session_options.SetInterOpNumThreads(1);
    session_options.SetGraphOptimizationLevel(GraphOptimizationLevel::ORT_ENABLE_EXTENDED);
    const char* model_path = "model.onnx";

    Ort::Session session(env, model_path, session_options);
    Ort::AllocatorWithDefaultOptions allocator;
    size_t num_input_nodes = session.GetInputCount();
    std::cout << "This model inludes has " << num_input_nodes << " input nodes."<< std::endl;
    std::cout << session.GetInputName(0, allocator) << std::endl;
    std::cout << session.GetInputName(1, allocator) << std::endl;
    size_t num_output_nodes = session.GetOutputCount();
    std::cout << "This model inludes has " << num_output_nodes << " output nodes."<< std::endl;
    std::cout << session.GetOutputName(0, allocator) << std::endl;
    
    std::vector<const char*> input_node_names = {"feat_ids", "feat_vals"};
    std::vector<const char*> output_node_names = {"prob"};
    std::vector<int64_t> input_node_dims = {2, 39};
    size_t input_tensor_size = 2 * 39;
    // feat_ids node
    std::vector<int64_t> feat_ids_tensor_values{1, 46083, 86323, 25806, 45678, 81769, 3948, 100714, 67679, 86021, 15761, 107961, 111813, 29150, 26991, 47468, 110431, 91142, 105117, 39091, 64180, 83621, 52327, 38212, 8810, 85661, 81799, 65109, 102601, 55306, 52315, 51648, 95763, 66291, 11107, 74377, 45597, 109698, 115471, 113995, 46083, 86323, 25806, 45678, 81769, 3948, 100714, 67679, 86021, 15761, 107961, 111813, 29150, 26991, 47468, 110431, 91142, 105117, 39091, 64180, 83621, 52327, 38212, 8810, 85661, 81799, 65109, 102601, 55306, 52315, 51648, 95763, 66291, 11107, 74377, 45597, 109698, 115471};
    // feat_vals node
    std::vector<float> feat_values_tensor_values{1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0};
   
    // create input tensor object from data values
    auto memory_info = Ort::MemoryInfo::CreateCpu(OrtArenaAllocator, OrtMemTypeDefault);
    Ort::Value feat_ids_input_tensor = Ort::Value::CreateTensor<int64_t>(memory_info, feat_ids_tensor_values.data(), input_tensor_size, input_node_dims.data(), 2);
    Ort::Value feat_vals_input_tensor = Ort::Value::CreateTensor<float>(memory_info, feat_values_tensor_values.data(), input_tensor_size, input_node_dims.data(), 2);
    assert(feat_ids_input_tensor.IsTensor());
    assert(feat_vals_input_tensor.IsTensor());

    std::vector<Ort::Value> ort_inputs;
    ort_inputs.push_back(std::move(feat_ids_input_tensor));
    ort_inputs.push_back(std::move(feat_vals_input_tensor));

    // score model & input tensor, get back output tensor
    auto output_tensors = session.Run(Ort::RunOptions{nullptr}, input_node_names.data(), ort_inputs.data(), ort_inputs.size(), output_node_names.data(), 1);
    float* floatarr = output_tensors[0].GetTensorMutableData<float>();
    std::cout << *floatarr << std::endl;
    return 0;
}