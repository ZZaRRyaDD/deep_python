import argparse
from collections import Counter
import json
import socket
import threading
from urllib import request, error

HOST = "127.0.0.1"
PORT = 8080
DEFAULT_ENCODING = "utf-8"
COUNT_COMPUTED_URLS = 0


def handle_url(url: str, most_common: int):
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


def worker_thread(connect, count_words, sem):
    with connect, sem:
        data = connect.recv(8192)
        top_words = handle_url(
            data.decode(DEFAULT_ENCODING),
            count_words,
        )
        global COUNT_COMPUTED_URLS
        COUNT_COMPUTED_URLS += 1
        connect.sendall(str(json.dumps(top_words)).encode(DEFAULT_ENCODING))
        print(COUNT_COMPUTED_URLS)


def master_thread(workers, count_words):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.bind((HOST, PORT))
        server.listen(1)
        while True:
            conn, _ = server.accept()
            sem = threading.Semaphore(workers)
            thread = threading.Thread(
                target=worker_thread,
                name="worker_thread",
                args=(conn, count_words, sem),
            )
            thread.start()
            thread.join()


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
    master = threading.Thread(
        target=master_thread,
        name="master_thread",
        args=(args.workers, args.count_words),
    )
    master.start()
    master.join()


if __name__ == "__main__":
    main()
