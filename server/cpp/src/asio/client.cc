#include <boost/asio.hpp>
#include <iostream>

using boost::asio::ip::tcp;

int main() {
    try {
        boost::asio::io_service io_service;
        tcp::resolver resolver(io_service);
        tcp::resolver::query query("localhost", "12345");
        tcp::resolver::iterator endpoint_iterator = resolver.resolve(query);
        tcp::socket socket(io_service);
        boost::asio::connect(socket, endpoint_iterator);

        // Send a request to the server
        std::string request = "Run model";
        boost::asio::write(socket, boost::asio::buffer(request));

        // Receive the response from the server
        std::array<char, 1024> buf;
        boost::system::error_code error;

        size_t len = socket.read_some(boost::asio::buffer(buf), error);
        std::cout.write(buf.data(), len);
        std::cout << std::endl;

        //while (true) {
        //    size_t len = socket.read_some(boost::asio::buffer(buf), error);
        //    if (error) {
        //        if (error == boost::asio::error::eof) {
        //            break; // Connection closed cleanly by peer.
        //        } else {
        //            throw boost::system::system_error(error); // Some other error.
        //        }
        //    }
        //    std::cout.write(buf.data(), len);
    } catch (const boost::system::system_error& e) {
        std::cout << std::endl;
        std::cerr << "Error: " << e.what() << ", " << e.code() << std::endl;
    }

    return 0;
}