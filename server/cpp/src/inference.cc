#include <iostream>
#include <assert.h>
#include <vector>
#include <onnxruntime_cxx_api.h>

int main(int argec, char* argv[]){
    Ort::Env env(ORT_LOGGING_LEVEL_WARNING, "test");
    Ort::SessionOptions session_options;
    session_options.SetInterOpNumThreads(1);
    session_options.SetGraphOptimizationLevel(GraphOptimizationLevel::ORT_ENABLE_EXTENDED);
    const char* model_path = "./model_onnx/model.onnx";

    Ort::Session session(env, model_path, session_options);
    Ort::AllocatorWithDefaultOptions allocator;
    size_t num_input_nodes = session.GetInputCount();
    std::cout << num_input_nodes;
    std::vector<const char*> input_node_names = {"input","input_mask"};
    std::vector<const char*> output_node_names = {"output","output_mask"};
    
    // std::vector<int64_t> input_node_dims = {10, 20};
    // size_t input_tensor_size = 10 * 20;
    // std::vector<float> input_tensor_values(input_tensor_size);
    // for (unsigned int i = 0; i < input_tensor_size; i++)
    //   input_tensor_values[i] = (float)i / (input_tensor_size + 1);
    // // create input tensor object from data values
    // auto memory_info = Ort::MemoryInfo::CreateCpu(OrtArenaAllocator, OrtMemTypeDefault);
    // Ort::Value input_tensor = Ort::Value::CreateTensor<float>(memory_info, input_tensor_values.data(), input_tensor_size, input_node_dims.data(), 2);
    // assert(input_tensor.IsTensor());

    // std::vector<int64_t> input_mask_node_dims = {1, 20, 4};
    // size_t input_mask_tensor_size = 1 * 20 * 4; 
    // std::vector<float> input_mask_tensor_values(input_mask_tensor_size);
    // for (unsigned int i = 0; i < input_mask_tensor_size; i++)
    //   input_mask_tensor_values[i] = (float)i / (input_mask_tensor_size + 1);
    // // create input tensor object from data values
    // auto mask_memory_info = Ort::MemoryInfo::CreateCpu(OrtArenaAllocator, OrtMemTypeDefault);
    // Ort::Value input_mask_tensor = Ort::Value::CreateTensor<float>(mask_memory_info, input_mask_tensor_values.data(), input_mask_tensor_size, input_mask_node_dims.data(), 3);
    // assert(input_mask_tensor.IsTensor());
    
    // std::vector<Ort::Value> ort_inputs;
    // ort_inputs.push_back(std::move(input_tensor));
    // ort_inputs.push_back(std::move(input_mask_tensor));
    // // score model & input tensor, get back output tensor
    // auto output_tensors = session.Run(Ort::RunOptions{nullptr}, input_node_names.data(), ort_inputs.data(), ort_inputs.size(), output_node_names.data(), 2);
  
    // // Get pointer to output tensor float values
    // float* floatarr = output_tensors[0].GetTensorMutableData<float>();
    // float* floatarr_mask = output_tensors[1].GetTensorMutableData<float>();
  
    return 0;
}