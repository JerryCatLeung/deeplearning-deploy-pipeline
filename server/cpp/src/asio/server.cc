#include <boost/asio.hpp>
#include "../onnxruntime/include/onnxruntime/core/session/onnxruntime_cxx_api.h"
#include <thread>
#include <vector>
#include <iostream>
#include <ctime>
#include <nlohmann/json.hpp>

using boost::asio::ip::tcp;

const int maxs=10;

class Session {
public:
    Session(tcp::socket socket, Ort::Session& session) 
        : socket_(std::move(socket)), session_(session) {}

    void start() {
      // Use the ONNX Runtime session to run the model
      // ...

      // For simplicity, we just send a message back to the client
      // get request data from client
      std::vector<int64_t> input_node_dims = {35, 39};
      size_t input_tensor_size = 35 * 39;
      // get request data
      // Read the request from the client
      
      std::array<char, 100000> buf;
      boost::system::error_code error;
      size_t len = socket_.read_some(boost::asio::buffer(buf), error);
      std::string request(buf.data(), len);

      // Deserialize the JSON string into a map
      nlohmann::json j = nlohmann::json::parse(request);
      std::map<std::string, nlohmann::json> intput_data = j.get<std::map<std::string, nlohmann::json>>();

      // Extract the vectors from the map
      std::vector<int64_t> feat_ids_tensor_values = intput_data["feat_ids"].get<std::vector<int64_t>>();
      std::vector<float> feat_values_tensor_values = intput_data["feat_vals"].get<std::vector<float>>();

      auto start = std::chrono::steady_clock::now();
      // create input tensor object from data values
      auto memory_info = Ort::MemoryInfo::CreateCpu(OrtArenaAllocator, OrtMemTypeDefault);
      Ort::Value feat_ids_input_tensor = Ort::Value::CreateTensor<int64_t>(memory_info,
                                                                        feat_ids_tensor_values.data(), input_tensor_size,
                                                                        input_node_dims.data(), 2);
      Ort::Value feat_vals_input_tensor = Ort::Value::CreateTensor<float>(memory_info,
                                                                        feat_values_tensor_values.data(), input_tensor_size, 
                                                                        input_node_dims.data(), 2);
      // set input
      std::vector<Ort::Value> ort_inputs;
      ort_inputs.push_back(std::move(feat_ids_input_tensor));
      ort_inputs.push_back(std::move(feat_vals_input_tensor));

      // Run the model
      auto output_tensors = session_.Run(Ort::RunOptions{nullptr}, input_node_names_.data(), ort_inputs.data(), ort_inputs.size(), output_node_names_.data(), 1);

      // Get the output results
      float* floatarr = output_tensors[0].GetTensorMutableData<float>();
      auto end = std::chrono::steady_clock::now();
      std::cout << "the cost of time is " << std::chrono::duration_cast<std::chrono::microseconds>(end - start).count() << " um" << std::endl;
      std::string message = "Output: " + std::to_string(floatarr[0]) + " " + std::to_string(rand() % maxs);

      boost::asio::write(socket_, boost::asio::buffer(message));
    }

private:
    std::vector<const char*> input_node_names_ = {"feat_ids", "feat_vals"};
    std::vector<const char*> output_node_names_ = {"prob"};
    tcp::socket socket_;
    Ort::Session& session_;
};

class Server {
public:
    Server(boost::asio::io_service& io_service, short port, Ort::Session& session)
        : acceptor_(io_service, tcp::endpoint(tcp::v4(), port)), session_(session) {
        do_accept();
    }

private:
    void do_accept() {
        acceptor_.async_accept([this](boost::system::error_code ec, tcp::socket socket) {
            if (!ec) {
                std::make_shared<Session>(std::move(socket), session_)->start();
            }
            do_accept();
        });
    }

    tcp::acceptor acceptor_;
    Ort::Session& session_;
};

int main() {
    // Initialize the environment
    Ort::Env env(ORT_LOGGING_LEVEL_WARNING, "ModelService");

    // Initialize the ONNX Runtime session with a model
    Ort::SessionOptions session_options;
    session_options.SetInterOpNumThreads(6);
    session_options.SetGraphOptimizationLevel(GraphOptimizationLevel::ORT_ENABLE_EXTENDED);
    Ort::Session session(env, "../../model/model.onnx", session_options);

    std::cout << "Model initialized" << std::endl;

    boost::asio::io_service io_service;
    Server server(io_service, 12345, session);

    // Create a pool of threads to run all of the io_services.
    std::vector<std::shared_ptr<std::thread>> threads;
    for (std::size_t i = 0; i < std::thread::hardware_concurrency(); ++i) {
        threads.emplace_back(std::make_shared<std::thread>([&io_service]() { io_service.run(); }));
    }

    // Wait for all threads in the pool to exit.
    for (auto& t : threads) {
        t->join();
    }

    return 0;
}