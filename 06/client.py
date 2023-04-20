import argparse
import json
import socket
import threading

HOST = "127.0.0.1"
PORT = 8080
DEFAULT_ENCODING = "utf-8"


def client_sender(file, lock):
    while True:
        with lock:
            url = file.readline().replace("\n", "")
            if not url:
                break
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
            client.connect((HOST, PORT))
            client.sendall(url.encode(DEFAULT_ENCODING))
            data = client.recv(8192)
            print(f"{url}: {json.loads(data.decode(DEFAULT_ENCODING))}\n")


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
    lock = threading.Lock()
    file = open(args.path, "r", encoding="utf-8")
    threads = [
        threading.Thread(
            target=client_sender,
            name=f"thread_{i}",
            args=(file, lock),
        )
        for i in range(args.threads)
    ]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    file.close()


if __name__ == "__main__":
    main()
