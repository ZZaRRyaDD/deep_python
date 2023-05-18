import argparse
import json
import socket
import threading
import queue
from collections import Counter
from typing import Callable
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
    timeout: int,
    lock: threading.Lock,
    handler_func: Callable = handle_url,
) -> None:
    while True:
        try:
            connection = in_queue.get(timeout=timeout)
            if not connection:
                break
            with connection:
                url = connection.recv(8192)
                top_words = handler_func(
                    url.decode(DEFAULT_ENCODING),
                    count_words,
                )
                result = str(json.dumps(top_words)).encode(DEFAULT_ENCODING)
                connection.sendall(result)
                with lock:
                    global COUNT_COMPUTED_URLS
                    COUNT_COMPUTED_URLS += 1
                print(COUNT_COMPUTED_URLS)
        except TimeoutError:
            break
        except queue.Empty:
            break
        except Exception:
            pass


def master_thread(
    workers: int,
    count_words: int,
    host: str,
    port: int,
    timeout: int = TIMEOUT,
    handler_func: Callable = handle_url,
) -> None:
    in_queue = queue.Queue()
    lock = threading.Lock()
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.settimeout(timeout)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((host, port))
        server.listen(5)
        threads = [
            threading.Thread(
                target=worker_thread,
                name=f"worker_thread_{i}",
                args=(count_words, in_queue, timeout, lock),
                kwargs={"handler_func": handler_func},
            )
            for i in range(workers)
        ]
        for thread in threads:
            thread.start()
        while True:
            try:
                conn, _ = server.accept()
                in_queue.put(conn)
            except TimeoutError:
                break
        for thread in threads:
            thread.join()


def server_starter(
    workers: int,
    count_words: int,
    host: str = HOST,
    port: int = PORT,
    handler_func: Callable = handle_url,
) -> None:
    master = threading.Thread(
        target=master_thread,
        name="master_thread",
        args=(workers, count_words, host, port),
        kwargs={"handler_func": handler_func},
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
