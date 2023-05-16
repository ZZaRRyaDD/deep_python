import argparse
from io import TextIOWrapper
import json
import socket
import threading

HOST = "localhost"
PORT = 8080
TIMEOUT = 20
DEFAULT_ENCODING = "utf-8"


def client_sender(
    lock: threading.Lock,
    host: str,
    port: int,
    file: TextIOWrapper,
    timeout: int = TIMEOUT,
) -> None:
    while True:
        try:
            with lock:
                url = file.readline()
            if not url:
                break
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
                client.connect((host, port))
                client.settimeout(timeout)
                client.sendall(url.encode(DEFAULT_ENCODING))
                data = client.recv(8192)
                print(f"{url}: {json.loads(data.decode(DEFAULT_ENCODING))}\n")
        except TimeoutError:
            break
        except Exception:
            pass


def client_starter(
    threads: int,
    path: str,
    host: str = HOST,
    port: int = PORT,
) -> None:
    lock = threading.Lock()
    with open(path, "r", encoding="utf-8") as file:
        threads = [
            threading.Thread(
                target=client_sender,
                name=f"client_thread_{i}",
                args=(lock, host, port, file),
            )
            for i in range(threads)
        ]
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()


def main() -> None:
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
    client_starter(args.threads, args.path)


if __name__ == "__main__":
    main()
