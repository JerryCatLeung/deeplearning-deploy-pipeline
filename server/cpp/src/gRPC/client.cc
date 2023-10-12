#include <grpcpp/grpcpp.h>
#include "model.grpc.pb.h"

using grpc::Channel;
using grpc::ClientContext;
using grpc::Status;
using model::ModelRequest;
using model::ModelReply;
using model::Model;

class ModelClient {
 public:
  ModelClient(std::shared_ptr<Channel> channel) : stub_(Model::NewStub(channel)) {}

  std::vector<float> RunModel(const std::vector<int64_t>& input1, const std::vector<float>& input2) {
    ModelRequest request;
    for (int64_t i : input1) {
      request.add_input1(i);
    }
    for (float i : input2) {
      request.add_input2(i);
    }

    ModelReply reply;
    ClientContext context;

    Status status = stub_->RunModel(&context, request, &reply);

    if (status.ok()) {
      return std::vector<float>(reply.output().begin(), reply.output().end());
    } else {
      std::cout << status.error_code() << ": " << status.error_message() << std::endl;
      return {};
    }
  }

 private:
  std::unique_ptr<Model::Stub> stub_;
};

int main(int argc, char** argv) {
  ModelClient model(grpc::CreateChannel("localhost:50051", grpc::InsecureChannelCredentials()));
  std::vector<int64_t> input1 = { /* your data here */ };
  std::vector<float> input2 = { /* your data here */ };
  std::vector<float> output = model.RunModel(input1, input2);
  for (float i : output) {
    std::cout << i << std::endl;
  }

  return 0;
}