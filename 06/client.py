import argparse
import socket

HOST = "127.0.0.1"
PORT = 65432


def main():
    parser = argparse.ArgumentParser(
        description="Сбор параметров для клиента",
    )
    parser.add_argument(
        "threads",
        type=int,
        help="Количество потоков",
    )
    parser.add_argument(
        "path",
        type=str,
        help="Путь к файлу",
    )
    args = parser.parse_args()
    urls = []
    with open(args.path, "r", encoding="utf-8") as file:
        urls = file.readlines()
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        s.sendall(b"Hello, world")
        data = s.recv(8192)


if __name__ == "__main__":
    main()
