import socket


def get_unused_data():
    socket_ = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket_.bind(('localhost', 0))
    host, port = socket_.getsockname()
    socket_.close()
    return host, port
