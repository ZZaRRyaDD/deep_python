import argparse
import json
import socket
import threading
import queue
from collections import Counter
from urllib import request, error

HOST = "localhost"
PORT = 8080
DEFAULT_ENCODING = "utf-8"
COUNT_COMPUTED_URLS = 0
TIMEOUT = 20


def handle_url(url: str, most_common: int) -> dict:
    try:
        html_body = request.urlopen(url, timeout=5)
    except TimeoutError:
        return {}
    except error.URLError:
        return {}
    data = html_body.read().decode()
    for symbol in ["\n", "\\", "<", ">"]:
        data = data.replace(symbol, "")
    data = data.split()
    return dict(Counter(data).most_common(most_common))


def worker_thread(
    count_words: int,
    in_queue: queue.Queue,
    out_queue: queue.Queue,
    timeout: int,
) -> None:
    while True:
        try:
            url = in_queue.get(timeout=timeout)
            if not url:
                break
            top_words = handle_url(
                url.decode(DEFAULT_ENCODING),
                count_words,
            )
            global COUNT_COMPUTED_URLS
            COUNT_COMPUTED_URLS += 1
            out_queue.put(str(json.dumps(top_words)).encode(DEFAULT_ENCODING))
            print(COUNT_COMPUTED_URLS)
        except queue.Empty:
            break


def master_thread(
    workers: int,
    count_words: int,
    host: str,
    port: int,
    timeout: int = TIMEOUT,
) -> None:
    in_queue = queue.Queue()
    out_queue = queue.Queue()
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.settimeout(timeout)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((host, port))
        server.listen(5)
        threads = [
            threading.Thread(
                target=worker_thread,
                name=f"worker_thread_{i}",
                args=(count_words, in_queue, out_queue, timeout),
            )
            for i in range(workers)
        ]
        for thread in threads:
            thread.start()
        while True:
            try:
                conn, _ = server.accept()
                with conn:
                    data = conn.recv(8192)
                    in_queue.put(data)
                    result = out_queue.get()
                    conn.sendall(result)
            except TimeoutError:
                break
        for thread in threads:
            thread.join()


def server_starter(
    workers: int,
    count_words: int,
    host: str = HOST,
    port: int = PORT,
) -> None:
    master = threading.Thread(
        target=master_thread,
        name="master_thread",
        args=(workers, count_words, host, port),
    )
    master.start()
    master.join()


def main() -> None:
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
    server_starter(args.workers, args.count_words)


if __name__ == "__main__":
    main()
