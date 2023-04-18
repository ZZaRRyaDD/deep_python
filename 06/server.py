import argparse
import socket

HOST = "127.0.0.1"
PORT = 65432


def main():
    parser = argparse.ArgumentParser(
        description="Сбор параметров для сервера",
    )
    parser.add_argument(
        "workers",
        type=int,
        help="Количество воркеров",
    )
    parser.add_argument(
        "count_words",
        type=int,
        help="Количество слов",
    )
    args = parser.parse_args()
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        conn, addr = s.accept()
        with conn:
            print(f"Connected by {addr}")
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                conn.sendall(data)


if __name__ == "__main__":
    main()
