import argparse
import json
import socket
import threading
import queue

HOST = "localhost"
PORT = 8080
TIMEOUT = 20
DEFAULT_ENCODING = "utf-8"


def client_sender(
    main_queue: queue.Queue,
    host: str,
    port: int,
    timeout: int = TIMEOUT,
) -> None:
    while True:
        try:
            url = main_queue.get(timeout=timeout)
            if not url:
                break
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
                client.connect((host, port))
                client.settimeout(timeout)
                client.sendall(url.encode(DEFAULT_ENCODING))
                data = client.recv(8192)
                print(f"{url}: {json.loads(data.decode(DEFAULT_ENCODING))}\n")
        except queue.Empty:
            break
        except TimeoutError:
            break


def client_starter(
    threads: int,
    path: str,
    host: str = HOST,
    port: int = PORT,
) -> None:
    main_queue = queue.Queue()
    threads = [
        threading.Thread(
            target=client_sender,
            name=f"thread_{i}",
            args=(main_queue, host, port),
        )
        for i in range(threads)
    ]
    for thread in threads:
        thread.start()
    with open(path, "r", encoding="utf-8") as file:
        while line := file.readline():
            main_queue.put(line.replace("\n", ""))
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
