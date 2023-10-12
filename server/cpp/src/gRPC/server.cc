#include <grpcpp/grpcpp.h>
#include "model.grpc.pb.h"
#include "../onnxruntime/include/onnxruntime/core/session/onnxruntime_cxx_api.h"

using grpc::Server;
using grpc::ServerBuilder;
using grpc::ServerContext;
using grpc::Status;
using model::ModelRequest;
using model::ModelReply;
using model::Model;

class ModelServiceImpl final : public Model::Service {
  Ort::Env env;
  Ort::Session session;
public:
  ModelServiceImpl() : env(ORT_LOGGING_LEVEL_WARNING, "ModelService"), session(env, "../../model/model.onnx", Ort::SessionOptions()) {}

  Status RunModel(ServerContext* context, const ModelRequest* request, ModelReply* reply) override {
    std::vector<float> input_data(request->input().begin(), request->input().end());
    std::array<int64_t, 2> input_dims = {1, static_cast<int64_t>(input_data.size())};

    auto memory_info = Ort::MemoryInfo::CreateCpu(OrtArenaAllocator, OrtMemTypeDefault);
    Ort::Value input_tensor = Ort::Value::CreateTensor<float>(memory_info, input_data.data(), input_data.size(), input_dims.data(), input_dims.size());

    const char* input_names[] = {"input"};
    std::vector<Ort::Value> input_tensors = {std::move(input_tensor)};

    const char* output_names[] = {"output"};
    std::vector<Ort::Value> output_tensors;

    output_tensors = session.Run(Ort::RunOptions{nullptr}, input_names, input_tensors.data(), 1, output_names, 1);

    float* floatarr = output_tensors[0].GetTensorMutableData<float>();
    std::vector<int64_t> output_shape = output_tensors[0].GetTensorTypeAndShapeInfo().GetShape();

    int64_t total_size = 1;
    for (int64_t dim : output_shape) {
        total_size *= dim;
    }

    for (int64_t i = 0; i < total_size; ++i) {
        reply->add_output(floatarr[i]);
    }

    return Status::OK;
  }
};

void RunServer() {
  std::string server_address("0.0.0.0:50051");
  ModelServiceImpl service;

  ServerBuilder builder;
  builder.AddListeningPort(server_address, grpc::InsecureServerCredentials());
  builder.RegisterService(&service);
  std::unique_ptr<Server> server(builder.BuildAndStart());
  std::cout << "Server listening on " << server_address << std::endl;

  server->Wait();
}

int main(int argc, char** argv) {
  RunServer();
  return 0;
}