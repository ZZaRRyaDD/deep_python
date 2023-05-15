import socket

def get_unused_data():
    so = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    so.bind(('localhost', 0))
    host, port = so.getsockname()
    so.close()
    return host, port
